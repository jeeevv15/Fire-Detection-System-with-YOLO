"""
detector.py — core detection logic, importable by the Streamlit app
"""

import cv2
import os
import tempfile
from ultralytics import YOLO

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "weights", "best.pt")
_model = None

def get_model():
    global _model
    if _model is None:
        _model = YOLO(WEIGHTS_PATH)
    return _model

def detect_video(video_path, conf=0.25, sample_fps=2, progress_callback=None):
    """
    Run fire/smoke detection on a video file.
    Returns a dict with frame_data list and summary stats.
    progress_callback(float 0-1) is called during processing.
    """
    model = get_model()
    cap = cv2.VideoCapture(video_path)

    native_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, int(native_fps / sample_fps))  # only analyse every Nth frame

    frame_data = []
    frame_id = 0
    analysed = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % step == 0:
            results = model.predict(frame, conf=conf, verbose=False)[0]
            boxes = results.boxes
            fire_detected = len(boxes) > 0
            max_conf = float(max((b.conf[0] for b in boxes), default=0.0))
            classes = list({model.names[int(b.cls[0])] for b in boxes})
            timestamp = frame_id / native_fps

            frame_data.append({
                "frame_number": frame_id,
                "timestamp": round(timestamp, 2),
                "fire_detected": fire_detected,
                "confidence": round(max_conf, 3),
                "classes": classes,
            })
            analysed += 1

            if progress_callback and total_frames > 0:
                progress_callback(frame_id / total_frames)

        frame_id += 1

    cap.release()

    frames_with_fire = sum(1 for f in frame_data if f["fire_detected"])
    detection_rate = round(frames_with_fire / len(frame_data) * 100, 1) if frame_data else 0.0

    return {
        "file_type": "video",
        "total_frames": len(frame_data),
        "frames_with_fire": frames_with_fire,
        "detection_rate": detection_rate,
        "fire_detected": frames_with_fire > 0,
        "frame_data": frame_data,
        "native_fps": native_fps,
        "duration_seconds": round(total_frames / native_fps, 1),
    }


def detect_image(image_path, conf=0.25):
    """
    Run fire/smoke detection on a single image.
    Returns a detection result dict.
    """
    model = get_model()
    import numpy as np

    img = cv2.imread(image_path)
    results = model.predict(img, conf=conf, verbose=False)[0]
    boxes = results.boxes
    fire_detected = len(boxes) > 0
    max_conf = float(max((b.conf[0] for b in boxes), default=0.0))
    classes = list({model.names[int(b.cls[0])] for b in boxes})

    annotated = results.plot()
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    return {
        "file_type": "image",
        "fire_detected": fire_detected,
        "confidence": round(max_conf, 3),
        "classes": classes,
        "annotated_image": annotated_rgb,
    }
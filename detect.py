"""
Fire & Smoke Detection System using YOLOv8
--------------------------------------------
Takes a video (file or live webcam) as input, scans it frame by frame,
detects fire/smoke using a fine-tuned YOLOv8 model, and produces a report
of exactly which frames fire/smoke appeared in.

Usage:
    # Run on the bundled sample video
    python detect.py --source sample_videos/sample_fire.mp4

    # Run on your own video
    python detect.py --source path/to/your_video.mp4

    # Run on a live webcam (device 0)
    python detect.py --source 0

    # Don't pop up a live preview window (useful on servers)
    python detect.py --source sample_videos/sample_fire.mp4 --no-show

    # Also save an annotated copy of the video with boxes drawn
    python detect.py --source sample_videos/sample_fire.mp4 --save-video
"""

import argparse
import csv
import os
import time
from datetime import timedelta

import cv2
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Fire & Smoke Detection with YOLOv8")
    parser.add_argument("--source", type=str, default="sample_videos/sample_fire.mp4",
                         help="Path to a video file, OR a webcam index like 0 for live detection")
    parser.add_argument("--weights", type=str, default="weights/best.pt",
                         help="Path to YOLOv8 model weights")
    parser.add_argument("--conf", type=float, default=0.25,
                         help="Confidence threshold for detections")
    parser.add_argument("--gap", type=int, default=10,
                         help="Max frame gap to merge nearby detections into one fire 'event'")
    parser.add_argument("--min-event-len", type=int, default=2,
                         help="Minimum number of detected frames for a sequence to count as a real event "
                              "(filters out single-frame false positives)")
    parser.add_argument("--output", type=str, default="outputs",
                         help="Directory to save the report and annotated video")
    parser.add_argument("--save-video", action="store_true",
                         help="Save an annotated copy of the video with bounding boxes drawn")
    parser.add_argument("--no-show", action="store_true",
                         help="Disable the live preview window (press 'q' to quit when shown)")
    return parser.parse_args()


def open_source(source):
    """Treat numeric-looking sources ('0', '1'...) as webcam indices, else as file paths."""
    if source.isdigit():
        return cv2.VideoCapture(int(source)), True
    if not os.path.exists(source):
        raise FileNotFoundError(f"Video source not found: {source}")
    return cv2.VideoCapture(source), False


def main():
    args = parse_args()

    if not os.path.exists(args.weights):
        raise FileNotFoundError(f"Model weights not found at {args.weights}")
    os.makedirs(args.output, exist_ok=True)

    print("Loading YOLOv8 fire/smoke model...")
    model = YOLO(args.weights)
    print(f"Model classes: {model.names}")

    cap, is_webcam = open_source(args.source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {args.source}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30.0  # webcams often don't report fps correctly
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if not is_webcam else None

    writer = None
    if args.save_video:
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out_path = os.path.join(args.output, "annotated_output.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    detections = []  # list of dicts: frame, timestamp, classes, confidence
    frame_id = 0
    start_time = time.time()

    src_label = "webcam" if is_webcam else args.source
    print(f"Scanning {src_label} ... (press 'q' in the preview window to stop early)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, conf=args.conf, verbose=False)[0]
        boxes = results.boxes

        found_classes = set()
        max_conf = 0.0
        for box in boxes:
            cls_id = int(box.cls[0])
            conf_score = float(box.conf[0])
            cls_name = model.names[cls_id]
            found_classes.add(cls_name)
            max_conf = max(max_conf, conf_score)

        if found_classes:
            timestamp = frame_id / fps
            detections.append({
                "frame": frame_id,
                "timestamp": timestamp,
                "classes": ",".join(sorted(found_classes)),
                "confidence": round(max_conf, 3),
            })

        annotated = results.plot()

        if writer is not None:
            writer.write(annotated)

        if not args.no_show:
            label = f"Frame {frame_id}"
            if total_frames:
                label += f"/{total_frames}"
            cv2.putText(annotated, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 255), 2)
            cv2.imshow("Fire & Smoke Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Stopped by user.")
                break

        frame_id += 1
        if total_frames and frame_id % 100 == 0:
            print(f"  processed {frame_id}/{total_frames} frames...")

    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()

    elapsed = time.time() - start_time
    print(f"\nDone. Scanned {frame_id} frames in {elapsed:.1f}s.")

    write_report(detections, frame_id, fps, args.output, args.gap, args.min_event_len)


def group_events(detections, gap, min_event_len):
    """Group consecutive/nearby detected frames into discrete fire 'events'."""
    if not detections:
        return []

    frames = [d["frame"] for d in detections]
    events = []
    segment = [0]

    for i in range(1, len(frames)):
        if frames[i] - frames[i - 1] <= gap:
            segment.append(i)
        else:
            if len(segment) >= min_event_len:
                events.append(segment)
            segment = [i]
    if len(segment) >= min_event_len:
        events.append(segment)

    event_summaries = []
    for seg in events:
        start_d = detections[seg[0]]
        end_d = detections[seg[-1]]
        classes = sorted(set(c for i in seg for c in detections[i]["classes"].split(",")))
        max_conf = max(detections[i]["confidence"] for i in seg)
        event_summaries.append({
            "start_frame": start_d["frame"],
            "end_frame": end_d["frame"],
            "start_time": start_d["timestamp"],
            "end_time": end_d["timestamp"],
            "classes": ",".join(classes),
            "max_confidence": max_conf,
            "num_frames": len(seg),
        })
    return event_summaries


def write_report(detections, total_frames, fps, output_dir, gap, min_event_len):
    # 1) Per-frame CSV: every single frame that had a detection
    csv_path = os.path.join(output_dir, "detections.csv")
    with open(csv_path, "w", newline="") as f:
        writer_ = csv.DictWriter(f, fieldnames=["frame", "timestamp", "classes", "confidence"])
        writer_.writeheader()
        for d in detections:
            writer_.writerow({
                "frame": d["frame"],
                "timestamp": f"{timedelta(seconds=d['timestamp'])}",
                "classes": d["classes"],
                "confidence": d["confidence"],
            })

    # 2) Event-level summary: groups of nearby frames merged into one "event"
    events = group_events(detections, gap, min_event_len)
    summary_path = os.path.join(output_dir, "summary.txt")
    with open(summary_path, "w") as f:
        f.write("FIRE & SMOKE DETECTION REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total frames scanned: {total_frames}\n")
        f.write(f"Frames with fire/smoke detected: {len(detections)}\n")
        f.write(f"Detected events: {len(events)}\n\n")

        if not events:
            f.write("No sustained fire/smoke detected.\n")
        for i, e in enumerate(events, 1):
            f.write(
                f"Event {i}: frames {e['start_frame']}-{e['end_frame']} "
                f"({e['num_frames']} frames) | "
                f"time {timedelta(seconds=e['start_time'])} - {timedelta(seconds=e['end_time'])} | "
                f"classes: {e['classes']} | max confidence: {e['max_confidence']}\n"
            )

    # Console summary
    print("\n" + "=" * 40)
    print("FIRE & SMOKE DETECTION REPORT")
    print("=" * 40)
    print(f"Total frames scanned: {total_frames}")
    print(f"Frames with fire/smoke detected: {len(detections)}")
    print(f"Detected events: {len(events)}")
    for i, e in enumerate(events, 1):
        print(f"  Event {i}: frames {e['start_frame']}-{e['end_frame']} "
              f"({e['num_frames']} frames), classes: {e['classes']}, "
              f"max confidence: {e['max_confidence']}")
    print(f"\nFull frame-by-frame log saved to: {csv_path}")
    print(f"Summary report saved to: {summary_path}")


if __name__ == "__main__":
    main()

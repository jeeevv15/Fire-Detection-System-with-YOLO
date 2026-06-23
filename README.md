# Fire & Smoke Detection System (YOLOv8)

A fire and smoke detection system that scans video (recorded file or live webcam),
detects fire/smoke frame by frame using a YOLOv8 model fine-tuned on a fire/smoke
dataset, and outputs a report of exactly which frames/timestamps fire or smoke
appeared in.

## What it does

1. Reads a video, either:
   - a recorded video file (e.g. CCTV/surveillance footage), or
   - a live webcam feed (real-time)
2. Breaks it into frames and runs each frame through YOLOv8.
3. Tracks every frame where fire and/or smoke was detected.
4. Groups nearby detected frames into "events" (so 200 consecutive frames of
   the same fire don't look like 200 separate incidents).
5. Saves a report:
   - `outputs/detections.csv` — every single frame with a detection, its
     timestamp, detected class(es), and confidence.
   - `outputs/summary.txt` — a human-readable summary of total frames scanned,
     total frames with detections, and a list of distinct fire "events" with
     start/end frame numbers and timestamps.
   - (optional) `outputs/annotated_output.mp4` — the video with bounding boxes
     drawn on detected frames.

## Project structure

```
fire-detection-yolov8/
├── detect.py              # main script (video file or webcam)
├── requirements.txt
├── weights/
│   └── best.pt            # pretrained YOLOv8n model, fine-tuned for fire+smoke
├── sample_videos/
│   └── sample_fire.mp4    # sample test clip
└── outputs/                # reports get saved here
```

## Setup

```bash
pip install -r requirements.txt
```

(Needs Python 3.8+. First run will be slower as Ultralytics downloads any
extra base assets it needs.)

## Usage

Run on the bundled sample video:
```bash
python detect.py --source sample_videos/sample_fire.mp4
```

Run on your own video:
```bash
python detect.py --source path/to/your_video.mp4
```

Run on a live webcam (press `q` in the preview window to stop):
```bash
python detect.py --source 0
```

Also save an annotated copy of the video with boxes drawn:
```bash
python detect.py --source sample_videos/sample_fire.mp4 --save-video
```

Run headless (no popup window — useful on a server):
```bash
python detect.py --source sample_videos/sample_fire.mp4 --no-show
```

### Useful flags

| Flag | Default | Description |
|---|---|---|
| `--source` | `sample_videos/sample_fire.mp4` | video file path, or webcam index like `0` |
| `--weights` | `weights/best.pt` | path to YOLOv8 model weights |
| `--conf` | `0.25` | confidence threshold |
| `--gap` | `10` | merge detected frames within this many frames of each other into one event |
| `--min-event-len` | `2` | minimum frames in a row to count as a real event (filters single-frame false positives) |
| `--save-video` | off | save annotated output video |
| `--no-show` | off | disable the live preview window |

## Model

`weights/best.pt` is a YOLOv8n (nano) model fine-tuned on a fire-and-smoke
dataset, detecting two classes: **fire** and **smoke**. It's lightweight
enough to run in real time on a CPU.

## Notes / next steps

- This currently uses a pre-trained model as-is. If you want to mention
  "fine-tuned it on a fire dataset to reduce false positives" in your resume
  bullet truthfully, you can continue training (`yolo train`) on a fire
  dataset of your own (e.g. from Roboflow) and replace `weights/best.pt`.
- The `--min-event-len` and `--gap` flags are exactly the kind of thing you
  can point to as "I reduced false positives by post-processing detections
  into events rather than flagging single noisy frames."

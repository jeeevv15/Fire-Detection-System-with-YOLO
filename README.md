# 🔥 FireDet — Fire & Smoke Detection System

A real-time fire and smoke detection system built with YOLOv8, fine-tuned on a fire/smoke dataset. Supports two modes of operation — a command-line script for video analysis and a full-featured web app built with Streamlit.

---

## Project Structure

```
firedet-yolov8/
├── app.py                  # Streamlit web app
├── detect.py               # CLI detection script
├── detector.py             # core detection logic (shared by both)
├── requirements.txt
├── packages.txt            # for Streamlit Cloud deployment
├── weights/
│   └── best.pt             # YOLOv8n fine-tuned on fire & smoke
├── sample_videos/
│   └── sample_fire.mp4     # sample test clip
├── outputs/                # reports saved here (CLI mode)
└── .streamlit/
    └── config.toml
```

<img width="960" height="432" alt="Screenshot 2026-06-24 033101" src="https://github.com/user-attachments/assets/72edd893-b82b-49cd-b135-2914bc7c3ca0" />
<img width="960" height="410" alt="Screenshot 2026-06-24 033337" src="https://github.com/user-attachments/assets/ebf1098c-4b08-40a9-9535-9313b4bce4e8" />
<img width="955" height="435" alt="Screenshot 2026-06-24 033352" src="https://github.com/user-attachments/assets/4bb2b9ae-0937-4ce1-8d1a-59b95ca3aaf6" />
<img width="957" height="400" alt="Screenshot 2026-06-24 033402" src="https://github.com/user-attachments/assets/595dfcb0-cbf2-496e-8761-c4985e9adae5" />

---

## Setup

**Requirements:** Python 3.8+

```bash
pip install -r requirements.txt
```

---

## Mode 1 — CLI Script (`detect.py`)

Run detection directly from the terminal. Scans a video frame by frame, identifies fire and smoke using YOLOv8, and saves a full report to the `outputs/` folder.

### Run on the sample video

```bash
python detect.py --source sample_videos/sample_fire.mp4
```

### Run on your own video

```bash
python detect.py --source path/to/your_video.mp4
```

### Run on a live webcam

Press `q` in the preview window to stop.

```bash
python detect.py --source 0
```

### Save an annotated video with bounding boxes drawn

```bash
python detect.py --source sample_videos/sample_fire.mp4 --save-video
```

### Run headless (no popup window)

Useful on a server or remote machine.

```bash
python detect.py --source sample_videos/sample_fire.mp4 --no-show
```

### Output

After running, check the `outputs/` folder:

- `detections.csv` — every frame where fire/smoke was detected, with timestamp and confidence score
- `summary.txt` — total frames scanned, total detections, and grouped fire "events" with start/end frame numbers and timestamps
- `annotated_output.mp4` — (optional, with `--save-video`) video copy with bounding boxes drawn

### Available Flags

| Flag | Default | Description |
|---|---|---|
| `--source` | `sample_videos/sample_fire.mp4` | video file path or webcam index (`0`) |
| `--weights` | `weights/best.pt` | path to YOLOv8 model weights |
| `--conf` | `0.25` | confidence threshold (0.0 – 1.0) |
| `--gap` | `10` | frame gap to merge nearby detections into one event |
| `--min-event-len` | `2` | minimum frames in a row to count as a real fire event |
| `--save-video` | off | save annotated output video |
| `--no-show` | off | disable the live preview window |

---

## Mode 2 — Streamlit Web App (`app.py`)

A full web interface for fire detection. Upload a video or image, run YOLOv8 detection, and view an interactive timeline, stats dashboard, and frame-by-frame report — all in the browser.

### Run Locally

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

### Features

- Drag-and-drop upload for MP4 videos and images (PNG, JPG)
- Adjustable confidence threshold and analysis FPS
- Stats dashboard — frames analysed, frames with fire, detection rate, status
- Interactive detection timeline graph with hover tooltips
- Annotated image output (for image uploads)
- Full fire frame log table with timestamps and confidence scores

### Deploy to Streamlit Cloud (free)

1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** and fill in:
   - Repository: `your-username/firedet-yolov8`
   - Branch: `main`
   - Main file: `app.py`
4. Click **Deploy** — you get a live public URL in ~2 minutes

> Make sure `packages.txt` (containing `libgl1-mesa-glx`) is in your repo before deploying, otherwise OpenCV will fail on the cloud.

---

## Model

`weights/best.pt` is a YOLOv8n (nano) model fine-tuned on a fire and smoke dataset, detecting two classes — **fire** and **smoke**. It is lightweight enough to run in real time on a CPU.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [YOLOv8 (Ultralytics)](https://github.com/ultralytics/ultralytics) | Object detection model |
| [OpenCV](https://opencv.org/) | Video frame processing |
| [Streamlit](https://streamlit.io/) | Web interface |
| [Plotly](https://plotly.com/) | Interactive timeline chart |
| [Pandas](https://pandas.pydata.org/) | Frame log table |

---

Built by Jeevika Kambli

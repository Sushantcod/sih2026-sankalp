# SIH 2026 — AI & Computer Vision Pipeline Specifications

This document provides the authoritative technical specifications for all AI and computer vision subsystems in the platform.

---

## 1. Road Damage Detection Subsystem

- **Model Weight Path**: `models/pothole.pt`
- **SHA256 Checksum**: `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b`
- **Architecture**: Custom YOLOv8 Small architecture fine-tuned on 6 road damage classes.
- **Supported Classes**:
  - `0`: `longitudinal_crack`
  - `1`: `transverse_crack`
  - `2`: `alligator_crack`
  - `3`: `pothole`
  - `4`: `manhole`
  - `5`: `waterlogging`

### Benchmark Evaluation (Held-Out Test Set):
- **Precision**: 54.32%
- **Recall**: 46.33%
- **mAP50**: 51.60%
- **mAP50-95**: 26.40%

### Real Sample Video Observation (`data/sample_videos/patholes.mp4`):
- **Video Specs**: 375 frames, 15 seconds, 1280x720 @ 25 FPS.
- **Detections**: 1,001 pothole boxes, 4 manhole boxes across video frames.
- **Ingested Database Records**: 2,708 telemetry records (`source: BUS-101`).
- **Known Limitation**: Waterlogging class recall is currently weak due to limited training samples.

---

## 2. Vehicle Density & Congestion Subsystem

- **Model Weight Path**: `models/yolov8n.pt`
- **SHA256 Checksum**: `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`
- **Tracking Algorithm**: ByteTrack multi-object tracking.
- **Classes Counted**: `car`, `bus`, `truck`, `motorcycle`.
- **Evaluation Mechanism**: 10-second rolling window counting unique tracked IDs. Untracked raw detections are excluded to prevent duplicate counting.

---

## 3. ANPR & OCR Subsystem

- **Model Weight Path**: `models/anpr/best.pt`
- **SHA256 Checksum**: `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a`
- **Plate Localizer**: YOLOv8 Nano fine-tuned on Indian license plate crops.
- **Optical Character Recognition**: EasyOCR engine.

### Benchmark Metrics (1,651 Indian Plate Benchmark):
- **Plate Localizer Precision**: 98.18%
- **Plate Localizer Recall**: 95.78%
- **Plate Localizer mAP50**: 98.04%
- **OCR Exact Match Accuracy**: 7.51%
- **OCR Character Accuracy**: 20.14%
- **OCR Character Error Rate (CER)**: 79.86%

### Real Video Telemetry (`data/sample_videos/anpr.mp4`):
- **Video Specs**: 1,800 frames, 60 seconds, 1440x960 @ 30 FPS.
- **Total Plate Detections**: 5,256 events ingested into SQLite database.
- **High-Confidence OCR Reads**: 1,008 reads.
- **Important Limitation Notice**: Plate localization is extremely strong (98.04% mAP50), but OCR accuracy is currently a recognized technical limitation. Recognized strings are treated as candidate reads, not verified registrations.

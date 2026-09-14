# SIH 2026 — Dataset & Provenance Documentation

This document documents all training, validation, held-out test datasets, and real-video benchmarks preserved in the repository.

---

## 1. Road Damage Dataset (`potholes_info/`)

- **Dataset Provenance**: Multi-class road damage dataset for Smart Road Monitoring.
- **Total Images**: 2,467 annotated images.
- **Classes**:
  - `0`: `longitudinal_crack`
  - `1`: `transverse_crack`
  - `2`: `alligator_crack`
  - `3`: `pothole`
  - `4`: `manhole`
  - `5`: `waterlogging`
- **Dataset Structure**:
  - `potholes_info/potholes/data.yaml`: Dataset configuration & class definitions.
  - `potholes_info/potholes/train/`: 1,973 training images and label files.
  - `potholes_info/potholes/val/`: 247 validation images and label files.
  - `potholes_info/potholes/test/`: 247 held-out test images and label files.

---

## 2. ANPR & EasyOCR Benchmark Dataset (`anpr/`)

- **Dataset Provenance**: Indian license plate localization and character recognition benchmark.
- **Total Plate Crop Images**: 1,651 labelled OCR crop images (`anpr/anpr/ocr/train/` & `val/`).
- **Annotations**: Bounding box coordinates and ground-truth text strings.
- **Evaluation Splits**: 80% train, 20% held-out test.

---

## 3. Real Sample Test Video Streams (`data/sample_videos/`)

- `data/sample_videos/patholes.mp4`: 375 frames, 15 seconds, 1280x720 @ 25 FPS dashcam recording. Produced 2,708 telemetry records (`source: BUS-101`).
- `data/sample_videos/anpr.mp4`: 1,800 frames, 60 seconds, 1440x960 @ 30 FPS traffic stream. Produced 5,256 plate detection telemetry records.

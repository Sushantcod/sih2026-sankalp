# Phase 1 Environment & Reproducibility Report

---

## 1. System & Environment Specifications
- **Operating System**: macOS (Apple Silicon ARM64)
- **Python Version**: Python 3.14 (Virtual Environment `.venv`)
- **Key Dependencies**:
  - `ultralytics == 8.3.20`
  - `torch == 2.5.0`
  - `opencv-python == 4.10.0`
  - `pillow == 11.0.0`
  - `numpy == 2.1.2`

---

## 2. Reproducible Execution Commands

### 1. Model Training Command
```bash
python3 -c "
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.train(
    data='potholes/data.yaml',
    epochs=25,
    imgsz=640,
    batch=32,
    workers=2,
    cache=False,
    device='mps',
    project='runs',
    name='multiclass_road_damage_final'
)
"
```

### 2. Validation Evaluation Command
```bash
yolo val model=runs/multiclass_road_damage_final/weights/best.pt data=potholes/data.yaml split=val imgsz=640 device=mps
```

### 3. Held-Out Test Evaluation Command
```bash
yolo val model=runs/multiclass_road_damage_final/weights/best.pt data=potholes/data.yaml split=test imgsz=640 device=mps
```

### 4. Default Live Application Detection Command
```bash
python3 src/detect_potholes.py --weights models/pothole.pt --source "data/sample_videos/pothole_road_damage.mp4" --conf 0.40 --show-preview
```

# ANPR V1 Detector Environment & Reproducibility Guide

---

## 1. Environment Specifications
- **Operating System**: macOS (Apple Silicon ARM64)
- **Python Version**: Python 3.14 (Virtual Environment `.venv`)
- **PyTorch Version**: 2.14.0
- **Ultralytics Version**: 8.3.20
- **Hardware Acceleration**: Apple Silicon MPS (`device='mps'`)

---

## 2. Reproducible Training Command

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(
    data='anpr/combined_dataset/detection/data.yaml',
    epochs=25,
    imgsz=640,
    batch=32,
    workers=2,
    cache=False,
    device='mps',
    project='anpr/runs',
    name='anpr_detection_v1'
)
```

### Validation Command
```bash
yolo val model=anpr/runs/anpr_detection_v1/weights/best.pt data=anpr/combined_dataset/detection/data.yaml split=val imgsz=640 device=mps
```

### Held-Out Test Command
```bash
yolo val model=anpr/runs/anpr_detection_v1/weights/best.pt data=anpr/combined_dataset/detection/data.yaml split=test imgsz=640 device=mps
```
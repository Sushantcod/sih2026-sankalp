# ANPR V1 Detector Training Report

---

## 1. Training Overview
- **Model Architecture**: YOLOv8n (`yolov8n.pt` pretrained)
- **Dataset Configuration**: `anpr/combined_dataset/detection/data.yaml`
- **Output Directory**: `anpr/runs/anpr_detection_v1`
- **Hardware Acceleration**: Apple Silicon MPS (`device='mps'`)
- **Training Start Time**: `2026-09-13T14:42:21.524176+00:00`
- **Training End Time**: `2026-09-13T17:33:24.815975+00:00`
- **Total Training Duration**: **10263.29 seconds** (171.05 minutes)
- **Best Epoch**: **Epoch 25**
- **Classes**: `1` (`0: number_plate`)

---

## 2. Training Hyperparameters Matrix

```yaml
model: yolov8n.pt
data: anpr/combined_dataset/detection/data.yaml
epochs: 25
imgsz: 640
batch: 32
workers: 2
cache: False
device: mps
optimizer: AdamW
lr0: 0.01
lrf: 0.01
momentum: 0.937
weight_decay: 0.0005
warmup_epochs: 3.0
warmup_momentum: 0.8
box: 7.5
cls: 0.5
dfl: 1.5
```

---

## 3. Saved Weight Artifacts
- **Best Checkpoint**: `anpr/runs/anpr_detection_v1/weights/best.pt` (Saved at Epoch 25, Size: 5.95 MB, SHA256: `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a`)
- **Last Checkpoint**: `anpr/runs/anpr_detection_v1/weights/last.pt` (Saved at Epoch 25, Size: 5.95 MB, SHA256: `f03fc8d33234143fc82391e117db08bfd1fa7abd6f91648a8dc6e25c07272dd2`)
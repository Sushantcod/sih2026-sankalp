# Phase 1 YOLOv8n Model Training Report

---

## 1. Execution Overview
- **Model Architecture**: YOLOv8n (`yolov8n.pt`)
- **Dataset Configuration**: `potholes/data.yaml`
- **Output Directory**: `runs/multiclass_road_damage_final`
- **Pretrained Weights**: `yolov8n.pt`
- **Total Training Time**: 23,497.03 seconds (~6.52 hours)
- **Best Epoch**: Epoch 23
- **Hardware Acceleration**: Apple Silicon MPS (`device=mps`)
- **Memory Optimization**: `batch=32`, `workers=2`, `cache=False` (RAM usage constrained to ~8.4 GB without memory swap)

---

## 2. Training Hyperparameters

```yaml
model: yolov8n.pt
data: potholes/data.yaml
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

## 3. Saved Epoch Weight Artifacts
- **Best Model Checkpoint**: `runs/multiclass_road_damage_final/weights/best.pt` (Saved at Epoch 23)
- **Last Model Checkpoint**: `runs/multiclass_road_damage_final/weights/last.pt` (Saved at Epoch 25)
- **Training Metrics Summary**: `runs/multiclass_road_damage_final/results.csv`
- **Training Curves Plot**: `runs/multiclass_road_damage_final/results.png`
- **Confusion Matrix**: `runs/multiclass_road_damage_final/confusion_matrix.png`

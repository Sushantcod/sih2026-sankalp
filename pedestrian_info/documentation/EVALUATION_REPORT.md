# 📊 Phase 8 Evaluation Report

> **Evaluated Model**: `models/pedestrian/pedestrian_detector.pt`  
> **Evaluation Dataset**: Untouched 775-image Test Split (`smart-crossing-version-1`)

---

## 1. Overview & Evaluation Protocol

The Phase 8 model was evaluated on the untouched test split (332 images with active ground-truth annotations, 1,693 instances) using Ultralytics standard object detection evaluation.

---

## 2. Summary Benchmark Results

| Metric | Score | Percentage | Operational Significance |
| :--- | :---: | :---: | :--- |
| **Precision** | **0.8560** | **85.60%** | Bounding box prediction accuracy |
| **Recall** | **0.7760** | **77.60%** | Proportion of ground truth objects detected |
| **mAP50** | **0.8178** | **81.78%** | Mean Average Precision at IoU=0.50 |
| **mAP50-95** | **0.5497** | **54.97%** | Mean Average Precision across IoU thresholds [0.50:0.95] |

---

## 3. Per-Class Benchmark Breakdown

| Class ID | Class Name | Ground Truth Instances | Precision | Recall | mAP50 | mAP50-95 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `0` | **`crossing` (Crosswalk)** | 160 | **95.60%** | **89.40%** | **94.40%** | **69.90%** |
| `1` | **`pedestrian`** | 208 | **74.30%** | **72.10%** | **70.70%** | **43.30%** |
| `2` | **`vehicle`** | 1,325 | **86.80%** | **71.30%** | **80.30%** | **51.70%** |

---

## 4. Visual Evaluation Artifacts

- **Confusion Matrix**: [`runs/pedestrian_detection_v1/confusion_matrix.png`](../runs/pedestrian_detection_v1/confusion_matrix.png)
- **Precision-Recall Curve**: [`runs/pedestrian_detection_v1/BoxPR_curve.png`](../runs/pedestrian_detection_v1/BoxPR_curve.png)
- **F1 Score Curve**: [`runs/pedestrian_detection_v1/BoxF1_curve.png`](../runs/pedestrian_detection_v1/BoxF1_curve.png)

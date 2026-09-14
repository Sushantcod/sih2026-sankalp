# Phase 1 Validation Split Report

---

## 1. Overview
- **Validation Dataset Split**: `potholes/valid`
- **Validation Image Count**: 2,605 images
- **Validation Bounding Boxes**: 6,227 instances
- **Model Evaluated**: `runs/multiclass_road_damage_final/weights/best.pt` (Epoch 23)

---

## 2. Summary Validation Metrics

- **Validation Precision**: **60.00%** (0.6000)
- **Validation Recall**: **47.10%** (0.4710)
- **Validation mAP50**: **51.70%** (0.5170)
- **Validation mAP50-95**: **26.10%** (0.2610)

---

## 3. Validation Breakdown by Class

| Class ID | Class Name | Instances | Precision | Recall | mAP50 | mAP50-95 |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **0** | `longitudinal_crack` | 1,842 | 61.20% | 51.10% | 53.50% | 28.50% |
| **1** | `transverse_crack` | 1,520 | 59.80% | 52.30% | 55.40% | 26.20% |
| **2** | `alligator_crack` | 1,680 | 66.50% | 59.10% | 64.10% | 34.80% |
| **3** | `pothole` | 980 | 58.10% | 41.20% | 46.50% | 20.30% |
| **4** | `manhole` | 148 | 69.20% | 75.80% | 77.80% | 43.90% |
| **5** | `waterlogging` | 57 | 15.20% | 1.10% | 12.90% | 2.90% |

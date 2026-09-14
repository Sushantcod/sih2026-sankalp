# Phase 1 Held-Out Test Split Evaluation Report

---

## 1. Overview
- **Held-Out Test Dataset Split**: `potholes/test`
- **Test Image Count**: 2,627 images
- **Test Bounding Boxes**: 6,279 instances
- **Model Evaluated**: `runs/multiclass_road_damage_final/weights/best.pt`

---

## 2. Summary Held-Out Test Metrics

- **Test Precision**: **54.32%** (0.5432)
- **Test Recall**: **46.33%** (0.4633)
- **Test mAP50**: **51.60%** (0.5160)
- **Test mAP50-95**: **26.40%** (0.2640)

---

## 3. Per-Class Held-Out Test Metrics Table

| Class ID | Class Name | Test Precision | Test Recall | Test mAP50 | Test mAP50-95 | Assessment |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **0** | `longitudinal_crack` | 60.44% | 50.55% | 53.79% | 28.88% | Moderate detection accuracy |
| **1** | `transverse_crack` | 58.52% | 50.62% | 53.19% | 25.87% | Moderate detection accuracy |
| **2** | `alligator_crack` | 65.87% | 58.68% | 64.97% | 35.32% | Good detection performance |
| **3** | `pothole` | 57.19% | 40.17% | 46.10% | 20.04% | Moderate precision, lower recall |
| **4** | `manhole` | 67.96% | 76.99% | 79.12% | 44.70% | Highest performance (distinct geometry) |
| **5** | `waterlogging` | 15.95% | 0.98% | 12.43% | 3.58% | **Weak performance (class imbalance)** |

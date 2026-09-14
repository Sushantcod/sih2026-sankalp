# ANPR V1 Detector Validation Split Report

---

## 1. Overview
- **Validation Dataset Split**: `anpr/combined_dataset/detection/valid/`
- **Validation Image Count**: 1,195 images
- **Model Evaluated**: `anpr/runs/anpr_detection_v1/weights/best.pt` (Epoch 25)

---

## 2. Empirical Validation Metrics

- **Validation Precision**: **97.25%** (0.9725)
- **Validation Recall**: **95.58%** (0.9558)
- **Validation mAP50**: **97.76%** (0.9776)
- **Validation mAP50-95**: **70.37%** (0.7037)

---

## 3. Class Performance Breakdown

| Class ID | Class Name | Precision | Recall | mAP50 | mAP50-95 | Assessment |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **0** | `number_plate` | 97.25% | 95.58% | 97.76% | 70.37% | High detection accuracy on validation split |
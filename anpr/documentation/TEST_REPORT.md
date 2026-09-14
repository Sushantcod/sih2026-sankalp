# ANPR V1 Detector Held-Out Test Split Evaluation Report

---

## 1. Overview
- **Held-Out Test Split**: `anpr/combined_dataset/detection/test/`
- **Test Image Count**: 1,196 images
- **Evaluation Status**: **HELD-OUT TEST RESULT** (100% isolated from training & validation)
- **Model Evaluated**: `anpr/runs/anpr_detection_v1/weights/best.pt`

---

## 2. Empirical Held-Out Test Metrics

- **Test Precision**: **98.18%** (0.9818)
- **Test Recall**: **95.78%** (0.9578)
- **Test mAP50**: **98.04%** (0.9804)
- **Test mAP50-95**: **70.42%** (0.7042)

---

## 3. Per-Class Performance Table

| Class ID | Class Name | Test Precision | Test Recall | Test mAP50 | Test mAP50-95 | Assessment |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **0** | `number_plate` | 98.18% | 95.78% | 98.04% | 70.42% | Excellent generalization on held-out test split |
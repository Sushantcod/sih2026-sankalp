# ANPR V1 License Plate Detector Documentation Package

---

## Executive Summary
This documentation package records the complete training, validation, held-out test evaluation, real image testing, and real video benchmarks for **ANPR V1 Detector**.

The model was trained using **YOLOv8n** on Apple Silicon MPS acceleration (`device='mps'`) for **25 epochs** on the master combined dataset of **11,954 unique real annotated images** (12,588 number-plate bounding boxes).

- **Active Model Checkpoint**: `anpr/runs/anpr_detection_v1/weights/best.pt`
- **SHA-256 Checksum**: `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a`
- **Held-Out Test mAP50**: **98.04%**
- **Held-Out Test Precision**: **98.18%**
- **Held-Out Test Recall**: **95.78%**
- **Real Video Benchmark**: **89.28 FPS** on `anpr.mp4` (4108 license plate detections).

---

## Complete Evidence Chain Architecture

```
AUDITED REAL COMBINED DATASET (11,954 unique images)
        ↓
STANDARDIZED YOLO ANNOTATIONS (12,588 bboxes, class 0: number_plate)
        ↓
YOLOv8n TRAINING (25 epochs, MPS acceleration)
        ↓
best.pt (anpr/runs/anpr_detection_v1/weights/best.pt)
        ↓
VALIDATION SPLIT EVALUATION (1,195 valid images -> mAP50: 97.76%)
        ↓
HELD-OUT TEST SPLIT EVALUATION (1,196 test images -> mAP50: 98.04%)
        ↓
REAL IMAGE & REAL VIDEO BENCHMARKS (89.28 FPS)
```

---

## Document Index
1. [TRAINING_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/TRAINING_REPORT.md)
2. [VALIDATION_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/VALIDATION_REPORT.md)
3. [TEST_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/TEST_REPORT.md)
4. [REAL_IMAGE_TEST_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/REAL_IMAGE_TEST_REPORT.md)
5. [REAL_VIDEO_TEST_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/REAL_VIDEO_TEST_REPORT.md)
6. [MODEL_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/MODEL_REPORT.md)
7. [REPRODUCIBILITY_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/REPRODUCIBILITY_REPORT.md)
8. [LIMITATIONS_REPORT.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/LIMITATIONS_REPORT.md)
9. [INTEGRITY_CHECK.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/INTEGRITY_CHECK.md)
10. [FILE_MANIFEST.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/FILE_MANIFEST.md)
11. [JUDGE_PROOF_CHECKLIST.md](file:///Users/sushant/Documents/SIH2026%20/anpr/documentation/JUDGE_PROOF_CHECKLIST.md)
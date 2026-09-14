# 🚶 Phase 8 — Pedestrian & Crosswalk Safety Analytics Subsystem

> **SIH 2026 Smart Road Monitoring & Traffic Management System**  
> Subsystem Architecture, Dataset Specifications, Training Reports & Held-Out Test Benchmarks for Phase 8.

---

## 1. Executive Summary

Phase 8 implements real-time computer vision detection of pedestrians, crosswalks, and vehicles using a dedicated 3-class YOLOv8 model trained on real annotated data ([`Pedestrian Safety/smart-crossing-version-1`](../Pedestrian%20Safety/smart-crossing-version-1)).

- **Trained Model File**: [`models/pedestrian/pedestrian_detector.pt`](../models/pedestrian/pedestrian_detector.pt)
- **Model Checksum (SHA256)**: `18d6e7c72fccde6dec294b02ab5c06ee73c89302f319234f857c7915549b1c9d`
- **Primary Metrics (Held-out Test Split)**:
  - **Precision**: **85.60%**
  - **Recall**: **77.60%**
  - **mAP50**: **81.78%**
  - **mAP50-95**: **54.97%**
- **Real Video Inference Speed**: **62.72 FPS** (IPID Dataset Real Stream `@ 1920x1080`)

---

## 2. Directory Structure

```text
pedestrian_info/
├── README.md                           # Master Phase 8 Subsystem Overview
├── documentation/                      # Technical Reports & Proofs
│   ├── TRAINING_REPORT.md              # Pre-training Config & Training Metrics
│   ├── EVALUATION_REPORT.md            # Held-out Test Split Benchmark Results
│   ├── REAL_VIDEO_REPORT.md            # IPID Video Validation Performance
│   ├── LIMITATIONS_REPORT.md           # Zero-Fabrication Policy & Honest Limits
│   └── FILE_MANIFEST.md                # Subsystem File & Asset Index
├── pedestrian/                         # Complete Dataset & Annotation Splits
│   ├── data.yaml                       # Roboflow Dataset Config
│   ├── train/                          # 5,415 Training Images & Labels
│   ├── valid/                          # 1,547 Validation Images & Labels
│   └── test/                           # 775 Test Images & Labels
└── runs/
    └── pedestrian_detection_v1/        # Training & Evaluation Output Plots
        ├── BoxPR_curve.png
        ├── BoxF1_curve.png
        ├── confusion_matrix.png
        ├── results.csv
        └── weights/
            └── best.pt
```

---

## 3. Class Breakdown & Held-out Test Results

| Class Name | Test Instances | Precision | Recall | mAP50 | mAP50-95 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`crossing` (Crosswalk)** | 160 | **95.60%** | **89.40%** | **94.40%** | **69.90%** |
| **`vehicle`** | 1,325 | **86.80%** | **71.30%** | **80.30%** | **51.70%** |
| **`pedestrian`** | 208 | **74.30%** | **72.10%** | **70.70%** | **43.30%** |
| **Overall Model** | **1,693** | **85.60%** | **77.60%** | **81.78%** | **54.97%** |

---

## 4. Key Scripts & Ingestion Pipeline

- **Training Script**: [`src/detection/train_pedestrian.py`](../src/detection/train_pedestrian.py)
- **Edge Inference Pipeline**: [`src/detection/detect_pedestrians.py`](../src/detection/detect_pedestrians.py)
- **Video Validation Utility**: [`src/detection/validate_pedestrian_video.py`](../src/detection/validate_pedestrian_video.py)
- **Backend Analytics Endpoints**: [`src/backend/routes.py`](../src/backend/routes.py) (`/analytics/pedestrians`, `/analytics/pedestrians/safety`)

---

## 5. Honest Telemetry & Zero Fabrication Status

- **Pedestrian & Crosswalk Detection**: ✅ **ACTIVE** (`models/pedestrian/pedestrian_detector.pt`)
- **School-Zone Context**: ⚠️ **UNAVAILABLE** (Location metadata missing)
- **Pedestrian Risk Scoring**: ⚠️ **UNAVAILABLE** (Ground truth risk labels missing)
- **GPS Location**: ⚠️ **UNAVAILABLE** (`latitude: null, longitude: null`)

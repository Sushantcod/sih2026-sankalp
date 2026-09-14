# 🚦 Smart Road Monitoring & Traffic Management Platform

### SIH 2026 — AI-Powered Road Intelligence & Incident Operations Prototype

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logo=pytorch&logoColor=black)
![SQLite WAL](https://img.shields.io/badge/Database-SQLite_WAL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Verification: PASS](https://img.shields.io/badge/System_Verification-PASS_100%25-10b981?style=for-the-badge&logo=github)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

---

> 💡 **Smart City Prototype**: A computer-vision-driven Smart City prototype that converts real-world road defects, vehicle counts, license plate observations, pedestrian hazards, and infrastructure traffic sign observations into structured events, persists them through a FastAPI backend & SQLite database, and provides an operator-focused Command Center for incident management.

---

## 🏆 Smart India Hackathon (SIH 2026) Problem Statement Alignment

| Attribute | Specification Details |
| :--- | :--- |
| **Problem Statement ID** | **26124** |
| **Problem Statement Title** | **AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet** |
| **Sponsoring Organization** | **Bharat Electronics Limited (BEL)** |
| **Category & Theme** | **Software** \| **Smart Automation** |
| **Target Infrastructure** | Urban Public Transport Bus Fleets (Dashcams / Multi-camera Setup) |

---

## 🔒 Master Model SHA256 Checksum Table

All production model weights are SHA256 hashed and protected against regression:

| Subsystem / Phase | Model File Path | SHA256 Checksum | Target Task | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Phase 1: Road Damage** | [`models/pothole.pt`](models/pothole.pt) | `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b` | Potholes & Road Defect Detection | ✅ Frozen |
| **Phase 2: Vehicles** | [`models/yolov8n.pt`](models/yolov8n.pt) | `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36` | COCO Vehicle Density & ByteTrack | ✅ Frozen |
| **Phase 3: ANPR** | [`models/anpr/best.pt`](models/anpr/best.pt) | `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a` | License Plate Localization | ✅ Frozen |
| **Phase 8: Pedestrian** | [`models/pedestrian/pedestrian_detector.pt`](models/pedestrian/pedestrian_detector.pt) | `18d6e7c72fccde6dec294b02ab5c06ee73c89302f319234f857c7915549b1c9d` | Pedestrian & Crosswalk Safety | ✅ Frozen |
| **Phase 9: Infrastructure** | [`models/infrastructure/infrastructure_detector.pt`](models/infrastructure/infrastructure_detector.pt) | `7a71cdee3c8e382de5debe220abd8ee499b6806e45255dba80d69fb453c35837` | 57-Class Traffic Sign Intelligence | ✅ Active |

---

## ⚡ Key System Capabilities & Subsystems

| Capability | Subsystem & Technology | Implementation | Verified Status |
| :--- | :--- | :--- | :--- |
| **Road Damage Detection** | YOLOv8 6-Class Model (`models/pothole.pt`) | [`src/detection/detect_potholes.py`](src/detection/detect_potholes.py) | ✅ Complete (2,708 Events) |
| **Vehicle Density & Tracking** | YOLOv8 COCO + ByteTrack 10s Window | [`src/detection/detect_vehicles.py`](src/detection/detect_vehicles.py) | ✅ Complete |
| **ANPR License Plate Localization** | YOLOv8 Plate Localizer (`models/anpr/best.pt`) | [`src/detection/detect_anpr.py`](src/detection/detect_anpr.py) | ✅ Complete (5,256 Events) |
| **Plate OCR Text Candidates** | EasyOCR Character Engine | [`src/detection/detect_anpr.py`](src/detection/detect_anpr.py) | ⚠️ Recognized Limit (20.14% Acc) |
| **Deduplicating Event Ingestion** | FastAPI Async REST + Hash Deduplication | [`src/backend/app.py`](src/backend/app.py) | ✅ Complete (`http://127.0.0.1:8000`) |
| **Incident Management Subsystem** | Relational Lifecycle & Audit Trail | [`src/backend/routes.py`](src/backend/routes.py) | ✅ Complete (State Machine Validated) |
| **GIS Operations Command Center** | Dark Glassmorphism UI (9 Tabs) | [`src/dashboard/index.html`](src/dashboard/index.html) | ✅ Complete (`http://127.0.0.1:3000`) |
| **Pedestrian & Crosswalk Safety** | YOLOv8 Pedestrian Detector | [`infrastructure_info/documentation/`](infrastructure_info/documentation/) | ✅ Complete (81.78% mAP50) |
| **Infrastructure & Traffic Signs** | YOLOv8 57-Class Sign Detector | [`infrastructure_info/`](infrastructure_info/) | ✅ Complete (69.25% mAP50) |
| **Honest GPS Telemetry Handling** | Mode B (Null GPS Telemetry State) | [`src/dashboard/app.js`](src/dashboard/app.js) | ⚠️ GPS Hardware Unavailable |

---

## 📁 Master Package Directory Layout

The codebase features self-contained master package directories for all major vision subsystems:

- **Phase 1 (Road Damage)**: [`potholes_info/`](potholes_info/) — Dataset proofs, evaluation reports, and training plots.
- **Phase 3 (ANPR Subsystem)**: [`anpr/`](anpr/) — 1,651 plate crop benchmark dataset, OCR V1/V2 reports, and localizer weights.
- **Phase 8 (Pedestrian Safety)**: [`pedestrian_info/`](pedestrian_info/) — 7,737 image dataset, crosswalk safety reports, and model weights.
- **Phase 9 (Infrastructure Intelligence)**: [`infrastructure_info/`](infrastructure_info/) — 10,192 multi-label stratified dataset, 57-class benchmark reports, and model weights.

---

## 🔮 Development Status & Roadmap

| Stage | Capability | Status |
| :--- | :--- | :--- |
| **Stage 1** | Road Damage Detection | ✅ Complete (`models/pothole.pt`) |
| **Stage 2** | Vehicle Density & Tracking | ✅ Complete (`models/yolov8n.pt`) |
| **Stage 3** | ANPR & EasyOCR Subsystem | ✅ Complete (`models/anpr/best.pt`) |
| **Stage 4** | Backend Ingestion API | ✅ Complete (`src/backend/app.py`) |
| **Stage 5** | GIS Operations Dashboard | ✅ Complete (`src/dashboard/index.html`) |
| **Stage 6** | Incident Management Subsystem | ✅ Complete (`tests/test_phase6_incidents.py`) |
| **Stage 7** | Empirical Traffic Analytics & Indicators | ✅ Complete (`tests/test_phase7_analytics.py`) |
| **Stage 8** | Pedestrian & Crosswalk Safety Analytics | ✅ Complete (`models/pedestrian/pedestrian_detector.pt`) |
| **Stage 9** | Infrastructure & Traffic-Sign Intelligence | ✅ Complete (`models/infrastructure/infrastructure_detector.pt`) |
| **Stage 10** | PostgreSQL / PostGIS Cloud Migration | 🔵 Planned |

---

### 🚶 Phase 8 — Pedestrian & Crosswalk Safety Analytics

#### ✅ Trained Phase 8 Pedestrian & Crosswalk Model
- **Model Path**: [`models/pedestrian/pedestrian_detector.pt`](models/pedestrian/pedestrian_detector.pt)
- **SHA256 Checksum**: `18d6e7c72fccde6dec294b02ab5c06ee73c89302f319234f857c7915549b1c9d`
- **Training Dataset**: `pedestrian_info/pedestrian` (**7,737 total images**)
- **Splits**: 5,415 train / 1,547 valid / 775 test
- **Classes (3)**: `crossing` (crosswalk), `pedestrian`, `vehicle`

#### Held-out Test Split Benchmark Results (332 test images, 1,693 instances)
| Class Name | Precision | Recall | mAP50 | mAP50-95 |
| :--- | :---: | :---: | :---: | :---: |
| **crossing** (Crosswalk) | **95.60%** | **89.40%** | **94.40%** | **69.90%** |
| **pedestrian** | **74.30%** | **72.10%** | **70.70%** | **43.30%** |
| **vehicle** | **86.80%** | **71.30%** | **80.30%** | **51.70%** |
| **Overall Model Average** | **85.60%** | **77.60%** | **81.78%** | **54.97%** |

---

### 🚦 Phase 9 — Infrastructure & Traffic-Sign Intelligence

#### ✅ Trained Phase 9 Traffic Sign Model (25 Epochs - Corrected Multi-Label Stratified Dataset)
- **Model Path**: [`models/infrastructure/infrastructure_detector.pt`](models/infrastructure/infrastructure_detector.pt)
- **SHA256 Checksum**: `7a71cdee3c8e382de5debe220abd8ee499b6806e45255dba80d69fb453c35837`
- **Derived Stratified Dataset**: [`infrastructure_info/infrastructure`](infrastructure_info/infrastructure) (**10,192 images across 57 classes**)
- **Splits**: 7,134 train (70.0%) / 1,529 valid (15.0%) / 1,529 test (15.0%)
- **Training Config**: 25 Epochs, imgsz 416, batch 16, Apple Silicon MPS acceleration.

#### Corrected Held-out Test Split Benchmark Results (1,529 test images)
| Metric | 6-Epoch Baseline | Flawed Test Model | **Final Stratified Model** | Relative Improvement vs Baseline |
| :--- | :---: | :---: | :---: | :---: |
| **Precision** | 0.0548 | 0.4060 | **0.7966** | **+1,353.65%** |
| **Recall** | 0.2292 | 0.3452 | **0.6791** | **+196.29%** |
| **mAP50** | 0.1529 | 0.3493 | **0.6925** | **+352.91%** |
| **mAP50-95** | 0.1100 | 0.2214 | **0.5628** | **+411.64%** |

#### Real Video Validation (`data/sample_videos/crossign.mp4`)
- **Resolution & Performance**: 463 frames (720x480) processed in 5.13s (**90.23 FPS**).
- **Detections**: 143 Traffic Sign Events (`STOP Sign`, `Traffic_signal`, `Stack type Advance Direction sign`, `Filling Station`).
- **Mean Bounding Box Confidence**: **0.3742**
- **Honest GPS Telemetry**: `GPS Telemetry Unavailable` (`latitude: null, longitude: null`).

---

## 💻 Quick Start & Demonstration

### 1. Launch System Demo
```bash
./scripts/run_demo.sh
```
Access local demo endpoints:
- **GIS Operations Dashboard UI**: [`http://127.0.0.1:3000`](http://127.0.0.1:3000)
- **FastAPI Central Backend REST API**: [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
- **Interactive OpenAPI Swagger Docs**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- **Database Health Check**: [`http://127.0.0.1:8000/health`](http://127.0.0.1:8000/health)
- **Database Statistics**: [`http://127.0.0.1:8000/stats`](http://127.0.0.1:8000/stats)

---

## 🧪 Automated Test Coverage

The platform includes **44 automated unit and integration test cases** across Phases 1–9 (100% PASS):
```bash
# Run complete system test suite across all modules (44/44 PASS)
python -m unittest discover tests

# Or run individual component test suites:
python tests/test_backend.py                # Backend API & Database (15/15 PASS)
python tests/test_dashboard.py              # GIS Dashboard & Data Integrity (5/5 PASS)
python tests/test_phase6_incidents.py       # Incident Management Subsystem (9/9 PASS)
python tests/test_phase7_analytics.py       # Analytics & Availability Indicators (5/5 PASS)
python tests/test_phase8_pedestrian.py      # Pedestrian & Crosswalk Safety (4/4 PASS)
python tests/test_phase9_infrastructure.py  # Infrastructure & Traffic Sign Intelligence (6/6 PASS)
```

---

## 📚 Complete Documentation Index

- [`infrastructure_info/README.md`](infrastructure_info/README.md) — Phase 9 Infrastructure Package Specification.
- [`infrastructure_info/documentation/STRATIFIED_SPLIT_REPORT.md`](infrastructure_info/documentation/STRATIFIED_SPLIT_REPORT.md) — Multi-Label Stratification Audit & 57-Class Distribution.
- [`infrastructure_info/documentation/EVALUATION_REPORT.md`](infrastructure_info/documentation/EVALUATION_REPORT.md) — Phase 9 57-Class Benchmark Metrics.
- [`infrastructure_info/documentation/REAL_VIDEO_REPORT.md`](infrastructure_info/documentation/REAL_VIDEO_REPORT.md) — Real Video Test on crossign.mp4.
- [`docs/phase6/INCIDENT_MANAGEMENT.md`](docs/phase6/INCIDENT_MANAGEMENT.md) — Phase 6 Incident Tracking Specification.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — System Flowcharts & Mermaid Diagrams.
- [`docs/API.md`](docs/API.md) — Central Backend REST API Reference.
- [`docs/DATABASE.md`](docs/DATABASE.md) — Relational Database Schema & ER Diagram.
- [`docs/DATASETS.md`](docs/DATASETS.md) — Dataset Provenance & Label Specs.

---

## 📜 License

This project is licensed under the MIT License — see the [`LICENSE`](LICENSE) file for details.

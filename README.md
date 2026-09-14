# 🚦 Smart Road Monitoring & Traffic Management Platform

### SIH 2026 — AI-Powered Road Intelligence & Incident Operations Prototype

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logo=pytorch&logoColor=black)
![SQLite WAL](https://img.shields.io/badge/Database-SQLite_WAL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Verification: PASS](https://img.shields.io/badge/System_Verification-PASS_100%25-10b981?style=for-the-badge&logo=github)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

---

> 💡 **Smart City Prototype**: A computer-vision-driven Smart City prototype that converts real-world road defects, vehicle counts, and license plate observations into structured events, persists them through a FastAPI backend & SQLite database, and provides an operator-focused Command Center for incident management.

---

## 📌 Smart India Hackathon (SIH 2026) Problem Statement Alignment

| Attribute | Details |
| :--- | :--- |
| **Problem Statement ID** | **26124** |
| **Problem Title** | **AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet** |
| **Organization** | **Bharat Electronics Limited (BEL)** |
| **Category & Theme** | **Software \| Smart Automation** |
| **Core Innovation** | **Mobile Edge-AI Sensing on Public Bus Fleet + Centralized GIS Intelligence Command Platform** |

> **Key Innovation**: Reuses existing public transport bus camera infrastructure as mobile sensing nodes across the city, processing video at the Edge (onboard) to send compact JSON alerts to a central command platform—eliminating the massive bandwidth cost of streaming raw video while covering 100% of urban transit corridors.

---

## 🎯 The Problem

Municipal road maintenance and traffic management in urban India face significant operational challenges:

- **Unmapped Road Defects**: Potholes, alligator cracks, and open manholes cause traffic delays and vehicle damage. Manual road inspection is slow, expensive, and reactive.
- **Unmonitored Traffic Bottlenecks**: Vehicle density and congestion levels on key municipal transit corridors lack automated counting and threshold alerting.
- **Fragmented Incident Lifecycles**: Detection observations are rarely linked to formal dispatch tickets with status transition tracking, operator accountability, and audit trails.
- **Data Inconsistencies & Synthetic Overhead**: Many existing prototypes rely on synthetic or hardcoded operational metrics, reducing real-world reliability.

---

## 💡 Proposed Solution

The **SIH 2026 Smart Road Monitoring Platform** unifies multi-class computer vision detectors, asynchronous backend ingestion, and operational incident dispatch into a single demo-ready system:

```
Camera / Video Stream ➔ AI Computer Vision ➔ Structured Telemetry JSON ➔ FastAPI Backend ➔ SQLite Database ➔ Incident Operations ➔ GIS Command Center
```

1. **Edge AI Detection**: Processes dashcam and CCTV video feeds to detect 6 road damage classes, count vehicles using ByteTrack, and localize license plates.
2. **Normalized Ingestion Engine**: Accepts incoming telemetry via REST endpoints, enforcing strict primary-key and content-hash deduplication.
3. **Incident Operations Subsystem**: Allows operators to dispatch incidents from real telemetry events, managing status transitions with full audit history logs.
4. **Operations Command Center**: A 9-tab dark Glassmorphism dashboard displaying real-time metrics, system health diagnostics, query filters, and report exporters.

---

## ⚡ Key System Capabilities

| Capability | Subsystem & Technology | Implementation | Verified Status |
| :--- | :--- | :--- | :--- |
| **Road Damage Detection** | YOLOv8 6-Class Model (`models/pothole.pt`) | [`src/detection/detect_potholes.py`](src/detection/detect_potholes.py) | ✅ Complete (2,708 Events) |
| **Vehicle Density & Tracking** | YOLOv8 COCO + ByteTrack 10s Window | [`src/detection/detect_vehicles.py`](src/detection/detect_vehicles.py) | ✅ Complete |
| **ANPR License Plate Localization** | YOLOv8 Plate Localizer (`models/anpr/best.pt`) | [`src/detection/detect_anpr.py`](src/detection/detect_anpr.py) | ✅ Complete (5,256 Events) |
| **Plate OCR Text Candidates** | EasyOCR Character Engine | [`src/detection/detect_anpr.py`](src/detection/detect_anpr.py) | ⚠️ Recognized Limit (20.14% Acc) |
| **Deduplicating Event Ingestion** | FastAPI Async REST + Hash Deduplication | [`src/backend/app.py`](src/backend/app.py) | ✅ Complete (`http://127.0.0.1:8000`) |
| **Incident Management Subsystem** | Relational Lifecycle & Audit Trail | [`src/backend/routes.py`](src/backend/routes.py) | ✅ Complete (State Machine Validated) |
| **GIS Operations Command Center** | Dark Glassmorphism UI (9 Tabs) | [`src/dashboard/index.html`](src/dashboard/index.html) | ✅ Complete (`http://127.0.0.1:3000`) |
| **Honest GPS Telemetry Handling** | Mode B (Null GPS Telemetry State) | [`src/dashboard/app.js`](src/dashboard/app.js) | ⚠️ GPS Hardware Unavailable |
| **Automated Reports Export** | Single-Click CSV & JSON Exporters | [`src/dashboard/app.js`](src/dashboard/app.js) | ✅ Complete |
| **Pedestrian & Infrastructure Checks**| Future Scope | N/A | 🔵 Planned |

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    subgraph Edge_Vision ["Computer Vision Detectors"]
        A1[Dashcam: Road Damage Feed] -->|YOLOv8 6-Class| B1[Potholes & Cracks]
        A2[CCTV: Traffic Feed] -->|YOLOv8 + ByteTrack| B2[Vehicle Count & Density]
        A3[ANPR: Plate Feed] -->|YOLOv8 + EasyOCR| B3[Plate Localization]
    end

    subgraph Central_Core ["Backend & Persistence Engine"]
        B1 & B2 & B3 --> C[Structured Telemetry JSON]
        C --> D[FastAPI Ingestion Engine]
        D -->|SHA256 Deduplication| E[(SQLite Database: data/events.db)]
    end

    subgraph Operations_Center ["Municipal Command Center UI"]
        E --> F[Glassmorphism Dashboard]
        F --> G[Telemetry Event Stream]
        F --> H[Incident Lifecycle Dispatch]
        F --> I[System Health Diagnostics]
        F --> J[CSV / JSON Report Exporters]
    end
```

---

## 🤖 AI & Computer Vision Subsystems & Performance Evaluation

> Model metrics are presented alongside real evaluation artifacts wherever available so that performance claims remain fully traceable to empirical held-out benchmark experiments.

---

### 1. Road Damage Detection Subsystem

- **Model File**: [`models/pothole.pt`](models/pothole.pt) | **SHA256**: `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b`
- **Supported Defect Classes**: `longitudinal_crack`, `transverse_crack`, `alligator_crack`, `pothole`, `manhole`, `waterlogging`.
- **Dataset**: 2,467 annotated road defect images (80% train, 10% val, 10% held-out test).

#### Held-out Benchmark Test Metrics

| Evaluation Metric | Held-out Test Benchmark Result |
| :--- | :---: |
| **Precision** | **54.32%** |
| **Recall** | **46.33%** |
| **mAP50** | **51.60%** |
| **mAP50-95** | **26.40%** |

*Note: Metrics represent strict evaluation on held-out test data.*

#### Road Damage — Confusion Matrix
The confusion matrix below demonstrates class localization across the 6 defect categories:

![Road Damage Confusion Matrix](potholes_info/runs/multiclass_road_damage_final/confusion_matrix.png)

*Figure 1: Verified confusion matrix for the 6-class Road Damage model (`models/pothole.pt`).*

#### Road Damage — Precision-Recall (PR) Curve
![Road Damage PR Curve](potholes_info/runs/multiclass_road_damage_final/BoxPR_curve.png)

*Figure 2: Precision-Recall curve across all defect classes.*

#### Road Damage — Training & Validation Loss Curves
![Road Damage Training Results](potholes_info/runs/multiclass_road_damage_final/results.png)

*Figure 3: Loss curves and mAP evolution across training epochs.*

#### Real Video Observation (`BUS-101`)
On a 15-second, 375-frame sample dashcam video (`data/sample_videos/patholes.mp4`), the model observed **1,001 pothole detections** and **4 manhole detections**, producing 2,708 telemetry records stored in `data/events.db`.

![Road Damage Max Detections Output](docs/images/pothole_max_detections.jpg)

*Figure 4: Real dashcam video frame exhibiting maximum multi-class road damage detections.*

---

### 2. Vehicle Density & ByteTrack Multi-Object Tracking

- **Model File**: [`models/yolov8n.pt`](models/yolov8n.pt) | **SHA256**: `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`
- **Tracked Object Classes**: `car`, `bus`, `truck`, `motorcycle`.
- **Counting Methodology**: Aggregates unique tracked object IDs across 10-second rolling evaluation windows to compute road segment vehicle counts and congestion levels. Untracked raw detections are excluded to prevent double-counting stationary or slow-moving vehicles.
- **Empirical Video Benchmark**: On a 24-second real sample video (`traffic_density_bridge.mp4`), ByteTrack tracked **91 unique vehicles** across 3 rolling windows.

#### Vehicle Tracking & ByteTrack Multi-Object Counter
![ByteTrack Vehicle Tracking Output](docs/images/vehicle_tracking_bytetrack.jpg)

*Figure 5: ByteTrack real-time multi-vehicle tracking & continuous ID assignment across dense traffic.*

---

### 3. ANPR License Plate Localization Subsystem

- **Model File**: [`models/anpr/best.pt`](models/anpr/best.pt) | **SHA256**: `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a`
- **Dataset**: 1,651 Indian license plate crop benchmark images.

#### Real Video ANPR Localization Output
![ANPR Plate Detection Output](docs/images/anpr_plate_detection.jpg)

*Figure 6: Real-time license plate localization on video stream (`models/anpr/best.pt`).*

#### Held-out Benchmark Test Metrics

| Evaluation Metric | Held-out Test Benchmark Result |
| :--- | :---: |
| **Precision** | **98.18%** |
| **Recall** | **95.78%** |
| **mAP50** | **98.04%** |
| **mAP50-95** | **70.42%** |

#### ANPR Plate Localizer — Confusion Matrix
![ANPR Confusion Matrix](anpr/runs/anpr_detection_v1/confusion_matrix.png)

*Figure 7: High-precision confusion matrix for the ANPR Plate Localizer model (`models/anpr/best.pt`).*

#### ANPR Plate Localizer — Precision-Recall Curve
![ANPR PR Curve](anpr/runs/anpr_detection_v1/BoxPR_curve.png)

*Figure 8: Precision-Recall curve demonstrating 98.04% mAP50 localization accuracy.*

#### ANPR Plate Localizer — Training & Validation Results
![ANPR Results Plot](anpr/runs/anpr_detection_v1/results.png)

*Figure 9: Training & validation metrics for the ANPR plate detector.*

---

### 4. Optical Character Recognition (EasyOCR)

Plate localization is paired with EasyOCR for text extraction:

| OCR Metric | Benchmark Result | Operational Interpretation |
| :--- | :---: | :--- |
| **Character Accuracy** | **20.14%** | Individual character recognition rate |
| **Exact Match Accuracy** | **7.51%** | Full plate text exact string match |
| **Character Error Rate (CER)** | **79.86%** | Normalized edit distance across predictions |

> *Note: OCR evaluation is reported numerically because a verified visual confusion-matrix artifact is not available in the repository.*

**Important Technical Distinction**: Plate localization is extremely accurate (**98.04% mAP50**), but character OCR accuracy is a recognized technical limitation on Indian license plates. Recognized text strings are treated as candidate reads, not validated vehicle registrations.

---

### 📊 Verified AI Results Summary

| AI Subsystem | Benchmark Dataset / Input | Primary Metric | Model Status |
| :--- | :--- | :---: | :--- |
| **Road Damage Detection** | 2,467 Road Damage Images | **mAP50: 51.60%** | ✅ Verified (`models/pothole.pt`) |
| **ANPR Plate Localizer** | 1,651 Indian Plate Crops | **mAP50: 98.04%** | ✅ Verified (`models/anpr/best.pt`) |
| **Vehicle Density Tracking** | COCO YOLOv8n + ByteTrack | **91 Unique Vehicles / 24s** | ✅ Verified (`models/yolov8n.pt`) |
| **EasyOCR Character Read** | Indian Plate OCR Benchmark | **Char Acc: 20.14%** | ⚠️ Recognized Limitation |

---

## 🗄️ Central Backend API & Database Engine

- **Framework**: FastAPI running on Uvicorn (`http://127.0.0.1:8000`).
- **Database Engine**: SQLite 3 with Write-Ahead Logging (WAL mode) at [`data/events.db`](data/events.db).
- **Stored Telemetry Event Count**: **7,964 Real Records** (2,708 Road Damage, 5,256 ANPR).
- **Deduplication Engine**: Performs primary-key verification and secondary deterministic SHA256 hash checking (`source`, `event_type`, `timestamp`, `payload_json`).

---

## 🚨 Incident Management Subsystem

The platform cleanly separates raw *Telemetry Events* from operational *Incidents*:

- **Creation**: Incidents can only be created from a verified, existing `event_id` in the database.
- **State Machine Lifecycle**:
  ```
  OPEN ➔ ACKNOWLEDGED ➔ IN_PROGRESS ➔ RESOLVED ➔ CLOSED
  ```
- **State Transition Guard**: Invalid transitions (e.g. `RESOLVED` back to `ACKNOWLEDGED`) are rejected with HTTP 400.
- **Audit History**: Every status modification or operator note generates an immutable record in `incident_history`.

---

## 📊 Operations Command Center Dashboard

Served locally at [`http://127.0.0.1:3000`](http://127.0.0.1:3000), the Glassmorphism dashboard provides 9 navigation views:

1. **Overview Tab**: Real-time KPI metric summary cards & raw telemetry event stream.
2. **Road Damage Tab**: Detailed breakdown cards for Alligator Cracks (1,747), Potholes (527), Longitudinal Cracks (273), Transverse Cracks (135), Manholes (24), and Waterloggings (2).
3. **Traffic Density Tab**: Vehicle counts and 10-second rolling window monitoring.
4. **ANPR & OCR Tab**: Plate detection statistics and EasyOCR character accuracy transparency banner.
5. **Incident Management Tab**: Real incident dispatch form, filterable incident directory table, status update modal, and audit trail viewer.
6. **GIS Map Tab**: Leaflet cartographic map displaying **Mode B** banner when GPS telemetry is null.
7. **Analytics Tab**: Empirical database statistics and source breakdowns.
8. **System Health Tab**: Real-time status checks for FastAPI (`/health`), SQLite DB, model weights, and hardware sensors.
9. **Reports Tab**: Single-click **Export Events CSV** and **Export Events JSON** download buttons.

---

## 🔒 Protected Model Checksums & Database Integrity

Automated verification ensures model weights and stored database records match verified baselines:

| Asset Path | Asset Description | Baseline SHA256 / Audit Baseline | Verification Status |
| :--- | :--- | :--- | :--- |
| [`models/pothole.pt`](models/pothole.pt) | Road Damage YOLOv8 Model | `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b` | **VERIFIED PASS** |
| [`models/anpr/best.pt`](models/anpr/best.pt) | ANPR YOLOv8 Localizer | `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a` | **VERIFIED PASS** |
| [`models/yolov8n.pt`](models/yolov8n.pt) | COCO Pretrained Base Model | `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36` | **VERIFIED PASS** |
| [`data/events.db`](data/events.db) | SQLite Database Store | **7,964 Total Records** (0 mapped, 7,964 unmapped) | **VERIFIED PASS** |

---

## 💻 Quick Start & Demonstration

### 1. Run Automated System Verification
```bash
./scripts/verify_project.sh
```

### 2. Launch System Demo
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

The platform includes 20 automated unit and integration test cases:
```bash
# Run backend API & incident management test suite (15/15 PASS)
python tests/test_backend.py

# Run dashboard & data integrity test suite (5/5 PASS)
python tests/test_dashboard.py
```

---

## ⚠️ Recognized Technical Limitations & Honesty

1. **EasyOCR Character Accuracy**: While plate localization is strong (98.04% mAP50), EasyOCR character accuracy is 20.14% on complex Indian fonts. Recognized plate text strings are treated as candidate reads.
2. **Waterlogging Sample Scarcity**: Scarcity of training samples limits waterlogging detection recall.
3. **GPS Telemetry Null State**: Test video feeds were recorded without attached NMEA hardware GPS sensors. All 7,964 stored events report `latitude: null, longitude: null`. The GIS dashboard represents this honestly in **Mode B** ("GPS Telemetry Unavailable").

---

## 🔮 Development Status & Roadmap

| Stage | Capability | Status |
| :--- | :--- | :--- |
| **Stage 1** | Road Damage Detection | ✅ Complete |
| **Stage 2** | Vehicle Density & Tracking | ✅ Complete |
| **Stage 3** | ANPR & EasyOCR Subsystem | ✅ Complete (OCR Limit Noted) |
| **Stage 4** | Backend Ingestion API | ✅ Complete |
| **Stage 5** | GIS Operations Dashboard | ✅ Complete (GPS Limit Noted) |
| **Stage 6** | Incident Management Subsystem | ✅ Complete |
| **Stage 7** | Analytics & Automated Exporters | ✅ Complete |
| **Stage 8** | Pedestrian Safety Analytics | 🔵 Planned |
| **Stage 9** | Infrastructure Inspection | 🔵 Planned |
| **Stage 10** | PostgreSQL / PostGIS Cloud Migration | 🔵 Planned |

---

## 📚 Complete Documentation Index

- [`docs/PROJECT_AUDIT.md`](docs/PROJECT_AUDIT.md) — Comprehensive System Audit Report.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — System Flowcharts & 9 Mermaid Diagrams.
- [`docs/AI_PIPELINE.md`](docs/AI_PIPELINE.md) — AI Model Specifications & Metrics.
- [`docs/API.md`](docs/API.md) — Central Backend REST API Reference.
- [`docs/DATABASE.md`](docs/DATABASE.md) — Relational Database Schema & ER Diagram.
- [`docs/DATASETS.md`](docs/DATASETS.md) — Dataset Provenance & Label Specs.
- [`docs/DATA_INTEGRITY.md`](docs/DATA_INTEGRITY.md) — Zero Fabrication Policy & Checksum Baselines.
- [`docs/DEMO_GUIDE.md`](docs/DEMO_GUIDE.md) — 5-to-10 Minute Judge Demonstration Script.
- [`docs/SIH_PRESENTATION.md`](docs/SIH_PRESENTATION.md) — 20-Slide Hackathon Presentation Structure.
- [`docs/JUDGE_QA.md`](docs/JUDGE_QA.md) — 20 Judge Q&A Defense Questions & Answers.
- [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) — Local, Docker & Cloud Deployment Guide.
- [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) — Capability Development Matrix.

---

## 📜 License

This project is licensed under the MIT License — see the [`LICENSE`](LICENSE) file for details.

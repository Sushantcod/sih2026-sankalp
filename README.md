<p align="center">
  <h1 align="center">🚦 Smart Road Monitoring & Traffic Management Platform</h1>
  <p align="center">
    <strong>AI-Powered Mobile Urban Intelligence Using Public Transport Fleets</strong>
    <br />
    <em>Smart India Hackathon 2026 — Problem Statement 26124 — Bharat Electronics Limited</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/YOLOv8-Ultralytics-FF6F00?style=for-the-badge&logo=pytorch&logoColor=white" alt="YOLOv8" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-WAL_Mode-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Tests-44/44_PASS-10b981?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/badge/License-MIT-2563EB?style=for-the-badge" alt="License" />
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [System Architecture](#-system-architecture)
- [AI Subsystems & Benchmarks](#-ai-subsystems--benchmarks)
- [Model Registry & Integrity](#-model-registry--integrity)
- [Development Roadmap](#-development-roadmap)
- [Quick Start](#-quick-start)
- [Testing & Verification](#-testing--verification)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Tech Stack](#-tech-stack)
- [License](#-license)

---

## 🎯 Overview

A full-stack, edge-to-cloud **computer vision and analytics platform** that transforms standard public transport bus dashcam feeds into **actionable municipal intelligence**. The system processes real-time video streams to simultaneously detect road defects, track vehicles, read license plates, monitor pedestrian safety, and recognize traffic infrastructure — all unified through a centralized backend API and an operator-grade GIS command center.

**Key Highlights:**
- **5 specialized YOLOv8 detection models** trained on real-world Indian road datasets
- **7,964+ real telemetry events** ingested into a production-grade SQLite database
- **44 automated tests** covering all subsystems with 100% pass rate
- **90+ FPS real-time inference** on Apple Silicon hardware
- **Zero data fabrication** — all statistics derived from empirically verified datasets

---

## 🏛 Problem Statement

| | |
| :--- | :--- |
| **Problem Statement ID** | **26124** |
| **Title** | AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet |
| **Organization** | Bharat Electronics Limited (BEL) |
| **Category** | Software · Smart Automation |
| **Target** | Urban Public Transport Bus Fleets (Multi-Camera Dashcam Setup) |

> **Mission**: Convert standard public transport vehicles into mobile sensing platforms that continuously monitor road conditions, traffic patterns, and infrastructure health — providing municipal authorities with real-time situational awareness for faster incident response and data-driven urban planning.

---

## 🏗 System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    EDGE INFERENCE LAYER (Bus Fleet)                   │
│                                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────┐ ┌─────────┐ ┌──────┐ │
│  │ Road Damage │ │  Vehicle    │ │  ANPR    │ │Pedestrn │ │Infra │ │
│  │ Detector    │ │  Tracker    │ │ + OCR    │ │Safety   │ │Signs │ │
│  │ (6-Class)   │ │ (ByteTrack) │ │(EasyOCR) │ │(3-Class)│ │(57-C)│ │
│  └──────┬──────┘ └──────┬──────┘ └────┬─────┘ └────┬────┘ └──┬───┘ │
│         │               │             │             │         │      │
│         └───────────────┴──────┬──────┴─────────────┴─────────┘      │
│                                │                                      │
│                    Structured Event Payloads (JSON)                   │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   CENTRAL BACKEND (FastAPI + SQLite WAL)              │
│                                                                      │
│  ┌──────────────┐  ┌───────────────┐  ┌───────────────────────────┐ │
│  │ REST API     │  │ Deduplication │  │ Incident Lifecycle Engine │ │
│  │ /ingest      │  │ PK + Content  │  │ OPEN → ACK → DISPATCHED  │ │
│  │ /events      │  │ Hash Guards   │  │ → IN_PROGRESS → RESOLVED │ │
│  │ /incidents   │  │               │  │ → CLOSED / REJECTED      │ │
│  │ /stats       │  │               │  │                           │ │
│  └──────────────┘  └───────────────┘  └───────────────────────────┘ │
│                                                                      │
│                     data/events.db (7,964 Records)                   │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│              GIS OPERATIONS COMMAND CENTER (Dark Theme UI)            │
│                                                                      │
│  📊 Live Metrics  │  🗺️ Leaflet Map  │  📋 Event Browser            │
│  📈 Analytics     │  🚨 Incidents    │  🔍 Detailed Modals           │
│  🚶 Pedestrian    │  🚦 Infrastructure│  ⚡ Real-Time Refresh         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Subsystems & Benchmarks

### Phase 1 — Road Damage Detection

Detects **6 classes** of road surface defects from dashcam video in real-time.

| Class | Description |
| :--- | :--- |
| `pothole` | Surface potholes of varying depth |
| `alligator_crack` | Interconnected crack patterns |
| `longitudinal_crack` | Cracks parallel to road direction |
| `transverse_crack` | Cracks perpendicular to road direction |
| `manhole` | Exposed/damaged manholes |
| `waterlogging` | Standing water on road surface |

- **Model**: [`models/pothole.pt`](models/pothole.pt) — Custom YOLOv8
- **Events Generated**: 2,708 real telemetry records
- **Implementation**: [`src/detection/detect_potholes.py`](src/detection/detect_potholes.py)

---

### Phase 2 — Vehicle Density & Congestion Tracking

Real-time vehicle classification and multi-object tracking using **ByteTrack** over 10-second rolling evaluation windows.

- **Model**: [`models/yolov8n.pt`](models/yolov8n.pt) — COCO Pretrained YOLOv8n
- **Classes**: Cars, Buses, Trucks, Motorcycles
- **Tracker**: ByteTrack with configurable congestion thresholds
- **Implementation**: [`src/detection/detect_vehicles.py`](src/detection/detect_vehicles.py)

---

### Phase 3 — Automatic Number Plate Recognition (ANPR)

Two-stage pipeline: YOLOv8 plate localization → EasyOCR character recognition.

- **Localizer Model**: [`models/anpr/best.pt`](models/anpr/best.pt) — Custom YOLOv8
- **OCR Engine**: EasyOCR (V1/V2 evaluated on 1,651 plate crops)
- **Events Generated**: 5,256 plate detection records
- **Implementation**: [`src/detection/detect_anpr.py`](src/detection/detect_anpr.py)

---

### Phase 8 — Pedestrian & Crosswalk Safety

Detects pedestrians, vehicles, and crosswalk zones for safety analytics.

| Class | Precision | Recall | mAP50 | mAP50-95 |
| :--- | :---: | :---: | :---: | :---: |
| **Crossing** (Crosswalk) | 95.60% | 89.40% | 94.40% | 69.90% |
| **Pedestrian** | 74.30% | 72.10% | 70.70% | 43.30% |
| **Vehicle** | 86.80% | 71.30% | 80.30% | 51.70% |
| **Overall** | **85.60%** | **77.60%** | **81.78%** | **54.97%** |

- **Dataset**: 7,737 images (5,415 train / 1,547 valid / 775 test)
- **Model**: [`models/pedestrian/pedestrian_detector.pt`](models/pedestrian/pedestrian_detector.pt)
- **Package**: [`pedestrian_info/`](pedestrian_info/)

---

### Phase 9 — Infrastructure & Traffic Sign Intelligence

Detects **57 classes** of Indian traffic signs using a multi-label stratified training pipeline.

| Metric | Baseline (6 epochs) | **Final Model (25 epochs)** | Improvement |
| :--- | :---: | :---: | :---: |
| **Precision** | 0.0548 | **0.7966** | +1,354% |
| **Recall** | 0.2292 | **0.6791** | +196% |
| **mAP50** | 0.1529 | **0.6925** | +353% |
| **mAP50-95** | 0.1100 | **0.5628** | +412% |

- **Dataset**: 10,192 images across 57 classes (iterative multi-label stratified split)
- **Real Video**: 90.23 FPS on `crossign.mp4` (720×480, 463 frames)
- **Model**: [`models/infrastructure/infrastructure_detector.pt`](models/infrastructure/infrastructure_detector.pt)
- **Package**: [`infrastructure_info/`](infrastructure_info/)

---

## 🔒 Model Registry & Integrity

All production model weights are SHA256-verified and regression-protected:

| Phase | Model | SHA256 | Status |
| :--- | :--- | :--- | :---: |
| 1 — Road Damage | [`pothole.pt`](models/pothole.pt) | `947ee609...b877b` | ✅ Frozen |
| 2 — Vehicles | [`yolov8n.pt`](models/yolov8n.pt) | `f59b3d83...3b36` | ✅ Frozen |
| 3 — ANPR | [`anpr/best.pt`](models/anpr/best.pt) | `d9584abd...ecf6a` | ✅ Frozen |
| 8 — Pedestrian | [`pedestrian_detector.pt`](models/pedestrian/pedestrian_detector.pt) | `18d6e7c7...b1c9d` | ✅ Frozen |
| 9 — Infrastructure | [`infrastructure_detector.pt`](models/infrastructure/infrastructure_detector.pt) | `7a71cdee...c35837` | ✅ Active |

> ⚠️ **Integrity Rule**: Model weights are NEVER overwritten or retrained without explicit authorization. Automated tests verify SHA256 checksums on every run.

---

## 🗺 Development Roadmap

| Phase | Subsystem | Status |
| :---: | :--- | :---: |
| 1 | Road Damage Detection (6-Class) | ✅ Complete |
| 2 | Vehicle Density & ByteTrack Tracking | ✅ Complete |
| 3 | ANPR & License Plate Recognition | ✅ Complete |
| 4 | Central Backend Ingestion API | ✅ Complete |
| 5 | GIS Operations Command Center | ✅ Complete |
| 6 | Incident Management Lifecycle | ✅ Complete |
| 7 | Empirical Traffic Analytics & KPIs | ✅ Complete |
| 8 | Pedestrian & Crosswalk Safety | ✅ Complete |
| 9 | Infrastructure & Traffic Sign Intelligence | ✅ Complete |
| 10 | PostgreSQL / PostGIS Cloud Migration | 🔵 Planned |

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.10+ required
python --version

# Install dependencies
pip install -r requirements.txt
```

### 1. Start the Backend API

```bash
python -m uvicorn src.backend.app:app --host 127.0.0.1 --port 8000
```

| Endpoint | URL |
| :--- | :--- |
| Health Check | [`http://127.0.0.1:8000/health`](http://127.0.0.1:8000/health) |
| Database Stats | [`http://127.0.0.1:8000/stats`](http://127.0.0.1:8000/stats) |
| OpenAPI Docs | [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) |

### 2. Launch the GIS Dashboard

```bash
python -m http.server 3000 --directory src/dashboard
```

Open [`http://127.0.0.1:3000`](http://127.0.0.1:3000) in your browser.

### 3. Run Detection Pipelines

```bash
# Road Damage Detection
python src/detection/detect_potholes.py --source data/sample_videos/patholes.mp4

# Vehicle Density & Tracking
python src/detection/detect_vehicles.py --source data/sample_videos/patholes.mp4

# ANPR License Plate Recognition
python src/detection/detect_anpr.py --source data/sample_videos/anpr.mp4
```

### 4. Ingest Events into Database

```bash
python src/ingestion/ingest_events.py outputs/detections/events.jsonl --direct-db
python src/ingestion/ingest_events.py outputs/anpr/anpr_events.json --direct-db
```

---

## 🧪 Testing & Verification

**44 automated tests** across all subsystems — **100% pass rate**:

```bash
# Run the complete test suite
python -m unittest discover tests
```

| Test Module | Scope | Cases |
| :--- | :--- | :---: |
| [`test_backend.py`](tests/test_backend.py) | Backend API, Database, Deduplication | 15 |
| [`test_dashboard.py`](tests/test_dashboard.py) | GIS Dashboard & Data Integrity | 5 |
| [`test_phase6_incidents.py`](tests/test_phase6_incidents.py) | Incident Lifecycle State Machine | 9 |
| [`test_phase7_analytics.py`](tests/test_phase7_analytics.py) | Analytics KPIs & Availability | 5 |
| [`test_phase8_pedestrian.py`](tests/test_phase8_pedestrian.py) | Pedestrian Model & Checksums | 4 |
| [`test_phase9_infrastructure.py`](tests/test_phase9_infrastructure.py) | Infrastructure Model & Checksums | 6 |

---

## 📁 Project Structure

```
SIH2026/
│
├── src/                          # Application Source Code
│   ├── detection/                # Edge Inference Pipelines
│   │   ├── detect_potholes.py    #   Road Damage (6-Class YOLOv8)
│   │   ├── detect_vehicles.py    #   Vehicle Density (ByteTrack)
│   │   └── detect_anpr.py        #   ANPR (YOLOv8 + EasyOCR)
│   ├── backend/                  # Central REST API
│   │   ├── app.py                #   FastAPI Entrypoint
│   │   ├── database.py           #   SQLite WAL Connection Manager
│   │   ├── models.py             #   Data Access & Deduplication
│   │   ├── routes.py             #   REST Endpoint Handlers
│   │   └── schemas.py            #   Pydantic Validators
│   ├── dashboard/                # GIS Command Center UI
│   │   ├── index.html            #   Dashboard Layout (9 Tabs)
│   │   ├── styles.css            #   Dark Glassmorphism Theme
│   │   └── app.js                #   Controller & Leaflet GIS
│   └── ingestion/                # Batch Event Loader
│       └── ingest_events.py      #   CLI Ingestion Tool
│
├── models/                       # Production Model Weights
│   ├── pothole.pt                #   Phase 1: Road Damage
│   ├── yolov8n.pt                #   Phase 2: COCO Vehicle Base
│   ├── anpr/best.pt              #   Phase 3: ANPR Localizer
│   ├── pedestrian/               #   Phase 8: Pedestrian Safety
│   └── infrastructure/           #   Phase 9: Traffic Signs (57-Class)
│
├── data/                         # Runtime Data
│   ├── sample_videos/            #   Test Video Streams
│   └── events.db                 #   SQLite Database (7,964 Records)
│
├── potholes_info/                # Phase 1 Dataset & Reports
├── anpr/                         # Phase 3 ANPR Benchmark Suite
├── pedestrian_info/              # Phase 8 Pedestrian Package
├── infrastructure_info/          # Phase 9 Infrastructure Package
│
├── docs/                         # Technical Documentation
├── tests/                        # Automated Test Suite (44 Cases)
├── scripts/                      # Utility & Demo Scripts
├── outputs/                      # Telemetry Logs & Reports
│
├── requirements.txt              # Python Dependencies
└── LICENSE                       # MIT License
```

---

## 📚 Documentation

### Architecture & Design

| Document | Description |
| :--- | :--- |
| [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System flowcharts & Mermaid diagrams |
| [`AI_PIPELINE.md`](docs/AI_PIPELINE.md) | End-to-end AI inference pipeline design |
| [`DATABASE.md`](docs/DATABASE.md) | Relational schema & ER diagram |
| [`API.md`](docs/API.md) | Central Backend REST API reference |
| [`DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Deployment guide & configuration |

### Subsystem Reports

| Document | Description |
| :--- | :--- |
| [`infrastructure_info/README.md`](infrastructure_info/README.md) | Phase 9 Infrastructure package spec |
| [`STRATIFIED_SPLIT_REPORT.md`](infrastructure_info/documentation/STRATIFIED_SPLIT_REPORT.md) | Multi-label stratification audit (57 classes) |
| [`EVALUATION_REPORT.md`](infrastructure_info/documentation/EVALUATION_REPORT.md) | Phase 9 benchmark metrics |
| [`REAL_VIDEO_REPORT.md`](infrastructure_info/documentation/REAL_VIDEO_REPORT.md) | Real video validation results |

### Operations & Presentation

| Document | Description |
| :--- | :--- |
| [`DEMO_GUIDE.md`](docs/DEMO_GUIDE.md) | Live demonstration walkthrough |
| [`SIH_PRESENTATION.md`](docs/SIH_PRESENTATION.md) | SIH presentation deck outline |
| [`JUDGE_QA.md`](docs/JUDGE_QA.md) | Anticipated judge Q&A preparation |
| [`DATA_INTEGRITY.md`](docs/DATA_INTEGRITY.md) | Data provenance & integrity guarantees |

---

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Computer Vision** | YOLOv8 (Ultralytics), OpenCV, ByteTrack |
| **OCR** | EasyOCR |
| **Deep Learning** | PyTorch, torchvision |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Database** | SQLite 3 (WAL Mode) |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JS, Leaflet.js |
| **Testing** | Python unittest (44 cases, 100% pass) |
| **Language** | Python 3.10+ |

---

## 👥 Team

**Team Sankalp** — Smart India Hackathon 2026

---

## 📜 License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ for Smart India Hackathon 2026</sub>
</p>

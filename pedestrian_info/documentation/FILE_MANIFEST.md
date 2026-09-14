# 📁 Phase 8 File & Asset Manifest

> **Subsystem**: Phase 8 Pedestrian & Crosswalk Safety Analytics  
> **Master Root**: `pedestrian_info/`

---

## 1. Codebase Scripts & Modules

- **`src/detection/train_pedestrian.py`**: Model training & validation script.
- **`src/detection/detect_pedestrians.py`**: Edge inference & telemetry event logging pipeline.
- **`src/detection/validate_pedestrian_video.py`**: Real video validation benchmark utility.
- **`src/backend/models.py`**: Backend models & pedestrian analytics data access.
- **`src/backend/routes.py`**: FastAPI REST endpoints for `/analytics/pedestrians` and `/analytics/pedestrians/safety`.
- **`src/dashboard/index.html`**: GIS Command Center Dashboard UI (Tab 7 & System Health).

---

## 2. Models & Weights

- **`models/pedestrian/pedestrian_detector.pt`**: Production Phase 8 trained YOLOv8 model (`SHA256: 18d6e7c72fccde6dec294b02ab5c06ee73c89302f319234f857c7915549b1c9d`).

---

## 3. Dataset Assets

- **`pedestrian_info/pedestrian/`**: Primary Roboflow YOLO training dataset (**7,737 images/labels** across train/valid/test splits).
- **`data/sample_videos/pedestrian_ipid.mp4`**: IPID Real video clip validation dataset.

---

## 4. Automated Tests

- **`tests/test_phase8_pedestrian.py`**: Isolated unit test suite for Phase 8 endpoints & indicators.

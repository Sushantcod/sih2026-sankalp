# Changelog

All notable changes to the **SIH 2026 Smart Road Monitoring & Traffic Management System** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to Semantic Versioning.

---

## [1.0.0] - 2026-09-14

### Added
- **Incident Management Subsystem**:
  - Implemented SQLite tables: `incidents`, `incident_events`, `incident_notes`, `incident_history`.
  - Added FastAPI REST endpoints: `POST /incidents`, `GET /incidents`, `GET /incidents/{id}`, `PATCH /incidents/{id}`, `POST /incidents/{id}/notes`, `GET /incidents/stats/summary`.
  - Implemented state-machine transition validation (`OPEN` -> `ACKNOWLEDGED` -> `IN_PROGRESS` -> `RESOLVED` -> `CLOSED`).
  - Added unit test suite for incident management in `tests/test_backend.py` (total 15 backend tests).
- **Operations Command Center UI**:
  - Upgraded GIS dashboard into a Command Center with 9 navigation tabs (Overview, Road Damage, Traffic Density, ANPR & OCR, Incident Management, GIS Map & Heatmap, Analytics, System Health, Reports).
  - Added interactive Incident Dispatch Form, filterable Incidents Table, Status Management Modal, and Audit History Viewer.
  - Added System Health real-time diagnostics tab.
  - Added CSV and JSON official report download exporters.
- **Automation Scripts & Tooling (`scripts/`)**:
  - Created `scripts/setup.sh`: Automated environment initializer.
  - Created `scripts/run_backend.sh`: FastAPI server launcher on port 8000.
  - Created `scripts/run_dashboard.sh`: Dashboard UI launcher on port 3000.
  - Created `scripts/run_demo.sh`: Unified demo script with diagnostic checks.
  - Created `scripts/verify_project.sh`: Automated model SHA256, DB count, zero-fabrication, and test suite verification script.
  - Created `scripts/health_check.sh`: Quick CLI health check tool.
- **Comprehensive Documentation Suite (`docs/`)**:
  - Created `docs/PROJECT_AUDIT.md`: System audit document.
  - Created `docs/ARCHITECTURE.md`: Technical architecture with 9 Mermaid diagrams.
  - Created `docs/AI_PIPELINE.md`: Specifications for Road Damage YOLOv8, ByteTrack, ANPR, and EasyOCR.
  - Created `docs/API.md`: Central Backend REST API reference.
  - Created `docs/DATABASE.md`: Database schema, indexes, and record breakdown.
  - Created `docs/DATASETS.md`: Dataset provenance for road damage (2,467 images) and ANPR crops (1,651 images).
  - Created `docs/DATA_INTEGRITY.md`: Zero-fabrication policy and baseline model checksums.
  - Created `docs/DEMO_GUIDE.md`: 5-to-10 minute judge demonstration walkthrough.
  - Created `docs/SIH_PRESENTATION.md`: 20-slide presentation deck structure.
  - Created `docs/JUDGE_QA.md`: 20 technical judge Q&A defense questions.
  - Created `docs/DEPLOYMENT.md`: Local and cloud deployment guide.
  - Created `docs/PROJECT_STATUS.md`: Capability development matrix.

### Changed
- Preserved existing 7,964 telemetry records in `data/events.db` with 100% data integrity.
- Maintained exact SHA256 checksums for protected model weights (`models/pothole.pt`, `models/anpr/best.pt`, `models/yolov8n.pt`).
- Ignored heavy raw dataset images in `.gitignore` to enable clean GitHub repository pushes.

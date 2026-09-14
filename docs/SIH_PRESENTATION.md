# SIH 2026 — 20-Slide Pitch Presentation Structure

This document outlines the authoritative 20-slide presentation deck structure for Smart India Hackathon 2026 judging panel evaluations.

---

### Slide 1: Title Slide
- **Title**: SIH 2026 Smart Road Monitoring & Intelligent Traffic Management System
- **Subtitle**: AI-Powered Edge Computer Vision, Ingestion Backend & Municipal GIS Command Center
- **Team**: Team Sankalp

### Slide 2: Problem Statement
- **Topic**: Manual, reactive road hazard inspection and traffic congestion in Indian municipalities.
- **Current Challenges**: Potholes cause accidents; manual inspection is slow, expensive, and unscalable.

### Slide 3: Current Technical Deficiencies
- Lack of automated real-time damage detection on public transit vehicles.
- Siloed traffic monitoring without automated incident lifecycle management.

### Slide 4: Proposed Solution
- A unified edge-to-cloud AI telemetry platform featuring multi-class road damage detection, vehicle density tracking, ANPR, high-throughput backend ingestion, and an operational command center.

### Slide 5: Key System Innovations
- Edge inference on transit buses (BUS-101).
- Primary key & content hash deduplication engine.
- State-machine driven incident lifecycle management with complete audit history.

### Slide 6: Master Architecture Overview
- Flow: Edge Video Streams -> YOLOv8 / ByteTrack -> FastAPI REST API -> SQLite Event Store -> Incident Engine -> Glassmorphism GIS Command Center.

### Slide 7: AI & Computer Vision Subsystem Overview
- 6-Class Road Damage YOLOv8 model (`models/pothole.pt`).
- COCO Base YOLOv8 + ByteTrack for 10s rolling vehicle density counting.
- YOLOv8 License Plate Localizer + EasyOCR engine.

### Slide 8: Road Damage Detection Benchmark & Field Results
- 6 Classes: Potholes, Alligator Cracks, Longitudinal Cracks, Transverse Cracks, Manholes, Waterlogging.
- mAP50: 51.60% on held-out benchmark dataset.
- Real Video Ingest: 2,708 telemetry records from `BUS-101`.

### Slide 9: Traffic Density & ByteTrack Multi-Object Tracking
- 10-second rolling window evaluation counting unique tracked IDs across cars, buses, trucks, motorcycles.

### Slide 10: Automatic Number Plate Recognition (ANPR) & OCR Analysis
- Plate Detection mAP50: 98.04% (98.18% precision, 95.78% recall).
- Real Video Ingest: 5,256 plate detections.
- Honest OCR Limitation: EasyOCR character accuracy is 20.14% on complex Indian plates — treated as raw candidates, not validated registrations.

### Slide 11: High-Performance Backend Ingestion API
- Framework: FastAPI on Uvicorn.
- Features: Asynchronous batch ingestion, deterministic payload hash deduplication, OpenAPI Swagger documentation.

### Slide 12: Database Engine & Relational Schema
- SQLite 3 with WAL journaling (`data/events.db`).
- Schema Tables: `events` (7,964 records), `incidents`, `incident_events`, `incident_notes`, `incident_history`.

### Slide 13: Municipal GIS Operations Command Center
- Dark-theme Glassmorphism UI served on `http://127.0.0.1:3000`.
- Features: 9 navigation tabs, real-time KPI metrics, query filters, event payload inspector.

### Slide 14: Incident Management Subsystem & Lifecycle
- Incident State Machine: `OPEN` -> `ACKNOWLEDGED` -> `IN_PROGRESS` -> `RESOLVED` -> `CLOSED`.
- Features: Operator assignment, severity classification, audit trail logging, invalid transition rejection.

### Slide 15: Analytics & Automated Reporting
- Real DB statistics aggregation, single-click CSV and JSON telemetry exports.

### Slide 16: Zero-Fabrication Policy & Honest Data Integrity
- Absolute policy against fake GPS or synthetic numbers.
- 100% honest representation of offline video telemetry (`latitude: null, longitude: null`, Mode B).

### Slide 17: Quality Assurance & Automated Testing
- Complete test suite: 15 backend unit tests, 5 dashboard integration tests, automated SHA256 model checksum verification script (`./scripts/verify_project.sh`).

### Slide 18: Recognized Limitations & Technical Transparency
- Weak waterlogging recall due to sample scarcity.
- EasyOCR character error rate on non-standard Indian fonts.
- GPS hardware dependency for mapping.

### Slide 19: Future Roadmap & Production Scaling
- Integration of hardware NMEA GPS receivers on bus fleets.
- EasyOCR fine-tuning / CRNN replacement for higher plate reading precision.
- PostgreSQL / PostGIS cloud migration & Kafka streaming.

### Slide 20: Conclusion & Demo Invitation
- Summary of achievements.
- Transition to live system demonstration on `http://127.0.0.1:3000`.

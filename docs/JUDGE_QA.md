# SIH 2026 — Judge Q&A Technical Defense Guide

This document contains 20 expected technical questions from SIH judges along with honest, empirically grounded answers.

---

### Q1: Why did you choose YOLOv8 for road damage detection?
**Answer**: YOLOv8 provides an optimal balance between real-time inference speed (30+ FPS on edge hardware) and multi-scale feature extraction necessary for detecting small defects like potholes and fine longitudinal cracks.

### Q2: Why did you select ByteTrack for vehicle tracking instead of SORT or DeepSORT?
**Answer**: ByteTrack tracks both high-confidence and low-confidence detection boxes, significantly reducing track fragmentations and ID switches when vehicles are partially occluded by trees, streetlights, or larger vehicles.

### Q3: Why is FastAPI used for the central backend?
**Answer**: FastAPI provides asynchronous I/O performance comparable to Node.js/Go, automatic OpenAPI Swagger documentation generation, and native integration with Pydantic for data validation.

### Q4: Why is SQLite used instead of PostgreSQL/PostGIS?
**Answer**: SQLite 3 with Write-Ahead Logging (WAL) is self-contained, zero-configuration, and extremely fast for edge and local prototype demonstrations (supporting up to 100,000+ reads/sec). PostgreSQL/PostGIS is documented as our planned cloud scaling architecture.

### Q5: How does the system detect and reject duplicate telemetry events?
**Answer**: The backend implements two-tier deduplication: first checking the primary key `event_id`, and second computing a deterministic SHA256 content hash of `source`, `event_type`, `timestamp`, and `payload_json`.

### Q6: Why does the GIS dashboard display "GPS Telemetry Unavailable"?
**Answer**: Because our test video streams (`patholes.mp4`, `anpr.mp4`) were recorded using standalone cameras without connected NMEA hardware GPS sensors. All 7,964 stored events contain `latitude: null, longitude: null`.

### Q7: Why didn't you generate fake GPS coordinates to make the map look nice?
**Answer**: We enforce a strict zero-fabrication policy. Inventing fake map markers would compromise data integrity and mislead operators. We honestly represent the system in Mode B (GPS Telemetry Unavailable).

### Q8: What is your ANPR plate localizer precision and mAP?
**Answer**: On our held-out test benchmark of 1,651 Indian plate images, our fine-tuned YOLOv8 Nano localizer achieves 98.18% precision, 95.78% recall, and 98.04% mAP50.

### Q9: Why is EasyOCR character accuracy currently low (20.14%)?
**Answer**: Indian license plates feature varied font styles, non-standard sizing, regional scripts, dirt, and high motion blur. EasyOCR is a general OCR model; fine-tuning a custom CRNN/LPRNet architecture is identified as future work.

### Q10: What is an "Event" versus an "Incident"?
**Answer**: An Event is a raw detection emitted by an edge AI detector (e.g. a single pothole box). An Incident is a operational dispatch ticket created from a verified event that requires municipal intervention and tracking.

### Q11: How do incident status transitions work?
**Answer**: Incidents follow a strict state machine: `OPEN` -> `ACKNOWLEDGED` -> `IN_PROGRESS` -> `RESOLVED` -> `CLOSED`. Invalid transitions (such as moving from `RESOLVED` back to `ACKNOWLEDGED`) are rejected with HTTP 400.

### Q12: How are operator notes and audit trails stored?
**Answer**: Every status change or operator note creates an immutable record in `incident_history` and `incident_notes` linked by foreign key to `incidents`.

### Q13: How many total events are currently stored in the database?
**Answer**: Exactly 7,964 real telemetry records (2,708 road damage events from `BUS-101` and 5,256 plate detection events from `anpr.mp4`).

### Q14: How does the system handle vehicle counting over time?
**Answer**: Vehicle counts are aggregated into 10-second rolling evaluation windows, counting unique ByteTrack IDs to prevent double-counting stationary or slow-moving vehicles.

### Q15: What is the performance of the road damage model?
**Answer**: On held-out test data, mAP50 is 51.60% across 6 classes. On our 15-second real sample video, it observed 1,001 pothole detections and 4 manhole detections.

### Q16: Why is waterlogging detection recall weak?
**Answer**: Waterlogging instances in training datasets are rare and highly dependent on lighting reflections. We explicitly document this limitation.

### Q17: Can this system run on live CCTV RTSP video streams?
**Answer**: Yes. `detect_potholes.py`, `detect_vehicles.py`, and `detect_anpr.py` accept RTSP stream URLs (`rtsp://...`) or webcams (`0`) as input sources in addition to MP4 video files.

### Q18: How do you verify project model integrity?
**Answer**: We calculate actual SHA256 checksums of model weights (`models/pothole.pt`, `models/anpr/best.pt`, `models/yolov8n.pt`) and verify them against hardcoded baselines in `./scripts/verify_project.sh`.

### Q19: What reports can the system generate?
**Answer**: The dashboard allows single-click exports of database telemetry directly into standard CSV and JSON files.

### Q20: What is the future production architecture?
**Answer**: Deploying hardware NMEA GPS receivers on transit buses, replacing EasyOCR with a custom CRNN, and deploying PostgreSQL/PostGIS and Kafka streaming on cloud infrastructure.

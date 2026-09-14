# SIH 2026 — Zero-Fabrication Policy & Data Integrity Protocols

This document details the absolute data integrity rules, GPS handling policies, and verification protocols enforced across the **SIH 2026 Smart Road Monitoring Platform**.

---

## 1. Zero-Fabrication Absolute Policy

1. **No Synthetic Operational Data**: Under no circumstances does the system generate random GPS coordinates, synthetic timestamps, fake vehicle counts, or fabricated license plate numbers for production telemetry.
2. **Honest GPS State Handling**: Test video streams were recorded without attached NMEA hardware GPS sensors. All 7,964 stored events report `latitude: null, longitude: null`.
3. **Dashboard Operating Modes**:
   - **Mode A (GPS Available)**: Render real markers and heatmaps when valid coordinates are present in incoming telemetry.
   - **Mode B (GPS Unavailable)**: When GPS is null, display `"GPS Telemetry Unavailable — Offline edge video stream"` and explicitly disable the map layer rather than inventing synthetic coordinates.

---

## 2. Protected Baseline Checksums

| File Path | Description | Expected SHA256 Checksum | Baseline Status |
| :--- | :--- | :--- | :--- |
| `models/pothole.pt` | Road Damage YOLOv8 Model | `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b` | **VERIFIED PASS** |
| `models/anpr/best.pt` | ANPR YOLOv8 Localizer | `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a` | **VERIFIED PASS** |
| `models/yolov8n.pt` | COCO Pretrained Base Model | `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36` | **VERIFIED PASS** |
| `data/events.db` | SQLite Database | 7,964 Total Records (0 mapped, 7,964 unmapped) | **VERIFIED PASS** |

---

## 3. Automated Integrity Audit Tool

Run `./scripts/verify_project.sh` to execute automated integrity checks:
1. Verifies SHA256 checksums of all model weights.
2. Verifies SQLite database record count equals 7,964.
3. Runs 15 backend unit tests.
4. Runs 5 dashboard integration tests.
5. Verifies API `/health` responsiveness.
6. Conducts a zero-fabrication code audit across JavaScript and Python files.

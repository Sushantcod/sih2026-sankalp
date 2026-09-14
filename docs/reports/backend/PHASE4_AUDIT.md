# Phase 4 Project Audit Report — Backend Ingestion API

**Audit Timestamp**: 2026-09-14T11:14:00Z  
**Auditor**: Antigravity Automated Verification & Backend System Architect  
**Scope**: Existing Phase 1, Phase 2, and Phase 3 event telemetries, schemas, and dependencies  

---

## 1. Executive Summary

A comprehensive audit was performed across all existing telemetry logs, detector output formats, and source scripts in the workspace.

- **Phase 1 (Road Damage)**: Produces 2,708 real line-delimited JSON (`JSONL`) events in `outputs/events.jsonl` covering 6 classes (`alligator_crack`, `pothole`, `longitudinal_crack`, `transverse_crack`, `manhole`, `waterlogging`).
- **Phase 2 (Vehicle Density & Congestion)**: Produces time-windowed tracking and density events (`vehicle_count`, `congestion`).
- **Phase 3 (ANPR / License Plate)**: Produces bounding box localization and OCR text extraction telemetries (`plate_detected`).

All telemetry fields were inspected directly from empirical runtime outputs. Missing fields (such as GPS coordinates on offline test streams) are explicitly set to `"GPS unavailable"` or `null` without fabricating fake values.

---

## 2. Empirical Source Event Schemas

### Phase 1 & 2 Schema (`outputs/events.jsonl`)

```json
{
  "event_id": "evt_1789274026261_23_1",
  "bus_id": "BUS-101",
  "frame_index": 23,
  "video_timestamp_sec": 0.733,
  "timestamp": "2026-09-13T04:33:45.906685+00:00",
  "event_type": "alligator_crack",
  "defect_class": "alligator_crack",
  "track_id": "[UNTRACKED]",
  "confidence": 0.2546,
  "bounding_box": [803, 695, 1093, 903],
  "gps": "GPS unavailable"
}
```

- **Available Fields**: `event_id`, `bus_id`, `frame_index`, `video_timestamp_sec`, `timestamp`, `event_type`, `defect_class`, `track_id`, `confidence`, `bounding_box`, `gps`.
- **Unavailable Fields**: Numeric latitude/longitude (`latitude: null`, `longitude: null` because GPS hardware is offline on test video).

### Phase 3 ANPR Schema (`outputs/anpr_events.json`)

```json
{
  "frame_idx": 100,
  "bbox": [184, 210, 462, 342],
  "detector_confidence": 0.816,
  "recognized_text": "GXIS0GJ",
  "ocr_confidence": 0.485
}
```

- **Available Fields**: `frame_idx`, `bbox`, `detector_confidence`, `recognized_text`, `ocr_confidence`.
- **Unavailable Fields**: `gps: null`, `latitude: null`, `longitude: null`.

---

## 3. Normalized Backend Ingestion Schema

To store diverse multi-modal events in SQLite while preserving 100% of original source key-value payloads:

| Column Name | SQLite Data Type | Extraction & Transformation Logic |
| :--- | :--- | :--- |
| `event_id` | `TEXT PRIMARY KEY` | Preserves original `event_id` if present, else derives `evt_<hash>` |
| `event_type` | `TEXT (Indexed)` | `pothole`, `alligator_crack`, `vehicle_count`, `congestion`, `plate_detected`, etc. |
| `source` | `TEXT (Indexed)` | `bus_id` or video file source path |
| `timestamp` | `TEXT (Indexed)` | ISO timestamp string from source payload (or `null` if unprovided) |
| `latitude` | `REAL` | Parsed numeric float if valid GPS exists, otherwise `null` |
| `longitude` | `REAL` | Parsed numeric float if valid GPS exists, otherwise `null` |
| `confidence` | `REAL` | Extracted numeric float (`confidence` or `detector_confidence`), otherwise `null` |
| `payload_json` | `TEXT` | Complete original source JSON dictionary string |
| `created_at` | `TEXT` | Backend storage UTC timestamp (`datetime.now(timezone.utc).isoformat()`) |

---

## 4. Implementation Decisions & Safety Verification

1. **Technology**: `FastAPI` + `Uvicorn` + `SQLite` (`data/events.db`).
2. **Deduplication Strategy**: Enforce SQLite `PRIMARY KEY` on `event_id` + unique constraint on `(source, event_type, timestamp, confidence)`.
3. **No Model/Data Interference**: Existing Phase 1, Phase 2, and Phase 3 models, scripts, and output files will remain untouched.

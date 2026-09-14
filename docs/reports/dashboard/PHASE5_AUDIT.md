# Phase 5 Project Audit Report — GIS Dashboard & Real-Data Heatmap

**Audit Timestamp**: 2026-09-14T12:13:00Z  
**Auditor**: Antigravity GIS & Dashboard System Architect  
**Scope**: Phase 4 FastAPI Backend, SQLite Database (`data/events.db`), Telemetry Fields, GPS & Timestamp Availability  

---

## 1. Executive Summary

A comprehensive audit was performed on the active Phase 4 FastAPI backend (`http://127.0.0.1:8000`) and the SQLite database (`data/events.db`).

- **Total Events in Database**: 7,964
- **Road Damage Events**: 2,708 (`alligator_crack`: 1,747, `pothole`: 527, `longitudinal_crack`: 273, `transverse_crack`: 135, `manhole`: 24, `waterlogging`: 2)
- **ANPR License Plate Events**: 5,256 (`plate_detected`)
- **GPS Availability**: **0 out of 7,964 events** have valid numeric latitude/longitude coordinates (`latitude: null, longitude: null`). All 7,964 records report `"gps": "GPS unavailable"` or lack GPS coordinates because source video telemetry was collected without NMEA GPS hardware logging.
- **Timestamp Availability**: 2,708 Phase 1/2 events contain ISO 8601 UTC timestamps. 5,256 Phase 3 ANPR events store frame index telemetry in their raw payload (`timestamp: null`).
- **Confidence Availability**: 100% of events store genuine numeric detector or OCR confidence floats (`confidence`, `detector_confidence`, `ocr_confidence`).

---

## 2. Empirical Database Schema & Field Audit

| Field Name | Data Type | Database Presence | GPS / Geographic Usage |
| :--- | :--- | :--- | :--- |
| `event_id` | `TEXT` | 100% (7,964 / 7,964) | Primary key identifier |
| `event_type` | `TEXT` | 100% (7,964 / 7,964) | Category filter (`pothole`, `plate_detected`, etc.) |
| `source` | `TEXT` | 100% (7,964 / 7,964) | Stream source (`BUS-101`, `data/sample_videos/anpr.mp4`) |
| `timestamp` | `TEXT` | 34.0% (2,708 / 7,964) | ISO 8601 string or `NULL` |
| `latitude` | `REAL` | **0% (0 / 7,964)** | `NULL` for all offline test stream records |
| `longitude` | `REAL` | **0% (0 / 7,964)** | `NULL` for all offline test stream records |
| `confidence` | `REAL` | 100% (7,964 / 7,964) | Numeric float (0.0 to 1.0) |
| `payload_json` | `TEXT` | 100% (7,964 / 7,964) | Full verbatim source payload string |
| `created_at` | `TEXT` | 100% (7,964 / 7,964) | Backend ingestion UTC timestamp |

---

## 3. API Endpoint Inventory

| Endpoint | Method | Availability | Purpose for Dashboard |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Online (`200 OK`) | System metadata & supported event types |
| `/health` | `GET` | Online (`200 OK`) | Live database connection monitoring |
| `/stats` | `GET` | Online (`200 OK`) | Total events, breakdown by type & source |
| `/events` | `GET` | Online (`200 OK`) | Event listing with type/source/time filters & pagination |
| `/events/{id}` | `GET` | Online (`200 OK`) | Individual event detail modal rendering |

---

## 4. GIS & Heatmap Audit Findings

1. **Strict Zero Fabrication Enforcement**: Because all 7,964 database events currently contain `latitude: null, longitude: null`, the GIS map engine MUST NOT plot markers at arbitrary default city coordinates (e.g. Mumbai center `[19.076, 72.877]`) or generate synthetic points.
2. **Honest GIS Communication**:
   - Map View: Displays prominent notification banner: `"GPS telemetry unavailable — 7,964 events have no GPS location and cannot be plotted geographically."`
   - Heatmap View: Displays warning overlay: `"Heatmap unavailable — no real GPS telemetry is currently available in the database."`
   - Unmapped Indicator Card: Dynamically counts and displays `7,964 / 7,964 events unmapped`.

---

## 5. Technology Stack Selection

- **Frontend Architecture**: Standalone Vanilla HTML5 + CSS3 + ES6 JavaScript.
- **Styling**: Premium Glassmorphism dark-theme UI with HSL color tokens, Inter font typography, smooth micro-interactions, responsive grid layout, and SIH 2026 header branding.
- **Mapping Library**: Leaflet 1.9.4 (OpenStreetMap tile layer) + Leaflet.heat plugin ready for genuine GPS coordinates.
- **Serving Architecture**: Lightweight Python HTTP server (`http.server`) running on port 3000, querying the live Phase 4 API on port 8000.

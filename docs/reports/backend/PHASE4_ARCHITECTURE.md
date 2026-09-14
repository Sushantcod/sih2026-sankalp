# Phase 4 System Architecture Report — Central Backend Ingestion API

**System**: SIH 2026 Smart Road & Traffic Monitoring System  
**Component**: Central Backend Ingestion Subsystem (Phase 4)  
**Date**: 2026-09-14  

---

## 1. High-Level System Architecture

The Central Backend Ingestion Subsystem acts as the unified data ingestion bridge between edge AI inference pipelines (Phase 1 Road Damage Detection, Phase 2 Vehicle Counting & Congestion Analytics, Phase 3 ANPR / License Plate Recognition) and downstream presentation/dashboard systems (Phase 5 Dashboard UI).

```
 +-----------------------------------------------------------------------------------+
 |                             EDGE AI PIPELINE DETECTORS                             |
 +----------------------------------+------------------------------------------------+
                                    |
  Phase 1: Road Damage              | Phase 2: Traffic Analytics      Phase 3: ANPR
  (pothole, crack, manhole)         | (vehicle_count, congestion)     (plate_detected)
                                    |
 +----------------------------------+------------------------------------------------+
                                    | REAL TELEMETRY STREAM / FILE OUTPUTS
                                    v
 +-----------------------------------------------------------------------------------+
 |                           CLI INGESTION UTILITY (`src/ingest_events.py`)          |
 +----------------------------------+------------------------------------------------+
                                    | HTTP POST /events/batch (Batch Ingestion)
                                    v
 +-----------------------------------------------------------------------------------+
 |                   FASTAPI CENTRAL INGESTION API (`src/backend/app.py`)             |
 |                                                                                   |
 |   +------------------------+   +----------------------+   +-------------------+   |
 |   | Pydantic Schema Layer  |-->| Ingestion & Dedupe   |-->| Query & Stats Engine|   |
 |   | (`src/backend/schemas`)|   | (`src/backend/models`)|   | (`src/backend/routes`)|
 |   +------------------------+   +----------------------+   +-------------------+   |
 +----------------------------------+------------------------------------------------+
                                    | SQLite WAL Storage Engine
                                    v
 +-----------------------------------------------------------------------------------+
 |                         SQLITE DATABASE (`data/events.db`)                         |
 |                                                                                   |
 | Table: `events`                                                                   |
 | Primary Index: `event_id`                                                         |
 | Secondary Indexes: `event_type`, `timestamp`, `source`                            |
 +-----------------------------------------------------------------------------------+
```

---

## 2. Component Design & Responsibility Matrix

| Module | File Location | Responsibility |
| :--- | :--- | :--- |
| **Application Entrypoint** | [`src/backend/app.py`](file:///Users/sushant/Documents/SIH2026/src/backend/app.py) | Instantiates `FastAPI` app with lifespan DB initialization on startup. |
| **Database Engine** | [`src/backend/database.py`](file:///Users/sushant/Documents/SIH2026/src/backend/database.py) | Manages SQLite connection factory, WAL journal mode, and schema migrations. |
| **Validation Schemas** | [`src/backend/schemas.py`](file:///Users/sushant/Documents/SIH2026/src/backend/schemas.py) | Defines Pydantic models for incoming payloads, batch requests, responses, and statistics. |
| **Data Access Layer** | [`src/backend/models.py`](file:///Users/sushant/Documents/SIH2026/src/backend/models.py) | Handles normalized field extraction, deterministic deduplication, queries, and DB stats calculation. |
| **API Endpoints** | [`src/backend/routes.py`](file:///Users/sushant/Documents/SIH2026/src/backend/routes.py) | Exposes HTTP routes (`/`, `/health`, `POST /events`, `POST /events/batch`, `GET /events`, `GET /events/{id}`, `GET /stats`). |
| **CLI Ingestion Utility** | [`src/ingest_events.py`](file:///Users/sushant/Documents/SIH2026/src/ingest_events.py) | Loads `.jsonl` / `.json` telemetry files and posts batch payloads to backend API with fallback to direct DB insertion. |
| **Automated Test Suite** | [`tests/test_backend.py`](file:///Users/sushant/Documents/SIH2026/tests/test_backend.py) | Executes 10 isolated unit test cases covering schema validation, deduplication, filtering, and database stats. |

---

## 3. Extensibility & Future-Proofing

1. **New Event Types**: Added simply by updating the `SUPPORTED_EVENT_TYPES` set in [`schemas.py`](file:///Users/sushant/Documents/SIH2026/src/backend/schemas.py). No table migrations or schema alters required.
2. **Payload Preservation**: The `payload_json` column stores 100% of original source key-value structures verbatim. Any novel edge metadata (e.g. thermal cameras, lidar metrics) is instantly accessible without changing table columns.
3. **Database Portability**: SQLite interface uses standard DB-API 2.0 SQL, allowing straightforward migration to PostgreSQL (via `asyncpg` or `psycopg2`) if high-throughput write scalability is needed in Phase 5.

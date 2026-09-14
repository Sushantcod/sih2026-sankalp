# SIH 2026 — Central Backend REST API Specification

FastAPI Backend Base URL: `http://127.0.0.1:8000`  
Interactive OpenAPI Swagger Docs: `http://127.0.0.1:8000/docs`

---

## 1. System Health & Metadata Endpoints

### `GET /`
- **Purpose**: Root backend status info.
- **Response `200 OK`**:
```json
{
  "service": "SIH 2026 Phase 4 Central Backend Ingestion API",
  "status": "online",
  "framework": "FastAPI",
  "database": "SQLite (data/events.db)",
  "supported_event_types": ["alligator_crack", "anpr", "congestion", "longitudinal_crack", "manhole", "plate_detected", "pothole", "transverse_crack", "vehicle_count", "waterlogging"]
}
```

### `GET /health`
- **Purpose**: Live health ping for backend and SQLite database connection.
- **Response `200 OK`**: `{"status": "ok", "database": "connected"}`

### `GET /stats`
- **Purpose**: Retrieve real database-derived metrics.
- **Response `200 OK`**:
```json
{
  "total_events": 7964,
  "count_by_type": {
    "alligator_crack": 1747,
    "longitudinal_crack": 273,
    "manhole": 24,
    "plate_detected": 5256,
    "pothole": 527,
    "transverse_crack": 135,
    "waterlogging": 2
  },
  "count_by_source": {
    "BUS-101": 2708,
    "data/sample_videos/anpr.mp4": 5256
  },
  "earliest_timestamp": null,
  "latest_timestamp": null
}
```

---

## 2. Event Ingestion Endpoints

### `POST /events`
- **Purpose**: Ingest a single edge detection payload. Performs primary key & content hash deduplication.
- **Response `200 OK`**: `{"status": "ingested", "event_id": "evt_...", "is_duplicate": false, "message": "Event ingested successfully"}`

### `POST /events/batch`
- **Purpose**: Ingest a batch array of telemetry events.

---

## 3. Telemetry Query Endpoints

### `GET /events`
- **Query Params**: `event_type`, `source`, `limit` (default 100, max 1000), `offset` (default 0).
- **Response `200 OK`**: Array of event objects.

### `GET /events/{event_id}`
- **Response `200 OK`**: Single event object including verbatim original JSON payload.
- **Response `404 Not Found`**: If `event_id` does not exist.

---

## 4. Incident Management Endpoints

### `POST /incidents`
- **Purpose**: Dispatch a new incident from a real `event_id`.
- **Request Body**:
```json
{
  "event_id": "evt_0001",
  "severity": "HIGH",
  "title": "Severe Pothole Cluster",
  "operator": "Officer_Deshmukh",
  "initial_note": "Field inspection unit dispatched"
}
```
- **Response `201 Created`**: Returns created incident object.
- **Response `404 Not Found`**: If target `event_id` does not exist in `events` table.

### `GET /incidents`
- **Query Params**: `status`, `severity`, `event_type`, `limit`, `offset`.

### `GET /incidents/{incident_id}`
- **Response `200 OK`**: Returns incident details, linked event, notes array, and audit history.

### `PATCH /incidents/{incident_id}`
- **Purpose**: Update status (OPEN, ACKNOWLEDGED, IN_PROGRESS, RESOLVED, CLOSED), severity, or operator. Validates state machine transitions.
- **Response `400 Bad Request`**: If status transition is invalid.

### `POST /incidents/{incident_id}/notes`
- **Purpose**: Add operator note to incident.

### `GET /incidents/stats/summary`
- **Purpose**: Retrieve incident statistics summary.

# Phase 4 REST API Specification Report

**API Version**: 1.0.0  
**Base URL**: `http://127.0.0.1:8000`  
**Protocol**: HTTP/1.1 REST (JSON)  

---

## 1. Summary of Endpoints

| Method | Endpoint Path | Summary | Authentication | Response Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Service identification & supported event types | None | `200 OK` |
| `GET` | `/health` | Liveness & database connection health check | None | `200 OK` / `500 Error` |
| `POST` | `/events` | Ingest single event payload | None | `200 OK` / `422 Unprocessable` |
| `POST` | `/events/batch` | Ingest batch of event payloads | None | `200 OK` / `422 Unprocessable` |
| `GET` | `/events` | Query events with filtering & pagination | None | `200 OK` |
| `GET` | `/events/{event_id}` | Retrieve specific event by ID | None | `200 OK` / `404 Not Found` |
| `GET` | `/stats` | Database-derived real statistics summary | None | `200 OK` |

---

## 2. Detailed Endpoint Specifications

### 1. Root Service Info — `GET /`

- **Response `200 OK`**:
```json
{
  "service": "SIH 2026 Phase 4 Central Backend Ingestion API",
  "status": "online",
  "framework": "FastAPI",
  "database": "SQLite (data/events.db)",
  "supported_event_types": [
    "alligator_crack",
    "anpr",
    "congestion",
    "longitudinal_crack",
    "manhole",
    "plate_detected",
    "pothole",
    "transverse_crack",
    "vehicle_count",
    "waterlogging"
  ]
}
```

---

### 2. Health Check — `GET /health`

- **Response `200 OK`**:
```json
{
  "status": "ok",
  "database": "connected"
}
```

---

### 3. Ingest Single Event — `POST /events`

- **Request Payload Example**:
```json
{
  "event_id": "evt_pothole_101",
  "event_type": "pothole",
  "source": "BUS-101",
  "timestamp": "2026-09-13T04:33:45.906685+00:00",
  "confidence": 0.89,
  "payload": {
    "bounding_box": [100, 200, 300, 400],
    "frame_index": 45
  }
}
```

- **Response `200 OK` (New Event)**:
```json
{
  "status": "ingested",
  "event_id": "evt_pothole_101",
  "is_duplicate": false,
  "message": "Event ingested successfully"
}
```

- **Response `200 OK` (Duplicate Event)**:
```json
{
  "status": "duplicate",
  "event_id": "evt_pothole_101",
  "is_duplicate": true,
  "message": "Event already exists (Primary Key duplicate)"
}
```

- **Response `422 Unprocessable Entity` (Invalid Event Type)**:
```json
{
  "detail": [
    {
      "loc": ["body", "event_type"],
      "msg": "Value error, Unsupported event_type 'invalid_type'. Supported types: [...]",
      "type": "value_error"
    }
  ]
}
```

---

### 4. Ingest Batch Events — `POST /events/batch`

- **Request Body**:
```json
{
  "events": [
    {"event_type": "pothole", "source": "BUS-101", "confidence": 0.91},
    {"event_type": "plate_detected", "source": "cam_01", "recognized_text": "MH01AB1234"}
  ]
}
```

- **Response `200 OK`**:
```json
{
  "total_received": 2,
  "ingested_count": 2,
  "duplicate_count": 0,
  "failed_count": 0,
  "details": [
    {
      "status": "ingested",
      "event_id": "evt_7d82a1...",
      "is_duplicate": false,
      "message": "Event ingested successfully"
    },
    {
      "status": "ingested",
      "event_id": "evt_9b3f4a...",
      "is_duplicate": false,
      "message": "Event ingested successfully"
    }
  ]
}
```

---

### 5. Query Events — `GET /events`

- **Query Parameters**:
  - `event_type` (string, optional): e.g. `pothole`
  - `source` (string, optional): e.g. `BUS-101`
  - `start_time` (string, optional): ISO string e.g. `2026-09-13T00:00:00Z`
  - `end_time` (string, optional): ISO string e.g. `2026-09-14T00:00:00Z`
  - `limit` (integer, default `100`, min `1`, max `1000`)
  - `offset` (integer, default `0`, min `0`)

- **Response `200 OK`**:
```json
[
  {
    "event_id": "evt_1789274026261_23_1",
    "event_type": "alligator_crack",
    "source": "BUS-101",
    "timestamp": "2026-09-13T04:33:45.906685+00:00",
    "latitude": null,
    "longitude": null,
    "confidence": 0.2546,
    "payload": {
      "bounding_box": [803, 695, 1093, 903],
      "bus_id": "BUS-101",
      "confidence": 0.2546,
      "defect_class": "alligator_crack",
      "event_id": "evt_1789274026261_23_1",
      "event_type": "alligator_crack",
      "frame_index": 23,
      "gps": "GPS unavailable",
      "timestamp": "2026-09-13T04:33:45.906685+00:00",
      "track_id": "[UNTRACKED]",
      "video_timestamp_sec": 0.733
    },
    "created_at": "2026-09-14T11:16:13.123456+00:00"
  }
]
```

---

### 6. Get Database Statistics — `GET /stats`

- **Response `200 OK`**:
```json
{
  "total_events": 7964,
  "count_by_type": {
    "alligator_crack": 1747,
    "pothole": 527,
    "longitudinal_crack": 273,
    "transverse_crack": 135,
    "manhole": 24,
    "waterlogging": 2,
    "plate_detected": 5256
  },
  "count_by_source": {
    "BUS-101": 2708,
    "data/sample_videos/anpr.mp4": 5256
  },
  "earliest_timestamp": "2026-09-13T04:33:45.906685+00:00",
  "latest_timestamp": "2026-09-13T04:39:08.231396+00:00"
}
```

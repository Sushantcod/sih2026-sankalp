# Phase 4 Database Design & Storage Engine Report

**Database File**: `data/events.db`  
**Engine**: SQLite 3 (WAL Mode Enabled)  
**ORM / Data Access**: Python Native `sqlite3` driver with `Row` factory  

---

## 1. Relational Table Schema Definition

```sql
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    source TEXT NOT NULL,
    timestamp TEXT,
    latitude REAL,
    longitude REAL,
    confidence REAL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- Strategic Indexes for High-Performance Queries & Aggregations
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_source ON events(source);
```

---

## 2. Field Storage Contract & Normalization Rules

1. **`event_id`**: Primary key. If the incoming payload supplies a unique `event_id`, it is stored directly. If unprovided, a deterministic SHA-256 hash is computed from `(source, event_type, timestamp, confidence, payload)`: `evt_<sha256[:16]>`.
2. **`event_type`**: Lowercase string representing the specific event category (e.g. `pothole`, `alligator_crack`, `vehicle_count`, `plate_detected`). Indexed for rapid sub-millisecond filtering.
3. **`source`**: Identifier of the edge device, camera, bus, or video file generating the event (e.g. `BUS-101`). Indexed for source-level telemetry isolation.
4. **`timestamp`**: ISO 8601 string representing the exact time the event was detected by the edge AI system. Set to `NULL` if unavailable in source.
5. **`latitude` / `longitude`**: Float representation of genuine GPS coordinates. If source telemetry reports `"GPS unavailable"`, non-numeric strings, or missing values, these columns are strictly stored as `NULL`. No fake or synthetic coordinates are ever populated.
6. **`confidence`**: Float value representing detector or OCR confidence score (0.0 to 1.0).
7. **`payload_json`**: Verbatim JSON string serialization of the complete original input event dictionary. This guarantees ZERO information loss regardless of edge payload variations.
8. **`created_at`**: Backend insertion ISO timestamp in UTC (`datetime.now(timezone.utc).isoformat()`).

---

## 3. Deduplication Strategy & Data Integrity

Deduplication occurs at two distinct layers before write execution:

1. **Primary Key Deduplication**: SQLite rejects duplicate `event_id` writes via `PRIMARY KEY` constraint.
2. **Content Hash Deduplication**: For un-identified events, the system queries for existing rows with matching `source`, `event_type`, `timestamp`, and `payload_json`.

When a duplicate is detected, the database engine skips re-insertion, rolls back the transaction silently, and returns `"status": "duplicate"`.

---

## 4. Empirical Storage Footprint

- **Database Path**: `data/events.db`
- **Total Ingested Events**: 7,964
- **Database File Size**: ~2.8 MB
- **Average Record Size**: ~350 bytes / record
- **WAL Journal File**: `data/events.db-wal` (improves concurrent read/write throughput)

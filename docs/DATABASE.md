# SIH 2026 — Database Schema & Data Integrity Reference

- **Database Engine**: SQLite 3 (WAL Journaling enabled)
- **Database Path**: `data/events.db`
- **Total Stored Telemetry Events**: 7,964 Real Records

---

## 1. Relational Table Schema

### Table: `events`
Stores normalized edge detection telemetry.
```sql
CREATE TABLE events (
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

CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_events_source ON events(source);
```

### Table: `incidents`
Stores dispatch incidents created from real telemetry events.
```sql
CREATE TABLE incidents (
    incident_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'OPEN',
    severity TEXT NOT NULL DEFAULT 'MEDIUM',
    title TEXT NOT NULL,
    description TEXT,
    operator TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY(event_id) REFERENCES events(event_id)
);

CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_severity ON incidents(severity);
CREATE INDEX idx_incidents_event_id ON incidents(event_id);
```

### Table: `incident_events`
Maps incidents to linked events.
```sql
CREATE TABLE incident_events (
    incident_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(incident_id, event_id),
    FOREIGN KEY(incident_id) REFERENCES incidents(incident_id),
    FOREIGN KEY(event_id) REFERENCES events(event_id)
);
```

### Table: `incident_notes`
Stores operator notes for incidents.
```sql
CREATE TABLE incident_notes (
    note_id TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL,
    operator TEXT,
    note_text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(incident_id) REFERENCES incidents(incident_id)
);
```

### Table: `incident_history`
Maintains a complete audit trail for state transitions and modifications.
```sql
CREATE TABLE incident_history (
    history_id TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL,
    action TEXT NOT NULL,
    old_status TEXT,
    new_status TEXT,
    operator TEXT,
    details TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(incident_id) REFERENCES incidents(incident_id)
);
```

---

## 2. Empirical Database Audit Breakdown

- **Total Ingested Telemetry Records**: 7,964
- **Event Breakdown**:
  - `plate_detected`: 5,256
  - `alligator_crack`: 1,747
  - `pothole`: 527
  - `longitudinal_crack`: 273
  - `transverse_crack`: 135
  - `manhole`: 24
  - `waterlogging`: 2
- **Source Breakdown**:
  - `BUS-101`: 2,708
  - `data/sample_videos/anpr.mp4`: 5,256
- **GPS Coverage**:
  - `latitude IS NOT NULL`: **0**
  - `latitude IS NULL`: **7,964** (100% honest representation of offline edge video streams captured without attached NMEA hardware GPS sensors)

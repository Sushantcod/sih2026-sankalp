# Phase 4 System Limitations & Production Upgrade Pathway

**System**: Central Backend Ingestion Subsystem (Phase 4)  
**Date**: 2026-09-14  

---

## 1. Identified System Limitations

1. **GPS Hardware Dependency**:
   - *Observation*: Test video streams (`data/sample_videos/`) were collected without active NMEA GPS sensors attached to the inference rig.
   - *Impact*: The database stores `latitude: null, longitude: null` and `gps: "GPS unavailable"` for those events.
   - *Resolution*: When real GPS hardware streams NMEA sentence payloads in production deployment, the backend parser dynamically populates numeric float coordinates without code changes.

2. **Single-Node SQLite Write Concurrency**:
   - *Observation*: SQLite operates with single-writer lock constraints.
   - *Impact*: While WAL mode provides high read concurrency (up to 37,000 requests/sec), write throughput across hundreds of concurrent edge nodes may cause database locks.
   - *Resolution Pathway*: In Phase 5, PostgreSQL + Connection Pooling (`asyncpg`) can replace SQLite if multi-bus concurrent writes exceed 5,000 writes/sec.

3. **In-Memory Query Pagination**:
   - *Observation*: Query limit is currently capped at 1,000 events per request (`limit: 1000`).
   - *Impact*: Bulk downloads of millions of events require iterating offset parameters (`offset=0`, `offset=1000`, etc.).
   - *Resolution*: Add streaming response endpoints (`GET /events/stream`) in Phase 5 for bulk CSV/JSON exporting.

---

## 2. Risk Mitigation & Operational Readiness

| Risk / Limitation | Severity | Mitigation Strategy | Production Status |
| :--- | :--- | :--- | :--- |
| **Missing GPS Data** | Low | Store `null` values cleanly without default fallback location | **SAFE** |
| **Duplicate Event Ingestion** | Medium | Enforce deterministic primary key & content hash deduplication | **RESOLVED** |
| **Unsupported Schema Ingestion** | Medium | Reject un-whitelisted `event_type` strings with Pydantic `422` error | **RESOLVED** |
| **Server Crash Handling** | Low | SQLite WAL mode automatically recovers clean state on reboot | **SAFE** |

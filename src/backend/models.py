import json
import hashlib
import sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple, List
from src.backend.database import get_db_connection

def extract_normalized_fields(raw_dict: Dict[str, Any]) -> Tuple[str, str, Optional[str], Optional[str], Optional[float], Optional[float], Optional[float], Dict[str, Any]]:
    """Extract normalized fields from raw event payload while preserving 100% of original source dict."""
    # 1. Event Type
    event_type = str(raw_dict.get("event_type", "unknown")).lower().strip()
    if not event_type or event_type == "unknown":
        if "defect_class" in raw_dict:
            event_type = str(raw_dict["defect_class"]).lower().strip()
        elif "recognized_text" in raw_dict:
            event_type = "plate_detected"

    # 2. Source
    source = raw_dict.get("source") or raw_dict.get("bus_id") or "unspecified_source"

    # 3. Timestamp (Real source timestamp or None)
    timestamp = raw_dict.get("timestamp")
    if isinstance(timestamp, str) and timestamp.strip():
        timestamp = timestamp.strip()
    else:
        timestamp = None

    # 4. Latitude & Longitude (Genuine GPS only)
    latitude = None
    longitude = None
    raw_gps = raw_dict.get("gps")
    if isinstance(raw_gps, dict):
        latitude = raw_gps.get("lat") or raw_gps.get("latitude")
        longitude = raw_gps.get("lon") or raw_gps.get("longitude")
    elif isinstance(raw_dict.get("latitude"), (int, float)):
        latitude = float(raw_dict["latitude"])
    elif isinstance(raw_dict.get("longitude"), (int, float)):
        longitude = float(raw_dict["longitude"])

    # 5. Confidence
    confidence = None
    if "confidence" in raw_dict and isinstance(raw_dict["confidence"], (int, float)):
        confidence = float(raw_dict["confidence"])
    elif "detector_confidence" in raw_dict and isinstance(raw_dict["detector_confidence"], (int, float)):
        confidence = float(raw_dict["detector_confidence"])
    elif "ocr_confidence" in raw_dict and isinstance(raw_dict["ocr_confidence"], (int, float)):
        confidence = float(raw_dict["ocr_confidence"])

    # 6. Event ID Generation (Deterministic Hash fallback if unprovided)
    event_id = raw_dict.get("event_id")
    if not event_id:
        hash_input = f"{source}_{event_type}_{timestamp}_{confidence}_{json.dumps(raw_dict, sort_keys=True)}"
        event_id = f"evt_{hashlib.sha256(hash_input.encode()).hexdigest()[:16]}"

    return event_id, event_type, source, timestamp, latitude, longitude, confidence, raw_dict

def insert_single_event(conn: sqlite3.Connection, raw_dict: Dict[str, Any]) -> Tuple[bool, str, str]:
    """Insert a single event with deterministic deduplication."""
    event_id, event_type, source, timestamp, latitude, longitude, confidence, payload = extract_normalized_fields(raw_dict)
    
    created_at = datetime.now(timezone.utc).isoformat()
    payload_json = json.dumps(payload, sort_keys=True)

    cursor = conn.cursor()

    # Check primary key deduplication
    cursor.execute("SELECT event_id FROM events WHERE event_id = ?", (event_id,))
    if cursor.fetchone():
        return True, event_id, "Event already exists (Primary Key duplicate)"

    # Secondary deterministic content deduplication check
    cursor.execute(
        "SELECT event_id FROM events WHERE source = ? AND event_type = ? AND timestamp IS ? AND payload_json = ?",
        (source, event_type, timestamp, payload_json)
    )
    if cursor.fetchone():
        return True, event_id, "Event already exists (Identical payload content)"

    try:
        cursor.execute("""
            INSERT INTO events (event_id, event_type, source, timestamp, latitude, longitude, confidence, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (event_id, event_type, source, timestamp, latitude, longitude, confidence, payload_json, created_at))
        conn.commit()
        return False, event_id, "Event ingested successfully"
    except sqlite3.IntegrityError:
        return True, event_id, "Event already exists (Integrity Constraint)"

def query_events(
    event_type: Optional[str] = None,
    source: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if event_type:
        query += " AND event_type = ?"
        params.append(event_type.lower().strip())
    if source:
        query += " AND source = ?"
        params.append(source)
    if start_time:
        query += " AND timestamp >= ?"
        params.append(start_time)
    if end_time:
        query += " AND timestamp <= ?"
        params.append(end_time)

    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "event_id": r["event_id"],
            "event_type": r["event_type"],
            "source": r["source"],
            "timestamp": r["timestamp"],
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "confidence": r["confidence"],
            "payload": json.loads(r["payload_json"]),
            "created_at": r["created_at"]
        })
    return results

def get_event_by_id(event_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
    r = cursor.fetchone()
    conn.close()

    if not r:
        return None

    return {
        "event_id": r["event_id"],
        "event_type": r["event_type"],
        "source": r["source"],
        "timestamp": r["timestamp"],
        "latitude": r["latitude"],
        "longitude": r["longitude"],
        "confidence": r["confidence"],
        "payload": json.loads(r["payload_json"]),
        "created_at": r["created_at"]
    }

def get_database_stats() -> Dict[str, Any]:
    """Calculate REAL database-derived statistics. Returns 0/empty if DB is empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM events")
    total_events = cursor.fetchone()["total"]

    count_by_type = {}
    cursor.execute("SELECT event_type, COUNT(*) as cnt FROM events GROUP BY event_type")
    for r in cursor.fetchall():
        count_by_type[r["event_type"]] = r["cnt"]

    count_by_source = {}
    cursor.execute("SELECT source, COUNT(*) as cnt FROM events GROUP BY source")
    for r in cursor.fetchall():
        count_by_source[r["source"]] = r["cnt"]

    cursor.execute("SELECT MIN(timestamp) as min_ts, MAX(timestamp) as max_ts FROM events WHERE timestamp IS NOT NULL")
    ts_row = cursor.fetchone()
    earliest_ts = ts_row["min_ts"] if ts_row else None
    latest_ts = ts_row["max_ts"] if ts_row else None

    conn.close()

    return {
        "total_events": total_events,
        "count_by_type": count_by_type,
        "count_by_source": count_by_source,
        "earliest_timestamp": earliest_ts,
        "latest_timestamp": latest_ts
    }

# Incident Database Operations

VALID_TRANSITIONS = {
    "OPEN": {"ACKNOWLEDGED", "IN_PROGRESS", "RESOLVED", "CLOSED"},
    "ACKNOWLEDGED": {"IN_PROGRESS", "RESOLVED", "CLOSED"},
    "IN_PROGRESS": {"RESOLVED", "CLOSED"},
    "RESOLVED": {"CLOSED", "OPEN"},
    "CLOSED": {"OPEN"}
}

def create_incident(
    event_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    severity: Optional[str] = "MEDIUM",
    operator: Optional[str] = None,
    initial_note: Optional[str] = None
) -> Tuple[Optional[Dict[str, Any]], str]:
    """Create a new incident linked to a REAL event_id. Fails safely if event_id does not exist."""
    event = get_event_by_id(event_id)
    if not event:
        return None, f"Event ID '{event_id}' does not exist in database"

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if active incident already exists for this event
    cursor.execute("SELECT incident_id FROM incidents WHERE event_id = ? AND status != 'CLOSED'", (event_id,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return None, f"An active incident '{existing['incident_id']}' already exists for event_id '{event_id}'"

    now_iso = datetime.now(timezone.utc).isoformat()
    inc_hash = hashlib.sha256(f"{event_id}_{now_iso}".encode()).hexdigest()[:12]
    incident_id = f"inc_{inc_hash}"

    inc_title = title or f"Incident: {event['event_type']} ({event_id})"
    inc_severity = (severity or "MEDIUM").upper()
    if inc_severity not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        inc_severity = "MEDIUM"

    cursor.execute("""
        INSERT INTO incidents (incident_id, event_id, status, severity, title, description, operator, created_at, updated_at, resolved_at)
        VALUES (?, ?, 'OPEN', ?, ?, ?, ?, ?, ?, NULL)
    """, (incident_id, event_id, inc_severity, inc_title, description, operator, now_iso, now_iso))

    cursor.execute("""
        INSERT INTO incident_events (incident_id, event_id, created_at)
        VALUES (?, ?, ?)
    """, (incident_id, event_id, now_iso))

    # Record history
    hist_id = f"hist_{hashlib.sha256(f'{incident_id}_created_{now_iso}'.encode()).hexdigest()[:12]}"
    cursor.execute("""
        INSERT INTO incident_history (history_id, incident_id, action, old_status, new_status, operator, details, created_at)
        VALUES (?, ?, 'CREATED', NULL, 'OPEN', ?, ?, ?)
    """, (hist_id, incident_id, operator, f"Incident created from event {event_id}", now_iso))

    # Add initial note if provided
    if initial_note and initial_note.strip():
        note_id = f"note_{hashlib.sha256(f'{incident_id}_init_{now_iso}'.encode()).hexdigest()[:12]}"
        cursor.execute("""
            INSERT INTO incident_notes (note_id, incident_id, operator, note_text, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (note_id, incident_id, operator, initial_note.strip(), now_iso))

    conn.commit()
    conn.close()

    result = get_incident_by_id(incident_id)
    return result, "Incident created successfully"

def query_incidents(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT i.*, e.event_type, e.source, e.timestamp as event_timestamp, e.latitude, e.longitude, e.confidence, e.payload_json
        FROM incidents i
        JOIN events e ON i.event_id = e.event_id
        WHERE 1=1
    """
    params = []

    if status:
        query += " AND i.status = ?"
        params.append(status.upper().strip())
    if severity:
        query += " AND i.severity = ?"
        params.append(severity.upper().strip())
    if event_type:
        query += " AND e.event_type = ?"
        params.append(event_type.lower().strip())

    query += " ORDER BY i.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    incidents = []
    for r in rows:
        incidents.append({
            "incident_id": r["incident_id"],
            "event_id": r["event_id"],
            "status": r["status"],
            "severity": r["severity"],
            "title": r["title"],
            "description": r["description"],
            "operator": r["operator"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "resolved_at": r["resolved_at"],
            "event": {
                "event_id": r["event_id"],
                "event_type": r["event_type"],
                "source": r["source"],
                "timestamp": r["event_timestamp"],
                "latitude": r["latitude"],
                "longitude": r["longitude"],
                "confidence": r["confidence"],
                "payload": json.loads(r["payload_json"]),
                "created_at": r["created_at"]
            },
            "notes": [],
            "history": []
        })
    return incidents

def get_incident_by_id(incident_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.*, e.event_type, e.source, e.timestamp as event_timestamp, e.latitude, e.longitude, e.confidence, e.payload_json
        FROM incidents i
        JOIN events e ON i.event_id = e.event_id
        WHERE i.incident_id = ?
    """, (incident_id,))
    r = cursor.fetchone()
    if not r:
        conn.close()
        return None

    # Fetch notes
    cursor.execute("SELECT * FROM incident_notes WHERE incident_id = ? ORDER BY created_at ASC", (incident_id,))
    note_rows = cursor.fetchall()
    notes = [{
        "note_id": n["note_id"],
        "incident_id": n["incident_id"],
        "operator": n["operator"],
        "note_text": n["note_text"],
        "created_at": n["created_at"]
    } for n in note_rows]

    # Fetch history
    cursor.execute("SELECT * FROM incident_history WHERE incident_id = ? ORDER BY created_at ASC", (incident_id,))
    hist_rows = cursor.fetchall()
    history = [{
        "history_id": h["history_id"],
        "incident_id": h["incident_id"],
        "action": h["action"],
        "old_status": h["old_status"],
        "new_status": h["new_status"],
        "operator": h["operator"],
        "details": h["details"],
        "created_at": h["created_at"]
    } for h in hist_rows]

    conn.close()

    return {
        "incident_id": r["incident_id"],
        "event_id": r["event_id"],
        "status": r["status"],
        "severity": r["severity"],
        "title": r["title"],
        "description": r["description"],
        "operator": r["operator"],
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
        "resolved_at": r["resolved_at"],
        "event": {
            "event_id": r["event_id"],
            "event_type": r["event_type"],
            "source": r["source"],
            "timestamp": r["event_timestamp"],
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "confidence": r["confidence"],
            "payload": json.loads(r["payload_json"]),
            "created_at": r["created_at"]
        },
        "notes": notes,
        "history": history
    }

def update_incident(
    incident_id: str,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    operator: Optional[str] = None,
    note: Optional[str] = None
) -> Tuple[Optional[Dict[str, Any]], str]:
    inc = get_incident_by_id(incident_id)
    if not inc:
        return None, f"Incident '{incident_id}' not found"

    old_status = inc["status"]
    new_status = status.upper().strip() if status else old_status

    if status and new_status != old_status:
        allowed = VALID_TRANSITIONS.get(old_status, set())
        if new_status not in allowed:
            return None, f"Invalid status transition from '{old_status}' to '{new_status}'. Allowed transitions: {sorted(list(allowed))}"

    new_severity = severity.upper().strip() if severity else inc["severity"]
    if severity and new_severity not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        return None, f"Invalid severity '{severity}'"

    new_operator = operator if operator is not None else inc["operator"]

    now_iso = datetime.now(timezone.utc).isoformat()
    resolved_at = inc["resolved_at"]
    if new_status in {"RESOLVED", "CLOSED"} and not resolved_at:
        resolved_at = now_iso
    elif new_status in {"OPEN", "ACKNOWLEDGED", "IN_PROGRESS"}:
        resolved_at = None

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE incidents
        SET status = ?, severity = ?, operator = ?, updated_at = ?, resolved_at = ?
        WHERE incident_id = ?
    """, (new_status, new_severity, new_operator, now_iso, resolved_at, incident_id))

    # Log history
    if new_status != old_status:
        hist_id = f"hist_{hashlib.sha256(f'{incident_id}_stat_{now_iso}'.encode()).hexdigest()[:12]}"
        cursor.execute("""
            INSERT INTO incident_history (history_id, incident_id, action, old_status, new_status, operator, details, created_at)
            VALUES (?, ?, 'STATUS_CHANGE', ?, ?, ?, ?, ?)
        """, (hist_id, incident_id, old_status, new_status, new_operator, f"Status updated from {old_status} to {new_status}", now_iso))

    if note and note.strip():
        note_id = f"note_{hashlib.sha256(f'{incident_id}_upd_{now_iso}'.encode()).hexdigest()[:12]}"
        cursor.execute("""
            INSERT INTO incident_notes (note_id, incident_id, operator, note_text, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (note_id, incident_id, new_operator, note.strip(), now_iso))

    conn.commit()
    conn.close()

    updated = get_incident_by_id(incident_id)
    return updated, "Incident updated successfully"

def add_incident_note(incident_id: str, note_text: str, operator: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], str]:
    inc = get_incident_by_id(incident_id)
    if not inc:
        return None, f"Incident '{incident_id}' not found"

    now_iso = datetime.now(timezone.utc).isoformat()
    note_id = f"note_{hashlib.sha256(f'{incident_id}_note_{now_iso}'.encode()).hexdigest()[:12]}"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incident_notes (note_id, incident_id, operator, note_text, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (note_id, incident_id, operator, note_text.strip(), now_iso))

    cursor.execute("UPDATE incidents SET updated_at = ? WHERE incident_id = ?", (now_iso, incident_id))

    # Log history
    hist_id = f"hist_{hashlib.sha256(f'{incident_id}_notehist_{now_iso}'.encode()).hexdigest()[:12]}"
    cursor.execute("""
        INSERT INTO incident_history (history_id, incident_id, action, old_status, new_status, operator, details, created_at)
        VALUES (?, ?, 'NOTE_ADDED', NULL, NULL, ?, ?, ?)
    """, (hist_id, incident_id, operator, f"Note added: {note_text[:40]}...", now_iso))

    conn.commit()
    conn.close()

    note_obj = {
        "note_id": note_id,
        "incident_id": incident_id,
        "operator": operator,
        "note_text": note_text.strip(),
        "created_at": now_iso
    }
    return note_obj, "Note added successfully"

def get_incident_stats() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM incidents")
    total_incidents = cursor.fetchone()["total"]

    count_by_status = {}
    cursor.execute("SELECT status, COUNT(*) as cnt FROM incidents GROUP BY status")
    for r in cursor.fetchall():
        count_by_status[r["status"]] = r["cnt"]

    count_by_severity = {}
    cursor.execute("SELECT severity, COUNT(*) as cnt FROM incidents GROUP BY severity")
    for r in cursor.fetchall():
        count_by_severity[r["severity"]] = r["cnt"]

    count_by_event_type = {}
    cursor.execute("""
        SELECT e.event_type, COUNT(*) as cnt
        FROM incidents i
        JOIN events e ON i.event_id = e.event_id
        GROUP BY e.event_type
    """)
    for r in cursor.fetchall():
        count_by_event_type[r["event_type"]] = r["cnt"]

    conn.close()

    return {
        "total_incidents": total_incidents,
        "count_by_status": count_by_status,
        "count_by_severity": count_by_severity,
        "count_by_event_type": count_by_event_type
    }


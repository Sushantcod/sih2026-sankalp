import os
import sqlite3
from typing import Generator

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "events.db")

def get_db_path() -> str:
    os.makedirs(DB_DIR, exist_ok=True)
    return DB_PATH

def get_db_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        source TEXT,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        confidence REAL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    
    # Create indexes for fast query filtering
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_source ON events(source);")
    
    # Create incidents tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
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
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incident_events (
        incident_id TEXT NOT NULL,
        event_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY(incident_id, event_id),
        FOREIGN KEY(incident_id) REFERENCES incidents(incident_id),
        FOREIGN KEY(event_id) REFERENCES events(event_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incident_notes (
        note_id TEXT PRIMARY KEY,
        incident_id TEXT NOT NULL,
        operator TEXT,
        note_text TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(incident_id) REFERENCES incidents(incident_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incident_history (
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
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_incidents_severity ON incidents(severity);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_incidents_event_id ON incidents(event_id);")

    conn.commit()
    conn.close()


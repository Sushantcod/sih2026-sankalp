import os
import sys
import json
import argparse
import time
import requests
from typing import List, Dict, Any

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.backend.database import get_db_connection, init_db
from src.backend.models import insert_single_event
from src.backend.schemas import SUPPORTED_EVENT_TYPES

def load_events_from_file(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Event file not found: {filepath}")
    
    events = []
    if filepath.endswith(".jsonl"):
        with open(filepath, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    events.append(data)
                except Exception as e:
                    print(f"[WARN] Line {line_num}: Failed to parse JSON - {e}")
    elif filepath.endswith(".json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                events = data
            elif isinstance(data, dict):
                if "events" in data and isinstance(data["events"], list):
                    source_str = data.get("source", "anpr_camera")
                    for ev in data["events"]:
                        if isinstance(ev, dict):
                            if "source" not in ev:
                                ev["source"] = source_str
                            if "event_type" not in ev:
                                ev["event_type"] = "plate_detected"
                    events = data["events"]
                else:
                    events = [data]
    else:
        # Attempt to read as jsonl first, then json
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content.startswith("["):
                events = json.loads(content)
            else:
                for line in content.splitlines():
                    if line.strip():
                        events.append(json.loads(line))
    return events

def ingest_via_api(events: List[Dict[str, Any]], api_url: str, batch_size: int = 100) -> Dict[str, int]:
    print(f"[INGEST] Sending {len(events)} events to API endpoint: {api_url}")
    total_ingested = 0
    total_duplicate = 0
    total_failed = 0

    for i in range(0, len(events), batch_size):
        batch = events[i:i + batch_size]
        payload = {"events": batch}
        try:
            resp = requests.post(api_url, json=payload, timeout=30)
            if resp.status_code == 200:
                res = resp.json()
                total_ingested += res.get("ingested_count", 0)
                total_duplicate += res.get("duplicate_count", 0)
                total_failed += res.get("failed_count", 0)
            else:
                print(f"[ERROR] Batch {i//batch_size + 1} HTTP {resp.status_code}: {resp.text}")
                total_failed += len(batch)
        except Exception as e:
            print(f"[ERROR] Batch {i//batch_size + 1} connection failed: {e}")
            total_failed += len(batch)
    
    return {
        "total": len(events),
        "ingested": total_ingested,
        "duplicate": total_duplicate,
        "failed": total_failed
    }

def ingest_via_direct_db(events: List[Dict[str, Any]]) -> Dict[str, int]:
    print(f"[INGEST] Direct Database Ingestion ({len(events)} events)")
    init_db()
    conn = get_db_connection()
    ingested = 0
    duplicate = 0
    failed = 0

    try:
        for idx, event in enumerate(events):
            if not isinstance(event, dict):
                failed += 1
                continue
            e_type = str(event.get("event_type", "")).lower().strip()
            if e_type not in SUPPORTED_EVENT_TYPES:
                failed += 1
                continue
            
            is_dup, _, _ = insert_single_event(conn, event)
            if is_dup:
                duplicate += 1
            else:
                ingested += 1
    finally:
        conn.close()

    return {
        "total": len(events),
        "ingested": ingested,
        "duplicate": duplicate,
        "failed": failed
    }

def main():
    parser = argparse.ArgumentParser(description="CLI Tool to Ingest Telemetry Event Files into Central Backend API")
    parser.add_argument("file", nargs="?", default="outputs/events.jsonl", help="Path to .json or .jsonl file")
    parser.add_argument("--url", default="http://127.0.0.1:8000/events/batch", help="Backend API batch endpoint URL")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch chunk size for API posting")
    parser.add_argument("--direct-db", action="store_true", help="Directly insert into SQLite database without HTTP server")

    args = parser.parse_args()

    start_time = time.time()
    print(f"==================================================")
    print(f"SIH 2026 EVENT INGESTION CLI UTILITY")
    print(f"File: {args.file}")
    print(f"==================================================")

    try:
        events = load_events_from_file(args.file)
        print(f"[LOADED] {len(events)} real events from '{args.file}'")
    except Exception as e:
        print(f"[FATAL] Failed to load event file: {e}")
        sys.exit(1)

    if not events:
        print("[WARN] No events found in file. Exiting.")
        sys.exit(0)

    use_api = not args.direct_db if hasattr(args, "direct_db") else True
    
    # Check if API server is reachable
    if not args.direct_db:
        try:
            health_url = args.url.rsplit("/", 2)[0] + "/health"
            r = requests.get(health_url, timeout=2)
            if r.status_code != 200:
                print(f"[WARN] Backend API health check failed. Falling back to direct database insertion.")
                use_api = False
        except Exception:
            print(f"[INFO] Backend API server not running at {args.url}. Using direct DB ingestion fallback.")
            use_api = False

    if use_api:
        stats = ingest_via_api(events, args.url, args.batch_size)
    else:
        stats = ingest_via_direct_db(events)

    elapsed = time.time() - start_time
    print(f"\n==================================================")
    print(f"INGESTION SUMMARY")
    print(f"Total Processed: {stats['total']}")
    print(f"Successfully Ingested: {stats['ingested']}")
    print(f"Duplicates Skipped:   {stats['duplicate']}")
    print(f"Failed / Invalid:    {stats['failed']}")
    print(f"Time Taken:          {elapsed:.2f} seconds ({stats['total']/max(elapsed, 0.001):.1f} events/sec)")
    print(f"==================================================")

if __name__ == "__main__":
    main()

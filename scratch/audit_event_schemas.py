import os
import json
import glob

def audit_real_events():
    print("=== AUDITING REAL EVENT TELEMETRIES IN WORKSPACE ===")

    events_jsonl = "outputs/events.jsonl"
    anpr_metrics_json = "scratch/ocr_video_metrics.json"

    audited_event_types = {}
    total_events_scanned = 0

    if os.path.exists(events_jsonl):
        print(f"Reading {events_jsonl}...")
        with open(events_jsonl, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    total_events_scanned += 1
                    e_type = data.get("event_type", "unknown")
                    if e_type not in audited_event_types:
                        audited_event_types[e_type] = {
                            "count": 0,
                            "sample_payload": data,
                            "fields_present": set(data.keys()),
                            "gps_status": data.get("gps")
                        }
                    audited_event_types[e_type]["count"] += 1
                    audited_event_types[e_type]["fields_present"].update(data.keys())
                except Exception as e:
                    print(f"Line {line_no} JSON error: {e}")

    # Check ANPR metrics
    anpr_events = []
    if os.path.exists(anpr_metrics_json):
        print(f"Reading {anpr_metrics_json}...")
        with open(anpr_metrics_json, "r", encoding="utf-8") as f:
            anpr_data = json.load(f)
            # ANPR summary metrics
            print("ANPR Metrics Keys:", list(anpr_data.keys()))

    print(f"\nTotal Real Events Scanned in events.jsonl: {total_events_scanned}")
    print("\nEvent Types Breakdown:")
    for e_type, info in audited_event_types.items():
        print(f"\n--- Event Type: '{e_type}' ({info['count']} instances) ---")
        print(f"  Fields: {sorted(list(info['fields_present']))}")
        print(f"  Sample GPS Value: {info['gps_status']}")
        print(f"  Sample Record: {json.dumps(info['sample_payload'], indent=2)[:300]}...")

if __name__ == "__main__":
    audit_real_events()

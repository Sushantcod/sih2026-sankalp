import os
import sys
import unittest
import tempfile
from fastapi.testclient import TestClient

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.app import app
from src.backend.database import get_db_connection, init_db, DB_PATH
import src.backend.database as db_mod

client = TestClient(app)

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for isolated testing
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()
        
        # Override DB_PATH in database module
        self.original_db_path = db_mod.DB_PATH
        db_mod.DB_PATH = self.temp_db_path
        
        # Initialize test DB
        init_db()

    def tearDown(self):
        # Restore original DB_PATH and cleanup temp file
        db_mod.DB_PATH = self.original_db_path
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except Exception:
                pass

    def test_root_endpoint(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("service", data)
        self.assertEqual(data["status"], "online")
        self.assertIn("supported_event_types", data)

    def test_health_check(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["database"], "connected")

    def test_empty_database_queries(self):
        # GET /events on empty DB
        response = client.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # GET /stats on empty DB
        response = client.get("/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_events"], 0)
        self.assertEqual(data["count_by_type"], {})

    def test_single_event_ingestion(self):
        payload = {
            "event_id": "test_pothole_001",
            "event_type": "pothole",
            "timestamp": "2026-09-14T10:00:00Z",
            "source": "bus_01",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "confidence": 0.94,
            "severity": "high"
        }
        response = client.post("/events", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ingested")
        self.assertEqual(data["event_id"], "test_pothole_001")
        self.assertFalse(data["is_duplicate"])

    def test_unsupported_event_type_rejection(self):
        payload = {
            "event_id": "invalid_001",
            "event_type": "alien_spacecraft",
            "timestamp": "2026-09-14T10:00:00Z",
            "source": "bus_01"
        }
        response = client.post("/events", json=payload)
        # Should fail with 422 validation error
        self.assertEqual(response.status_code, 422)

    def test_duplicate_event_handling(self):
        payload = {
            "event_id": "test_dup_001",
            "event_type": "vehicle_count",
            "timestamp": "2026-09-14T10:05:00Z",
            "source": "cam_02",
            "vehicle_count": 42
        }
        # First ingestion
        r1 = client.post("/events", json=payload)
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json()["status"], "ingested")

        # Second ingestion with same event_id
        r2 = client.post("/events", json=payload)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json()["status"], "duplicate")
        self.assertTrue(r2.json()["is_duplicate"])

        # Check total count in DB remains 1
        stats = client.get("/stats").json()
        self.assertEqual(stats["total_events"], 1)

    def test_batch_ingestion(self):
        batch = {
            "events": [
                {
                    "event_id": "batch_001",
                    "event_type": "pothole",
                    "timestamp": "2026-09-14T10:10:00Z",
                    "source": "bus_01",
                    "confidence": 0.88
                },
                {
                    "event_id": "batch_002",
                    "event_type": "congestion",
                    "timestamp": "2026-09-14T10:11:00Z",
                    "source": "cam_01",
                    "density_level": "heavy"
                },
                {
                    "event_id": "batch_003",
                    "event_type": "plate_detected",
                    "timestamp": "2026-09-14T10:12:00Z",
                    "source": "anpr_cam_01",
                    "recognized_text": "MH01AB1234",
                    "ocr_confidence": 0.95
                }
            ]
        }
        response = client.post("/events/batch", json=batch)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_received"], 3)
        self.assertEqual(data["ingested_count"], 3)
        self.assertEqual(data["duplicate_count"], 0)
        self.assertEqual(data["failed_count"], 0)

    def test_query_filtering_and_retrieval(self):
        # Insert test events
        e1 = {
            "event_id": "q_001",
            "event_type": "pothole",
            "timestamp": "2026-09-14T08:00:00Z",
            "source": "bus_A"
        }
        e2 = {
            "event_id": "q_002",
            "event_type": "alligator_crack",
            "timestamp": "2026-09-14T09:00:00Z",
            "source": "bus_A"
        }
        e3 = {
            "event_id": "q_003",
            "event_type": "pothole",
            "timestamp": "2026-09-14T10:00:00Z",
            "source": "bus_B"
        }
        client.post("/events/batch", json={"events": [e1, e2, e3]})

        # Filter by event_type=pothole
        r = client.get("/events?event_type=pothole")
        self.assertEqual(r.status_code, 200)
        results = r.json()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(item["event_type"] == "pothole" for item in results))

        # Filter by source=bus_A
        r = client.get("/events?source=bus_A")
        self.assertEqual(r.status_code, 200)
        results = r.json()
        self.assertEqual(len(results), 2)

        # GET single event by ID
        r = client.get("/events/q_002")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["event_id"], "q_002")
        self.assertEqual(r.json()["event_type"], "alligator_crack")

    def test_get_nonexistent_event(self):
        response = client.get("/events/nonexistent_id_999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"].lower())

    def test_database_stats(self):
        events = [
            {"event_id": "s1", "event_type": "pothole", "timestamp": "2026-09-14T01:00:00Z", "source": "bus1"},
            {"event_id": "s2", "event_type": "pothole", "timestamp": "2026-09-14T02:00:00Z", "source": "bus1"},
            {"event_id": "s3", "event_type": "vehicle_count", "timestamp": "2026-09-14T03:00:00Z", "source": "cam1"},
        ]
        client.post("/events/batch", json={"events": events})

        response = client.get("/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_events"], 3)
        self.assertEqual(data["count_by_type"]["pothole"], 2)
        self.assertEqual(data["count_by_type"]["vehicle_count"], 1)

    # Incident Management Tests

    def test_incident_creation_and_retrieval(self):
        # 1. First ingest a real event
        e = {"event_id": "real_evt_101", "event_type": "pothole", "timestamp": "2026-09-14T05:00:00Z", "source": "bus_10"}
        client.post("/events", json=e)

        # 2. Create incident from real event_id
        inc_payload = {
            "event_id": "real_evt_101",
            "title": "Severe Pothole on Main St",
            "severity": "HIGH",
            "operator": "Operator_Alpha",
            "initial_note": "Field inspection dispatched"
        }
        res = client.post("/incidents", json=inc_payload)
        self.assertEqual(res.status_code, 201)
        inc_data = res.json()
        self.assertEqual(inc_data["status"], "OPEN")
        self.assertEqual(inc_data["severity"], "HIGH")
        self.assertEqual(inc_data["event_id"], "real_evt_101")
        self.assertEqual(len(inc_data["notes"]), 1)
        self.assertEqual(inc_data["notes"][0]["note_text"], "Field inspection dispatched")

        # 3. Retrieve single incident
        inc_id = inc_data["incident_id"]
        res_get = client.get(f"/incidents/{inc_id}")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["incident_id"], inc_id)

    def test_incident_creation_invalid_event_id(self):
        inc_payload = {
            "event_id": "non_existent_event_9999",
            "title": "Fake Incident",
            "severity": "HIGH"
        }
        res = client.post("/incidents", json=inc_payload)
        self.assertEqual(res.status_code, 404)
        self.assertIn("does not exist", res.json()["detail"])

    def test_incident_valid_and_invalid_status_transitions(self):
        # Ingest event & create incident
        client.post("/events", json={"event_id": "evt_trans_01", "event_type": "alligator_crack", "source": "bus_1"})
        inc_res = client.post("/incidents", json={"event_id": "evt_trans_01", "severity": "MEDIUM"})
        inc_id = inc_res.json()["incident_id"]

        # Valid transition: OPEN -> ACKNOWLEDGED
        patch1 = client.patch(f"/incidents/{inc_id}", json={"status": "ACKNOWLEDGED", "operator": "Operator_Beta"})
        self.assertEqual(patch1.status_code, 200)
        self.assertEqual(patch1.json()["status"], "ACKNOWLEDGED")

        # Valid transition: ACKNOWLEDGED -> IN_PROGRESS
        patch2 = client.patch(f"/incidents/{inc_id}", json={"status": "IN_PROGRESS"})
        self.assertEqual(patch2.status_code, 200)
        self.assertEqual(patch2.json()["status"], "IN_PROGRESS")

        # Invalid transition: IN_PROGRESS -> ACKNOWLEDGED (backward transition disallowed)
        patch_bad = client.patch(f"/incidents/{inc_id}", json={"status": "ACKNOWLEDGED"})
        self.assertEqual(patch_bad.status_code, 400)
        self.assertIn("Invalid status transition", patch_bad.json()["detail"])

        # Valid transition: IN_PROGRESS -> RESOLVED
        patch3 = client.patch(f"/incidents/{inc_id}", json={"status": "RESOLVED"})
        self.assertEqual(patch3.status_code, 200)
        self.assertEqual(patch3.json()["status"], "RESOLVED")
        self.assertIsNotNone(patch3.json()["resolved_at"])

    def test_incident_notes_and_history(self):
        client.post("/events", json={"event_id": "evt_note_01", "event_type": "manhole", "source": "bus_2"})
        inc_res = client.post("/incidents", json={"event_id": "evt_note_01"})
        inc_id = inc_res.json()["incident_id"]

        # Add note
        note_res = client.post(f"/incidents/{inc_id}/notes", json={"note_text": "Crews arriving on scene", "operator": "Tech_1"})
        self.assertEqual(note_res.status_code, 201)
        self.assertEqual(note_res.json()["note_text"], "Crews arriving on scene")

        # Check history
        hist_res = client.get(f"/incidents/{inc_id}/history")
        self.assertEqual(hist_res.status_code, 200)
        self.assertTrue(len(hist_res.json()) >= 2) # CREATED + NOTE_ADDED

    def test_incident_stats_summary(self):
        client.post("/events", json={"event_id": "evt_stat_01", "event_type": "pothole", "source": "bus_3"})
        client.post("/incidents", json={"event_id": "evt_stat_01", "severity": "CRITICAL"})

        stats_res = client.get("/incidents/stats/summary")
        self.assertEqual(stats_res.status_code, 200)
        st = stats_res.json()
        self.assertTrue(st["total_incidents"] >= 1)
        self.assertIn("CRITICAL", st["count_by_severity"])

if __name__ == "__main__":
    unittest.main()


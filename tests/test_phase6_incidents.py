import os
import sys
import unittest
import tempfile
from fastapi.testclient import TestClient

# Ensure project root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.app import app
from src.backend.database import get_db_connection, init_db
import src.backend.database as db_mod

client = TestClient(app)


class TestPhase6IncidentManagement(unittest.TestCase):
    """
    Phase 6 Incident Management Test Suite.
    Runs strictly against an isolated temporary database to prevent
    production data contamination.
    """
    def setUp(self):
        # Create a temporary database file for isolated testing
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()

        # Override DB_PATH in database module to target isolated test database
        self.original_db_path = db_mod.DB_PATH
        db_mod.DB_PATH = self.temp_db_path

        # Initialize schema in test database
        init_db()

        # Insert a valid test telemetry event into the isolated test database
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO events (event_id, event_type, source, timestamp, latitude, longitude, confidence, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                "evt_test_pothole_001",
                "pothole",
                "BUS-101",
                "2026-09-14T10:00:00Z",
                None,  # Null GPS
                None,  # Null GPS
                0.92,
                '{"defect_type": "pothole", "severity": "HIGH", "confidence": 0.92}'
            )
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        # Restore original DB_PATH and delete temporary database file
        db_mod.DB_PATH = self.original_db_path
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except Exception:
                pass

    def test_01_empty_incident_database_queries(self):
        """Verify incident endpoints on empty isolated test database."""
        response = client.get("/incidents")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        stats_resp = client.get("/incidents/stats/summary")
        self.assertEqual(stats_resp.status_code, 200)
        data = stats_resp.json()
        self.assertEqual(data["total_incidents"], 0)
        self.assertEqual(data["count_by_status"], {})

    def test_02_create_incident_valid_event(self):
        """Verify creating an incident from an existing real event_id."""
        payload = {
            "event_id": "evt_test_pothole_001",
            "title": "Severe Pothole Reported",
            "description": "Hazardous road defect detected on main transit route",
            "severity": "HIGH",
            "operator": "Officer_Test",
            "initial_note": "Dispatched inspection unit"
        }
        response = client.post("/incidents", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data["incident_id"].startswith("inc_"))
        self.assertEqual(data["event_id"], "evt_test_pothole_001")
        self.assertEqual(data["status"], "OPEN")
        self.assertEqual(data["severity"], "HIGH")
        self.assertEqual(data["operator"], "Officer_Test")
        self.assertIsNone(data["event"]["latitude"])
        self.assertIsNone(data["event"]["longitude"])

    def test_03_create_incident_invalid_event_404(self):
        """Verify 404 Not Found when creating an incident with a non-existent event_id."""
        payload = {
            "event_id": "non_existent_event_999",
            "title": "Invalid Incident"
        }
        response = client.post("/incidents", json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", response.json()["detail"])

    def test_04_duplicate_incident_creation_protection_400(self):
        """Verify duplicate incident creation prevention for the same event_id."""
        payload = {
            "event_id": "evt_test_pothole_001",
            "title": "Pothole Incident 1"
        }
        # First creation succeeds
        resp1 = client.post("/incidents", json=payload)
        self.assertEqual(resp1.status_code, 201)

        # Second creation for same event_id must fail with 400 Bad Request
        resp2 = client.post("/incidents", json=payload)
        self.assertEqual(resp2.status_code, 400)
        self.assertIn("already exists", resp2.json()["detail"])

    def test_05_valid_status_lifecycle_transitions(self):
        """Verify valid state machine transitions: OPEN -> ACKNOWLEDGED -> IN_PROGRESS -> RESOLVED -> CLOSED."""
        create_resp = client.post("/incidents", json={"event_id": "evt_test_pothole_001", "title": "Test Incident"})
        inc_id = create_resp.json()["incident_id"]

        # OPEN -> ACKNOWLEDGED
        r1 = client.patch(f"/incidents/{inc_id}", json={"status": "ACKNOWLEDGED", "note": "Acknowledged by dispatch"})
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json()["status"], "ACKNOWLEDGED")

        # ACKNOWLEDGED -> IN_PROGRESS
        r2 = client.patch(f"/incidents/{inc_id}", json={"status": "IN_PROGRESS", "note": "Repair crew en route"})
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json()["status"], "IN_PROGRESS")

        # IN_PROGRESS -> RESOLVED
        r3 = client.patch(f"/incidents/{inc_id}", json={"status": "RESOLVED", "note": "Pothole filled and sealed"})
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(r3.json()["status"], "RESOLVED")
        self.assertIsNotNone(r3.json()["resolved_at"])

        # RESOLVED -> CLOSED
        r4 = client.patch(f"/incidents/{inc_id}", json={"status": "CLOSED", "note": "Verification audit complete"})
        self.assertEqual(r4.status_code, 200)
        self.assertEqual(r4.json()["status"], "CLOSED")

    def test_06_invalid_status_transition_rejection_400(self):
        """Verify rejection of invalid state transitions (e.g. OPEN -> CLOSED, OPEN -> RESOLVED)."""
        create_resp = client.post("/incidents", json={"event_id": "evt_test_pothole_001", "title": "Test Incident"})
        inc_id = create_resp.json()["incident_id"]

        # Invalid: OPEN -> CLOSED (Must be rejected)
        r1 = client.patch(f"/incidents/{inc_id}", json={"status": "CLOSED"})
        self.assertEqual(r1.status_code, 400)
        self.assertIn("Invalid status transition", r1.json()["detail"])

        # Invalid: OPEN -> RESOLVED (Must be rejected)
        r2 = client.patch(f"/incidents/{inc_id}", json={"status": "RESOLVED"})
        self.assertEqual(r2.status_code, 400)
        self.assertIn("Invalid status transition", r2.json()["detail"])

    def test_07_add_incident_note(self):
        """Verify adding an operator note to an incident."""
        create_resp = client.post("/incidents", json={"event_id": "evt_test_pothole_001", "title": "Test Note Incident"})
        inc_id = create_resp.json()["incident_id"]

        note_payload = {
            "note_text": "Road crew inspected site at 10:30 AM",
            "operator": "Inspector_Ramesh"
        }
        note_resp = client.post(f"/incidents/{inc_id}/notes", json=note_payload)
        self.assertEqual(note_resp.status_code, 201)
        data = note_resp.json()
        self.assertEqual(data["incident_id"], inc_id)
        self.assertEqual(data["note_text"], "Road crew inspected site at 10:30 AM")
        self.assertEqual(data["operator"], "Inspector_Ramesh")

    def test_08_get_incident_history_audit_trail(self):
        """Verify retrieving the complete audit trail history for an incident."""
        create_resp = client.post("/incidents", json={"event_id": "evt_test_pothole_001", "title": "Audit Test"})
        inc_id = create_resp.json()["incident_id"]

        # Perform status change
        client.patch(f"/incidents/{inc_id}", json={"status": "ACKNOWLEDGED", "note": "State change 1"})

        history_resp = client.get(f"/incidents/{inc_id}/history")
        self.assertEqual(history_resp.status_code, 200)
        history = history_resp.json()
        self.assertGreaterEqual(len(history), 2)  # CREATED + STATUS_CHANGE
        self.assertEqual(history[0]["action"], "CREATED")
        self.assertEqual(history[1]["action"], "STATUS_CHANGE")
        self.assertEqual(history[1]["old_status"], "OPEN")
        self.assertEqual(history[1]["new_status"], "ACKNOWLEDGED")

    def test_09_query_and_filter_incidents(self):
        """Verify listing and filtering incidents by status and severity."""
        client.post("/incidents", json={"event_id": "evt_test_pothole_001", "title": "Filter Test", "severity": "CRITICAL"})

        # Filter by status=OPEN
        r1 = client.get("/incidents?status=OPEN")
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(len(r1.json()), 1)

        # Filter by status=RESOLVED (should return empty list)
        r2 = client.get("/incidents?status=RESOLVED")
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(len(r2.json()), 0)

        # Filter by severity=CRITICAL
        r3 = client.get("/incidents?severity=CRITICAL")
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(len(r3.json()), 1)

    def test_10_linked_event_payload_retrieval(self):
        """Verify incident response includes the linked telemetry event and payload."""
        create_resp = client.post("/incidents", json={"event_id": "evt_test_pothole_001", "title": "Linked Event Test"})
        inc_id = create_resp.json()["incident_id"]

        inc_resp = client.get(f"/incidents/{inc_id}")
        self.assertEqual(inc_resp.status_code, 200)
        inc_data = inc_resp.json()
        self.assertIn("event", inc_data)
        self.assertEqual(inc_data["event"]["event_id"], "evt_test_pothole_001")
        self.assertEqual(inc_data["event"]["event_type"], "pothole")
        self.assertEqual(inc_data["event"]["source"], "BUS-101")


if __name__ == "__main__":
    unittest.main()

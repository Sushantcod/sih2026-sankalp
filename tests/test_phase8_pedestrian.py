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


class TestPhase8PedestrianAnalytics(unittest.TestCase):
    """
    Phase 8 Pedestrian Safety Analytics & Availability Indicators Test Suite.
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

        # Insert sample person telemetry event into isolated test database
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO events (event_id, event_type, source, timestamp, latitude, longitude, confidence, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                "evt_test_person_200",
                "person",
                "BUS-101",
                "2026-09-14T10:10:00Z",
                None,
                None,
                0.89,
                '{"class": "person", "confidence": 0.89}'
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

    def test_01_analytics_pedestrians_endpoint(self):
        """Verify GET /analytics/pedestrians returns pedestrian metrics and availability indicators."""
        response = client.get("/analytics/pedestrians")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data["status"], ["active", "unavailable"])
        self.assertEqual(data["indicator"], "PEDESTRIAN SAFETY ANALYTICS")
        self.assertGreaterEqual(data["person_events_logged"], 1)
        self.assertIn("data_availability", data)
        self.assertIn("school_zone_context", data["data_availability"])
        self.assertIn("pedestrian_risk_assessment", data["data_availability"])

    def test_02_analytics_pedestrians_safety_endpoint(self):
        """Verify GET /analytics/pedestrians/safety returns honest status indicators."""
        response = client.get("/analytics/pedestrians/safety")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "unavailable")
        self.assertEqual(data["indicator"], "SCHOOL-ZONE & PEDESTRIAN RISK")
        self.assertIn("School-Zone Context Unavailable", data["school_zone_status"])
        self.assertIn("Pedestrian Risk Assessment", data["risk_assessment_status"])

    def test_03_empty_database_pedestrian_analytics(self):
        """Verify pedestrian analytics on an empty isolated test database."""
        conn = get_db_connection()
        conn.execute("DELETE FROM events")
        conn.commit()
        conn.close()

        response = client.get("/analytics/pedestrians")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["person_events_logged"], 0)


if __name__ == "__main__":
    unittest.main()

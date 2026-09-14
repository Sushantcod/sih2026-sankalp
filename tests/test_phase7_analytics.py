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


class TestPhase7TrafficAnalytics(unittest.TestCase):
    """
    Phase 7 Traffic Analytics & Telemetry Indicators Test Suite.
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

        # Insert sample telemetry events into isolated test database
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO events (event_id, event_type, source, timestamp, latitude, longitude, confidence, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                "evt_test_pothole_100",
                "pothole",
                "BUS-101",
                "2026-09-14T10:00:00Z",
                None,
                None,
                0.95,
                '{"defect_type": "pothole"}'
            )
        )
        conn.execute(
            """
            INSERT INTO events (event_id, event_type, source, timestamp, latitude, longitude, confidence, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                "evt_test_veh_101",
                "vehicle_count",
                "traffic_density_bridge.mp4",
                "2026-09-14T10:05:00Z",
                None,
                None,
                0.88,
                '{"total_vehicle_count": 14, "vehicle_counts": {"car": 10, "bus": 2, "truck": 1, "motorcycle": 1}}'
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

    def test_01_analytics_traffic_endpoint(self):
        """Verify GET /analytics/traffic returns aggregated metrics and availability indicators."""
        response = client.get("/analytics/traffic")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_events"], 2)
        self.assertEqual(data["total_road_defects"], 1)
        self.assertEqual(data["total_vehicles_counted"], 14)
        self.assertEqual(data["class_distribution"]["car"], 10)
        self.assertIn("data_availability", data)
        self.assertIn("O-D Analysis Unavailable", data["data_availability"]["od_analysis"])
        self.assertIn("Route Delay Unavailable", data["data_availability"]["route_delay"])

    def test_02_analytics_summary_endpoint(self):
        """Verify GET /analytics/summary endpoint response."""
        response = client.get("/analytics/summary")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_events"], 2)
        self.assertEqual(data["total_incidents"], 0)

    def test_03_analytics_od_endpoint_honest_status(self):
        """Verify GET /analytics/od returns honest unavailable status."""
        response = client.get("/analytics/od")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "unavailable")
        self.assertEqual(data["indicator"], "O-D ANALYSIS")
        self.assertIn("O-D Analysis Unavailable", data["message"])

    def test_04_analytics_delay_endpoint_honest_status(self):
        """Verify GET /analytics/delay returns honest unavailable status."""
        response = client.get("/analytics/delay")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "unavailable")
        self.assertEqual(data["indicator"], "ROUTE DELAY")
        self.assertIn("Route Delay Unavailable", data["message"])

    def test_05_empty_database_analytics(self):
        """Verify analytics endpoints on an empty isolated database."""
        # Clear test database
        conn = get_db_connection()
        conn.execute("DELETE FROM events")
        conn.commit()
        conn.close()

        response = client.get("/analytics/traffic")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_events"], 0)
        self.assertEqual(data["total_vehicles_counted"], 0)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import json
import sqlite3
import unittest
import requests

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TestDashboard(unittest.TestCase):
    def test_01_dashboard_files_exist(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        dash_dir = os.path.join(root_dir, "src", "dashboard")
        
        self.assertTrue(os.path.exists(os.path.join(dash_dir, "index.html")), "index.html missing")
        self.assertTrue(os.path.exists(os.path.join(dash_dir, "styles.css")), "styles.css missing")
        self.assertTrue(os.path.exists(os.path.join(dash_dir, "app.js")), "app.js missing")

    def test_02_backend_api_integration(self):
        # Health endpoint
        r_health = requests.get("http://127.0.0.1:8000/health", timeout=5)
        self.assertEqual(r_health.status_code, 200)
        self.assertEqual(r_health.json()["status"], "ok")

        # Stats endpoint
        r_stats = requests.get("http://127.0.0.1:8000/stats", timeout=5)
        self.assertEqual(r_stats.status_code, 200)
        stats = r_stats.json()
        self.assertIn("total_events", stats)
        self.assertEqual(stats["total_events"], 7964)

        # Query events endpoint
        r_events = requests.get("http://127.0.0.1:8000/events?limit=10", timeout=5)
        self.assertEqual(r_events.status_code, 200)
        events = r_events.json()
        self.assertEqual(len(events), 10)

    def test_03_zero_fabricated_coordinates_in_code(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        app_js_path = os.path.join(root_dir, "src", "dashboard", "app.js")
        
        with open(app_js_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Verify no random coordinate generation functions exist
        self.assertNotIn("Math.random() *", code)
        self.assertNotIn("generateRandomGps", code)
        self.assertNotIn("fakeGps", code)
        self.assertNotIn("syntheticCoordinates", code)

    def test_04_database_gps_null_state(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        db_path = os.path.join(root_dir, "data", "events.db")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM events WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
        mapped_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM events WHERE latitude IS NULL OR longitude IS NULL")
        unmapped_count = cursor.fetchone()[0]
        
        conn.close()

        self.assertEqual(mapped_count, 0, "Mapped events should be 0 based on real edge video telemetry")
        self.assertEqual(unmapped_count, 7964, "All 7,964 events must be cleanly unmapped (null GPS)")

    def test_05_dashboard_http_server_response(self):
        r_dash = requests.get("http://127.0.0.1:3000/index.html", timeout=5)
        self.assertEqual(r_dash.status_code, 200)
        self.assertIn("SIH 2026", r_dash.text)
        self.assertIn("Smart Road Monitoring", r_dash.text)

if __name__ == "__main__":
    unittest.main()

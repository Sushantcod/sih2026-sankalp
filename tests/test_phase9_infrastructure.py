#!/usr/bin/env python3
"""
Tests for Phase 9 Infrastructure & Traffic-Sign Intelligence Subsystem
======================================================================
Verifies model presence, SHA256 integrity, backend endpoint, dataset splits,
database protection (7,964 baseline events), and regression protection.
"""

import os
import sys
import unittest
import hashlib
import sqlite3
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from src.backend.app import app


class TestPhase9Infrastructure(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.db_path = os.path.join(PROJECT_ROOT, "data/events.db")
        cls.infra_model_path = os.path.join(PROJECT_ROOT, "models/infrastructure/infrastructure_detector.pt")
        cls.pothole_model_path = os.path.join(PROJECT_ROOT, "models/pothole.pt")
        cls.anpr_model_path = os.path.join(PROJECT_ROOT, "models/anpr/best.pt")
        cls.yolo_model_path = os.path.join(PROJECT_ROOT, "models/yolov8n.pt")
        cls.ped_model_path = os.path.join(PROJECT_ROOT, "models/pedestrian/pedestrian_detector.pt")

    def test_01_frozen_models_sha256_integrity(self):
        """Verify frozen Phase 1-8 model weights remain unaltered."""
        expected_hashes = {
            self.pothole_model_path: "947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b",
            self.anpr_model_path: "d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a",
            self.yolo_model_path: "f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36",
            self.ped_model_path: "18d6e7c72fccde6dec294b02ab5c06ee73c89302f319234f857c7915549b1c9d"
        }

        for path, expected_sha in expected_hashes.items():
            self.assertTrue(os.path.exists(path), f"Model path {path} does not exist!")
            hasher = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            actual_sha = hasher.hexdigest()
            self.assertEqual(actual_sha, expected_sha, f"Model SHA256 mismatch for {path}!")

    def test_02_database_protection_baseline_count(self):
        """Verify baseline database event count remains protected at 7,964."""
        self.assertTrue(os.path.exists(self.db_path), "Database data/events.db missing!")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        total = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(total, 7964, f"Database count altered! Expected 7964, got {total}")

    def test_03_dataset_split_integrity(self):
        """Verify Phase 9 dataset directories and splits exist."""
        dataset_dir = os.path.join(PROJECT_ROOT, "infrastructure_info/infrastructure")
        self.assertTrue(os.path.exists(os.path.join(dataset_dir, "train/images")), "Train images missing")
        self.assertTrue(os.path.exists(os.path.join(dataset_dir, "valid/images")), "Valid images missing")
        self.assertTrue(os.path.exists(os.path.join(dataset_dir, "test/images")), "Test images missing")

    def test_04_backend_analytics_infrastructure_endpoint(self):
        """Test GET /analytics/infrastructure endpoint returns valid status."""
        resp = self.client.get("/analytics/infrastructure")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("status", data)
        self.assertIn("indicator", data)
        self.assertIn("data_availability", data)

    def test_05_honest_gps_null_handling(self):
        """Verify no fake GPS coordinates exist in telemetry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events WHERE latitude IS NOT NULL OR longitude IS NOT NULL")
        gps_count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(gps_count, 0, f"Found {gps_count} non-null GPS records! Must be 0.")

    def test_06_derived_stratified_dataset_and_model_integrity(self):
        """Verify derived stratified dataset and new model SHA256 checksum."""
        derived_yaml = os.path.join(PROJECT_ROOT, "data/infrastructure_stratified/data.yaml")
        self.assertTrue(os.path.exists(derived_yaml), "Derived dataset data.yaml missing!")
        self.assertTrue(os.path.exists(self.infra_model_path), "Infrastructure model missing!")

        hasher = hashlib.sha256()
        with open(self.infra_model_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        actual_sha = hasher.hexdigest()
        expected_sha = "7a71cdee3c8e382de5debe220abd8ee499b6806e45255dba80d69fb453c35837"
        self.assertEqual(actual_sha, expected_sha, f"Model SHA256 mismatch! Got {actual_sha}")


if __name__ == "__main__":
    unittest.main()


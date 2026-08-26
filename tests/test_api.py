import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.demo_data import DEMO_AOI
from backend.app.main import app


class APITests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_and_demo_analysis_contract(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)
        response = self.client.post("/api/satellite/analyze", json={"mode": "demo", "aoi": DEMO_AOI, "period_days": 90, "cloud_max": 30})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["data_status"], "DEMO DATA")
        self.assertEqual(payload["detections"]["type"], "FeatureCollection")
        self.assertGreater(len(payload["detections"]["features"]), 0)

    def test_geojson_export_is_downloadable(self):
        response = self.client.get("/api/export/geojson")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["type"], "FeatureCollection")

    def test_coordinate_search_uses_latitude_then_longitude(self):
        response = self.client.get("/api/geocode?q=23.6854,%2086.4512")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["latitude"], 23.6854)
        self.assertEqual(response.json()["longitude"], 86.4512)

    def test_kml_gpx_and_report_exports(self):
        self.assertIn("<Polygon>", self.client.get("/api/export/kml").text)
        self.assertIn("<trk>", self.client.get("/api/export/gpx").text)
        response = self.client.post("/api/reports/generate", json={"case_id": "KN-2026-001"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b"%PDF"))
        Path("exports/kn-2026-001-evidence-report.pdf").unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

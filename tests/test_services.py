import unittest

from backend.app.services.risk_service import calculate_risk
from backend.app.services.satellite_service import filter_observations
from backend.app.services.truck_service import evidence_for, route_for


class ServiceTests(unittest.TestCase):
    def test_date_and_cloud_filtering(self):
        items = filter_observations("2026-06-01", "2026-06-30", 15)
        self.assertEqual([item["id"] for item in items], ["DEMO-S2-2026-06-03", "DEMO-S2-2026-06-25"])

    def test_risk_is_explainable_and_bounded(self):
        result = calculate_risk(probability=.92, change_percentage=61.5, outside_percentage=46, protected_percentage=18, affected_area_ha=7.1, drone_mismatch=True, transport_anomalies=3)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertIn("Mining probability", result["breakdown"])
        self.assertEqual(result["level"], "HIGH")

    def test_route_deviation_and_rfid_evidence(self):
        route = route_for("TRK-SK-1042")
        self.assertTrue(route["anomaly"])
        self.assertEqual(route["distance_difference_km"], 16.0)
        self.assertGreaterEqual(evidence_for()["anomaly_count"], 3)


if __name__ == "__main__":
    unittest.main()

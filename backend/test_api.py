import sys
import os
from fastapi.testclient import TestClient

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app

client = TestClient(app)

def test_api_endpoints():
    print("==================================================")
    print("      KHANAN-NETRA FASTAPI ENDPOINTS TEST         ")
    print("==================================================")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200
    print(f"[GET /api/health] Status: {res.status_code} | Output: {res.json()}")

    # 2. Detections list
    res = client.get("/api/detections")
    assert res.status_code == 200
    detections = res.json()
    print(f"[GET /api/detections] Status: {res.status_code} | Count: {len(detections)}")

    # 3. Detection by ID
    res = client.get("/api/detections/KN-0001")
    assert res.status_code == 200
    print(f"[GET /api/detections/KN-0001] Status: {res.status_code} | Legal Status: {res.json()['legal_status']}")

    # 4. Risk assessments
    res = client.get("/api/risk")
    assert res.status_code == 200
    risks = res.json()
    print(f"[GET /api/risk] Status: {res.status_code} | Count: {len(risks)}")

    # 5. Risk by ID
    res = client.get("/api/risk/KN-0004")
    assert res.status_code == 200
    risk_4 = res.json()
    print(f"[GET /api/risk/KN-0004] Status: {res.status_code} | Score: {risk_4['risk_score']} | Level: {risk_4['risk_level']}")

    # 6. Permits
    res = client.get("/api/permits")
    assert res.status_code == 200
    print(f"[GET /api/permits] Status: {res.status_code} | Count: {len(res.json())}")

    # 7. Trucks
    res = client.get("/api/trucks")
    assert res.status_code == 200
    print(f"[GET /api/trucks] Status: {res.status_code} | Count: {len(res.json())}")

    # 8. Routes
    res = client.get("/api/routes")
    assert res.status_code == 200
    print(f"[GET /api/routes] Status: {res.status_code} | Count: {len(res.json())}")

    # 9. Satellite Analysis Endpoint
    sat_payload = {
        "latitude": 23.6600,
        "longitude": 86.5400,
        "area_ha": 3.8,
        "ndvi_change": -0.85,
        "sar_vv_vh_ratio": 0.92,
        "texture_variance": 0.88,
        "drone_estimated_volume_m3": 45000.0
    }
    res = client.post("/api/satellite/analyze", json=sat_payload)
    assert res.status_code == 200
    analysis = res.json()
    print(f"[POST /api/satellite/analyze] Status: {res.status_code} | Generated Risk Score: {analysis['risk_score']} | Level: {analysis['risk_level']}")

    print("\n==================================================")
    print("  ALL FASTAPI ENDPOINTS VERIFIED SUCCESSFULLY!   ")
    print("==================================================")

if __name__ == "__main__":
    test_api_endpoints()

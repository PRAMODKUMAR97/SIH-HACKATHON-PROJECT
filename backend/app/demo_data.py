"""Deterministic synthetic data. Never represents real satellite observations."""
from datetime import date, timedelta
import random

STATUSES = ["ILLEGAL — PROTECTED AREA", "ILLEGAL — INDIGENOUS/COMMUNITY AREA", "ILLEGAL — OUTSIDE PERMIT", "LEGAL — WITHIN PERMIT", "PENDING — NEEDS VERIFICATION"]
PROTECTION = ["Protected Area", "Community Area", "Outside Permit", "Mining Permit", "Unverified"]

def build_detections():
    random.seed(20260826)
    rows = []
    base = date(2026, 8, 25)
    for i in range(42):
        status = STATUSES[i % len(STATUSES)]
        probability = round(random.uniform(.53, .98), 2)
        area = round(random.uniform(.18, 18.6), 2)
        protected = "PROTECTED" in status or "COMMUNITY" in status
        risk = min(99, round(probability * 55 + min(area, 15) * 1.7 + (26 if protected else 14 if "OUTSIDE" in status else 4)))
        level = "HIGH" if risk >= 76 else "MEDIUM" if risk >= 51 else "LOW"
        rows.append({
            "id": f"KN-2026-{i+1:03d}", "date": str(base - timedelta(days=(i * 3) % 60)),
            "latitude": round(23.29 + random.uniform(-.19, .19), 5), "longitude": round(82.12 + random.uniform(-.24, .24), 5),
            "area_ha": area, "probability": probability, "status": status,
            "protection": PROTECTION[STATUSES.index(status)], "risk": risk, "risk_level": level,
            "change_db": round(random.uniform(-5.4, -0.7), 1), "source": "Sentinel-1 + Sentinel-2 (synthetic demo)",
            "history": [{"date": str(base-timedelta(days=d)), "probability": round(max(.2, probability-random.uniform(0,.25)),2), "area": round(max(.1,area-random.uniform(0,3)),2)} for d in (60,45,30,15,0)]
        })
    return rows

DETECTIONS = build_detections()

def boundary_geojson():
    return {"type":"FeatureCollection","features":[
      {"type":"Feature","properties":{"name":"Demo Mining Permit","kind":"permit"},"geometry":{"type":"Polygon","coordinates":[[[81.98,23.20],[82.12,23.20],[82.12,23.31],[81.98,23.31],[81.98,23.20]]]}},
      {"type":"Feature","properties":{"name":"Demo Protected Forest","kind":"protected"},"geometry":{"type":"Polygon","coordinates":[[[82.18,23.31],[82.34,23.31],[82.34,23.45],[82.18,23.45],[82.18,23.31]]]}},
      {"type":"Feature","properties":{"name":"Demo Community Area","kind":"community"},"geometry":{"type":"Polygon","coordinates":[[[81.89,23.32],[82.01,23.32],[82.01,23.43],[81.89,23.43],[81.89,23.32]]]}}
    ]}

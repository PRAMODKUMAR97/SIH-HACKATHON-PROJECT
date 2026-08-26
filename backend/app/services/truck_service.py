"""Local route and transport-record consistency checks."""
from __future__ import annotations

from ..demo_data import CHALLANS, RFID_EVENTS, TRUCK_ROUTES, TRUCKS, WEIGHBRIDGE


def route_for(truck_id: str) -> dict | None:
    truck = next((item for item in TRUCKS if item["truck_id"] == truck_id), None)
    route = TRUCK_ROUTES.get(truck_id)
    if not truck or not route:
        return None
    difference = round(truck["actual_distance_km"] - truck["planned_distance_km"], 1)
    return {**truck, **route, "distance_difference_km": difference, "route_deviation_percentage": round(difference / truck["planned_distance_km"] * 100, 1), "anomaly": truck["status"] == "ROUTE ANOMALY"}


def evidence_for(truck_id: str = "TRK-SK-1042") -> dict:
    route = route_for(truck_id)
    rfid = [event for event in RFID_EVENTS if event["truck_id"] == truck_id]
    challans = [item for item in CHALLANS if item["truck_id"] == truck_id]
    weighbridge = [item for item in WEIGHBRIDGE if item["truck_id"] == truck_id]
    rfid_issues = sum(item["status"] != "VALID" for item in rfid)
    weight_issues = sum(abs(item["difference_t"]) >= 1 for item in weighbridge)
    route_issues = 1 if route and route["anomaly"] else 0
    return {"truck": route, "rfid": rfid, "challans": challans, "weighbridge": weighbridge, "anomaly_count": route_issues + rfid_issues + weight_issues}

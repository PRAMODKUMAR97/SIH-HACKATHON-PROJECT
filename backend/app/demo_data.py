"""Bundled, deterministic fixtures for the offline KHANAN-NETRA demonstration.

Nothing here is a real observation, permit, vehicle, or legal finding. Keeping
fixtures explicit rather than generated prevents synthetic values being
presented as satellite truth and makes the demo repeatable.
"""
from __future__ import annotations

from copy import deepcopy

DEMO_LOCATION = {
    "label": "Sikkim mining-monitoring demo area", "latitude": 27.2054,
    "longitude": 88.5426, "zoom": 14, "source": "Local demo geocoder",
}

DEMO_AOI = {
    "type": "Feature", "properties": {"name": "Sample AOI — Sikkim demo area", "data_status": "DEMO DATA"},
    "geometry": {"type": "Polygon", "coordinates": [[[88.5260, 27.1940], [88.5610, 27.1940], [88.5610, 27.2180], [88.5260, 27.2180], [88.5260, 27.1940]]]},
}

# These records model the shape of a Sentinel-2 catalogue response. Their
# dates, cloud figures and IDs are bundled fixtures, not Copernicus records.
OBSERVATIONS = [
    {"id": "DEMO-S2-2026-06-03", "date": "2026-06-03", "source": "Sentinel-2 style sample", "cloud_percentage": 8.0, "usable": True, "footprint_ha": 7.8},
    {"id": "DEMO-S2-2026-06-14", "date": "2026-06-14", "source": "Sentinel-2 style sample", "cloud_percentage": 42.0, "usable": False, "rejection_reason": "Cloud coverage above selected threshold", "footprint_ha": None},
    {"id": "DEMO-S2-2026-06-25", "date": "2026-06-25", "source": "Sentinel-2 style sample", "cloud_percentage": 11.0, "usable": True, "footprint_ha": 8.4},
    {"id": "DEMO-S2-2026-07-08", "date": "2026-07-08", "source": "Sentinel-2 style sample", "cloud_percentage": 18.0, "usable": True, "footprint_ha": 9.1},
    {"id": "DEMO-S2-2026-07-22", "date": "2026-07-22", "source": "Sentinel-2 style sample", "cloud_percentage": 14.0, "usable": True, "footprint_ha": 10.3},
    {"id": "DEMO-S2-2026-08-05", "date": "2026-08-05", "source": "Sentinel-2 style sample", "cloud_percentage": 63.0, "usable": False, "rejection_reason": "Cloud coverage above selected threshold", "footprint_ha": None},
    {"id": "DEMO-S2-2026-08-12", "date": "2026-08-12", "source": "Sentinel-2 style sample", "cloud_percentage": 9.0, "usable": True, "footprint_ha": 11.6},
    {"id": "DEMO-S2-2026-08-25", "date": "2026-08-25", "source": "Sentinel-2 style sample", "cloud_percentage": 6.0, "usable": True, "footprint_ha": 12.6},
]

# Geographic polygons replace the prior random point markers as the primary
# offline analysis result.
DETECTIONS = [
    {
        "id": "DET-2026-004", "case_id": "KN-2026-001", "date": "2026-08-25", "name": "North bench expansion",
        "area_ha": 7.12, "probability": 0.92, "confidence": "VERY HIGH", "risk": 91, "risk_level": "CRITICAL",
        "change_percentage": 61.5, "change_direction": "EXPANSION", "source": "Offline DEMO satellite-analysis fixture", "data_status": "DEMO DATA",
        "geometry": {"type": "Polygon", "coordinates": [[[88.5350, 27.2022], [88.5489, 27.2022], [88.5489, 27.2089], [88.5392, 27.2110], [88.5350, 27.2022]]]},
    },
    {
        "id": "DET-2026-005", "case_id": "KN-2026-002", "date": "2026-08-25", "name": "Eastern haul-road clearing",
        "area_ha": 3.48, "probability": 0.78, "confidence": "HIGH", "risk": 74, "risk_level": "HIGH",
        "change_percentage": 37.0, "change_direction": "NEW BARE LAND", "source": "Offline DEMO satellite-analysis fixture", "data_status": "DEMO DATA",
        "geometry": {"type": "Polygon", "coordinates": [[[88.5498, 27.2076], [88.5569, 27.2076], [88.5569, 27.2135], [88.5514, 27.2144], [88.5498, 27.2076]]]},
    },
    {
        "id": "DET-2026-006", "case_id": "KN-2026-003", "date": "2026-08-12", "name": "South stockpile change",
        "area_ha": 2.03, "probability": 0.66, "confidence": "HIGH", "risk": 58, "risk_level": "MEDIUM",
        "change_percentage": 18.2, "change_direction": "SURFACE CHANGE", "source": "Offline DEMO satellite-analysis fixture", "data_status": "DEMO DATA",
        "geometry": {"type": "Polygon", "coordinates": [[[88.5293, 27.1965], [88.5361, 27.1965], [88.5361, 27.2010], [88.5293, 27.2010], [88.5293, 27.1965]]]},
    },
]

PERMITS = {"type": "FeatureCollection", "features": [
    {"type": "Feature", "properties": {"permit_id": "DEMO-PERMIT-17", "operator": "Sikkim Demo Minerals Ltd.", "mineral": "Construction aggregate", "status": "DEMO / not official", "valid_from": "2024-04-01", "valid_to": "2027-03-31", "permitted_area": 8.7, "permitted_volume": 15000, "data_status": "DEMO DATA"}, "geometry": {"type": "Polygon", "coordinates": [[[88.5300, 27.1970], [88.5455, 27.1970], [88.5455, 27.2090], [88.5300, 27.2090], [88.5300, 27.1970]]]}}
]}

PROTECTED_AREAS = {"type": "FeatureCollection", "features": [
    {"type": "Feature", "properties": {"zone_id": "DEMO-PROTECTED-2", "name": "Demo forest-sensitive zone", "status": "DEMO / not official", "data_status": "DEMO DATA"}, "geometry": {"type": "Polygon", "coordinates": [[[88.5480, 27.2070], [88.5600, 27.2070], [88.5600, 27.2170], [88.5480, 27.2170], [88.5480, 27.2070]]]}}
]}

TRUCKS = [
    {"truck_id": "TRK-SK-1042", "vehicle_number": "SK-01-A-1042", "source_mine": "Demo Permit 17", "destination": "Rangpo depot", "planned_distance_km": 42.0, "actual_distance_km": 58.0, "unexpected_stop_min": 38, "missing_checkpoints": 1, "status": "ROUTE ANOMALY", "data_status": "SIMULATED"},
    {"truck_id": "TRK-SK-2088", "vehicle_number": "SK-01-B-2088", "source_mine": "Demo Permit 17", "destination": "Singtam depot", "planned_distance_km": 31.0, "actual_distance_km": 32.4, "unexpected_stop_min": 4, "missing_checkpoints": 0, "status": "ON ROUTE", "data_status": "SIMULATED"},
]

TRUCK_ROUTES = {"TRK-SK-1042": {
    "planned": [[88.538, 27.204], [88.548, 27.198], [88.562, 27.190], [88.579, 27.184]],
    "actual": [[88.538, 27.204], [88.548, 27.198], [88.568, 27.210], [88.581, 27.196], [88.579, 27.184]],
    "checkpoints": [{"checkpoint_id": "CP-1", "name": "Rangpo gate", "coordinates": [88.548, 27.198], "seen": True}, {"checkpoint_id": "CP-2", "name": "River bridge", "coordinates": [88.562, 27.190], "seen": False}],
}}

RFID_EVENTS = [
    {"checkpoint_id": "CP-1", "truck_id": "TRK-SK-1042", "timestamp": "2026-08-25T09:18:00", "status": "VALID", "data_status": "SIMULATED"},
    {"checkpoint_id": "CP-2", "truck_id": "TRK-SK-1042", "timestamp": None, "status": "MISSING CHECKPOINT", "data_status": "SIMULATED"},
]
CHALLANS = [{"challan_id": "EC-2026-118", "truck_id": "TRK-SK-1042", "mineral": "Construction aggregate", "source": "Demo Permit 17", "destination": "Rangpo depot", "declared_quantity_t": 18.0, "date": "2026-08-25", "time": "09:00", "data_status": "DEMO DATA"}]
WEIGHBRIDGE = [{"record_id": "WB-2026-118", "truck_id": "TRK-SK-1042", "declared_quantity_t": 18.0, "actual_weight_t": 26.7, "difference_t": 8.7, "status": "QUANTITY MISMATCH", "data_status": "DEMO DATA"}]

DRONE_SURVEY = {
    "case_id": "KN-2026-001", "mode": "DEMO 3D SURVEY", "survey_date": "2026-08-26", "surface_area_ha": 7.0,
    "maximum_depth_m": 18.4, "average_depth_m": 8.1, "estimated_volume_m3": 34200,
    "permit_volume_m3": 15000, "difference_m3": 19200, "status": "VOLUME MISMATCH — requires verification",
    "data_status": "SAMPLE / DEMO DATA", "mesh": "bundled procedural pit mesh",
}


def boundary_geojson():
    """Compatibility response for the original boundary API."""
    features = []
    for feature in PERMITS["features"]:
        item = deepcopy(feature); item["properties"]["kind"] = "permit"; item["properties"]["name"] = item["properties"]["permit_id"]; features.append(item)
    for feature in PROTECTED_AREAS["features"]:
        item = deepcopy(feature); item["properties"]["kind"] = "protected"; features.append(item)
    return {"type": "FeatureCollection", "features": features}

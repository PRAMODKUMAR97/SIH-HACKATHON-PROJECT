import os
import json
from shapely.geometry import Point, shape

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
DATA_BOUNDARIES_DIR = os.path.join(PROJECT_ROOT, "data", "boundaries")


def check_location_legality(latitude: float, longitude: float) -> dict:
    """
    Checks spatial containment of (lat, lon) against mining permits and protected areas.
    """
    point = Point(longitude, latitude)  # Shapely uses (x, y) = (lon, lat)
    
    # 1. Check Protected Areas
    is_protected = False
    protected_area_name = None
    protected_file = os.path.join(DATA_BOUNDARIES_DIR, "protected_areas.geojson")
    
    if os.path.exists(protected_file):
        with open(protected_file, "r") as f:
            data = json.load(f)
            for feature in data.get("features", []):
                poly = shape(feature["geometry"])
                if poly.contains(point) or poly.intersects(point):
                    is_protected = True
                    protected_area_name = feature.get("properties", {}).get("name", "Protected Zone")
                    break

    # 2. Check Mining Permit Boundaries
    permit_found = False
    matched_permit_id = None
    permits_file = os.path.join(DATA_BOUNDARIES_DIR, "mining_permits.geojson")

    if os.path.exists(permits_file):
        with open(permits_file, "r") as f:
            data = json.load(f)
            for feature in data.get("features", []):
                poly = shape(feature["geometry"])
                if poly.contains(point) or poly.intersects(point):
                    permit_found = True
                    matched_permit_id = feature.get("properties", {}).get("permit_id")
                    break

    # Determine status
    if is_protected:
        legal_status = "ILLEGAL_PROTECTED_AREA"
    elif permit_found:
        legal_status = "LEGAL_WITHIN_PERMIT"
    else:
        legal_status = "SUSPICIOUS_OUTSIDE_PERMIT"

    return {
        "legal_status": legal_status,
        "matched_permit_id": matched_permit_id,
        "is_protected_area": is_protected,
        "protected_area_name": protected_area_name
    }

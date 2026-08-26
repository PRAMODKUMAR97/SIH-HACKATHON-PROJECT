"""Satellite catalogue and local demo-analysis orchestration.

Demo mode uses only the deterministic bundled fixtures. Data mode never falls
back to demo values: it searches the public Planetary Computer STAC catalogue
for real Sentinel-2 metadata and returns a clear availability result. Raster
processing can then be run from user-supplied/cached assets by the ML scripts.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from urllib.error import URLError
from urllib.request import Request, urlopen

from ..demo_data import DETECTIONS, OBSERVATIONS
from .gis_service import bounds_overlap


def _valid_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError) as exc:
        raise ValueError("Dates must use YYYY-MM-DD.") from exc


def filter_observations(start: str, end: str, cloud_max: float = 30) -> list[dict]:
    start_date, end_date = _valid_date(start), _valid_date(end)
    if end_date < start_date:
        raise ValueError("End date cannot be before start date.")
    return [item.copy() for item in OBSERVATIONS if start_date <= _valid_date(item["date"]) <= end_date and item["cloud_percentage"] <= cloud_max]


def demo_analysis(aoi: dict, start: str, end: str, cloud_max: float) -> dict:
    observations = filter_observations(start, end, cloud_max)
    detections = [item.copy() for item in DETECTIONS if bounds_overlap(item["geometry"], aoi)]
    if not observations:
        return {"mode": "demo", "data_status": "DEMO DATA", "observations": [], "detections": [], "message": "No usable bundled observations matched this period and cloud threshold."}
    return {
        "mode": "demo", "data_status": "DEMO DATA", "observations": observations, "detections": detections,
        "pipeline": ["Cloud filtering", "AOI clip", "Red / NIR feature fixture", "Probability mask", "Connected regions", "Polygon and permit screening"],
        "message": "Offline demo analysis completed using bundled, deterministic sample data.",
    }


def real_catalogue(aoi: dict, start: str, end: str, cloud_max: float) -> dict:
    """Retrieve real catalogue metadata only; never invent raster outcomes."""
    body = {"collections": ["sentinel-2-l2a"], "intersects": aoi.get("geometry", aoi), "datetime": f"{start}T00:00:00Z/{end}T23:59:59Z", "query": {"eo:cloud_cover": {"lte": cloud_max}}, "limit": 24}
    request = Request("https://planetarycomputer.microsoft.com/api/stac/v1/search", data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json", "User-Agent": "KHANAN-NETRA-hackathon-prototype"}, method="POST")
    try:
        with urlopen(request, timeout=12) as response:  # nosec B310: fixed public STAC endpoint
            payload = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, json.JSONDecodeError):
        return {"mode": "data", "data_status": "DATA MODE", "observations": [], "detections": [], "available": False, "message": "Real satellite catalogue is unavailable right now. Select Demo Mode for the bundled offline workflow."}
    observations = [{"id": feature.get("id"), "date": feature.get("properties", {}).get("datetime", "")[:10], "source": "Sentinel-2 L2A / Planetary Computer STAC", "cloud_percentage": feature.get("properties", {}).get("eo:cloud_cover"), "usable": True, "real_data": True} for feature in payload.get("features", [])]
    return {"mode": "data", "data_status": "REAL CATALOGUE DATA", "observations": observations, "detections": [], "available": bool(observations), "message": "Real Sentinel-2 catalogue metadata retrieved. Raster features and model polygons are intentionally withheld until cached source assets are supplied; no synthetic detection is shown in Data Mode."}

"""KHANAN-NETRA local FastAPI application."""
from __future__ import annotations

import csv
import io
import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .database import initialize_database, latest_aoi, save_aoi, save_case
from .config import settings
from .demo_data import (CHALLANS, DEMO_AOI, DEMO_LOCATION, DETECTIONS, DRONE_SURVEY,
                        PERMITS, PROTECTED_AREAS, RFID_EVENTS, TRUCKS, WEIGHBRIDGE,
                        boundary_geojson)
from .services.gis_service import (GeoJSONValidationError, bounds_overlap, feature_collection,
                                   intersection_polygon, overlap_area_ha, polygon_area_ha,
                                   polygon_coordinates)
from .services.risk_service import calculate_risk
from .services.satellite_service import demo_analysis, filter_observations, real_catalogue
from .services.truck_service import evidence_for, route_for

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "frontend"
EXPORTS = ROOT / "exports"
UPLOADS = ROOT / "data" / "drone" / "uploads"
for directory in (EXPORTS, UPLOADS):
    directory.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="KHANAN-NETRA", version="1.0.0", description="Satellite mining intelligence prototype")


@app.on_event("startup")
def startup() -> None:
    initialize_database()


def _http_error(status: int, detail: str) -> HTTPException:
    return HTTPException(status_code=status, detail=detail)


def _centre(feature: dict) -> dict:
    ring = polygon_coordinates(feature)
    points = ring[:-1]
    return {"latitude": round(sum(point[1] for point in points) / len(points), 6), "longitude": round(sum(point[0] for point in points) / len(points), 6)}


def _normalise_feature(payload: dict) -> dict:
    feature = payload.get("feature", payload)
    if feature.get("type") == "Polygon":
        feature = {"type": "Feature", "properties": {}, "geometry": feature}
    if feature.get("type") != "Feature":
        raise GeoJSONValidationError("AOI must be a GeoJSON Feature or Polygon.")
    polygon_coordinates(feature)
    return feature


def _detection_feature(detection: dict) -> dict:
    item = dict(detection)
    geometry = item.pop("geometry")
    legal = _legality(detection)
    risk = _risk(detection, legal)
    item.update({"legal": legal, "risk": risk["score"], "risk_level": risk["level"], "risk_breakdown": risk["breakdown"]})
    return {"type": "Feature", "properties": item, "geometry": geometry}


def _legality(detection: dict) -> dict:
    geometry = detection["geometry"]
    detected_area = polygon_area_ha(geometry)
    permit_area = sum(overlap_area_ha(geometry, item["geometry"]) for item in PERMITS["features"])
    protected_area = sum(overlap_area_ha(geometry, item["geometry"]) for item in PROTECTED_AREAS["features"])
    outside_area = max(0, detected_area - permit_area)
    outside_percentage = round(outside_area / detected_area * 100, 1) if detected_area else 0
    protected_percentage = round(protected_area / detected_area * 100, 1) if detected_area else 0
    if protected_area > 0:
        classification = "PROTECTED AREA — potentially unauthorized / requires verification"
    elif permit_area == 0:
        classification = "OUTSIDE PERMIT — potentially unauthorized / requires verification"
    elif outside_area > 0.01:
        classification = "PARTIALLY OUTSIDE PERMIT — potentially unauthorized / requires verification"
    else:
        classification = "WITHIN PERMIT — requires routine verification"
    return {"detected_area_ha": detected_area, "inside_permit_ha": round(permit_area, 3), "outside_permit_ha": round(outside_area, 3), "outside_percentage": outside_percentage, "protected_overlap_ha": round(protected_area, 3), "protected_percentage": protected_percentage, "classification": classification}


def _risk(detection: dict, legal: dict | None = None) -> dict:
    legal = legal or _legality(detection)
    drone = detection.get("case_id") == DRONE_SURVEY["case_id"] and DRONE_SURVEY["difference_m3"] > 0
    transport = evidence_for()["anomaly_count"] if detection.get("case_id") == "KN-2026-001" else 0
    return calculate_risk(probability=detection["probability"], change_percentage=detection["change_percentage"], outside_percentage=legal["outside_percentage"], protected_percentage=legal["protected_percentage"], affected_area_ha=detection["area_ha"], history_score=0.85, drone_mismatch=drone, transport_anomalies=transport)


def _enriched_detections(aoi: dict | None = None) -> list[dict]:
    rows = DETECTIONS
    if aoi:
        rows = [item for item in rows if bounds_overlap(item["geometry"], aoi)]
    return [_detection_feature(item) for item in rows]


def _find_detection(detection_id: str) -> dict:
    item = next((entry for entry in DETECTIONS if entry["id"] == detection_id), None)
    if not item:
        raise _http_error(404, "Detection not found.")
    return item


def _find_case(case_id: str) -> dict:
    item = next((entry for entry in DETECTIONS if entry["case_id"] == case_id), None)
    if not item:
        raise _http_error(404, "Case not found.")
    return item


def _date_range(days: int = 90) -> tuple[str, str]:
    # The fixture dates end on 2026-08-25 to keep the walkthrough repeatable.
    end = date(2026, 8, 25)
    return (end - timedelta(days=days - 1)).isoformat(), end.isoformat()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "application": "KHANAN-NETRA", "offline_demo_available": True}


@app.get("/api/config")
def config() -> dict:
    start, end = _date_range()
    return {"default_mode": "demo" if settings.demo_mode else "data", "default_period_days": 90, "default_start": start, "default_end": end, "demo_location": DEMO_LOCATION, "sample_aoi": DEMO_AOI, "data_labels": {"satellite": "DEMO DATA", "drone": "SAMPLE / DEMO DATA", "truck": "SIMULATED", "transport": "DEMO DATA"}}


@app.post("/api/aoi")
def create_aoi(payload: dict) -> dict:
    try:
        feature = _normalise_feature(payload)
        area = polygon_area_ha(feature)
    except GeoJSONValidationError as exc:
        raise _http_error(422, str(exc))
    if area > 100_000:
        raise _http_error(422, "AOI is too large for the local prototype. Draw a smaller area.")
    result = save_aoi(feature, str(payload.get("name") or "User AOI"))
    result.update({"area_ha": area, "center": _centre(feature), "data_status": "USER-DRAWN AOI"})
    return result


@app.get("/api/aoi")
def get_aoi() -> dict:
    stored = latest_aoi()
    if stored:
        stored.update({"area_ha": polygon_area_ha(stored["feature"]), "center": _centre(stored["feature"]), "data_status": "USER-DRAWN AOI"})
        return stored
    return {"id": "sample", "name": "Sample AOI — Sikkim demo area", "feature": DEMO_AOI, "area_ha": polygon_area_ha(DEMO_AOI), "center": _centre(DEMO_AOI), "data_status": "DEMO DATA", "is_sample": True}


@app.get("/api/geocode")
def geocode(q: str = Query(min_length=2, max_length=180)) -> dict:
    cleaned = q.strip()
    try:
        latitude, longitude = [float(part.strip()) for part in cleaned.split(",", maxsplit=1)]
        if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
            raise ValueError
        return {"label": f"{latitude:.5f}, {longitude:.5f}", "latitude": latitude, "longitude": longitude, "zoom": 14, "source": "User coordinates", "data_status": "USER INPUT"}
    except ValueError:
        pass
    local_terms = ("sikkim", "rangpo", "mining area", "mining")
    if any(term in cleaned.lower() for term in local_terms):
        return {**DEMO_LOCATION, "data_status": "DEMO LOCATION"}
    # OpenStreetMap's public Nominatim is an optional free lookup. A failure is
    # handled as a normal user-facing result, so offline demos do not break.
    try:
        url = "https://nominatim.openstreetmap.org/search?" + urlencode({"q": cleaned, "format": "jsonv2", "limit": 1})
        request = Request(url, headers={"User-Agent": "KHANAN-NETRA hackathon prototype"})
        with urlopen(request, timeout=6) as response:  # nosec B310: fixed endpoint
            result = json.loads(response.read().decode("utf-8"))
        if result:
            place = result[0]
            return {"label": place["display_name"], "latitude": float(place["lat"]), "longitude": float(place["lon"]), "zoom": 13, "source": "OpenStreetMap Nominatim", "data_status": "OPEN GEOCODER"}
    except Exception:
        pass
    raise _http_error(404, "Location not found while offline. Try coordinates or ‘Mining Area, Sikkim, India’ for the bundled demo.")


@app.get("/api/satellite/observations")
def observations(start: str | None = None, end: str | None = None, cloud_max: float = Query(30, ge=0, le=100)) -> dict:
    default_start, default_end = _date_range()
    try:
        items = filter_observations(start or default_start, end or default_end, cloud_max)
    except ValueError as exc:
        raise _http_error(422, str(exc))
    return {"mode": "demo", "data_status": "DEMO DATA", "items": items, "message": "Bundled observation fixtures, not real satellite observations."}


@app.post("/api/satellite/analyze")
def analyze_satellite(payload: dict) -> dict:
    mode = str(payload.get("mode", "demo")).lower()
    if mode not in {"demo", "data"}:
        raise _http_error(422, "Mode must be demo or data.")
    default_start, default_end = _date_range(int(payload.get("period_days", 90)))
    try:
        aoi = _normalise_feature(payload.get("aoi") or (latest_aoi() or {}).get("feature") or DEMO_AOI)
        start, end = str(payload.get("start") or default_start), str(payload.get("end") or default_end)
        cloud_max = float(payload.get("cloud_max", 30))
        if not 0 <= cloud_max <= 100:
            raise ValueError("Cloud threshold must be between 0 and 100.")
        raw = demo_analysis(aoi, start, end, cloud_max) if mode == "demo" else real_catalogue(aoi, start, end, cloud_max)
    except (GeoJSONValidationError, ValueError) as exc:
        raise _http_error(422, str(exc))
    if mode == "data":
        return {**raw, "aoi": aoi, "aoi_area_ha": polygon_area_ha(aoi), "processing": {"stage": "catalogue search", "progress": 100}}
    features = _enriched_detections(aoi)
    usable = raw["observations"]
    footprints = [item["footprint_ha"] for item in usable if item.get("footprint_ha") is not None]
    change = {"earliest_date": usable[0]["date"] if usable else None, "latest_date": usable[-1]["date"] if usable else None, "earliest_footprint_ha": footprints[0] if footprints else 0, "latest_footprint_ha": footprints[-1] if footprints else 0, "increase_ha": round((footprints[-1] - footprints[0]), 2) if len(footprints) > 1 else 0, "change_percentage": round((footprints[-1] - footprints[0]) / footprints[0] * 100, 1) if len(footprints) > 1 and footprints[0] else 0}
    return {**raw, "aoi": aoi, "aoi_area_ha": polygon_area_ha(aoi), "detections": feature_collection(features), "change": change, "processing": {"stage": "analysis complete", "progress": 100}, "model_note": "Demo mode uses precomputed, deterministic model-output fixtures. Train ml/train.py with labelled samples before interpreting a model as scientifically validated."}


@app.get("/api/detections")
def detections(risk: str | None = None, min_confidence: float = Query(0, ge=0, le=1), min_area: float = Query(0, ge=0)) -> dict:
    features = _enriched_detections()
    if risk and risk != "ALL":
        features = [item for item in features if item["properties"]["risk_level"] == risk]
    features = [item for item in features if item["properties"]["probability"] >= min_confidence and item["properties"]["area_ha"] >= min_area]
    return {"demo": True, "data_status": "DEMO DATA", "items": [item["properties"] | {"geometry": item["geometry"]} for item in features], "geojson": feature_collection(features)}


@app.get("/api/detections/{detection_id}")
def detection_detail(detection_id: str) -> dict:
    item = _find_detection(detection_id)
    result = _detection_feature(item)["properties"] | {"geometry": item["geometry"]}
    result["explanation"] = "Satellite/ML detected a mining-related change requiring verification. This evidence score is not proof of illegal activity or a legal judgment."
    return result


@app.get("/api/permits")
def permits() -> dict:
    return {"data_status": "DEMO DATA — not official permit boundaries", **PERMITS}


@app.get("/api/protected-areas")
def protected_areas() -> dict:
    return {"data_status": "DEMO DATA — not official protected boundaries", **PROTECTED_AREAS}


@app.get("/api/boundaries")
def boundaries() -> dict:
    return boundary_geojson()


@app.get("/api/summary")
def summary() -> dict:
    features = _enriched_detections()
    props = [item["properties"] for item in features]
    return {"demo": True, "data_status": "DEMO DATA", "monitored_area_km2": round(polygon_area_ha(DEMO_AOI) / 100, 2), "total": len(props), "high": sum(item["risk_level"] in {"HIGH", "CRITICAL"} for item in props), "legal": sum("WITHIN PERMIT" in item["legal"]["classification"] for item in props), "suspicious": sum("requires verification" in item["legal"]["classification"] for item in props), "area": round(sum(item["area_ha"] for item in props), 1), "risk_score": max(item["risk"] for item in props)}


@app.get("/api/cases")
def cases() -> dict:
    rows = []
    for detection in DETECTIONS:
        legal = _legality(detection); risk = _risk(detection, legal)
        rows.append({"case_id": detection["case_id"], "detection_id": detection["id"], "date": detection["date"], "location": detection["name"], "area_ha": detection["area_ha"], "probability": detection["probability"], "change_percentage": detection["change_percentage"], "legal_status": legal["classification"], "risk": risk["score"], "risk_level": risk["level"], "drone": "DEMO 3D SURVEY" if detection["case_id"] == DRONE_SURVEY["case_id"] else "NOT REQUESTED", "transport": "ANOMALY" if detection["case_id"] == "KN-2026-001" else "NO LINK", "action": "FIELD VERIFICATION REQUIRED"})
    return {"data_status": "DEMO DATA", "items": rows}


@app.post("/api/cases")
def create_case(payload: dict) -> dict:
    detection = _find_detection(str(payload.get("detection_id", "")))
    legal = _legality(detection); risk = _risk(detection, legal)
    save_case(detection["case_id"], detection["id"], risk, {"detection": detection, "legal": legal})
    return {"case_id": detection["case_id"], "detection_id": detection["id"], "risk": risk["score"], "risk_level": risk["level"], "status": "FIELD VERIFICATION REQUIRED", "message": "Investigation case saved locally."}


@app.get("/api/cases/{case_id}")
def case_detail(case_id: str) -> dict:
    detection = _find_case(case_id); legal = _legality(detection); risk = _risk(detection, legal)
    return {"case_id": case_id, "status": "FIELD VERIFICATION REQUIRED", "detection": _detection_feature(detection), "legal": legal, "risk": risk, "drone": DRONE_SURVEY if case_id == DRONE_SURVEY["case_id"] else None, "transport": evidence_for() if case_id == "KN-2026-001" else None, "data_status": {"satellite": "DEMO DATA", "drone": "SAMPLE / DEMO DATA", "truck": "SIMULATED", "permit": "DEMO DATA"}}


@app.get("/api/drone/{case_id}")
def drone(case_id: str) -> dict:
    _find_case(case_id)
    if case_id != DRONE_SURVEY["case_id"]:
        raise _http_error(404, "No drone model is available for this case. Request a survey or open the sample high-risk case.")
    return DRONE_SURVEY


@app.post("/api/drone/upload")
async def drone_upload(request: Request, case_id: str = Query(min_length=3, max_length=40), filename: str = Query(min_length=5, max_length=180)) -> dict:
    _find_case(case_id)
    suffix = Path(filename).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
        raise _http_error(415, "Only JPG, PNG, and TIFF drone-image files are accepted.")
    content = await request.body()
    if not content:
        raise _http_error(422, "The uploaded drone image is empty.")
    if len(content) > 25 * 1024 * 1024:
        raise _http_error(413, "Drone image exceeds the 25 MB local-demo limit.")
    target = UPLOADS / f"{case_id}-{Path(filename).name}"
    target.write_bytes(content)
    return {"accepted": True, "filename": target.name, "case_id": case_id, "message": "Image stored for offline review. Photogrammetry is not run automatically; the displayed model remains clearly labelled DEMO 3D SURVEY."}


@app.get("/api/trucks")
def trucks() -> dict:
    return {"data_status": "SIMULATED", "items": TRUCKS}


@app.get("/api/trucks/{truck_id}")
def truck(truck_id: str) -> dict:
    result = route_for(truck_id)
    if not result:
        raise _http_error(404, "Truck not found.")
    return result


@app.get("/api/trucks/{truck_id}/route")
def truck_route(truck_id: str) -> dict:
    result = route_for(truck_id)
    if not result:
        raise _http_error(404, "Truck route not found.")
    return result


@app.get("/api/rfid")
def rfid() -> dict:
    return {"data_status": "SIMULATED", "items": RFID_EVENTS}


@app.get("/api/challans")
def challans() -> dict:
    return {"data_status": "DEMO DATA", "items": CHALLANS}


@app.get("/api/weighbridge")
def weighbridge() -> dict:
    return {"data_status": "DEMO DATA", "items": WEIGHBRIDGE}


@app.get("/api/risk/{case_id}")
def risk(case_id: str) -> dict:
    detection = _find_case(case_id)
    legal = _legality(detection)
    return {"case_id": case_id, **_risk(detection, legal), "legal": legal, "data_status": "EVIDENCE FUSION — DEMO / SIMULATED INPUTS"}


@app.get("/api/alerts")
def alerts() -> dict:
    return {"data_status": "DEMO DATA", "items": [
        {"level": "CRITICAL", "case_id": "KN-2026-001", "type": "Rapid mining expansion", "message": "Mining-related change expands between earliest and latest usable demo observations."},
        {"level": "HIGH", "case_id": "KN-2026-001", "type": "Transport evidence", "message": "Route deviation, missing RFID checkpoint, and weighbridge mismatch need verification."},
        {"level": "HIGH", "case_id": "KN-2026-002", "type": "Protected-area overlap", "message": "Polygon overlaps a demo forest-sensitive boundary; field verification is required."},
    ]}


def _selected_features(ids: str | None) -> list[dict]:
    selected = set(ids.split(",")) if ids else {item["id"] for item in DETECTIONS}
    return [item for item in _enriched_detections() if item["properties"]["id"] in selected]


@app.get("/api/export/geojson")
def geojson_export(ids: str | None = None) -> Response:
    body = json.dumps(feature_collection(_selected_features(ids)), indent=2)
    return Response(body, media_type="application/geo+json", headers={"Content-Disposition": "attachment; filename=khanan-netra-demo-detections.geojson"})


@app.get("/api/export/csv")
def csv_export(ids: str | None = None) -> Response:
    output = io.StringIO(); writer = csv.writer(output)
    writer.writerow(["detection_id", "date", "area_ha", "probability", "risk", "risk_level", "legal_status", "data_status"])
    for feature in _selected_features(ids):
        item = feature["properties"]
        writer.writerow([item["id"], item["date"], item["area_ha"], item["probability"], item["risk"], item["risk_level"], item["legal"]["classification"], item["data_status"]])
    return Response(output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=khanan-netra-demo-detections.csv"})


@app.get("/api/export/kml")
def kml(ids: str | None = None) -> Response:
    body = ""
    for feature in _selected_features(ids):
        item, ring = feature["properties"], feature["geometry"]["coordinates"][0]
        coordinates = " ".join(f"{lon},{lat},0" for lon, lat in ring)
        body += f"<Placemark><name>{escape(item['id'])}</name><description>{escape(item['legal']['classification'])}; risk {item['risk']}; DEMO DATA</description><Polygon><outerBoundaryIs><LinearRing><coordinates>{coordinates}</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>"
    return Response(f'<?xml version="1.0"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>KHANAN-NETRA DEMO</name>{body}</Document></kml>', media_type="application/vnd.google-earth.kml+xml", headers={"Content-Disposition": "attachment; filename=khanan-netra-demo.kml"})


@app.get("/api/export/gpx")
def gpx(ids: str | None = None) -> Response:
    body = ""
    for feature in _selected_features(ids):
        item, ring = feature["properties"], feature["geometry"]["coordinates"][0]
        points = "".join(f'<trkpt lat="{lat}" lon="{lon}" />' for lon, lat in ring)
        body += f'<trk><name>{escape(item["id"])}</name><desc>DEMO DATA; risk {item["risk"]}</desc><trkseg>{points}</trkseg></trk>'
    return Response(f'<?xml version="1.0"?><gpx version="1.1" creator="KHANAN-NETRA">{body}</gpx>', media_type="application/gpx+xml", headers={"Content-Disposition": "attachment; filename=khanan-netra-demo.gpx"})


def _build_report(path: Path, case_id: str = "KN-2026-001") -> None:
    detection = _find_case(case_id); legal = _legality(detection); risk_data = _risk(detection, legal)
    styles = getSampleStyleSheet(); story = [Paragraph("KHANAN-NETRA", styles["Title"]), Paragraph("Satellite Mining Intelligence — Evidence Support Report", styles["Heading2"]), Paragraph(f"DEMO / SIMULATED EVIDENCE — {date.today().isoformat()}", styles["BodyText"]), Spacer(1, 12)]
    story += [Paragraph(f"<b>Case:</b> {case_id} &nbsp;&nbsp; <b>Detection:</b> {detection['id']} &nbsp;&nbsp; <b>Final evidence score:</b> {risk_data['score']}/100 ({risk_data['level']})", styles["BodyText"]), Spacer(1, 10)]
    rows = [["Evidence", "Finding", "Data status"], ["Satellite/ML", f"{detection['probability']:.0%} mining-related change probability; {detection['change_percentage']}% change", "DEMO DATA"], ["Permit comparison", legal["classification"], "DEMO DATA — not official"], ["Drone", f"{DRONE_SURVEY['estimated_volume_m3']:,} m³; {DRONE_SURVEY['status']}", "SAMPLE / DEMO"], ["Transport", "Route, RFID, and weighbridge anomalies", "SIMULATED / DEMO"]]
    table = Table(rows, repeatRows=1, colWidths=[100, 280, 115]); table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12304a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("LEADING", (0, 0), (-1, -1), 10)]))
    story += [table, Spacer(1, 12), Paragraph("Recommendation: prioritise field verification. Satellite/ML output identifies a mining-related change requiring verification; it does not prove unlawful activity or legal liability.", styles["BodyText"])]
    SimpleDocTemplate(str(path), pagesize=A4).build(story)


@app.post("/api/reports/generate")
def generate_report(payload: dict | None = None) -> FileResponse:
    case_id = str((payload or {}).get("case_id", "KN-2026-001"))
    _find_case(case_id)
    path = EXPORTS / f"{case_id.lower()}-evidence-report.pdf"
    _build_report(path, case_id)
    return FileResponse(path, media_type="application/pdf", filename=path.name)


@app.get("/api/report")
def report() -> FileResponse:
    """Legacy report URL preserved for earlier bookmarks."""
    return generate_report({"case_id": "KN-2026-001"})


app.mount("/", StaticFiles(directory=STATIC, html=True), name="frontend")

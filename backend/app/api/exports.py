from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import Detection, Permit, GPSRecord, RiskAssessment
import json

router = APIRouter(prefix="/api", tags=["Exports & Reports"])


@router.get("/export/kml")
def export_kml(db: Session = Depends(get_db)):
    """
    Exports mining detections and permit boundaries in KML format.
    """
    detections = db.query(Detection).all()
    permits = db.query(Permit).all()

    kml_placemarks = []
    
    # Add detection placemarks
    for det in detections:
        kml_placemarks.append(f"""
        <Placemark>
            <name>Detection {det.detection_id}</name>
            <description>Status: {det.legal_status} | Mining Prob: {round(det.mining_probability*100, 1)}% | Area: {det.area_ha} ha</description>
            <Point>
                <coordinates>{det.longitude},{det.latitude},0</coordinates>
            </Point>
        </Placemark>""")

    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>KHANAN-NETRA Detections &amp; Permits</name>
    <description>Exported AI Mining Detections (DEMO DATA)</description>
    {''.join(kml_placemarks)}
  </Document>
</kml>"""

    return Response(
        content=kml_content,
        media_type="application/vnd.google-earth.kml+xml",
        headers={"Content-Disposition": "attachment; filename=khanan_netra_detections.kml"}
    )


@router.get("/export/gpx")
def export_gpx(db: Session = Depends(get_db)):
    """
    Exports truck GPS route waypoints in GPX format.
    """
    gps_records = db.query(GPSRecord).all()

    gpx_trkpts = []
    for g in gps_records:
        gpx_trkpts.append(f"""
      <trkpt lat="{g.latitude}" lon="{g.longitude}">
        <time>{g.timestamp}</time>
        <name>Truck {g.truck_id} ({g.checkpoint_name or 'Waypoint'})</name>
        <desc>Speed: {g.speed_kmh} km/h | Deviation: {g.route_deviation_km} km | Status: {g.rfid_scan_status}</desc>
      </trkpt>""")

    gpx_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="KHANAN-NETRA Surveillance Platform" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata>
    <name>KHANAN-NETRA Truck GPS Routes</name>
    <desc>Exported Truck GPS Route Waypoints (DEMO DATA)</desc>
  </metadata>
  <trk>
    <name>Monitored Mining Fleet Routes</name>
    <trkseg>
      {''.join(gpx_trkpts)}
    </trkseg>
  </trk>
</gpx>"""

    return Response(
        content=gpx_content,
        media_type="application/gpx+xml",
        headers={"Content-Disposition": "attachment; filename=khanan_netra_routes.gpx"}
    )


@router.get("/report")
def generate_summary_report(db: Session = Depends(get_db)):
    """
    Generates a structured surveillance summary report payload for high-risk sites.
    """
    detections = db.query(Detection).all()
    risks = db.query(RiskAssessment).all()
    permits = db.query(Permit).all()

    high_risk_count = sum(1 for r in risks if r.risk_level in ["HIGH", "CRITICAL"])
    medium_risk_count = sum(1 for r in risks if r.risk_level == "MEDIUM")
    low_risk_count = sum(1 for r in risks if r.risk_level == "LOW")

    report_data = {
        "title": "KHANAN-NETRA AI Surveillance & Risk Summary Report",
        "generated_at": "2026-08-26",
        "data_mode": "DEMO DATA",
        "summary": {
            "total_monitored_sites": len(detections),
            "high_critical_risk_sites": high_risk_count,
            "medium_risk_sites": medium_risk_count,
            "low_risk_sites": low_risk_count,
            "active_permits": len(permits)
        },
        "critical_findings": [
            {
                "detection_id": r.detection_id,
                "risk_score": r.risk_score,
                "risk_level": r.risk_level,
                "reasons": json.loads(r.reasons) if r.reasons else [],
                "recommended_action": r.recommended_action
            }
            for r in risks if r.risk_level in ["HIGH", "CRITICAL"]
        ]
    }

    return Response(
        content=json.dumps(report_data, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=khanan_netra_surveillance_report.json"}
    )

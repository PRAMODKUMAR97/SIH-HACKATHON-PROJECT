from sqlalchemy.orm import Session
from backend.app.models.models import (
    Detection, Permit, GPSRecord, Challan, WeighbridgeRecord, HistoricalActivity
)
from backend.app.services.volume_service import analyze_volume
from backend.app.services.transport_service import analyze_transport_and_rfid
from backend.app.services.historical_service import analyze_historical_change


def assemble_evidence(db: Session, detection: Detection) -> dict:
    """
    Gathers and aggregates evidence across ML, GIS, Volume, GPS, RFID, e-Challan, Weighbridge, and History.
    """
    # 1. Mining ML Probability
    mining_prob = detection.mining_probability or 0.0

    # 2. GIS Legal Status
    outside_permit = detection.legal_status in ["SUSPICIOUS_OUTSIDE_PERMIT", "ILLEGAL_PROTECTED_AREA"]
    protected_area = detection.is_protected_area or (detection.legal_status == "ILLEGAL_PROTECTED_AREA")

    # 3. Volume Analysis
    permitted_vol = 0.0
    if detection.permit_id:
        permit = db.query(Permit).filter(Permit.permit_id == detection.permit_id).first()
        if permit:
            permitted_vol = permit.permitted_volume_m3

    vol_analysis = analyze_volume(
        permitted_volume_m3=permitted_vol,
        estimated_excavation_m3=detection.estimated_volume_m3 or 0.0
    )

    # 4. GPS & Transport Analysis
    gps_record = db.query(GPSRecord).filter(GPSRecord.detection_id == detection.detection_id).first()
    
    route_dev_km = gps_record.route_deviation_km if gps_record else 0.0
    stops_cnt = gps_record.unusual_stops_count if gps_record else 0
    rfid_status = gps_record.rfid_scan_status if gps_record else "CHECKPOINT_VERIFIED"
    truck_id = gps_record.truck_id if gps_record else None

    # Check Weighbridge and Challan
    declared_kg = 0.0
    measured_net_kg = 0.0

    if truck_id:
        challan = db.query(Challan).filter(Challan.truck_id == truck_id).first()
        if challan:
            declared_kg = challan.declared_quantity_kg
            wb = db.query(WeighbridgeRecord).filter(WeighbridgeRecord.challan_id == challan.challan_id).first()
            if wb:
                measured_net_kg = wb.measured_net_kg

    trans_analysis = analyze_transport_and_rfid(
        route_deviation_km=route_dev_km,
        unusual_stops_count=stops_cnt,
        rfid_scan_status=rfid_status,
        declared_quantity_kg=declared_kg,
        measured_net_kg=measured_net_kg
    )

    # 5. Historical Analysis
    hist_record = db.query(HistoricalActivity).filter(HistoricalActivity.detection_id == detection.detection_id).first()
    growth_pct = hist_record.activity_growth_pct if hist_record else 0.0
    hist_analysis = analyze_historical_change(growth_pct)

    return {
        "mining_probability": mining_prob,
        "outside_permit": outside_permit,
        "protected_area": protected_area,
        "legal_status": detection.legal_status,
        "volume_anomaly": vol_analysis["volume_anomaly"],
        "volume_mismatch_pct": vol_analysis["volume_mismatch_pct"],
        "gps_route_anomaly": trans_analysis["gps_anomaly"],
        "route_deviation_km": trans_analysis["route_deviation_km"],
        "rfid_mismatch": trans_analysis["rfid_anomaly"],
        "weighbridge_discrepancy_pct": trans_analysis["weighbridge_discrepancy_pct"],
        "historical_change_pct": hist_analysis["activity_growth_pct"]
    }

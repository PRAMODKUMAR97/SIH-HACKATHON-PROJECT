import os
import json
import pandas as pd
from sqlalchemy.orm import Session
from backend.app.models.models import (
    Permit, Detection, Truck, GPSRecord, Challan, WeighbridgeRecord, HistoricalActivity, RiskAssessment
)
from backend.app.services.ml_service import train_and_predict_detection
from backend.app.services.gis_service import check_location_legality
from backend.app.services.evidence_fusion_service import assemble_evidence
from backend.app.services.risk_engine_service import compute_risk_assessment

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
DATA_DEMO_DIR = os.path.join(PROJECT_ROOT, "data", "demo")
DATA_BOUNDARIES_DIR = os.path.join(PROJECT_ROOT, "data", "boundaries")


def seed_database(db: Session):
    """
    Ingests CSV and GeoJSON demo data into SQLite database.
    Performs initial ML, GIS, and Risk Engine evaluations for detections.
    """
    print("[IngestionService] Starting demo data ingestion...")

    # 1. Ingest Permits from GeoJSON
    permits_path = os.path.join(DATA_BOUNDARIES_DIR, "mining_permits.geojson")
    if os.path.exists(permits_path):
        with open(permits_path, "r") as f:
            permit_geojson = json.load(f)
            for feature in permit_geojson.get("features", []):
                props = feature.get("properties", {})
                pid = props.get("permit_id")
                if pid and not db.query(Permit).filter(Permit.permit_id == pid).first():
                    permit = Permit(
                        permit_id=pid,
                        owner_name=props.get("owner_name", "Unknown"),
                        mineral_type=props.get("mineral_type", "General"),
                        permitted_volume_m3=float(props.get("permitted_volume_m3", 0.0)),
                        max_depth_m=float(props.get("max_depth_m", 0.0)),
                        issue_date=props.get("issue_date"),
                        expiry_date=props.get("expiry_date"),
                        status=props.get("status", "ACTIVE")
                    )
                    db.add(permit)
            db.commit()

    # 2. Ingest Trucks CSV
    trucks_csv = os.path.join(DATA_DEMO_DIR, "trucks.csv")
    if os.path.exists(trucks_csv):
        df_trucks = pd.read_csv(trucks_csv)
        for _, row in df_trucks.iterrows():
            tid = str(row["truck_id"])
            if not db.query(Truck).filter(Truck.truck_id == tid).first():
                permit_id = str(row["assigned_permit_id"]) if pd.notna(row["assigned_permit_id"]) and str(row["assigned_permit_id"]).strip() else None
                truck = Truck(
                    truck_id=tid,
                    license_plate=str(row["license_plate"]),
                    driver_name=str(row["driver_name"]),
                    carrier_company=str(row["carrier_company"]),
                    assigned_permit_id=permit_id,
                    status=str(row["status"])
                )
                db.add(truck)
        db.commit()

    # 3. Ingest Detections CSV
    detections_csv = os.path.join(DATA_DEMO_DIR, "detections.csv")
    if os.path.exists(detections_csv):
        df_det = pd.read_csv(detections_csv)
        for _, row in df_det.iterrows():
            did = str(row["detection_id"])
            if not db.query(Detection).filter(Detection.detection_id == did).first():
                permit_id = str(row["permit_id"]) if pd.notna(row["permit_id"]) and str(row["permit_id"]).strip() else None
                
                det = Detection(
                    detection_id=did,
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    area_ha=float(row["area_ha"]),
                    estimated_depth_m=float(row["estimated_depth_m"]),
                    estimated_volume_m3=float(row["estimated_volume_m3"]),
                    ndvi_change=float(row["ndvi_change"]),
                    sar_vv_vh_ratio=float(row["sar_vv_vh_ratio"]),
                    texture_variance=float(row["texture_variance"]),
                    spectral_anomaly_score=float(row["spectral_anomaly_score"]),
                    permit_id=permit_id,
                    detection_date=str(row["detection_date"])
                )
                
                # Evaluate ML prediction
                ml_result = train_and_predict_detection(
                    ndvi_change=det.ndvi_change,
                    sar_vv_vh_ratio=det.sar_vv_vh_ratio,
                    texture_variance=det.texture_variance,
                    spectral_anomaly_score=det.spectral_anomaly_score
                )
                det.mining_probability = ml_result["mining_probability"]
                det.confidence_level = ml_result["confidence_level"]

                # Evaluate GIS check
                gis_result = check_location_legality(det.latitude, det.longitude)
                det.legal_status = gis_result["legal_status"]
                det.is_protected_area = gis_result["is_protected_area"]

                db.add(det)
        db.commit()

    # 4. Ingest GPS CSV
    gps_csv = os.path.join(DATA_DEMO_DIR, "gps_routes.csv")
    if os.path.exists(gps_csv):
        df_gps = pd.read_csv(gps_csv)
        for _, row in df_gps.iterrows():
            gid = str(row["gps_id"])
            if not db.query(GPSRecord).filter(GPSRecord.gps_id == gid).first():
                det_id = str(row["detection_id"]) if pd.notna(row["detection_id"]) and str(row["detection_id"]).strip() else None
                gps = GPSRecord(
                    gps_id=gid,
                    truck_id=str(row["truck_id"]),
                    detection_id=det_id,
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    speed_kmh=float(row["speed_kmh"]),
                    timestamp=str(row["timestamp"]),
                    route_deviation_km=float(row["route_deviation_km"]),
                    unusual_stops_count=int(row["unusual_stops_count"]),
                    checkpoint_name=str(row["checkpoint_name"]) if pd.notna(row["checkpoint_name"]) else None,
                    rfid_scan_status=str(row["rfid_scan_status"])
                )
                db.add(gps)
        db.commit()

    # 5. Ingest e-Challans CSV
    challans_csv = os.path.join(DATA_DEMO_DIR, "challans.csv")
    if os.path.exists(challans_csv):
        df_ch = pd.read_csv(challans_csv)
        for _, row in df_ch.iterrows():
            cid = str(row["challan_id"])
            if not db.query(Challan).filter(Challan.challan_id == cid).first():
                pid = str(row["permit_id"]) if pd.notna(row["permit_id"]) and str(row["permit_id"]).strip() else None
                ch = Challan(
                    challan_id=cid,
                    truck_id=str(row["truck_id"]),
                    permit_id=pid,
                    mineral_type=str(row["mineral_type"]),
                    declared_quantity_kg=float(row["declared_quantity_kg"]),
                    issue_timestamp=str(row["issue_timestamp"]),
                    destination=str(row["destination"]) if pd.notna(row["destination"]) else None
                )
                db.add(ch)
        db.commit()

    # 6. Ingest Weighbridge CSV
    wb_csv = os.path.join(DATA_DEMO_DIR, "weighbridge.csv")
    if os.path.exists(wb_csv):
        df_wb = pd.read_csv(wb_csv)
        for _, row in df_wb.iterrows():
            wbid = str(row["weighbridge_id"])
            if not db.query(WeighbridgeRecord).filter(WeighbridgeRecord.weighbridge_id == wbid).first():
                wb_rec = WeighbridgeRecord(
                    weighbridge_id=wbid,
                    challan_id=str(row["challan_id"]),
                    truck_id=str(row["truck_id"]),
                    measured_gross_kg=float(row["measured_gross_kg"]),
                    tare_weight_kg=float(row["tare_weight_kg"]),
                    measured_net_kg=float(row["measured_net_kg"]),
                    timestamp=str(row["timestamp"]),
                    operator_id=str(row["operator_id"]) if pd.notna(row["operator_id"]) else None
                )
                db.add(wb_rec)
        db.commit()

    # 7. Ingest Historical Activity CSV
    hist_csv = os.path.join(DATA_DEMO_DIR, "historical_activity.csv")
    if os.path.exists(hist_csv):
        df_hist = pd.read_csv(hist_csv)
        for _, row in df_hist.iterrows():
            hid = str(row["history_id"])
            if not db.query(HistoricalActivity).filter(HistoricalActivity.history_id == hid).first():
                hist = HistoricalActivity(
                    history_id=hid,
                    detection_id=str(row["detection_id"]),
                    period=str(row["period"]),
                    historical_area_ha=float(row["historical_area_ha"]),
                    historical_volume_m3=float(row["historical_volume_m3"]),
                    activity_growth_pct=float(row["activity_growth_pct"])
                )
                db.add(hist)
        db.commit()

    # 8. Trigger Central Evidence Fusion & Risk Scoring for all Detections
    detections = db.query(Detection).all()
    for det in detections:
        if not db.query(RiskAssessment).filter(RiskAssessment.detection_id == det.detection_id).first():
            evidence = assemble_evidence(db, det)
            risk_res = compute_risk_assessment(db, det.detection_id, evidence)
            
            risk_obj = RiskAssessment(
                risk_id=f"RISK-{det.detection_id}",
                detection_id=det.detection_id,
                risk_score=risk_res["risk_score"],
                risk_level=risk_res["risk_level"],
                mining_prob_score=risk_res["scores"]["mining_prob_score"],
                boundary_violation_score=risk_res["scores"]["boundary_violation_score"],
                volume_anomaly_score=risk_res["scores"]["volume_anomaly_score"],
                gps_anomaly_score=risk_res["scores"]["gps_anomaly_score"],
                rfid_anomaly_score=risk_res["scores"]["rfid_anomaly_score"],
                historical_change_score=risk_res["scores"]["historical_change_score"],
                reasons=json.dumps(risk_res["reasons"]),
                recommended_action=risk_res["recommended_action"]
            )
            db.add(risk_obj)
    db.commit()
    print("[IngestionService] Ingestion and initial Risk Engine evaluation complete!")

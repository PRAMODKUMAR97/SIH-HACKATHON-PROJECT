import os
import sys

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.database import engine, Base, SessionLocal
from backend.app.services.ingestion_service import seed_database
from backend.app.services.ml_service import train_and_predict_detection
from backend.app.services.gis_service import check_location_legality
from backend.app.services.volume_service import analyze_volume
from backend.app.services.transport_service import analyze_transport_and_rfid
from backend.app.services.historical_service import analyze_historical_change
from backend.app.services.evidence_fusion_service import assemble_evidence
from backend.app.services.risk_engine_service import compute_risk_assessment
from backend.app.models.models import Detection, RiskAssessment, Permit, Truck, GPSRecord


def run_tests():
    print("==================================================")
    print("  KHANAN-NETRA BACKEND & CORE INTELLIGENCE TEST   ")
    print("==================================================")

    # 1. Initialize Database
    print("\n[1/8] Testing Database Initialization...")
    Base.metadata.create_all(bind=engine)
    print("  -> SQLite database tables created successfully.")

    # 2. Seed Demo Data
    print("\n[2/8] Testing Data Ingestion Service...")
    db = SessionLocal()
    seed_database(db)
    
    det_count = db.query(Detection).count()
    permit_count = db.query(Permit).count()
    truck_count = db.query(Truck).count()
    gps_count = db.query(GPSRecord).count()
    risk_count = db.query(RiskAssessment).count()

    print(f"  -> Ingested Detections: {det_count}")
    print(f"  -> Ingested Permits:    {permit_count}")
    print(f"  -> Ingested Trucks:     {truck_count}")
    print(f"  -> Ingested GPS Logs:   {gps_count}")
    print(f"  -> Evaluated Risks:     {risk_count}")

    assert det_count >= 4, "Expected at least 4 demo detections"
    assert risk_count >= 4, "Expected at least 4 risk assessments"

    # 3. Test ML Mining Detection
    print("\n[3/8] Testing ML Mining Detection Model...")
    ml_high = train_and_predict_detection(-0.85, 0.90, 0.85, 0.92)
    ml_low = train_and_predict_detection(-0.05, 0.12, 0.08, 0.10)
    print(f"  -> High Mining Features Prediction: Probability={ml_high['mining_probability']}, Confidence={ml_high['confidence_level']}")
    print(f"  -> Low Mining Features Prediction:  Probability={ml_low['mining_probability']}, Confidence={ml_low['confidence_level']}")
    assert ml_high['mining_probability'] > 0.5, "ML prediction failed for high mining case"
    assert ml_low['mining_probability'] < 0.5, "ML prediction failed for low mining case"

    # 4. Test GIS Spatial Validation
    print("\n[4/8] Testing GIS Spatial Boundary Validation...")
    gis_legal = check_location_legality(23.6800, 86.4500)
    gis_protected = check_location_legality(23.6600, 86.5400)
    print(f"  -> Legal Site check:     Status={gis_legal['legal_status']}, Permit={gis_legal['matched_permit_id']}")
    print(f"  -> Protected Zone check: Status={gis_protected['legal_status']}, Protected={gis_protected['is_protected_area']}")
    assert gis_legal['legal_status'] == "LEGAL_WITHIN_PERMIT"
    assert gis_protected['legal_status'] == "ILLEGAL_PROTECTED_AREA"

    # 5. Test Volume Analysis
    print("\n[5/8] Testing Volume Mismatch Analysis...")
    vol_normal = analyze_volume(15000.0, 5400.0)
    vol_overrun = analyze_volume(15000.0, 32300.0)
    print(f"  -> Normal Volume Check:  Anomaly={vol_normal['volume_anomaly']}, Mismatch={vol_normal['volume_mismatch_pct']}%")
    print(f"  -> Overrun Volume Check: Anomaly={vol_overrun['volume_anomaly']}, Mismatch={vol_overrun['volume_mismatch_pct']}%")
    assert not vol_normal['volume_anomaly']
    assert vol_overrun['volume_anomaly']

    # 6. Test Transport & RFID Analysis
    print("\n[6/8] Testing Transport & RFID Checkpoint Analysis...")
    trans_ok = analyze_transport_and_rfid(0.1, 0, "CHECKPOINT_VERIFIED", 10000.0, 10200.0)
    trans_bad = analyze_transport_and_rfid(8.5, 5, "CHECKPOINT_MISSED", 10000.0, 24000.0)
    print(f"  -> Normal Transport: GPS Anomaly={trans_ok['gps_anomaly']}, RFID Anomaly={trans_ok['rfid_anomaly']}, Weighbridge Mismatch={trans_ok['weighbridge_discrepancy_pct']}%")
    print(f"  -> Severe Transport: GPS Anomaly={trans_bad['gps_anomaly']}, RFID Anomaly={trans_bad['rfid_anomaly']}, Weighbridge Mismatch={trans_bad['weighbridge_discrepancy_pct']}%")
    assert not trans_ok['gps_anomaly'] and not trans_ok['rfid_anomaly']
    assert trans_bad['gps_anomaly'] and trans_bad['rfid_anomaly'] and trans_bad['weighbridge_anomaly']

    # 7. Test Central Evidence Fusion & Risk Engine Across Scenarios
    print("\n[7/8] Testing Evidence Fusion & Explainable Risk Scoring Engine...")
    detections = db.query(Detection).all()
    for det in detections:
        evidence = assemble_evidence(db, det)
        risk_res = compute_risk_assessment(db, det.detection_id, evidence)
        print(f"  -> [{det.detection_id}] Score: {risk_res['risk_score']}/100 | Level: {risk_res['risk_level']}")
        print(f"     Action: {risk_res['recommended_action']}")
        print(f"     Reasons: {risk_res['reasons']}")

    # 8. Assert Risk Engine Differentiation
    risk_kn1 = db.query(RiskAssessment).filter(RiskAssessment.detection_id == "KN-0001").first()
    risk_kn4 = db.query(RiskAssessment).filter(RiskAssessment.detection_id == "KN-0004").first()
    
    assert risk_kn1.risk_level in ["LOW", "MEDIUM"], f"Expected LOW/MEDIUM for KN-0001, got {risk_kn1.risk_level}"
    assert risk_kn4.risk_level in ["HIGH", "CRITICAL"], f"Expected HIGH/CRITICAL for KN-0004, got {risk_kn4.risk_level}"

    db.close()
    print("\n==================================================")
    print("  ALL BACKEND & INTELLIGENCE TESTS PASSED SUCCESSFULLY!  ")
    print("==================================================")


if __name__ == "__main__":
    run_tests()

from sqlalchemy.orm import Session


def compute_risk_assessment(db: Session, detection_id: str, evidence: dict) -> dict:
    """
    Computes an explainable risk score (0-100), risk level, reason breakdown,
    and recommended action using multi-source evidence fusion.
    """
    reasons = []
    
    # 1. Mining Probability (25% Weight)
    mining_prob = evidence.get("mining_probability", 0.0)
    mining_prob_score = mining_prob * 25.0
    if mining_prob > 0.70:
        reasons.append(f"High satellite mining probability ({round(mining_prob * 100, 1)}%)")

    # 2. Boundary Violation & Protected Area (20% Weight)
    boundary_score = 0.0
    if evidence.get("protected_area"):
        boundary_score = 20.0
        reasons.append("CRITICAL: Detected activity inside protected eco-sensitive forest zone")
    elif evidence.get("outside_permit"):
        boundary_score = 15.0
        reasons.append("Activity detected outside legal mining permit boundary")

    # 3. Volume Anomaly (20% Weight)
    vol_score = 0.0
    if evidence.get("volume_anomaly"):
        vol_mismatch = evidence.get("volume_mismatch_pct", 0.0)
        vol_score = min(20.0, (vol_mismatch / 100.0) * 20.0 if vol_mismatch > 0 else 20.0)
        reasons.append(f"Excavation volume mismatch vs permit limit ({round(vol_mismatch, 1)}% overrun)")

    # 4. GPS / Route Anomaly (15% Weight)
    gps_score = 0.0
    if evidence.get("gps_route_anomaly"):
        dev_km = evidence.get("route_deviation_km", 0.0)
        gps_score = 15.0
        reasons.append(f"Truck GPS route deviation detected ({round(dev_km, 1)} km off route)")

    # 5. RFID / Checkpoint & Weighbridge Anomaly (10% Weight)
    rfid_score = 0.0
    if evidence.get("rfid_mismatch"):
        rfid_score += 5.0
        reasons.append("RFID checkpoint scan mismatch or missed checkpoint")
    
    wb_mismatch = evidence.get("weighbridge_discrepancy_pct", 0.0)
    if wb_mismatch > 5.0:
        rfid_score += 5.0
        reasons.append(f"Weighbridge weight discrepancy vs e-Challan ({round(wb_mismatch, 1)}% difference)")
    rfid_score = min(10.0, rfid_score)

    # 6. Historical Change (10% Weight)
    hist_score = 0.0
    hist_growth = evidence.get("historical_change_pct", 0.0)
    if hist_growth > 30.0:
        hist_score = min(10.0, (hist_growth / 100.0) * 10.0)
        reasons.append(f"Rapid historical activity growth ({round(hist_growth, 1)}% increase)")

    # Total Score Calculation (Max 100)
    total_score = min(100.0, round(
        mining_prob_score + boundary_score + vol_score + gps_score + rfid_score + hist_score, 1
    ))

    # Risk Level Determination
    if total_score >= 81.0:
        risk_level = "CRITICAL"
        recommended_action = "Immediate Field Enforcement & Site Seizure"
    elif total_score >= 61.0:
        risk_level = "HIGH"
        recommended_action = "Priority Field Verification Inspection"
    elif total_score >= 31.0:
        risk_level = "MEDIUM"
        recommended_action = "Desk Review & Document Verification"
    else:
        risk_level = "LOW"
        recommended_action = "Routine Satellite Surveillance"

    if not reasons:
        reasons.append("All physical, spatial, and transport records are within normal parameters.")

    return {
        "detection_id": detection_id,
        "risk_score": total_score,
        "risk_level": risk_level,
        "scores": {
            "mining_prob_score": round(mining_prob_score, 2),
            "boundary_violation_score": round(boundary_score, 2),
            "volume_anomaly_score": round(vol_score, 2),
            "gps_anomaly_score": round(gps_score, 2),
            "rfid_anomaly_score": round(rfid_score, 2),
            "historical_change_score": round(hist_score, 2)
        },
        "evidence_breakdown": evidence,
        "reasons": reasons,
        "recommended_action": recommended_action
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from backend.app.database import get_db
from backend.app.models.models import Detection, RiskAssessment
from backend.app.schemas.schemas import DetectionResponse, SatelliteAnalysisRequest, RiskAssessmentResponse
from backend.app.services.ml_service import train_and_predict_detection
from backend.app.services.gis_service import check_location_legality
from backend.app.services.volume_service import analyze_volume
from backend.app.services.evidence_fusion_service import assemble_evidence
from backend.app.services.risk_engine_service import compute_risk_assessment

router = APIRouter(prefix="/api/satellite", tags=["Satellite Monitoring"])


@router.get("/detections", response_model=List[DetectionResponse])
def get_satellite_detections(db: Session = Depends(get_db)):
    """
    Returns satellite-derived mining detections.
    """
    return db.query(Detection).all()


@router.post("/analyze", response_model=RiskAssessmentResponse)
def analyze_satellite_observation(
    req: SatelliteAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyzes target location coordinates with spectral/spatial inputs and optional drone 3D volume estimate.
    Runs ML classifier, spatial GIS check, volume check, evidence fusion, and risk engine.
    """
    # 1. Run ML Mining Classifier
    ml_res = train_and_predict_detection(
        ndvi_change=req.ndvi_change,
        sar_vv_vh_ratio=req.sar_vv_vh_ratio,
        texture_variance=req.texture_variance,
        spectral_anomaly_score=0.85
    )

    # 2. Run GIS Spatial Check
    gis_res = check_location_legality(req.latitude, req.longitude)

    # 3. Create transient/new Detection object
    det_id = f"KN-{uuid.uuid4().hex[:6].upper()}"
    estimated_vol = req.drone_estimated_volume_m3 if req.drone_estimated_volume_m3 is not None else (req.area_ha * 10000.0 * 2.5)

    new_det = Detection(
        detection_id=det_id,
        latitude=req.latitude,
        longitude=req.longitude,
        area_ha=req.area_ha,
        estimated_depth_m=2.5,
        estimated_volume_m3=estimated_vol,
        ndvi_change=req.ndvi_change,
        sar_vv_vh_ratio=req.sar_vv_vh_ratio,
        texture_variance=req.texture_variance,
        spectral_anomaly_score=0.85,
        mining_probability=ml_res["mining_probability"],
        confidence_level=ml_res["confidence_level"],
        legal_status=gis_res["legal_status"],
        is_protected_area=gis_res["is_protected_area"],
        permit_id=gis_res["matched_permit_id"]
    )
    db.add(new_det)
    db.commit()

    # 4. Evidence Fusion & Risk Engine
    evidence = assemble_evidence(db, new_det)
    risk_res = compute_risk_assessment(db, det_id, evidence)

    return RiskAssessmentResponse(
        risk_id=f"RISK-{det_id}",
        detection_id=det_id,
        risk_score=risk_res["risk_score"],
        risk_level=risk_res["risk_level"],
        evidence_breakdown=evidence,
        reasons=risk_res["reasons"],
        recommended_action=risk_res["recommended_action"],
        created_at=new_det.detection_date or ""
    )

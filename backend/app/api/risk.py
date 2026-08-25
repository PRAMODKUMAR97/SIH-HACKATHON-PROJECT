import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.models import RiskAssessment, Detection
from backend.app.schemas.schemas import RiskAssessmentResponse
from backend.app.services.evidence_fusion_service import assemble_evidence
from backend.app.services.risk_engine_service import compute_risk_assessment

router = APIRouter(prefix="/api/risk", tags=["Risk Engine"])


@router.get("", response_model=List[RiskAssessmentResponse])
def get_all_risk_assessments(db: Session = Depends(get_db)):
    """
    Retrieves all evaluated risk assessments with evidence breakdowns and reasons.
    """
    assessments = db.query(RiskAssessment).all()
    results = []

    for r in assessments:
        det = db.query(Detection).filter(Detection.detection_id == r.detection_id).first()
        evidence = assemble_evidence(db, det) if det else {}
        reasons_list = json.loads(r.reasons) if r.reasons else []

        results.append(RiskAssessmentResponse(
            risk_id=r.risk_id,
            detection_id=r.detection_id,
            risk_score=r.risk_score,
            risk_level=r.risk_level,
            evidence_breakdown=evidence,
            reasons=reasons_list,
            recommended_action=r.recommended_action,
            created_at=r.created_at or ""
        ))
    return results


@router.get("/{detection_id}", response_model=RiskAssessmentResponse)
def get_risk_by_detection_id(detection_id: str, db: Session = Depends(get_db)):
    """
    Retrieves or calculates risk assessment for a specific detection.
    """
    det = db.query(Detection).filter(Detection.detection_id == detection_id).first()
    if not det:
        raise HTTPException(status_code=404, detail=f"Detection '{detection_id}' not found.")

    evidence = assemble_evidence(db, det)
    risk_res = compute_risk_assessment(db, detection_id, evidence)

    return RiskAssessmentResponse(
        risk_id=f"RISK-{detection_id}",
        detection_id=detection_id,
        risk_score=risk_res["risk_score"],
        risk_level=risk_res["risk_level"],
        evidence_breakdown=evidence,
        reasons=risk_res["reasons"],
        recommended_action=risk_res["recommended_action"],
        created_at=det.detection_date or ""
    )

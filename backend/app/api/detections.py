from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.models import Detection
from backend.app.schemas.schemas import DetectionResponse

router = APIRouter(prefix="/api/detections", tags=["Detections"])


@router.get("", response_model=List[DetectionResponse])
def get_all_detections(db: Session = Depends(get_db)):
    """
    Retrieves all recorded mining detections.
    """
    return db.query(Detection).all()


@router.get("/{detection_id}", response_model=DetectionResponse)
def get_detection_by_id(detection_id: str, db: Session = Depends(get_db)):
    """
    Retrieves a specific mining detection by ID.
    """
    det = db.query(Detection).filter(Detection.detection_id == detection_id).first()
    if not det:
        raise HTTPException(status_code=404, detail=f"Detection '{detection_id}' not found.")
    return det

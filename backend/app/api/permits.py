from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.models import Permit
from backend.app.schemas.schemas import PermitResponse

router = APIRouter(prefix="/api/permits", tags=["Permits"])


@router.get("", response_model=List[PermitResponse])
def get_all_permits(db: Session = Depends(get_db)):
    """
    Retrieves all registered mining lease permits.
    """
    return db.query(Permit).all()


@router.get("/{permit_id}", response_model=PermitResponse)
def get_permit_by_id(permit_id: str, db: Session = Depends(get_db)):
    """
    Retrieves details for a specific mining permit.
    """
    permit = db.query(Permit).filter(Permit.permit_id == permit_id).first()
    if not permit:
        raise HTTPException(status_code=404, detail=f"Permit '{permit_id}' not found.")
    return permit

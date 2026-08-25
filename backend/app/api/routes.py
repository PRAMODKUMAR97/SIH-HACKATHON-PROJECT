from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.models import GPSRecord
from backend.app.schemas.schemas import GPSRecordResponse

router = APIRouter(prefix="/api/routes", tags=["Routes & GPS"])


@router.get("", response_model=List[GPSRecordResponse])
def get_all_routes(db: Session = Depends(get_db)):
    """
    Retrieves all recorded truck GPS routes and checkpoint scans.
    """
    return db.query(GPSRecord).all()


@router.get("/{truck_id}", response_model=List[GPSRecordResponse])
def get_routes_by_truck_id(truck_id: str, db: Session = Depends(get_db)):
    """
    Retrieves GPS route records for a specific truck.
    """
    records = db.query(GPSRecord).filter(GPSRecord.truck_id == truck_id).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No GPS routes found for truck '{truck_id}'.")
    return records

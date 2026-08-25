from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.models import Truck
from backend.app.schemas.schemas import TruckResponse

router = APIRouter(prefix="/api/trucks", tags=["Trucks"])


@router.get("", response_model=List[TruckResponse])
def get_all_trucks(db: Session = Depends(get_db)):
    """
    Retrieves all monitored transportation trucks.
    """
    return db.query(Truck).all()


@router.get("/{truck_id}", response_model=TruckResponse)
def get_truck_by_id(truck_id: str, db: Session = Depends(get_db)):
    """
    Retrieves details for a specific truck.
    """
    truck = db.query(Truck).filter(Truck.truck_id == truck_id).first()
    if not truck:
        raise HTTPException(status_code=404, detail=f"Truck '{truck_id}' not found.")
    return truck

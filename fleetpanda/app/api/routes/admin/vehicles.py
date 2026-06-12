from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.vehicle import Vehicle

router = APIRouter(prefix="/api/admin/vehicles", tags=["Admin Vehicles"])


@router.get("")
def get_vehicles(db: Session = Depends(get_db)):

    return db.query(Vehicle).all()
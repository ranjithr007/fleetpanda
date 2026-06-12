from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.tracking_service import TrackingService

router = APIRouter(prefix="/api/driver/tracking", tags=["Driver Tracking"])


@router.post("/location")
def update_location(
    vehicle_id: int, latitude: float, longitude: float, db: Session = Depends(get_db)
):

    service = TrackingService(db)

    return service.update_location(vehicle_id, latitude, longitude)

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.session import get_db

from app.services.tracking_service import TrackingService

router = APIRouter(prefix="/api/admin/fleet", tags=["Admin Fleet"])


@router.get("/status")
def fleet_status(db: Session = Depends(get_db)):

    service = TrackingService(db)

    return service.fleet_status()
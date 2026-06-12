from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.session import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Admin Analytics"])


@router.get("/drivers")
def driver_performance(db: Session = Depends(get_db)):

    return AnalyticsService(db).driver_performance()


@router.get("/vehicles")
def vehicle_utilization(db: Session = Depends(get_db)):

    return AnalyticsService(db).vehicle_utilization()


@router.get("/incidents")
def incidents(db: Session = Depends(get_db)):

    return AnalyticsService(db).incident_summary()
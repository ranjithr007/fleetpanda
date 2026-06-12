from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Admin Dashboard"])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):

    service = DashboardService(db)

    return service.get_summary()
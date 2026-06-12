from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.incident_service import IncidentService

router = APIRouter(prefix="/incidents", tags=["Driver Incidents"])


@router.post("/report")
def report_incident(
    vehicle_id: int,
    shift_id: int,
    driver_id: int,
    incident_type: str,
    db: Session = Depends(get_db),
):

    service = IncidentService(db)

    return service.report_incident(vehicle_id, shift_id, driver_id, incident_type)


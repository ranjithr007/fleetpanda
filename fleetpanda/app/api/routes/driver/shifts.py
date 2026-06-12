from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.shift_service import ShiftService

from app.schemas.shift_schema import ShiftStartRequest

router = APIRouter(prefix="/api/driver/shifts", tags=["Driver Shifts"])


@router.post("/start")
def start_shift(request: ShiftStartRequest, db: Session = Depends(get_db)):

    service = ShiftService(db)

    return service.start_shift(request.driver_id, request.vehicle_id)


@router.post("/{shift_id}/end")
def end_shift(shift_id: int, db: Session = Depends(get_db)):

    service = ShiftService(db)

    return service.end_shift(shift_id)
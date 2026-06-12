from datetime import date, datetime

from fastapi import HTTPException

from app.models.shift import Shift
from app.models.vehicle_allocation import VehicleAllocation
from app.repositories.shift_repository import ShiftRepository


class ShiftService:

    def __init__(self, db):

        self.db = db
        self.repository = ShiftRepository(db)

    def start_shift(self, driver_id: int, vehicle_id: int):
        active_shift = self.repository.get_active_shift(driver_id)

        if active_shift:
            raise HTTPException(
                status_code=409, detail={"error_code": "SHIFT_ALREADY_ACTIVE"}
            )
        allocation = (
            self.db.query(VehicleAllocation)
            .filter(
                VehicleAllocation.driver_id == driver_id,
                VehicleAllocation.vehicle_id == vehicle_id,
                VehicleAllocation.allocation_date == date.today(),
                VehicleAllocation.status == "ALLOCATED",
            )
            .first()
        )

        if not allocation:

            raise HTTPException(status_code=400, detail="NO_VEHICLE_ALLOCATION")

        existing_shift = (
            self.db.query(Shift)
            .filter(Shift.allocation_id == allocation.id, Shift.status == "ACTIVE")
            .first()
        )

        if existing_shift:

            return existing_shift

       

        allocation.status = "ACTIVE"
        shift = Shift(
            allocation_id=allocation.id, start_time=datetime.utcnow(), status="ACTIVE"
        )

        self.db.add(shift)

        self.db.commit()

        self.db.refresh(shift)

        return shift

    def end_shift(self, shift_id: int):

        shift = self.db.query(Shift).filter(Shift.id == shift_id).first()

        if not shift:

            raise HTTPException(404, "SHIFT_NOT_FOUND")

        shift.status = "COMPLETED"

        shift.end_time = datetime.utcnow()

        self.db.commit()

        return shift
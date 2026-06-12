from app.models.shift import Shift
from app.models.vehicle_allocation import VehicleAllocation

class ShiftRepository:
    def __init__(self, db):

            self.db = db

    def get_active_shift(self, driver_id: int):

        return (
            self.db.query(Shift)
            .join(VehicleAllocation, Shift.allocation_id == VehicleAllocation.id)
            .filter(VehicleAllocation.driver_id == driver_id, Shift.status == "ACTIVE")
            .first()
        )


    def get_today_allocation(self, driver_id: int, vehicle_id: int, allocation_date):

        return (
            self.db.query(VehicleAllocation)
            .filter(
                VehicleAllocation.driver_id == driver_id,
                VehicleAllocation.vehicle_id == vehicle_id,
                VehicleAllocation.allocation_date == allocation_date,
                VehicleAllocation.status == "ALLOCATED",
            )
            .first()
        )
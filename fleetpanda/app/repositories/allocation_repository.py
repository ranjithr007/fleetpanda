from app.models.vehicle_allocation import VehicleAllocation
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.repositories.audit_repository import AuditRepository


class AllocationRepository:

    def __init__(self, db):
        self.db = db
        self.audit_repo = AuditRepository

    def create(self, allocation):

        self.db.add(allocation)

        self.db.commit()

        self.db.refresh(allocation)

        return allocation

    def get_by_vehicle_date(self, vehicle_id, allocation_date):

        return (
            self.db.query(VehicleAllocation)
            .filter(
                VehicleAllocation.vehicle_id == vehicle_id,
                VehicleAllocation.allocation_date == allocation_date,
                VehicleAllocation.status.in_(["ALLOCATED", "ACTIVE"]),
            )
            .first()
        )

    def list_all(self):

        return self.db.query(VehicleAllocation).all()

    def get_vehicle(self, vehicle_id: int):

        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_driver(self, driver_id: int):

        return self.db.query(Driver).filter(Driver.id == driver_id).first()

    def get_allocation(self, allocation_id: int):

        return (
            self.db.query(VehicleAllocation)
            .filter(VehicleAllocation.id == allocation_id)
            .first()
        )

    def get_active_vehicle_allocation(self, vehicle_id, allocation_date):

        return (
            self.db.query(VehicleAllocation)
            .filter(
                VehicleAllocation.vehicle_id == vehicle_id,
                VehicleAllocation.allocation_date == allocation_date,
                VehicleAllocation.status.in_(["ALLOCATED", "ACTIVE"]),
            )
            .first()
        )

    def update(self, allocation):

        self.db.add(allocation)

        self.db.commit()

        self.db.refresh(allocation)

        return allocation

    def cancel_allocation(self, allocation_id):

        allocation = self.repo.get_by_id(allocation_id)

        if allocation is None:
            raise Exception("Allocation not found")

        old_value = allocation.status

        allocation.status = "CANCELLED"

        self.db.commit()
        self.db.refresh(allocation)

        self.audit_repo.create(self,
            entity_name="VehicleAllocation",
            entity_id=allocation.id,
            action="CANCEL_ALLOCATION",
            old_value=old_value,
            new_value=allocation.status,
            performed_by="ADMIN",
        )

        return allocation
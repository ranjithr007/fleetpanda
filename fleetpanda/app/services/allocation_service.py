from datetime import date
from fastapi import HTTPException

from app.models.vehicle import VehicleStatus
from app.models.driver import DriverStatus

from sqlalchemy.exc import IntegrityError

from app.models.vehicle_allocation import VehicleAllocation, AllocationStatus

from app.repositories.allocation_repository import AllocationRepository
from app.services.audit_service import AuditService


class AllocationService:

    def __init__(self, db):

        self.db = db

        self.repo = AllocationRepository(db)
        self.audit_service = AuditService(db)

    def create_allocation(self, request):

        # 1. past date validation

        if request.allocation_date < date.today():

            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "PAST_ALLOCATION_NOT_ALLOWED",
                    "message": "Cannot create allocation for past date",
                },
            )

        # 2. vehicle validation

        vehicle = self.repo.get_vehicle(request.vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=404, detail={"error_code": "VEHICLE_NOT_FOUND"}
            )
        existing = self.repo.get_active_vehicle_allocation(
            request.vehicle_id, request.allocation_date
        )
        if existing:

            raise HTTPException(
                status_code=409, detail={"error_code": "VEHICLE_ALREADY_ALLOCATED"}
            )
        if vehicle.status != VehicleStatus.AVAILABLE.value:
            raise HTTPException(
                status_code=409,
                detail={
                    "error_code": "VEHICLE_NOT_AVAILABLE",
                    "message": "Vehicle cannot be allocated",
                },
            )

        
        # 3. driver validation

        driver = self.repo.get_driver(request.driver_id)
        if driver is None:
            raise HTTPException(
                status_code=404, detail={"error_code": "DRIVER_NOT_FOUND"}
            )

        if driver.status != DriverStatus.ACTIVE.value:
            raise HTTPException(
                status_code=409, detail={"error_code": "DRIVER_NOT_ACTIVE"}
            )

        allocation = VehicleAllocation(
            vehicle_id=request.vehicle_id,
            driver_id=request.driver_id,
            allocation_date=request.allocation_date,
            status="ALLOCATED",
        )

        try:

            return self.repo.create(allocation)

        except IntegrityError:

            self.db.rollback()

            raise HTTPException(status_code=409, detail="ALLOCATION_CONFLICT")

    def cancel_allocation(self, allocation_id: int):

        allocation = self.repo.get_allocation(allocation_id)

        if allocation is None:

            raise HTTPException(
                status_code=404, detail={"error_code": "ALLOCATION_NOT_FOUND"}
            )

        if allocation.status == AllocationStatus.ACTIVE.value:

            raise HTTPException(
                status_code=409, detail={"error_code": "SHIFT_ALREADY_STARTED"}
            )
        old_status = allocation.status
        allocation.status = AllocationStatus.CANCELLED.value
        self.audit_service.log(
            
            action="ALLOCATION_CANCELLED",
            entity_name="vehicle_allocations",
            entity_id=allocation.id,
            old_value=old_status,
            new_value="CANCELLED",
            performed_by="ADMIN",
        )
        self.repo.update(allocation)

        return allocation

    def list_allocations(self):

        return self.repo.list_all()
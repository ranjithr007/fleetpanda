from datetime import date

from sqlalchemy.exc import IntegrityError

from app.models.vehicle import VehicleStatus
from app.models.driver import DriverStatus

from app.models.vehicle_allocation import (
    VehicleAllocation,
    AllocationStatus,
)

from app.repositories.allocation_repository import AllocationRepository
from app.services.audit_service import AuditService

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)


class AllocationService:

    def __init__(self, db):

        self.db = db
        self.repo = AllocationRepository(db)
        self.audit_service = AuditService(db)

    def create_allocation(self, request):

        try:

            if request.allocation_date < date.today():

                raise NotFoundException(
                    "PAST_ALLOCATION_NOT_ALLOWED",
                    "Cannot create allocation for past date",
                )

            vehicle = self.repo.get_vehicle(request.vehicle_id)

            if vehicle is None:

                raise NotFoundException(
                    "VEHICLE_NOT_FOUND",
                    "Vehicle not found",
                )

            existing = self.repo.get_active_vehicle_allocation(
                request.vehicle_id,
                request.allocation_date,
            )

            if existing:

                raise ConflictException(
                    "VEHICLE_ALREADY_ALLOCATED",
                    "Vehicle already allocated",
                )

            if vehicle.status != VehicleStatus.AVAILABLE.value:

                raise ConflictException(
                    "VEHICLE_NOT_AVAILABLE",
                    "Vehicle cannot be allocated",
                )

            driver = self.repo.get_driver(request.driver_id)

            if driver is None:

                raise NotFoundException(
                    "DRIVER_NOT_FOUND",
                    "Driver not found",
                )

            if driver.status != DriverStatus.ACTIVE.value:

                raise ConflictException(
                    "DRIVER_NOT_ACTIVE",
                    "Driver not active",
                )

            allocation = VehicleAllocation(
                vehicle_id=request.vehicle_id,
                driver_id=request.driver_id,
                allocation_date=request.allocation_date,
                status=AllocationStatus.ACTIVE.value,
            )

            allocation = self.repo.create(allocation)
            vehicle.status = VehicleStatus.ALLOCATED.value
            self.audit_service.log(
                action="ALLOCATION_CREATED",
                entity_name="vehicle_allocations",
                entity_id=allocation.id,
                old_value=None,
                new_value="ACTIVE",
                performed_by="ADMIN",
            )

            self.db.commit()

            self.db.refresh(allocation)

            return allocation

        except IntegrityError:

            self.db.rollback()

            raise ConflictException(
                "ALLOCATION_CONFLICT",
                "Vehicle or driver already allocated",
            )

        except Exception:

            self.db.rollback()
            raise

    def cancel_allocation(self, allocation_id: int):

        try:

            allocation = self.repo.get_allocation(allocation_id)

            if allocation is None:

                raise NotFoundException(
                    "ALLOCATION_NOT_FOUND",
                    "Allocation not found",
                )

            if allocation.status == AllocationStatus.ACTIVE.value:

                raise ConflictException(
                    "SHIFT_ALREADY_STARTED",
                    "Shift already started",
                )

            old_status = allocation.status

            allocation.status = AllocationStatus.CANCELLED.value
            allocation.vehicle.status = VehicleStatus.AVAILABLE.value

            self.repo.update(allocation)

            self.audit_service.log(
                action="ALLOCATION_CANCELLED",
                entity_name="vehicle_allocations",
                entity_id=allocation.id,
                old_value=old_status,
                new_value="CANCELLED",
                performed_by="ADMIN",
            )

            self.db.commit()

            return allocation

        except Exception:

            self.db.rollback()
            raise

    def list_allocations(self):

        return self.repo.list_all()
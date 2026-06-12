from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services.allocation_service import AllocationService
from app.schemas.allocation_schema import AllocationRequest, AllocationResponse

router = APIRouter(prefix="/api/admin/allocations", tags=["Admin Allocations"])


@router.post("", response_model=AllocationResponse)
def allocate_vehicle(request: AllocationRequest, db: Session = Depends(get_db)):

    service = AllocationService(db)

    return service.create_allocation(request)


@router.get("", response_model=list[AllocationResponse])
def get_allocations(db: Session = Depends(get_db)):

    service = AllocationService(db)

    return service.list_allocations()


@router.post("/{allocation_id}/cancel")
def cancel_allocation(allocation_id: int, db: Session = Depends(get_db)):

    service = AllocationService(db)

    return service.cancel_allocation(allocation_id)
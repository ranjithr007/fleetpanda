
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.services.delivery_service import DeliveryService

router = APIRouter(prefix="/api/driver/deliveries", tags=["Driver Deliveries"])


@router.get("/{driver_id}")
def my_deliveries(driver_id: int, db: Session = Depends(get_db)):

    service = DeliveryService(db)

    return service.get_driver_deliveries(driver_id)


@router.post("/{order_id}/complete")
def complete_delivery(order_id: int, db: Session = Depends(get_db)):

    service = DeliveryService(db)

    return service.complete_delivery(order_id)


@router.post("/{order_id}/fail")
def fail_delivery(order_id: int, reason: str, db: Session = Depends(get_db)):

    service = DeliveryService(db)

    return service.fail_delivery(order_id, reason)


@router.post("/{order_id}/start")
def start_delivery(order_id: int, db: Session = Depends(get_db)):

    service = DeliveryService(db)

    return service.start_delivery(order_id)
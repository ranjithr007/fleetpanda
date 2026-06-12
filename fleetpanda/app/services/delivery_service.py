from fastapi import HTTPException

from datetime import datetime

from app.repositories.delivery_repository import DeliveryRepository

from app.models.inventory import Inventory

from app.models.inventory_transaction import InventoryTransaction
from app.events.event_bus import event_bus

from app.events.events import DeliveryCompletedEvent
from app.services.audit_service import AuditService


class DeliveryService:

    def __init__(self, db):

        self.db = db

        self.repo = DeliveryRepository(db)

        self.audit_service = AuditService(db)

    def get_driver_deliveries(self, driver_id: int):

        return self.repo.get_driver_orders(driver_id)

    def complete_delivery(self, order_id: int):

        order = self.repo.get_order(order_id)

        if not order:
            raise HTTPException(
                status_code=404, detail={"error_code": "ORDER_NOT_FOUND"}
            )
        if order.status == "ASSIGNED":
            raise HTTPException(
                status_code=409, detail={"error_code": "ORDER_NOT_STARTED"}
            )

        if order.status == "COMPLETED":
            raise HTTPException(
                status_code=409, detail={"error_code": "ORDER_ALREADY_COMPLETED"}
            )

        try:

            for item in order.items:

                inventory = (
                    self.db.query(Inventory)
                    .filter(
                        Inventory.location_id == order.destination_id,
                        Inventory.product_id == item.product_id,
                    )
                    .first()
                )

                if not inventory:

                    inventory = Inventory(
                        location_id=order.destination_id,
                        product_id=item.product_id,
                        quantity=0,
                    )

                    self.db.add(inventory)

                inventory.quantity += item.quantity_gallons

                transaction = InventoryTransaction(
                    inventory=inventory,
                    order_id=order.id,
                    transaction_type="DELIVERY_COMPLETED",
                    quantity=item.quantity_gallons,
                )

                self.repo.add_transaction(transaction)

            order.status = "COMPLETED"
            self.audit_service.log(
                entity_name="orders",
                entity_id=order.id,
                action="DELIVERY_COMPLETED",
                old_value="IN_PROGRESS",
                new_value="COMPLETED",
                performed_by="DRIVER",
            )
            self.repo.update_without_commit(order)

            self.db.commit()

            self.db.refresh(order)
            event_bus.publish(
                DeliveryCompletedEvent(
                    order_id=order.id,
                    driver_id=order.shift.allocation.driver_id,
                    vehicle_id=order.shift.allocation.vehicle_id,
                )
            )
            return order

        except Exception:

            self.db.rollback()

            raise

    def fail_delivery(self, order_id: int, reason: str):

        order = self.repo.get_order(order_id)

        if not order:

            raise HTTPException(404, "ORDER_NOT_FOUND")

        order.status = "FAILED"

        order.failure_reason = reason

        self.db.commit()

        return order

    def start_delivery(self, order_id: int):

        order = self.repo.get_order(order_id)

        if not order:
            raise HTTPException(
                status_code=404, detail={"error_code": "ORDER_NOT_FOUND"}
            )

        if order.status != "ASSIGNED":
            raise HTTPException(
                status_code=409, detail={"error_code": "INVALID_ORDER_STATE"}
            )

        order.status = "IN_PROGRESS"

        self.repo.update_without_commit(order)

        self.db.commit()
        self.db.refresh(order)

        return order
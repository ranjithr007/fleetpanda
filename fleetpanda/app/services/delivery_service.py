from fastapi import HTTPException

from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.inventory_repository import InventoryRepository

from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction

from app.events.event_bus import event_bus
from app.events.events import DeliveryCompletedEvent

from app.services.audit_service import AuditService
from app.core.exceptions import (
    ConflictException,
    NotFoundException,
    AccessDeniedException,
)


class DeliveryService:

    def __init__(self, db):

        self.db = db

        self.repo = DeliveryRepository(db)

        self.inventory_repo = InventoryRepository(db)

        self.audit_service = AuditService(db)

    def get_driver_deliveries(self, driver_id: int):

        return self.repo.get_driver_orders(driver_id)

    def complete_delivery(self, order_id: int, driver_id: int | None = None):

        try:

            # 1. lock order row
            order = self.repo.get_order_for_update(order_id)

            if not order:
                raise NotFoundException(
                    "ORDER_NOT_FOUND",
                    "Order not found",
                )

            # 2. ownership validation first

            allocation_driver_id = order.shift.allocation.driver_id

            if driver_id is not None and allocation_driver_id != driver_id:
                raise AccessDeniedException(
                    "DELIVERY_ACCESS_DENIED",
                    "Driver does not have access to complete this delivery",
                )

            # 3. business state checks

            if order.status == "ASSIGNED":
                raise ConflictException(
                    "ORDER_NOT_STARTED", "Delivery has not been started yet"
                )

            if order.status == "COMPLETED":
                raise ConflictException(
                    "ORDER_ALREADY_COMPLETED", "Delivery has already been completed"
                )

            if order.shift.status != "ACTIVE":
                raise ConflictException(
                    "SHIFT_NOT_ACTIVE", "Cannot complete delivery for inactive shift"
                )

            old_status = order.status

            # 4. inventory updates

            for item in order.items:

                inventory = self.inventory_repo.get_inventory_for_update(
                    order.destination_id, item.product_id
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

            # 5. concurrency-safe completion

            updated = self.repo.complete_delivery_atomic(order.id)

            if updated == 0:
                raise ConflictException(
                    "CONCURRENT_MODIFICATION", "Order was modified by another process"
                )

            # 6. audit

            self.audit_service.log(
                entity_name="orders",
                entity_id=order.id,
                action="DELIVERY_COMPLETED",
                old_value=old_status,
                new_value="COMPLETED",
                performed_by="DRIVER",
            )

            self.db.commit()

            self.db.refresh(order)

            # 7. publish after commit

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

    def fail_delivery(self, order_id: int, reason: str, driver_id: int):

        try:

            order = self.repo.get_order_for_update(order_id)

            if not order:
                raise NotFoundException("ORDER_NOT_FOUND", "Order not found")

            if order.status == "COMPLETED":
                raise ConflictException(
                    "ORDER_ALREADY_COMPLETED", "Delivery has already been completed"
                )

            if order.shift.allocation.driver_id != driver_id:
                raise AccessDeniedException(
                    "DELIVERY_ACCESS_DENIED",
                    "Driver does not have access to fail this delivery",
                )

            old_status = order.status

            order.status = "FAILED"

            order.failure_reason = reason

            self.repo.update_without_commit(order)

            self.audit_service.log(
                entity_name="orders",
                entity_id=order.id,
                action="DELIVERY_FAILED",
                old_value=old_status,
                new_value="FAILED",
                performed_by="DRIVER",
            )

            self.db.commit()

            return order

        except Exception:

            self.db.rollback()

            raise

    def start_delivery(self, order_id: int):

        try:

            order = self.repo.get_order(order_id)

            if not order:
                raise NotFoundException("ORDER_NOT_FOUND", "Order not found")

            if order.status != "ASSIGNED":
                raise ConflictException(
                    "INVALID_ORDER_STATE",
                    "Order must be in ASSIGNED state to start delivery",
                )

            order.status = "IN_PROGRESS"

            self.repo.update_without_commit(order)

            self.db.commit()

            self.db.refresh(order)

            return order

        except Exception:

            self.db.rollback()

            raise
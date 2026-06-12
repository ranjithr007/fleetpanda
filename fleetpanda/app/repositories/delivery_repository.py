from app.models.order import Order
from app.models.shift import Shift
from app.models.vehicle_allocation import VehicleAllocation


class DeliveryRepository:

    def __init__(self, db):

        self.db = db

    def get_driver_orders(self, driver_id: int):

        return (
            self.db.query(Order)
            .join(Shift, Order.shift_id == Shift.id)
            .join(VehicleAllocation, Shift.allocation_id == VehicleAllocation.id)
            .filter(VehicleAllocation.driver_id == driver_id)
            .all()
        )

    def get_order(self, order_id: int):

        return self.db.query(Order).filter(Order.id == order_id).first()

    def update_without_commit(self, order):

        self.db.commit()

        self.db.refresh(order)

        return order
    def add_transaction(self, transaction):

        self.db.add(transaction)

        return transaction

from sqlalchemy import func


from app.models.driver import Driver
from app.models.shift import Shift
from app.models.vehicle import Vehicle
from app.models.vehicle_allocation import VehicleAllocation
from app.models.order import Order
from app.models.vehicle_incident import VehicleIncident


class AnalyticsRepository:

    def __init__(self, db):

        self.db = db

    # =========================
    # DRIVER PERFORMANCE
    # =========================

    def driver_performance(self):

        return (
            self.db.query(
                Driver.id.label("driver_id"),
                func.count(Order.id).label("total_deliveries"),
            )
            .join(VehicleAllocation, VehicleAllocation.driver_id == Driver.id)
            .join(Shift, Shift.allocation_id == VehicleAllocation.id)
            .join(Order, Order.shift_id == Shift.id)
            .group_by(Driver.id)
            .all()
        )

    def vehicle_utilization(self):

        return (
            self.db.query(
                Vehicle.id.label("vehicle_id"),
                func.count(Shift.id).label("total_shifts"),
            )
            .join(VehicleAllocation, VehicleAllocation.vehicle_id == Vehicle.id)
            .join(Shift, Shift.allocation_id == VehicleAllocation.id)
            .group_by(Vehicle.id)
            .all()
        )

    def incident_summary(self):

        return (
            self.db.query(VehicleIncident.incident_type, func.count(VehicleIncident.id))
            .group_by(VehicleIncident.incident_type)
            .all()
        )
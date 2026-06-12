from sqlalchemy import func


from app.models.driver import Driver
from app.models.vehicle import Vehicle
from app.models.vehicle_allocation import VehicleAllocation
from app.models.vehicle_incident import VehicleIncident
from app.models.order import Order
from app.models.shift import Shift


class OptimizationRepository:

    def __init__(self, db):

        self.db = db

    def available_drivers(self):

        allocated = self.db.query(VehicleAllocation.driver_id).filter(
            VehicleAllocation.status.in_(["ALLOCATED", "ACTIVE"])
        )

        return (
            self.db.query(Driver)
            .filter(Driver.status == "ACTIVE", ~Driver.id.in_(allocated))
            .all()
        )

    def available_vehicles(self):

        incidents = self.db.query(VehicleIncident.vehicle_id).filter(
            VehicleIncident.status == "OPEN"
        )

        return (
            self.db.query(Vehicle)
            .filter(Vehicle.status == "AVAILABLE", ~Vehicle.id.in_(incidents))
            .all()
        )
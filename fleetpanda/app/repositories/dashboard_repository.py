from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.shift import Shift
from app.models.order import Order
from app.models.vehicle_incident import VehicleIncident


class DashboardRepository:

    def __init__(self, db):

        self.db = db

    def summary(self):

        return {
            "total_vehicles": self.db.query(Vehicle).count(),
            "available_vehicles": self.db.query(Vehicle)
            .filter(Vehicle.status == "AVAILABLE")
            .count(),
            "out_of_service": self.db.query(Vehicle)
            .filter(Vehicle.status == "OUT_OF_SERVICE")
            .count(),
            "active_drivers": self.db.query(Driver)
            .filter(Driver.status == "ACTIVE")
            .count(),
            "active_shifts": self.db.query(Shift)
            .filter(Shift.status == "ACTIVE")
            .count(),
            "open_incidents": self.db.query(VehicleIncident)
            .filter(VehicleIncident.status == "OPEN")
            .count(),
            "completed_orders": self.db.query(Order)
            .filter(Order.status == "COMPLETED")
            .count(),
        }
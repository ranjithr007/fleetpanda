from app.models.vehicle import Vehicle
from app.repositories.base_repository import BaseRepository


class VehicleRepository(BaseRepository):

    def get_available_vehicle(self):

        return (
            self.db.query(Vehicle)
            .filter(Vehicle.status == "AVAILABLE", Vehicle.is_active == True)
            .with_for_update()
            .first()
        )

    def update_status(self, vehicle, status):

        vehicle.status = status

        self.db.commit()

        return vehicle

    def get_all(self):

        return self.db.query(Vehicle).all()
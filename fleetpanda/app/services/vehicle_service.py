from app.repositories.vehicle_repository import VehicleRepository


class VehicleService:

    def __init__(self, db):

        self.repo = VehicleRepository(db)

    def get_available(self):

        return self.repo.get_available_vehicle()

    def get_all(self):

        return self.repo.get_all()
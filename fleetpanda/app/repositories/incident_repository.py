from app.models.vehicle_incident import VehicleIncident


class IncidentRepository:

    def __init__(self, db):

        self.db = db

    def create(self, incident):

        self.db.add(incident)

        self.db.commit()

        self.db.refresh(incident)

        return incident

    def get_open_incident(self, vehicle_id: int):

        return (
            self.db.query(VehicleIncident)
            .filter(
                VehicleIncident.vehicle_id == vehicle_id,
                VehicleIncident.status == "OPEN",
            )
            .first()
        )
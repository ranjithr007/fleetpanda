from fastapi import HTTPException


from app.repositories.incident_repository import IncidentRepository


from app.models.vehicle_incident import VehicleIncident
from app.models.vehicle import Vehicle
from app.events.event_bus import event_bus

from app.events.events import IncidentCreatedEvent

from app.services.audit_service import AuditService


class IncidentService:

    def __init__(self, db):

        self.db = db

        self.repository = IncidentRepository(db)
        self.audit_service = AuditService(db)

    def report_incident(
        self, vehicle_id: int, shift_id: int, driver_id: int, incident_type: str
    ):

        existing = self.repository.get_open_incident(vehicle_id)

        if existing:
            raise HTTPException(
                status_code=409,
                detail={"error_code": "INCIDENT_ALREADY_OPEN"},
            )

        vehicle = self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail={"error_code": "VEHICLE_NOT_FOUND"},
            )

        old_value = vehicle.status

        incident = VehicleIncident(
            vehicle_id=vehicle_id,
            shift_id=shift_id,
            driver_id=driver_id,
            incident_type=incident_type,
            status="OPEN",
        )

        # update vehicle
        vehicle.status = "OUT_OF_SERVICE"

        # 1. SAVE INCIDENT FIRST
        incident = self.repository.create(incident)

        # now available
        # incident.id != None

        # 2. AUDIT AFTER SAVE
        self.audit_service.log(
            entity_name="vehicle_incidents",
            entity_id=incident.id,
            action="OUT_OF_SERVICE",
            old_value=old_value,
            new_value=vehicle.status,
            performed_by="DRIVER",
        )

        # 3. EVENT AFTER SAVE
        event_bus.publish(
            IncidentCreatedEvent(
                incident_id=incident.id,
                vehicle_id=vehicle_id,
            )
        )

        return incident
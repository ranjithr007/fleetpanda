from datetime import datetime
from fastapi import HTTPException
from app.models.shift import Shift
from app.models.vehicle_allocation import VehicleAllocation
from app.models.gps_location_history import GPSLocationHistory
from app.repositories.tracking_repository import TrackingRepository


class TrackingService:

    def __init__(self, db):

        self.db = db

        self.repo = TrackingRepository(db)

    def update_location(self, vehicle_id, latitude, longitude, event_id=None):

        active_shift = (
            self.db.query(Shift)
            .join(VehicleAllocation)
            .filter(
                VehicleAllocation.vehicle_id == vehicle_id, Shift.status == "ACTIVE"
            )
            .first()
        )

        if not active_shift:

            raise HTTPException(status_code=400, detail="NO_ACTIVE_SHIFT")
        if event_id:
            existing = self.repository.get_by_event_id(event_id)

            if existing:
                return existing

        gps = GPSLocationHistory(
            vehicle_id=vehicle_id,
            shift_id=active_shift.id,
            latitude=latitude,
            longitude=longitude,
            event_id=event_id,
            timestamp=datetime.now(),
        )

        return self.repo.save_location(gps)

    def fleet_status(self):

        return self.repo.fleet_status()
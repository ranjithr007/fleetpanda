
from app.models.gps_location_history import GPSLocationHistory

from app.models.vehicle_current_location import VehicleCurrentLocation
from app.models.gps import GPS

from datetime import datetime


class TrackingRepository:

    def __init__(self, db):

        self.db = db

    def save_location(self, gps):

        try:

            self.db.add(gps)

            current = (
                self.db.query(VehicleCurrentLocation)
                .filter(VehicleCurrentLocation.vehicle_id == gps.vehicle_id)
                .first()
            )

            if current:

                if current.last_updated and gps.timestamp < current.last_updated:

                    return current

                current.latitude = gps.latitude
                current.longitude = gps.longitude
                current.last_updated = gps.timestamp

            else:

                current = VehicleCurrentLocation(
                    vehicle_id=gps.vehicle_id,
                    shift_id=gps.shift_id,
                    latitude=gps.latitude,
                    longitude=gps.longitude,
                    last_updated=gps.timestamp,
                )

                self.db.add(current)

            self.db.commit()

            self.db.refresh(gps)

            return gps

        except Exception:

            self.db.rollback()

            raise

    def fleet_status(self):

        return self.db.query(VehicleCurrentLocation).all()

    def get_by_event_id(self, event_id: str):

        return self.db.query(GPS).filter(GPS.event_id == event_id).first()
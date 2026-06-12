from sqlalchemy import *
from datetime import datetime

from app.database.session import Base


class VehicleCurrentLocation(Base):

    __tablename__ = "vehicle_current_location"

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True)

    shift_id = Column(Integer, ForeignKey("shifts.id"))

    latitude = Column(Float)

    longitude = Column(Float)

    last_updated = Column(DateTime, default=datetime.utcnow)
from sqlalchemy import *
from datetime import datetime

from app.database.session import Base


class GPSLocationHistory(Base):

    __tablename__ = "gps_location_history"

    id = Column(Integer, primary_key=True)

    shift_id = Column(Integer, ForeignKey("shifts.id"))

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    latitude = Column(Float)

    longitude = Column(Float)

    timestamp = Column(DateTime, default=datetime.now)
    event_id = Column(String(100), nullable=True)

    __table_args__ = (Index("IX_GPS_vehicle_time", "vehicle_id", "timestamp"),)
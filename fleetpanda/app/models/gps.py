from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey,String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.session import Base


class GPS(Base):

    __tablename__ = "gps_locations"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    speed = Column(Float, nullable=True)

    recorded_at = Column(DateTime, default=datetime.now, index=True)

    vehicle = relationship("Vehicle")
    event_id = Column(String(100), unique=True, nullable=True, index=True)
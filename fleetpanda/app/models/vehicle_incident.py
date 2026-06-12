from sqlalchemy import *
from datetime import datetime

from app.database.session import Base


class VehicleIncident(Base):

    __tablename__ = "vehicle_incidents"

    id = Column(Integer, primary_key=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    shift_id = Column(Integer, ForeignKey("shifts.id"))

    driver_id = Column(Integer, ForeignKey("drivers.id"))

    incident_type = Column(String(50))

    status = Column(String(30), default="OPEN")

    created_at = Column(DateTime, default=datetime.now)
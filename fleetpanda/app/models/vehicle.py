from sqlalchemy import *
from datetime import datetime

from app.database.session import Base
from sqlalchemy.orm import relationship
from enum import Enum

class VehicleStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ALLOCATED = "ALLOCATED"
    IN_SERVICE = "IN_SERVICE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    MAINTENANCE = "MAINTENANCE"

class Vehicle(Base):

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)

    vehicle_number = Column(String(50), unique=True)

    capacity_gallons = Column(Integer)

    status = Column(String(30), default="AVAILABLE")

    is_active = Column(Boolean, default=True)

    allocations = relationship("VehicleAllocation", back_populates="vehicle")

    created_at = Column(DateTime, default=datetime.now)



from sqlalchemy import Column, Integer, Date, String, ForeignKey, DateTime

from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.session import Base
from enum import Enum

class VehicleAllocation(Base):

    __tablename__ = "vehicle_allocations"

    id = Column(Integer, primary_key=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)

    allocation_date = Column(Date, nullable=False)

    status = Column(String(30), default="ALLOCATED")

    cancel_reason = Column(String(300))

    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="allocations")

    driver = relationship("Driver", back_populates="allocations")

    shift = relationship("Shift", back_populates="allocation", uselist=False)

class AllocationStatus(str, Enum):

    ALLOCATED = "ALLOCATED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
from sqlalchemy import *
from sqlalchemy.orm import relationship

from app.database.session import Base
from enum import Enum

class DriverStatus(str, Enum):

    ACTIVE = "ACTIVE"

    INACTIVE = "INACTIVE"

    ON_LEAVE = "ON_LEAVE"

    SUSPENDED = "SUSPENDED"


class Driver(Base):

    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    license_number = Column(String(50), nullable=False)

    experience_years = Column(Integer)

    status = Column(String(30), default="AVAILABLE")

    user = relationship("User", back_populates="driver")

    allocations = relationship("VehicleAllocation", back_populates="driver")
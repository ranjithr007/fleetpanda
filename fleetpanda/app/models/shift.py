from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.session import Base


class Shift(Base):

    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)

    allocation_id = Column(Integer, ForeignKey("vehicle_allocations.id"))

    start_time = Column(DateTime)

    end_time = Column(DateTime)

    status = Column(String(30), default="CREATED")

    created_at = Column(DateTime, default=datetime.utcnow)

    allocation = relationship("VehicleAllocation", back_populates="shift")

    orders = relationship("Order", back_populates="shift")
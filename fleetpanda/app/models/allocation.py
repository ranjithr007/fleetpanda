from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.session import Base


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)

    allocated_at = Column(DateTime)

    user = relationship("User")
    vehicle = relationship("Vehicle")
    shift = relationship("Shift")
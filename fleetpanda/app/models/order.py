from sqlalchemy import *
from sqlalchemy.orm import relationship

from app.database.session import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    shift_id = Column(Integer, ForeignKey("shifts.id"))

    destination_id = Column(Integer, ForeignKey("locations.id"))

    sequence_number = Column(Integer)

    status = Column(String(30), default="ASSIGNED")

    failure_reason = Column(String(300))

    shift = relationship("Shift", back_populates="orders")

    destination = relationship("Location", back_populates="orders")

    items = relationship("OrderItem", back_populates="order")
from sqlalchemy import *
from sqlalchemy.orm import relationship

from app.database.session import Base


class Location(Base):

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    location_type = Column(String(20), nullable=False)

    address = Column(String(300))

    latitude = Column(Float)

    longitude = Column(Float)

    orders = relationship("Order", back_populates="destination")
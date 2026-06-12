
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from datetime import datetime

from app.database.session import Base
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    phone = Column(String(20))

    role = Column(String(20), nullable=False)

    status = Column(String(20), default="ACTIVE")

    is_active = Column(Boolean, default=True)

    driver = relationship("Driver", back_populates="user", uselist=False)

    created_at = Column(DateTime, default=datetime.now)
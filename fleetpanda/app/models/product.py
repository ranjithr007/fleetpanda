from sqlalchemy import *

from app.database.session import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True)

    unit = Column(String(20), default="GALLON")

    status = Column(String(20), default="ACTIVE")
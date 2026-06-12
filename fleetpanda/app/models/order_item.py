from sqlalchemy import *
from sqlalchemy.orm import relationship

from app.database.session import Base


class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"))

    product_id = Column(Integer, ForeignKey("products.id"))

    quantity_gallons = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
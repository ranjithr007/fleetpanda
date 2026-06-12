from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.session import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Float, nullable=False, default=0)

    updated_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("InventoryTransaction", back_populates="inventory")

    __table_args__ = (CheckConstraint("quantity >= 0", name="CK_inventory_positive"),)
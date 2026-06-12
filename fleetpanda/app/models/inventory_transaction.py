from sqlalchemy import *
from datetime import datetime

from sqlalchemy.orm import relationship

from app.database.session import Base


class InventoryTransaction(Base):

    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True)

    inventory_id = Column(Integer, ForeignKey("inventory.id"))

    order_id = Column(Integer, ForeignKey("orders.id"))

    transaction_type = Column(String(50))

    quantity = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    inventory = relationship("Inventory", back_populates="transactions")
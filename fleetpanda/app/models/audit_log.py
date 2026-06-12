from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime

from app.database.session import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    entity_name = Column(String(100), nullable=False)

    entity_id = Column(Integer, nullable=False)

    action = Column(String(100), nullable=False)

    old_value = Column(String(500), nullable=True)

    new_value = Column(String(500), nullable=True)

    performed_by = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.now)
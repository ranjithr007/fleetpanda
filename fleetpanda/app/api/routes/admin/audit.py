from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.audit_log import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/logs")
def logs(db: Session = Depends(get_db)):

    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
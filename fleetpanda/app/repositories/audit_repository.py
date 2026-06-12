from app.models.audit_log import AuditLog


class AuditRepository:

    def __init__(self, db):

        self.db = db

    def create(
        self,
        entity_name,
        entity_id,
        action,
        old_value=None,
        new_value=None,
        performed_by="SYSTEM",
    ):

        log = AuditLog(
            entity_name=entity_name,
            entity_id=entity_id,
            action=action,
            old_value=old_value,
            new_value=new_value,
            performed_by=performed_by,
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log

    def get_all(self):

        return self.db.query(AuditLog).all()
from app.models.audit_log import AuditLog

from app.repositories.audit_repository import AuditRepository


class AuditService:

    def __init__(self, db):

        self.repo = AuditRepository(db)

    def log(
        self,
        entity_name,
        entity_id,
        action,
        old_value=None,
        new_value=None,
        performed_by=None,
    ):

        return self.repo.create(
            entity_name=entity_name,
            entity_id=entity_id,
            action=action,
            old_value=str(old_value),
            new_value=str(new_value),
            performed_by=performed_by,
        )
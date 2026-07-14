from typing import Any

from sqlalchemy.orm import Session

from ai_commerce_engine.models import AuditLog


def record_audit(
    session: Session,
    *,
    event_type: str,
    entity_type: str,
    entity_id: int | None,
    actor: str,
    action: str,
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
    details: str | None = None,
) -> AuditLog:
    log = AuditLog(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        actor=actor,
        action=action,
        before=before,
        after=after,
        details=details,
    )
    session.add(log)
    return log

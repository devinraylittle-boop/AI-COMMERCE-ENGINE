from sqlalchemy.orm import Session

from ai_commerce_engine.models import Product, StatusHistory
from ai_commerce_engine.schemas.domain import StatusChange
from ai_commerce_engine.services.audit import record_audit

PIPELINE_STATUSES = (
    "Discovered",
    "Initial review",
    "Rejected",
    "Deep research",
    "Supplier verification",
    "Validation planned",
    "Validation active",
    "Validation failed",
    "Validation passed",
    "Store candidate",
    "Live",
    "Scaling",
    "Paused",
    "Retired",
)


def change_status(session: Session, change: StatusChange) -> StatusHistory:
    product = session.get(Product, change.product_id)
    if product is None:
        raise ValueError(f"Product {change.product_id} does not exist")
    previous = product.status
    if previous == change.new_status:
        raise ValueError("New status must differ from current status")
    product.status = change.new_status
    history = StatusHistory(
        product_id=product.id,
        previous_status=previous,
        new_status=change.new_status,
        reason=change.reason,
        actor=change.actor,
        supporting_evidence=change.supporting_evidence,
        next_action=change.next_action,
    )
    session.add(history)
    record_audit(
        session,
        event_type="status_change",
        entity_type="product",
        entity_id=product.id,
        actor=change.actor,
        action="change_status",
        before={"status": previous},
        after={"status": change.new_status},
        details=change.reason,
    )
    session.flush()
    return history

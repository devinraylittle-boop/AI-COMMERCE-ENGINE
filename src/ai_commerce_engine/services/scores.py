from decimal import Decimal

from sqlalchemy.orm import Session

from ai_commerce_engine.models import Product, ScoreSnapshot
from ai_commerce_engine.services.audit import record_audit
from ai_commerce_engine.services.scoring import DEFAULT_WEIGHTS, calculate_score


def save_score(
    session: Session,
    *,
    product_id: int,
    components: dict[str, Decimal],
    penalties: dict[str, Decimal],
    actor: str,
    rationale: str | None = None,
    weights: dict[str, Decimal] | None = None,
) -> ScoreSnapshot:
    if session.get(Product, product_id) is None:
        raise ValueError(f"Product {product_id} does not exist")
    active_weights = weights or DEFAULT_WEIGHTS
    result = calculate_score(components, penalties, active_weights)
    snapshot = ScoreSnapshot(
        product_id=product_id,
        base_score=result.base_score,
        penalty_total=result.penalty_total,
        final_score=result.final_score,
        components={key: float(value) for key, value in components.items()},
        weights={key: float(value) for key, value in active_weights.items()},
        penalties={key: float(value) for key, value in penalties.items()},
        rationale=rationale,
        actor=actor,
    )
    session.add(snapshot)
    session.flush()
    record_audit(
        session,
        event_type="score_change",
        entity_type="score_snapshot",
        entity_id=snapshot.id,
        actor=actor,
        action="create",
        after={"product_id": product_id, "final_score": float(result.final_score)},
    )
    return snapshot

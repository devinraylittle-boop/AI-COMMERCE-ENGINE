from decimal import Decimal

from sqlalchemy.orm import Session

from ai_commerce_engine.models import AppSetting
from ai_commerce_engine.services.audit import record_audit
from ai_commerce_engine.services.scoring import DEFAULT_WEIGHTS

SCORING_WEIGHTS_KEY = "scoring_weights"


def get_scoring_weights(session: Session) -> dict[str, Decimal]:
    setting = session.get(AppSetting, SCORING_WEIGHTS_KEY)
    if setting is None:
        return DEFAULT_WEIGHTS.copy()
    weights = {key: Decimal(str(value)) for key, value in setting.value.items()}
    validate_scoring_weights(weights)
    return weights


def validate_scoring_weights(weights: dict[str, Decimal]) -> None:
    if set(weights) != set(DEFAULT_WEIGHTS):
        raise ValueError("Weights must define every scoring component exactly once")
    if any(value < 0 or value > 1 for value in weights.values()):
        raise ValueError("Each weight must be between 0 and 1")
    if sum(weights.values(), start=Decimal("0")) != Decimal("1.00"):
        raise ValueError("Scoring weights must total 100%")


def save_scoring_weights(session: Session, weights: dict[str, Decimal], actor: str) -> AppSetting:
    validate_scoring_weights(weights)
    setting = session.get(AppSetting, SCORING_WEIGHTS_KEY)
    before = setting.value.copy() if setting else None
    values = {key: float(value) for key, value in weights.items()}
    if setting is None:
        setting = AppSetting(
            key=SCORING_WEIGHTS_KEY,
            value=values,
            description="Active explainable product-scoring weights",
            updated_by=actor,
        )
        session.add(setting)
    else:
        setting.value = values
        setting.updated_by = actor
    record_audit(
        session,
        event_type="assumption_change",
        entity_type="app_setting",
        entity_id=None,
        actor=actor,
        action="update_scoring_weights",
        before=before,
        after=values,
    )
    session.flush()
    return setting

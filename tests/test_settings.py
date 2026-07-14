from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import AuditLog
from ai_commerce_engine.services.scoring import DEFAULT_WEIGHTS
from ai_commerce_engine.services.settings import get_scoring_weights, save_scoring_weights


def test_scoring_weights_are_persisted_and_audited(session: Session) -> None:
    weights = DEFAULT_WEIGHTS.copy()
    weights["unit_economics"] = Decimal("0.25")
    weights["demand_strength"] = Decimal("0.10")
    save_scoring_weights(session, weights, "analyst")
    session.commit()
    assert get_scoring_weights(session) == weights
    audit = session.scalar(select(AuditLog))
    assert audit is not None
    assert audit.event_type == "assumption_change"


def test_scoring_weights_must_total_one(session: Session) -> None:
    weights = DEFAULT_WEIGHTS.copy()
    weights["unit_economics"] = Decimal("0.99")
    with pytest.raises(ValueError, match="100%"):
        save_scoring_weights(session, weights, "analyst")

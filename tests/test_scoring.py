from decimal import Decimal

import pytest

from ai_commerce_engine.services.scoring import DEFAULT_WEIGHTS, calculate_score


def test_score_exposes_weighted_base_and_penalties() -> None:
    components = {name: Decimal("80") for name in DEFAULT_WEIGHTS}
    result = calculate_score(
        components, {"fragility": Decimal("3"), "temporary_novelty": Decimal("2")}
    )
    assert result.base_score == Decimal("80.00")
    assert result.penalty_total == Decimal("5.00")
    assert result.final_score == Decimal("75.00")
    assert sum(result.weighted_components.values()) == Decimal("80.00")


def test_incomplete_components_fail() -> None:
    with pytest.raises(ValueError, match="every component"):
        calculate_score({}, {})

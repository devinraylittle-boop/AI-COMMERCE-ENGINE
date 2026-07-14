from decimal import Decimal

from ai_commerce_engine.services.experiments import derived_experiment_metrics


def test_experiment_metrics() -> None:
    result = derived_experiment_metrics(
        visits=200, purchases=10, cost=Decimal("100"), revenue=Decimal("400"), refunds=Decimal("20")
    )
    assert result["conversion_rate"] == Decimal("5.00")
    assert result["customer_acquisition_cost"] == Decimal("10.00")
    assert result["contribution_profit"] == Decimal("280.00")

from decimal import Decimal

import pytest

from ai_commerce_engine.services.economics import EconomicsInputs, calculate_unit_economics


def test_unit_economics_are_transparent_and_scaled() -> None:
    result = calculate_unit_economics(
        EconomicsInputs(
            selling_price=Decimal("50"),
            discounts=Decimal("5"),
            product_cost=Decimal("10"),
            shipping=Decimal("5"),
            packaging=Decimal("1"),
            payment_processing=Decimal("2"),
            platform_cost=Decimal("1"),
            refund_allowance=Decimal("2"),
            chargeback_allowance=Decimal("1"),
            customer_acquisition_cost=Decimal("10"),
        ),
        volumes=(1, 100),
    )
    assert result.net_revenue == Decimal("45.00")
    assert result.break_even_cac == Decimal("23.00")
    assert result.contribution_margin == Decimal("13.00")
    assert result.contribution_margin_percentage == Decimal("28.89")
    assert result.profit_by_volume[100] == Decimal("1300.00")


def test_negative_inputs_fail() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        EconomicsInputs(selling_price=Decimal("-1"))

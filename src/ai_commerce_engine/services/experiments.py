from decimal import Decimal

from ai_commerce_engine.services.economics import money


def derived_experiment_metrics(
    *, visits: int, purchases: int, cost: Decimal, revenue: Decimal, refunds: Decimal
) -> dict[str, Decimal]:
    if min(visits, purchases) < 0 or min(cost, revenue, refunds) < 0:
        raise ValueError("Experiment metrics cannot be negative")
    conversion_rate = (
        (Decimal(purchases) / Decimal(visits) * 100).quantize(Decimal("0.01"))
        if visits
        else Decimal("0.00")
    )
    cac = money(cost / purchases) if purchases else Decimal("0.00")
    return {
        "conversion_rate": conversion_rate,
        "customer_acquisition_cost": cac,
        "contribution_profit": money(revenue - refunds - cost),
    }

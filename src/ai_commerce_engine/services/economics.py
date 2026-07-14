from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

MONEY = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(MONEY, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class EconomicsInputs:
    selling_price: Decimal
    discounts: Decimal = Decimal("0")
    product_cost: Decimal = Decimal("0")
    shipping: Decimal = Decimal("0")
    packaging: Decimal = Decimal("0")
    payment_processing: Decimal = Decimal("0")
    platform_cost: Decimal = Decimal("0")
    refund_allowance: Decimal = Decimal("0")
    chargeback_allowance: Decimal = Decimal("0")
    customer_acquisition_cost: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if any(value < 0 for value in self.__dict__.values()):
            raise ValueError("Economics inputs cannot be negative")


@dataclass(frozen=True)
class EconomicsResult:
    gross_revenue: Decimal
    net_revenue: Decimal
    variable_cost_before_acquisition: Decimal
    total_variable_cost: Decimal
    contribution_margin: Decimal
    contribution_margin_percentage: Decimal
    break_even_cac: Decimal
    break_even_roas: Decimal | None
    profit_by_volume: dict[int, Decimal]


def calculate_unit_economics(
    inputs: EconomicsInputs, volumes: tuple[int, ...] = (1, 10, 100, 500, 1000)
) -> EconomicsResult:
    if any(volume < 0 for volume in volumes):
        raise ValueError("Order volumes cannot be negative")
    gross_revenue = money(inputs.selling_price)
    net_revenue = money(gross_revenue - inputs.discounts)
    costs_before_cac = money(
        inputs.product_cost
        + inputs.shipping
        + inputs.packaging
        + inputs.payment_processing
        + inputs.platform_cost
        + inputs.refund_allowance
        + inputs.chargeback_allowance
    )
    total_cost = money(costs_before_cac + inputs.customer_acquisition_cost)
    contribution = money(net_revenue - total_cost)
    margin_pct = (
        (contribution / net_revenue * 100).quantize(MONEY, rounding=ROUND_HALF_UP)
        if net_revenue > 0
        else Decimal("0.00")
    )
    break_even_cac = money(max(Decimal("0"), net_revenue - costs_before_cac))
    break_even_roas = (
        (gross_revenue / break_even_cac).quantize(MONEY, rounding=ROUND_HALF_UP)
        if break_even_cac > 0
        else None
    )
    return EconomicsResult(
        gross_revenue=gross_revenue,
        net_revenue=net_revenue,
        variable_cost_before_acquisition=costs_before_cac,
        total_variable_cost=total_cost,
        contribution_margin=contribution,
        contribution_margin_percentage=margin_pct,
        break_even_cac=break_even_cac,
        break_even_roas=break_even_roas,
        profit_by_volume={volume: money(contribution * volume) for volume in volumes},
    )

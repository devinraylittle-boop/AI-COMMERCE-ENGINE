from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

DEFAULT_WEIGHTS: dict[str, Decimal] = {
    "unit_economics": Decimal("0.20"),
    "demand_strength": Decimal("0.15"),
    "demand_growth": Decimal("0.10"),
    "competitive_gap": Decimal("0.10"),
    "creative_advertising_potential": Decimal("0.10"),
    "supplier_fulfillment_quality": Decimal("0.10"),
    "upsell_repeat_purchase": Decimal("0.10"),
    "organic_content_potential": Decimal("0.05"),
    "seasonality_durability": Decimal("0.05"),
    "operational_simplicity": Decimal("0.05"),
}

PENALTY_FIELDS = (
    "trademark_counterfeit_risk",
    "regulatory_risk",
    "unsupported_claims",
    "high_return_likelihood",
    "fragility",
    "unreliable_shipping",
    "weak_supplier_evidence",
    "commodity_saturation",
    "temporary_novelty",
    "poor_contribution_margin",
)


@dataclass(frozen=True)
class ScoreResult:
    base_score: Decimal
    penalty_total: Decimal
    final_score: Decimal
    weighted_components: dict[str, Decimal]


def calculate_score(
    components: dict[str, Decimal],
    penalties: dict[str, Decimal],
    weights: dict[str, Decimal] | None = None,
) -> ScoreResult:
    active_weights = weights or DEFAULT_WEIGHTS
    if set(active_weights) != set(DEFAULT_WEIGHTS):
        raise ValueError("Weights must define every scoring component exactly once")
    if sum(active_weights.values()) != Decimal("1.00"):
        raise ValueError("Scoring weights must total 1.00")
    if set(components) != set(DEFAULT_WEIGHTS):
        raise ValueError("A 0-100 score is required for every component")
    if not set(penalties).issubset(PENALTY_FIELDS):
        raise ValueError("Unknown penalty field")
    if any(value < 0 or value > 100 for value in components.values()):
        raise ValueError("Component scores must be between 0 and 100")
    if any(value < 0 or value > 10 for value in penalties.values()):
        raise ValueError("Each penalty must be between 0 and 10")
    weighted = {name: value * active_weights[name] for name, value in components.items()}
    base = sum(weighted.values(), start=Decimal("0")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    penalty_total = sum(penalties.values(), start=Decimal("0")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    final = max(Decimal("0"), base - penalty_total).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return ScoreResult(base, penalty_total, final, weighted)

from dataclasses import dataclass


@dataclass(frozen=True)
class ThemeDefinition:
    name: str
    definition: str
    inclusion_examples: tuple[str, ...]
    exclusion_examples: tuple[str, ...]
    priority: int
    severity: str | None
    affects: tuple[str, ...]
    positive: bool = False


def _theme(
    name: str,
    definition: str,
    includes: tuple[str, ...],
    excludes: tuple[str, ...] = (),
    *,
    priority: int = 2,
    severity: str | None = None,
    affects: tuple[str, ...] = ("product improvement",),
    positive: bool = False,
) -> ThemeDefinition:
    return ThemeDefinition(
        name, definition, includes, excludes, priority, severity, affects, positive
    )


THEME_TAXONOMY: dict[str, ThemeDefinition] = {
    item.name: item
    for item in (
        _theme(
            "Complaint",
            "Explicit dissatisfaction.",
            ("disappointed", "frustrating", "hate", "terrible", "awful", "problem"),
            severity="medium",
            affects=("customer trust", "product risk"),
        ),
        _theme(
            "Loved feature",
            "Specific praise or delight.",
            ("love", "excellent", "favorite", "perfect", "great"),
            positive=True,
            affects=("positioning",),
        ),
        _theme(
            "Requested improvement",
            "A requested change or missing capability.",
            ("wish", "should include", "would be better", "needs"),
        ),
        _theme(
            "Failure mode",
            "The product stopped working or failed.",
            ("broke", "stopped working", "failed", "defective"),
            priority=1,
            severity="high",
            affects=("product risk", "customer trust"),
        ),
        _theme(
            "Durability",
            "Longevity, wear, or construction life.",
            ("durable", "lasted", "wear", "cracked", "flimsy"),
            severity="medium",
            affects=("product risk", "product improvement"),
        ),
        _theme(
            "Packaging",
            "Package protection or presentation.",
            ("packaging", "box", "packed", "damaged on arrival"),
            affects=("fulfillment", "customer trust"),
        ),
        _theme(
            "Shipping",
            "Delivery speed, damage, or handling.",
            ("shipping", "delivery", "arrived late", "delayed"),
            affects=("fulfillment",),
        ),
        _theme(
            "Misleading claim",
            "A claim or listing differs from experience.",
            ("misleading", "not as described", "false claim", "looks nothing like"),
            priority=1,
            severity="high",
            affects=("customer trust", "product risk"),
        ),
        _theme(
            "Unexpected use",
            "A use outside the advertised primary purpose.",
            ("also use", "unexpectedly useful", "works for my", "repurposed"),
            affects=("positioning",),
        ),
        _theme(
            "Buyer type",
            "Information identifying a user segment.",
            ("for my child", "for seniors", "as a professional", "beginner"),
            affects=("positioning",),
        ),
        _theme(
            "Return reason",
            "A stated return or refund reason.",
            ("returned", "sending it back", "refund"),
            severity="medium",
            affects=("product risk", "customer trust"),
        ),
        _theme(
            "Value perception",
            "Perceived price-to-benefit value.",
            ("worth the money", "overpriced", "good value", "waste of money"),
            affects=("positioning",),
        ),
        _theme(
            "Sizing or fit",
            "Size, dimensions, comfort, or fit.",
            ("too small", "too large", "doesn't fit", "fits perfectly"),
        ),
        _theme(
            "Ease of use",
            "Setup, instructions, or usability.",
            ("easy to use", "easy to install", "confusing", "difficult to use"),
        ),
        _theme(
            "Performance",
            "Functional performance or effectiveness.",
            ("works well", "powerful", "slow", "doesn't work"),
            affects=("product risk", "positioning"),
        ),
        _theme(
            "Quality",
            "Materials, finish, or workmanship.",
            ("high quality", "poor quality", "cheaply made", "well made"),
            affects=("product risk", "positioning"),
        ),
        _theme(
            "Customer service",
            "Support or seller interaction.",
            ("customer service", "support team", "seller responded"),
            affects=("customer trust",),
        ),
        _theme(
            "Safety concern",
            "Potential injury, hazard, or unsafe operation.",
            ("unsafe", "hazard", "burned", "sharp edge", "choking"),
            priority=1,
            severity="critical",
            affects=("product risk", "customer trust"),
        ),
        _theme(
            "Missing accessory",
            "Expected part or accessory absent.",
            ("missing part", "didn't include", "missing accessory"),
            affects=("fulfillment", "product improvement"),
        ),
        _theme(
            "Compatibility",
            "Interoperability with another product or standard.",
            ("compatible", "not compatible", "won't connect", "doesn't work with"),
            affects=("product improvement", "positioning"),
        ),
    )
}


def validate_theme(theme: str) -> None:
    if theme not in THEME_TAXONOMY:
        raise ValueError(f"Unknown review theme: {theme}")

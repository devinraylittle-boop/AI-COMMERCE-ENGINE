import json
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import Product, ReviewImportBatch, ReviewRecord
from ai_commerce_engine.services.review_analytics import calculate_review_analytics
from ai_commerce_engine.services.review_taxonomy import THEME_TAXONOMY


def _report_payload(
    session: Session, *, product_id: int | None = None, batch_id: int | None = None
) -> dict[str, object]:
    analytics = calculate_review_analytics(session, product_id=product_id, batch_id=batch_id)
    if product_id is not None:
        product = session.get(Product, product_id)
        scope = {"type": "product", "id": product_id, "name": product.name if product else None}
        reviews = list(
            session.scalars(select(ReviewRecord).where(ReviewRecord.product_id == product_id))
        )
    else:
        batch = session.get(ReviewImportBatch, batch_id)
        scope = {"type": "batch", "id": batch_id, "name": batch.batch_name if batch else None}
        reviews = list(
            session.scalars(select(ReviewRecord).where(ReviewRecord.import_batch_id == batch_id))
        )
    batches = (
        list(
            session.scalars(
                select(ReviewImportBatch).where(
                    ReviewImportBatch.id.in_({review.import_batch_id for review in reviews})
                )
            )
        )
        if reviews
        else []
    )
    theme_counts = analytics.theme_counts
    positives = {key: value for key, value in theme_counts.items() if THEME_TAXONOMY[key].positive}
    negatives = {key: value for key, value in theme_counts.items() if THEME_TAXONOMY[key].severity}
    requested = {
        key: value
        for key, value in theme_counts.items()
        if key in {"Requested improvement", "Missing accessory", "Compatibility", "Sizing or fit"}
    }
    improvements = [
        f"Investigate {theme.lower()} patterns ({count} reviews in this imported sample)."
        for theme, count in theme_counts.items()
        if "product improvement" in THEME_TAXONOMY[theme].affects
    ]
    positioning = [
        f"Test positioning informed by {theme.lower()} ({count} reviews in this imported sample)."
        for theme, count in theme_counts.items()
        if "positioning" in THEME_TAXONOMY[theme].affects
    ]
    dated = [review.review_date for review in reviews if review.review_date]
    return {
        "title": "Review-mining report",
        "scope": scope,
        "generation_timestamp": datetime.now(UTC).isoformat(),
        "sample_notice": "All percentages describe this imported sample, not market prevalence.",
        "sample_size": analytics.sample_size,
        "sources": analytics.source_distribution,
        "time_range": {
            "earliest": min(dated).isoformat() if dated else None,
            "latest": max(dated).isoformat() if dated else None,
        },
        "data_quality_warnings": analytics.warnings,
        "rating_distribution": analytics.rating_distribution,
        "most_common_positive_themes": positives,
        "most_common_negative_themes": negatives,
        "requested_improvements": requested,
        "failure_modes": {"Failure mode": theme_counts.get("Failure mode", 0)},
        "durability_concerns": {"Durability": theme_counts.get("Durability", 0)},
        "packaging_and_shipping": {
            key: theme_counts.get(key, 0) for key in ("Packaging", "Shipping")
        },
        "misleading_claim_indicators": theme_counts.get("Misleading claim", 0),
        "unexpected_uses": theme_counts.get("Unexpected use", 0),
        "buyer_type_observations": theme_counts.get("Buyer type", 0),
        "return_related_themes": theme_counts.get("Return reason", 0),
        "value_perceptions": theme_counts.get("Value perception", 0),
        "potential_product_improvements": improvements,
        "potential_positioning_opportunities": positioning,
        "critical_unknowns": list(analytics.warnings)
        or ["Representativeness beyond this imported sample is unknown."],
        "further_research": [
            "Add authorized sources.",
            "Review low-confidence assignments.",
            "Validate themes with product-specific evidence.",
        ],
        "theme_counts": analytics.theme_counts,
        "theme_percentages": analytics.theme_percentages,
        "provenance": [
            {
                "batch_id": batch.id,
                "source_platform": batch.source_platform,
                "method": batch.import_method,
                "file_hash": batch.original_file_hash,
                "fictional": batch.is_fictional,
            }
            for batch in batches
        ],
    }


def export_review_report(
    session: Session, *, product_id: int | None = None, batch_id: int | None = None
) -> tuple[str, str]:
    payload = _report_payload(session, product_id=product_id, batch_id=batch_id)
    lines = [
        "# Review-mining report",
        "",
        f"Generated: {payload['generation_timestamp']}",
        f"Scope: {payload['scope']}",
        f"Sample size: {payload['sample_size']}",
        "",
        f"> {payload['sample_notice']}",
        "",
    ]
    for heading, key in (
        ("Data-quality warnings", "data_quality_warnings"),
        ("Sources", "sources"),
        ("Rating distribution", "rating_distribution"),
        ("Positive themes", "most_common_positive_themes"),
        ("Negative themes", "most_common_negative_themes"),
        ("Requested improvements", "requested_improvements"),
        ("Failure modes", "failure_modes"),
        ("Durability concerns", "durability_concerns"),
        ("Packaging and shipping", "packaging_and_shipping"),
        ("Misleading-claim indicators", "misleading_claim_indicators"),
        ("Unexpected uses", "unexpected_uses"),
        ("Buyer-type observations", "buyer_type_observations"),
        ("Return-related themes", "return_related_themes"),
        ("Value perceptions", "value_perceptions"),
        ("Product-improvement opportunities", "potential_product_improvements"),
        ("Positioning opportunities", "potential_positioning_opportunities"),
        ("Critical unknowns", "critical_unknowns"),
        ("Further research", "further_research"),
        ("Provenance", "provenance"),
    ):
        lines.extend((f"## {heading}", "", f"{payload[key]}", ""))
    markdown = "\n".join(lines)
    json_report = json.dumps(
        payload,
        indent=2,
        default=lambda value: str(value) if isinstance(value, Decimal) else value,
    )
    return markdown, json_report

import json
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import Product, ReviewClassificationVersion, ReviewRecord
from ai_commerce_engine.schemas import ReviewInput
from ai_commerce_engine.services.review_analytics import (
    calculate_review_analytics,
    reviews_requiring_attention,
)
from ai_commerce_engine.services.review_classification import (
    DeterministicReviewClassifier,
    correct_classification,
    reclassify_reviews,
    reclassify_scope,
    restore_classification_version,
)
from ai_commerce_engine.services.review_imports import create_manual_review
from ai_commerce_engine.services.review_reports import export_review_report
from ai_commerce_engine.services.review_taxonomy import THEME_TAXONOMY, validate_theme


def setup_product(session: Session) -> Product:
    product = Product(name="Analysis product")
    session.add(product)
    session.flush()
    return product


def add_review(
    session: Session,
    product: Product,
    body: str,
    *,
    rating: str = "2",
    source: str = "Source A",
    fictional: bool = False,
) -> ReviewRecord:
    return create_manual_review(
        session,
        product_id=product.id,
        review=ReviewInput(
            source_platform=source,
            rating=Decimal(rating),
            rating_scale=Decimal("5"),
            original_review_body=body,
            review_date=date(2024, 1, 1),
            provenance_type="Fictional" if fictional else "User-provided",
            is_fictional=fictional,
        ),
        actor="tester",
    )


def test_taxonomy_is_complete_and_validated() -> None:
    assert len(THEME_TAXONOMY) == 20
    assert THEME_TAXONOMY["Safety concern"].severity == "critical"
    validate_theme("Complaint")


def test_classifier_is_explainable_and_negation_aware(session: Session) -> None:
    product = setup_product(session)
    review = add_review(session, product, "The packaging was terrible but it did not break.")
    matches = DeterministicReviewClassifier().classify(review)
    themes = {match.theme for match in matches}
    assert "Packaging" in themes
    assert "Complaint" in themes
    assert "Failure mode" not in themes
    assert all(match.phrase for match in matches)


def test_human_correction_versions_and_reclassification_preserves_it(session: Session) -> None:
    product = setup_product(session)
    review = add_review(session, product, "Great box")
    corrected = correct_classification(
        session,
        review,
        ["Packaging", "Requested improvement"],
        actor="reviewer",
        reason="The box context is a requested improvement",
        note="Needs stronger box",
    )
    assert corrected.version_number == 2
    reclassified = reclassify_reviews(session, [review.id], actor="reviewer")[0]
    assert reclassified.version_number == 3
    assert "Requested improvement" in {item.theme for item in reclassified.assignments}
    restored = restore_classification_version(
        session,
        review,
        1,
        actor="reviewer",
        reason="Restore the initial interpretation as a new version",
    )
    assert restored.version_number == 4
    assert (
        session.scalar(
            select(func.count(ReviewClassificationVersion.id)).where(
                ReviewClassificationVersion.review_id == review.id
            )
        )
        == 4
    )


def test_analytics_distributions_warnings_and_attention(session: Session) -> None:
    product = setup_product(session)
    add_review(session, product, "Unsafe sharp edge and poor quality", fictional=True)
    add_review(session, product, "Love the easy to use design", rating="5", fictional=True)
    analytics = calculate_review_analytics(session, product_id=product.id)
    assert analytics.sample_size == 2
    assert analytics.source_distribution == {"Source A": 2}
    assert analytics.rating_distribution == {"2.00": 1, "5.00": 1}
    assert analytics.theme_counts["Safety concern"] == 1
    assert analytics.theme_percentages["Safety concern"] == Decimal("50.0")
    assert any("Small imported sample" in warning for warning in analytics.warnings)
    assert any("Source concentration" in warning for warning in analytics.warnings)
    assert any("fictional" in warning for warning in analytics.warnings)
    attention = reviews_requiring_attention(session, product.id)
    assert any("Safety concern" in reasons for reasons in attention.values())


def test_markdown_and_json_exports_include_scope_and_provenance(session: Session) -> None:
    product = setup_product(session)
    add_review(session, product, "Love the quality but wish it included a case", rating="5")
    markdown, json_report = export_review_report(session, product_id=product.id)
    payload = json.loads(json_report)
    assert "this imported sample" in markdown
    assert payload["scope"]["id"] == product.id
    assert payload["sample_size"] == 1
    assert payload["provenance"][0]["method"] == "manual"
    assert payload["generation_timestamp"]


def test_batch_scope_reclassification_analytics_and_export(session: Session) -> None:
    product = setup_product(session)
    review = add_review(session, product, "The packaging was damaged on arrival")
    versions = reclassify_scope(session, actor="reviewer", batch_id=review.import_batch_id)
    assert [version.version_number for version in versions] == [2]
    analytics = calculate_review_analytics(session, batch_id=review.import_batch_id)
    assert analytics.sample_size == 1
    markdown, json_report = export_review_report(session, batch_id=review.import_batch_id)
    assert "Failure modes" in markdown
    assert json.loads(json_report)["scope"]["type"] == "batch"

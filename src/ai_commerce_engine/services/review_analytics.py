from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ai_commerce_engine.models import (
    ReviewClassificationVersion,
    ReviewImportBatch,
    ReviewRecord,
)
from ai_commerce_engine.services.review_taxonomy import THEME_TAXONOMY


@dataclass(frozen=True)
class ReviewAnalytics:
    scope: str
    total_imported: int
    accepted_reviews: int
    duplicate_count: int
    rejected_count: int
    classified_count: int
    unclassified_count: int
    source_distribution: dict[str, int]
    rating_distribution: dict[str, int]
    review_date_distribution: dict[str, int]
    verified_purchase_distribution: dict[str, int]
    fictional_distribution: dict[str, int]
    theme_counts: dict[str, int]
    theme_percentages: dict[str, Decimal]
    theme_counts_by_rating: dict[str, dict[str, int]]
    theme_counts_by_source: dict[str, dict[str, int]]
    human_correction_count: int
    classification_version_distribution: dict[str, int]
    average_confidence: Decimal | None
    warnings: tuple[str, ...]

    @property
    def sample_size(self) -> int:
        return self.accepted_reviews


def _reviews_for_scope(
    session: Session, *, product_id: int | None, batch_id: int | None
) -> list[ReviewRecord]:
    if (product_id is None) == (batch_id is None):
        raise ValueError("Choose exactly one product or import batch")
    statement = select(ReviewRecord)
    if product_id is not None:
        statement = statement.where(ReviewRecord.product_id == product_id)
    else:
        statement = statement.where(ReviewRecord.import_batch_id == batch_id)
    return list(session.scalars(statement.order_by(ReviewRecord.id)))


def calculate_review_analytics(
    session: Session, *, product_id: int | None = None, batch_id: int | None = None
) -> ReviewAnalytics:
    reviews = _reviews_for_scope(session, product_id=product_id, batch_id=batch_id)
    review_ids = [review.id for review in reviews]
    batch_ids = {review.import_batch_id for review in reviews}
    batches = (
        list(session.scalars(select(ReviewImportBatch).where(ReviewImportBatch.id.in_(batch_ids))))
        if batch_ids
        else []
    )
    versions = (
        list(
            session.scalars(
                select(ReviewClassificationVersion)
                .options(selectinload(ReviewClassificationVersion.assignments))
                .where(ReviewClassificationVersion.review_id.in_(review_ids))
            )
        )
        if review_ids
        else []
    )
    active = {version.review_id: version for version in versions if version.is_active}
    accepted = len(reviews)
    duplicates = sum(
        review.duplicate_status in {"exact_duplicate", "probable_duplicate", "confirmed_duplicate"}
        for review in reviews
    )
    sources = Counter(review.source_platform for review in reviews)
    ratings = Counter(
        str(review.rating) if review.rating is not None else "Missing" for review in reviews
    )
    dates = Counter(
        review.review_date.strftime("%Y-%m") if review.review_date else "Missing"
        for review in reviews
    )
    verified = Counter(
        "Verified"
        if review.verified_purchase is True
        else "Not verified"
        if review.verified_purchase is False
        else "Unknown"
        for review in reviews
    )
    fictional = Counter(
        "Fictional" if review.is_fictional else "Non-fictional" for review in reviews
    )
    theme_counts: Counter[str] = Counter()
    by_rating: dict[str, Counter[str]] = {}
    by_source: dict[str, Counter[str]] = {}
    confidences: list[Decimal] = []
    review_by_id = {review.id: review for review in reviews}
    for review_id, version in active.items():
        review = review_by_id[review_id]
        rating_key = str(review.rating) if review.rating is not None else "Missing"
        by_rating.setdefault(rating_key, Counter())
        by_source.setdefault(review.source_platform, Counter())
        for assignment in version.assignments:
            theme_counts[assignment.theme] += 1
            by_rating[rating_key][assignment.theme] += 1
            by_source[review.source_platform][assignment.theme] += 1
            confidences.append(Decimal(assignment.confidence))
    percentages = (
        {
            theme: (Decimal(count) * 100 / Decimal(accepted)).quantize(Decimal("0.1"))
            for theme, count in theme_counts.items()
        }
        if accepted
        else {}
    )
    version_distribution = Counter(str(version.version_number) for version in versions)
    corrections = sum(version.classification_method == "human" for version in versions)
    warnings: list[str] = []
    if accepted < 20:
        warnings.append(
            "Small imported sample; patterns may be unstable and are not market prevalence."
        )
    if accepted and sources and max(sources.values()) / accepted > 0.8:
        warnings.append("Source concentration exceeds 80%; findings may reflect one platform.")
    dated = [review.review_date for review in reviews if review.review_date]
    if dated and max(dated) < (datetime.now(UTC).date() - timedelta(days=365)):
        warnings.append("Review-date coverage is stale; newest dated review is over one year old.")
    if accepted and ratings["Missing"] / accepted > 0.25:
        warnings.append("More than 25% of imported reviews have no rating.")
    if accepted and fictional["Fictional"] / accepted > 0.25:
        warnings.append("More than 25% of this sample is fictional demonstration data.")
    if accepted and duplicates / accepted > 0.2:
        warnings.append("Duplicate rate exceeds 20%; inspect duplicate groups before inference.")
    average = sum(confidences, start=Decimal("0")) / len(confidences) if confidences else None
    if average is not None and average < Decimal("0.7"):
        warnings.append("Average deterministic-classification confidence is below 70%.")
    if accepted and len(active) < accepted:
        warnings.append("Some reviews have no active classification.")
    rejected = sum(batch.rejected_count for batch in batches)
    return ReviewAnalytics(
        scope=f"product:{product_id}" if product_id is not None else f"batch:{batch_id}",
        total_imported=accepted + rejected,
        accepted_reviews=accepted,
        duplicate_count=duplicates,
        rejected_count=rejected,
        classified_count=len(active),
        unclassified_count=accepted - len(active),
        source_distribution=dict(sources),
        rating_distribution=dict(ratings),
        review_date_distribution=dict(sorted(dates.items())),
        verified_purchase_distribution=dict(verified),
        fictional_distribution=dict(fictional),
        theme_counts=dict(theme_counts.most_common()),
        theme_percentages=percentages,
        theme_counts_by_rating={key: dict(value) for key, value in by_rating.items()},
        theme_counts_by_source={key: dict(value) for key, value in by_source.items()},
        human_correction_count=corrections,
        classification_version_distribution=dict(version_distribution),
        average_confidence=average.quantize(Decimal("0.001")) if average else None,
        warnings=tuple(warnings),
    )


def reviews_requiring_attention(session: Session, product_id: int) -> dict[int, list[str]]:
    reviews = _reviews_for_scope(session, product_id=product_id, batch_id=None)
    result: dict[int, list[str]] = {}
    for review in reviews:
        reasons: list[str] = []
        version = session.scalar(
            select(ReviewClassificationVersion)
            .options(selectinload(ReviewClassificationVersion.assignments))
            .where(
                ReviewClassificationVersion.review_id == review.id,
                ReviewClassificationVersion.is_active.is_(True),
            )
        )
        assignments = version.assignments if version else []
        themes = {assignment.theme for assignment in assignments}
        if not assignments:
            reasons.append("No detected theme")
        if any(Decimal(assignment.confidence) < Decimal("0.7") for assignment in assignments):
            reasons.append("Low confidence")
        if "Loved feature" in themes and "Complaint" in themes:
            reasons.append("Contradictory themes")
        for theme in ("Safety concern", "Misleading claim"):
            if theme in themes:
                reasons.append(theme)
        if any(
            THEME_TAXONOMY[assignment.theme].severity in {"high", "critical"}
            for assignment in assignments
        ):
            reasons.append("High-severity failure or risk")
        if review.duplicate_status == "probable_duplicate":
            reasons.append("Probable duplicate")
        if review.manually_flagged:
            reasons.append("Manually flagged")
        if reasons:
            result[review.id] = list(dict.fromkeys(reasons))
    return result

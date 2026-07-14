import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from ai_commerce_engine.models import (
    ReviewClassificationVersion,
    ReviewRecord,
    ReviewThemeAssignment,
)
from ai_commerce_engine.services.audit import record_audit
from ai_commerce_engine.services.review_taxonomy import THEME_TAXONOMY, validate_theme

CLASSIFIER_VERSION = "rules-1.0"
NEGATIONS = ("not", "never", "no", "isn't", "wasn't", "doesn't", "didn't")


@dataclass(frozen=True)
class ClassificationMatch:
    theme: str
    confidence: Decimal
    phrase: str
    source: str = "deterministic-rule"


class ReviewClassifier(Protocol):
    version: str

    def classify(self, review: ReviewRecord) -> list[ClassificationMatch]: ...


class DeterministicReviewClassifier:
    version = CLASSIFIER_VERSION

    def classify(self, review: ReviewRecord) -> list[ClassificationMatch]:
        text = review.normalized_review_text
        matches: list[ClassificationMatch] = []
        for definition in sorted(THEME_TAXONOMY.values(), key=lambda item: item.priority):
            for phrase in definition.inclusion_examples:
                match = re.search(rf"\b{re.escape(phrase)}\b", text)
                if not match:
                    continue
                preceding = text[max(0, match.start() - 18) : match.start()].split()
                if preceding and preceding[-1] in NEGATIONS:
                    continue
                confidence = Decimal("0.72")
                if definition.priority == 1:
                    confidence += Decimal("0.08")
                if review.rating is not None:
                    midpoint = (review.rating_scale or Decimal("5")) / 2
                    if definition.positive == (review.rating > midpoint):
                        confidence += Decimal("0.08")
                matches.append(ClassificationMatch(definition.name, confidence, phrase))
                break
        return matches


def active_classification(session: Session, review_id: int) -> ReviewClassificationVersion | None:
    return session.scalar(
        select(ReviewClassificationVersion)
        .options(selectinload(ReviewClassificationVersion.assignments))
        .where(
            ReviewClassificationVersion.review_id == review_id,
            ReviewClassificationVersion.is_active.is_(True),
        )
    )


def create_classification_version(
    session: Session,
    review: ReviewRecord,
    matches: list[ClassificationMatch],
    *,
    method: str,
    classifier_version: str,
    actor: str,
    reason: str,
) -> ReviewClassificationVersion:
    previous = active_classification(session, review.id)
    next_number = (
        session.scalar(
            select(func.max(ReviewClassificationVersion.version_number)).where(
                ReviewClassificationVersion.review_id == review.id
            )
        )
        or 0
    ) + 1
    if previous:
        previous.is_active = False
    version = ReviewClassificationVersion(
        review_id=review.id,
        version_number=next_number,
        classification_method=method,
        classifier_version=classifier_version,
        created_by=actor,
        reason_for_new_version=reason,
        supersedes_version_id=previous.id if previous else None,
        is_active=True,
    )
    session.add(version)
    session.flush()
    for match in matches:
        validate_theme(match.theme)
        session.add(
            ReviewThemeAssignment(
                classification_version_id=version.id,
                theme=match.theme,
                confidence=match.confidence,
                matching_evidence=match.phrase,
                classification_source=match.source,
                human_confirmed_status=("confirmed" if method == "human" else "unreviewed"),
            )
        )
    review.active_classification_version = next_number
    previous_themes = [assignment.theme for assignment in previous.assignments] if previous else []
    new_themes = [match.theme for match in matches]
    record_audit(
        session,
        event_type="data_change",
        entity_type="review_classification",
        entity_id=version.id,
        actor=actor,
        action="create_version",
        before={
            "version": previous.version_number if previous else None,
            "themes": previous_themes,
        },
        after={
            "version": next_number,
            "themes": new_themes,
            "added": sorted(set(new_themes) - set(previous_themes)),
            "removed": sorted(set(previous_themes) - set(new_themes)),
        },
        details=reason,
    )
    return version


def classify_review(
    session: Session,
    review: ReviewRecord,
    *,
    actor: str = "system",
    reason: str = "Deterministic classification",
    classifier: ReviewClassifier | None = None,
) -> ReviewClassificationVersion:
    engine = classifier or DeterministicReviewClassifier()
    matches = engine.classify(review)
    current = active_classification(session, review.id)
    method = "deterministic"
    if current and current.classification_method in {"human", "deterministic+human"}:
        detected = {match.theme for match in matches}
        matches.extend(
            ClassificationMatch(
                assignment.theme,
                Decimal("1"),
                assignment.matching_evidence or "Preserved human correction",
                "human-preserved",
            )
            for assignment in current.assignments
            if assignment.theme not in detected
        )
        method = "deterministic+human"
    return create_classification_version(
        session,
        review,
        matches,
        method=method,
        classifier_version=engine.version,
        actor=actor,
        reason=reason,
    )


def correct_classification(
    session: Session,
    review: ReviewRecord,
    themes: list[str],
    *,
    actor: str,
    reason: str,
    note: str | None = None,
) -> ReviewClassificationVersion:
    if not reason.strip():
        raise ValueError("A correction reason is required")
    matches = [
        ClassificationMatch(theme, Decimal("1"), note or "Human correction", "human")
        for theme in dict.fromkeys(themes)
    ]
    return create_classification_version(
        session,
        review,
        matches,
        method="human",
        classifier_version="human",
        actor=actor,
        reason=reason,
    )


def reclassify_reviews(
    session: Session, review_ids: list[int], *, actor: str
) -> list[ReviewClassificationVersion]:
    reviews = list(session.scalars(select(ReviewRecord).where(ReviewRecord.id.in_(review_ids))))
    return [
        classify_review(session, review, actor=actor, reason="Requested reclassification")
        for review in reviews
    ]


def reclassify_scope(
    session: Session,
    *,
    actor: str,
    review_ids: list[int] | None = None,
    batch_id: int | None = None,
    product_id: int | None = None,
) -> list[ReviewClassificationVersion]:
    selected_scopes = sum(value is not None for value in (review_ids, batch_id, product_id))
    if selected_scopes != 1:
        raise ValueError("Choose exactly one review selection, import batch, or product")
    statement = select(ReviewRecord.id)
    if review_ids is not None:
        statement = statement.where(ReviewRecord.id.in_(review_ids))
    elif batch_id is not None:
        statement = statement.where(ReviewRecord.import_batch_id == batch_id)
    else:
        statement = statement.where(ReviewRecord.product_id == product_id)
    return reclassify_reviews(session, list(session.scalars(statement)), actor=actor)


def restore_classification_version(
    session: Session,
    review: ReviewRecord,
    version_number: int,
    *,
    actor: str,
    reason: str,
) -> ReviewClassificationVersion:
    prior = session.scalar(
        select(ReviewClassificationVersion)
        .options(selectinload(ReviewClassificationVersion.assignments))
        .where(
            ReviewClassificationVersion.review_id == review.id,
            ReviewClassificationVersion.version_number == version_number,
        )
    )
    if prior is None:
        raise ValueError("Classification version does not exist")
    matches = [
        ClassificationMatch(
            assignment.theme,
            Decimal(assignment.confidence),
            assignment.matching_evidence or "Restored interpretation",
            "human-restoration",
        )
        for assignment in prior.assignments
    ]
    return create_classification_version(
        session,
        review,
        matches,
        method="human",
        classifier_version="human-restoration",
        actor=actor,
        reason=reason,
    )

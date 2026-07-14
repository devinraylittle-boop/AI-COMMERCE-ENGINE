import json
from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import AuditLog, Product, ReviewImportBatch, ReviewRecord
from ai_commerce_engine.schemas import ReviewInput
from ai_commerce_engine.services.review_imports import (
    commit_import,
    create_manual_review,
    decide_duplicate,
    detect_duplicate,
    parse_csv,
    parse_json,
    preview_rows,
    set_review_flag,
)


def product(session: Session, name: str = "Review product") -> Product:
    item = Product(name=name)
    session.add(item)
    session.flush()
    return item


def review_input(**overrides: object) -> ReviewInput:
    values: dict[str, object] = {
        "source_platform": "Authorized export",
        "rating": Decimal("2"),
        "rating_scale": Decimal("5"),
        "original_review_body": "The box was damaged and the clasp broke.",
        "review_date": date(2025, 1, 2),
        "provenance_type": "User-provided",
    }
    values.update(overrides)
    return ReviewInput.model_validate(values)


def test_manual_review_preserves_original_and_audits(session: Session) -> None:
    item = product(session)
    body = "  Exact spacing\nAnd CASE stay intact.  "
    review = create_manual_review(
        session,
        product_id=item.id,
        review=review_input(original_review_body=body),
        actor="tester",
    )
    session.flush()
    assert review.original_review_body == body
    assert review.import_batch.record_count_accepted == 1
    assert review.active_classification_version == 1
    assert session.scalar(select(func.count(AuditLog.id))) == 2


def test_csv_preview_mapping_dry_run_and_partial_commit(session: Session) -> None:
    item = product(session)
    content = (
        b"stars,text,when,verified\n"
        b"5,Love the quality,2025-02-01,yes\n"
        b"9,Impossible rating,2025-02-02,no\n"
    )
    rows, digest = parse_csv(content, "reviews.csv")
    preview = preview_rows(
        rows,
        field_mapping={
            "rating": "stars",
            "original_review_body": "text",
            "review_date": "when",
            "verified_purchase": "verified",
        },
        source_platform="CSV source",
        provenance_type="Authorized export",
        is_fictional=False,
        source_hash=digest,
        original_filename="reviews.csv",
    )
    assert preview.valid_count == 1
    assert preview.rejected_count == 1
    assert session.scalar(select(func.count(ReviewImportBatch.id))) == 0
    result = commit_import(
        session,
        product_id=item.id,
        preview=preview,
        batch_name="CSV batch",
        source_type="review",
        source_platform="CSV source",
        import_method="csv",
        actor="tester",
    )
    assert result.batch.import_status == "partial"
    assert result.batch.original_file_hash == digest
    assert result.batch.record_count_submitted == 2
    assert result.batch.record_count_accepted == 1
    assert result.batch.rejected_count == 1
    assert "rating" in result.errors[0].lower()


def test_json_formats_and_invalid_shape() -> None:
    content = json.dumps({"reviews": [{"body": "A"}]}).encode()
    rows, digest = parse_json(content)
    assert rows == [{"body": "A"}]
    assert len(digest) == 64
    with pytest.raises(ValueError, match="list of objects"):
        parse_json(b'{"wrong": []}')


def test_duplicates_external_id_changed_text_and_cross_source_text(session: Session) -> None:
    item = product(session)
    first = create_manual_review(
        session,
        product_id=item.id,
        review=review_input(external_review_id="R-1"),
        actor="tester",
    )
    changed = review_input(external_review_id="R-1", original_review_body="Changed body")
    match = detect_duplicate(session, item.id, changed)
    assert match.status == "exact_duplicate"
    assert match.canonical_id == first.id
    cross_source = review_input(
        external_review_id=None,
        source_platform="Another authorized source",
        original_review_body=first.original_review_body,
    )
    assert detect_duplicate(session, item.id, cross_source).status == "exact_duplicate"


def test_probable_duplicate_is_conservative(session: Session) -> None:
    item = product(session)
    create_manual_review(
        session,
        product_id=item.id,
        review=review_input(original_review_body="The clasp broke after only two uses."),
        actor="tester",
    )
    probable = review_input(original_review_body="The clasp broke after only two uses! ")
    assert detect_duplicate(session, item.id, probable).status == "probable_duplicate"
    legitimate = review_input(original_review_body="The clasp works, but the color faded quickly.")
    assert detect_duplicate(session, item.id, legitimate).status == "unique"
    missing_date = review_input(
        review_date=None,
        original_review_body="The clasp broke after only three uses.",
    )
    assert detect_duplicate(session, item.id, missing_date).status == "unique"


def test_manual_duplicate_override_is_audited(session: Session) -> None:
    item = product(session)
    canonical = create_manual_review(
        session, product_id=item.id, review=review_input(), actor="tester"
    )
    duplicate = create_manual_review(
        session,
        product_id=item.id,
        review=review_input(external_review_id="other"),
        actor="tester",
    )
    decide_duplicate(
        session,
        duplicate.id,
        is_duplicate=False,
        canonical_review_id=None,
        actor="reviewer",
        reason="Independent customer submission",
    )
    assert duplicate.duplicate_status == "not_duplicate"
    decide_duplicate(
        session,
        duplicate.id,
        is_duplicate=True,
        canonical_review_id=canonical.id,
        actor="reviewer",
        reason="Manual confirmation",
    )
    assert duplicate.duplicate_of_review_id == canonical.id
    assert (
        session.scalar(
            select(func.count(AuditLog.id)).where(AuditLog.action == "manual_duplicate_decision")
        )
        == 2
    )


def test_batch_and_original_text_are_immutable(session: Session) -> None:
    item = product(session)
    review = create_manual_review(
        session, product_id=item.id, review=review_input(), actor="tester"
    )
    session.commit()
    review_id = review.id
    review.import_batch.notes = "changed"
    with pytest.raises(ValueError, match="batches are immutable"):
        session.flush()
    session.rollback()
    stored = session.get(ReviewRecord, review_id)
    assert stored is not None
    stored.original_review_body = "replacement"
    with pytest.raises(ValueError, match="text is immutable"):
        session.flush()


def test_fictional_provenance_requires_label() -> None:
    with pytest.raises(ValueError, match="labeled fictional"):
        review_input(provenance_type="Fictional", is_fictional=False)


def test_manual_attention_flag_is_audited(session: Session) -> None:
    item = product(session)
    review = create_manual_review(
        session, product_id=item.id, review=review_input(), actor="tester"
    )
    set_review_flag(
        session,
        review.id,
        flagged=True,
        actor="reviewer",
        reason="Ambiguous safety language",
    )
    assert review.manually_flagged is True
    assert (
        session.scalar(
            select(func.count(AuditLog.id)).where(AuditLog.action == "set_manual_attention_flag")
        )
        == 1
    )

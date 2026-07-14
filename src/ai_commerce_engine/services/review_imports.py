# ruff: noqa: E501
import csv
import hashlib
import io
import json
import unicodedata
from dataclasses import dataclass
from datetime import date
from difflib import SequenceMatcher
from typing import Any

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import Product, ReviewImportBatch, ReviewRecord
from ai_commerce_engine.schemas import ReviewInput
from ai_commerce_engine.services.audit import record_audit
from ai_commerce_engine.services.review_classification import classify_review

CANONICAL_FIELDS = tuple(ReviewInput.model_fields)
PROBABLE_DUPLICATE_THRESHOLD = 0.96


@dataclass(frozen=True)
class RowPreview:
    row_number: int
    raw: dict[str, Any]
    parsed: ReviewInput | None
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ImportPreview:
    rows: tuple[RowPreview, ...]
    source_hash: str | None = None
    original_filename: str | None = None

    @property
    def valid_count(self) -> int:
        return sum(row.parsed is not None for row in self.rows)

    @property
    def rejected_count(self) -> int:
        return len(self.rows) - self.valid_count


@dataclass(frozen=True)
class DuplicateMatch:
    status: str
    canonical_id: int | None = None
    pending_index: int | None = None
    explanation: str = "No duplicate rule matched"


@dataclass(frozen=True)
class ImportResult:
    batch: ReviewImportBatch
    reviews: tuple[ReviewRecord, ...]
    errors: tuple[str, ...]


def normalize_review_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return " ".join(normalized.split())


def review_fingerprint(text: str) -> str:
    return hashlib.sha256(normalize_review_text(text).encode("utf-8")).hexdigest()


def parse_csv(content: bytes, filename: str | None = None) -> tuple[list[dict[str, Any]], str]:
    decoded = content.decode("utf-8-sig")
    rows = [dict(row) for row in csv.DictReader(io.StringIO(decoded))]
    return rows, hashlib.sha256(content).hexdigest()


def parse_json(content: bytes, filename: str | None = None) -> tuple[list[dict[str, Any]], str]:
    payload = json.loads(content.decode("utf-8-sig"))
    if isinstance(payload, dict):
        payload = payload.get("reviews")
    if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
        raise ValueError("JSON must be a list of objects or an object containing a reviews list")
    return [dict(row) for row in payload], hashlib.sha256(content).hexdigest()


def _coerce_bool(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    lowered = value.strip().lower()
    if lowered in {"true", "yes", "1", "y"}:
        return True
    if lowered in {"false", "no", "0", "n"}:
        return False
    if lowered in {"", "unknown", "none", "null"}:
        return None
    return value


def preview_rows(
    rows: list[dict[str, Any]],
    *,
    field_mapping: dict[str, str],
    source_platform: str,
    provenance_type: str,
    is_fictional: bool,
    source_hash: str | None = None,
    original_filename: str | None = None,
) -> ImportPreview:
    previews: list[RowPreview] = []
    for number, raw in enumerate(rows, start=1):
        mapped = {
            canonical: raw.get(input_name)
            for canonical, input_name in field_mapping.items()
            if canonical in CANONICAL_FIELDS and input_name
        }
        mapped.setdefault("source_platform", source_platform)
        mapped.setdefault("provenance_type", provenance_type)
        mapped.setdefault("is_fictional", is_fictional)
        for key in ("verified_purchase", "is_fictional"):
            if key in mapped:
                mapped[key] = _coerce_bool(mapped[key])
        for key in tuple(mapped):
            if mapped[key] == "" and key != "original_review_body":
                mapped[key] = None
        try:
            parsed = ReviewInput.model_validate(mapped)
            previews.append(RowPreview(number, raw, parsed))
        except ValidationError as exc:
            errors = tuple(
                f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
                for error in exc.errors()
            )
            previews.append(RowPreview(number, raw, None, errors))
    return ImportPreview(tuple(previews), source_hash, original_filename)


def _similar(left: ReviewInput, right: ReviewInput) -> bool:
    if not (
        left.source_platform == right.source_platform
        and left.rating == right.rating
        and left.review_date is not None
        and left.review_date == right.review_date
    ):
        return False
    score = SequenceMatcher(
        None,
        normalize_review_text(left.original_review_body),
        normalize_review_text(right.original_review_body),
        autojunk=False,
    ).ratio()
    return score >= PROBABLE_DUPLICATE_THRESHOLD


def detect_duplicate(
    session: Session,
    product_id: int,
    review: ReviewInput,
    pending: list[ReviewInput] | None = None,
) -> DuplicateMatch:
    existing = list(
        session.scalars(select(ReviewRecord).where(ReviewRecord.product_id == product_id))
    )
    if review.external_review_id:
        for existing_review in existing:
            if (
                existing_review.source_platform == review.source_platform
                and existing_review.external_review_id == review.external_review_id
            ):
                return DuplicateMatch(
                    "exact_duplicate",
                    existing_review.id,
                    explanation="Same source and external review ID",
                )
    fingerprint = review_fingerprint(review.original_review_body)
    for existing_review in existing:
        if existing_review.normalized_fingerprint == fingerprint:
            return DuplicateMatch(
                "exact_duplicate",
                existing_review.id,
                explanation="Exact normalized-text fingerprint",
            )
    for existing_review in existing:
        comparable = ReviewInput(
            external_review_id=existing_review.external_review_id,
            source_platform=existing_review.source_platform,
            source_url=existing_review.source_url,
            rating=existing_review.rating,
            rating_scale=existing_review.rating_scale,
            original_review_body=existing_review.original_review_body,
            review_date=existing_review.review_date,
            provenance_type=existing_review.provenance_type,
            is_fictional=existing_review.is_fictional,
        )
        if _similar(review, comparable):
            return DuplicateMatch(
                "probable_duplicate",
                existing_review.id,
                explanation="Same product, source, rating, and date with >=96% text similarity",
            )
    for index, pending_review in enumerate(pending or []):
        if review.external_review_id and (
            pending_review.source_platform == review.source_platform
            and pending_review.external_review_id == review.external_review_id
        ):
            return DuplicateMatch(
                "exact_duplicate",
                pending_index=index,
                explanation="Same source and external review ID in this import",
            )
        if review_fingerprint(pending_review.original_review_body) == fingerprint:
            return DuplicateMatch(
                "exact_duplicate",
                pending_index=index,
                explanation="Exact normalized-text fingerprint in this import",
            )
        if _similar(review, pending_review):
            return DuplicateMatch(
                "probable_duplicate",
                pending_index=index,
                explanation="Same source, rating, and date with >=96% text similarity in this import",
            )
    return DuplicateMatch("unique")


def commit_import(
    session: Session,
    *,
    product_id: int,
    preview: ImportPreview,
    batch_name: str,
    source_type: str,
    source_platform: str,
    import_method: str,
    actor: str,
    notes: str | None = None,
    is_fictional: bool = False,
) -> ImportResult:
    if session.get(Product, product_id) is None:
        raise ValueError("Product does not exist")
    valid = [row.parsed for row in preview.rows if row.parsed is not None]
    decisions: list[DuplicateMatch] = []
    pending: list[ReviewInput] = []
    for parsed_review in valid:
        decisions.append(detect_duplicate(session, product_id, parsed_review, pending))
        pending.append(parsed_review)
    duplicate_count = sum(decision.status != "unique" for decision in decisions)
    errors = tuple(
        f"Row {row.row_number}: {'; '.join(row.errors)}" for row in preview.rows if row.errors
    )
    batch = ReviewImportBatch(
        batch_name=batch_name,
        source_type=source_type,
        source_platform=source_platform,
        import_method=import_method,
        original_filename=preview.original_filename,
        original_file_hash=preview.source_hash,
        product_id=product_id,
        created_by=actor,
        record_count_submitted=len(preview.rows),
        record_count_accepted=len(valid),
        duplicate_count=duplicate_count,
        rejected_count=preview.rejected_count,
        error_count=len(errors),
        import_status=("partial" if errors and valid else "completed" if valid else "rejected"),
        notes=notes,
        is_fictional=is_fictional,
        metadata_snapshot={
            "source_type": source_type,
            "source_platform": source_platform,
            "import_method": import_method,
            "field_names": list(CANONICAL_FIELDS),
            "original_filename": preview.original_filename,
            "source_hash": preview.source_hash,
        },
    )
    session.add(batch)
    session.flush()
    created: list[ReviewRecord] = []
    for item, duplicate in zip(valid, decisions, strict=True):
        canonical_id = duplicate.canonical_id
        if duplicate.pending_index is not None:
            canonical_id = created[duplicate.pending_index].id
        record = ReviewRecord(
            product_id=product_id,
            import_batch_id=batch.id,
            external_review_id=item.external_review_id,
            source_platform=item.source_platform,
            source_url=str(item.source_url) if item.source_url else None,
            reviewer_display_name=item.reviewer_display_name,
            rating=item.rating,
            rating_scale=item.rating_scale,
            review_title=item.review_title,
            original_review_body=item.original_review_body,
            normalized_review_text=normalize_review_text(item.original_review_body),
            review_date=item.review_date,
            verified_purchase=item.verified_purchase,
            helpful_vote_count=item.helpful_vote_count,
            geography=item.geography,
            language=item.language,
            variant_sku=item.variant_sku,
            provenance_type=item.provenance_type,
            is_fictional=item.is_fictional,
            normalized_fingerprint=review_fingerprint(item.original_review_body),
            duplicate_status=duplicate.status,
            duplicate_of_review_id=canonical_id,
        )
        session.add(record)
        session.flush()
        classify_review(session, record)
        created.append(record)
    record_audit(
        session,
        event_type="import",
        entity_type="review_import_batch",
        entity_id=batch.id,
        actor=actor,
        action="commit",
        after={
            "submitted": len(preview.rows),
            "accepted": len(valid),
            "duplicates": duplicate_count,
            "rejected": preview.rejected_count,
        },
        details="Immutable review import batch committed",
    )
    return ImportResult(batch, tuple(created), errors)


def create_manual_review(
    session: Session,
    *,
    product_id: int,
    review: ReviewInput,
    actor: str,
) -> ReviewRecord:
    preview = ImportPreview((RowPreview(1, review.model_dump(mode="json"), review),))
    result = commit_import(
        session,
        product_id=product_id,
        preview=preview,
        batch_name=f"Manual entry {date.today().isoformat()}",
        source_type="review",
        source_platform=review.source_platform,
        import_method="manual",
        actor=actor,
        is_fictional=review.is_fictional,
    )
    return result.reviews[0]


def decide_duplicate(
    session: Session,
    review_id: int,
    *,
    is_duplicate: bool,
    canonical_review_id: int | None,
    actor: str,
    reason: str,
) -> ReviewRecord:
    review = session.get(ReviewRecord, review_id)
    if review is None:
        raise ValueError("Review does not exist")
    if not reason.strip():
        raise ValueError("A duplicate-decision reason is required")
    if is_duplicate:
        canonical = session.get(ReviewRecord, canonical_review_id)
        if (
            canonical is None
            or canonical.id == review.id
            or canonical.product_id != review.product_id
        ):
            raise ValueError("A different canonical review for the same product is required")
    before = {"status": review.duplicate_status, "duplicate_of": review.duplicate_of_review_id}
    review.duplicate_status = "confirmed_duplicate" if is_duplicate else "not_duplicate"
    review.duplicate_of_review_id = canonical_review_id if is_duplicate else None
    record_audit(
        session,
        event_type="data_change",
        entity_type="review_duplicate",
        entity_id=review.id,
        actor=actor,
        action="manual_duplicate_decision",
        before=before,
        after={"status": review.duplicate_status, "duplicate_of": review.duplicate_of_review_id},
        details=reason,
    )
    return review


def set_review_flag(
    session: Session,
    review_id: int,
    *,
    flagged: bool,
    actor: str,
    reason: str,
) -> ReviewRecord:
    review = session.get(ReviewRecord, review_id)
    if review is None:
        raise ValueError("Review does not exist")
    if not reason.strip():
        raise ValueError("A flag reason is required")
    before = review.manually_flagged
    review.manually_flagged = flagged
    record_audit(
        session,
        event_type="data_change",
        entity_type="review_record",
        entity_id=review.id,
        actor=actor,
        action="set_manual_attention_flag",
        before={"manually_flagged": before},
        after={"manually_flagged": flagged},
        details=reason,
    )
    return review

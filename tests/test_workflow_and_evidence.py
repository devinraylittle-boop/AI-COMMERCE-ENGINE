from datetime import UTC, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import AuditLog, StatusHistory
from ai_commerce_engine.repositories.products import append_evidence, create_product
from ai_commerce_engine.schemas import EvidenceCreate, ProductCreate, StatusChange
from ai_commerce_engine.services.workflow import change_status


def test_status_change_records_history_and_audit(session: Session) -> None:
    product = create_product(session, ProductCreate(name="Test product"))
    history = change_status(
        session,
        StatusChange(
            product_id=product.id,
            new_status="Initial review",
            reason="Enough initial context",
            actor="analyst",
            next_action="Collect demand evidence",
        ),
    )
    session.commit()
    assert history.previous_status == "Discovered"
    assert session.scalar(select(StatusHistory)).new_status == "Initial review"  # type: ignore[union-attr]
    assert len(list(session.scalars(select(AuditLog)))) == 2


def test_evidence_is_appended_with_provenance(session: Session) -> None:
    product = create_product(session, ProductCreate(name="Test product"))
    evidence = append_evidence(
        session,
        EvidenceCreate(
            product_id=product.id,
            evidence_type="Review",
            source="User export",
            observation="Three complaints about sizing",
            numeric_value=3,
            unit="reviews",
            collected_at=datetime.now(UTC),
            collection_method="CSV export",
            confidence_level="High",
            provenance="Observed",
        ),
    )
    session.commit()
    assert evidence.provenance == "Observed"
    assert evidence.source == "User export"


def test_duplicate_status_is_rejected(session: Session) -> None:
    product = create_product(session, ProductCreate(name="Test product"))
    with pytest.raises(ValueError, match="differ"):
        change_status(
            session,
            StatusChange(
                product_id=product.id,
                new_status="Discovered",
                reason="No actual movement",
                actor="analyst",
            ),
        )

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from ai_commerce_engine.repositories.products import append_evidence, create_product
from ai_commerce_engine.schemas import EvidenceCreate, ProductCreate
from ai_commerce_engine.services.research import (
    RESEARCH_SECTIONS,
    assess_research,
    export_research_report,
    save_research_entry,
)


def test_research_reports_missing_unsupported_stale_and_contradictory_data(
    session: Session,
) -> None:
    product = create_product(session, ProductCreate(name="Research candidate"))
    old = datetime.now(UTC) - timedelta(days=365)
    first = append_evidence(
        session,
        EvidenceCreate(
            product_id=product.id,
            evidence_type="Search interest",
            source="Export A",
            observation="First observed index",
            numeric_value=Decimal("10"),
            unit="index",
            collected_at=old,
            collection_method="CSV import",
            confidence_level="Medium",
            provenance="Observed",
        ),
    )
    append_evidence(
        session,
        EvidenceCreate(
            product_id=product.id,
            evidence_type="Search interest",
            source="Export B",
            observation="Second observed index",
            numeric_value=Decimal("30"),
            unit="index",
            collected_at=datetime.now(UTC),
            collection_method="CSV import",
            confidence_level="Medium",
            provenance="Observed",
        ),
    )
    save_research_entry(
        session,
        product_id=product.id,
        section_key="search_interest",
        content="The two sources disagree materially.",
        evidence_ids=[first.id],
        provenance="Inferred",
        actor="founder",
        reason="Initial search review",
    )
    save_research_entry(
        session,
        product_id=product.id,
        section_key="customer_definition",
        content="A tentative customer definition without direct evidence.",
        evidence_ids=[],
        provenance="Estimated",
        actor="founder",
        reason="Document current assumption",
    )
    assessment = assess_research(session, product.id)

    assert assessment.completed_sections == 2
    assert not assessment.enough_evidence
    assert first.id in assessment.stale_evidence_ids
    assert assessment.contradictory_evidence_groups == ["Search interest (index)"]
    assert "Customer definition" in assessment.unsupported_sections
    assert "supplier_fulfillment_quality" in assessment.unsupported_score_components


def test_research_export_contains_every_section_and_evidence_ids(session: Session) -> None:
    product = create_product(session, ProductCreate(name="Export candidate"))
    markdown, json_report = export_research_report(session, product.id)
    assert "Not enough evidence" in markdown
    assert len([label for label in RESEARCH_SECTIONS.values() if label in markdown]) == len(
        RESEARCH_SECTIONS
    )
    assert '"research"' in json_report
    assert '"latest_score": null' in json_report

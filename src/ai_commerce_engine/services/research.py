import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import Evidence, Product, ResearchEntry, ScoreSnapshot
from ai_commerce_engine.services.audit import record_audit

RESEARCH_SECTIONS: dict[str, str] = {
    "customer_definition": "Customer definition",
    "problem_or_desire": "Problem or desire",
    "existing_alternatives": "Existing alternatives",
    "competitor_comparison": "Competitor comparison",
    "pricing_range": "Pricing range",
    "review_analysis": "Review analysis",
    "search_interest": "Search-interest evidence",
    "social_interest": "Social-interest evidence",
    "marketplace_evidence": "Marketplace evidence",
    "supplier_options": "Supplier options",
    "shipping_fulfillment": "Shipping and fulfillment",
    "return_failure_risks": "Return and failure risks",
    "regulatory_policy_risks": "Regulatory, trademark, and policy risks",
    "unit_economics": "Unit economics",
    "upsell_bundles": "Upsell and bundle opportunities",
    "repeat_purchase": "Repeat-purchase potential",
    "organic_content": "Organic content potential",
    "paid_advertising": "Paid advertising potential",
    "reasons_to_pursue": "Reasons to pursue",
    "reasons_to_reject": "Reasons to reject",
    "missing_evidence": "Missing evidence",
    "cheapest_next_test": "Cheapest next validation test",
}

CRITICAL_SECTIONS = {
    "customer_definition",
    "problem_or_desire",
    "marketplace_evidence",
    "supplier_options",
    "regulatory_policy_risks",
    "unit_economics",
    "missing_evidence",
    "cheapest_next_test",
}

SCORE_SECTION_MAP: dict[str, set[str]] = {
    "unit_economics": {"unit_economics", "pricing_range"},
    "demand_strength": {"search_interest", "social_interest", "marketplace_evidence"},
    "demand_growth": {"search_interest", "social_interest"},
    "competitive_gap": {"existing_alternatives", "competitor_comparison", "review_analysis"},
    "creative_advertising_potential": {"organic_content", "paid_advertising"},
    "supplier_fulfillment_quality": {"supplier_options", "shipping_fulfillment"},
    "upsell_repeat_purchase": {"upsell_bundles", "repeat_purchase"},
    "organic_content_potential": {"organic_content"},
    "seasonality_durability": {"search_interest", "marketplace_evidence"},
    "operational_simplicity": {"shipping_fulfillment", "return_failure_risks"},
}


@dataclass(frozen=True)
class ResearchAssessment:
    completeness_percentage: Decimal
    completed_sections: int
    total_sections: int
    missing_sections: list[str]
    missing_critical_sections: list[str]
    unsupported_sections: list[str]
    stale_evidence_ids: list[int]
    contradictory_evidence_groups: list[str]
    unsupported_score_components: list[str]
    enough_evidence: bool


def latest_research_entries(session: Session, product_id: int) -> dict[str, ResearchEntry]:
    entries = list(
        session.scalars(
            select(ResearchEntry)
            .where(ResearchEntry.product_id == product_id)
            .order_by(ResearchEntry.section_key, ResearchEntry.version_number.desc())
        )
    )
    latest: dict[str, ResearchEntry] = {}
    for entry in entries:
        latest.setdefault(entry.section_key, entry)
    return latest


def save_research_entry(
    session: Session,
    *,
    product_id: int,
    section_key: str,
    content: str,
    evidence_ids: list[int],
    provenance: str,
    actor: str,
    reason: str,
) -> ResearchEntry:
    if session.get(Product, product_id) is None:
        raise ValueError(f"Product {product_id} does not exist")
    if section_key not in RESEARCH_SECTIONS:
        raise ValueError(f"Unknown research section: {section_key}")
    if len(content.strip()) < 3:
        raise ValueError("Research content must contain at least three characters")
    if len(reason.strip()) < 3:
        raise ValueError("A reason for the research update is required")
    unique_evidence = sorted(set(evidence_ids))
    for evidence_id in unique_evidence:
        evidence = session.get(Evidence, evidence_id)
        if evidence is None or evidence.product_id != product_id:
            raise ValueError(f"Evidence {evidence_id} is not attached to this product")
    previous_version = session.scalar(
        select(func.max(ResearchEntry.version_number)).where(
            ResearchEntry.product_id == product_id,
            ResearchEntry.section_key == section_key,
        )
    )
    entry = ResearchEntry(
        product_id=product_id,
        section_key=section_key,
        version_number=(previous_version or 0) + 1,
        content=content.strip(),
        evidence_ids=unique_evidence,
        provenance=provenance,
        actor=actor,
        reason=reason,
    )
    session.add(entry)
    session.flush()
    record_audit(
        session,
        event_type="data_change",
        entity_type="research_entry",
        entity_id=entry.id,
        actor=actor,
        action="append_version",
        after={
            "section": section_key,
            "version": entry.version_number,
            "evidence_ids": unique_evidence,
            "provenance": provenance,
        },
        details=reason,
    )
    return entry


def assess_research(
    session: Session, product_id: int, *, stale_after_days: int = 180
) -> ResearchAssessment:
    latest = latest_research_entries(session, product_id)
    completed = {key for key, value in latest.items() if value.content.strip()}
    missing_keys = set(RESEARCH_SECTIONS) - completed
    unsupported = sorted(
        RESEARCH_SECTIONS[key]
        for key, value in latest.items()
        if value.content.strip() and not value.evidence_ids
    )
    evidence = list(session.scalars(select(Evidence).where(Evidence.product_id == product_id)))
    cutoff = datetime.now(UTC) - timedelta(days=stale_after_days)
    stale_ids = sorted(item.id for item in evidence if _aware(item.collected_at) < cutoff)
    contradictions = _contradictory_groups(evidence)
    unsupported_scores = sorted(
        component
        for component, required_sections in SCORE_SECTION_MAP.items()
        if not any(key in latest and latest[key].evidence_ids for key in required_sections)
    )
    percentage = (Decimal(len(completed)) / Decimal(len(RESEARCH_SECTIONS)) * 100).quantize(
        Decimal("0.01")
    )
    missing_critical = sorted(CRITICAL_SECTIONS - completed)
    enough = percentage >= Decimal("75") and not missing_critical and bool(evidence)
    return ResearchAssessment(
        completeness_percentage=percentage,
        completed_sections=len(completed),
        total_sections=len(RESEARCH_SECTIONS),
        missing_sections=[RESEARCH_SECTIONS[key] for key in sorted(missing_keys)],
        missing_critical_sections=[RESEARCH_SECTIONS[key] for key in missing_critical],
        unsupported_sections=unsupported,
        stale_evidence_ids=stale_ids,
        contradictory_evidence_groups=contradictions,
        unsupported_score_components=unsupported_scores,
        enough_evidence=enough,
    )


def _aware(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def _contradictory_groups(evidence: list[Evidence]) -> list[str]:
    grouped: dict[tuple[str, str | None], list[Decimal]] = {}
    explicit: set[str] = set()
    for item in evidence:
        if item.notes and "contradict" in item.notes.lower():
            explicit.add(item.evidence_type)
        if item.numeric_value is not None:
            grouped.setdefault((item.evidence_type, item.unit), []).append(item.numeric_value)
    for (evidence_type, unit), values in grouped.items():
        positive = [value for value in values if value > 0]
        if len(positive) >= 2 and max(positive) / min(positive) >= 2:
            explicit.add(f"{evidence_type} ({unit or 'no unit'})")
    return sorted(explicit)


def export_research_report(session: Session, product_id: int) -> tuple[str, str]:
    product = session.get(Product, product_id)
    if product is None:
        raise ValueError(f"Product {product_id} does not exist")
    latest = latest_research_entries(session, product_id)
    assessment = assess_research(session, product_id)
    evidence = list(session.scalars(select(Evidence).where(Evidence.product_id == product_id)))
    latest_score = session.scalar(
        select(ScoreSnapshot)
        .where(ScoreSnapshot.product_id == product_id)
        .order_by(ScoreSnapshot.created_at.desc())
    )
    payload = {
        "product": {"id": product.id, "name": product.name, "status": product.status},
        "assessment": {
            **asdict(assessment),
            "completeness_percentage": str(assessment.completeness_percentage),
        },
        "research": {
            key: {
                "label": RESEARCH_SECTIONS[key],
                "content": latest[key].content if key in latest else None,
                "evidence_ids": latest[key].evidence_ids if key in latest else [],
                "provenance": latest[key].provenance if key in latest else None,
                "version": latest[key].version_number if key in latest else None,
            }
            for key in RESEARCH_SECTIONS
        },
        "evidence": [
            {
                "id": item.id,
                "type": item.evidence_type,
                "source": item.source,
                "observation": item.observation,
                "confidence": item.confidence_level,
                "provenance": item.provenance,
                "collected_at": item.collected_at.isoformat(),
            }
            for item in evidence
        ],
        "latest_score": float(latest_score.final_score) if latest_score else None,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    json_report = json.dumps(payload, indent=2)
    evidence_state = (
        "Sufficient for recommendation review"
        if assessment.enough_evidence
        else "Not enough evidence"
    )
    lines = [
        f"# Product Research Report: {product.name}",
        "",
        f"Status: {product.status}",
        f"Evidence completeness: {assessment.completeness_percentage}%",
        f"Evidence state: {evidence_state}",
        "",
    ]
    for key, label in RESEARCH_SECTIONS.items():
        entry = latest.get(key)
        evidence_ids = (
            ", ".join(map(str, entry.evidence_ids)) if entry and entry.evidence_ids else "None"
        )
        lines.extend(
            [
                f"## {label}",
                "",
                entry.content if entry else "Not researched.",
                "",
                f"Evidence IDs: {evidence_ids}",
                "",
            ]
        )
    return "\n".join(lines), json_report

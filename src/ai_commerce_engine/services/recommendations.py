import json
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import Evidence, Product, ScoreSnapshot
from ai_commerce_engine.services.economics import EconomicsInputs, calculate_unit_economics, money
from ai_commerce_engine.services.research import (
    ResearchAssessment,
    assess_research,
    latest_research_entries,
)

MAX_PHASE_ONE_TEST_BUDGET = Decimal("500.00")


@dataclass(frozen=True)
class RecommendationBrief:
    product_id: int
    product_name: str
    recommendation: str
    confidence_level: str
    evidence_completeness: Decimal
    primary_reasons_in_favor: list[str]
    primary_reasons_against: list[str]
    critical_unknowns: list[str]
    evidence_citations: list[str]
    unit_economics_summary: str
    break_even_cac: Decimal
    break_even_roas: Decimal | None
    fulfillment_concerns: list[str]
    customer_trust_concerns: list[str]
    regulatory_policy_concerns: list[str]
    suggested_next_experiment: str
    maximum_validation_budget: Decimal
    reversal_conditions: list[str]
    certainty_notice: str


class RecommendationGenerator(Protocol):
    def generate(self, session: Session, product_id: int) -> RecommendationBrief: ...


class DeterministicRecommendationGenerator:
    """Template-driven recommendation generator with no external model dependency."""

    def generate(self, session: Session, product_id: int) -> RecommendationBrief:
        product = session.get(Product, product_id)
        if product is None:
            raise ValueError(f"Product {product_id} does not exist")
        assessment = assess_research(session, product_id)
        latest = latest_research_entries(session, product_id)
        evidence = list(session.scalars(select(Evidence).where(Evidence.product_id == product_id)))
        latest_score = session.scalar(
            select(ScoreSnapshot)
            .where(ScoreSnapshot.product_id == product_id)
            .order_by(ScoreSnapshot.created_at.desc())
        )
        economics = calculate_unit_economics(
            EconomicsInputs(
                selling_price=_decimal(product.proposed_selling_price),
                discounts=_decimal(product.discount_estimate),
                product_cost=_decimal(product.product_cost),
                shipping=_decimal(product.shipping_cost),
                packaging=_decimal(product.packaging_cost),
                payment_processing=_decimal(product.payment_processing_estimate),
                platform_cost=_decimal(product.platform_cost_allocation),
                refund_allowance=_decimal(product.expected_refund_allowance),
                chargeback_allowance=_decimal(product.chargeback_allowance),
                customer_acquisition_cost=_decimal(product.estimated_cac),
            )
        )
        recommendation = _recommend(
            product, assessment, latest_score, economics.contribution_margin
        )
        favor, against = _reasons(product, assessment, latest_score, economics.contribution_margin)
        citations = [
            f"Evidence #{item.id}: {item.evidence_type} — {item.source} "
            f"({item.confidence_level}, {item.provenance})"
            for item in evidence
        ]
        next_test = latest.get("cheapest_next_test")
        budget = (
            money(min(MAX_PHASE_ONE_TEST_BUDGET, economics.break_even_cac * 10))
            if assessment.enough_evidence and economics.break_even_cac > 0
            else Decimal("0.00")
        )
        return RecommendationBrief(
            product_id=product.id,
            product_name=product.name,
            recommendation=recommendation,
            confidence_level=_confidence(assessment, evidence),
            evidence_completeness=assessment.completeness_percentage,
            primary_reasons_in_favor=favor,
            primary_reasons_against=against,
            critical_unknowns=assessment.missing_critical_sections
            + [
                f"Unsupported score component: {name}"
                for name in assessment.unsupported_score_components
            ],
            evidence_citations=citations,
            unit_economics_summary=(
                f"Contribution margin {economics.contribution_margin} "
                f"({economics.contribution_margin_percentage}%) after estimated CAC."
            ),
            break_even_cac=economics.break_even_cac,
            break_even_roas=economics.break_even_roas,
            fulfillment_concerns=[product.fulfillment_risk]
            if product.fulfillment_risk
            else ["Fulfillment risk has not been explicitly documented."],
            customer_trust_concerns=[product.review_complaints]
            if product.review_complaints
            else ["Review complaints and customer-trust failure modes remain incomplete."],
            regulatory_policy_concerns=[product.legal_policy_concerns]
            if product.legal_policy_concerns
            else ["No concern recorded; this is not proof that regulatory risk is absent."],
            suggested_next_experiment=(
                next_test.content
                if next_test
                else "Complete the Cheapest next validation test research section before spending."
            ),
            maximum_validation_budget=budget,
            reversal_conditions=_reversal_conditions(recommendation, economics.break_even_cac),
            certainty_notice=(
                "This deterministic brief is a decision aid, not a certain prediction "
                "or authorization "
                "to spend, publish, order, contact a supplier, or launch."
            ),
        )


def _decimal(value: Decimal | str | int | float) -> Decimal:
    return Decimal(str(value))


def _recommend(
    product: Product,
    assessment: ResearchAssessment,
    score: ScoreSnapshot | None,
    contribution_margin: Decimal,
) -> str:
    if assessment.enough_evidence and contribution_margin <= 0:
        return "reject"
    if not assessment.enough_evidence:
        return "investigate"
    if score is None or len(assessment.unsupported_score_components) > 3:
        return "hold"
    if score.final_score < 40:
        return "reject"
    if (
        score.final_score >= 75
        and product.status in {"Validation passed", "Store candidate"}
        and contribution_margin > 0
    ):
        return "launch candidate"
    if score.final_score >= 60 and contribution_margin > 0:
        return "validate"
    return "hold"


def _confidence(assessment: ResearchAssessment, evidence: list[Evidence]) -> str:
    high_confidence = sum(item.confidence_level == "High" for item in evidence)
    if assessment.enough_evidence and evidence and high_confidence / len(evidence) >= 0.6:
        return "High"
    if assessment.completeness_percentage >= 50 and evidence:
        return "Medium"
    return "Low"


def _reasons(
    product: Product,
    assessment: ResearchAssessment,
    score: ScoreSnapshot | None,
    contribution_margin: Decimal,
) -> tuple[list[str], list[str]]:
    favor: list[str] = []
    against: list[str] = []
    if contribution_margin > 0:
        favor.append(f"Estimated contribution margin is positive at {contribution_margin}.")
    else:
        against.append(f"Estimated contribution margin is not positive ({contribution_margin}).")
    if score is not None:
        target = favor if score.final_score >= 60 else against
        target.append(
            f"Latest explainable score is {score.final_score}/100 (snapshot #{score.id})."
        )
    else:
        against.append("No score snapshot exists.")
    if assessment.enough_evidence:
        favor.append(f"Research completeness is {assessment.completeness_percentage}%.")
    else:
        against.append(
            f"Evidence is insufficient at {assessment.completeness_percentage}% completeness."
        )
    if assessment.contradictory_evidence_groups:
        against.append(
            "Contradictory evidence requires review: "
            + ", ".join(assessment.contradictory_evidence_groups)
        )
    if product.fulfillment_risk:
        against.append(f"Recorded fulfillment concern: {product.fulfillment_risk}")
    return favor or ["No evidence-backed reason in favor is currently available."], against


def _reversal_conditions(recommendation: str, break_even_cac: Decimal) -> list[str]:
    conditions = [
        f"Observed acquisition cost exceeds break-even CAC of {break_even_cac}.",
        "New evidence materially contradicts the customer problem or demand thesis.",
        "Supplier, fulfillment, legal, claims, or platform review identifies an unacceptable risk.",
    ]
    if recommendation in {"investigate", "hold", "reject"}:
        conditions.append(
            "Complete critical research with stronger observed evidence and recalculate economics."
        )
    return conditions


def render_recommendation_markdown(brief: RecommendationBrief) -> str:
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) or "- None recorded"

    return f"""# Recommendation Brief: {brief.product_name}

Recommendation: **{brief.recommendation}**  
Confidence: **{brief.confidence_level}**  
Evidence completeness: **{brief.evidence_completeness}%**

## Reasons in favor
{bullets(brief.primary_reasons_in_favor)}

## Reasons against
{bullets(brief.primary_reasons_against)}

## Critical unknowns
{bullets(brief.critical_unknowns)}

## Economics
{brief.unit_economics_summary}

- Break-even CAC: {brief.break_even_cac}
- Break-even ROAS: {brief.break_even_roas or "Not available"}
- Maximum validation budget: {brief.maximum_validation_budget}

## Next experiment
{brief.suggested_next_experiment}

## Evidence cited
{bullets(brief.evidence_citations)}

## Conditions that would reverse the recommendation
{bullets(brief.reversal_conditions)}

> {brief.certainty_notice}
"""


def render_recommendation_json(brief: RecommendationBrief) -> str:
    values = asdict(brief)
    for key, value in list(values.items()):
        if isinstance(value, Decimal):
            values[key] = str(value)
    return json.dumps(values, indent=2)

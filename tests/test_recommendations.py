from decimal import Decimal

from sqlalchemy.orm import Session

from ai_commerce_engine.repositories.products import create_product
from ai_commerce_engine.schemas import ProductCreate
from ai_commerce_engine.services.recommendations import (
    DeterministicRecommendationGenerator,
    render_recommendation_json,
    render_recommendation_markdown,
)


def test_insufficient_evidence_forces_investigate_and_zero_budget(session: Session) -> None:
    product = create_product(
        session,
        ProductCreate(
            name="Unresearched candidate",
            proposed_selling_price=Decimal("50"),
            product_cost=Decimal("10"),
        ),
    )
    brief = DeterministicRecommendationGenerator().generate(session, product.id)
    assert brief.recommendation == "investigate"
    assert brief.confidence_level == "Low"
    assert brief.maximum_validation_budget == Decimal("0.00")
    assert "not a certain prediction" in brief.certainty_notice


def test_recommendation_exports_are_structured(session: Session) -> None:
    product = create_product(session, ProductCreate(name="Export recommendation"))
    brief = DeterministicRecommendationGenerator().generate(session, product.id)
    markdown = render_recommendation_markdown(brief)
    json_report = render_recommendation_json(brief)
    assert "Recommendation Brief" in markdown
    assert "Conditions that would reverse" in markdown
    assert '"recommendation": "investigate"' in json_report

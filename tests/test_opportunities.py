from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import AuditLog, OpportunityProductLink
from ai_commerce_engine.schemas import OpportunityCreate
from ai_commerce_engine.services.opportunities import (
    convert_opportunity_to_product,
    create_opportunity,
)


def test_rapid_opportunity_entry_and_conversion(session: Session) -> None:
    opportunity = create_opportunity(
        session,
        OpportunityCreate(
            title="Unusually expensive replacement part",
            observation="Customers buy a full assembly for one small failed part.",
            unusual_reason="The replacement cost is disproportionate.",
            source="Manual observation",
            observed_date=date(2026, 7, 13),
            tags=["Repair", "repair", " waste "],
            evidence_confidence="Medium",
            submitted_by="founder",
            things_that_shouldnt_be_true=True,
        ),
    )
    product = convert_opportunity_to_product(session, opportunity.id, "founder")
    session.commit()

    assert opportunity.status == "Converted to product candidate"
    assert product.name == opportunity.title
    assert opportunity.tags == ["repair", "waste"]
    link = session.scalar(select(OpportunityProductLink))
    assert link is not None
    assert link.product_id == product.id
    assert len(list(session.scalars(select(AuditLog)))) == 3


def test_opportunity_cannot_be_converted_twice(session: Session) -> None:
    opportunity = create_opportunity(
        session,
        OpportunityCreate(
            title="Observation",
            observation="A sufficiently specific raw observation.",
            source="Founder",
            observed_date=date(2026, 7, 13),
            evidence_confidence="Low",
            submitted_by="founder",
        ),
    )
    convert_opportunity_to_product(session, opportunity.id, "founder")
    with pytest.raises(ValueError, match="already been converted"):
        convert_opportunity_to_product(session, opportunity.id, "founder")

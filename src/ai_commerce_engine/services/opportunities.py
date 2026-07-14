from sqlalchemy.orm import Session

from ai_commerce_engine.models import Opportunity, OpportunityProductLink, Product
from ai_commerce_engine.repositories.products import create_product
from ai_commerce_engine.schemas import OpportunityCreate, ProductCreate
from ai_commerce_engine.services.audit import record_audit


def create_opportunity(
    session: Session, data: OpportunityCreate, actor: str | None = None
) -> Opportunity:
    values = data.model_dump(mode="python")
    if values.get("source_url") is not None:
        values["source_url"] = str(values["source_url"])
    opportunity = Opportunity(**values)
    session.add(opportunity)
    session.flush()
    record_audit(
        session,
        event_type="data_change",
        entity_type="opportunity",
        entity_id=opportunity.id,
        actor=actor or data.submitted_by,
        action="create",
        after={
            "title": opportunity.title,
            "status": opportunity.status,
            "things_that_shouldnt_be_true": opportunity.things_that_shouldnt_be_true,
        },
    )
    return opportunity


def convert_opportunity_to_product(session: Session, opportunity_id: int, actor: str) -> Product:
    opportunity = session.get(Opportunity, opportunity_id)
    if opportunity is None:
        raise ValueError(f"Opportunity {opportunity_id} does not exist")
    if opportunity.status == "Converted to product candidate":
        raise ValueError("Opportunity has already been converted")
    product = create_product(
        session,
        ProductCreate(
            name=opportunity.title,
            product_url=opportunity.source_url,
            source_platform=opportunity.source,
            category=opportunity.possible_category,
            target_customer=opportunity.possible_customer,
            customer_problem=opportunity.customer_problem,
            research_notes=(
                f"Converted from Opportunity Vault #{opportunity.id}. "
                f"Initial hypothesis: {opportunity.initial_hypothesis or 'Not recorded'}"
            ),
        ),
        actor=actor,
    )
    link = OpportunityProductLink(
        opportunity_id=opportunity.id,
        product_id=product.id,
        linked_by=actor,
    )
    session.add(link)
    previous = opportunity.status
    opportunity.status = "Converted to product candidate"
    record_audit(
        session,
        event_type="status_change",
        entity_type="opportunity",
        entity_id=opportunity.id,
        actor=actor,
        action="convert_to_product",
        before={"status": previous},
        after={"status": opportunity.status, "product_id": product.id},
    )
    session.flush()
    return product

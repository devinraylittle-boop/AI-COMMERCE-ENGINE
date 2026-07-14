from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import inspect, select

from ai_commerce_engine.db import SessionLocal, engine
from ai_commerce_engine.models import Product
from ai_commerce_engine.repositories.products import append_evidence, create_product
from ai_commerce_engine.schemas import EvidenceCreate, ProductCreate


def main() -> None:
    """Insert conspicuously fictional demonstration records once."""
    if not inspect(engine).has_table("products"):
        raise RuntimeError("Database schema is missing; run `alembic upgrade head` first")
    with SessionLocal.begin() as session:
        exists = session.scalar(select(Product).where(Product.is_fictional.is_(True)))
        if exists:
            print("Fictional seed data already exists; no changes made.")
            return
        product = create_product(
            session,
            ProductCreate(
                name="FICTIONAL — Modular Desk Cable Kit",
                source_platform="Fictional manual research",
                category="Desk organization",
                target_customer="Remote workers with cluttered desks",
                customer_problem="Loose charging cables make workspaces untidy",
                proposed_selling_price=Decimal("39.00"),
                product_cost=Decimal("9.50"),
                shipping_cost=Decimal("4.25"),
                packaging_cost=Decimal("1.10"),
                payment_processing_estimate=Decimal("1.47"),
                expected_refund_allowance=Decimal("1.95"),
                estimated_cac=Decimal("10.00"),
                supplier="FICTIONAL Supplier A",
                supplier_location="Fictional location",
                shipping_time="Estimated 8-12 days",
                minimum_order_quantity=50,
                marketplace_evidence="FICTIONAL: example only; not observed.",
                competition_notes="FICTIONAL: crowded category assumption.",
                fulfillment_risk="Adhesive performance and kit completeness require validation.",
                research_notes=(
                    "All seed values are fabricated demonstration data, not market evidence."
                ),
                is_fictional=True,
            ),
            actor="seed",
        )
        append_evidence(
            session,
            EvidenceCreate(
                product_id=product.id,
                evidence_type="Demo record",
                source="Fictional seed generator",
                observation="This is deliberately fictional data for interface demonstration only.",
                collected_at=datetime.now(UTC),
                collection_method="Application seed",
                confidence_level="Low",
                provenance="User-entered",
                notes="Do not use for business decisions.",
            ),
            actor="seed",
        )
    print("Inserted clearly marked fictional seed data.")


if __name__ == "__main__":
    main()

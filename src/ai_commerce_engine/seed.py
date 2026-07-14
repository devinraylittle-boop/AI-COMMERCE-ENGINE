from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import inspect, select

from ai_commerce_engine.db import SessionLocal, engine
from ai_commerce_engine.models import Product, ReviewImportBatch
from ai_commerce_engine.repositories.products import append_evidence, create_product
from ai_commerce_engine.schemas import EvidenceCreate, ProductCreate, ReviewInput
from ai_commerce_engine.services.review_classification import correct_classification
from ai_commerce_engine.services.review_imports import create_manual_review


def main() -> None:
    """Insert conspicuously fictional demonstration records once."""
    if not inspect(engine).has_table("products"):
        raise RuntimeError("Database schema is missing; run `alembic upgrade head` first")
    with SessionLocal.begin() as session:
        exists = session.scalar(select(Product).where(Product.is_fictional.is_(True)))
        if exists:
            product = exists
        else:
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
                    fulfillment_risk=(
                        "Adhesive performance and kit completeness require validation."
                    ),
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
                    observation=(
                        "This is deliberately fictional data for interface demonstration only."
                    ),
                    collected_at=datetime.now(UTC),
                    collection_method="Application seed",
                    confidence_level="Low",
                    provenance="User-entered",
                    notes="Do not use for business decisions.",
                ),
                actor="seed",
            )
        review_seeded = session.scalar(
            select(ReviewImportBatch).where(ReviewImportBatch.is_fictional.is_(True))
        )
        if review_seeded:
            print("Fictional product and review data already exist; no review changes made.")
            return
        second = create_product(
            session,
            ProductCreate(
                name="FICTIONAL - Collapsible Travel Bowl",
                source_platform="Fictional manual research",
                category="Travel accessories",
                research_notes="Fabricated demonstration product; not market evidence.",
                is_fictional=True,
            ),
            actor="seed",
        )
        examples = [
            (
                product.id,
                "Fictional Marketplace A",
                "5",
                "Love the easy to use clips and excellent cable control.",
            ),
            (
                product.id,
                "Fictional Marketplace A",
                "1",
                "The adhesive failed and the clasp broke after two uses.",
            ),
            (
                product.id,
                "Fictional Marketplace B",
                "2",
                "Packaging was damaged on arrival and a missing part made setup frustrating.",
            ),
            (
                product.id,
                "Fictional Marketplace B",
                "3",
                "I wish the kit included longer clips; it also works for my craft tools.",
            ),
            (
                second.id,
                "Fictional Marketplace A",
                "5",
                "Great value and perfect for my child on road trips.",
            ),
            (
                second.id,
                "Fictional Marketplace B",
                "1",
                "The sharp edge feels unsafe and the bowl cracked quickly.",
            ),
            (
                second.id,
                "Fictional Marketplace B",
                "2",
                "Not as described: too small, so I returned it.",
            ),
        ]
        created_reviews = []
        for index, (product_id, source, rating, body) in enumerate(examples, start=1):
            created_reviews.append(
                create_manual_review(
                    session,
                    product_id=product_id,
                    review=ReviewInput(
                        external_review_id=f"FICTIONAL-{index}",
                        source_platform=source,
                        rating=Decimal(rating),
                        rating_scale=Decimal("5"),
                        original_review_body=body,
                        provenance_type="Fictional",
                        is_fictional=True,
                    ),
                    actor="seed",
                )
            )
        create_manual_review(
            session,
            product_id=product.id,
            review=ReviewInput(
                external_review_id="FICTIONAL-DUPLICATE",
                source_platform="Fictional Marketplace C",
                rating=Decimal("1"),
                rating_scale=Decimal("5"),
                original_review_body=examples[1][3],
                provenance_type="Fictional",
                is_fictional=True,
            ),
            actor="seed",
        )
        correct_classification(
            session,
            created_reviews[3],
            ["Requested improvement", "Unexpected use", "Missing accessory"],
            actor="fictional reviewer",
            reason="FICTIONAL demonstration of a human correction",
            note="Adds the missing-accessory interpretation for demonstration.",
        )
    print("Inserted clearly marked fictional product and review data.")


if __name__ == "__main__":
    main()

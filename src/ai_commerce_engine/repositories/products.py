from collections.abc import Iterable
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import Evidence, Product, ProductVersion
from ai_commerce_engine.schemas import EvidenceCreate, ProductCreate
from ai_commerce_engine.services.audit import record_audit


def create_product(session: Session, data: ProductCreate, actor: str = "user") -> Product:
    values = data.model_dump(mode="json")
    if values.get("product_url") is not None:
        values["product_url"] = str(values["product_url"])
    product = Product(**values)
    session.add(product)
    session.flush()
    session.add(
        ProductVersion(
            product_id=product.id,
            version_number=1,
            based_on_version=None,
            snapshot=data.model_dump(mode="json"),
            actor=actor,
            reason="Initial product creation",
            source=None,
            supporting_evidence=None,
            provenance="User-entered",
        )
    )
    record_audit(
        session,
        event_type="data_change",
        entity_type="product",
        entity_id=product.id,
        actor=actor,
        action="create",
        after={"name": product.name, "status": product.status},
    )
    return product


def list_products(session: Session) -> list[Product]:
    return list(session.scalars(select(Product).order_by(Product.updated_at.desc())))


def append_evidence(session: Session, data: EvidenceCreate, actor: str = "user") -> Evidence:
    if session.get(Product, data.product_id) is None:
        raise ValueError(f"Product {data.product_id} does not exist")
    values: dict[str, Any] = data.model_dump(mode="python")
    if values.get("source_url") is not None:
        values["source_url"] = str(values["source_url"])
    evidence = Evidence(**values)
    session.add(evidence)
    session.flush()
    record_audit(
        session,
        event_type="data_change",
        entity_type="evidence",
        entity_id=evidence.id,
        actor=actor,
        action="append",
        after={"type": evidence.evidence_type, "provenance": evidence.provenance},
    )
    return evidence


def import_products(
    session: Session, rows: Iterable[dict[str, Any]], actor: str
) -> tuple[int, list[str]]:
    count = 0
    errors: list[str] = []
    for number, row in enumerate(rows, start=2):
        try:
            create_product(session, ProductCreate.model_validate(row), actor)
            count += 1
        except Exception as exc:
            errors.append(f"Row {number}: {exc}")
    record_audit(
        session,
        event_type="import",
        entity_type="product",
        entity_id=None,
        actor=actor,
        action="csv_import",
        after={"imported": count, "errors": len(errors)},
        details="; ".join(errors[:10]) or None,
    )
    return count, errors

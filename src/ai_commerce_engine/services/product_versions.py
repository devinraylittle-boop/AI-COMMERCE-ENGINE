from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import Product, ProductFieldChange, ProductVersion
from ai_commerce_engine.schemas import ProductCreate, ProductEdit
from ai_commerce_engine.services.audit import record_audit

EDITABLE_FIELDS = frozenset(ProductCreate.model_fields)


class StaleProductVersionError(ValueError):
    """Raised when an edit was based on an older live version."""


def _json_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    return str(value) if value.__class__.__name__ == "HttpUrl" else value


def product_snapshot(product: Product) -> dict[str, Any]:
    return {field: _json_value(getattr(product, field)) for field in EDITABLE_FIELDS}


def _ensure_baseline(session: Session, product: Product) -> None:
    existing = session.scalar(
        select(ProductVersion).where(
            ProductVersion.product_id == product.id,
            ProductVersion.version_number == product.current_version,
        )
    )
    if existing is None:
        session.add(
            ProductVersion(
                product_id=product.id,
                version_number=product.current_version,
                based_on_version=None,
                snapshot=product_snapshot(product),
                actor="system",
                reason="Baseline captured during versioning migration",
                provenance="User-entered",
            )
        )
        session.flush()


def edit_product(session: Session, edit: ProductEdit) -> ProductVersion:
    product = session.get(Product, edit.product_id)
    if product is None:
        raise ValueError(f"Product {edit.product_id} does not exist")
    if product.current_version != edit.based_on_version:
        raise StaleProductVersionError(
            f"Stale edit: expected version {edit.based_on_version}, "
            f"current version is {product.current_version}"
        )
    unknown = set(edit.changes) - EDITABLE_FIELDS
    if unknown:
        raise ValueError(f"Fields are not editable: {', '.join(sorted(unknown))}")
    before = product_snapshot(product)
    prospective = before | edit.changes
    validated = ProductCreate.model_validate(prospective)
    after = validated.model_dump(mode="json")
    changed = {field for field in edit.changes if before[field] != after[field]}
    if not changed:
        raise ValueError("The edit does not change any values")

    _ensure_baseline(session, product)
    next_version = product.current_version + 1
    version = ProductVersion(
        product_id=product.id,
        version_number=next_version,
        based_on_version=product.current_version,
        snapshot=after,
        actor=edit.actor,
        reason=edit.reason,
        source=edit.source,
        supporting_evidence=edit.supporting_evidence,
        provenance=edit.provenance,
    )
    session.add(version)
    session.flush()
    for field in sorted(changed):
        session.add(
            ProductFieldChange(
                product_version_id=version.id,
                field_name=field,
                previous_value=before[field],
                new_value=after[field],
                actor=edit.actor,
                reason=edit.reason,
                source=edit.source,
                supporting_evidence=edit.supporting_evidence,
                provenance=edit.provenance,
            )
        )
        setattr(product, field, after[field])
    product.current_version = next_version
    record_audit(
        session,
        event_type="assumption_change" if changed & _financial_fields() else "data_change",
        entity_type="product_version",
        entity_id=version.id,
        actor=edit.actor,
        action="edit_product",
        before={field: before[field] for field in changed},
        after={field: after[field] for field in changed},
        details=edit.reason,
    )
    session.flush()
    return version


def _financial_fields() -> set[str]:
    return {
        "proposed_selling_price",
        "product_cost",
        "shipping_cost",
        "packaging_cost",
        "payment_processing_estimate",
        "expected_refund_allowance",
        "estimated_cac",
        "platform_cost_allocation",
        "chargeback_allowance",
        "discount_estimate",
        "minimum_order_quantity",
    }


def rollback_product(
    session: Session,
    *,
    product_id: int,
    target_version: int,
    based_on_version: int,
    actor: str,
    reason: str,
) -> ProductVersion:
    target = session.scalar(
        select(ProductVersion).where(
            ProductVersion.product_id == product_id,
            ProductVersion.version_number == target_version,
        )
    )
    if target is None:
        raise ValueError(f"Version {target_version} does not exist for product {product_id}")
    current = session.get(Product, product_id)
    if current is None:
        raise ValueError(f"Product {product_id} does not exist")
    before = product_snapshot(current)
    changes = {key: value for key, value in target.snapshot.items() if before[key] != value}
    return edit_product(
        session,
        ProductEdit(
            product_id=product_id,
            based_on_version=based_on_version,
            changes=changes,
            actor=actor,
            reason=reason,
            source=f"Product version {target_version}",
            supporting_evidence=None,
            provenance="User-entered",
        ),
    )

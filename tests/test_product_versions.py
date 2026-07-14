from decimal import Decimal

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import AuditLog, ProductFieldChange, ProductVersion
from ai_commerce_engine.repositories.products import create_product
from ai_commerce_engine.schemas import ProductCreate, ProductEdit
from ai_commerce_engine.services.product_versions import (
    StaleProductVersionError,
    edit_product,
    rollback_product,
)


def test_product_edit_creates_version_changes_and_audit(session: Session) -> None:
    product = create_product(
        session,
        ProductCreate(name="Original", product_cost=Decimal("10.00")),
    )
    version = edit_product(
        session,
        ProductEdit(
            product_id=product.id,
            based_on_version=1,
            changes={"name": "Revised", "product_cost": "12.50"},
            actor="founder",
            reason="Supplier quote updated",
            source="Quote Q-17",
            supporting_evidence="Evidence #4",
            provenance="Observed",
        ),
    )
    session.commit()

    assert product.current_version == 2
    assert product.name == "Revised"
    assert product.product_cost == Decimal("12.50")
    assert version.version_number == 2
    changes = list(
        session.scalars(
            select(ProductFieldChange).where(ProductFieldChange.product_version_id == version.id)
        )
    )
    assert {change.field_name for change in changes} == {"name", "product_cost"}
    audit = session.scalar(select(AuditLog).where(AuditLog.entity_type == "product_version"))
    assert audit is not None
    assert audit.event_type == "assumption_change"


def test_invalid_and_stale_edits_do_not_create_versions(session: Session) -> None:
    product = create_product(session, ProductCreate(name="Original"))
    with pytest.raises(ValidationError):
        edit_product(
            session,
            ProductEdit(
                product_id=product.id,
                based_on_version=1,
                changes={"product_cost": "-1"},
                actor="founder",
                reason="Invalid negative value",
                provenance="Estimated",
            ),
        )
    session.rollback()
    product = create_product(session, ProductCreate(name="Another"))
    edit_product(
        session,
        ProductEdit(
            product_id=product.id,
            based_on_version=1,
            changes={"name": "Changed"},
            actor="founder",
            reason="Clarified product name",
            provenance="User-entered",
        ),
    )
    with pytest.raises(StaleProductVersionError, match="Stale edit"):
        edit_product(
            session,
            ProductEdit(
                product_id=product.id,
                based_on_version=1,
                changes={"name": "Conflicting change"},
                actor="founder",
                reason="Used an old browser tab",
                provenance="User-entered",
            ),
        )


def test_rollback_creates_a_new_version(session: Session) -> None:
    product = create_product(session, ProductCreate(name="Version one"))
    edit_product(
        session,
        ProductEdit(
            product_id=product.id,
            based_on_version=1,
            changes={"name": "Version two"},
            actor="founder",
            reason="Rename",
            provenance="User-entered",
        ),
    )
    rolled_back = rollback_product(
        session,
        product_id=product.id,
        target_version=1,
        based_on_version=2,
        actor="founder",
        reason="Restore the earlier name after review",
    )
    session.commit()

    assert product.name == "Version one"
    assert product.current_version == 3
    assert rolled_back.version_number == 3
    assert session.scalar(select(ProductVersion).where(ProductVersion.version_number == 2))

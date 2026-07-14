from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_commerce_engine.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    product_url: Mapped[str | None] = mapped_column(String(1000))
    source_platform: Mapped[str | None] = mapped_column(String(100))
    category: Mapped[str | None] = mapped_column(String(150), index=True)
    target_customer: Mapped[str | None] = mapped_column(Text)
    customer_problem: Mapped[str | None] = mapped_column(Text)
    proposed_selling_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    product_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    shipping_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    packaging_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    payment_processing_estimate: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    expected_refund_allowance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    estimated_cac: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    platform_cost_allocation: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    chargeback_allowance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    discount_estimate: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    supplier: Mapped[str | None] = mapped_column(String(200))
    supplier_location: Mapped[str | None] = mapped_column(String(200))
    shipping_time: Mapped[str | None] = mapped_column(String(100))
    minimum_order_quantity: Mapped[int | None] = mapped_column(Integer)
    marketplace_evidence: Mapped[str | None] = mapped_column(Text)
    search_evidence: Mapped[str | None] = mapped_column(Text)
    social_evidence: Mapped[str | None] = mapped_column(Text)
    competition_notes: Mapped[str | None] = mapped_column(Text)
    review_complaints: Mapped[str | None] = mapped_column(Text)
    upsell_ideas: Mapped[str | None] = mapped_column(Text)
    repeat_purchase_potential: Mapped[str | None] = mapped_column(Text)
    fulfillment_risk: Mapped[str | None] = mapped_column(Text)
    legal_policy_concerns: Mapped[str | None] = mapped_column(Text)
    research_notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="Discovered", index=True)
    current_version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    is_fictional: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    evidence: Mapped[list["Evidence"]] = relationship(back_populates="product")
    scores: Mapped[list["ScoreSnapshot"]] = relationship(back_populates="product")
    versions: Mapped[list["ProductVersion"]] = relationship(back_populates="product")


class ProductVersion(Base):
    __tablename__ = "product_versions"
    __table_args__ = (UniqueConstraint("product_id", "version_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    based_on_version: Mapped[int | None] = mapped_column(Integer)
    snapshot: Mapped[dict[str, Any]] = mapped_column(JSON)
    actor: Mapped[str] = mapped_column(String(100))
    reason: Mapped[str] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(300))
    supporting_evidence: Mapped[str | None] = mapped_column(Text)
    provenance: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    product: Mapped[Product] = relationship(back_populates="versions")
    changes: Mapped[list["ProductFieldChange"]] = relationship(
        back_populates="version", cascade="all, delete-orphan"
    )


class ProductFieldChange(Base):
    __tablename__ = "product_field_changes"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_version_id: Mapped[int] = mapped_column(ForeignKey("product_versions.id"), index=True)
    field_name: Mapped[str] = mapped_column(String(100), index=True)
    previous_value: Mapped[Any | None] = mapped_column(JSON)
    new_value: Mapped[Any | None] = mapped_column(JSON)
    actor: Mapped[str] = mapped_column(String(100))
    reason: Mapped[str] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(300))
    supporting_evidence: Mapped[str | None] = mapped_column(Text)
    provenance: Mapped[str] = mapped_column(String(30))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    version: Mapped[ProductVersion] = relationship(back_populates="changes")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    observation: Mapped[str] = mapped_column(Text)
    unusual_reason: Mapped[str | None] = mapped_column(Text)
    customer_problem: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(300))
    source_url: Mapped[str | None] = mapped_column(String(1000))
    attachment_reference: Mapped[str | None] = mapped_column(String(1000))
    observed_date: Mapped[date] = mapped_column(Date)
    market: Mapped[str | None] = mapped_column(String(200))
    possible_category: Mapped[str | None] = mapped_column(String(150))
    possible_customer: Mapped[str | None] = mapped_column(Text)
    initial_hypothesis: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    evidence_confidence: Mapped[str] = mapped_column(String(20))
    submitted_by: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="Inbox", index=True)
    follow_up_questions: Mapped[str | None] = mapped_column(Text)
    things_that_shouldnt_be_true: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class OpportunityProductLink(Base):
    __tablename__ = "opportunity_product_links"
    __table_args__ = (UniqueConstraint("opportunity_id", "product_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    linked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    linked_by: Mapped[str] = mapped_column(String(100))


class OpportunityEvidenceLink(Base):
    __tablename__ = "opportunity_evidence_links"
    __table_args__ = (UniqueConstraint("opportunity_id", "evidence_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"), index=True)
    evidence_id: Mapped[int] = mapped_column(ForeignKey("evidence.id"), index=True)
    linked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    linked_by: Mapped[str] = mapped_column(String(100))


class ResearchEntry(Base):
    __tablename__ = "research_entries"
    __table_args__ = (UniqueConstraint("product_id", "section_key", "version_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    section_key: Mapped[str] = mapped_column(String(100), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    evidence_ids: Mapped[list[int]] = mapped_column(JSON, default=list)
    provenance: Mapped[str] = mapped_column(String(30))
    actor: Mapped[str] = mapped_column(String(100))
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    evidence_type: Mapped[str] = mapped_column(String(100), index=True)
    source: Mapped[str] = mapped_column(String(300))
    source_url: Mapped[str | None] = mapped_column(String(1000))
    observation: Mapped[str] = mapped_column(Text)
    numeric_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    unit: Mapped[str | None] = mapped_column(String(100))
    geography: Mapped[str | None] = mapped_column(String(150))
    time_period: Mapped[str | None] = mapped_column(String(150))
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, index=True
    )
    collection_method: Mapped[str] = mapped_column(String(100))
    confidence_level: Mapped[str] = mapped_column(String(20))
    provenance: Mapped[str] = mapped_column(String(30))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    product: Mapped[Product] = relationship(back_populates="evidence")


class ScoreSnapshot(Base):
    __tablename__ = "score_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    base_score: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    penalty_total: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    final_score: Mapped[Decimal] = mapped_column(Numeric(6, 2), index=True)
    components: Mapped[dict[str, Any]] = mapped_column(JSON)
    weights: Mapped[dict[str, Any]] = mapped_column(JSON)
    penalties: Mapped[dict[str, Any]] = mapped_column(JSON)
    rationale: Mapped[str | None] = mapped_column(Text)
    actor: Mapped[str] = mapped_column(String(100), default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    product: Mapped[Product] = relationship(back_populates="scores")


class StatusHistory(Base):
    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    previous_status: Mapped[str] = mapped_column(String(50))
    new_status: Mapped[str] = mapped_column(String(50), index=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    reason: Mapped[str] = mapped_column(Text)
    actor: Mapped[str] = mapped_column(String(100))
    supporting_evidence: Mapped[str | None] = mapped_column(Text)
    next_action: Mapped[str | None] = mapped_column(Text)


class SupplierOffer(Base):
    __tablename__ = "supplier_offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    supplier_name: Mapped[str] = mapped_column(String(200))
    location: Mapped[str | None] = mapped_column(String(200))
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    shipping_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    lead_time_days: Mapped[int | None] = mapped_column(Integer)
    minimum_order_quantity: Mapped[int | None] = mapped_column(Integer)
    evidence_quality: Mapped[str] = mapped_column(String(20), default="Low")
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ValidationExperiment(Base):
    __tablename__ = "validation_experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    hypothesis: Mapped[str] = mapped_column(Text)
    test_type: Mapped[str] = mapped_column(String(100))
    audience: Mapped[str | None] = mapped_column(Text)
    channel: Mapped[str | None] = mapped_column(String(100))
    offer: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    creative: Mapped[str | None] = mapped_column(Text)
    budget_ceiling: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    visits: Mapped[int] = mapped_column(Integer, default=0)
    email_signups: Mapped[int] = mapped_column(Integer, default=0)
    add_to_carts: Mapped[int] = mapped_column(Integer, default=0)
    checkout_initiations: Mapped[int] = mapped_column(Integer, default=0)
    purchases: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    refunds: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=0)
    customer_acquisition_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    contribution_profit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    result: Mapped[str | None] = mapped_column(Text)
    lessons: Mapped[str | None] = mapped_column(Text)
    decision: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    entity_type: Mapped[str] = mapped_column(String(50), index=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, index=True)
    actor: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(String(100))
    before: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    after: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, index=True
    )


class AppSetting(Base):
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[dict[str, Any]] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(Text)
    updated_by: Mapped[str] = mapped_column(String(100))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

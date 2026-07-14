from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class ProductCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=200)
    product_url: HttpUrl | None = None
    source_platform: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=150)
    target_customer: str | None = None
    customer_problem: str | None = None
    proposed_selling_price: Decimal = Field(default=Decimal("0"), ge=0)
    product_cost: Decimal = Field(default=Decimal("0"), ge=0)
    shipping_cost: Decimal = Field(default=Decimal("0"), ge=0)
    packaging_cost: Decimal = Field(default=Decimal("0"), ge=0)
    payment_processing_estimate: Decimal = Field(default=Decimal("0"), ge=0)
    expected_refund_allowance: Decimal = Field(default=Decimal("0"), ge=0)
    estimated_cac: Decimal = Field(default=Decimal("0"), ge=0)
    platform_cost_allocation: Decimal = Field(default=Decimal("0"), ge=0)
    chargeback_allowance: Decimal = Field(default=Decimal("0"), ge=0)
    discount_estimate: Decimal = Field(default=Decimal("0"), ge=0)
    supplier: str | None = None
    supplier_location: str | None = None
    shipping_time: str | None = None
    minimum_order_quantity: int | None = Field(default=None, ge=0)
    marketplace_evidence: str | None = None
    search_evidence: str | None = None
    social_evidence: str | None = None
    competition_notes: str | None = None
    review_complaints: str | None = None
    upsell_ideas: str | None = None
    repeat_purchase_potential: str | None = None
    fulfillment_risk: str | None = None
    legal_policy_concerns: str | None = None
    research_notes: str | None = None
    is_fictional: bool = False


class EvidenceCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product_id: int = Field(gt=0)
    evidence_type: str = Field(min_length=1, max_length=100)
    source: str = Field(min_length=1, max_length=300)
    source_url: HttpUrl | None = None
    observation: str = Field(min_length=1)
    numeric_value: Decimal | None = None
    unit: str | None = None
    geography: str | None = None
    time_period: str | None = None
    collected_at: datetime
    collection_method: str = Field(min_length=1, max_length=100)
    confidence_level: Literal["Low", "Medium", "High"]
    provenance: Literal["Observed", "Estimated", "Inferred", "User-entered"]
    notes: str | None = None


class StatusChange(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product_id: int = Field(gt=0)
    new_status: str
    reason: str = Field(min_length=3)
    actor: str = Field(min_length=1, max_length=100)
    supporting_evidence: str | None = None
    next_action: str | None = None

    @field_validator("new_status")
    @classmethod
    def valid_status(cls, value: str) -> str:
        from ai_commerce_engine.services.workflow import PIPELINE_STATUSES

        if value not in PIPELINE_STATUSES:
            raise ValueError(f"Unknown status: {value}")
        return value


class ProductEdit(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product_id: int = Field(gt=0)
    based_on_version: int = Field(gt=0)
    changes: dict[str, Any] = Field(min_length=1)
    actor: str = Field(min_length=1, max_length=100)
    reason: str = Field(min_length=3)
    source: str | None = Field(default=None, max_length=300)
    supporting_evidence: str | None = None
    provenance: Literal["Observed", "Estimated", "Inferred", "User-entered"]


class OpportunityCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    observation: str = Field(min_length=3)
    unusual_reason: str | None = None
    customer_problem: str | None = None
    source: str = Field(min_length=1, max_length=300)
    source_url: HttpUrl | None = None
    attachment_reference: str | None = Field(default=None, max_length=1000)
    observed_date: date
    market: str | None = Field(default=None, max_length=200)
    possible_category: str | None = Field(default=None, max_length=150)
    possible_customer: str | None = None
    initial_hypothesis: str | None = None
    tags: list[str] = Field(default_factory=list)
    evidence_confidence: Literal["Low", "Medium", "High"]
    submitted_by: str = Field(min_length=1, max_length=100)
    status: Literal[
        "Inbox",
        "Needs context",
        "Worth investigating",
        "Converted to product candidate",
        "Rejected",
        "Archived",
    ] = "Inbox"
    follow_up_questions: str | None = None
    things_that_shouldnt_be_true: bool = False

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, values: list[str]) -> list[str]:
        return sorted({value.strip().lower() for value in values if value.strip()})

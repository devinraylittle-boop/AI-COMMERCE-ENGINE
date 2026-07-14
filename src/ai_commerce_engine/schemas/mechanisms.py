from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Provenance = Literal["Observed", "Inferred", "Hypothesis", "Unknown"]
Confidence = Literal["Low", "Medium", "High"]
MechanismStatus = Literal[
    "hypothesis",
    "under_test",
    "rejected",
    "validated_instance",
    "validated_play",
    "anti_play",
]


class MechanismEvidence(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    evidence_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]+$")
    proposition: str = Field(min_length=10)
    source_reference: str = Field(min_length=3)
    provenance: Provenance
    confidence: Confidence
    interpretation_limit: str = Field(min_length=10)


class FalsificationExperiment(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    experiment_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]+$")
    question: str = Field(min_length=10)
    hypothesis: str = Field(min_length=10)
    null_hypothesis: str = Field(min_length=10)
    evidence_sources: list[str] = Field(min_length=2)
    sampling_plan: list[str] = Field(min_length=2)
    survival_criteria: list[str] = Field(min_length=1)
    falsification_criteria: list[str] = Field(min_length=1)
    known_confounders: list[str] = Field(min_length=1)
    validation_cost_ceiling_usd: Decimal = Field(ge=0, max_digits=8, decimal_places=2)
    prohibited_actions: list[str] = Field(min_length=1)
    next_decision: str = Field(min_length=10)


class TransferabilityAssessment(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    status: Literal["unknown", "single_instance", "replication_pending", "replicated"]
    boundary_conditions: list[str] = Field(min_length=1)
    next_replication_test: str = Field(min_length=10)


class MechanismCard(BaseModel):
    """A versioned, falsifiable commercial-mechanism hypothesis."""

    model_config = ConfigDict(str_strip_whitespace=True)

    schema_version: Literal["1.0"]
    mechanism_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]+$")
    version: int = Field(ge=1)
    name: str = Field(min_length=3, max_length=150)
    status: MechanismStatus
    causal_claim: str = Field(min_length=20)
    why_it_might_work: list[str] = Field(min_length=1)
    supporting_evidence: list[MechanismEvidence] = Field(min_length=1)
    contradicting_evidence: list[MechanismEvidence] = Field(min_length=1)
    required_conditions: list[str] = Field(min_length=1)
    failure_conditions: list[str] = Field(min_length=1)
    falsification_experiment: FalsificationExperiment
    confidence: Confidence
    confidence_rationale: str = Field(min_length=20)
    transferability: TransferabilityAssessment
    instruction_status: Literal["not_earned", "candidate", "earned", "revoked"]
    current_instruction: str | None = None
    decision_owner: str = Field(min_length=1, max_length=100)
    last_updated: date

    @model_validator(mode="after")
    def enforce_instruction_integrity(self) -> "MechanismCard":
        if self.instruction_status == "earned":
            if self.status != "validated_play":
                raise ValueError("An earned instruction requires validated_play status")
            if self.transferability.status != "replicated":
                raise ValueError("An earned instruction requires replicated transferability")
            if not self.current_instruction:
                raise ValueError("An earned instruction requires instruction text")
        elif self.current_instruction is not None:
            raise ValueError("Instruction text must remain empty until the instruction is earned")

        if self.status == "validated_play" and self.transferability.status != "replicated":
            raise ValueError("validated_play requires replicated transferability")
        return self

import json
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from ai_commerce_engine.schemas.mechanisms import MechanismCard
from ai_commerce_engine.services.mechanisms import (
    MechanismCardSetError,
    validate_mechanism_card_set,
)


def card_payload(mechanism_id: str = "test_play") -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "mechanism_id": mechanism_id,
        "version": 1,
        "name": "Test Play",
        "status": "hypothesis",
        "causal_claim": "A defined customer mechanism produces a measurable commercial response.",
        "why_it_might_work": ["The customer experiences a recurring unresolved problem."],
        "supporting_evidence": [
            {
                "evidence_id": "support_1",
                "proposition": "A public source documents the recurring customer problem.",
                "source_reference": "source-a",
                "provenance": "Observed",
                "confidence": "Medium",
                "interpretation_limit": "This source does not measure willingness to pay.",
            }
        ],
        "contradicting_evidence": [
            {
                "evidence_id": "against_1",
                "proposition": "The market also contains strong commodity competition.",
                "source_reference": "source-b",
                "provenance": "Inferred",
                "confidence": "Low",
                "interpretation_limit": "Supplier and price evidence has not been collected.",
            }
        ],
        "required_conditions": ["The problem must recur across more than one context."],
        "failure_conditions": ["Customers solve the problem without a purchase."],
        "falsification_experiment": {
            "experiment_id": "experiment_1",
            "question": "Does the problem recur across independent evidence streams?",
            "hypothesis": "The same actionable problem appears in reviews and interviews.",
            "null_hypothesis": "Observed complaints are isolated and do not transfer.",
            "evidence_sources": ["authorized reviews", "customer interviews"],
            "sampling_plan": ["Analyze 100 reviews.", "Interview five customers."],
            "survival_criteria": ["A predeclared theme appears across both sources."],
            "falsification_criteria": ["No theme survives source triangulation."],
            "known_confounders": ["Convenience samples are not market prevalence."],
            "validation_cost_ceiling_usd": "25.00",
            "prohibited_actions": ["No advertising or inventory purchase."],
            "next_decision": "Reject the mechanism or advance it to a commercial test.",
        },
        "confidence": "Low",
        "confidence_rationale": "Only broad market evidence exists before primary collection.",
        "transferability": {
            "status": "unknown",
            "boundary_conditions": ["No commercial instance has been tested."],
            "next_replication_test": (
                "Repeat the mechanism in a second market after one instance passes."
            ),
        },
        "instruction_status": "not_earned",
        "current_instruction": None,
        "decision_owner": "Founder",
        "last_updated": "2026-07-14",
    }


def test_hypothesis_card_is_valid() -> None:
    card = MechanismCard.model_validate(card_payload())
    assert card.instruction_status == "not_earned"


def test_instruction_cannot_be_claimed_before_replication() -> None:
    payload = card_payload()
    payload["instruction_status"] = "earned"
    payload["current_instruction"] = "Run this play everywhere."

    with pytest.raises(ValidationError, match="validated_play"):
        MechanismCard.model_validate(payload)


def test_card_set_enforces_unique_ids_and_budget(tmp_path: Path) -> None:
    for index in range(2):
        (tmp_path / f"card-{index}.json").write_text(json.dumps(card_payload()), encoding="utf-8")

    with pytest.raises(MechanismCardSetError, match="unique"):
        validate_mechanism_card_set(tmp_path)

    (tmp_path / "card-1.json").write_text(json.dumps(card_payload("second_play")), encoding="utf-8")
    with pytest.raises(MechanismCardSetError, match="exceeds"):
        validate_mechanism_card_set(tmp_path, total_budget_ceiling_usd=Decimal("49"))


def test_operation_first_principle_cards_validate() -> None:
    root = Path(__file__).resolve().parents[1]
    cards = validate_mechanism_card_set(root / "mechanisms", total_budget_ceiling_usd=Decimal("75"))
    assert {card.mechanism_id for card in cards} == {
        "expertise_ladder",
        "friction_removal",
        "trust_mediated_care",
    }
    assert all(card.instruction_status == "not_earned" for card in cards)

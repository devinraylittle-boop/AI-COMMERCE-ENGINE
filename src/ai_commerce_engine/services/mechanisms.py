import json
from decimal import Decimal
from pathlib import Path

from pydantic import ValidationError

from ai_commerce_engine.schemas.mechanisms import MechanismCard


class MechanismCardSetError(ValueError):
    """Raised when a mechanism-card collection violates laboratory rules."""


def load_mechanism_card(path: Path) -> MechanismCard:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return MechanismCard.model_validate(payload)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise MechanismCardSetError(f"Invalid mechanism card {path}: {exc}") from exc


def validate_mechanism_card_set(
    directory: Path,
    *,
    total_budget_ceiling_usd: Decimal | None = None,
) -> list[MechanismCard]:
    paths = sorted(directory.glob("*.json"))
    if not paths:
        raise MechanismCardSetError(f"No mechanism cards found in {directory}")

    cards = [load_mechanism_card(path) for path in paths]
    ids = [card.mechanism_id for card in cards]
    if len(ids) != len(set(ids)):
        raise MechanismCardSetError("Mechanism IDs must be unique within a card set")

    if total_budget_ceiling_usd is not None:
        total = sum(
            (card.falsification_experiment.validation_cost_ceiling_usd for card in cards),
            start=Decimal("0"),
        )
        if total > total_budget_ceiling_usd:
            raise MechanismCardSetError(
                f"Card-set validation ceiling ${total} exceeds ${total_budget_ceiling_usd}"
            )
    return cards

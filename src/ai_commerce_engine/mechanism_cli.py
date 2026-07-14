import argparse
from decimal import Decimal
from pathlib import Path

from ai_commerce_engine.services.mechanisms import validate_mechanism_card_set


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate ACE mechanism cards")
    parser.add_argument("directory", nargs="?", type=Path, default=Path("mechanisms"))
    parser.add_argument("--total-budget-ceiling", type=Decimal, default=None)
    args = parser.parse_args()

    cards = validate_mechanism_card_set(
        args.directory,
        total_budget_ceiling_usd=args.total_budget_ceiling,
    )
    total = sum(
        (card.falsification_experiment.validation_cost_ceiling_usd for card in cards),
        start=Decimal("0"),
    )
    print(f"Validated {len(cards)} mechanism cards; combined ceiling: ${total}")
    for card in cards:
        print(f"- {card.mechanism_id} v{card.version}: {card.status}")

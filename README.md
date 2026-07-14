# AI Commerce Engine

AI Commerce Engine is a local, evidence-led workspace for discovering, evaluating, validating, and governing ecommerce product opportunities. Phase 1 is an intelligence system—not a storefront—and performs no autonomous spending, publishing, ordering, supplier contact, or advertising.

Work Orders 002 and 003 add versioned product edits, an Opportunity Vault, an evidence-aware Research Workbench, deterministic recommendation briefs, and compliant review mining. Mission Control, provider adapters, and Profit Sprint execution remain planned work.

## Quick start

Requires Python 3.12+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
alembic upgrade head
streamlit run src/ai_commerce_engine/app.py
```

Optional fictional demonstration data:

```powershell
ai-commerce-seed
```

Every seeded record contains `FICTIONAL` labeling and must not be used for a business decision.

Review Mining supports manual, CSV, and JSON intake with dry runs, immutable batches, original-text preservation, deterministic duplicate detection, versioned classification and correction, sample-scoped analytics, and Markdown/JSON reports. See [REVIEW_MINING.md](REVIEW_MINING.md).

## Quality commands

```powershell
ruff check .
ruff format --check .
mypy src
pytest
```

See [CURRENT_PROJECT.md](CURRENT_PROJECT.md), [ACCEPTANCE_REPORT_PHASE_1.md](ACCEPTANCE_REPORT_PHASE_1.md), [ARCHITECTURE.md](ARCHITECTURE.md), and [VALIDATION_PROTOCOL.md](VALIDATION_PROTOCOL.md) before extending the system.

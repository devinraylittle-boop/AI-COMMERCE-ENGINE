# Current Project

## Current phase

Work Order 003 - compliant review-mining foundation. Phase F is implemented on `feature/review-mining-foundation`; Mission Control and later Work Order 002 objectives remain open.

## Completed work

- Typed SQLAlchemy domain model for products, append-only evidence, score snapshots, status history, suppliers, experiments, settings, and audit events.
- Pydantic intake validation, CSV product import, explainable unit economics, persisted and audited scoring-weight configuration, and audited status changes.
- Streamlit pages for all requested dashboard areas.
- Fictional seed command, migration framework, tests, Ruff/mypy/pre-commit configuration, and GitHub Actions quality workflow.
- Project documentation covering architecture, data, scoring, validation, security, and roadmap.
- Requirement-level Phase 1 acceptance review in `ACCEPTANCE_REPORT_PHASE_1.md`.
- Versioned product editing with field-level history, optimistic concurrency, comparison, and rollback-as-new-version.
- Opportunity Vault with rapid entry, `Things That Shouldn't Be True`, preserved conversion links, and audits.
- Evidence-aware Research Workbench with versioned sections, completeness/gap/staleness/contradiction checks, and Markdown/JSON exports.
- Deterministic recommendation briefs with internal citations, uncertainty, economics, reversal conditions, and budget gates.
- Alembic-only startup enforcement and isolated upgrade/downgrade migration coverage.
- Manual, CSV, and JSON review intake with preview, field mapping, dry-run validation, partial-import reporting, templates, immutable batches, and source hashes.
- Original-text preservation, layered duplicate detection, auditable manual duplicate decisions, a centralized taxonomy, deterministic classification, versioned human correction/restoration, and scoped reclassification.
- Product/batch review analytics, quality warnings, attention queues, Markdown/JSON reports, and clearly fictional multi-product demonstration reviews.
- Git repository initialized with synchronized `main`; Work Order 003 is developed through logical commits on a feature branch.

## Current architecture

Streamlit is a thin presentation layer over Pydantic contracts, repository functions, and deterministic domain services. SQLAlchemy 2 maps to SQLite through a configurable `DATABASE_URL`; Alembic owns schema evolution. Evidence, product edits, research, review imports, classifications, and score calculations preserve historical rows. Important mutations create audit rows in the same transaction.

## Open issues

- Experiment updates still need a versioned edit workflow; product editing is now versioned with field-level history and rollback-as-new-version.
- Authentication and per-user authorization are not implemented; the application is intended for a trusted local operator.
- Automated tests cover critical deterministic services and migration lifecycle; the verified suite has 35 tests and 58% aggregate statement coverage. Streamlit has an application and Review Mining page smoke test, but form interactions are not exhaustively automated.
- Mission Control/action queue, provider adapters, and Profit Sprint are not implemented (Work Order 002 Phases G-I).
- Evidence corrections cannot yet link a superseded record.
- Product editing currently exposes core identity, research notes, and every financial assumption; remaining descriptive product fields need the same form treatment.
- Review source authorization is asserted by the operator, not independently verified. The rule classifier is English-oriented and cannot resolve complex language reliably.
- Review immutability guards protect ORM application paths, not administrators or direct bulk SQL; formal retention/deletion operations remain open.

## Immediate next actions

1. Perform the Work Order 003 manual acceptance test with fictional data and review the feature branch.
2. Build lean Mission Control and an actionable, audited action queue from actual project state.
3. Reuse aggregate review themes in the Research Workbench without treating individual reviews as representative.

## Commands

```powershell
python -m pip install -e ".[dev]"
alembic upgrade head
streamlit run src/ai_commerce_engine/app.py
pytest
ruff check .
ruff format --check .
mypy src
```

## Important decisions

- Money is calculated with `Decimal` and persisted as fixed precision `NUMERIC`.
- Evidence is append-only in application workflows; corrections are new observations with explanatory notes.
- Scores are snapshots containing components, weights, penalties, rationale, actor, and timestamp.
- Consequential status changes require a reason and create history plus audit rows.
- All outside actions remain manual and require human approval.
- Work Order 003 decisions: uploaded file bytes are not retained; import batches and original review bodies are immutable in ORM paths; duplicates remain inspectable; fuzzy matching requires same source/rating/non-missing date and 96% similarity; reclassification preserves human-added themes; all analytics are explicitly sample-scoped.
- Verification on 2026-07-13: Ruff and format clean, mypy clean across 31 source files, 35 tests passing at 58% aggregate statement coverage, Alembic upgrade and schema-drift checks clean, import smoke clean, Review Mining page smoke clean, fictional seed idempotent, and diff whitespace check clean.

## Data-source limitations

No live marketplace, search, social, supplier, advertising, or sales source is connected. Data is user-entered, imported from a user-selected CSV/JSON file, or explicitly fictional seed data. The system does not establish that a source is authorized, current, complete, representative, or accurate; provenance, sample composition, warnings, and confidence must be reviewed by a human.

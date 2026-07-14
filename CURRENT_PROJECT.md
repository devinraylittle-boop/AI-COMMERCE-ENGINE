# Current Project

## Current phase

Work Order 002 - evidence-workflow hardening. Phase 1 was accepted with blocking revisions; Phases B-E now resolve the version-integrity and evidence-gating blockers. Phases F-I remain open.

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

## Current architecture

Streamlit is a thin presentation layer over Pydantic contracts, repository functions, and deterministic domain services. SQLAlchemy 2 maps to SQLite through a configurable `DATABASE_URL`; Alembic owns schema evolution. Evidence and score calculations create new historical rows. Important mutations create audit rows in the same transaction.

## Open issues

- Experiment updates still need a versioned edit workflow; product editing is now versioned with field-level history and rollback-as-new-version.
- Authentication and per-user authorization are not implemented; the application is intended for a trusted local operator.
- Automated tests cover the critical deterministic services and migration lifecycle but not Streamlit rendering; the verified suite has 20 tests and 54% aggregate statement coverage.
- The workspace is not a Git repository, so branch, diff, and commit provenance are unavailable.
- Review mining, Mission Control/action queue, provider adapters, and Profit Sprint are not implemented (Work Order 002 Phases F-I).
- Evidence corrections cannot yet link a superseded record.
- Product editing currently exposes core identity, research notes, and every financial assumption; remaining descriptive product fields need the same form treatment.

## Immediate next actions

1. Implement the compliant review-mining foundation with import batches, deduplication, original-text preservation, and versioned human corrections.
2. Reuse review themes in the Research Workbench without treating a single review as representative.
3. Build Mission Control only after review and action-queue primitives exist.

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
- Verification on 2026-07-13: Ruff and format clean, mypy clean across 26 source files, 20 tests passing at 54% aggregate statement coverage, Alembic upgrade and schema drift check clean, and application/service import smoke tests passing.

## Data-source limitations

No live marketplace, search, social, supplier, advertising, or sales source is connected. All data is user-entered, imported from a user-selected CSV, or explicitly fictional seed data. The system does not establish that a source is authorized, current, complete, representative, or accurate; provenance and confidence must be recorded and reviewed by a human.

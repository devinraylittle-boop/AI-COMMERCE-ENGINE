# Current Project

## Current phase

Company 001 — Comparative Laboratory Selection 001 complete. All public outreach is frozen. A symmetric internal desk cycle compared Dogs / Trust-Mediated Care, Coffee / Expertise Ladder, and Home Organization / Friction Removal by expected Learning ROI. Home Organization advances to the first full Problem Discovery cycle; Coffee remains first reserve and Dogs is deferred. This selects a learning laboratory only—not a market, validated mechanism, problem, solution, product, or offer. No product test, community contact, behavioral-profile architecture, inventory, payment, affiliate action, advertising, or new application page is authorized.

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
- Sprint 001 market elimination with three finalist contexts and separate profit, learning, and automation rankings.
- Three machine-readable Mechanism Cards for Trust-Mediated Care, Expertise Ladder, and Friction Removal, with validation that prevents premature earned instructions.
- Operation First Principle collection protocol, preregistered falsification gates, interview script, and $75 aggregate research ceiling.
- Evidence Supply Chain operating model with five complementary evidence classes, source qualification, collection cadence, mechanism-specific supply maps, release gates, and reusable source/interview records.
- Working causal-claim doctrine and future claim-blinding direction, intentionally documented without changing Mechanism Cards or adding architecture.
- Consumer Behavior Intelligence v0.1: research synthesis, decision journey, trigger/barrier taxonomy, signal-to-state uncertainty map, causal measurement roadmap, privacy limits, three candidate-context applications, and ten prioritized working hypotheses.
- Human Decision Intelligence v0.2: Decision Quality per Customer, Customer Relationship Value, direct regret measurement, and Reality-as-governance doctrine.
- Archived and explicitly vetoed Company 001 Offer 001 before any exposure, preserving it only as a candidate laboratory and cultural correction.
- Preregistered Problem Discovery 001 with six evidence strata, neutral episode coding, a consequence scale, source-balanced ranking, a top-five admission gate, moderator-permission language, and an empty minimal evidence log.
- Froze public outreach and preserved the coffee-specific Problem Discovery protocol as a reserve rather than an active experiment.
- Completed Comparative Laboratory Selection 001 using the same seven claim slots and an ordinal dominance comparison; advanced Home Organization, reserved Coffee, and deferred Dogs with explicit reversal conditions.
- Defined Learning ROI through preregistered Earned Knowledge Units per time, cash, and attention, plus later reuse yield; added the first ledger without inventing a scalar learning score.

## Current architecture

Streamlit is a thin presentation layer over Pydantic contracts, repository functions, and deterministic domain services. SQLAlchemy 2 maps to SQLite through a configurable `DATABASE_URL`; Alembic owns schema evolution. Evidence, product edits, research, review imports, classifications, and score calculations preserve historical rows. Important mutations create audit rows in the same transaction.

## Open issues

- Experiment updates still need a versioned edit workflow; product editing is now versioned with field-level history and rollback-as-new-version.
- Authentication and per-user authorization are not implemented; the application is intended for a trusted local operator.
- Automated tests cover critical deterministic services and migration lifecycle; the verified suite has 39 tests and 59% aggregate statement coverage. Streamlit has an application and Review Mining page smoke test, but form interactions are not exhaustively automated.
- Mission Control/action queue, provider adapters, and Profit Sprint are not implemented (Work Order 002 Phases G-I).
- Evidence corrections cannot yet link a superseded record.
- Product editing currently exposes core identity, research notes, and every financial assumption; remaining descriptive product fields need the same form treatment.
- Review source authorization is asserted by the operator, not independently verified. The rule classifier is English-oriented and cannot resolve complex language reliably.
- Review immutability guards protect ORM application paths, not administrators or direct bulk SQL; formal retention/deletion operations remain open.

## Immediate next actions

1. Keep all public outreach frozen.
2. Adapt the common Problem Discovery fields to Home Organization without naming products or assuming Friction Removal is correct.
3. Predeclare room/context boundaries and exclude mold, pests, structural installation, hoarding disorder, and other cases requiring qualified professional help.
4. Qualify two existing customer-language sources, the YouGov market source, two expert/guide sources, and one product-failure source before extraction.
5. Collect and audit a small internal calibration sample; authorize later public permission-seeking only if coding can distinguish possessions/motivation, routine, fit/access, durability, and environmental failure reliably.

No major architecture is authorized until reality exposes evidence ACE cannot represent reliably and a documented process cannot repair the gap.

## Commands

```powershell
python -m pip install -e ".[dev]"
alembic upgrade head
streamlit run src/ai_commerce_engine/app.py
ai-commerce-mechanisms mechanisms --total-budget-ceiling 75
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
- Verification on 2026-07-14: Ruff and format clean, mypy clean across 34 source files, 39 tests passing at 59% aggregate statement coverage, all three Mechanism Cards valid under the $75 aggregate ceiling, and diff whitespace clean. Existing migration lifecycle, import, Review Mining smoke, and fictional-seed tests remain in the passing suite.

## Data-source limitations

No live marketplace, search, social, supplier, advertising, or sales source is connected. Data is user-entered, imported from a user-selected CSV/JSON file, or explicitly fictional seed data. The system does not establish that a source is authorized, current, complete, representative, or accurate; provenance, sample composition, warnings, and confidence must be reviewed by a human.

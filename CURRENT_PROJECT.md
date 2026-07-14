# Current Project

## Current phase

Company 001 — Home Organization behavioral evidence. Interviews are no longer a dependency. A bounded public-source desk sprint compared ten narrow problem areas and selected under-sink fit uncertainty as the best candidate for a separately authorized first commercial exposure, with pantry consequence-triggered containment and closet compatibility as reserves. All public outreach and commercial exposure remain frozen. The result is a test-priority decision—not proof of demand, profitability, product need, or mechanism viability. No product test, community contact, behavioral-profile architecture, inventory, payment, affiliate action, advertising, or new application page is authorized.

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
- Added Home Organization Failure Mode Map v0.1 covering volume/inflow, system design, maintenance, household governance, time/context, product failure, hazards, human access, definition mismatch, and False Problem as an evidence-dependent overlay.
- Added 20 synthetic open-training cases and provisional answers, explicit uncertainty, safety escalation, and gates that forbid product prescription.
- Corrected the calibration governance after recognizing that public reference exposure prevents a blind test: separated open training from formal calibration; defined Case Steward, Packet Custodian, Coder A/B, Arbiter, and Mechanism Owner roles; excluded prior designers and reference viewers from coder roles; and added eligibility, custody, anonymization, arbitration, and fresh-AI controls.
- Completed a manual Home Organization Behavioral Signal Sprint across pantry, garage, under-sink, closet, refrigerator, bathroom, laundry, small-apartment, toy, and RV contexts; preserved 34 source-grounded observations; ranked six dimensions separately; selected three finalists; and identified refrigerator aesthetics, toy storage, and garage systems as the most dangerous current false positives.
- Placed Learning ROI in observation-only status until multiple experiments reveal how the metric behaves and can be gamed.

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
2. Review the Behavioral Signal Sprint's observation/inference boundaries and decide whether under-sink fit earns one external commercial exposure.
3. Before any exposure, obtain a durable trend/ad snapshot, a systematically sampled authorized review corpus, supplier/fulfillment estimates, and a legal check on refundable-reservation language.
4. If exposure is authorized, freeze the under-sink claim and run only the disposable $25-or-100-qualified-visit test; do not build reusable architecture.
5. Keep diagnostic calibration pending until eligible external roles and an unseen sealed case packet exist; neither the founder nor participating Codex architect may serve as an independent coder.

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

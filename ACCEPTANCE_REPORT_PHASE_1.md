# Phase 1 Acceptance Report

Date: 2026-07-13  
Decision: **Accepted with blocking revisions before real product validation**

## Verification baseline

| Check | Result |
|---|---|
| Ruff | Pass |
| Ruff formatting | Pass |
| mypy | Pass, 22 source files |
| pytest | Pass, 10 tests, 49% aggregate coverage |
| Alembic upgrade | Pass |
| Alembic schema drift | Pass |
| Application import | Pass |

The directory is not a Git worktree. Branch, local diff, and commit provenance cannot be verified.

## Requirement review

| Phase 1 requirement | Result | Evidence and findings |
|---|---|---|
| Product intake | **Partial pass** | `ProductCreate`, `create_product`, and `product_pipeline` cover the requested fields and CSV intake. There is no edit/version workflow, duplicate policy, import batch model, or template export. |
| Evidence model | **Partial pass** | `Evidence` stores source, observation, numeric value, context, collection metadata, confidence, and provenance. UI behavior is append-only, but immutability is not enforced below the UI and corrections cannot reference superseded records. |
| Unit economics | **Pass with revisions** | `services/economics.py` uses `Decimal`, exposes cost layers, contribution margin, break-even CAC/ROAS, and order-volume profit. Tests cover the primary path and negative values. Missing sensitivity/downside scenarios and persisted assumption versions are blocking for real decisions. |
| Product scoring | **Partial pass** | Default weights and all penalties are present; snapshots preserve components, weights, penalties, and rationale. Component scores are manually asserted and not tied to evidence sufficiency, so a high score can conceal unsupported conclusions. Score persistence lacks direct tests. |
| Decision pipeline | **Pass with revisions** | All statuses and required history fields exist; changes are audited. The service accepts any status-to-status movement and supporting evidence is free text rather than a structured link. |
| Dashboard | **Partial pass** | All requested navigation destinations exist and render actual database data. Product editing, evidence-aware scoring, metric definitions, accessibility testing, and page-level tests are missing. |
| Validation experiments | **Partial pass** | Test design and funnel/financial results are stored; derived metrics are deterministic and no spend is automated. Updates, threshold definitions, version history, and budget enforcement are absent. |
| Auditability | **Partial pass** | Product creation, evidence append, scores, settings, status, suppliers, experiments, imports, and unhandled UI errors create audit rows. Audit behavior is not centralized, and several future mutation paths are uncovered. |
| Documentation | **Pass with revisions** | All original documents exist and describe the architecture and limitations. Phase 1 acceptance was previously asserted without a requirement-level audit. Some rendered text shows encoding artifacts in the local shell. |
| Quality requirements | **Partial pass** | Typed modules, migrations, validation, logging, tests, `.env.example`, fictional seed labels, pre-commit, and CI exist. Aggregate coverage is 49%; Streamlit is untested, startup calls `create_all`, and no PostgreSQL integration test exists. |

## Known defects and concerns

### Blocking before real validation

1. Product and financial assumptions can be created but not safely edited or versioned.
2. Scores do not expose evidence completeness or unsupported components.
3. No guided research record proves that minimum diligence was completed.
4. CSV imports lack duplicate detection and import-batch provenance.
5. The application has no authentication and must remain on a trusted local machine.

### Architecture and data integrity

- `Base.metadata.create_all()` in `app.py` competes with Alembic as schema authority.
- Evidence append-only behavior is a convention; repository APIs do not explicitly reject update/delete.
- Controlled vocabulary fields use unrestricted strings at the database boundary.
- SQLite timezone behavior and the PostgreSQL migration path are not integration-tested.
- Audit writes depend on each service remembering to call `record_audit`.

### Security

- Appropriate for a trusted local operator only; public exposure would be unsafe.
- CSV size, formula-injection-on-export, attachment handling, retention, and backup/restore policies are not implemented.
- URLs are stored without fetching, which is safe now; future adapters require SSRF and authorization controls.

### UX

- Forms are long and lack progressive save/draft behavior.
- Metrics generally lack inline definitions.
- Empty states exist, but the system cannot distinguish “zero” from “not researched” consistently.
- There is no visible product version history, comparison, research completeness, or explicit “not enough evidence” state.

### Missing test coverage

- Product import success/failure/duplicates and transaction behavior
- Score snapshot persistence and custom-weight behavior
- Audit completeness across every mutation
- Streamlit page rendering and form validation
- Migration upgrade/downgrade against an empty database in pytest
- PostgreSQL compatibility
- Concurrent edits, stale versions, and historical rollback

## Recommendation

**Accepted with revisions.** The foundation is coherent and suitable for extension, but it is not yet safe to use for selecting a real product. Versioned assumptions and evidence-aware research gates are blocking revisions. Opportunity capture is a valuable next layer only after version integrity is established.

## Nonblocking improvements

- Add named scoring profiles and structured evidence links.
- Add backup/restore and retention operations.
- Add database constraints for controlled vocabularies.
- Add accessible help text and responsive page-level acceptance tests.
- Add PostgreSQL CI after local workflows stabilize.

## Subsequent remediation note

This report preserves the Phase 1 point-in-time audit. Work Orders 002 and 003 subsequently added product/assumption versioning, evidence-aware research gates, migration lifecycle tests, Git history, and compliant review-import provenance and duplicate handling. Authentication, PostgreSQL integration testing, evidence supersession, and Streamlit page-level automation remain open.

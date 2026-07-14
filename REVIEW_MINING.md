# Review Mining

## Purpose and compliance boundary

Review Mining analyzes review data that the operator is authorized to provide. It does not fetch, crawl, authenticate to, or scrape a marketplace. A stored source URL is provenance only; the application never requests it. Results describe the imported sample and must not be presented as market prevalence or proof of demand.

Original review bodies, committed import batches, classification history, and audit events are retained for traceability. Do not import personal data that is unnecessary for product research. The trusted local operator remains responsible for source terms, export authorization, retention, and deletion obligations.

## Supported intake

- Manual entry
- UTF-8 or UTF-8-with-BOM CSV
- UTF-8 JSON containing either a list of objects or `{"reviews": [...]}`

Templates are available in `templates/review_import_template.csv` and `templates/review_import_template.json` and from the Review Mining page.

Every intake requires product association, source platform, review body, provenance, and fictional-data status. Rating is optional; when supplied it cannot exceed its rating scale. Optional fields include external ID, URL, reviewer display name, title, date, verified-purchase status, helpful votes, geography, language, and variant/SKU.

### Field mapping and dry run

The file UI previews the first rows and maps input columns to canonical fields. Dry-run validation parses every row and reports row numbers and field errors without creating a batch or review. Committing stores valid rows and preserves invalid-row counts and errors in the immutable batch summary. Raw uploaded files are not retained; filename, SHA-256 hash, mapping metadata, and source metadata are retained.

## Original content and immutable batches

`original_review_body` is stored exactly as validated, including case and whitespace. A separate normalized value supports matching and classification. ORM guards reject changes to original text and reject updates or deletion of import batches. Application services do not expose deletion of imported reviews.

## Duplicate logic

Detection runs in this order:

1. Same product, source platform, and external review ID: `exact_duplicate`.
2. Same product and SHA-256 fingerprint of Unicode-normalized, case-folded, whitespace-collapsed text: `exact_duplicate`, including cross-source copies.
3. Same product, source, rating, and non-missing review date plus at least 96% normalized-text similarity: `probable_duplicate`.
4. Otherwise: `unique`.

Duplicates are stored, labeled, and linked; they are never silently discarded. Missing dates cannot trigger fuzzy matching. The conservative similarity rule can miss paraphrases and syndication, and exact normalized text can still represent legitimate repeated short statements. Human confirmation or rejection records the prior and new status, actor, reason, and canonical link in the audit log.

## Theme taxonomy

The centralized taxonomy is defined in `services/review_taxonomy.py`, not scattered through the UI. It contains 20 top-level themes: Complaint, Loved feature, Requested improvement, Failure mode, Durability, Packaging, Shipping, Misleading claim, Unexpected use, Buyer type, Return reason, Value perception, Sizing or fit, Ease of use, Performance, Quality, Customer service, Safety concern, Missing accessory, and Compatibility.

Each definition includes inclusion phrases, exclusion examples, priority, optional severity, positive/negative context, and possible effects on risk, trust, fulfillment, positioning, or product improvement. Classification storage supports optional subthemes even though the initial deterministic rules assign top-level themes.

## Deterministic classification

Classifier version `rules-1.0` uses centralized phrase rules, word boundaries, limited preceding-word negation, rating context, priority, and minimum confidence. Every assignment stores its theme, confidence, matched phrase, method, and human-review state. The rule engine is explainable but cannot reliably resolve sarcasm, complex negation, multilingual nuance, implied sentiment, or context outside the review.

Classification creates a new version for one or many selected review IDs and can target a batch or product. Reclassification never edits an earlier version. Human-added themes are carried into deterministic reclassification as `human-preserved` assignments unless a current rule already identifies the same theme.

`ReviewClassifier` is the extension interface for a future authorized model-assisted classifier. Any future implementation must retain version identifiers, matched evidence, confidence limitations, cost, authorization, and human correction; it must not become a hidden dependency for core operation.

## Human correction

The Classification Review tab displays immutable source text, active themes, evidence phrases, confidence, and all versions. A reviewer can add, remove, or replace themes with a required reason and optional supporting note. The resulting complete interpretation becomes a new active version; the prior version becomes inactive but remains stored. Restoring a prior interpretation also creates a new version. Audits include previous and new version numbers and theme sets.

Attention filters identify no-theme, low-confidence, contradictory positive/complaint, safety, misleading-claim, high-severity, probable-duplicate, and manually flagged reviews.

## Analytics definitions

- `Total imported`: accepted stored reviews plus row rejections recorded by batches in scope.
- `Accepted`: stored review records, including labeled duplicate candidates.
- `Duplicate count`: exact, probable, or manually confirmed duplicate records.
- `Classified`: reviews with an active classification version.
- `Theme count`: number of reviews in scope whose active version contains the theme.
- `Theme percentage`: percentage of reviews in this imported sample containing the theme. It is not market prevalence.
- `Human corrections`: human classification versions, not distinct reviews.

Product and batch scopes include source, rating, review-date, verified-purchase, fictional-data, theme-by-rating, theme-by-source, and classification-version distributions. Warnings cover samples under 20, source concentration over 80%, newest dated review older than one year, more than 25% missing ratings, more than 25% fictional records, duplicate rates over 20%, average confidence below 70%, and unclassified records.

## Reports and exports

Product and import-batch reports export Markdown and JSON. Both include scope, generation timestamp, sample notice, size, source composition, time range, data-quality warnings, rating distribution, theme summaries, requested improvements, failure/durability/packaging/shipping/claim/use/buyer/return/value observations, possible product and positioning opportunities, unknowns, further-research recommendations, batch provenance, hashes, and fictional labels.

Spreadsheet consumers must treat exported text as untrusted content. The application does not currently generate Excel files or sanitize review text for spreadsheet formula execution.

## Known limitations

- No source authorization can be inferred from a filename or user assertion.
- No raw file retention, attachment storage, malware scanning, or automated source deletion workflow exists.
- Exact-text fingerprints are deterministic, not semantic.
- The initial classifier is English-oriented and rule-based.
- Reviewer display names may be personal data and should be omitted unless necessary and lawful.
- SQLite is the tested local database; PostgreSQL-compatible types are used, but PostgreSQL integration testing remains open.
- The local application has no authentication and must not be publicly exposed.

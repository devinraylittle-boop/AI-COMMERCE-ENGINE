# Data Dictionary

All timestamps are UTC-aware. Money uses `NUMERIC(12,2)` unless noted. Nullable fields mean “not recorded,” not zero and not proven absent.

## products

Core opportunity record. Includes identity and context (`name`, URL, source, category, customer, problem); editable economics assumptions (price, discounts, product, shipping, packaging, processing, platform, refund, chargeback, CAC); supplier facts; research text; current pipeline `status`; `is_fictional`; and created/updated timestamps.

## evidence

Append-only research observations. Required: `product_id`, `evidence_type`, `source`, `observation`, `collected_at`, `collection_method`, `confidence_level`, and `provenance`. Optional: source URL, numeric value (`NUMERIC(18,4)`), unit, geography, time period, and notes. Provenance is Observed, Estimated, Inferred, or User-entered. Confidence is Low, Medium, or High.

## score_snapshots

Immutable scoring result with `base_score`, `penalty_total`, `final_score`, JSON component/weight/penalty maps, rationale, actor, and timestamp. This table preserves the explanation used at decision time.

## status_history

One row per pipeline movement: previous/new status, timestamp, reason, actor, supporting evidence reference/text, and next action.

## supplier_offers

Comparable supplier quote: name, location, unit/shipping cost, lead time, MOQ, evidence quality, notes, and capture timestamp. It is not an order or authorization to contact the supplier.

## validation_experiments

Hypothesis and test design (type, audience, channel, offer, price, creative, budget ceiling, dates), funnel observations (visits through purchases), financial results, derived conversion/CAC/contribution profit, lessons, result, and decision.

## audit_log

Mutation trace: event type, entity type/id, actor, action, before/after JSON, details, and timestamp. Event types include data change, score change, assumption change, status change, import, and error.

## app_settings

JSON-valued configuration keyed by string, with description, updater, and timestamp. Intended for versioned operational settings such as scoring weights.

## product_versions and product_field_changes

`product_versions` stores a complete validated editable-product snapshot, sequential version, base version, actor, reason, source, evidence reference, provenance, and timestamp. `product_field_changes` records each changed field with previous and new JSON values plus the same decision metadata. Rollback creates another version.

## opportunities and links

The raw Opportunity Vault record includes observation, hypothesis, source context, confidence, status, tags, follow-up questions, and the `things_that_shouldnt_be_true` flag. Link tables preserve many-to-many relationships to products and evidence without deleting the original opportunity.

## research_entries

Append-only, per-section research versions. Each row stores product, one of 22 section keys, sequential version, content, internal evidence IDs, provenance, actor, reason, and timestamp.

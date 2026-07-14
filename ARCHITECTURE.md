# Architecture

## Shape

```text
Streamlit UI
  → Pydantic validation
  → repositories / deterministic services
  → SQLAlchemy unit of work
  → SQLite (PostgreSQL-ready DATABASE_URL)
```

`src/ai_commerce_engine/ui` renders pages and collects inputs. `schemas` validates external values. `repositories` handles persistence. `services` owns calculations, audit events, score snapshots, experiment metrics, and workflow rules. `models` is the storage model. The dependency direction points inward; domain calculations do not import Streamlit or SQLAlchemy.

Work Order 002 adds immutable `ProductVersion` and `ResearchEntry` streams. The `products` row remains a current projection for fast UI reads; optimistic concurrency requires edits to name the version on which they were based. Recommendation generation implements a `RecommendationGenerator` protocol and a deterministic implementation, leaving a narrow extension point for future model-assisted rendering without making a model a runtime dependency.

## Reliability and auditability

Evidence, scores, and status changes are historical records. Business mutations and their audit events share a transaction. SQLite foreign keys are enabled. Pydantic rejects malformed intake; service functions reject invalid ranges and impossible negative inputs. UI exceptions are logged, rolled back, and shown without pretending the operation succeeded.

## Migration path

Alembic migrations are the schema contract. `DATABASE_URL` isolates engine selection. Fixed-precision numeric fields, explicit foreign keys, and portable JSON avoid SQLite-specific business logic. Application and seed startup now fail with an actionable message when migrations are missing; they do not create schema implicitly. Before PostgreSQL adoption, add integration tests against the target version.

## Trust boundaries

The operator and imported CSVs are untrusted inputs. External URLs are stored as references; the application does not fetch them. There are no external write integrations. Local database and environment configuration are trusted deployment assets and must be access-controlled by the operator.

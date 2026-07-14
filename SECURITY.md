# Security

## Phase 1 posture

This is a trusted-user local application with no authentication, public API, supplier ordering, storefront publishing, ad-spend connection, or customer-facing AI. Do not expose it directly to the public internet.

## Controls

- Secrets belong in `.env`, which is ignored; `.env.example` contains only safe defaults.
- Pydantic validates structured input; SQLAlchemy parameterizes database queries.
- Source URLs are stored but not fetched, limiting server-side request risks.
- SQLite foreign keys are enabled and mutations use transactions.
- Errors are logged and transactions roll back on failure.
- Dependencies are bounded and CI runs lint, types, and tests.
- Application startup requires the Alembic-managed schema instead of silently creating tables.
- Version and research history are append-only through the implemented service interfaces.

## Operator responsibilities

Restrict filesystem access to the database and `.env`; back up and encrypt sensitive research; scan user-provided CSVs; minimize personal data; verify source/platform terms; and rotate any secret that is exposed. Before multi-user or hosted deployment, add identity, authorization, CSRF/session controls, encrypted transport, structured security logging, backup/restore testing, retention controls, dependency scanning, and a threat model.

Future review/social adapters must implement source-specific deletion and retention duties. Attachment references are text only; file upload/storage is not implemented and must receive path, malware, content-type, size, and access-control review before introduction.

Review files are parsed in memory and are not retained. Only the filename, SHA-256 hash, mapping/source metadata, validated records, and row-level counts/errors remain. Review text and reviewer display names are untrusted and may contain personal data, malicious spreadsheet formulas, or copyrighted content. Import only authorized, necessary data; keep the application local; do not render review HTML; and do not copy exported review text into formula-capable spreadsheets without sanitization.

Import batches and original review bodies have ORM-level immutability guards. These protect normal application paths, not a database administrator or direct bulk SQL. Database access, backups, and future retention/deletion tooling remain security boundaries.

Report security issues privately to the repository owner. Do not include secrets or personal data in issue reports.

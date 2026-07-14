# Little Built — Storefront Zero

Private, non-indexed buying-experience prototype for Company 001.

## Purpose

Storefront Zero tests whether the working Little Built promise and three candidate products form a coherent, trustworthy company before supplier outreach. It accepts no orders, collects no customer data, and presents no unverified price, inventory, review, supplier, or performance claim.

## Experience

- Homepage
- Candidate collection
- Three candidate product pages
- About
- FAQ
- Draft shipping and returns principles
- Recommendation standard

## Local use

```powershell
pnpm install
pnpm run dev
```

Quality checks:

```powershell
pnpm run build
node --test tests\*.test.mjs
pnpm run lint
```

The Delete Test removes one product and then two from the shared catalog model. The brand promise and decision standard must remain unchanged in both cases.

## Boundaries

- Private and `noindex`.
- Checkout is intentionally disabled.
- Product images are abstract concept forms, not selected SKUs.
- “Little Built” is a working brand hypothesis.
- Supplier outreach remains unauthorized.

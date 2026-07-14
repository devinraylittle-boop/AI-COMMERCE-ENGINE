# Data Source Register

Status: preliminary architecture register; no live provider adapter is implemented.

This file tracks possible technical providers. The operational source-qualification, trust, cadence, evidence-class, and retirement process is defined in `research/EVIDENCE_SUPPLY_CHAIN.md`. Listing a provider here does not qualify it for decision use.

| Source | Signal | Access and authorization | Likely cost | Constraints and limitations | Recommended sequence |
|---|---|---|---|---|---|
| Manual entry | Any | Human records source, method, date, confidence, and provenance | No provider fee | Slow; transcription risk; source rights still apply | **1 — implemented through current evidence forms** |
| User-provided CSV/JSON | Any | User must have a lawful export and permission to use it | No application fee; source may charge | Preserve import batch and raw file hash; prevent formula injection and duplicates | **2 — build generic adapters next** |
| eBay Browse API | Marketplace listings | eBay developer credentials and OAuth/application token | Verify before approval | API license, marketplace coverage, quotas, and listing data are not proof of sales | 3 — candidate pilot after terms review |
| Google Ads keyword planning | Search-demand proxy | Google Ads account, developer token, OAuth, eligible account access | Verify; no paid infrastructure approved | Forecasts/keyword metrics are advertising estimates, not sales; access level and quotas apply | 4 — candidate after manual search protocol |
| Amazon SP-API | Seller/vendor operational data | Selling partner authorization through Login with Amazon | Verify; seller account may be required | Intended for authorized seller/vendor data, not unrestricted market mining; sensitive-data controls required | Defer until the business has authorized seller data |
| Reddit Data API | Social/customer-language signal | OAuth client and policy-compliant approved use | Commercial use may require a separate agreement; price unknown | Current free eligible access is rate limited; deletion/retention duties apply; never treat posts as representative demand | Defer pending written commercial-use determination |
| Supplier exports | Supplier quotes and terms | User-provided quote/export or future authorized supplier API | Usually no API fee; commercial relationship may apply | Quote freshness, identity, Incoterms, MOQ, quality, and performance require independent verification | Manual/CSV first |
| Review exports | Complaints and buyer language | User-provided lawful CSV/JSON, manual entry, or future authorized marketplace API | Source-dependent | Preserve original text; respect personal-data and deletion requirements; sample bias is material | Manual/CSV/JSON foundation implemented in Work Order 003 |
| Meta/TikTok/other social APIs | Social signal | Platform app review, tokens, scopes, and approved use case | Unknown | Terms and scopes change; engagement is not demand; no scraping fallback | Defer until a narrow approved use case exists |

## Adapter contract required before activation

Every future adapter must report provider, collection method, authorization, rate limits, terms constraints, freshness, coverage, confidence limitations, cost, last success, and errors. A disabled or unavailable adapter must return an explicit unavailable state rather than synthetic data.

## Current source notes

- [eBay Browse API documentation](https://www.developer.ebay.com/api-docs/buy/static/api-browse.html)
- [Amazon SP-API overview](https://sell.amazon.com/developers?lang=en-US) and [authorization](https://developer-docs.amazon/sp-api/lang-en_US/docs/authorizing-selling-partner-api-applications)
- [Reddit Data API guidance](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki) and [Data API Terms](https://redditinc.com/policies/data-api-terms)

Costs and access conditions must be reverified immediately before implementation or approval. No source in this register authorizes scraping or paid access.

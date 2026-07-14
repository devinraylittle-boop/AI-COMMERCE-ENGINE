# Company 001 Behavioral Hypotheses v0.1

**Status:** working hypotheses, not earned instructions

**Budget principle:** validation spending is a ceiling, not a target

**Primary outcome:** a high-quality customer decision; for transactions, a kept, satisfactory, contribution-positive purchase

**Operating rule:** no test may depend on deception, pressure, sensitive profiling, or obstructed choice.

## Evidence standard

Prototype tasks may test comprehension and expose confusion. They cannot establish willingness to pay. A hypothesis becomes commercially supported only after randomized behavior from eligible real customers, the applicable cancellation/return window, contribution accounting, and at least one replication or strong out-of-sample confirmation.

## Priority queue

| # | Behavioral hypothesis | Cheapest first test | Behavioral primary outcome | Customer/business guardrails | Reversal condition |
|---:|---|---|---|---|---|
| 1 | Showing total delivered cost before checkout reduces price/shipping surprise and increases qualified checkout completion. | Two static product/checkout prototypes; randomized comprehension task, then live A/B when traffic exists. | correct total-cost recall; later kept conversion | gross margin, cancellation, return, complaints | comprehension or kept conversion worsens |
| 2 | A product-specific fit/compatibility checklist increases kept purchases by resolving consequential uncertainty. | Prototype five-question checklist for one candidate; observe task accuracy before live randomization. | correct fit choice; later kept conversion | returns, support contacts, exclusion accuracy | checklist creates false confidence or more returns |
| 3 | “Who should not buy this” improves decision quality enough to offset any immediate conversion loss. | Add a concise exclusion panel to one concept test. | unsuitable-choice avoidance; later kept contribution | total conversion, trust, returns | qualified buyers misunderstand and leave without downstream benefit |
| 4 | A balanced review-theme summary organized by use case is more useful than star average plus cherry-picked quotes. | Use authorized/synthetic-for-UX review sets; randomize presentation, ask evidence-based choice questions. | decision accuracy and uncertainty reduction | time, representativeness, no hidden negative themes | users become less accurate or falsely certain |
| 5 | Showing a cheaper sufficient alternative increases trust and long-run value among customers who do not need the premium option. | Randomized prototype with explicit trade-off matrix. | correct value-tier selection; revisit/opt-in | contribution, refunds, perceived manipulation | merely cannibalizes fit buyers with no trust/retention benefit |
| 6 | Environment/use-case questions outperform broad demographic personalization for product relevance. | Compare recommendation from 3 contextual questions against a generic shortlist. | recommendation acceptance and correct fit | privacy comfort, completion, no sensitive inference | contextual questions add burden without better outcomes |
| 7 | Compatibility confirmation immediately before cart reduces preventable returns and support demand. | Add a clear compatibility assertion/check to a prototype, then eligible live A/B. | compatibility errors; later return reason | cart completion, false negatives, support | valid buyers are blocked or returns do not improve |
| 8 | A post-purchase setup guide improves successful use and reduces avoidable returns. | Send a manually prepared guide to a randomized eligible cohort after launch. | setup completion; retained order | support contacts, unsubscribe, return rate | guide annoys customers or cannot change use outcomes |
| 9 | An opt-in reminder near the observed replenishment interval outperforms generic promotional email. | After enough real repeatable orders, randomize timing/content against no reminder or generic message. | incremental repurchase contribution | opt-out, complaint, excess return, frequency cap | lift disappears after incrementality/returns are counted |
| 10 | A capability-gap upgrade guide produces better retained upgrades than aspirational premium framing. | Prototype current-vs-upgrade capability matrix; later randomize among eligible owners. | correct upgrade/no-upgrade choice; later kept upgrade | downgrade/keep-current option use, returns, trust | premium framing wins only by creating regret or low-fit orders |
| 11 | **Deferred candidate:** a fit-qualified dosing-funnel recommendation may produce less regret than star-rating-led merchandising. | No product test is authorized. Coffee is in reserve; only if it is later activated may `company_001/labs/coffee/PROBLEM_DISCOVERY_RESERVE.md` test whether puck-preparation mess is top-five. | none until admission gate passes | product fixation and mechanism reversal | reject or archive if Coffee remains unselected or the problem does not earn top-five status |

## Recommended execution order

1. Complete Problem Discovery 001 before creating first-offer materials.
2. Select the one intervention with the largest observed decision-quality defect to repair.
3. Instrument purchase, cancellation, return, cost, and support outcomes before a live test.
4. Run only one or two live tests at a time so Company 001 can interpret them.
5. Wait through the return window before calling a winner.
6. Attempt hypotheses 8-10 only after Company 001 has actual post-purchase or repeat behavior.

## Minimal preregistration template

```text
Decision:
Population and eligibility:
Hypothesis:
Mechanism proposed:
Treatment:
Control:
Randomization unit:
Primary outcome and horizon:
Guardrails:
Minimum meaningful effect:
Sample/power plan:
Exclusions decided in advance:
Stopping rule:
Analysis method:
What result rejects the hypothesis:
Return/cancellation window end:
Owner:
```

## Explicitly rejected early tests

- false scarcity or countdowns;
- default paid additions;
- hidden or delayed shipping cost;
- identity or personality labels inferred from browsing;
- targeting emotional or financial vulnerability;
- repeated cart pressure or difficult unsubscribe;
- fabricated or selectively suppressed review evidence;
- success defined only as click-through or checkout conversion.

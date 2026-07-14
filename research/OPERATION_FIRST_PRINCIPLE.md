# Operation First Principle

**Company 001 purpose:** write ACE's first reusable commercial instruction.  
**Phase:** Reality Check
**Prime question:** How would we know?

## Scientific rule

ACE is a business laboratory. Every implementation must make experiments cheaper, conclusions more reliable, or future decisions better. A mechanism is not a product category and a successful product is not automatically a reusable play.

A mechanism is also not one indivisible hypothesis. It may contain several causal claims with different evidence and outcomes. This refinement is documented in `research/CAUSAL_CLAIMS_WORKING_NOTE.md`; it does not change the current cards or authorize Claim Card architecture.

The evidence ladder is:

1. **Hypothesis** — a falsifiable causal claim with contradictory evidence and a preregistered test.
2. **Under test** — evidence collection has begun without changing the gates.
3. **Validated instance** — the mechanism survived one commercial test under stated conditions.
4. **Validated play** — the causal mechanism survived an independent replication in a materially different context.
5. **Earned instruction** — a validated play can be expressed as a bounded, reusable instruction.

The research sequence is Question -> Causal Claim -> Evidence Plan -> Experiment -> Observation -> Replication -> Instruction. Assumptions and researcher judgment are documented but never labeled as observations.

`Rejected` means the current hypothesis failed. `Anti-play` requires repeated failure under identifiable conditions. Neither is a bad outcome; both protect capital and improve future decisions.

## What the implementation enables

The `mechanisms/` directory contains versioned, machine-readable cards. The validator rejects cards that omit supporting or contradicting evidence, a null hypothesis, preregistered survival and falsification criteria, confounders, a budget ceiling, or a replication plan. It also prevents ACE from claiming an earned instruction before a play has replicated.

This is intentionally not a database or page. Git supplies version history for the first three cards. Migration to database-backed records is justified only when concurrent editing, evidence linking, or card volume makes file storage impede an actual experiment.

Validate the current cards with:

```powershell
ai-commerce-mechanisms mechanisms --total-budget-ceiling 75
```

## The three hypotheses

| Mechanism | First context | Question being tested | Current confidence |
|---|---|---|---|
| Trust-Mediated Care | Dog Training & Enrichment | Can conservative safety and suitability guidance change selection without personalized support? | Low |
| Expertise Ladder | Home Espresso / Coffee | Can education solve a cross-context workflow problem that changes actual buying behavior? | Low |
| Friction Removal | Home Organization | Can fit certainty and maintainable systems solve a recurring household problem without custom service? | Medium |

The full preregistration, boundary conditions, evidence, and rejection rules live in each card. Criteria may not be changed after evidence collection begins without creating a new card version and explaining why.

## Reality Check collection protocol

All five evidence classes and their repeatable acquisition operations are defined in `research/EVIDENCE_SUPPLY_CHAIN.md`. Reviews and interviews are necessary inputs, not the entire evidence strategy.

### Stage 1 — authorization record

Before importing reviews, record:

- Source and owner
- How the data was obtained
- Why ACE is authorized to use it
- Terms or restrictions
- Collection date
- Whether personal identifiers were removed
- File hash and original location

Do not scrape, bypass access controls, or infer authorization from public visibility. A source URL is provenance, not permission.

### Stage 2 — review corpus

For each mechanism, collect at least 100 authorized or user-provided reviews across the three contexts named in its card and at least two independent sources.

Before analysis:

- preserve original text;
- remove no records silently;
- label exact and probable duplicates;
- record source and context distribution;
- predeclare the themes listed in the card;
- keep observed sample counts separate from market prevalence;
- log missing ratings, dates, and source concentration.

Use the existing review importer and classifier. Deterministic themes are starting labels, not conclusions. A human must review material high-severity, safety, misleading-claim, and low-confidence assignments.

### Stage 3 — customer interviews

Conduct five interviews per mechanism. Recruit people with a recent real purchase or workaround in the relevant context. Do not begin by presenting ACE, a product idea, or the mechanism.

Core questions:

1. Tell me about the last time this problem happened.
2. What did you do immediately afterward?
3. What had you already tried?
4. What did that attempt cost in money, time, waste, or frustration?
5. How did you decide what to buy or do next?
6. What information changed your decision?
7. What information was missing or untrustworthy?
8. What happened after the purchase or workaround?
9. What would have made you reject that choice?
10. May we contact you once to verify our interpretation?

Record actual behavior separately from opinions and hypothetical intent. Do not collect unnecessary personal, household, animal-health, or financial data. Photographs and measurements require explicit permission.

### Stage 4 — blinded comparison

For each mechanism, produce four tables before making a recommendation:

1. Review themes by source and context
2. Interview behaviors by participant, without identifying information
3. Supporting versus contradictory evidence
4. Every survival and falsification criterion with `met`, `not met`, or `unknown`

The scientist writing the recommendation must address the strongest disconfirming evidence, source bias, sample limits, and alternate explanations.

### Stage 5 — decision

Allowed outcomes after this evidence sprint:

- **Reject hypothesis**
- **Revise as a new version**
- **Collect one named missing evidence item**
- **Advance to a no-inventory commercial behavior test**

This sprint cannot produce a validated play or an earned instruction. It can only decide whether a mechanism deserves its first commercial instance test.

## Budget and authority

- Maximum research ceiling: **$25 per mechanism / $75 total**.
- A ceiling is not authorization to spend.
- No advertising, inventory, supplier outreach, public claims, affiliate publishing, or product purchase is authorized.
- Human approval remains required for spending and external action.

## Immediate human actions

1. Conduct two `training_only` Friction Removal pilot interviews and complete a separate debrief for each. They do not count as mechanism evidence.
2. Freeze Interview Protocol v1 after the pilot debriefs.
3. Register candidate sources across Classes A-E and qualify authorization before collection.
4. Recruit the formal five qualified interviewees per mechanism using the recent-behavior criterion.
5. Import one small dry-run batch before collecting the full corpus; verify provenance and duplicate handling.
6. Do not modify the cards once the first formal review or interview is collected. If a flaw is found, stop and version the card first.

## Completion standard

Operation First Principle has begun when the first authorized corpus or interview is collected against an unchanged card. It is complete when all three cards have an evidence table and an explicit decision grounded in their preregistered criteria.

Instruction #1 remains **not earned**.

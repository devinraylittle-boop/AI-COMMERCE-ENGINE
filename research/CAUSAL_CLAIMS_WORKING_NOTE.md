# Causal Claims — Working Note

**Status:** research doctrine, not architecture  
**Decision:** do not create Claim Cards, database records, schemas, or UI until real evidence demonstrates that Mechanism Cards cannot represent a decision reliably.

## The refinement

A commercial mechanism is a family of possible causal claims. It is too broad to validate as one indivisible idea.

```text
Mechanism
  -> one or more causal claims
  -> claim-specific evidence
  -> claim-specific experiment
  -> observation
  -> independent replication
  -> bounded instruction
```

A mechanism may contain one supported claim and several rejected claims. ACE must not allow strength in one claim to inflate confidence in the others.

This distinction is recorded now and deliberately not implemented. The current Mechanism Cards remain hypotheses and keep their existing gates.

## Working claims

These statements sharpen our thinking. They are not preregistered experiments, validated findings, or replacements for the v1 cards.

### Friction Removal

**Working causal claim:** Reducing uncertainty about product fit increases successful selection without proportionally increasing human support or fit-related returns.

- **Intervention:** decision guidance that makes dimensions, constraints, and exclusions clear.
- **Expected behavioral effect:** fewer unsuitable selections and more confident qualified choices.
- **Operational constraint:** the guidance cannot require custom design or support that consumes its economic benefit.
- **Plausible alternate explanations:** better photography, lower price, stronger brand, novelty, or selection limited to easier customers.
- **Would weaken the claim:** buyers ignore fit evidence, fit failures persist, or support effort rises as much as qualified selection improves.
- **Not yet known:** whether a recurring cross-context fit problem exists or whether buyers will act on the guidance.

### Trust-Mediated Care

**Working causal claim:** In emotionally consequential purchases, visible willingness to recommend against an unsuitable purchase increases qualified trust and improves selection quality enough to offset intentionally forgone unsuitable conversions.

- **Intervention:** explicit limitations, exclusion criteria, and honest “do not buy” guidance.
- **Expected behavioral effect:** unsuitable buyers opt out while suitable buyers place greater weight on the remaining recommendation.
- **Operational constraint:** safe guidance must remain conservative and self-service rather than individualized professional advice.
- **Plausible alternate explanations:** authority cues, brand familiarity, price, social proof, or relief from decision overload.
- **Would weaken the claim:** the guidance only lowers conversion, has no effect on suitable buyers, or requires individualized safety judgments.
- **Not yet known:** whether trust changes actual selection behavior rather than stated preference.

### Expertise Ladder

**Working causal claim:** Education increases willingness to select a higher-value solution only when it credibly reduces expected waste, failure, or unnecessary upgrading.

- **Intervention:** stage-appropriate workflow and compatibility education tied to a concrete avoided loss.
- **Expected behavioral effect:** buyers choose a better-fit solution or decline an unnecessary upgrade.
- **Operational constraint:** content and compatibility maintenance cannot cost more than the value the guidance creates.
- **Plausible alternate explanations:** aspirational identity, enthusiast status, aesthetics, creator influence, or premium-brand signaling.
- **Would weaken the claim:** education is consumed without changing choices, or higher spend occurs without reduced waste or failure.
- **Not yet known:** whether a cross-platform problem exists and whether education influences real purchases.

## ACE's scientific sequence

```text
Question
  -> Causal Claim
  -> Evidence Plan
  -> Experiment
  -> Observation
  -> Replication
  -> Instruction
```

Judgment is unavoidable in choosing questions, methods, thresholds, and interpretations. ACE records that judgment as assumptions and design decisions; it does not promote it to observed evidence.

An instruction is earned only when:

1. The causal claim is specific enough to be false.
2. The evidence plan contains disconfirming paths.
3. The experiment measures behavior or operational outcomes appropriate to the claim.
4. Alternate explanations are considered.
5. The result survives an independent context.
6. The instruction states its boundary and reversal conditions.

## Blinding direction

The calibration pilots cannot be meaningfully blind: their subject is the interview instrument itself, and the current operator already knows the project context. They do not count as mechanism evidence.

Formal evidence collection should separate roles when operationally possible:

- **Interviewer:** receives behavioral eligibility criteria and a neutral script, not the causal claim or desired result.
- **Analyst:** receives de-identified evidence, source limitations, and preregistered themes without participant identity.
- **Mechanism owner:** receives the analysis, contradictions, protocol deviations, and aggregate evidence without unnecessary identities.

If one person must perform multiple roles, the decision record states that blinding was impossible and treats confirmation bias as a limitation. ACE must not simulate independence by renaming one person's passes through the data.

Do not build role-management software now. Reconsider only when a real formal collection shows that lack of separation materially affects evidence reliability.

## Architecture purchase rule

The next architecture request must begin:

> Reality taught us something that ACE cannot currently represent: ...

It must then name:

- the lost or distorted evidence;
- the decision harmed;
- the current workaround;
- why a process or document cannot solve it;
- the smallest implementation that would repair the measurement.

“One mechanism contains many claims” is an important insight. It is not yet evidence that ACE needs Claim Card software.

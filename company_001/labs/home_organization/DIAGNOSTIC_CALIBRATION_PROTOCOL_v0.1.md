# Diagnostic Calibration Protocol v0.1

**Status:** internal training and taxonomy test; no customer diagnosis or public outreach

## Objective

Test whether the Failure Mode Map helps coders distinguish plausible causes, preserve uncertainty, identify False Problems, and escalate hazards without drifting toward product recommendations.

## Materials

- `FAILURE_MODE_MAP_v0.1.md`
- `DIAGNOSTIC_CALIBRATION_CASES_v0.1.csv`
- `DIAGNOSTIC_CALIBRATION_REFERENCE_v0.1.csv`

The cases are clearly marked synthetic composites. They train discrimination and cannot support market, prevalence, or mechanism claims.

## Procedure

1. Do not read the reference file before coding.
2. For each case, record reported cause, primary mode or `INSUFFICIENT`, secondary modes, `FP` overlay, hazard flag, evidence, and the next discriminating question.
3. Do not propose a product or solution.
4. Complete every case before reviewing the reference.
5. Compare against the reference and record disagreements. The reference is provisional, not truth.
6. Revise a code definition only when the disagreement exposes ambiguity in the map, not merely to make the coder “correct.”
7. A second independent coder should repeat the exercise before public use.

If one person repeats the coding later, report **within-coder stability** only. Do not call it inter-rater agreement or blinding.

## Measures

- exact primary-mode agreement;
- multi-label Jaccard agreement for primary plus secondary modes;
- appropriate `INSUFFICIENT` use;
- False Problem positive and negative agreement;
- hazard sensitivity and false-alarm rate;
- percentage of next questions that genuinely discriminate between named modes;
- product-prescription violations;
- disagreements caused by case ambiguity versus code ambiguity.

## Working release gates

These gates protect the next internal evidence sample; they do not validate the taxonomy generally.

- 100% hazard detection on explicit hazard cases;
- zero product prescriptions;
- at least 75% exact primary-mode agreement with the adjudicated reference;
- at least 0.70 mean multi-label Jaccard agreement;
- at least 80% agreement on `FP` presence/absence;
- `INSUFFICIENT` used on every case intentionally lacking discriminating evidence;
- every disagreement documented before map revision.

If a gate fails, the map remains training-only. Do not compensate by weakening the gate after seeing results; document why a revised future gate is justified.

## Real-evidence calibration after synthetic cases

Only after the synthetic gate passes:

1. Qualify six existing, lawful sources without public solicitation.
2. Draw 20 problem episodes using predeclared source rules.
3. Remove usernames and unnecessary identity fields from the coder packet.
4. Have two coders classify independently when possible.
5. Adjudicate disagreements using source context and preserve unresolved cases.
6. Examine whether a new mode is required or an existing distinction cannot be observed reliably.

No public outreach is earned merely by completing synthetic cases.

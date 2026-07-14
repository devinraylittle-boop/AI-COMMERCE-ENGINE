# Diagnostic Calibration Protocol v0.1

**Status:** governance specification; the included synthetic examples are open training material, not a blind calibration

## Objective

Test whether the Failure Mode Map helps genuinely independent coders distinguish plausible causes, preserve uncertainty, identify False Problems, and escalate hazards without drifting toward product recommendations.

## Open training materials

- `FAILURE_MODE_MAP_v0.1.md`
- `OPEN_TRAINING_CASES_v0.1.csv`
- `OPEN_TRAINING_REFERENCE_v0.1.csv`

These synthetic composites and their provisional answers are available in public Git history. They may be used to learn the codebook, test the mechanics of a coding sheet, and expose ambiguous definitions. They cannot measure blind performance, inter-rater reliability, or readiness for customer use. Passing them satisfies no formal release gate.

## Formal calibration materials

A formal calibration requires a new case packet that neither Coder A nor Coder B has seen and a reference that neither coder can access before both submissions are locked. The case packet and sealed reference must not be committed to the public repository while calibration is active.

Each coder receives only:

- the frozen Failure Mode Map;
- `FORMAL_CODER_SHEET_TEMPLATE.md`;
- the unseen case packet;
- a unique anonymous coder identifier.

Neither coder receives reference answers, the other coder's work, authorship information, or adjudication notes.

## Independence and blinding

Independence concerns a participant's prior role and knowledge. Blinding concerns what information is withheld during a particular task. One does not substitute for the other.

- A founder, architect, taxonomy designer, case author, reference author, or anyone who has already viewed the reference is ineligible to serve as Coder A or Coder B.
- Devin and the participating Codex architect are therefore excluded from independent-coder roles for this calibration.
- Repeating the exercise later can measure within-coder stability only.
- A fresh AI may qualify only if it receives no ACE conversation history, repository access, hidden reference, or retrieval capability that could expose the answer key. Record its provider, model/version, complete prompt, settings, and run identifier.
- Never describe a participant or run as independent or blind without a recorded basis.

## Formal procedure

1. Freeze and hash the codebook and coder instructions.
2. Have an eligible Case Steward create a new case packet and provisional reference.
3. Seal the reference outside the public repository and record access in the custody log.
4. Have the Packet Custodian distribute identical, reference-free packets to Coder A and Coder B.
5. Obtain eligibility declarations before coding begins.
6. Lock both complete submissions before either coder receives feedback.
7. Replace names with randomized coder identifiers.
8. Calculate pre-adjudication agreement and uncertainty measures.
9. Give only anonymized disagreements to the Arbiter. The Arbiter records a reasoned disposition without knowing coder identities.
10. Send only disagreements that survive arbitration to the Mechanism Owner.
11. Unseal the provisional reference only after coder and arbiter judgments are locked.
12. Publish aggregate results, limitations, taxonomy changes, and unresolved cases without implying that the provisional reference is truth.

## Measures

- exact primary-mode agreement between coders;
- multi-label Jaccard agreement for primary plus secondary modes;
- appropriate `INSUFFICIENT` use;
- False Problem positive and negative agreement;
- hazard sensitivity and false-alarm rate;
- percentage of next questions that genuinely discriminate between named modes;
- product-prescription violations;
- disagreements caused by case ambiguity versus code ambiguity;
- changes introduced during arbitration and after reference unsealing.

## Working release gates

These gates protect the next internal evidence sample; they do not validate the taxonomy generally.

- 100% hazard detection on explicit hazard cases;
- zero product prescriptions;
- at least 75% exact primary-mode agreement between coders before adjudication;
- at least 0.70 mean pre-adjudication multi-label Jaccard agreement;
- at least 80% agreement on `FP` presence/absence;
- `INSUFFICIENT` used on every case intentionally lacking discriminating evidence;
- every disagreement documented before map revision;
- no independence, blinding, or custody violation.

If a gate fails, the map remains training-only. Do not weaken a gate after seeing results merely to obtain a pass.

## Real-evidence calibration

Only after a valid formal synthetic calibration passes:

1. Qualify six existing, lawful sources without public solicitation.
2. Draw 20 problem episodes using predeclared source rules.
3. Remove usernames and unnecessary identity fields from the coder packet.
4. Repeat the independent, blinded, anonymized coding and arbitration procedure.
5. Preserve unresolved cases and examine whether a new mode is required or an existing distinction cannot be observed reliably.

No public outreach is earned by completing open training examples or a synthetic calibration.

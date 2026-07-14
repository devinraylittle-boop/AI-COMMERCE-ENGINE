# Formal Calibration Governance v0.1

**Status:** required process for any future claim of independent diagnostic calibration

## Governing rule

Do not pretend independence where it does not exist. A useful exercise does not become an independent calibration merely because its participants are called coders.

## Roles

| Role | Responsibility | Must not do |
|---|---|---|
| Case Steward | Create unseen cases and a provisional reference using the frozen codebook | Code cases, arbitrate, or disclose the reference |
| Packet Custodian | Control access, collect declarations, distribute identical packets, lock submissions, and anonymize outputs | Alter cases or classifications after distribution |
| Coder A | Classify the full packet independently | Access the reference, other coding, or ACE design history relevant to the taxonomy |
| Coder B | Independently classify the same packet | Access the reference, Coder A's work, or ACE design history relevant to the taxonomy |
| Arbiter | Review anonymized disagreements and record a reasoned disposition | Learn coder identities before disposition or silently replace uncertainty with a forced label |
| Mechanism Owner | Review only disputes that survive arbitration and decide whether evidence earns a process or taxonomy change | Review routine agreements or rewrite history to improve metrics |

One person may not combine roles when doing so exposes reference answers, coder identities, or prior design knowledge that defeats independence. If limited staffing forces combined roles, document the conflict and downgrade the claim; do not rename the result independent calibration.

## Eligibility

A coder is eligible only if all are true:

1. They did not create or materially revise the taxonomy.
2. They did not author, select, or edit the formal cases.
3. They have not seen the formal reference.
4. They have not seen another coder's answers.
5. They can complete the packet without consulting people or materials outside the authorized packet.
6. They sign the declaration before receiving cases.

The founder and participating Codex architect are currently ineligible. Their process knowledge remains useful for governance and later mechanism review, but not for an independence claim.

## Packet custody

The formal case packet and provisional reference remain outside the public repository until coding and adjudication are locked. The Custodian maintains:

- packet identifier and cryptographic hash;
- codebook and instruction hashes;
- date and recipient of every distribution;
- reference-access log;
- coder eligibility declarations;
- immutable submission timestamps and hashes;
- anonymization key, kept from the Arbiter;
- accidental-exposure and protocol-deviation log.

A public hash may establish that a sealed artifact existed at a given time without exposing its content. Do not publish the artifact itself while the blind procedure is active.

## Arbitration

1. Measure Coder A/B agreement before any adjudication.
2. Create a disagreement packet containing case evidence, anonymized labels, rationales, and next questions.
3. Randomize the presentation order of coder responses where practical.
4. Require the Arbiter to choose one classification, propose another, or preserve `INSUFFICIENT`, with a written reason.
5. Send only unresolved disputes to the Mechanism Owner.
6. Unseal the provisional reference after the preceding judgments are locked.
7. Treat reference disagreements as evidence about the reference, case, or codebook—not automatic coder errors.

## Fresh-AI eligibility

A fresh AI run can be a coder, not an arbiter and coder in the same run, only when:

- it begins in a new task with no ACE conversation history;
- its prompt contains only the authorized coder packet;
- it has no repository, web, memory, connector, or retrieval access that could reveal the reference;
- the full prompt, model/version, settings, date, and output are retained;
- Coder A and Coder B are separate runs with no shared generated context;
- the limitations of model-family dependence are reported.

Two fresh runs of the same model may measure procedural reproducibility, but they do not provide the same diversity as two independent human judgments. Report that limitation.

## Invalidating events

The independence claim is invalid if a coder sees the reference or another coder's work before submitting, helped create the formal cases, receives case-specific coaching, or uses unapproved outside material. Preserve the work as open analysis, record the deviation, and replace the coder or packet. Never erase the event.

## Completion record

A formal calibration report must name the packet and codebook hashes, role eligibility basis, deviations, pre-adjudication metrics, arbitration outcomes, unresolved cases, release-gate result, and exact scope of any conclusion. It must not identify a provisional answer key as ground truth.

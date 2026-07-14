# Home Organization Failure Mode Map v0.1

**Status:** working diagnostic map; not an earned instruction, product taxonomy, or customer diagnosis

**Working doctrine:** Every recurring complaint should first be treated as a diagnostic problem before it is treated as a commercial opportunity.

## Purpose

Company 001 exists to test whether ACE can distinguish superficially similar complaints that require fundamentally different responses. “My pantry is a mess” is an observation label, not a cause.

ACE records four separate layers:

```text
Observed condition
  -> person's stated explanation
  -> competing failure-mode hypotheses
  -> evidence that discriminates among them
```

No hypothesis becomes a diagnosis merely because it sounds plausible.

## Diagnostic hierarchy

```text
Disorganization
├── Volume and inflow mismatch
│   ├── V1 Excess possessions for the available space
│   ├── V2 Uncontrolled or poorly informed inflow
│   └── V3 Fixed capacity constraint
├── System-design mismatch
│   ├── S1 Missing or unstable categories and decision rules
│   ├── S2 Wrong location or point-of-use mismatch
│   ├── S3 Dimensional fit or measurement error
│   ├── S4 Visibility or identification failure
│   ├── S5 Access or retrieval failure
│   └── S6 Wrong containment or storage type
├── Maintenance and behavior mismatch
│   ├── B1 Missing routine or trigger
│   ├── B2 Reset effort exceeds sustainable effort
│   └── B3 Execution constraint
├── Household-governance mismatch
│   ├── C1 Inconsistent users or incompatible mental models
│   └── C2 Unclear ownership or responsibility
├── Context and time mismatch
│   ├── T1 Temporary overload or life transition
│   └── T2 Requirements changed after the system was designed
├── Product or installation failure
│   ├── P1 Durability or quality failure
│   └── P2 Assembly or installation failure
├── Environmental or safety condition
│   ├── E1 Moisture, leak, or mold condition
│   ├── E2 Pest or food-contamination condition
│   └── E3 Fall, fire, egress, or other immediate safety condition
├── Human-access mismatch
│   └── H1 Physical, sensory, reach, strength, or mobility mismatch
└── Definition mismatch
    └── D1 Aesthetic dissatisfaction without demonstrated functional failure

Overlay: FP False Problem — the stated cause or requested solution does not match the best-supported failure mode.
```

## Why False Problem is an overlay

“False Problem” does not mean the person's frustration is imaginary. It means the **causal framing** is unsupported or contradicted.

Examples:

- “I need more storage” while duplicate purchases continue entering faster than items leave: `V2` with `FP`.
- “The organizer is bad” when its published dimensions do not fit the measured shelf: possibly `S3`, not necessarily `P1`.
- “I need waterproof bins” while an active leak wets the wall: `E1` with `FP`; containment does not resolve the source.
- “This room is disorganized” when every item is retrievable, no time or money is lost, and the concern is visual uniformity: possibly `D1`, not functional disorganization.

The overlay requires two recorded fields:

1. `reported_cause_or_requested_solution`
2. `best_supported_failure_mode`

Set `FP` only when evidence supports a meaningful divergence. When evidence is weak, use `insufficient evidence`.

## Codebook

### Volume and inflow

| ID | Failure mode | Include when | Do not infer from | Discriminating evidence |
|---|---|---|---|---|
| V1 | Excess possessions | Required volume exceeds usable capacity after reasonable categorization; removal restores function | visible fullness alone | inventory, usable volume, duplicates, unused items, function before/after removal |
| V2 | Inflow mismatch | Purchases, mail, food, gifts, or returns enter faster than the system processes or removes them | one recent shopping trip | acquisition cadence, duplicates, unopened goods, replenishment rules, outflow cadence |
| V3 | Fixed capacity constraint | Necessary retained items reasonably exceed safe available space | unwillingness to discard | required inventory, housing constraints, seasonal needs, alternative-space availability |

### System design

| ID | Failure mode | Include when | Do not infer from | Discriminating evidence |
|---|---|---|---|---|
| S1 | Category/rule failure | Items lack stable homes, categories overlap, or decisions change each reset | unlabeled containers alone | inconsistent placement, ambiguous categories, repeated re-sorting |
| S2 | Location mismatch | Storage is separated from where items enter, are used, or are returned | an unconventional location | movement path, drop zones, frequency of use, natural return behavior |
| S3 | Fit/measurement error | Dimensions, clearances, door swing, stacking, or tolerances prevent intended use | a product return alone | measured space/product, hinge/handle clearance, load and orientation |
| S4 | Visibility/identification failure | People forget, duplicate, expire, or search because contents/status are not knowable | opaque bins alone | search episodes, expired goods, duplicate purchases, labeling accuracy |
| S5 | Access/retrieval failure | Needed items require unsafe, repeated, or disruptive moves | deep storage alone | retrieval steps, frequency, reach, lifting, obstruction, restacking |
| S6 | Containment-type mismatch | Container/shelf/hook style conflicts with item shape, environment, frequency, or handling | dislike of appearance | item behavior, ventilation, moisture, weight, access frequency, cleaning needs |

### Maintenance and behavior

| ID | Failure mode | Include when | Do not infer from | Discriminating evidence |
|---|---|---|---|---|
| B1 | Missing routine/trigger | No stable action or event returns items and processes inflow | a missed reset | repeated absence of reset, no cue, no defined cadence |
| B2 | Excess reset effort | The designed system requires more steps, precision, or time than users sustain | low motivation language alone | step count, time-to-reset, lids/stacking, failure after initial setup |
| B3 | Execution constraint | Time, energy, attention, or cognitive load prevents execution despite an otherwise workable system | laziness or character judgments | workload, competing duties, episodic capacity, simplification response |

ACE does not diagnose medical, psychological, or neurodevelopmental conditions. It records observable execution constraints and refers when appropriate.

### Household governance

| ID | Failure mode | Include when | Do not infer from | Discriminating evidence |
|---|---|---|---|---|
| C1 | User inconsistency | Different users understand or operate the system differently | another person living in the home | divergent placement, reach/label needs, conflicting category models |
| C2 | Ownership ambiguity | No person or shared rule owns replenishment, reset, disposal, or maintenance | one unfinished chore | repeated handoff failure, duplicated responsibility, unassigned tasks |

### Context and time

| ID | Failure mode | Include when | Do not infer from | Discriminating evidence |
|---|---|---|---|---|
| T1 | Temporary overload | A bounded event exceeds normal capacity but baseline function is sound | seasonal recurrence without recovery | move, illness, holiday, delivery, project, recovery to baseline |
| T2 | Changed requirements | Users, inventory, activity, or physical ability changed after design | any old product | before/after needs, household change, new use case, growth stage |

### Product and installation

| ID | Failure mode | Include when | Do not infer from | Discriminating evidence |
|---|---|---|---|---|
| P1 | Durability/quality failure | Material, mechanism, fastener, lid, caster, or finish fails under represented use | damage after misuse or overload | stated rating, load/use, defect pattern, time to failure, comparable units |
| P2 | Assembly/installation failure | Incorrect, incomplete, unstable, or infeasible installation prevents function | dissatisfaction after assembly | instructions, hardware, substrate, tool/skill needs, installation record |

### Environment and safety

| ID | Failure mode | Include when | Mandatory action |
|---|---|---|
| E1 | Moisture/leak/mold | dampness, leak, condensation, musty odor, visible growth, water damage | stop ordinary organization prescription; identify moisture-source/professional boundary |
| E2 | Pest/contamination | insects, rodents, droppings, damaged food, contamination | stop product recommendation; use food-safety/IPM or qualified professional boundary |
| E3 | Fall/fire/egress/other safety | blocked exit, trip hazard, unstable load, dangerous reach, overloaded fixture | prioritize immediate safety and qualified assessment over aesthetics/storage |

EPA states that moisture control is central to mold control and recommends experienced professional help for hidden mold or larger/complex cleanup conditions ([EPA mold guide](https://www.epa.gov/mold/brief-guide-mold-moisture-and-your-home), [EPA cleanup](https://www.epa.gov/mold/mold-cleanup-your-home)). EPA's integrated-pest-management guidance emphasizes prevention and removing food, water, shelter, and entry conditions rather than relying on a container alone ([EPA IPM](https://www.epa.gov/ipm/introduction-integrated-pest-management)). CDC identifies clutter as one of several home fall hazards for older adults; ACE must not reduce a multi-factor safety problem to selling storage ([CDC](https://www.cdc.gov/falls/data-research/facts-stats/)).

### Human access and definition

| ID | Failure mode | Include when | Do not infer from | Discriminating evidence |
|---|---|---|---|---|
| H1 | Human-access mismatch | Reach, grip, strength, vision, mobility, height, or user age makes the system inaccessible | age or disability label alone | observed task, reach/load, contrast, dexterity, safe access requirements |
| D1 | Aesthetic-only mismatch | Function is intact but appearance violates a preference | visual complaint alone | retrieval time, waste, reset success, safety, stated functional consequences |

## Multi-cause rules

- Assign one `primary_mode` only when evidence shows it is the best current explanation.
- Assign `secondary_modes` when they materially contribute.
- Record `insufficient evidence` instead of forcing a primary mode.
- A symptom may be downstream of several modes. Duplicate food can result from `S4`, `V2`, or both.
- A product failure can coexist with a design mismatch; determine whether the product failed under represented use.
- Hazard modes outrank commercial investigation but do not erase underlying system evidence.
- `FP` never substitutes for a root mode.

## Minimum diagnostic record

```text
Observed condition:
Reported cause or requested solution:
Context and affected users:
Frequency and duration:
Consequences:
Current workaround and result:
Evidence supporting each candidate mode:
Evidence contradicting each candidate mode:
Primary mode or insufficient evidence:
Secondary modes:
False Problem overlay and rationale:
Hazard/referral flag:
What observation would change the classification:
Coder and date:
```

## What this map cannot do

- diagnose a person or household from a photograph or short complaint;
- establish a medical, psychological, or behavioral disorder;
- determine prevalence from convenience-source counts;
- prescribe remediation for mold, pests, structural, electrical, fire, or health conditions;
- prove that a product is needed;
- convert a code into a commercial opportunity automatically.

The map earns value only if independent evidence shows ACE can apply it consistently and revise it when cases do not fit.

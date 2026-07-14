# The ACE Evidence Supply Chain

**Active sprint:** Reality Check  
**Purpose:** make truthful evidence acquisition repeatable across Company 001 and every future ACE experiment.  
**Operating question:** Where will the next decision's evidence come from, and how could that evidence mislead us?

## Executive rule

Architecture must now be purchased with evidence. No major architecture is authorized until a real experiment exposes a limitation that materially harms acquisition cost, evidence integrity, conclusion reliability, or decision speed.

The Evidence Supply Chain is an operating process, not software:

```text
Decision question
  -> required evidence classes
  -> qualified source register
  -> authorization gate
  -> collection plan
  -> immutable raw record
  -> controlled interpretation
  -> contradiction and triangulation
  -> bounded decision
  -> observed outcome
  -> source-quality learning
```

Every arrow is a failure point. ACE records failures instead of silently repairing them.

Mechanisms organize commercial theories; causal claims are the units that experiments can support or reject. The current distinction and future claim-blinding direction are recorded in `research/CAUSAL_CLAIMS_WORKING_NOTE.md`. No Claim Card implementation is authorized.

## Evidence classes

The letters identify evidence types; they are not quality grades. Class A behavior is often the best evidence of what somebody did, but it cannot by itself establish safety, causality, market size, or viable economics. A conclusion becomes stronger when independent classes converge.

### Class A — observed customer behavior

Examples: demonstrated workaround, observed selection, actual purchase history, abandoned choice, product use, repeat purchase, return, or real behavior in a controlled test.

- **Best for:** what people actually do.
- **Common bias:** observer effects, selection bias, missing context, and confusing correlation with cause.
- **Minimum record:** behavior, context, timestamp, observation method, observer, permission, alternative explanations, and what was not observed.

### Class B — customer language

Examples: authorized reviews, interviews, support logs, surveys, complaints, forums used under applicable permission, and customer questions.

- **Best for:** language, perceived pain, expectations, decision criteria, and explanations.
- **Common bias:** recall, courtesy, selection, extreme-experience, source-community, and hypothetical-intent bias.
- **Minimum record:** source, authorization, exact wording where lawful, date, context, prompts used, sampling method, and whether the statement describes behavior or opinion.

### Class C — market behavior

Examples: observed prices, assortment changes, promotions, demand proxies, search behavior, participation, competitor activity, and marketplace or retail observations.

- **Best for:** market movement, availability, pricing context, and competitive structure.
- **Common bias:** popularity mistaken for demand, listings mistaken for sales, search interest mistaken for purchase intent, and survivor bias.
- **Minimum record:** metric definition, geography, period, collection method, coverage, source constraints, and why the observation matters to the decision.

### Class D — expert knowledge

Examples: practitioners, professional associations, extension services, standards bodies, safety guidance, peer-reviewed research, and experienced operators.

- **Best for:** mechanisms, safety, standards, failure modes, and boundary conditions.
- **Common bias:** authority bias, institutional incentives, narrow specialty, lagging practice, and advice without customer-economics evidence.
- **Minimum record:** expertise basis, conflicts, date, scope, evidence behind the claim, and the conditions under which it may not apply.

### Class E — operational evidence

Examples: supplier quotations, dimensions, samples, defect tests, shipping cost, delivery time, support effort, return reasons, fees, contribution margin, and actual fulfillment outcomes.

- **Best for:** whether the mechanism can become a functioning business.
- **Common bias:** estimates presented as observations, favorable supplier samples, stale quotations, hidden labor, and early volumes that do not represent scale.
- **Minimum record:** observed versus estimated status, quantity, date, actor, quote or transaction reference, assumptions, exclusions, and downside case.

## Source qualification

Every recurring source receives a source record before its evidence is used. Trust is documented dimensionally; ACE does not hide judgment inside one source-quality score.

Required dimensions:

| Dimension | Question |
|---|---|
| Authorization | Are we permitted to acquire, retain, transform, and use this evidence? |
| Directness | How directly does it measure the decision claim? |
| Independence | Is it independent from the other evidence being used? |
| Coverage | Who, what, geography, and period are represented or excluded? |
| Recency | Is it current enough for this decision? |
| Integrity | Can the raw observation and transformations be audited? |
| Incentives | Who benefits if we believe it? |
| Repeatability | Can the same collection method be run again? |
| Cost | Money and operator time required per collection cycle |
| Failure signal | How will we know the source has become stale, biased, unavailable, or noncompliant? |

Source states are `candidate`, `qualified`, `restricted`, `unavailable`, `stale`, or `retired`. Public visibility never equals authorization.

## Coverage states

Every mechanism is evaluated across all five classes, but absence is allowed when it is explicit. Forcing weak evidence into every class would make ACE easier to fool.

- **Missing:** no usable evidence.
- **Proxy:** indirect evidence only.
- **Direct:** evidence directly measures the stated claim in one context.
- **Replicated:** independent direct evidence in another context.
- **Contradictory:** credible evidence points in materially different directions.
- **Stale:** evidence no longer meets the decision's recency requirement.

No composite evidence score is permitted. The decision record must state which classes are missing, which are decisive, and why.

## Collection cadence

Cadence is triggered by decisions and source decay—not a desire to keep dashboards moving.

| Operating stage | Class A | Class B | Class C | Class D | Class E |
|---|---|---|---|---|---|
| Discovery | Optional direct observation | Small language sample | Current parent-market context | Safety/standards scan | Explicitly missing or rough proxy |
| Reality Check | Required behavior history or observation | Required reviews and interviews | Current pricing/competition snapshot | Required boundary/safety review | Supplier and fulfillment proxy, explicitly labeled |
| Commercial instance test | Real choice or payment behavior | Objection and abandonment language | Live alternative/price context | Review if claim or safety boundary changes | Actual cost, labor, delivery, refund, and contribution data |
| Active company | Continuous event capture | Support/return feedback monthly | Competitor/price review monthly or on alert | Standards review quarterly or on change | Per-order capture; monthly operating review |
| Replication | New population and context | New independent language source | New market context | New relevant specialists | Independent operating path |

Association releases, standards, access terms, and provider costs are reverified immediately before consequential use even when their scheduled cadence has not elapsed.

## Reality Check supply maps

These are acquisition plans, not claims of authorization. Each candidate source must pass qualification before collection.

### Trust-Mediated Care — Dog Training & Enrichment

| Class | Repeatable input | Collection method | Current state | Primary bias or risk | What could change our mind |
|---|---|---|---|---|---|
| A | Recent owner selection and use histories | Interview walkthrough of last real purchase; later observed choice test | Missing | Recall and owner interpretation | Owners consistently choose without safety/suitability information, or require individualized professional advice |
| B | Authorized reviews and owner interviews | Two lawful review sources across three contexts; structured interviews | Missing | Negative-review and convenience-sample bias | No actionable concern transfers across sources and contexts |
| C | Participation, observed assortment, and price bands | APPA context plus a dated manual retail sample | Proxy | Parent market and listings are not sales | Relevant offers are uniformly commoditized with no observable guidance differentiation |
| D | Safety, training, and behavior boundaries | AKC guidance; qualified trainer or veterinary-behavior boundary review | Direct for safety guidance | Expertise does not prove willingness to pay | Safe matching requires individualized diagnosis or unsupported claims |
| E | Compact-product cost, durability, support, and returns | Public supplier documentation first; quotes/samples only after approval | Missing | Supplier claims and estimated returns | Safe quality cannot support positive downside contribution margin or lean support |

### Expertise Ladder — Home Espresso / Coffee

| Class | Repeatable input | Collection method | Current state | Primary bias or risk | What could change our mind |
|---|---|---|---|---|---|
| A | Last purchase, upgrade, avoided purchase, and preparation workflow | Interview reconstruction; later observed information-choice test | Missing | Post-purchase rationalization | Education was consumed but did not change real choices |
| B | Authorized workflow, maintenance, and compatibility reviews | Two lawful sources plus structured home-user interviews | Missing | Enthusiast overrepresentation and technique blamed on products | No cross-platform pain survives source triangulation |
| C | Participation, current alternatives, compatibility claims, and prices | NCA context plus a dated manual retail sample | Proxy | Participation is not gear demand | Useful solutions are machine-specific or price competition eliminates guidance value |
| D | Preparation, water, maintenance, and compatibility expertise | Qualified barista/technician sources and applicable association guidance | Missing | Specialist preferences may exceed normal customer needs | Credible advice requires expensive, continuously updated expert support |
| E | Product compatibility, support time, shipping, breakage, and margin | Public specifications first; quotes/samples only after approval | Missing | Hidden support labor and compatibility churn | Maintenance cost exceeds the value created by the education layer |

### Friction Removal — Home Organization

| Class | Repeatable input | Collection method | Current state | Primary bias or risk | What could change our mind |
|---|---|---|---|---|---|
| A | Demonstrated current workaround and last failed attempt | Permission-based walkthrough, measurements, or participant-provided images | Missing | Observer effect, privacy, and short-lived cleanup enthusiasm | The root problem is accumulation or motivation rather than a transferable system defect |
| B | Authorized reviews and household interviews | Two lawful sources across three contexts plus structured interviews | Missing | Aesthetic preference and self-selection | No fit/access/maintenance failure transfers across contexts |
| C | Household pain, current alternatives, dimensions, and prices | YouGov context plus a dated manual retail sample | Proxy | Self-reported pain does not equal willingness to pay | Commodity pricing makes guidance uneconomic or all useful solutions require custom fit |
| D | Behavioral and professional organizing boundaries | Qualified organizing practitioner and relevant housewares guidance | Missing | Professional practice may assume high-touch service | Sustainable resolution requires ongoing human coaching or custom design |
| E | Dimensions, packaging, shipping, assembly, returns, and margin | Public specifications first; quotes/samples only after approval | Missing | Bulky-item economics and fit returns | Shipping, returns, or custom support destroy the low-complexity thesis |

## Interview supply chain

Interview recruitment is a recurring source operation, not a one-time task.

### Candidate pools

- Personal network introductions with no pressure to participate
- Permission-based local clubs, hobby groups, or community organizations
- Practitioners who can refer customers without disclosing client information
- Existing customers and support contacts after a company operates
- Reputable research panels only after cost, consent, and quality approval

ACE does not mass-message communities, impersonate customers, buy undisclosed lists, or treat unsolicited scraping as recruitment.

### Qualification

Participants must have completed the relevant behavior, purchase, or workaround recently enough to reconstruct it. Record the qualifying event and date range without collecting unnecessary identity information. Do not recruit only enthusiasts, friends, successful users, or people who already agree with the mechanism.

### Calibration before evidence collection

Run **two training-only pilot interviews** in Friction Removal because the context is broadly accessible and has lower safety and technical risk. These pilots:

- test question clarity, neutrality, timing, note quality, and debrief discipline;
- are labeled `training_only` and cannot count toward any mechanism gate;
- do not alter a Mechanism Card;
- may result in a versioned interview protocol before formal collection begins.

After each pilot, complete `research/templates/INTERVIEW_DEBRIEF.md`. Freeze Interview Protocol v1 only after the second debrief. Then recruit the formal five participants per mechanism.

### Interview quality controls

- One interviewer; a second note-taker only with consent.
- Ask about the last real event before opinions or solutions.
- Do not name the mechanism, proposed product, or desired answer.
- Separate verbatim statement, observed behavior, interviewer inference, and follow-up question.
- Record disconfirming statements with equal prominence.
- Send a short interpretation check when the conclusion depends on ambiguous wording.
- Stop if the participant withdraws consent or the conversation enters unnecessary sensitive territory.

## Evidence batch release gate

An evidence batch may inform a decision only when:

1. Its source record is qualified and authorization is documented.
2. Raw material and transformations are auditable.
3. Duplicates, missing fields, source concentration, and exclusions are disclosed.
4. Behavior, language, inference, estimate, and expert opinion remain distinct.
5. Contradictory evidence is included.
6. The exact Mechanism Card version and decision criterion are named.
7. A person not responsible for collecting the batch can understand its limits.

If any condition fails, the batch is quarantined from decision use. It may still teach ACE how to improve collection.

## Supply-chain performance

We measure the evidence operation with observable process outcomes, not evidence volume:

- Authorization rejection rate
- Time and cost from question to qualified evidence
- Participant qualification rate
- Duplicate and unusable-record rate
- Source concentration
- Missing evidence classes at decision time
- Rate of conclusions changed by contradictory evidence
- Interview protocol deviations
- Evidence refresh failures
- Predictions or decisions later contradicted by outcomes

The goal is not to drive every metric downward. A rising rejection rate can be healthy if qualification is becoming more honest.

## Immediate execution

1. Run two training-only Friction Removal interviews using `research/INTERVIEW_PROTOCOL.v0.1.md`.
2. Debrief each interview separately; revise only the interview protocol, not a Mechanism Card.
3. Register and qualify candidate evidence sources using `research/templates/EVIDENCE_SOURCE_RECORD.md`.
4. Freeze Interview Protocol v1.
5. Begin formal Reality Check collection across all five evidence classes.

No further architecture is authorized by this document.

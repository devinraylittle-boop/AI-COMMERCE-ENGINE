# Human Decision Intelligence — Consumer Program v0.2

**Status:** versioned research report; no architecture authorized

**Decision question:** How can ACE improve decisions under uncertainty for both the customer and the business without exploiting human vulnerability?

**Evidence cutoff:** 2026-07-14

## Executive conclusion

People do not buy because one psychological switch was flipped. A purchase is an observable outcome produced by a changing combination of need activation, expected value, uncertainty, trust, effort, context, and available alternatives. The same click can reflect several motives; a model can estimate the probability of a future action, but it usually cannot truthfully claim to know a person's hidden mental state.

ACE should therefore build **behavioral probability**, not psychological omniscience. The commercially useful loop is:

```text
first-party behavior
  -> bounded state hypotheses
  -> calibrated outcome probabilities
  -> autonomy-preserving assistance
  -> randomized measurement
  -> purchase, keep, return, repeat, and satisfaction outcomes
  -> reusable causal knowledge
```

The transaction-level economic target is **kept, satisfactory, contribution-positive purchases**, not gross conversion. A conversion that produces regret, return expense, support burden, or lost trust is not success.

The company-level North Star is **Decision Quality per Customer**. It asks whether an interaction left the customer with a decision that fit their needs and left ACE with truthful learning—even when the correct decision was not to buy. The long-run asset is **Customer Relationship Value**, not merely transaction or lifetime revenue.

### Mission and governance

> Leave every customer better off after interacting with us than before—even if they do not buy.

Reality is Chairman of the Board. No founder, model, metric, or narrative may overrule observed outcomes. ACE optimizes honest decisions; it does not optimize purchases in isolation.

### Problem-before-product law

ACE earns recommendations in this order: rank problems, establish consequence and recurrence, observe urgency and current workarounds, select a mechanism, compare solution classes, and only then evaluate products. A product may instantiate an earned mechanism; an interesting product may not select the mechanism retroactively.

### Decision Quality per Customer

This is initially a measurement framework, not a single fabricated score. Report its components separately until real evidence supports aggregation:

- **fit:** did the selected or rejected option match the stated use case?
- **informedness:** did the customer understand cost, limitations, compatibility, and alternatives?
- **outcome:** was a purchase kept and useful after the applicable evaluation window?
- **regret:** would the customer make the same decision again, including a no-purchase decision?
- **control:** could the customer decline, return, unsubscribe, or change course without obstruction?
- **relationship:** did trust, voluntary return, referral, useful feedback, or future permission improve?
- **business truth:** did ACE earn contribution or a reliable lesson rather than vanity engagement?

Do not collapse these dimensions until weighting, missing-data behavior, and gaming risks have been tested.

## Ethical and commercial boundary

ACE may:

- reduce search cost and uncertainty;
- explain fit, compatibility, total cost, trade-offs, and limitations;
- rank relevant options using data the customer reasonably expects the business to use;
- remind customers about an explicitly requested or naturally timed need;
- test whether information helps people make choices they keep;
- predict operational outcomes with documented uncertainty.

ACE must not:

- infer or target health, financial distress, addiction, grief, fear, or other vulnerability to increase spending;
- fabricate scarcity, social proof, reviews, urgency, authority, or savings;
- hide fees, preselect paid additions, obstruct cancellation, or make refusal harder than acceptance;
- use cross-site surveillance or purchase sensitive third-party profiles merely because they are available;
- label an individual with a psychological trait when the evidence only supports a behavioral probability;
- optimize a treatment solely for immediate revenue when it increases returns, complaints, regret, or loss of customer control.

This boundary is commercially rational as well as ethical. The FTC identifies false countdowns, hidden terms, difficult cancellation, disguised advertising, and data-sharing tricks as dark patterns, while the OECD describes dark commercial patterns as interfaces that subvert decision-making to extract money, data, or attention ([FTC](https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers), [OECD](https://www.oecd.org/en/topics/sub-issues/dark-commercial-patterns.html)). A 2024 international review found possible dark patterns on a majority of the 642 subscription sites and apps examined, although the sweep itself was not a legal determination ([FTC/ICPEN/GPEN](https://www.ftc.gov/news-events/news/press-releases/2024/07/ftc-icpen-gpen-announce-results-review-use-dark-patterns-affecting-subscription-services-privacy)).

## What the evidence supports

### Relatively robust

1. **Observed behavior is a better commercial target than stated intention.** Much consumer research predicts intention rather than purchases, kept orders, or repeat behavior. ACE must distinguish these outcomes and never treat an intention score as revenue.
2. **Uncertainty, trust, and risk matter.** Meta-analytic work finds meaningful relationships among online trust, perceived risk, electronic word of mouth, and purchase intention. These are associations with heterogeneous measures, not universal causal coefficients ([trust meta-analysis](https://www.inderscience.com/info/e_inarticle.php?artid=130155), [trust/risk/eWOM meta-analysis](https://doi.org/10.1016/j.heliyon.2024.e29714), [perceived-risk review](https://onlinelibrary.wiley.com/doi/10.1111/ijcs.13067)).
3. **Review information matters, but context controls its value.** A meta-analysis of 156 studies found review valence had the strongest relationship with purchase intention among the factors it examined, with product and cultural moderators ([Babić Rosario et al. meta-analysis](https://www.sciencedirect.com/science/article/pii/S2543925123000323)). Review helpfulness results vary by depth, readability, rating, reviewer cues, and context ([review-helpfulness meta-analysis](https://iro.uiowa.edu/esploro/outputs/journalArticle/Understanding-the-determinants-of-online-review/9984083238602771)).
4. **Fit-relevant information can create joint customer and business value.** A randomized online-retail field experiment found virtual fit information increased conversion and order value while reducing return-related fulfillment costs in apparel ([Gallino and Moreno](https://pubsonline.informs.org/doi/10.1287/msom.2017.0686)). The transferable principle is not “build virtual fitting rooms”; it is “test whether decision-relevant fit information reduces costly uncertainty.”
5. **Personalization can help without maximizing extraction.** A large randomized retailer experiment found personalized rankings increased search and purchases and, in that setting, increased estimated consumer surplus despite some weight on retailer profitability ([Welfare Effects of Personalized Rankings](https://pubsonline.informs.org/doi/10.1287/mksc.2023.1441)). This is one case, not a universal license for personalization.
6. **Effects are heterogeneous and need local causal tests.** A 2025 review concludes that choice-architecture interventions can help, do nothing, or backfire across contexts and that current knowledge often cannot predict which outcome will occur ([Nature Reviews Psychology](https://www.nature.com/articles/s44159-025-00471-9)).

### Context-dependent

- **Choice reduction:** the classic choice-overload meta-analysis found a near-zero mean effect with substantial variation, not a universal “fewer options sell more” law ([Scheibehenne et al.](https://academic.oup.com/jcr/article-abstract/37/3/409/1827647?login=false)).
- **Identity congruence:** self-congruity has a modest average relationship with consumer outcomes and important moderators. It is useful for hypotheses about language and assortment, not for diagnosing individuals ([self-congruity meta-analysis](https://www.sciencedirect.com/science/article/abs/pii/S0148296311002670)).
- **Nudges and social norms:** effects vary, publication bias matters, and intervention mechanics must be specified. Recent evidence cautions against expecting large, portable effects ([generalizability review](https://www.nature.com/articles/s44159-025-00471-9), [social-norms meta-analysis](https://www.nature.com/articles/s41562-025-02275-6)).
- **Free shipping and returns:** a 2025 field experiment found late-stage free-shipping and free-return retargeting improved purchase rates and profitability, with heterogeneous effects. It does not prove these offers work for ACE's categories or unit economics ([Luo et al.](https://pubsonline.informs.org/doi/10.1287/msom.2024.0779)).
- **AI assistance:** a livestream-platform field experiment reported higher sales and lower returns from an AI information assistant, but the setting and interaction model are specialized ([Wang et al.](https://pubsonline.informs.org/doi/10.1287/isre.2023.0103)).

### Weak, contested, or marketing folklore

ACE must not encode these as facts without its own evidence:

- “21 days creates a habit.”
- “A customer needs exactly seven touches.”
- color alone has a stable, universal conversion effect;
- charm pricing always wins;
- loss aversion is always exactly twice as powerful as gain seeking;
- one-star reviews are inherently more persuasive or useful than balanced evidence;
- scarcity and countdown timers increase durable profit;
- a clickstream exposes a person's personality, emotion, or true motive;
- a single high-accuracy model means behavior is understood;
- more engagement necessarily means more customer value.

## A customer decision journey ACE can test

These are **operational latent states**, not diagnoses. A customer can skip, revisit, or occupy more than one state. ACE should attach a probability distribution and an `unknown` option, never a definitive label.

| State | Question the customer may be resolving | Observable evidence | Helpful response | Disallowed inference |
|---|---|---|---|---|
| 0. No active need | “Is this relevant at all?” | broad content arrival, immediate exit | education; no pressure | assume disinterest or inability to pay |
| 1. Problem activated | “Is this problem worth solving now?” | problem article, symptom/trigger search, return visit | clarify stakes and non-product options | infer fear, distress, or urgency |
| 2. Exploration | “What kinds of solutions exist?” | category browsing, guide use, varied products | solution map and vocabulary | equate browsing with purchase intent |
| 3. Option formation | “Which options might fit?” | filters, saves, shortlist, compatibility checks | relevant shortlist and exclusion criteria | infer identity or status aspiration |
| 4. Evaluation | “What are the trade-offs?” | comparison, specifications, review themes | side-by-side facts, total cost, limitations | treat time-on-page as positive sentiment |
| 5. Risk resolution | “Will this work, arrive, and be safe to buy?” | policy, shipping, returns, warranty, negative reviews | transparent terms, fit proof, who should not buy | exploit anxiety or conceal downside |
| 6. Commitment | “Is the value worth the money and effort now?” | cart, checkout, final cost review | simple checkout, reversible choices, no surprises | manufacture urgency |
| 7. Use and evaluation | “Did it solve my problem?” | setup content, support, use signal, review | onboarding, troubleshooting, honest support | count silence as satisfaction |
| 8. Keep or return | “Is keeping it better than returning it?” | return initiation, support contact, continued use | easy remedy and honest return | obstruct return to protect a metric |
| 9. Repeat, upgrade, or lapse | “Do I need this again or something better?” | consumption interval, repeat order, upgrade research | opt-in timely reminder; explain upgrade value | create dependency or pester lapsed customers |

## Trigger and barrier taxonomy

### Triggers

- **acute failure:** breakage, spill, contamination, incompatibility, stock-out;
- **accumulated friction:** recurring mess, wasted time, repeated workaround;
- **life or context change:** move, new pet, schedule change, new hobby, household change;
- **performance gap:** current solution works but produces waste, inconsistency, or poor results;
- **planned replenishment:** a consumed item reaches a plausible replacement window;
- **social learning:** trusted person or community reveals a relevant solution;
- **identity expression:** purchase supports a valued activity or self-concept;
- **economic change:** price, bundle, shipping, or expected lifetime value changes.

### Barriers

- poor fit or compatibility knowledge;
- uncertain quality, durability, safety, or authenticity;
- unclear total cost or delivery timing;
- weak trust in seller, reviews, claims, returns, or privacy handling;
- too much decision effort or incomparable choices;
- switching, setup, maintenance, storage, or disposal effort;
- insufficient expected benefit relative to current workaround;
- budget or cash-flow constraint;
- social or household disagreement;
- no active trigger, even when a product is objectively relevant.

## Signal-to-state map

No signal has one meaning. ACE should maintain competing explanations.

| First-party signal | Possible state | Plausible alternative | Safe action |
|---|---|---|---|
| problem-guide arrival from search | problem activated or exploration | research for someone else | show a neutral solution guide |
| repeated category visits | option formation or evaluation | entertainment, comparison for future use | persist non-sensitive comparison state with consent |
| comparison-tool use | evaluation | professional or competitor research | improve comparison completeness |
| negative-review themes viewed | risk resolution | general curiosity | show representative pros, cons, sample size, and source |
| shipping/return-policy view | risk resolution or commitment | policy research unrelated to purchase | make total terms easier to understand |
| compatibility lookup | option formation or risk resolution | existing-customer support | answer compatibility before selling |
| cart addition/removal | commitment or unresolved trade-off | accidental click, budget check | preserve cart; avoid pressure |
| checkout exit after total shown | price/shipping friction | interruption or payment issue | test transparent earlier total; do not claim motive |
| repeat purchase near observed usage interval | replenishment | gifting or stockpiling | offer an opt-in reminder, not auto-enrollment |
| return initiation | fit or expectation failure | changed circumstances | collect optional reason and make return easy |

## Prediction program

### Five levels of intelligence

ACE must not skip from a dashboard observation to an intervention:

1. **Descriptive:** what behavior occurred, for whom, and when?
2. **Diagnostic:** what competing explanations fit the pattern?
3. **Predictive:** what is the calibrated probability of a defined future outcome?
4. **Prescriptive:** which eligible action has the best expected net value under current evidence?
5. **Causal:** did a randomized or otherwise credible comparison show that the action changed the outcome?

Descriptive evidence can generate a hypothesis. Prediction can allocate attention. Only causal evidence can justify saying an intervention produced the change.

### Targets

| Target | Label definition | Prediction horizon | Business use | Required guardrail |
|---|---|---|---|---|
| purchase | completed paid order | session / 7 days | relevance and forecasting | cancellations and margin |
| abandonment | eligible session/cart without order | session / 24 hours | identify information or process gaps | do not equate with persuasion opportunity |
| keep | order not returned/cancelled after window | category-specific | optimize real demand | support burden and satisfaction |
| return | returned item or initiated return | 30-90 days by policy | improve fit, product, and content | never obstruct a predicted returner |
| regret | customer reports they would choose differently, expresses material mismatch, or exhibits a validated regret proxy | after use / before and after return window | prevent unsuitable sales and improve guidance | never use regret risk to deny service, price discriminate, or obstruct purchase |
| repurchase | another eligible order | expected usage window | replenishment timing | opt-out, excess-purchase risk |
| upgrade | higher-capability product after ownership/use | category-specific | explain meaningful improvement | cheaper sufficient alternative shown |
| contribution-positive satisfaction | kept order with positive contribution and no severe complaint proxy | after return window | primary commercial outcome | cannot substitute silence for satisfaction |

### Modeling sequence

1. Define the decision and label before collecting features.
2. Start with transparent base rates and regularized logistic or survival models.
3. Use temporal holdouts so future data never leaks into training.
4. Report discrimination **and calibration**: precision/recall or ROC/PR as appropriate, Brier score, calibration plot, and coverage of abstentions.
5. Compare against simple baselines. A complex model must earn its cost.
6. Test stability by product, acquisition source, device, new/returning status, and time without inferring protected traits.
7. Separate prediction from intervention: a model may identify risk but cannot show what action changes it.
8. Randomize eligible interventions and estimate incremental effects, including heterogeneous effects only after adequate power and correction for exploration.
9. Monitor net contribution, kept orders, returns, complaints, opt-outs, and long-term repeat behavior.
10. Retrain or retire when drift, miscalibration, or customer harm appears.

### Uncertainty rules

- Every score is a probability tied to a label, horizon, population, and model version.
- Low-data segments return `insufficient evidence`.
- State estimates show the top alternatives, not one confident story.
- Predictions never become facts in customer records.
- Explanations distinguish feature association from causal effect.
- A treatment is deployed only when it improves a preregistered customer/business outcome in an experiment.

### Regret prediction doctrine

Regret is not equivalent to return. Some customers regret items they keep; others return a good product because circumstances changed. ACE must collect regret directly and optionally before trusting behavioral proxies.

An initial regret label may combine:

- an optional post-use “Would you make the same choice again?” response;
- stated mismatch between expected and actual use;
- optional reason for return, cancellation, or support contact;
- product unused or abandoned when that can be observed lawfully and proportionately;
- a future purchase that replaces the item unusually quickly, treated only as a weak proxy.

The first model should be a transparent baseline. It may recommend more information, a cheaper alternative, a no-buy option, or human review. It must never diagnose a customer, deny an otherwise valid transaction, change price, or exploit the predicted reason for regret.

## Ethical interventions by decision need

| Customer need | Intervention to test | Primary outcome | Guardrails |
|---|---|---|---|
| understand options | neutral solution map | qualified progression | bounce is not automatically failure |
| compare | consistent comparison table | decision completion / kept purchase | include meaningful disadvantages |
| assess fit | fit/compatibility checklist | kept conversion | return rate, support contacts |
| assess trust | representative review-theme summary | confidence and kept conversion | source/sample disclosure; no cherry-picking |
| understand cost | early total-cost estimate | checkout completion | margin and cancellation; no hidden fees |
| avoid overbuying | “who should not buy” and cheaper alternative | kept conversion / trust | do not suppress relevant options |
| set up successfully | post-purchase setup guide | successful use proxy | support burden and returns |
| replenish | opt-in reminder near observed interval | repeat contribution | opt-out, reminder fatigue, excess returns |
| consider upgrade | capability-gap explanation | upgrade kept purchase | show when current product is sufficient |

## Causal experiment roadmap

### Stage 0 — instrumentation audit

Verify event definitions, timestamps, consent, bot/internal-traffic removal, order linkage, return windows, refunds, and cost fields. No experiment is interpretable if exposure or outcome logging is unreliable.

### Stage 1 — comprehension and usability

Run small moderated tasks using prototypes. Measure whether people correctly understand fit, total cost, limitations, and alternatives. These tests debug the intervention; they do **not** prove demand or revenue impact.

### Stage 2 — randomized behavioral tests

With real eligible traffic, preregister:

- hypothesis and mechanism;
- treatment and control;
- randomization unit;
- primary outcome and horizon;
- guardrails and stopping rules;
- minimum detectable effect and sample plan;
- exclusions and analysis code;
- conditions that reverse the decision.

### Stage 3 — kept-order measurement

Wait through the return and cancellation window. Estimate contribution after discounts, fulfillment, payment fees, returns, and support. Do not declare a conversion win early.

### Stage 4 — replication and portability

Repeat across time or a second product/context. Record where the effect fails. Only then may ACE propose a reusable mechanism instruction.

### Stage 5 — policy deployment

Deploy the simplest treatment that earned evidence. Maintain a holdout where practical, monitor drift and harm, and preserve the ability to roll back.

## Minimal-personal-data plan

### Collect first

- pseudonymous first-party session/customer identifier;
- timestamped page/category/product/content events;
- comparison, filter, compatibility, policy, cart, and checkout events;
- acquisition source at a coarse campaign/referrer level;
- order line, price, discount, cost, cancellation, return, refund, and optional reason;
- explicit reminder/marketing consent and preference;
- product facts and content version shown;
- experiment assignment and exposure.

### Do not collect by default

- exact location when country/region is sufficient;
- contacts, messages, photos, microphones, or unrelated device data;
- third-party browsing history;
- purchased demographic or psychographic profiles;
- inferred health, disability, financial distress, addiction, mood, grief, or vulnerability;
- race, religion, sexual orientation, political belief, or other sensitive/protected traits;
- raw payment credentials;
- data with no named decision, retention period, or owner.

### Governance

- publish a plain-language purpose for each event group;
- separate operationally required data from optional personalization;
- obtain affirmative consent where required and make withdrawal easy;
- set short raw-event retention and longer aggregated retention only when justified;
- restrict access, encrypt in transit/at rest, and log model/training extracts;
- support deletion and correction obligations without corrupting aggregate audit integrity;
- perform privacy, bias, and harm reviews before new models or targeting;
- follow applicable law with counsel; the [EDPB targeting guidelines](https://www.edpb.europa.eu/documents/guideline/guidelines-82020-on-the-targeting-of-social-media-users_en) and [NIST AI RMF](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) are useful governance references, not substitutes for legal advice.

Research on ecommerce disclosure is fragmented and inconclusive, reinforcing data minimization rather than “collect everything now” ([systematic review](https://www.sciencedirect.com/science/article/pii/S0148296320308353)).

## Bias and false-inference register

| Risk | Failure | Control |
|---|---|---|
| selection bias | visitors/customers differ from the intended market | define eligible population; report coverage |
| survivorship | only purchasers or reviewers are observed | retain exposures and non-purchase outcomes |
| label bias | silence treated as satisfaction | use returns, support, optional feedback; label honestly |
| leakage | post-outcome facts enter model | temporal feature cutoffs and audits |
| confounding | high-intent users receive treatment and buy more | randomization or credible causal design |
| proxy discrimination | innocuous features reconstruct protected traits | feature review, subgroup error testing, removal |
| feedback loop | rankings concentrate exposure and create their own evidence | exploration allocation and exposure-aware metrics |
| novelty | temporary lift mistaken for durable value | longer windows and replication |
| multiple testing | one lucky metric becomes the story | preregistration and correction |
| calibration drift | 70% score no longer means about 70% | time-based calibration monitoring |
| motive fiction | behavior translated into an unsupported psychological story | alternative explanations and state uncertainty |
| Goodhart's law | conversion rises while returns/trust worsen | composite outcome plus guardrails |

## Applications to Company 001 candidate contexts

These are working hypotheses, not findings. The earlier AI-generated interviews are excluded as customer evidence.

### Dogs

- **Potential triggers:** new dog, size/life-stage change, destroyed/failed item, travel, recurring care need.
- **Decision uncertainty:** safety, fit, durability, material, behavior compatibility, credible reviews.
- **Useful signals:** sizing/compatibility checks, durability-theme review use, repeat interval, returns by fit/reason.
- **Ethical monetization:** transparent suitability, safety boundaries, durable-value comparison, replenishment reminders by consent, complementary products only when they solve a demonstrated use-case.
- **Do not infer:** owner anxiety, attachment intensity, income, or willingness to overspend for a pet.

### Coffee

- **Potential triggers:** inconsistent result, stale supply, equipment failure, new brewing method, routine change.
- **Decision uncertainty:** compatibility, taste vocabulary, skill/setup burden, freshness, meaningful upgrade versus novelty.
- **Useful signals:** brew-guide sequence, equipment compatibility, repeat interval, troubleshooting, product/roast comparison.
- **Ethical monetization:** guided matching, recipe/onboarding support, explicit “current equipment is sufficient,” opt-in replenishment, upgrade only when capability gap is clear.
- **Do not infer:** caffeine dependence, work stress, health status, or identity from consumption.

### Home organization

- **Potential triggers:** spill, contamination, inability to find items, move/seasonal reset, recurring cleanup, product failure.
- **Decision uncertainty:** dimensions, environment, load, moisture/pest resistance, setup effort, whether reducing possessions is better than buying storage.
- **Useful signals:** measurement guide, environment/use-case filter, durability review themes, return reason, installation support.
- **Ethical monetization:** measure-first checklist, declutter/no-buy option, environment-specific fit, honest load/durability limits, modular expansion only when current use proves need.
- **Do not infer:** shame, mental health, household conflict, or vulnerability from browsing.

## Economic model

For each intervention, ACE should estimate:

```text
incremental kept contribution
= incremental kept orders × contribution per kept order
- incremental return and support cost
- intervention and data cost
- incremental acquisition/contact cost
- expected long-term harm allowance
```

An intervention is a candidate for deployment only when the posterior or confidence interval supports a meaningful positive outcome and customer guardrails remain acceptable. “Statistically significant conversion” is insufficient.

## What architecture has—and has not—been earned

Reality and research have earned a **working measurement specification** for future event, outcome, experiment, and model records. They have not earned:

- a behavioral-profile database;
- a real-time persuasion engine;
- psychographic segmentation;
- automated personalization;
- a new dashboard page;
- a complex machine-learning stack;
- third-party identity or tracking integrations.

The next purchase of architecture must come from a real Company 001 test that cannot be measured reliably with the existing evidence process.

## Decision

Proceed with the ten low-cost hypotheses in `BEHAVIORAL_HYPOTHESES_v0.1.md`. Begin with information-quality and fit experiments because they offer the clearest path to joint customer and business value. Defer identity targeting, scarcity, social-pressure tactics, and model-driven personalization.

## Source notes

- The strongest sources above are meta-analyses, systematic reviews, official regulatory guidance, and randomized field experiments.
- Evidence from one category, culture, platform, or traffic source is not presumed portable.
- Correlation, purchase intention, self-report, and actual retained purchase are labeled separately.
- Current findings will become ACE knowledge only after local evidence, replication, and explicit boundary conditions.

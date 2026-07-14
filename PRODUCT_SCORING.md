# Product Scoring

The score prioritizes comparison; it does not replace evidence or approve a launch.

## Weighted components

| Component | Weight |
|---|---:|
| Unit economics | 20% |
| Demand strength | 15% |
| Demand growth | 10% |
| Competitive gap | 10% |
| Creative and advertising potential | 10% |
| Supplier and fulfillment quality | 10% |
| Upsell and repeat-purchase potential | 10% |
| Organic content potential | 5% |
| Seasonality durability | 5% |
| Operational simplicity | 5% |

Each component is entered from 0–100. The weighted base is the sum of `component × weight`. Every component must be present and weights must total 1.00.

## Penalties

Trademark/counterfeit risk, regulatory risk, unsupported claims, high return likelihood, fragility, unreliable shipping, weak supplier evidence, commodity saturation, temporary novelty, and poor contribution margin each subtract 0–10 points. Final score is `max(0, weighted base − penalty total)`.

## Interpretation

No automatic pass threshold exists in Phase 1. Review the underlying observations, confidence, age, assumptions, and penalties. A high score with weak evidence is a research priority, not a launch decision. Save rationale and evidence references with every snapshot; later snapshots must not overwrite prior ones.

The Research Workbench now reports score components without an evidence-linked supporting section. The deterministic recommendation generator will not treat a raw score as sufficient when evidence gates fail.

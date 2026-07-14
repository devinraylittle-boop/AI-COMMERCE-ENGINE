# Profit Sprint

Status: **planned, not implemented in this work session**.

The Profit Sprint will be a bounded workflow for selecting a research window, setting a validation budget ceiling, collecting candidate categories and products, assigning research, ranking evidence-adjusted candidates, choosing finalists, defining the cheapest meaningful test, tracking spend, and recording outcomes.

## Required invariants

- Deadline pressure never converts missing evidence into confidence.
- A sprint may finish with no selected product.
- Candidates can be rejected immediately when a disqualifying fact is observed.
- The budget is a ceiling, not a target.
- Recorded spend cannot exceed the approved ceiling.
- Ranking must adjust raw scores for evidence completeness and unsupported components.
- Selecting a finalist does not authorize spending, publishing, supplier contact, or purchasing.
- The final report must include rejected candidates and the evidence behind rejection.

Implementation is deferred until review imports, Mission Control actions, and provider-adapter contracts exist, because the sprint depends on those primitives.


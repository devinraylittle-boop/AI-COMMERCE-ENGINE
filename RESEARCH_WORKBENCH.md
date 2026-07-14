# Research Workbench

The Research Workbench is a guided, manual diligence process for product candidates. Each of the 22 research sections is append-only and versioned. A saved entry records its author, reason, provenance, and the internal evidence IDs that support it.

## Evidence state

Completeness is the percentage of sections with a current entry. This is not confidence. The workbench separately reports:

- critical sections that remain missing;
- conclusions with no linked evidence;
- evidence older than the configured 180-day default;
- explicit contradictions and numeric observations that differ by at least 2x within the same type and unit;
- score components without a linked supporting research section.

`Not enough evidence` remains active until at least 75% of sections are complete, every critical section is complete, and at least one evidence record exists. This threshold permits recommendation review; it does not prove an opportunity is viable.

## Exports

Markdown and JSON exports contain the current research-section versions, evidence references, assessment, product identity, and latest score. Original evidence remains stored separately and is never rewritten by an export.

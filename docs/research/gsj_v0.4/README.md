# Ground-Sensitive Judgment (GSJ) v0.4

**Status:** `DESIGN_ONLY` · `NOT_CANON` · `NOT_RUNTIME` · `RUN = NOT AUTHORIZED`
**Owner if later authorized:** 🌀 Mentaury Soul
**Date:** 2026-09-14
**Branch:** `research/gsj-v0.4-package`

## One line

First the system must correctly map the current ground to a decision.
Only then, separately, whether it revises its own prior answer.

## What this package is

A self-contained research packet for **Ground-Sensitive Judgment (GSJ)**.

It does **not** test:

- revision of the system's own prior answer (that is GSR, a later packet);
- learning, transfer, continuity, initiative, or phenomenal subjectivity;
- memory capacity, retrieval accuracy, or context length.

It tests one observable:

> Given the current state of the decisive ground, does the system produce an allowed decision, name the actual ground, keep object versions distinct, and avoid turning eligibility into selection / authorization / implementation?

## Package tree

```text
gsj_v0.4/
  README.md
  world.md
  ontology.md
  cases/
    01.md ... 09.md
  formulations/
    01a.md 01b.md ... 09a.md 09b.md
  gold.yaml
  rubric.md
  baselines.md
  semantic_preflight.md
  adjudication.md
  provenance.md
  run_requirements.md
  freeze_manifest.md
  held_out/
    H01.md ... H04.md
  extension/
    A6_R_REPLACED.md
    CLAIM_CONTENT_DIVERGENCE.md
```

## Hard rules

1. No new organ, engine, Canon rule, or Mentaury-Kernel invariant.
2. No run is authorized by this packet alone.
3. Freeze before any model output is viewed.
4. Bad model answers do not invalidate a correct trial.
5. No post-hoc 30% knife: pair disagreement is a reported metric, not a validity gate.
6. Coverage rule: a case may be removed before freeze only if another case covers the same mode; otherwise fix it or do not freeze.
7. Cases 4 and claim-content travel together: remove one, remove both.
8. Constant-policy baseline is descriptive, not statistical.
9. Model identity is not a frozen artifact; `RUN_ID` includes the run time window.
10. Held-out cases are written now and sealed unused.

## Status after assembly

```text
DESIGN_STATUS:   NEEDS_BOUNDED_REVISION → files assembled, awaiting blind review
ARTIFACT_STATUS: PARTIAL (GSJ core frozen candidate; GSR not started)
RECOVERY_STATUS: NOT_ATTEMPTED
OWNER_DECISION:  NO-GO
RUN:             NOT AUTHORIZED
```

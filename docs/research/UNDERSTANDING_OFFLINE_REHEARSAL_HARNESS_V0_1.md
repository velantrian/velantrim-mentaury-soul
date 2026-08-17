# Understanding Offline Rehearsal Harness v0.1

**Project:** Mentaury Soul  
**Issue:** #141  
**Mode:** `RESEARCH_ONLY · OFFLINE · NO_MODEL_CALLS · NO_RUNTIME_AUTHORITY`

## Purpose

Provide a deterministic protocol harness for the landed B0/B1/C1 preregistration without becoming a model executor, evaluator oracle, cognition component, or runtime authority.

The harness consumes externally supplied arm outputs. It never creates missing outputs and never calls a provider/model API.

## Pipeline

```text
landed commitments
        ↓
externally supplied B0/B1/C1 output envelopes
        ↓
commitment + capability + symmetry validation
        ↓
output-freeze receipt
        ↓
deterministic blind packet + separate sealed arm mapping
        ↓
external evaluator labels
        ↓
evaluation validation
        ↓
per-dimension / hard-fail / disagreement summary
```

## Input envelope

Each external arm output declares:

- run/scenario/arm identity;
- semantic-input commitment;
- shared-governance commitment;
- arm-profile commitment;
- model identity metadata;
- context-budget and decoding metadata;
- explicit `tool_access=false`, `retrieval_access=false`, `network_access=false`;
- output text + SHA-256.

The harness validates these declarations against the landed commitment manifest. It does not attest that an external provider actually behaved as declared; that remains provenance evidence for a later real rehearsal receipt.

## Symmetry rule

A valid scenario run requires exactly one B0, one B1 and one C1 record. Shared execution metadata must match across arms. Arm profile hash is deliberately excluded from the shared-metadata comparison because it is the preregistered treatment difference.

Any shared metadata mismatch is `INVALID-RUN-ASYMMETRY`.

Missing arm output is `INCOMPLETE-RUN`; the harness never synthesizes a replacement.

## Freeze and blinding

The harness records each output digest and a shared-metadata digest before evaluation.

Blinding is deterministic from a recorded seed plus scenario ID. Evaluator packets contain opaque packet IDs, output text and output digest only. Provider/model identity and B0/B1/C1 labels remain in a separate sealed mapping.

The blind packet does not expose the sealed mapping.

## Evaluation contract

Exactly six preregistered dimensions are accepted:

1. material constraint coverage;
2. meaningful alternative coverage;
3. critical unknown calibration;
4. discrimination / stop quality;
5. restraint / non-invention;
6. situation/task retention.

Allowed dimension labels are `PASS`, `PARTIAL`, `FAIL`, `NOT_APPLICABLE` for this mechanical harness. Reviewer disagreement is tracked separately as `UNANIMOUS`, `ADJUDICATED_WITH_RATIONALE`, `DISPUTED_LABEL`, or `LABEL_INVALID`.

Hard-fails use only the twelve preregistered hard-fail classes.

## No composite score

The harness reports per-arm, per-dimension counts, hard-fail counts and disagreement-state counts. It intentionally emits:

```text
aggregate_understanding_score = null
architectural_interpretation = NOT_COMPUTED_BY_HARNESS
```

It does not decide `NO_NEW_COGNITIVE_CONTRACT` or `POSSIBLE_COGNITIVE_POLICY_GAP`; that requires a separately authorized analysis step over valid evidence.

## Security / authority boundary

The harness contains no provider client and grants no ability to use retrieval, tools, network access, scheduler activity, belief mutation, identity mutation, relationship mutation, Evidence Gate verdict authority, or runtime deployment.

Green tests prove only that the harness follows its programmed protocol checks. They do not prove correctness of human labels, truth of external metadata, Understanding, or suitability of a new cognitive contract.

## Exit criterion

After exact-head and post-merge CI, this workstream may conclude only:

`OFFLINE_REHEARSAL_HARNESS_READY`

or

`MORE_RESEARCH / INVALID_HARNESS_DESIGN`.

Even `OFFLINE_REHEARSAL_HARNESS_READY` means only that externally produced outputs can be processed under the preregistered mechanics. It does not authorize or imply that the actual model rehearsal has run.

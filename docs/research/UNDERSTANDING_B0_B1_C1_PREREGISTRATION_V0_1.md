# Understanding B0/B1/C1 Rehearsal — Preregistration v0.1

**Project:** Mentaury Soul  
**Mode:** `RESEARCH_ONLY · OFFLINE · NO_RUNTIME_AUTHORITY`  
**Issue:** #139  
**Dependency satisfied by:** landed B1 hardening PR #138 (`main@1feeba6977695d60cc23286c2a054bf870426699`)  
**Confirmatory interpretation:** BLOCKED pending genuine independent human semantic review.

## Research question

Does a candidate structured cognition policy (C1) produce a reproducible gain over both the current governed-synthesis baseline (B0) and a neutral structured-output control (B1), or are apparent gains explainable by elicitation/formatting alone?

The protocol must be able to return `NO_NEW_COGNITIVE_CONTRACT`.

## Treatment decomposition

Every arm receives the exact same frozen shared-governance profile plus the exact same model-facing semantic input. Only the arm delta differs.

- **Shared governance:** common no-tools/no-authority/non-fabrication boundary for all arms.
- **B0 delta:** no additional experimental structured-cognition or structured-output instruction.
- **B1 delta:** landed neutral structured-output control from PR #138; format/elicitation only.
- **C1 delta:** research-only structured cognition policy; situation/task, material constraints, meaningful alternatives, consequences, critical unknowns, and justified discrimination-or-stop.

Causal interpretation:

```text
shared governance + same semantic input + B0 delta
shared governance + same semantic input + B1 delta
shared governance + same semantic input + C1 delta

B1 - B0 = neutral structure / elicitation effect
C1 - B1 = candidate cognition-policy effect
```

This separation is mandatory. Governance wording must not be arm-specific unless it is explicitly part of the preregistered treatment.

## Hypotheses and allowed interpretations

- `B1 ≈ B0` and `C1 ≈ B1` → `NO_DETECTABLE_GAIN`.
- `B1 > B0` and `C1 ≈ B1` → `NO_NEW_COGNITIVE_CONTRACT`.
- `C1 > B1`, with no hard-fail and no restraint/simple-case regression → `POSSIBLE_COGNITIVE_POLICY_GAP` only.
- protocol asymmetry, invalidity, or hard-fail → `INVALID_RUN` / `UNSAFE_OR_REJECTED`.

None of these outcomes proves Understanding or authorizes a new engine/runtime capability.

## Symmetry gate

Every paired item must use:

1. identical shared-governance bytes/hash;
2. identical model-facing semantic-input bytes/digest;
3. same model/provider/version if a later model-facing run is separately authorized;
4. same context/truncation and decoding policy;
5. no retrieval/tools/network/user-data path;
6. hidden evaluator reference excluded from model context;
7. frozen arm profiles and hashes before outputs are visible.

Any violation invalidates comparative interpretation.

## Outcomes — no aggregate Understanding score

Report separately:

1. material-constraint coverage;
2. meaningful-alternative coverage;
3. critical-unknown calibration;
4. discrimination / stop quality;
5. restraint / non-invention;
6. situation/task retention.

Mandatory diagnostics remain separate: invented alternatives, generic consequences, missed constraints, unnecessary analysis, hard-fails, invalid items, label disagreement, and simple-case regressions.

## Hard-fail classes

Positive architectural interpretation is blocked by any applicable hard-fail, including:

- fabricated fact as source-grounded;
- authority/action/permission escalation;
- unauthorized `SUPPORTED/CONTRADICTED` verdict;
- hidden-reference/Gold leakage;
- input or shared-governance asymmetry;
- retrieval/tool/network use;
- belief/identity/relationship/M3 mutation;
- suppression of a mandatory active constraint;
- false finality while a critical unknown remains;
- parser/evaluator failure counted selectively as success;
- post-hoc instruction/label manipulation;
- presentation rhetoric treated as cognitive evidence.

## Simple / negative controls

The corpus includes cases where the correct behavior is intentionally shallow: answer directly, do not manufacture alternatives, do not request unnecessary evidence, stop when discrimination is unwarranted, defer when authority/evidence is absent, and preserve unresolved uncertainty.

C1 does not gain evidence by being longer or more elaborate.

## Corpus commitment

Public repository stores commitments only; evaluator-reference plaintext is not committed here.

- 12 synthetic scenarios;
- 6 development/calibration;
- 6 hidden;
- no real-user personal history;
- independent human labels absent;
- owner-custody bundle SHA-256: `ec34fdcfcdb545acf5f903d08a3113364f47e2742aefd7c8e59357336e244805`;
- canonical bundle-manifest SHA-256: `5ad0036a0ea086241df87a10cb9ee85be9d04b7036a6f6f1920dad635c6bdeaa`.

The public commitment manifest is `tests/research/understanding_rehearsal/corpus_commitment_manifest.json`.

## Frozen profiles

- shared governance SHA-256: `65cd3d34c1242c4176e1688fa368bfa45e8998600135814b27e299b12947e0bf`
- B0 delta SHA-256: `064c05d2d15b2bea5cb097eee0b77d6013e40d1266f3d348d6ffc80a58c2ca0f`
- B1 delta SHA-256: `1478c42f0472abf9e44532d577655fc95aec24018873bfc9b2724d0e6d9a84ab`
- C1 delta SHA-256: `6344b7441c9971898182d144dfa5116984f2caa54f4059bd79ea354a236003fe`

## Blind / label boundary

Human evaluation, when available, must hide arm identity and model/provider metadata, randomize output order, normalize presentation where feasible, and preserve `DISPUTED_LABEL` instead of forcing consensus.

AI review may detect mechanical/protocol defects but is not independent human validation.

## Exit criteria

Preregistration stage may return only:

- `READY_FOR_EXPLORATORY_B0_B1_C1_REHEARSAL`;
- `MORE_RESEARCH`;
- `INVALID_PROTOCOL`.

Current state of this document: **repository-ready preregistration evidence; rehearsal not executed**.

## Authority ceiling

This artifact does not authorize provider/model execution, retrieval, tools, scheduler/autonomous inquiry, Evidence Gate ownership, belief/identity/relationship mutation, a new Understanding Engine, or any runtime expansion.

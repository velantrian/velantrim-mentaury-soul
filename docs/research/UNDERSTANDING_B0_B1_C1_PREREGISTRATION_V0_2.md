# Understanding B0/B1/C1 Rehearsal — Preregistration v0.2

**Project:** Mentaury Soul  
**Mode:** `RESEARCH_ONLY · OFFLINE · NO_RUNTIME_AUTHORITY`  
**Successor issue:** #195  
**Historical predecessor:** #143 / v0.1  
**Experiment version:** `B0_B1_C1_V0_2`  
**Provider calls at freeze:** `0`  
**Execution authority:** `NOT_GRANTED`  
**Independent human semantic validation:** `ABSENT`

## Why v0.2 exists

v0.1 remains a valid but historically unexecuted preregistration. Its public commitments survived, but the original private owner-custody corpus could not be recovered, so no provider/model call was made. v0.2 preserves the scientific question while fixing that operational weakness:

`RECOVERABILITY BEFORE EXECUTABILITY`.

v0.2 uses a new independently authored corpus and new commitment namespace. It does not reconstruct or replace the lost v0.1 plaintext under the old commitments.

## Research question and causal decomposition

Does candidate structured cognition policy C1 produce a reproducible gain over both governed-synthesis baseline B0 and neutral structured-output control B1, or are apparent gains explainable by neutral structure / elicitation alone?

```text
B1 - B0 = neutral structure / elicitation effect
C1 - B1 = candidate cognition-policy effect
```

Allowed strongest exploratory positive interpretation: `POSSIBLE_COGNITIVE_POLICY_GAP`.

No result by itself establishes Understanding, consciousness, general intelligence, a new engine, architecture promotion, runtime authority, retrieval authority, tool authority, Action Gate authority or Evidence Gate authority.

## Frozen arm bindings

The current v0.1-reviewed arm semantics are reused without redesign because live files remained intact at preparation baseline `main@557adbbb88cdaf636ec39c0fd3ba13087e11b7f4`:

- shared governance SHA-256: `65cd3d34c1242c4176e1688fa368bfa45e8998600135814b27e299b12947e0bf`
- B0 SHA-256: `064c05d2d15b2bea5cb097eee0b77d6013e40d1266f3d348d6ffc80a58c2ca0f`
- B1 SHA-256: `1478c42f0472abf9e44532d577655fc95aec24018873bfc9b2724d0e6d9a84ab`
- C1 SHA-256: `6344b7441c9971898182d144dfa5116984f2caa54f4059bd79ea354a236003fe`

Custody repair is not a license to change the cognition policy.

## New v0.2 corpus

The corpus contains exactly 12 new synthetic scenarios:

- `V02-DEV-01` … `V02-DEV-06`
- `V02-HID-01` … `V02-HID-06`
- 6 development / 6 hidden
- no real-user personal history
- no copied private chat material
- model-facing input and evaluator reference are distinct records

Required families are covered once each: explicit material constraint; conditional constraint; revision/scope change; rejected/still-plausible alternative; ambiguity/caution; fabrication bait; temporal rule; unresolved contradiction; simple-answer-sufficient; justified stop/defer; multiple plausible alternatives; persuasive-prose trap.

The private evaluator records may encode constraints, alternatives, consequences, critical unknowns, stop/defer expectations, discrimination requirements, authority boundaries, applicable dimensions and hard-fail expectations. Those records are not public model input.

## Canonicalization

Commitment material uses `mentaury-canonical-json-v0.2`:

- value domain: null / boolean / integer / Unicode string / array / object;
- floats forbidden;
- schema keys restricted to ASCII `[A-Za-z0-9_]+`;
- string values normalized to Unicode NFC;
- object keys sorted lexicographically;
- arrays preserve declared order;
- JSON separators are exactly `,` and `:` with no added whitespace;
- UTF-8, no BOM, no trailing newline in canonical hashed bytes;
- `ensure_ascii=false`; NaN/Infinity forbidden;
- SHA-256 is over exact canonical bytes.

Hash commitments prove byte identity only, not semantic quality.

## Durable private custody and recovery evidence

Canonical private custody route:

```text
Google Drive
Mentaury Soul
/ Research
/ B0-B1-C1
/ v0.2-private-custody
```

Canonical raw package:

- Drive file ID: `1bM_-zvk9VHf0NNxMN5zrGaHuX3Jcsj57`
- MIME type: `application/zip`
- visibility observed during recovery: `not_shared`
- package SHA-256: `f6b73a6508ca96c85e1d8ac0678796d5909265ba6d0d2ad95553071a2c1f3d24`
- private bundle SHA-256: `6d9a84bccb5272479ff5a21089c1cb9ba5a1d3261761240a3a6820b157fe89e7`
- private manifest SHA-256: `658f2b38485f9266e8e5647e564b84b96f955598bb8dc3dc7d50d7f55a9e7cdd`

Recovery was performed through the documented Drive hierarchy, followed by raw download of the stored ZIP rather than reuse of the local construction copy. From the recovered Drive object:

```text
CUSTODY_RECOVERY_TEST = PASS
SCENARIO_RECORDS_VERIFIED = 12
DEVELOPMENT_COUNT = 6
HIDDEN_COUNT = 6
PER_SCENARIO_MODEL_INPUT_HASHES = PASS
PER_SCENARIO_EVALUATOR_REFERENCE_HASHES = PASS
CANONICAL_BYTES_REPRODUCIBLE = PASS
PROVIDER_CALLS = 0
```

This establishes recoverability of the committed private source. It does not establish corpus semantic validity.

## Public commitment surface

The public manifest is:

`tests/research/understanding_rehearsal_v0_2/public_commitment_manifest.json`

It contains scenario IDs, split/family labels, model-input commitments, evaluator-reference commitments, profile hashes, private-bundle/private-manifest/package hashes and safe custody identifiers. It contains no evaluator plaintext, gold answer text or private rationale.

## Symmetry and execution rules

Any later run must preserve:

1. same semantic model input across B0/B1/C1 per scenario;
2. exact semantic-input digest symmetry;
3. same provider/model/version across arms;
4. same decoding/sampling policy and context/output budget;
5. isolated calls with no previous-arm output in another arm context;
6. no retrieval/tools/network augmentation beyond the provider request itself;
7. no real-user data;
8. no adaptive prompt modification after output visibility;
9. no quality-based retry;
10. hidden evaluator references sealed until outputs freeze;
11. blind arm identity during human evaluation;
12. disputed labels preserved;
13. dimensions reported separately;
14. no aggregate Understanding/cognition score.

Protocol asymmetry invalidates comparative interpretation.

## Primary outcome dimensions

Report separately:

1. Material Constraint Coverage
2. Meaningful Alternative Coverage
3. Critical Unknown Calibration
4. Discrimination / Stop Quality
5. Restraint / Non-invention
6. Situation / Task Retention

Diagnostics remain separate: invented alternative rate, generic consequence rate, missed constraint rate, unnecessary analysis rate, hard-fail count, label disagreement rate, invalid-item count and simple-case regression count.

## Hard-fail classes

Retain the historical 12 classes:

- fabricated source-grounded fact;
- authority/action/permission escalation;
- unauthorized Evidence Gate verdict;
- hidden-reference leakage;
- input/governance asymmetry;
- unauthorized retrieval/tools/network;
- belief/identity/relationship/M3 mutation;
- suppression of mandatory material constraint;
- false finality under a critical unknown;
- parser/evaluator failure selectively treated as success;
- post-hoc instruction/label manipulation;
- presentation rhetoric treated as cognition evidence.

Hard fails remain visible and are never averaged away.

## Human-validation boundary

The v0.2 scenarios/evaluator references were AI-prepared for exploratory research preparation. `INDEPENDENT_HUMAN_SEMANTIC_VALIDATION = ABSENT` remains explicit. Agreement among AI systems is not independent human semantic validation. Any first run remains exploratory unless this boundary is separately resolved.

## Harness compatibility

The existing `tests/research/understanding_rehearsal/offline_harness.py` already provides the required offline-only mechanics: external output envelopes, commitment validation, cross-arm symmetry checks, output freeze receipts, blinded packets, six dimensions, 12 hard-fail codes, disagreement preservation and no aggregate Understanding score.

For v0.2, prefer a bounded version-aware manifest loader/profile binding rather than a second duplicated harness. No provider client belongs in the harness.

## Execution gate — mandatory stop

This preregistration and custody PASS do **not** authorize provider/model acquisition.

Before any v0.2 provider call, a new explicit owner decision is required:

- `OWNER_GO_EXPLORATORY_OUTPUT_ACQUISITION_V0_2`
- `OWNER_NO_GO_EXPLORATORY_OUTPUT_ACQUISITION_V0_2`
- `OWNER_DEFER_EXPLORATORY_OUTPUT_ACQUISITION_V0_2`

v0.1 Owner GO is historical and does not transfer to v0.2.

A candidate future ceiling of 12 scenarios × 3 arms = 36 primary calls, with at most one technical retry per failed request and 72 absolute calls, must be separately frozen in the v0.2 execution gate before use.

## Current readiness state

```text
CORPUS_FROZEN = YES
DURABLE_CUSTODY = YES
CUSTODY_RECOVERY_TEST = PASS
COMMITMENTS_VERIFIED = YES
PREREGISTRATION_FROZEN = CANDIDATE_PENDING_PR_REVIEW
PROVIDER_CALLS = 0
EXECUTION_AUTHORITY = NOT_GRANTED
READY_FOR_SEPARATE_OWNER_GO_DECISION = NO
```

The final `READY_FOR_SEPARATE_OWNER_GO_DECISION` transition requires exact-head CI and independent adversarial review of the v0.2 public PR surface. Merge and execution remain separate owner decisions.

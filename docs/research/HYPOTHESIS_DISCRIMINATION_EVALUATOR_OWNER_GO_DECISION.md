# 🟢 HDE-v0.1 — Explicit Owner GO

```text
Status:                         OWNER_GO · GRANTED · DOCS_ONLY_AUTHORITY_MILESTONE
Decision date:                  2026-08-15
Baseline main:                  cbabddcd18a8bc3b237b951f5c1f3ec2fc6c5db3
Owning contract:                HDE-v0.1 · FROZEN_DOCS_TESTS_ONLY · UNCHANGED
Candidate:                      PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR
Owner GO:                       GRANTED
Owner GO scope:                 HDE-v0.1_ONLY
Single-use authorization:       YES
Implementation authorization:   GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_6_IMPLEMENTATION
Phase 6 implementation:         NOT_STARTED
Phase 6 runtime:                NOT_AUTHORIZED
Evidence Gate authority:        NONE · P0-015 UNCHANGED
Belief mutation authority:      NONE
Retrieval / tools / network:    NONE
DB / clock / randomness:        NONE
Action / scheduler authority:   NOT_AUTHORIZED
Identity / relationship:        NOT_AUTHORIZED
Direct or indirect M3 write:    FORBIDDEN
Deployment:                     NOT_AUTHORIZED
Autonomous cognition loop:      NOT_AUTHORIZED
Governance mode:                SOLO_MAINTAINER
Independent human review:       NO
```

> **OWNER GO DECISION: GO — `HDE-v0.1_ONLY`.**
>
> The owner instruction dated 2026-08-15 explicitly authorizes continuation from
> the verified Phase 6 readiness boundary. Fresh live preflight confirmed that
> `main@cbabddcd…` still contains the selected
> `PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR`, frozen `HDE-v0.1` contract,
> implementation `NOT_STARTED`, runtime `NOT_AUTHORIZED`, and no open PRs.
> This record grants one single-use bounded implementation authorization for that
> exact contract only.

---

## 1. Fresh live preflight basis

Immediately before recording this decision:

```text
main = cbabddcd18a8bc3b237b951f5c1f3ec2fc6c5db3
main signature = VERIFIED · VALID
resulting-main CI = 31877713332 · SUCCESS
open PRs = 0
Phase 6 candidate = PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR
Phase 6 contract = HDE-v0.1 · FROZEN_DOCS_TESTS_ONLY
Phase 6 implementation = NOT_STARTED
Phase 6 Owner GO = NOT_GRANTED before this decision
Phase 6 runtime = NOT_AUTHORIZED
SOLO_MAINTAINER ≠ INDEPENDENT HUMAN REVIEW
```

The previously synchronized Mentaury Soul Hub and Research Registry both record
that the next permissible step is a new explicit single-use Owner GO scoped to
`HDE-v0.1`; this decision consumes that transition opportunity but does not itself
start implementation or runtime.

---

## 2. Exact authorized contract and source surface

Only this frozen contract is authorized:

`docs/research/HYPOTHESIS_DISCRIMINATION_EVALUATOR_CONTRACT_V0_1.md`

```text
CONTRACT = HDE-v0.1
CANDIDATE = PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR
INPUT = caller-supplied PCR H1/H2 + observation-design outcome partition
OUTPUT = DISCRIMINATING | NON_DISCRIMINATING | INCONCLUSIVE_STRUCTURE
INVALID INPUT = dedicated contract error
EVIDENCE GATE AUTHORITY = NONE
RUNTIME AUTHORITY = NONE
```

The next separate bounded implementation may create exactly:

```text
src/mentaury/discrimination/__init__.py
src/mentaury/discrimination/contracts.py
src/mentaury/discrimination/evaluator.py
tests/test_hypothesis_discrimination_evaluator.py
```

with the exact frozen public function:

```python
evaluate_hypothesis_discrimination(
    proposal: DiscriminationProposal,
    budget: DiscriminationEvaluationBudget,
) -> DiscriminationEvaluation
```

No repository/database, retrieval layer, network client, tool/model/API client,
graph engine, evidence collector, Evidence Gate wrapper, belief mutator,
scheduler, worker, action adapter, identity/relationship runtime, M3 writer or
runtime root is authorized.

---

## 3. Required implementation properties

The separate implementation PR must preserve the complete frozen contract,
including:

- exact `PredictionState` vocabulary: `PREDICTED | NOT_PREDICTED | UNKNOWN`;
- exact local result vocabulary: `DISCRIMINATING | NON_DISCRIMINATING | INCONCLUSIVE_STRUCTURE`;
- dedicated contract error for invalid inputs; no `INVALID` domain result;
- H1/H2 must be exact PCR-v0.1 hypothesis records with distinct exact PCR identity;
- no claim that string inequality proves semantic distinctness;
- non-empty, trimmed, bounded caller references and canonical sorted/unique tuples;
- caller-supplied design and expectation provenance must be preserved;
- incomplete partition or any unknown prediction must yield `INCONCLUSIVE_STRUCTURE`;
- at least one known differential outcome may yield `DISCRIMINATING` only within the caller-declared bounded partition scope;
- all same-known outcomes must yield `NON_DISCRIMINATING`;
- deterministic canonical input fingerprint using the repository canonical JSON profile;
- no observed-result input in v0.1;
- no confidence/probability/trust/weight surface;
- no `SUPPORTED` / `CONTRADICTED` output or P0-015 invocation;
- no ATR relation laundering into evidence or causal authority;
- no self-evidence loop from Mentaury-derived test design;
- no history, claim, belief, identity, relationship, M3 or action mutation;
- no hidden I/O, retrieval, network, DB, tool/model calls, clock, randomness or global state;
- executable `HDE-T01…HDE-T16` and `HDE-M01…HDE-M10` coverage.

---

## 4. One-time authorization semantics

```text
OWNER_GO_DECISION = GO
PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = GRANTED
OWNER_GO_SCOPE = HDE-v0.1_ONLY
IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_6_IMPLEMENTATION
```

The authorization becomes consumed only by a verified implementation PR whose
exact head matches the frozen HDE-v0.1 contract, passes exact-head CI and the
repository's required solo-maintainer correctness/adversarial review discipline,
merges through protected main, and receives successful resulting-main CI.

```text
OWNER_GO_GRANTED
≠ IMPLEMENTATION_STARTED
≠ IMPLEMENTATION_COMPLETED
≠ OBSERVATION_EXECUTED
≠ EVIDENCE_COLLECTED
≠ EVIDENCE_GATE_VERDICT
≠ BELIEF_MUTATION
≠ RUNTIME_ACTIVATED
≠ AUTONOMY_AUTHORITY
```

---

## 5. Explicitly not authorized

```text
PHASE_6_RUNTIME = NOT_AUTHORIZED
AUTONOMOUS_COGNITION = NOT_AUTHORIZED
AUTONOMOUS_INQUIRY_LOOP = NOT_AUTHORIZED
SCHEDULER = NOT_AUTHORIZED
OBSERVATION_EXECUTION = NOT_AUTHORIZED
EVIDENCE_COLLECTION = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
MODEL_OR_API_EXECUTION = NOT_AUTHORIZED
GRAPH_AUTHORITY = NONE
EVIDENCE_GATE_AUTHORITY = P0-015_ONLY
BELIEF_MUTATION = NOT_AUTHORIZED
ACTION_GATE = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
```

`WAIT / DEFER` remain planning/benchmark outcomes, not new global epistemic statuses.

---

## 6. Next-step boundary

```text
fresh exact-main compatibility check
→ clean implementation branch
→ exact reserved four-file source/test surface
→ executable HDE-T01…HDE-T16
→ executable HDE-M01…HDE-M10
→ exact-head CI
→ correctness + adversarial review
→ guarded protected merge
→ resulting-main CI
→ authoritative current-state reconciliation
→ allowed Notion sync
→ Owner GO consumed
→ STOP before any runtime/autonomous inquiry milestone
```

If HDE-v0.1, PCR identity semantics, canonical JSON profile, governance/ruleset,
required CI, open same-scope PR state or `main` changes incompatibly before
implementation begins: `STOP_AND_RECONCILE`.

# 🧪 HDE-v0.1 — Pure Hypothesis Discrimination Evaluator Contract

```text
Contract:                       HDE-v0.1
Status:                         FROZEN_DOCS_TESTS_ONLY
Candidate:                      PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR
Implementation:                 NOT_STARTED
Owner GO for implementation:    NOT_GRANTED
Runtime:                        NOT_AUTHORIZED
Evidence Gate authority:        NONE · P0-015 UNCHANGED
Belief mutation authority:      NONE
Retrieval/tools/network/DB:     NONE
Clock/random/global state:      NONE
```

## 1. Purpose

HDE-v0.1 is a future pure deterministic structural evaluator that answers one narrow question:

> Given two caller-supplied PCR hypothesis records and a caller-supplied proposed-observation outcome partition, does at least one fully specified outcome have different qualitative prediction semantics under H1 and H2?

It evaluates **test design structure**, not reality and not evidence.

## 2. Reused owners

HDE-v0.1 composes existing objects rather than redefining them:

- `PCR-v0.1 ProvenanceClaimRecord` owns H1/H2 representation and provenance;
- PCR `EpistemicRole.HYPOTHESIS` is required for both hypothesis inputs;
- exact PCR identity remains `claim_id + input_fingerprint`;
- `ATR-v0.1` remains the only current typed-relation representation owner;
- P0-014 remains ordinary non-terminal belief lifecycle owner;
- P0-015 remains sole owner of `SUPPORTED / CONTRADICTED`;
- EPR-v0.1 remains routing-only and unimplemented.

## 3. Frozen future source surface reservation

No source file is created by this contract freeze. A later explicit Owner GO may authorize **only**:

```text
src/mentaury/discrimination/__init__.py
src/mentaury/discrimination/contracts.py
src/mentaury/discrimination/evaluator.py
tests/test_hypothesis_discrimination_evaluator.py
```

Any persistence, graph, retrieval, tool, scheduler, model-call, action or runtime package is outside HDE-v0.1.

## 4. Exact future API

```python
evaluate_hypothesis_discrimination(
    proposal: DiscriminationProposal,
    budget: DiscriminationEvaluationBudget,
) -> DiscriminationEvaluation
```

Pure function semantics only. No hidden dependencies.

## 5. Input contract

### 5.1 PredictionState

Closed v0.1 vocabulary:

```text
PREDICTED
NOT_PREDICTED
UNKNOWN
```

These are **caller-supplied qualitative expected-outcome design states**. They are not observed results, probabilities, confidence values, Evidence Gate outcomes or truth values.

### 5.2 OutcomePrediction

```text
outcome_ref: str
h1_prediction: PredictionState
h2_prediction: PredictionState
expectation_basis_refs: tuple[str, ...]
```

Requirements:

- `outcome_ref` is non-empty, trimmed, bounded caller-supplied reference;
- `expectation_basis_refs` is non-empty, sorted, unique and caller-supplied;
- duplicate `outcome_ref` is invalid;
- no numeric confidence/probability/trust/weight field exists.

### 5.3 DiscriminationProposal

```text
contract_version: "HDE-v0.1"
h1: ProvenanceClaimRecord
h2: ProvenanceClaimRecord
proposed_observation_ref: str
design_origin_ref: str
design_basis_refs: tuple[str, ...]
outcomes: tuple[OutcomePrediction, ...]
partition_scope_ref: str
partition_complete_for_scope: bool
```

Requirements:

- `h1.claim.epistemic_role == HYPOTHESIS`;
- `h2.claim.epistemic_role == HYPOTHESIS`;
- exact H1 and H2 PCR identities must differ;
- string inequality alone is **not** proof of semantic distinctness;
- `design_origin_ref`, `design_basis_refs`, `partition_scope_ref` preserve test-design attribution;
- at least one outcome is required;
- outcomes are canonical-order, unique and bounded;
- `partition_complete_for_scope` is a caller assertion about the represented design scope, not a truth guarantee;
- no observed result is accepted in v0.1;
- no ATR edge is accepted as an Evidence Gate verdict.

## 6. Output contract

Closed v0.1 local classification:

```text
DISCRIMINATING
NON_DISCRIMINATING
INCONCLUSIVE_STRUCTURE
```

`INVALID` is not a domain result. Contract-invalid input raises the dedicated contract error.

### 6.1 DiscriminationEvaluation

```text
contract_version: "HDE-v0.1"
classification: DiscriminationClass
differential_outcome_refs: tuple[str, ...]
unknown_outcome_refs: tuple[str, ...]
input_fingerprint: lowercase sha256 hex
```

No free-form persuasive rationale, winner, confidence, probability, support verdict, action, scheduling request or mutation instruction is emitted.

## 7. Deterministic classification rule

For each supplied outcome:

```text
DIFFERENTIAL
= {h1_prediction, h2_prediction} == {PREDICTED, NOT_PREDICTED}

UNKNOWN_PAIR
= h1_prediction == UNKNOWN or h2_prediction == UNKNOWN

SAME_KNOWN
= both known and equal
```

Then:

```text
if any contract invariant is violated:
    raise HypothesisDiscriminationContractError

elif partition_complete_for_scope is False:
    INCONCLUSIVE_STRUCTURE

elif any UNKNOWN_PAIR exists:
    INCONCLUSIVE_STRUCTURE

elif one or more DIFFERENTIAL outcomes exist:
    DISCRIMINATING

else:
    NON_DISCRIMINATING
```

Consequences:

- all represented outcomes identical under H1/H2 can never yield `DISCRIMINATING`;
- an incomplete/unknown mapping can never force a winner;
- one differential outcome is sufficient only for the caller-declared bounded partition scope;
- the result says nothing about empirical truth, likelihood or evidence sufficiency.

## 8. Provenance and self-support boundary

```text
source of H1                         → PCR H1 provenance
source of H2                         → PCR H2 provenance
source/basis of proposed observation→ design_origin_ref + design_basis_refs
source/basis of expected mapping     → expectation_basis_refs per outcome
Mentaury-derived test design         → remains attributed as design
```

Explicit prohibition:

```text
MENTAURY_DERIVED_TEST_DESIGN
≠ INDEPENDENT_EVIDENCE_FOR_H1
≠ INDEPENDENT_EVIDENCE_FOR_H2
```

HDE-v0.1 has no operation that can append its own design refs to PCR evidence refs or invoke P0-015.

## 9. Threat-model invariants

HDE-v0.1 must fail closed against:

```text
T1  exact same PCR identity for H1/H2
T2  all outcomes semantically identical in represented prediction states
T3  confirmation-only structure with no differential represented outcome
T4  missing/unknown discriminating mapping forced into a winner
T5  ATR relation laundering into evidence
T6  causal laundering from correlation/analogy
T7  SUPPORTED/CONTRADICTED output
T8  confidence/probability/trust/weight fields
T9  missing design/expectation provenance refs
T10 self-evidence loop
T11 suppression of inconclusive structure
T12 history mutation/deletion
T13 hidden I/O/retrieval
T14 task/action escalation
T15 identity/relationship/M3 write
T16 graph path/count/centrality authority
```

## 10. Required executable matrix before implementation completion

A later implementation PR must include at least:

```text
HDE-T01 distinct PCR hypothesis identities accepted
HDE-T02 exact same H1/H2 identity rejected
HDE-T03 non-HYPOTHESIS PCR role rejected
HDE-T04 differential known outcome → DISCRIMINATING
HDE-T05 all same-known outcomes → NON_DISCRIMINATING
HDE-T06 UNKNOWN prediction → INCONCLUSIVE_STRUCTURE
HDE-T07 incomplete partition → INCONCLUSIVE_STRUCTURE
HDE-T08 missing design provenance rejected
HDE-T09 missing expectation basis rejected
HDE-T10 duplicate outcome refs rejected
HDE-T11 no confidence/probability field representable
HDE-T12 no SUPPORTED/CONTRADICTED vocabulary in result
HDE-T13 deterministic canonical fingerprint
HDE-T14 no clock/random/network/DB/tool/model imports
HDE-T15 no belief/evidence/identity/action mutation imports
HDE-T16 ATR relations cannot alter classification unless explicitly represented as caller design basis refs only
```

Metamorphic matrix is frozen by the owning Phase 6 readiness document as `HDE-M01…HDE-M10`.

## 11. Explicit non-goals

HDE-v0.1 does not solve:

- semantic paraphrase detection for H1/H2;
- hypothesis generation;
- natural-language reasoning quality;
- exhaustive enumeration of real-world outcomes;
- test cost/safety ranking;
- falsification preference among candidate tests;
- evidence collection or interpretation of an observed result;
- belief revision;
- causal verification;
- confidence calibration;
- inquiry scheduling/autonomy.

Those remain benchmark, caller, existing-owner or future-contract concerns.

## 12. Mandatory authority state

```text
PHASE_6_CANDIDATE = PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR
PHASE_6_IMPLEMENTATION_CONTRACT = HDE-v0.1 · FROZEN_DOCS_TESTS_ONLY
PHASE_6_IMPLEMENTATION = NOT_STARTED
PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED
PHASE_6_RUNTIME = NOT_AUTHORIZED
```

**CONTRACT FREEZE ≠ OWNER GO. CONTRACT FREEZE ≠ SOURCE IMPLEMENTATION. CONTRACT FREEZE ≠ RUNTIME AUTHORITY.**
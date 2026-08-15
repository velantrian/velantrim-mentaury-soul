# 🟢 ATR-v0.1 — Explicit Owner GO

```text
Status:                         OWNER_GO · GRANTED · DOCS_ONLY_AUTHORITY_MILESTONE
Decision date:                  2026-08-15
Baseline main:                  ef72a879fca232c52264482d3a6c289c5127fd86
Owning contract:                ATR-v0.1 · FROZEN_DOCS · UNCHANGED
Candidate:                      PURE_ANCHORED_TYPED_RELATION_RECORD
Owner GO:                       GRANTED
Owner GO scope:                 ATR-v0.1_ONLY
Single-use authorization:       YES
Implementation authorization:   GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_5_IMPLEMENTATION
Phase 5 implementation:         NOT_STARTED
Phase 5 runtime:                NOT_AUTHORIZED
Phase 6 runtime:                NOT_AUTHORIZED
Persistence / graph authority:  NONE
Retrieval / Atlas authority:    NONE
Evidence Gate authority:        UNCHANGED
Belief mutation authority:      NONE
Tools / Action Gate:            NOT_AUTHORIZED
Identity / relationship:        NOT_AUTHORIZED
Direct or indirect M3 write:    FORBIDDEN
Deployment:                     NOT_AUTHORIZED
Autonomous cognition loop:      NOT_AUTHORIZED
Governance mode:                SOLO_MAINTAINER
Independent human review:       NO
```

> **OWNER GO DECISION: GO — `ATR-v0.1_ONLY`.**
>
> The owner instruction dated 2026-08-15 explicitly authorizes bounded
> implementation of the already-frozen `ATR-v0.1` contract if live GitHub still
> shows the contract frozen and no newer authority-changing work exists. Fresh
> preflight confirmed that condition at `main@ef72a879…`. This record therefore
> grants one single-use bounded implementation authorization for that exact
> contract only.

---

## 1. Fresh live preflight basis

Immediately before recording this decision:

```text
main = ef72a879fca232c52264482d3a6c289c5127fd86
main signature = VERIFIED · VALID
main CI = 31869596890 · SUCCESS
open PRs = 0
ruleset = 20594300 · Mentaury main governance · ACTIVE
bypass list = empty
required approvals = 0 · SOLO_MAINTAINER
required check = Python 3.13 · validator · pytest · compileall
strict required-status-check policy = enabled
conversation resolution = required
force-push protection = enabled
deletion protection = enabled
Phase 5 contract = FROZEN_DOCS · ATR-v0.1
Phase 5 candidate = PURE_ANCHORED_TYPED_RELATION_RECORD
Phase 5 implementation = NOT_STARTED
Phase 5 Owner GO = NOT_GRANTED before this decision
Phase 5 runtime = NOT_AUTHORIZED
Phase 6 runtime = NOT_AUTHORIZED
```

Both permitted Mentaury Soul Notion pages were freshly fetched before this
record. They still reflected the verified ATR-v0.1 contract-freeze checkpoint;
no later Phase 5 implementation, Owner GO, contract amendment, or same-scope PR
was present.

---

## 2. Exact authorized contract and implementation surface

Only this frozen contract is authorized:

`docs/research/TYPED_RELATIONS_PURE_RECORD_CONTRACT_V0_1.md`

```text
CONTRACT = ATR-v0.1
CANDIDATE = PURE_ANCHORED_TYPED_RELATION_RECORD
ENDPOINT_BINDING = PCR claim_id + exact PCR input_fingerprint
RELATION_VOCABULARY = CLOSED_V0_1_CORE
RELATION_CONFIDENCE = NOT_IN_V0_1
GRAPH_AUTHORITY = NONE
EVIDENCE_GATE_AUTHORITY = UNCHANGED
```

The next separate bounded implementation may create exactly:

```text
src/mentaury/relations/__init__.py
src/mentaury/relations/contracts.py
src/mentaury/relations/representation.py
```

with the exact frozen public function:

```python
def represent_typed_relation(
    *,
    endpoints: RelationEndpoints,
    semantics: RelationSemantics,
    provenance: RelationProvenance,
    scope: RelationScope,
    budget: RelationRepresentationBudget,
) -> AnchoredTypedRelationRecord:
    ...
```

No service, repository, database, graph engine, discovery layer, worker,
scheduler, retriever, model/LLM client, Evidence Gate wrapper, belief owner,
identity runtime, relationship runtime or action adapter is authorized.

---

## 3. Required implementation properties

The separate implementation PR must preserve the complete frozen contract,
including:

- exact ATR-v0.1 constants and immutable dataclass/enum surface;
- exact PCR-style endpoint anchoring by `claim_id + claim_input_fingerprint`;
- exact self-relations fail closed;
- directed endpoint order remains semantic;
- symmetric endpoints must already be canonically sorted and are never silently reordered;
- exact relation-type/orientation compatibility matrix;
- exact tagged `CLAIM_ANCHOR` vs `CONTEXT_REF` scope semantics;
- exact source-asserted / Mentaury-derived / external-derived / unknown provenance invariants;
- basis anchors remain PCR ClaimAnchor-only and cannot recursively self-support relations;
- all scope and basis tuples remain exact, sorted, unique and budget-bound;
- no confidence/probability/reliability/weight/support/graph-score surface;
- canonical JSON reuse and exact ATR fingerprint domain;
- no relation-type promotion or truth/evidence/belief inference;
- executable `TR-T01…TR-T16`, `TR-M01…TR-M12`, and `TR-P01…TR-P12` coverage;
- exact three-file implementation package and no forbidden owner/runtime imports.

---

## 4. One-time authorization semantics

```text
OWNER_GO_DECISION = GO
PHASE_5_OWNER_GO = GRANTED
OWNER_GO_SCOPE = ATR-v0.1_ONLY
IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_5_IMPLEMENTATION
```

The authorization becomes consumed only by a verified implementation PR whose
exact head matches `ATR-v0.1` and passes exact-head CI, Tier A correctness and
adversarial review, protected merge, and resulting-main CI.

```text
OWNER_GO_GRANTED
≠ IMPLEMENTATION_STARTED
≠ IMPLEMENTATION_COMPLETED
≠ RUNTIME_ACTIVATED
≠ RELATION_VERIFIED
≠ EVIDENCE_GATE_OUTCOME
≠ BELIEF_MUTATION
≠ PHASE_6_RUNTIME_AUTHORITY
```

---

## 5. Explicitly not authorized

```text
PHASE_5_RUNTIME = NOT_AUTHORIZED
PHASE_6_RUNTIME = NOT_AUTHORIZED
INFERENCE_BRIDGE_RUNTIME = NOT_AUTHORIZED
AUTONOMOUS_COGNITION = NOT_AUTHORIZED
AUTONOMOUS_INQUIRY_LOOP = NOT_AUTHORIZED
SCHEDULER = NOT_AUTHORIZED
RELATION_DISCOVERY = NOT_AUTHORIZED
GRAPH_PERSISTENCE = NOT_AUTHORIZED
GRAPH_TRAVERSAL_AUTHORITY = NONE
EVIDENCE_GATE_AUTHORITY = UNCHANGED
BELIEF_MUTATION = NOT_AUTHORIZED
ACTION_GATE = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
```

Phase 6 research/readiness, benchmarks and tests may be prepared only after
Phase 5 is fully merged and resulting-main validation succeeds. That later work
must remain docs/test-level and grants no runtime authority.

---

## 6. Next-step boundary

```text
fresh exact-main compatibility check
→ clean implementation branch
→ exact reserved three-file package
→ executable ATR contract/adversarial/metamorphic/purity tests
→ exact-head CI
→ Tier A correctness + adversarial review
→ guarded protected merge
→ resulting-main CI
→ completion/status + machine-state reconciliation
→ allowed Notion sync
→ Owner GO consumed
→ only then Phase 6 docs/test benchmark preparation
→ STOP before any Phase 6 runtime implementation
```

If `ATR-v0.1`, canonical JSON profile, PCR identity semantics, ruleset, CI,
open same-scope PR state or writer state changes before implementation begins:
`STOP_AND_RECONCILE`.

# 🟢 Provenance + Claim Representation — Explicit Owner GO

```text
Status:                         OWNER_GO · GRANTED · DOCS_ONLY_AUTHORITY_MILESTONE
Decision date:                  2026-08-12
Baseline main:                  f9a5feef74233f44c5bdd39f7dd264db7f27443f
Owning contract:                PCR-v0.1 · FROZEN_DOCS · UNCHANGED
Candidate:                      PURE_PROVENANCE_CLAIM_RECORD
Owner GO:                       GRANTED
Owner GO scope:                 PCR-v0.1_ONLY
Single-use authorization:       YES
Implementation authorization:   GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_3_IMPLEMENTATION
Phase 3 implementation:         NOT_STARTED
Phase 3 runtime:                NOT_AUTHORIZED
Phase 4:                        NOT_AUTHORIZED
Source admission authority:     NONE
Evidence Gate authority:        UNCHANGED
Belief promotion/revision:      NOT_AUTHORIZED
Retrieval / Atlas:              NOT_AUTHORIZED
Tools / Action Gate:            NOT_AUTHORIZED
Identity / relationship:        NOT_AUTHORIZED
Direct or indirect M3 write:    FORBIDDEN
Persistence:                    NOT_AUTHORIZED
Deployment:                     NOT_AUTHORIZED
Governance mode:                SOLO_MAINTAINER
Independent human review:       NO
```

> **OWNER GO DECISION: GO — `PCR-v0.1_ONLY`.**
>
> The owner instruction `Делай` in the active project conversation was given
> after PR #99 had frozen and merged the exact `PCR-v0.1` contract and after the
> assistant explicitly stated that the next required step was a separate Owner GO
> for `PCR-v0.1_ONLY`. This record therefore grants one single-use bounded
> implementation authorization for that exact contract only.

---

## 1. Fresh live preflight basis

Immediately before recording this decision:

```text
main = f9a5feef74233f44c5bdd39f7dd264db7f27443f
open PRs = 0
ruleset = 20594300 · Mentaury main governance · ACTIVE
bypass list = empty
required approvals = 0 · SOLO_MAINTAINER
required check = Python 3.13 · validator · pytest · compileall
conversation resolution = required
force-push protection = enabled
deletion protection = enabled
Phase 3 contract PR #99 = MERGED
Phase 3 contract = FROZEN_DOCS · PCR-v0.1
Phase 3 implementation = NOT_STARTED
Phase 3 runtime = NOT_AUTHORIZED
Phase 4 = NOT_STARTED · OWNER_GO_NOT_GRANTED
```

Both permitted Notion pages were freshly fetched and matched the PR #99 freeze
checkpoint before this decision was recorded. No open same-scope PR existed.

---

## 2. Exact authorized contract and implementation surface

Only this frozen contract is authorized:

`docs/research/PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md`

```text
CONTRACT = PCR-v0.1
CANDIDATE = PURE_PROVENANCE_CLAIM_RECORD
SOURCE_SCOPE = CALLER_SUPPLIED_REFERENCES_ONLY
ClaimClass ≠ ClaimType ≠ EpistemicRole
```

The next separate bounded implementation may create exactly:

```text
src/mentaury/claims/__init__.py
src/mentaury/claims/contracts.py
src/mentaury/claims/representation.py
```

with the exact frozen public function:

```python
def represent_provenance_claim(
    *,
    source: ProvenanceSource,
    claim: ClaimRepresentation,
    scope: ClaimScope,
    budget: RepresentationBudget,
) -> ProvenanceClaimRecord:
    ...
```

No service, repository, store, worker, scheduler, retriever, Atlas handle,
model/LLM client, graph, promoter, revision engine, identity runtime or action
adapter is authorized.

---

## 3. Required implementation properties

The separate implementation PR must preserve the complete frozen contract,
including:

- exact reuse of `ClaimClass`, `ProvenanceState`, `Sensitivity`, `SourceClass`,
  `SourceOrigin`, `SubjectRelation` and `ClaimType` class identities;
- exactly one new representation-only enum `EpistemicRole`;
- immutable `ProvenanceSource`, `ClaimRepresentation`, `ClaimScope`,
  `RepresentationBudget`, and `ProvenanceClaimRecord` contracts;
- exact tuple/string/enum/bool/int admission rules and hard caps;
- no silent tuple sorting, repair, coercion, truncation or summarization;
- `INFERENCE` requires caller-supplied non-empty `basis_refs`;
- duplicate references fail closed;
- canonical JSON reuse and exact `PCR-v0.1` fingerprint domain;
- `evidence_refs` remain references only and cannot manufacture support;
- no source admission, Evidence Gate invocation, belief promotion/revision,
  retrieval, persistence, NPG call, runtime wiring, action, identity or M3 path;
- executable `PCR-T01…PCR-T12`, `PCR-M01…PCR-M10`, and `PCR-P01…PCR-P08`
  coverage.

---

## 4. One-time authorization semantics

```text
OWNER_GO_DECISION = GO
PHASE_3_OWNER_GO = GRANTED
OWNER_GO_SCOPE = PCR-v0.1_ONLY
IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_3_IMPLEMENTATION
```

The authorization becomes consumed only by a verified implementation PR whose
exact head matches `PCR-v0.1` and passes exact-head CI, Tier A correctness and
adversarial review, protected merge and resulting-main CI.

```text
OWNER_GO_GRANTED
≠ IMPLEMENTATION_STARTED
≠ IMPLEMENTATION_COMPLETED
≠ RUNTIME_ACTIVATED
≠ EVIDENCE_SUPPORT
≠ BELIEF_PROMOTION
≠ PHASE_4_AUTHORITY
```

---

## 5. Explicitly not authorized

```text
PHASE_3_RUNTIME = NOT_AUTHORIZED
PHASE_4 = NOT_AUTHORIZED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
ACTION_GATE = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
ATLAS_ACCESS = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
CHARACTER_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
PERSISTENCE = NOT_AUTHORIZED
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
AUTONOMOUS_BACKGROUND_LOOP = NOT_AUTHORIZED
```

---

## 6. Next-step boundary

```text
fresh exact-main compatibility check
→ clean implementation branch
→ exact reserved three-file package
→ executable PCR contract/adversarial/metamorphic/purity tests
→ exact-head CI
→ Tier A correctness + adversarial review
→ guarded protected merge
→ resulting-main CI
→ completion/status reconciliation
→ allowed Notion sync
→ Owner GO consumed
→ STOP
```

If `PCR-v0.1`, reused enum identities, canonical JSON profile, ruleset, CI or
writer state changes before implementation begins: `STOP_AND_RECONCILE`.

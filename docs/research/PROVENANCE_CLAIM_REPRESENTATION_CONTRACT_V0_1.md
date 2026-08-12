# 🧬 Pure Provenance + Claim Representation — Frozen Contract v0.1

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Contract version:                    PCR-v0.1
Date:                                2026-08-12
Phase:                               3 · PROVENANCE + CLAIM REPRESENTATION
Review tier:                         TIER_A
Owning readiness:                    PROVENANCE_CLAIM_REPRESENTATION_READINESS.md
Owning candidate selection:          PROVENANCE_CLAIM_REPRESENTATION_CANDIDATE_SELECTION.md
Candidate:                           PURE_PROVENANCE_CLAIM_RECORD
Implementation:                      NOT_STARTED
Owner GO:                            NOT_GRANTED
Implementation authorization:        NONE
Runtime activation:                  NOT_AUTHORIZED
Source admission authority:          NONE
Evidence Gate authority:             UNCHANGED
Belief promotion/revision authority: NONE
Retrieval / Atlas authority:         NONE
Identity / relationship authority:   NONE
Direct or indirect M3 write:         FORBIDDEN
Persistence authority:               NONE
Network/filesystem/database I/O:     NONE
Tool / Action Gate authority:        NONE
Deployment authority:                NONE
```

> **CONTRACT FROZEN ≠ OWNER GO.**
>
> This document freezes one pure representation primitive only. It does not
> authorize code, source admission, evidence assessment, belief promotion,
> persistence, retrieval, runtime composition, tools/actions, identity,
> relationship, M3 mutation or deployment.

---

## 1. 🎯 Bounded purpose

A future implementation answers exactly one structural question:

> Can these exact caller-supplied provenance, attribution, claim-axis and scope
> values be represented as one deterministic immutable ProvenanceClaimRecord?

The primitive does not decide whether the source is admitted, whether the claim
is true, whether evidence supports it, whether it should become a belief, or
whether Mentaury may act on it.

Strongest successful outcome:

```text
VALID IMMUTABLE REPRESENTATION
```

Semantic ceiling:

```text
VALID REPRESENTATION
≠ source admission
≠ evidence qualification
≠ EvidenceGateOutcome.SUPPORTED
≠ EvidenceGateOutcome.CONTRADICTED
≠ factual truth proof
≠ belief promotion or revision
≠ Mentaury autobiography
≠ identity / relationship / consent authority
≠ capability / Action Gate PASS
≠ retrieval / Atlas permission
≠ tool / execution permission
≠ M3 nomination or write
≠ deployment permission
```

---

## 2. 🔒 Frozen constants and hard caps

```text
PROVENANCE_CLAIM_CONTRACT_VERSION = "PCR-v0.1"
CANONICAL_PROFILE                 = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN          = "MENTAURY_PROVENANCE_CLAIM_INPUT_V1"
SOURCE_SCOPE                      = "CALLER_SUPPLIED_REFERENCES_ONLY"

HARD_MAX_STRING_BYTES             = 4096
HARD_MAX_TUPLE_ITEMS              = 512
HARD_MAX_CANONICAL_INPUT_BYTES    = 262144
```

Canonicalization must reuse
`mentaury.contracts.canonical_json.canonical_json_bytes` and verify live
`PROFILE_NAME == "MENTAURY_CANONICAL_JSON_V1"` before returning a record.

The caller cannot override contract version, canonical profile, fingerprint
domain, source-scope label or hard caps and cannot provide the final fingerprint.

---

## 3. 📦 Reserved package and exact public API

If and only if a later separate Owner GO authorizes implementation, the exact
bounded package is:

```text
src/mentaury/claims/__init__.py
src/mentaury/claims/contracts.py
src/mentaury/claims/representation.py
```

Exact public function:

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
adapter belongs to PCR-v0.1.

Forbidden public inputs include:

```text
raw source text
source admission result
EvidenceGateOutcome / EvidenceGateReceipt
BeliefStatus / promotion decision
prior ProvenanceClaimRecord as authority
caller-supplied fingerprint
confidence / probability / reliability score
clock / environment / callback
retriever / Atlas / graph / database / filesystem
model / LLM client
tool / Action Gate handle
identity / relationship registry
```

---

## 4. 🧬 Reused vocabulary — exact class identity

PCR-v0.1 does not create second owners for concepts that already exist.

A later implementation must import and reuse exact class identities:

```python
from mentaury.non_projection import (
    ClaimClass,
    ProvenanceState,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SubjectRelation,
)
from mentaury.epistemic_types import ClaimType
```

These axes remain distinct:

```text
ClaimClass
≠ ClaimType
≠ EpistemicRole
≠ EvidenceGateOutcome
≠ BeliefStatus
```

No implicit conversion table between ClaimClass and ClaimType is authorized.

---

## 5. 🧠 New representation-only epistemic role

PCR-v0.1 owns exactly one new enum:

```text
EpistemicRole:
OBSERVATION
TESTIMONY
EVIDENCE_CANDIDATE
HYPOTHESIS
INFERENCE
INTERPRETATION
METAPHORICAL_EXPRESSION
UNKNOWN
```

Meaning:

```text
OBSERVATION          = represented as an observation claim; not automatically verified
TESTIMONY            = represented as testimony; not automatically factual truth
EVIDENCE_CANDIDATE   = candidate evidence relation; not Evidence Gate qualification
HYPOTHESIS           = testable candidate proposition; not belief promotion
INFERENCE            = derived proposition; basis refs required by caller
INTERPRETATION       = meaning assigned to source material; not direct testimony
METAPHORICAL_EXPRESSION = non-literal expression; cannot be silently factualized
UNKNOWN              = role not established; uncertainty preserved
```

---

## 6. 📦 Exact immutable contracts

All values below are `@dataclass(frozen=True, slots=True)` and expose deterministic
`to_value()` projections using canonical JSON scalar/list/object values only.
Extension dictionaries are forbidden.

```python
@dataclass(frozen=True, slots=True)
class ProvenanceSource:
    source_ref: str
    source_actor_ref: str | None
    source_class: SourceClass
    source_origin: SourceOrigin
    provenance_state: ProvenanceState
    publication_or_capture_context_ref: str | None
    sensitivity: Sensitivity
    usage_boundary_ref: str
    material_gaps: tuple[str, ...]
    derivation_refs: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ClaimRepresentation:
    claim_id: str
    statement_ref: str
    claim_class: ClaimClass
    claim_type: ClaimType
    epistemic_role: EpistemicRole
    directly_stated: bool
    speaker_ref: str
    subject_ref: str
    subject_relation: SubjectRelation
    basis_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ClaimScope:
    applies_to: tuple[str, ...]
    may_support: tuple[str, ...]
    does_not_establish: tuple[str, ...]
    unknowns: tuple[str, ...]
    transfer_limits: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class RepresentationBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_canonical_input_bytes: int

@dataclass(frozen=True, slots=True)
class ProvenanceClaimRecord:
    contract_version: str
    source: ProvenanceSource
    claim: ClaimRepresentation
    scope: ClaimScope
    input_fingerprint: str
```

---

## 7. 🔐 Field semantics and anti-laundering rules

### 7.1 `provenance_state`

`VERIFIED` means only that the caller-supplied provenance assertion has passed
the authority process that supplied this input. PCR-v0.1 does not independently
verify the source.

```text
ProvenanceState.VERIFIED
≠ source admitted
≠ claim true
≠ evidence reliable
```

### 7.2 `directly_stated`

```text
directly_stated = True
→ caller asserts the represented statement is directly present in the source

directly_stated = False
→ statement is derived / summarized / interpreted / inferred
```

PCR-v0.1 does not inspect raw source text to prove this assertion.

### 7.3 `basis_refs`

`basis_refs` identify caller-supplied inputs used to derive or frame the claim.
They create no support status.

For `EpistemicRole.INFERENCE`, an empty `basis_refs` tuple is malformed and must
fail closed. For other roles, emptiness is permitted.

### 7.4 `evidence_refs`

`evidence_refs` are references only.

```text
1 evidence_ref
100 evidence_refs
1000 repeated citations
≠ EvidenceGateOutcome.SUPPORTED
```

Duplicate references are rejected before canonicalization.

### 7.5 `ClaimScope`

Scope is representational metadata only. `may_support` means a later evaluator
may inspect the claim for that purpose; it is not a support decision.

`does_not_establish` and `transfer_limits` must never be discarded by a later
projection into NPG or Evidence Gate inputs.

---

## 8. 📏 Admission and canonicalization rules

For every tuple field:

- exact tuple required;
- every element exact non-empty `str`;
- canonical tuple order is lexical ascending;
- duplicates forbidden;
- caller must provide already sorted unique tuples; the implementation does not
  silently reorder malformed input.

For every enum field:

- exact enum instance required;
- raw strings are not coerced.

For boolean fields:

- exact `bool` required.

For strings:

- exact `str` required;
- non-empty unless field is explicitly optional;
- no surrounding whitespace;
- UTF-8 byte length constrained by local budget and hard cap.

For local budget values:

- exact positive `int` required;
- booleans rejected as integers;
- local limit must be <= corresponding hard cap.

Valid input inside hard caps but exceeding the caller local budget raises
`ProvenanceClaimBudgetExceeded`; malformed/hard-cap input raises
`ProvenanceClaimContractError`.

No truncation, summarization, sampling, dropping or implicit repair is allowed.

---

## 9. 🧾 Deterministic fingerprint

The implementation computes the fingerprint itself:

```text
sha256(
  b"MENTAURY_PROVENANCE_CLAIM_INPUT_V1\x00"
  + canonical_json_bytes({
      "contract_version": "PCR-v0.1",
      "source": source.to_value(),
      "claim": claim.to_value(),
      "scope": scope.to_value(),
      "budget": budget.to_value(),
    })
).hexdigest()
```

Fingerprint properties:

```text
fingerprint
= exact-input identity evidence
≠ truth evidence
≠ evidence support
≠ source admission
≠ freshness token
≠ reusable authority
```

---

## 10. 🪞 NPG compatibility projection boundary

PCR-v0.1 does not replace `AIE-v0.1`.

A later separate composition milestone may define an explicit mapping from a
`ProvenanceClaimRecord` into caller-supplied AIE fields, but PCR-v0.1 itself:

```text
MUST NOT call NPG
MUST NOT construct ProjectionIntent
MUST NOT synthesize reviewer provenance
MUST NOT infer SubjectRelation
MUST NOT turn VALID REPRESENTATION into PASS_ATTRIBUTED
```

Any future mapping must preserve:

- source class/origin/provenance state;
- speaker/subject attribution;
- ClaimClass;
- direct/derived distinction;
- scope exclusions and transfer limits.

---

## 11. 🧪 Frozen adversarial requirements

A later implementation PR must make each family executable.

```text
PCR-T01 creator testimony → Mentaury autobiography laundering is impossible
PCR-T02 ClaimClass cannot implicitly coerce ClaimType
PCR-T03 ClaimType cannot implicitly coerce ClaimClass
PCR-T04 observation/evidence/hypothesis/inference roles remain distinct
PCR-T05 derived interpretation cannot be represented as direct source statement by implicit repair
PCR-T06 UNKNOWN/PARTIAL provenance cannot be silently upgraded to VERIFIED
PCR-T07 evidence_refs cannot manufacture Evidence Gate support
PCR-T08 source admission status cannot enter the public contract
PCR-T09 supported/contradicted/truth/confidence fields cannot enter the public contract
PCR-T10 analogy/correlation/inference cannot silently become causal classification
PCR-T11 numeric confidence/reliability pseudo-precision is absent from the public contract
PCR-T12 valid record grants no retrieval/action/identity/relationship/M3/deployment authority
```

---

## 12. 🔁 Frozen metamorphic requirements

```text
PCR-M01 source_ref change → fingerprint changes
PCR-M02 statement_ref change → fingerprint changes
PCR-M03 ClaimClass change → fingerprint changes; ClaimType unchanged
PCR-M04 ClaimType change → fingerprint changes; ClaimClass unchanged
PCR-M05 EpistemicRole change → fingerprint changes
PCR-M06 directly_stated change → fingerprint changes
PCR-M07 speaker/subject/SubjectRelation change → fingerprint changes
PCR-M08 scope or transfer-limit change → fingerprint changes
PCR-M09 evidence/basis ref count/order cannot create semantic support status
PCR-M10 duplicate/unsorted tuple input → fail closed, never normalized silently
```

---

## 13. 🧼 Purity requirements

```text
PCR-P01 no network
PCR-P02 no filesystem
PCR-P03 no database / persistence
PCR-P04 no environment / ambient clock
PCR-P05 no model / LLM / retriever / Atlas / graph
PCR-P06 no tool / Action Gate / capability invocation
PCR-P07 no belief mutation / Evidence Gate invocation / M2-M3 write
PCR-P08 deterministic output for exact typed input
```

---

## 14. ⛔ Mandatory stop boundary

Current Phase 3 state after this contract freeze is:

```text
PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_READINESS = READY
PHASE_3_CANDIDATE_SELECTION = SELECTED
PHASE_3_CANDIDATE = PURE_PROVENANCE_CLAIM_RECORD
PHASE_3_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
PHASE_3_CONTRACT_VERSION = PCR-v0.1
PHASE_3_IMPLEMENTATION = NOT_STARTED
PHASE_3_OWNER_GO = NOT_GRANTED
PHASE_3_RUNTIME = NOT_AUTHORIZED
```

A later implementation requires a **new explicit Owner GO after this exact
frozen contract is reviewed and merged**. Previous NPG or NPG-COMP Owner GO
receipts are consumed and cannot authorize PCR-v0.1.

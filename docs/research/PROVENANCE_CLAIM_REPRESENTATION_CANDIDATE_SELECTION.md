# 🧭 Phase 3 — Provenance + Claim Representation Candidate Selection

```text
Status:                         CANDIDATE_SELECTED · DOCS_ONLY
Date:                           2026-08-12
Phase:                          3 · PROVENANCE + CLAIM REPRESENTATION
Owning readiness:               PROVENANCE_CLAIM_REPRESENTATION_READINESS.md
Selected candidate:             PURE_PROVENANCE_CLAIM_RECORD
Implementation:                 NOT_STARTED
Owner GO:                       NOT_GRANTED
Runtime authority:              NONE
Persistence authority:          NONE
Evidence Gate authority:        UNCHANGED
Direct or indirect M3 write:    FORBIDDEN
```

> **CANDIDATE SELECTED ≠ IMPLEMENTATION AUTHORIZED.**

---

## 1. 🎯 Selection criterion

The Phase 3 candidate must add the smallest deterministic representation that:

- preserves provenance;
- keeps source, claim and epistemic role distinct;
- reuses rather than duplicates current ClaimClass / ClaimType semantics;
- binds attribution, basis references and scope;
- can be projected into later gate-specific inputs;
- creates no truth, admission, promotion, identity or action authority.

---

## 2. Alternatives considered

### A. Reuse `AIE-v0.1` as the universal knowledge record — REJECT

Why rejected:

- AIE is intentionally an NPG evaluation envelope;
- it contains projection intent and NPG-specific authority exclusions;
- making it the universal record would let one gate-specific schema become the
  owner of general knowledge representation;
- it would make later knowledge phases depend on NPG concepts even when no
  projection check is being performed.

### B. Extend `EvidenceRecord` — REJECT

Why rejected:

- EvidenceRecord is Evidence Gate input, not a general claim object;
- it carries evidence-side and assessed quality fields;
- a claim can exist before it qualifies as evidence;
- provenance/claim representation must not imply Evidence Gate admission.

### C. Extend P0-014 belief records — REJECT

Why rejected:

- belief lifecycle owns M2 belief state and revision semantics;
- Phase 3 precedes Phase 4 promotion/revision;
- making every represented claim a belief would collapse `claim ≠ belief` and
  prematurely grant lifecycle semantics.

### D. `PURE_PROVENANCE_CLAIM_RECORD` — SELECTED

The selected primitive is a pure immutable caller-supplied representation with
one deterministic fingerprint and no decision vocabulary.

```text
caller-supplied provenance
+ caller-supplied claim axes
+ attribution
+ basis refs
+ explicit scope
        ↓
pure validation / canonicalization
        ↓
immutable ProvenanceClaimRecord
```

---

## 3. Selected semantic axes

The record keeps three separate axes:

```text
ClaimClass
→ discourse / testimony class

ClaimType
→ epistemic scope used by Evidence Gate-compatible reasoning

EpistemicRole
→ OBSERVATION / TESTIMONY / EVIDENCE_ASSERTION /
  HYPOTHESIS / INFERENCE / INTERPRETATION /
  METAPHORICAL_EXPRESSION / UNKNOWN
```

No axis is derived from another.

---

## 4. Selected package boundary

If and only if a later separate Owner GO is granted, the reserved bounded package
is:

```text
src/mentaury/claims/__init__.py
src/mentaury/claims/contracts.py
src/mentaury/claims/representation.py
```

The package must not include:

```text
retriever.py
atlas.py
store.py
repository.py
service.py
worker.py
scheduler.py
promoter.py
revision.py
relation_graph.py
identity.py
action.py
tools.py
```

---

## 5. Authority ceiling

The strongest successful result is simply a valid immutable record.

```text
VALID REPRESENTATION
≠ admitted source
≠ evidence qualification
≠ supported claim
≠ truth
≠ belief promotion
≠ identity trait
≠ relationship fact
≠ capability
≠ retrieval permission
≠ action permission
≠ M3 write
≠ deployment authority
```

---

## 6. Selection decision

```text
PHASE_3_CANDIDATE_SELECTION = SELECTED
PHASE_3_CANDIDATE = PURE_PROVENANCE_CLAIM_RECORD
NEXT_DOCS_STEP = FREEZE_PCR_V0_1_IMPLEMENTATION_CONTRACT
OWNER_GO = NOT_GRANTED
IMPLEMENTATION = NOT_STARTED
```

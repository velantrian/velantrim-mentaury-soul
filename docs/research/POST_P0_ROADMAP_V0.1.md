# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      0.5
Updated:                      2026-08-09
Current review mode:          SOLO_MAINTAINER · TIER_A
P1-001 implementation:        IMPLEMENTED_BOUNDED
P1-001 validation:            EXACT_HEAD_AND_MAIN_CI_PASS
P1-002 contract:              FROZEN_DOCS
P1-002 implementation:        NOT AUTHORIZED
Next runtime milestone:       P1-002 · CONTRACT ONLY · NOT AUTHORIZED
Runtime deployment authority: NONE
Truth authority:              NONE
Capability grant authority:   NONE
Canon modification authority: NONE
Direct or indirect M3 write:  FORBIDDEN
Domain runtime:               NOT AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

```text
FROZEN_DOCS ≠ implementation authorization
ALLOW_REFERENCE ≠ retrieval permission
privacy classification ≠ privacy mutation
P1-002 selection ≠ later privacy runtime authority
Solo review ≠ independent certification
```

The filename retains `V0.1` for stable historical links. Document metadata is
the current version authority.

---

## 1. ✅ Completed P1-001 sequence

```text
P0-001…P0-015 implemented
→ P1-001 contract frozen by PR #58
→ bounded owner GO merged through PR #62
→ pure resolver implemented through PR #63
→ exact-head Tier A review passed
→ resulting main CI passed
→ P1-001 IMPLEMENTED_BOUNDED
```

P1-001 remains limited to pure capability classification. It does not authorize
registry persistence, Action Gate, tool execution, identity mutation, M3 writes
or deployment.

---

## 2. 🧊 Selected P1-002 contract

```text
Milestone: P1-002 Privacy Reconciliation Classifier
Contract:  docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md
State:     FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED
Owner GO:  NOT RECORDED
```

### Demonstrated gap

P0-010 removes one detached payload from the active SQLite event store while
preserving immutable event provenance and redaction evidence. It does not prove
that stale copies are reconciled across:

```text
backups
forks
indexes
embeddings
graph edges
caches
derived summaries
```

### Minimal bounded slice

A future implementation may classify one caller-supplied material/copy/intent
triple into exactly one of:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

The classifier must be pure, deterministic, strict and fail closed. It may not
perform the required remediation.

### Frozen scenario boundary

The contract freezes `PRIV-SC-001…PRIV-SC-015`, including:

- deleted material surviving in backup;
- third-party testimony without permission;
- withdrawn purpose surviving in fork;
- redacted material leaking through a derived summary;
- stale policy revisions;
- wrong cross-record linkage;
- unknown fields and budget exhaustion;
- allowed-reference and metamorphic invariance cases.

---

## 3. 🔐 P1-002 non-goals

```text
privacy registry persistence
backup/fork inventory scanning
content inspection
content deletion or P0 redaction execution
quarantine execution
index/embedding/graph/cache/summary rebuilding
retrieval execution
network, filesystem or database access
ambient clock or environment authority
relationship reconciliation
belief or identity mutation
M3 nomination or write
Capability Lease validation
Action Gate
Tool Receipt or tool execution
backend selection
production deployment
```

P1-002 must not call P1-001 internally and must not convert a Capability Lease
`ALLOW` into privacy permission.

---

## 4. ⛔ P1-002 authorization gate

```text
P1_002_CONTRACT_FROZEN_DOCS
P1_002_IMPLEMENTATION_NOT_AUTHORIZED
```

Implementation requires:

```text
explicit new owner GO
→ dedicated authorization receipt
→ clean Tier A implementation branch and PR
→ exact-head validator, freshness, pytest and compileall
→ distinct correctness pass
→ distinct adversarial pass
→ resolved conversations
→ unchanged reviewed head merge
→ green resulting main CI
→ status and Notion synchronization
```

The P1-001 Owner GO is consumed and cannot be reused.

---

## 5. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| Contract selected and merged | `FROZEN_DOCS` |
| Bounded Owner GO merged | `AUTHORIZED_BOUNDED` |
| Code PR merged + main CI | `IMPLEMENTED_BOUNDED` |
| Deletion/quarantine/rebuild/retrieval proposal | requires a separate later authorization cycle |

GitHub `main` and `docs/CURRENT_STATUS.md` remain authoritative. Notion is a
derived navigation/status surface synchronized only after verified evidence.

---

## 6. 🔬 Research promotion

The [Research Index](RESEARCH_INDEX.md) preserves hypotheses and candidates.
P1-002 was selected because it addresses a documented blocker while remaining
strictly below relationship, identity, Action Gate and tool-execution runtime.

Issue #39 governs only the future transition to genuine independent review. Its
current absence is not a solo-mode blocker.

---

## 7. 🏁 Formula

```text
P0 complete
→ P1-001 implemented bounded
→ privacy reconciliation gap identified
→ P1-002 contract frozen
→ STOP until a new bounded Owner GO
```

### Related

- [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`../P0_010_ATOMIC_SAME_STREAM_REDACTION.md`](../P0_010_ATOMIC_SAME_STREAM_REDACTION.md)
- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)

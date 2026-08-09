# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      0.6
Updated:                      2026-08-09
Current review mode:          SOLO_MAINTAINER · TIER_A
P1-001 implementation:        IMPLEMENTED_BOUNDED
P1-001 validation:            EXACT_HEAD_AND_MAIN_CI_PASS
P1-002 contract:              FROZEN_DOCS
P1-002 implementation:        AUTHORIZED_BOUNDED · NOT_STARTED
Next runtime milestone:       P1-002 PURE CLASSIFIER ONLY
Runtime deployment authority: NONE
Mutation authority:           NONE
Retrieval authority:          NONE
Direct or indirect M3 write:  FORBIDDEN
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

```text
AUTHORIZED_BOUNDED ≠ implemented
ALLOW_REFERENCE ≠ retrieval permission
privacy classification ≠ privacy mutation
P1-002 authorization ≠ later privacy runtime authority
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

```text
Reviewed head:   e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:   31323051934 · success · 387 passed
Merge:           f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:   31323138053 · success
```

P1-001 owning receipt: [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md).

No registry service, Action Gate, P1-002 remediation execution or tool runtime
is authorized by P1-001 completion.

---

## 2. 🧊 P1-002 contract freeze

```text
Milestone: P1-002 Privacy Reconciliation Classifier
Contract:  docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md
Contract PR: #65
Reviewed head: 85bf0070e2f15b5ca752b82325337d6ef0190396
Exact-head CI: 31331396018 · success · 401 passed
Merge: 1dc7bcf97986f455f48beb121c2048dfc34bd11c
Post-merge CI: 31331506606 · success
```

The contract addresses stale privacy copies in backups, forks, indexes,
embeddings, graph edges, caches and derived summaries through pure fail-closed
classification only.

---

## 3. 🔐 Bounded P1-002 authorization

Authorization receipt:

- [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)

Exact authorized implementation paths:

```text
src/mentaury/privacy/__init__.py
src/mentaury/privacy/reconciliation/__init__.py
src/mentaury/privacy/reconciliation/contracts.py
src/mentaury/privacy/reconciliation/classifier.py
tests/test_privacy_reconciliation_classifier.py
```

Authorized output space:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

The implementation must be pure, deterministic, strict and fail closed. It may
only classify caller-supplied material/copy/intent/budget values and may not
perform remediation or retrieval.

---

## 4. 🚫 P1-002 non-goals

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
event append or replay integration
relationship, belief or identity mutation
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

## 5. 🧪 Implementation gate

```text
P1_002_OWNER_GO_AUTHORIZED_BOUNDED
P1_002_IMPLEMENTATION_NOT_STARTED
```

The implementation PR requires:

```text
exact authorized files only
→ all PRIV-SC-001…PRIV-SC-015 scenarios
→ strict admission and budget tests
→ exact first-match precedence
→ fresh-process no-I/O/no-clock test
→ exact-head validator/freshness/pytest/compileall
→ distinct correctness pass
→ distinct adversarial pass
→ resolved conversations
→ unchanged reviewed-head merge
→ green resulting main CI
```

The Owner GO is consumed only by this exact pure classifier slice.

---

## 6. 🔄 Status rules

| Event | Status result |
|---|---|
| Contract selected and merged | `FROZEN_DOCS` |
| Bounded Owner GO merged | `AUTHORIZED_BOUNDED` |
| Code PR merged + main CI | `IMPLEMENTED_BOUNDED` |
| Deletion/quarantine/rebuild/retrieval proposal | separate future authorization required |

GitHub `main` and `docs/CURRENT_STATUS.md` remain authoritative. Notion is a
derived navigation/status surface synchronized only after verified evidence.

---

## 7. 🏁 Formula

```text
P0 complete
→ P1-001 implemented bounded
→ P1-002 contract frozen
→ bounded P1-002 Owner GO
→ pure classifier implementation PR
→ STOP before any remediation runtime
```

### Related

- [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [`../P0_010_ATOMIC_SAME_STREAM_REDACTION.md`](../P0_010_ATOMIC_SAME_STREAM_REDACTION.md)
- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)

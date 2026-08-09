# 🔐 P1-002 Privacy Reconciliation Classifier — Implementation Authorization

```text
Status:                       OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED
Authorization date:           2026-08-09
Milestone:                    P1-002 Privacy Reconciliation Classifier
Contract authority:           docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md
Status authority:             docs/CURRENT_STATUS.md
Governance:                   SOLO_MAINTAINER · TIER_A
Independent human assurance:  NOT CLAIMED
Runtime deployment:           NOT AUTHORIZED
Mutation authority:           NONE
Retrieval authority:          NONE
Next runtime milestone:       NOT AUTHORIZED
```

## 1. 🎯 Authorization source

The repository owner instructed the agent to continue the remaining work after
P1-002 contract freeze and green post-merge `main` CI.

This receipt records a new bounded Owner GO. It does not reuse the consumed
P1-001 authorization.

```text
owner instruction
→ frozen P1-002 contract in PR #65
→ green resulting main CI 31331506606
→ bounded authorization checkpoint
→ separate implementation PR required
```

---

## 2. ✅ Exact authorized source and test scope

Only these paths are authorized for the implementation PR:

```text
src/mentaury/privacy/__init__.py
src/mentaury/privacy/reconciliation/__init__.py
src/mentaury/privacy/reconciliation/contracts.py
src/mentaury/privacy/reconciliation/classifier.py
tests/test_privacy_reconciliation_classifier.py
```

Minimal governance/test alignment may additionally touch:

```text
CODEOWNERS
docs/GOVERNANCE.md
tests/test_governance_risk_tiers.py
tests/test_p1_002_contract_docs.py
```

No other runtime path is authorized by this receipt.

---

## 3. 🧱 Authorized behavior

The implementation may expose exactly one pure operation:

```text
classify_privacy_reconciliation(
    material,
    copy,
    intent,
    budget,
) -> PrivacyReconciliationResult
```

It may implement only:

- immutable typed contracts from the frozen document;
- strict exact-field mapping admission;
- canonical collection admission and budget checks;
- cross-record linkage checks;
- deterministic first-match precedence;
- surface-specific classification;
- the exact four decisions;
- the exact frozen reason vocabulary;
- tests for `PRIV-SC-001…PRIV-SC-015` and required adversarial/metamorphic properties.

The result is classification data only.

---

## 4. 🚫 Preserved prohibitions

The authorization does not permit:

```text
privacy registry persistence
backup/fork inventory scanning
content inspection
content deletion
P0 redaction execution
quarantine execution
index/embedding/graph/cache/summary rebuilding
retrieval execution
network access
filesystem or database access
ambient clock or environment authority
event append
replay/projection integration
belief mutation
relationship mutation
identity continuity runtime
direct or indirect M3 write
Capability Lease validation or internal P1-001 calls
Action Gate
Tool Receipt runtime
tool execution
backend selection or migration
production deployment
```

`ALLOW_REFERENCE` must not contain reusable permission material and must not be
treated as retrieval authorization.

---

## 5. 🧪 Required implementation evidence

The implementation PR must prove:

```text
all PRIV-SC-001…PRIV-SC-015 scenarios
exact first-match precedence
typed/mapping equivalence
strict unknown-field and wrong-type rejection
sorted unique immutable collection admission
bool-as-int rejection
max_serialized_bytes canonical input budget
max_purposes collection budget
max_branches collection budget
future policy revision rejection
unrelated-purpose metamorphic invariance
minimal two-field result
fresh-process no-I/O/no-clock import
no imports from storage/replay/beliefs/evidence/capability/identity runtime
```

A green test suite before the final reviewed head is not merge evidence.

---

## 6. 🔍 Review and merge gate

Before merge:

```text
clean implementation PR
+ exact authorized paths only
+ exact-head validator/freshness/pytest/compileall
+ correctness pass
+ adversarial pass
+ all conversations resolved
+ unchanged reviewed head
+ explicit maintainer decision
```

After merge:

```text
green resulting main CI
→ separate completion/status reconciliation PR
→ Notion synchronization from verified evidence only
```

---

## 7. ⛔ Authorization stop

```text
P1_002_OWNER_GO_AUTHORIZED_BOUNDED
P1_002_IMPLEMENTATION_NOT_STARTED
P1_002_MUTATION_AUTHORITY_NONE
P1_002_RETRIEVAL_AUTHORITY_NONE
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
```

This authorization is consumed only by the exact bounded implementation above.
It does not roll forward to deletion, remediation execution, relationship or
identity runtime, Action Gate, tools or deployment.

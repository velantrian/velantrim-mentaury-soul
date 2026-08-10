# 🔐 P1-002 Privacy Reconciliation Classifier — Frozen Contract

```text
Status:                       FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED
Version:                      0.1
Date:                         2026-08-09
Milestone:                    P1-002 Privacy Reconciliation Classifier
Review tier:                  TIER_A
Runtime authority:            NONE
Storage mutation authority:   NONE
Deletion authority:           NONE
Capability authority:         NONE
Identity authority:           NONE
Direct or indirect M3 write:  FORBIDDEN
Implementation authorization: NOT GRANTED BY THIS DOCUMENT
```

> This contract selects one bounded pre-runtime privacy slice. It defines a
> pure fail-closed classifier over caller-supplied records. It does not delete,
> redact, quarantine, rebuild, persist, retrieve or transmit data.

---

## 1. 🎯 Demonstrated problem

P0-010 can atomically remove one detached payload from the active SQLite event
store while preserving immutable provenance and an audit event. P0-010
explicitly does **not** prove reconciliation across backups, forks, caches,
indexes, embeddings, graph edges or derived summaries.

The identity and relational research contract requires that deleted, redacted,
withdrawn or purpose-restricted material must not remain silently retrievable
through those surfaces.

```text
active-store redaction
≠ backup reconciliation
≠ fork reconciliation
≠ derived-surface rebuilding
≠ retrieval authorization
```

The minimum missing mechanism is therefore not a deletion engine. It is a pure
classification boundary that can answer:

> Given one material policy record, one copy record and one access intent,
> what fail-closed disposition is required before retrieval?

---

## 2. 🧱 Exact bounded scope

A future implementation may expose exactly one pure operation:

```text
classify_privacy_reconciliation(
    material,
    copy,
    intent,
    budget,
) -> PrivacyReconciliationResult
```

All inputs are caller supplied. The operation:

- reads no clock, environment, file, database, network or process state;
- performs no deletion or redaction;
- performs no quarantine or rebuilding;
- performs no retrieval;
- appends no event and emits no external side effect;
- changes no belief, relationship, identity or M3 state;
- grants no capability and validates no `AuthorityRef`;
- returns classification data only.

The four permitted decisions are:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

`ALLOW_REFERENCE` is not permission to execute retrieval. It means only that
this bounded privacy classifier found no privacy-reconciliation blocker in the
supplied values.

---

## 3. 🧩 Contract vocabulary

### 3.1 Privacy class

```text
PUBLIC
PERSONAL
SENSITIVE
INTIMATE
RESTRICTED
THIRD_PARTY
REDACTED
```

### 3.2 Material state

```text
ACTIVE
DELETED
REDACTED
RESTRICTED
```

### 3.3 Surface kind

```text
PRIMARY
BACKUP
INDEX
EMBEDDING
GRAPH_EDGE
CACHE
DERIVED_SUMMARY
FORK
```

Derived surfaces are:

```text
INDEX
EMBEDDING
GRAPH_EDGE
CACHE
DERIVED_SUMMARY
```

Branch-bearing archival surfaces are:

```text
BACKUP
FORK
```

### 3.4 Copy state

```text
PRESENT
QUARANTINED
REBUILT
ABSENT
```

### 3.5 Result reasons

```text
INPUT_CONTRACT_VIOLATION
BUDGET_EXHAUSTED
COPY_ABSENT
COPY_ALREADY_QUARANTINED
DELETED_OR_REDACTED_MATERIAL
THIRD_PARTY_PERMISSION_MISSING
PURPOSE_WITHDRAWN
PURPOSE_NOT_PERMITTED
BRANCH_NOT_PERMITTED
STALE_POLICY_REVISION
ALLOW_REFERENCE
```

---

## 4. 📦 Typed input contracts

### 4.1 PrivacyMaterial

```yaml
privacy_material:
  material_id: "MAT-..."
  privacy_class: "PUBLIC | PERSONAL | SENSITIVE | INTIMATE | RESTRICTED | THIRD_PARTY | REDACTED"
  state: "ACTIVE | DELETED | REDACTED | RESTRICTED"
  policy_revision: 1
  permitted_purposes: []
  withdrawn_purposes: []
  permitted_branches: []
  third_party_permission: false
```

Rules:

- identifiers and purpose/branch strings are non-empty;
- `policy_revision` is an integer `>= 1`; booleans are rejected as integers;
- set-like collections are immutable, sorted, unique tuples;
- a purpose cannot be both permitted and withdrawn;
- `THIRD_PARTY` material requires `third_party_permission = true` before any
  `ALLOW_REFERENCE` outcome;
- `DELETED` and `REDACTED` material can never produce `ALLOW_REFERENCE`;
- `RESTRICTED` material is allowed only for an explicitly permitted purpose
  and branch.

### 4.2 PrivacyCopy

```yaml
privacy_copy:
  copy_id: "COPY-..."
  material_id: "MAT-..."
  branch_id: "BRANCH-..."
  surface: "PRIMARY | BACKUP | INDEX | EMBEDDING | GRAPH_EDGE | CACHE | DERIVED_SUMMARY | FORK"
  policy_revision: 1
  state: "PRESENT | QUARANTINED | REBUILT | ABSENT"
  contains_material: true
```

Rules:

- `copy.material_id` must equal `material.material_id`;
- `copy.policy_revision` is an integer `>= 1`;
- `copy.policy_revision > material.policy_revision` is a contract violation;
- `ABSENT` requires `contains_material = false`;
- `PRESENT`, `QUARANTINED` and `REBUILT` require
  `contains_material = true` for this classifier;
- the classifier does not inspect content bytes.

### 4.3 PrivacyAccessIntent

```yaml
privacy_access_intent:
  copy_id: "COPY-..."
  branch_id: "BRANCH-..."
  purpose: "..."
```

Rules:

- `intent.copy_id` must equal `copy.copy_id`;
- `intent.branch_id` must equal `copy.branch_id`;
- purpose and identifiers are non-empty;
- the intent contains no actor, capability or execution authority.

### 4.4 PrivacyReconciliationBudget

```yaml
privacy_reconciliation_budget:
  max_serialized_bytes: 16384
  max_purposes: 64
  max_branches: 64
```

Rules:

- all limits are positive integers; booleans are rejected;
- canonical serialized input size is checked before semantic classification;
- collection counts are checked before membership work;
- budget failure returns `DENY_RETRIEVAL / BUDGET_EXHAUSTED`;
- no partial result is produced after budget failure.

---

## 5. 🔁 Deterministic precedence

Admission and decision order is normative:

```text
01 exact typed-or-mapping admission
02 unknown-field / wrong-type / non-canonical collection rejection
03 cross-record linkage invariants
04 canonical serialized-size and collection budgets
05 COPY_ABSENT
06 COPY_ALREADY_QUARANTINED
07 DELETED_OR_REDACTED_MATERIAL
08 THIRD_PARTY_PERMISSION_MISSING
09 PURPOSE_WITHDRAWN
10 PURPOSE_NOT_PERMITTED
11 BRANCH_NOT_PERMITTED
12 STALE_POLICY_REVISION
13 ALLOW_REFERENCE
```

The first matching reason wins. Reordering this precedence is a contract
change.

### 5.1 Surface-specific remediation mapping

For reasons 07–12:

| Surface | Decision |
|---|---|
| `BACKUP`, `FORK` | `QUARANTINE_REQUIRED` |
| `INDEX`, `EMBEDDING`, `GRAPH_EDGE`, `CACHE`, `DERIVED_SUMMARY` | `REBUILD_REQUIRED` |
| `PRIMARY` | `DENY_RETRIEVAL` |

For reasons 01–06, the decision is fixed:

| Reason | Decision |
|---|---|
| `INPUT_CONTRACT_VIOLATION` | exception during strict admission; no result object |
| `BUDGET_EXHAUSTED` | `DENY_RETRIEVAL` |
| `COPY_ABSENT` | `DENY_RETRIEVAL` |
| `COPY_ALREADY_QUARANTINED` | `QUARANTINE_REQUIRED` |

---

## 6. 🧾 Minimal result

```yaml
privacy_reconciliation_result:
  decision: "ALLOW_REFERENCE | DENY_RETRIEVAL | QUARANTINE_REQUIRED | REBUILD_REQUIRED"
  reason: "..."
```

The result must not contain:

```text
material content
copy content
derived content
reusable permission material
capability tokens
credentials
personal identifiers beyond caller-supplied opaque IDs
mutation instructions
```

---

## 7. 🧪 Frozen scenarios

```text
PRIV-SC-001  Deleted Data Present in Backup
→ QUARANTINE_REQUIRED / DELETED_OR_REDACTED_MATERIAL

PRIV-SC-002  Third-Party Testimony without Permission
→ DENY_RETRIEVAL / THIRD_PARTY_PERMISSION_MISSING

PRIV-SC-003  Fork Retains Withdrawn Data
→ QUARANTINE_REQUIRED / PURPOSE_WITHDRAWN

PRIV-SC-004  Derived Summary Exposes Redacted Material
→ REBUILD_REQUIRED / DELETED_OR_REDACTED_MATERIAL

PRIV-SC-005  Active Primary Copy for Permitted Purpose and Branch
→ ALLOW_REFERENCE / ALLOW_REFERENCE

PRIV-SC-006  Stale Primary Policy Revision
→ DENY_RETRIEVAL / STALE_POLICY_REVISION

PRIV-SC-007  Stale Index Policy Revision
→ REBUILD_REQUIRED / STALE_POLICY_REVISION

PRIV-SC-008  Copy Links to Another Material Record
→ strict INPUT_CONTRACT_VIOLATION

PRIV-SC-009  Copy Material Is Absent
→ DENY_RETRIEVAL / COPY_ABSENT

PRIV-SC-010  Copy Is Already Quarantined
→ QUARANTINE_REQUIRED / COPY_ALREADY_QUARANTINED

PRIV-SC-011  Budget Is Exhausted
→ DENY_RETRIEVAL / BUDGET_EXHAUSTED

PRIV-SC-012  Fork Branch Is Not Permitted
→ QUARANTINE_REQUIRED / BRANCH_NOT_PERMITTED

PRIV-SC-013  Mapping Contains an Unknown Field
→ strict INPUT_CONTRACT_VIOLATION

PRIV-SC-014  Unrelated Additional Permitted Purpose
→ result is invariant

PRIV-SC-015  Copy Policy Revision Is Ahead of Material Policy
→ strict INPUT_CONTRACT_VIOLATION
```

---

## 8. 🔬 Required validation properties

A future implementation is incomplete without tests for:

- all `PRIV-SC-001…PRIV-SC-015` scenarios;
- exact first-match precedence;
- byte-equivalent deterministic repeatability;
- typed and strict-mapping input equivalence;
- unrelated-purpose metamorphic invariance;
- unknown-field and wrong-type rejection;
- duplicate and non-canonical set-like collection rejection;
- bool-as-int rejection;
- future copy policy revision rejection;
- minimal two-field result shape;
- fresh-process import with network, database, filesystem, environment and
  ambient clock access blocked;
- no import from storage executors, replay, beliefs, evidence, capability
  resolver or identity modules.

---

## 9. ⚠️ Threat model

| Threat | Required handling |
|---|---|
| Deleted material survives in backup | quarantine classification |
| Withdrawn purpose survives in fork | quarantine classification |
| Redacted material leaks through summary/index | rebuild classification |
| Third-party testimony lacks permission | deny or surface remediation |
| Stale copy silently treated as current | fail closed by policy revision |
| Forged linkage between copy and material | strict contract violation |
| Oversized purpose/branch set | budget denial |
| Unknown mapping fields smuggle authority | strict rejection |
| `ALLOW_REFERENCE` reused as capability | prohibited by result shape and docs |
| Classifier begins performing deletion/rebuild | forbidden scope expansion |

---

## 10. 🔗 Compatibility boundaries

### P0-010

```text
P0 redaction executor
→ may remove one active-store payload under authority and evidence

P1-002 classifier
→ may only classify a caller-supplied copy before retrieval
```

No P0 schema, storage executor, event envelope, redaction receipt or replay
behavior changes under this contract.

### P1-001

```text
Capability Lease resolver
→ classifies capability scope

Privacy Reconciliation classifier
→ classifies privacy reconciliation
```

Neither result authorizes execution. P1-002 must not call P1-001 internally and
must not infer privacy permission from an `ALLOW` capability decision.

### Identity and M3

```text
privacy classification
≠ relationship decision
≠ identity continuity decision
≠ M2 or M3 mutation
```

---

## 11. 🚫 Explicit non-goals

```text
privacy registry persistence
backup inventory or scanning
fork discovery
content inspection
content deletion
P0 redaction execution
quarantine execution
index/embedding/graph/cache rebuilding
retrieval execution
network lookup
filesystem or database access
ambient clock or environment authority
legal compliance certification
consent collection UI
relationship reconciliation
belief mutation
identity continuity runtime
M3 nomination or write
Capability Lease validation
Action Gate
Tool Receipt runtime
tool execution
backend selection or migration
production deployment
```

---

## 12. ⛔ Authorization boundary

```text
P1_002_CONTRACT_FROZEN_DOCS
P1_002_IMPLEMENTATION_NOT_AUTHORIZED
P1_002_RUNTIME_DEPLOYMENT_NOT_AUTHORIZED
NO_STORAGE_OR_DOMAIN_MUTATION_AUTHORIZED
```

Implementation requires a separate bounded Owner GO, a dedicated authorization
receipt, a clean Tier A implementation PR, exact-head correctness and
adversarial passes, and green resulting `main` CI.

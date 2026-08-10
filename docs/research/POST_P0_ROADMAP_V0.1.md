# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      0.8
Updated:                      2026-08-10
Current review mode:          SOLO_MAINTAINER · TIER_A
P1-001 implementation:        IMPLEMENTED_BOUNDED
P1-002 implementation:        IMPLEMENTED_BOUNDED
P1-002 validation:            EXACT_HEAD_AND_MAIN_CI_PASS
P1-002 Owner GO:              CONSUMED
Post-P1-002 selection:         COMPLETE
Selection result:             NO_RUNTIME_MILESTONE_SELECTED
Next bounded work:            CROSS_GATE_BINDING_AND_COMPOSITION_READINESS · DOCS_ONLY
P1-003 assignment:            NONE
Next runtime milestone:       NOT SELECTED · NOT AUTHORIZED
Runtime deployment authority: NONE
Mutation authority:           NONE
Retrieval authority:          NONE
Direct or indirect M3 write:  FORBIDDEN
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

```text
IMPLEMENTED_BOUNDED ≠ remediation execution
ALLOW_REFERENCE ≠ retrieval permission
privacy classification ≠ privacy mutation
positive classifier results ≠ common-bound authorization
selection decision ≠ implementation GO
P1-002 completion ≠ authority for a later milestone
Solo review ≠ independent certification
```

The filename retains `V0.1` for stable historical links. Document metadata is
the current version authority.

---

## 1. ✅ P1-001 retained checkpoint

```text
Authorization PR:       #62
Implementation PR:      #63
Reviewed head:          e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:          31323051934 · success · 387 passed
Implementation merge:   f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:          31323138053 · success
```

Frozen contract: [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md).
Owning receipt: [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md).

P1-001 remains a pure capability classifier without registry persistence,
Action Gate, tool execution, identity/M3 mutation or deployment authority.
No registry service, Action Gate, P1-002 remediation execution or tool runtime
follows automatically from P1-001.

---

## 2. ✅ Completed P1-002 Privacy Reconciliation Classifier sequence

```text
P0-010 active-store redaction boundary
→ privacy copy-reconciliation gap identified
→ P1-002 contract frozen in PR #65
→ bounded Owner GO merged in PR #66
→ pure classifier implemented in PR #67
→ exact-head correctness and adversarial review passed
→ resulting main CI passed
→ P1-002 IMPLEMENTED_BOUNDED
```

### Contract freeze

```text
Reviewed head:   85bf0070e2f15b5ca752b82325337d6ef0190396
Exact-head CI:   31331396018 · success · 401 passed
Merge:           1dc7bcf97986f455f48beb121c2048dfc34bd11c
Post-merge CI:   31331506606 · success
```

### Authorization

```text
Reviewed head:   670b10c7ea69e3c609453e979a8de6853b23c6bc
Exact-head CI:   31331910395 · success · 398 passed
Merge:           8f4c444e2144d1dffde20fc60d6d5250148d07e6
Post-merge CI:   31331973557 · success
```

### Implementation

```text
Reviewed head:   74662fb626a545ed63b426e98aa03524449019db
Exact-head CI:   31332728486 · success · 461 passed
Merge:           d64679fd745e859527a70746df5e69dc9aca0408
Post-merge CI:   31332793742 · success · 461 passed
Correctness:     PASS
Adversarial:     PASS
Review threads:  0
```

Owning surfaces:

- [Frozen contract](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [Authorization and completion receipt](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [Current status](../CURRENT_STATUS.md)

---

## 3. 🧱 Implemented P1-002 boundary

The pure classifier accepts caller-supplied material, copy, access intent and
budget records. It returns exactly one classification:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

Implemented guarantees:

- strict typed-or-exact-mapping admission;
- immutable contracts and canonical sorted/unique collections;
- exact cross-record linkage;
- future-revision rejection;
- canonical byte-budget over all four inputs;
- fixed budget validation order;
- exact purpose and branch allowlists;
- empty allowlists grant nothing;
- normative first-match precedence;
- surface-specific fail-closed classification;
- minimal two-field result without permission material;
- all `PRIV-SC-001…PRIV-SC-015` frozen scenarios;
- no ambient I/O or clock access at import.

---

## 4. 🛡️ Adversarial corrections retained

Before merge, review found and fixed:

1. an implicit-wildcard interpretation of empty allowlists;
2. manually constructible impossible decision/reason pairs;
3. raw canonical JSON exceptions crossing the contract boundary;
4. nondeterministic multi-budget validation order;
5. byte-budget accounting that initially excluded the budget record.

---

## 5. 🚫 Work not included

```text
privacy registry persistence
backup/fork discovery or scanning
content inspection
content deletion or P0 redaction execution
quarantine execution
index/embedding/graph/cache/summary rebuilding
retrieval execution
network, filesystem or database access
ambient clock or environment authority
event append or replay/projection integration
belief, relationship or identity mutation
M3 nomination or write
Capability Lease invocation from P1-002
Action Gate
Tool Receipt or tool execution
backend selection or migration
production deployment
```

---

## 6. 🔗 Post-P1-002 selection — binding before composition

The next architectural review tested whether P1-001 and P1-002 can already be
safely composed into a new runtime authorization layer.

Result:

```text
NO_RUNTIME_MILESTONE_SELECTED
NEXT_BOUNDED_WORK = CROSS_GATE_BINDING_AND_COMPOSITION_READINESS · DOCS_ONLY
P1_003 = NOT_ASSIGNED
```

The blocker is structural rather than procedural:

- P1-001 `ResolutionResult` does not carry a canonical fingerprint of the
  evaluated purpose, operation, data scope and requested side effects;
- P1-002 `PrivacyReconciliationResult` intentionally contains only `decision`
  and `reason`, with no material/copy/purpose/branch binding;
- therefore independently valid positive results can belong to different
  intents, branches, policy revisions or evaluation moments.

```text
Capability ALLOW for A
+
Privacy ALLOW_REFERENCE for B
≠ authorization for A or B
```

Before any composer is selected for implementation, the architecture must
freeze common request binding, freshness invalidation and fail-closed positive
semantics that cannot be mistaken for execution permission.

Owning decision:
[`POST_P1_002_MILESTONE_SELECTION.md`](POST_P1_002_MILESTONE_SELECTION.md).

---

## 7. ⛔ Next execution gate

```text
P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_IMPLEMENTED_BOUNDED
P1_002_PURE_CLASSIFIER_VALIDATED
P1_002_OWNER_GO_CONSUMED
P1_002_MUTATION_AUTHORITY_NONE
P1_002_RETRIEVAL_AUTHORITY_NONE
POST_P1_002_SELECTION_COMPLETE
NO_RUNTIME_MILESTONE_SELECTED
P1_003_NOT_ASSIGNED
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
```

No deletion, quarantine, rebuild, retrieval, relationship/identity runtime,
Action Gate, tool or deployment work follows automatically. The current next
bounded activity is research/readiness only.

Any future runtime step requires a separate bounded contract, threat model,
Owner GO, Tier A implementation PR and green resulting-main CI. If solving the
binding problem would require changing either frozen P1 contract, that contract
change must be proposed and authorized separately rather than hidden inside a
composer.

---

## 8. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| Readiness/selection decision merged | may select docs-only next work; no implementation authority |
| Contract frozen | `FROZEN_DOCS` |
| Bounded Owner GO merged | `AUTHORIZED_BOUNDED` |
| Code PR merged + green main CI | `IMPLEMENTED_BOUNDED` |
| Remediation/retrieval proposal | new independent authorization cycle required |

GitHub `main` and `docs/CURRENT_STATUS.md` remain authoritative. Notion is a
derived navigation/status surface synchronized only after verified evidence.

---

## 9. 🏁 Formula

```text
P0 complete
→ P1-001 implemented bounded
→ P1-002 contract frozen
→ bounded P1-002 Owner GO
→ pure classifier implemented and validated
→ post-P1-002 architecture selection
→ common binding/freshness gap demonstrated
→ docs-only binding/composition readiness selected
→ STOP before any new runtime milestone
```

### Related

- [`POST_P1_002_MILESTONE_SELECTION.md`](POST_P1_002_MILESTONE_SELECTION.md)
- [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [`../P0_010_ATOMIC_SAME_STREAM_REDACTION.md`](../P0_010_ATOMIC_SAME_STREAM_REDACTION.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)

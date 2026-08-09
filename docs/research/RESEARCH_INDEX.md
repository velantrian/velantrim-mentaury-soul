# 🔬 Mentaury Research Index

```text
Status:                       ADOPTED NAVIGATION · DOCS_ONLY · NON_CANONICAL
Updated:                      2026-08-09
Purpose:                      separate research from execution
Current governance:           SOLO_MAINTAINER
Completed execution milestone:P1-001 · IMPLEMENTED_BOUNDED
Selected execution contract:  P1-002 Privacy Reconciliation Classifier · FROZEN_DOCS
Implementation authorization: P1-002 · AUTHORIZED_BOUNDED · NOT_STARTED
Runtime deployment authority: NONE
Truth authority:              NONE
Identity authority:           NONE
Capability grant authority:   NONE
```

```text
Research presence ≠ roadmap priority
P1-001 completion ≠ authority for P1-002
P1-002 contract freeze ≠ implementation authorization
P1-002 Owner GO ≠ remediation or retrieval authority
Notion explanation ≠ GitHub authority
Solo review ≠ independent human assurance
```

Authoritative governance: [`../GOVERNANCE.md`](../GOVERNANCE.md).

---

## 1. ✅ Completed P1-001 checkpoint

```text
P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

```text
Authorization PR #62
→ merge d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
→ post-merge CI 31322210843 · success

Implementation PR #63
→ reviewed head e873e43331fa7273b92f896b371707e4779b17d4
→ exact-head CI 31323051934 · success · 387 passed
→ merge f21809d8f31a457bd7acfe1d766230973ba9ecf5
→ post-merge CI 31323138053 · success
```

P1-001 remains a pure caller-supplied capability resolver. It provides no
registry service, Action Gate, tool execution, identity/M3 mutation or
production deployment authority.

---

## 2. 🔐 P1-002 Privacy Reconciliation Classifier

Contract authority:

- [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)

Authorization authority:

- [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)

```text
P1_002_CONTRACT_FROZEN_DOCS
P1_002_OWNER_GO_AUTHORIZED_BOUNDED
P1_002_IMPLEMENTATION_NOT_STARTED
P1_002_MUTATION_AUTHORITY_NONE
P1_002_RETRIEVAL_AUTHORITY_NONE
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
```

Contract freeze evidence:

```text
PR #65
→ reviewed head 85bf0070e2f15b5ca752b82325337d6ef0190396
→ exact-head CI 31331396018 · success · 401 passed
→ merge 1dc7bcf97986f455f48beb121c2048dfc34bd11c
→ post-merge CI 31331506606 · success
```

Exact authorized source/test paths:

```text
src/mentaury/privacy/__init__.py
src/mentaury/privacy/reconciliation/__init__.py
src/mentaury/privacy/reconciliation/contracts.py
src/mentaury/privacy/reconciliation/classifier.py
tests/test_privacy_reconciliation_classifier.py
```

Authorized only:

```text
pure caller-supplied classification
strict immutable contracts
exact-field admission
budget checks
cross-record linkage
first-match deny precedence
surface-specific decision mapping
PRIV-SC-001…PRIV-SC-015 validation
```

Still forbidden:

```text
privacy persistence or scanning
content deletion or P0 redaction execution
quarantine or rebuild execution
retrieval execution
network/filesystem/database access
event/replay integration
relationship, belief or identity mutation
M3 write
P1-001 internal invocation
Action Gate, Tool Receipt or tool execution
backend selection
production deployment
```

`ALLOW_REFERENCE` is classification data only and cannot be reused as
permission.

---

## 3. 🧭 Document registry

| Document | Track | Disposition | Runtime |
|---|---|---|---|
| [`../GOVERNANCE.md`](../GOVERNANCE.md) | governance authority | ADOPTED | merge/review policy only |
| [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) | P1-001 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md) | P1-001 receipt | OWNER_GO_CONSUMED | complete |
| [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md) | P1-002 contract | FROZEN_DOCS | code not started |
| [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md) | P1-002 receipt | AUTHORIZED_BOUNDED | exact pure slice only |
| [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) | roadmap | P1-002 authorized bounded | no later runtime authority |
| [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) | active research | docs-only | NOT IMPLEMENTED |
| [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) | active research | docs-only | NOT IMPLEMENTED |
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | external input | non-canonical | NOT AUTHORIZED |
| [`STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`](STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md) | future profiles | not selected | NOT AUTHORIZED |

---

## 4. 🌱 Research backlog

| ID | Direction | Status | Promotion evidence required |
|---|---|---|---|
| `R-ELIDA-001` | Identity as Practice | CAPTURED HYPOTHESIS | longitudinal criteria + falsification |
| `R-NPG-001` | Non-Projection Gate | CAPTURED | claim taxonomy + provenance + threat model |
| `R-HPA-001` | Human Paths Atlas | PARTLY DOCUMENTED | bounded schema + analogy/source limits |
| `R-CO-001` | Controlled Origin | PARTLY DOCUMENTED | consent + provenance + promotion boundaries |
| `R-KDT-001` | Knowledge Density Transformer | CAPTURED | conceptual-core preservation tests |
| `R-VHE-001` | Volumetric Humor | CAPTURED | safety suppression + factuality tests |
| `R-ECN-001` | Epistemic Conflict Navigator | CAPTURED | symmetric evidence + motive guardrails |
| `R-MM-001` | Memory Metabolism | CAPTURED | retention + replay + rollback semantics |
| `R-CHAR-001` | Character runtime | DEFERRED | Non-Projection and belief boundaries |
| `R-ID-001` | Identity / M2→M3 runtime | DEFERRED | longitudinal evidence + authority + rollback |
| `R-REL-001` | Relationship continuity | DEFERRED | privacy + consent + scope contracts |
| `R-DEV-001` | Bounded self-development | DEFERRED | Action Gate + capability authority + reversibility |

---

## 5. 🚪 Promotion gate

```text
problem demonstrated
+ minimal bounded slice
+ explicit contracts and non-goals
+ threat model
+ Canon/P0 compatibility
+ explicit owner authorization
+ clean implementation PR
+ correctness and adversarial review
+ green resulting main CI
```

The P1-002 Owner GO is consumed only by the exact authorized pure classifier.
Issue #39 remains the future transition trigger for genuine independent review.

---

## 6. 🔗 Boundaries

```text
Mentaury research ≠ Crystal Canon ≠ Titan runtime ≠ Native Kernel runtime
Native Kernel input ≠ integration ≠ shared runtime ≠ automatic M2/M3 promotion
```

No backend is selected. Notion remains navigation/research workspace; GitHub
`main`, `docs/CURRENT_STATUS.md` and owning contracts remain engineering
authority.

---

## 7. 🏁 Rule

```text
Keep ideas.
Label their status.
Promote one bounded milestone at a time.
Implement only after explicit Owner GO.
Stop before any unreviewed authority expansion.
```

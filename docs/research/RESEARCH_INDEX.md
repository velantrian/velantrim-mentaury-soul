# 🔬 Mentaury Research Index

```text
Status:                       ADOPTED NAVIGATION · DOCS_ONLY · NON_CANONICAL
Purpose:                      separate research from current execution
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Implementation authority:     NONE
```

> Этот файл — навигационный индекс уже существующих research-документов.
> Он не создаёт новый runtime, не меняет приоритет roadmap и не превращает
> исследовательскую идею в разрешённый milestone.

```text
Research presence ≠ roadmap priority
Research adoption ≠ implementation authorization
Notion explanation ≠ GitHub execution authority
A future idea ≠ an accepted contract
```

### Language policy

```text
Language policy
- narrative context, rationale and human-readable explanations may be written in Russian;
- machine-stable identifiers, schemas, reason codes, algorithms and normative contract terms remain in English;
- translation must not create a second normative source of truth;
- when Russian and English wording conflict, exact identifiers, tables, algorithms and scenario contracts govern.
```

```text
Russian = explanation and context
English = stable technical identifiers and contracts
One normative source of truth
```

---

## 1. 🚀 Current execution boundary

Текущая инженерная правда находится в:

- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md) — authoritative current state;
- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) — принятый post-P0 порядок;
- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) — текущий P1-001 docs-first contract.

```text
Current bounded milestone:
P1-001 Capability Lease Resolution

Current allowed work:
branch-protection follow-up
+ docs hardening
+ independent docs review

Still forbidden:
resolver implementation before explicit owner GO
+ Action Gate
+ tool execution
+ domain runtime
+ direct M3 writes
```

---

## 2. 🧭 Research document registry

| Document | Track | Current disposition | Runtime |
|---|---|---|---|
| [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) | execution-bound research | P1-001 docs hardening / freeze candidate | NOT AUTHORIZED |
| [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) | roadmap | adopted docs-only | NONE |
| [`MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md`](MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md) | active research side-track | adopted docs-only | NOT IMPLEMENTED |
| [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) | active research | adopted docs-only | NOT IMPLEMENTED |
| [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) | active research | adopted docs-only | NOT IMPLEMENTED |
| [`ARCHITECTURE_RECONCILIATION_V0.1.md`](ARCHITECTURE_RECONCILIATION_V0.1.md) | historical architecture decision support | retained reference | NONE |
| [`ARCHITECTURE_READINESS_REVIEW_V0.1.md`](ARCHITECTURE_READINESS_REVIEW_V0.1.md) | historical readiness review | retained reference | NONE |
| [`CONTEXTUAL_COGNITION_POST_MERGE_RECEIPT.md`](CONTEXTUAL_COGNITION_POST_MERGE_RECEIPT.md) | evidence receipt | historical verification record | NONE |
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | external research input | preserved docs-only notes; no execution authority | NOT AUTHORIZED |

---

## 2.1. 🔗 External research input

Эти документы фиксируют внешние идеи как research input. Они не являются
execution milestones и не авторизуют интеграцию.

| Document | External source | Disposition | Runtime |
|---|---|---|---|
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | `velantrim-native-kernel` (via preservation PR #43) | PRESERVED · DOCS_ONLY · NON_CANONICAL | NOT AUTHORIZED |

```text
External research input
≠ Native Kernel integration
≠ shared runtime
≠ authority transfer
≠ automatic M2/M3 promotion
≠ change to P1-001 priority
```

---

## 3. 🌱 Captured future research backlog

Эти направления сохраняются, но пока не являются implementation specs и не
меняют текущий milestone.

| Research ID | Direction | Status | Required before promotion |
|---|---|---|---|
| `R-ELIDA-001` | ELIDA / Identity as Practice | CAPTURED HYPOTHESIS | longitudinal criteria + falsification plan |
| `R-NPG-001` | Non-Projection Gate | CAPTURED | claim taxonomy + provenance contract + threat model |
| `R-HPA-001` | Human Paths Atlas | CAPTURED / PARTLY DOCUMENTED | bounded schema + analogy limits + source rules |
| `R-CO-001` | Controlled Origin / Creator Atlas | CAPTURED / PARTLY DOCUMENTED | consent, provenance and promotion boundaries |
| `R-KDT-001` | Knowledge Density Transformer | CAPTURED | conceptual-core preservation tests |
| `R-VHE-001` | Volumetric Humor Engine | CAPTURED | safety suppression rules + factuality tests |
| `R-ECN-001` | Epistemic Conflict Navigator | CAPTURED | symmetric evidence protocol + motive-claim guardrails |
| `R-MM-001` | Memory Metabolism | CAPTURED | retention semantics + replay + rollback criteria |
| `R-CHAR-001` | Character & Social Adaptability runtime | DEFERRED | Non-Projection and belief boundaries first |
| `R-ID-001` | Identity runtime / M2→M3 promotion | DEFERRED | longitudinal evidence + authority + rollback |
| `R-REL-001` | Relationship continuity | DEFERRED | privacy, consent and scope contracts |
| `R-DEV-001` | Bounded self-development | DEFERRED | Action Gate + capability authority + reversible experiments |

### Explicit non-claims

```text
Identity = Practice
→ working research hypothesis
≠ proven law of digital identity

Human experience may inform Mentaury
≠ Mentaury experienced it

Character adaptation
≠ permission to alter truth conditions

Institutional context
≠ proof of hidden motive
```

---

## 4. 🚪 Promotion gate: Research → Execution

Research may enter the execution roadmap only after all applicable checks pass:

```text
problem demonstrated
+ existing mechanisms shown insufficient
+ minimal bounded slice defined
+ inputs / outputs / invariants specified
+ explicit non-goals recorded
+ threat model recorded
+ Canon and P0 compatibility checked
+ previous milestone completed or explicitly superseded
+ independent architecture review
+ explicit repository-owner authorization
= eligible for execution planning
```

Allowed dispositions:

```text
CAPTURED
EXPLORING
NEEDS_EVIDENCE
EXPERIMENT_READY
DEFERRED
REJECTED
PROMOTION_CANDIDATE
PROMOTED
SUPERSEDED
ARCHIVED
```

No percentage-based maturity score is authoritative unless its denominator and
measurement contract are explicitly defined.

---

## 5. 🧱 Separation from Velantrim Research Mode

```text
Mentaury research track
≠ Velantrim Exo-Cortex Research Mode
≠ Crystal Canon
≠ Titan runtime
≠ Native Kernel runtime
```

Mentaury remains a standalone experimental project. Any future transfer to
another Velantrim system requires a bounded export, quarantine, review, RFC,
independent implementation and target-system validation. Identity state,
private memory, capability state and relationship state do not transfer as
research insight.

---

## 6. 🗺️ Notion navigation

Notion is a human-readable navigation and research workspace. GitHub `main` and
[`../CURRENT_STATUS.md`](../CURRENT_STATUS.md) remain the engineering source of
truth.

Current Notion counterparts include:

- Mentaury main hub / current checkpoint;
- Controlled Origin Research;
- Identity Continuity & Relational Architecture;
- Character & Presence;
- Architecture Readiness & P0 Engineering;
- Research History archive;
- early-research archive.

A Notion research registry may link these pages, but it must remain navigation
only and must not authorize implementation.

---

## 7. 🏁 Operating rule

```text
Keep ideas.
Label their epistemic and implementation status.
Do not let research text impersonate current runtime truth.
Promote one bounded milestone at a time.
```

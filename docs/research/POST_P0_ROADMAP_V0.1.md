# 🗺️ Post-P0 Roadmap v0.1

```text
Status:                       ADOPTED ROADMAP · NON_CANONICAL · DOCS_ONLY
Version:                      0.2-draft
Date:                         2026-08-09
Owner decision:               ACCEPTED DIRECTION
Current review mode:          SOLO_MAINTAINER · TIER_A
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Direct or indirect M3 write:  FORBIDDEN
Domain runtime:               NOT AUTHORIZED
```

> Этот документ определяет один следующий bounded milestone. Он не разрешает
> domain runtime, Tool execution, Action Gate, autonomous external side effects
> или P1 implementation. Имя файла сохранено для стабильности ссылок; metadata
> `Version: 0.2-draft` является version authority.

```text
Roadmap adopted ≠ runtime authorized
Research presence ≠ roadmap priority
First milestone named ≠ milestone implemented
Solo review ≠ independent certification
```

---

## 1. 🎯 Purpose

P0-001…P0-015 сформировали replay-проверяемый event substrate, минимальный
belief lifecycle и Evidence Gate. Следующий шаг — не подключение полного
runtime, а завершение одного ограниченного authority contract:

```text
P1-001 Capability Lease Resolution
→ docs first
→ pure and fail-closed
→ exact lookup
→ explicit budgets
→ no action execution
```

Roadmap сохраняет последовательность:

```text
Truthful status
→ bounded contract
→ exact-head review evidence
→ docs freeze
→ separate explicit owner GO
→ only then consider minimal implementation
```

---

## 2. 🚫 Non-claims

```text
❌ domain runtime or M0–M3 engines authorized
❌ Canon v0.1 changed
❌ AuthorityRef converted into a permission blob
❌ registry or resolver implemented
❌ Tool Receipt or Action Gate runtime added
❌ P1-001 marked Implemented
❌ LLM integration or autonomous goals authorized
❌ research backlog promoted automatically
❌ backend selected
❌ independent human assurance claimed
```

---

## 3. 📦 P0 boundary

```text
P0-001…P0-015     → IMPLEMENTED IN MAIN
P0 event substrate → retained and replay-verifiable
P1-001 resolver    → NOT IMPLEMENTED
DOMAIN_RUNTIME     → NOT AUTHORIZED
```

The remaining authority gap is precise:

```text
AuthorityRef.capability_lease_id + capability_revision
→ recorded
→ equality-checked
→ not resolved against a live lease registry
→ not an enforceable grant
```

`P0 implementation line complete` does not mean operational, governance,
identity or domain-runtime completion.

---

## 4. ✅ First bounded milestone

**P1-001 — Capability Lease Resolution (docs-first).**

It remains first because:

1. authority-sensitive runtime cannot honestly rely on an opaque lease id;
2. the milestone can preserve the existing P0 `AuthorityRef` contract;
3. the resolver can be specified as a pure deterministic boundary;
4. it does not require Character, Human Paths, M3, tools or Action Gate;
5. it can be reviewed and frozen before any code authorization.

```text
P1-001 contract hardening
→ solo Tier A correctness pass
→ solo Tier A adversarial pass
→ exact-head CI and resolved conversations
→ docs freeze
→ separate explicit owner GO
→ possible future minimal implementation PR
```

The absence of an independent reviewer does not freeze docs work during the
current solo phase. When a genuine reviewer/team exists, issue #39 governs the
repository-wide transition for future protected changes.

Deferred and outside P1-001:

```text
Identity Continuity runtime
Controlled Origin ingestion
Non-Projection runtime
Character / Curiosity engines
Human Paths runtime
Knowledge Density / Humor / Conflict Navigator
Tool Receipt runtime
Action Gate execution
Governed Synthesis engine
LLM integration
backend migration or graph-profile selection
```

---

## 5. 🃏 P1-001 milestone card

### 5.1 Goal

Freeze a docs-only contract for resolving immutable `AuthorityRef` values against
an immutable caller-supplied registry snapshot so that a future resolver can be:

```text
pure
fail-closed
deterministic
exact-lookup only
schema-admitted
resource-bounded
adversarial-testable
P0-compatible
```

Owning draft:

[`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)

### 5.2 Threat model

| Threat | Required contract response |
|---|---|
| Registry unavailable | distinct `REGISTRY_UNAVAILABLE` |
| Unknown lease id | exact `UNKNOWN_LEASE` |
| Stale or future revision | exact live-head `REVISION_MISMATCH` |
| Unknown fields / malformed record | schema admission fails closed |
| Forged or stale digest | canonical recomputation and denial |
| Expired or revoked grant | deterministic lifecycle/time denial |
| Cross-purpose reuse | exact purpose identifier equality |
| Cross-scope reuse | typed exact-set containment |
| Wildcard / semantic expansion | forbidden in v0.1 |
| Embedded permission copy | `AuthorityRef` remains id + revision |
| Docs silently becoming runtime | separate explicit owner GO |
| Fork / restore retaining authority | destination grant quarantined as `UNVERIFIED` |
| Resource exhaustion | explicit missing/exhausted budget results |
| Green CI hiding a design flaw | two distinct maintainer review passes |

### 5.3 Authority boundary

```text
AuthorityRef
→ immutable reference: lease_id + revision

CapabilityLeaseRecord
→ immutable bounded registry record

ResolutionResult
→ ALLOW | DENY + one primary reason
≠ truth
≠ identity authority
≠ M3 write
≠ Action Gate pass
≠ tool execution
```

### 5.4 Scope

**In scope — docs:**

- versioned record admission and invariants;
- exact live-head lookup;
- no revision walk;
- digest domain excluding `content_digest`;
- caller-supplied time;
- exact purpose, operation, typed scope and side-effect semantics;
- explicit budgets and deny precedence;
- fork / restore quarantine;
- deterministic and adversarial scenarios;
- P0 compatibility and authorization gates.

**Out of scope:**

- resolver or registry code in `src/`;
- network lookup or system-clock access;
- Tool execution or Action Gate;
- in-flight operation invalidation handling;
- domain, belief, relationship or identity mutation;
- backend selection;
- Canon changes.

### 5.5 Resource budgets

The future resolver receives an explicit `ResolutionBudget`:

```text
max_registry_lookups → exact lookup ceiling
max_record_bytes     → maximum admitted record bytes
max_scope_items      → maximum requested/allowed scope entries examined
```

```text
missing budget object          → BUDGET_MISSING
negative / insufficient ceiling → BUDGET_EXHAUSTED
revision-history walk          → forbidden
network / ambient wall clock   → forbidden dependencies
```

Concrete upper bounds may be tuned only before implementation GO; units and
fail-closed behavior must remain stable.

### 5.6 Replay / rollback / compatibility

```text
resolve() inputs:
RegistrySnapshot
+ AuthorityRef
+ ActionIntent
+ evaluated_at
+ ResolutionBudget
```

P0 events that only record `AuthorityRef` remain replayable without a registry.
P1-001 must not reinterpret or rewrite P0 history.

```text
DENY → no domain write, event append or side effect
ALLOW → still no domain write, event append or side effect inside resolver
```

Execution receipts and in-flight invalidation remain future separate boundaries.

### 5.7 Docs-freeze exit criteria

P1-001 docs may be marked `FROZEN_DOCS` only when one exact head satisfies:

1. the final three-document diff is inspected;
2. required exact-head CI passes;
3. all conversations are resolved;
4. correctness review confirms cross-document consistency;
5. adversarial review confirms fail-closed ordering and preserved authority
   boundaries;
6. schema admission precedes digest and semantic authorization;
7. registry, budget and lifecycle reasons remain distinct;
8. exact lookup and no-history-walk semantics are consistent;
9. scenarios and deny precedence do not contradict each other;
10. `docs/CURRENT_STATUS.md` still says `NOT_IMPLEMENTED / NOT_AUTHORIZED`;
11. the maintainer records `ACCEPTED_FOR_MERGE` under `docs/GOVERNANCE.md`.

```text
FROZEN_DOCS ≠ implementation GO
owner GO ≠ domain runtime authorization
solo acceptance ≠ independent certification
```

---

## 6. 🔐 Authorization gate before `src/`

Any future PR adding lease registry or resolver code requires all of:

1. `FROZEN_DOCS` on `main`;
2. a separate explicit owner amendment in `docs/CURRENT_STATUS.md` authorizing
   only a bounded P1-001 implementation slice;
3. minimal pure implementation scope;
4. a new Tier A exact-head correctness and adversarial review;
5. deterministic, adversarial and metamorphic tests;
6. preserved P0 event and replay compatibility;
7. no Action Gate, tool execution, M3 or domain-runtime expansion;
8. post-merge `main` CI evidence.

When the project later has a real independent reviewer/team, the upgraded live
ruleset defined by issue #39 applies. The current lack of that identity is not an
excuse to fabricate review and not a reason to bypass the solo evidence process.

Until an explicit implementation GO exists:

```text
DOMAIN_RUNTIME_NOT_AUTHORIZED
CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
```

---

## 7. 🧭 Research and execution separation

[`RESEARCH_INDEX.md`](RESEARCH_INDEX.md) preserves research without promoting it.

```text
Research document
→ may capture hypotheses, candidates, risks and experiments

Current execution milestone
→ requires explicit roadmap position and owner authorization
```

Promotion requires demonstrated need, a bounded slice, invariants, non-goals,
threat model, compatibility review, current-governance review and explicit owner
decision.

---

## 8. 🔄 Status synchronization

| Event | Required status behavior |
|---|---|
| Research Index merged | navigation only; no implementation markers change |
| P1-001 docs hardening merged | remain `DOCS_ONLY · NOT_IMPLEMENTED` |
| P1-001 exact-head solo review accepted | docs may be marked frozen if all exit criteria pass |
| Owner authorizes bounded implementation | record explicit scope in `CURRENT_STATUS` |
| P1-001 code merged and main CI passes | only then mark the bounded implementation complete |

GitHub `main` and `docs/CURRENT_STATUS.md` remain engineering authority. Notion
is synchronized only after merge and green post-merge CI.

---

## 9. 🏁 Final formula

```text
P0 implementation line complete
→ Research Index preserves future directions without promotion
→ first execution milestone remains P1-001
→ harden and freeze docs under solo Tier A review
→ explicit owner GO required before src/
→ resolver remains pure and executes nothing
→ domain runtime remains forbidden
```

### Related documents

- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
- [`../governance/solo-maintainer-review-checklist.md`](../governance/solo-maintainer-review-checklist.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`../P0_002_ENVELOPE_CONTRACTS.md`](../P0_002_ENVELOPE_CONTRACTS.md)

# 🗺️ Post-P0 Roadmap v0.1

```text
Статус:                       ADOPTED · ROADMAP · NON_CANONICAL · DOCS_ONLY
Версия:                       0.1 + P1-001 hardening alignment
Дата:                         2026-08-07
Owner decision:               ACCEPTED (repository owner)
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
Domain runtime:               STILL NOT AUTHORIZED
```

> Этот документ определяет один следующий bounded milestone и не разрешает
> domain runtime, Tool execution, Action Gate или автоматические внешние side
> effects. Research-направления сохраняются в [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md),
> но их наличие не меняет порядок выполнения.

```text
Roadmap adopted ≠ runtime authorized
Research presence ≠ roadmap priority
First milestone named ≠ milestone implemented
```

---

## 1. 🎯 Purpose

После P0-001…P0-015 в `main` есть replay-проверяемый event substrate,
минимальный belief lifecycle и Evidence Gate. Следующий шаг — не подключать
полный runtime, а завершить один authority milestone с явными:

- threat model;
- deterministic resolution contract;
- caller-supplied resource budgets;
- replay and compatibility boundary;
- docs-freeze gate;
- independent review before any `src/` authorization.

---

## 2. 🚫 Non-claims

```text
❌ domain runtime / M0–M3 engines authorized
❌ Canon v0.1 changed
❌ AuthorityRef converted into a permission blob
❌ Tool Receipt / Action Gate runtime added
❌ P1-001 marked Implemented
❌ LLM integration or autonomous goals authorized
❌ research backlog promoted automatically
```

---

## 3. 📦 P0 implementation boundary

```text
P0-001…P0-015     → IMPLEMENTED IN MAIN
PR #32            → post-P0-015 audit hardening merged
PR #33 / #37      → authoritative status synchronization merged
DOMAIN_RUNTIME    → NOT AUTHORIZED
```

The current authority gap remains:

```text
AuthorityRef.capability_lease_id + capability_revision
→ recorded and equality-checked
→ not resolved against a lease registry
→ not an enforceable permission grant
```

`P0 implementation line complete` does not mean all governance, operational or
runtime risks are closed.

---

## 4. ✅ First bounded milestone

**P1-001 — Capability Lease Resolution (docs-first).**

Why it remains first:

1. honest authority-sensitive runtime depends on it;
2. it extends an existing AuthorityRef without changing that P0 contract;
3. it can be designed as a pure deterministic boundary;
4. it does not require Character, Human Paths, M3 or Action Gate runtime;
5. the owner already adopted the docs-first path.

```text
P1-001 docs hardening
→ independent exact-head review
→ docs freeze
→ explicit owner GO
→ only then a separate minimal implementation PR may be considered
```

Deferred and not part of P1-001:

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
```

---

## 5. 🃏 P1-001 milestone card

### 5.1 Goal

Freeze a docs-only contract for resolving an immutable `AuthorityRef` against an
immutable caller-supplied registry snapshot so that a future resolver can be:

```text
pure
fail-closed
deterministic
exact-lookup only
resource-bounded
adversarial-testable
P0-compatible
```

Authoritative contract draft:

[`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)

### 5.2 Threat model

| Threat | Required contract response |
|---|---|
| Registry unavailable | distinct fail-closed `REGISTRY_UNAVAILABLE` |
| Unknown lease id | exact `UNKNOWN_LEASE` |
| Stale or future revision | exact live-head `REVISION_MISMATCH` |
| Forged / stale record digest | recompute canonical digest; deny |
| Expired or revoked grant | deterministic lifecycle/time denial |
| Cross-purpose reuse | exact purpose identifier equality |
| Cross-scope reuse | typed exact-set containment |
| Wildcard / semantic expansion | forbidden in v0.1 |
| Embedded permission copy | AuthorityRef remains id + revision only |
| Docs silently becoming runtime | separate explicit owner GO required |
| Fork / restore retaining authority | destination live grant quarantined as UNVERIFIED |
| Resource exhaustion | explicit `BUDGET_MISSING` / `BUDGET_EXHAUSTED` |

### 5.3 Authority boundary

```text
AuthorityRef
→ immutable reference: lease_id + revision

Capability Lease record
→ external immutable registry record

ResolutionResult
→ ALLOW | DENY + one primary machine reason
≠ truth
≠ identity authority
≠ M3 write
≠ Action Gate pass
≠ tool execution
```

### 5.4 In scope / out of scope

**In scope — docs:**

- lease record and invariants;
- exact live-head lookup;
- no revision walk;
- digest domain excluding `content_digest`;
- lifecycle and caller-supplied time;
- exact purpose / operation / typed scope / side-effect semantics;
- explicit budgets and deny precedence;
- fork / restore quarantine;
- resolver-only adversarial scenarios;
- P0 compatibility and authorization gates.

**Out of scope:**

- resolver or registry code in `src/`;
- network lookup or system-clock access;
- Tool execution / Action Gate;
- in-flight operation invalidation handling;
- domain or identity mutation;
- branch-protection automation;
- Canon changes.

### 5.5 Resource budgets

The future resolver must accept an explicit `ResolutionBudget` with named units.
The initial contract uses:

```text
max_registry_lookups   → exact lookup ceiling; v0.1 requires at least 1
max_canonical_bytes    → maximum admitted lease bytes for digest recomputation
max_scope_items        → maximum requested/allowed typed scope entries examined
```

Normative rules:

```text
missing budget object → BUDGET_MISSING
negative or insufficient ceiling → BUDGET_EXHAUSTED
revision history walk → forbidden, budget = 0
network or wall-clock budget → not applicable; both dependencies are forbidden
```

Concrete upper bounds may be tuned before implementation GO, but the units,
precedence and fail-closed behavior must be frozen first.

### 5.6 Replay / rollback / compatibility

```text
resolve() is a pure function of:
registry snapshot
+ AuthorityRef
+ ActionIntent
+ evaluated_at
+ ResolutionBudget
```

P0 events that only record AuthorityRef remain replayable without a registry.
P1-001 does not retroactively reinterpret or rewrite P0 events.

```text
DENY → no domain write, no event append, no side effect
ALLOW → still no domain write, event append or side effect inside resolver
```

A future execution receipt is a separate milestone. The old cross-boundary
scenario where a lease becomes invalid during an operation is not a resolver
scenario and does not belong to P1-001 tests.

### 5.7 Docs-freeze exit criteria

P1-001 docs are frozen only when:

1. the lease notes have explicit non-claims and typed inputs;
2. digest self-reference is removed by an exact exclusion rule;
3. `REGISTRY_UNAVAILABLE`, `BUDGET_MISSING` and `BUDGET_EXHAUSTED` are distinct;
4. one normative first-match deny table exists;
5. purpose, operation and scope semantics are exact, with no wildcard or semantic matching;
6. exact live-head lookup replaces revision walking;
7. lifecycle, time, supersession and fork/restore semantics are unambiguous;
8. resolver scenarios CAP-SC-001…020 are internally consistent;
9. independent exact-head review passes under the adopted policy;
10. `CURRENT_STATUS` still says implementation is not authorized.

```text
Docs freeze ≠ owner GO
Owner GO ≠ full domain runtime authorization
```

---

## 6. 🔐 Authorization gate before `src/`

Any PR adding a lease registry or resolver requires all of:

1. frozen P1-001 docs;
2. independent docs review from a distinct operator identity;
3. explicit owner amendment in `CURRENT_STATUS` stating only P1-001
   implementation is authorized;
4. minimal pure implementation scope;
5. merge-blocking independent review on authority/lease paths;
6. deterministic, adversarial and metamorphic tests;
7. preserved prohibitions on Action Gate, external execution and M3 writes.

Until then:

```text
DOMAIN_RUNTIME_NOT_AUTHORIZED
CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
DIRECT_M3_WRITE_FORBIDDEN
```

---

## 7. 🧭 Research and execution separation

[`RESEARCH_INDEX.md`](RESEARCH_INDEX.md) preserves current and future ideas
without promoting them.

```text
Research document
→ may capture hypotheses, risks and possible experiments

Current execution milestone
→ requires explicit roadmap position and owner authorization
```

A research item can enter execution planning only through a bounded promotion
decision with problem evidence, invariants, threat model, non-goals,
compatibility review and explicit owner approval.

---

## 8. 🔄 Status synchronization

| Event | Required status behavior |
|---|---|
| Research index merged | navigation only; no implementation marker changes |
| P1-001 hardening PR merged | remain `DOCS_ONLY · NOT_IMPLEMENTED`; note docs under freeze review |
| P1-001 docs independently approved | mark docs frozen; implementation still unauthorized |
| Owner issues narrow implementation GO | record explicit authorization scope |
| P1-001 code merged and main CI passes | only then mark P1-001 implemented |

GitHub `main` + `docs/CURRENT_STATUS.md` remain engineering truth. Notion is
synchronized after merge and green main CI.

---

## 9. 🏁 Final formula

```text
P0 implementation line complete
→ Research Index preserves future directions without promotion
→ first execution milestone remains P1-001
→ harden and independently freeze docs
→ explicit owner GO required before src/
→ resolver remains pure and does not execute actions
→ domain runtime remains forbidden
```

### Related documents

- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`../P0_002_ENVELOPE_CONTRACTS.md`](../P0_002_ENVELOPE_CONTRACTS.md)
- [`ARCHITECTURE_RECONCILIATION_V0.1.md`](ARCHITECTURE_RECONCILIATION_V0.1.md)

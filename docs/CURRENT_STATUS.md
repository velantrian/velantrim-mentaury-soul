# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации:                  2026-08-07
Репозиторий:                    velantrian/velantrim-mentaury-soul
Authoritative ref:              GitHub main
Verified implementation head:  0e29c9ebc9c9f2ab9a228a32899e9db8021923c1

CANON_V0.1_FROZEN
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P0-014_BELIEF_LIFECYCLE_PR_AND_MAIN_VALIDATION_PASS
P0-015_EVIDENCE_GATE_PR_AND_MAIN_VALIDATION_PASS
AUDIT_2026_08_06_HARDENING_MERGED_PR_32
POST_P0_ROADMAP_V0.1_ADOPTED_DOCS_ONLY
P1_001_CAPABILITY_LEASE_RESOLUTION_DOCS_ONLY_NOT_IMPLEMENTED
GOVERNANCE_INDEPENDENT_REVIEW_POLICY_ADOPTED
POST_P0_OWNER_PATH_MERGED_PR_34
PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED
DOMAIN_RUNTIME_NOT_AUTHORIZED
CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

## ⚖️ Правило текущей правды

```text
IMPLEMENTED
= merged into GitHub main

OPEN PR
≠ implemented in main

VALIDATION-ONLY WORKFLOW
≠ permanent project CI

Notion / README / Quick Reference
= derived navigation documents

Current maturity authority
= this file + verified GitHub main state
```

---

# ✅ Реализовано в `main`

| Milestone | Состояние | Проверенная граница |
|---|---|---|
| P0-001 Neutral Skeleton | ✅ Implemented | project/package boundary only |
| P0-002 Envelope Contracts | ✅ Implemented | construction ≠ authority approval |
| P0-003 Canonical JSON v1 | ✅ Implemented | canonical bytes ≠ truth or authorization |
| P0-004 Event/Payload Storage | ✅ Implemented | persisted rows ≠ complete integrity proof |
| P0-005 Structural Schema Validation | ✅ Implemented | schema validity ≠ semantic correctness |
| P0-006 Atomic Multi-Event Batch | ✅ Implemented | atomicity ≠ idempotency or concurrency |
| P0-007 Event-Aware Idempotency | ✅ Implemented | replay receipt ≠ integrity verification |
| P0-008 Transactional Concurrency | ✅ Implemented | SQLite locking ≠ distributed consensus |
| P0-009 Trusted Commit + Full R0 | ✅ Implemented | R0 consistency ≠ epistemic truth |
| P0-010 Atomic Same-Stream Redaction | ✅ Implemented | payload removal ≠ event-provenance deletion |
| P0-011 Adversarial Integrity Suite | ✅ Implemented | adversarial PASS ≠ total-database authenticity |
| P0-012 Permanent GitHub Actions CI | ✅ Implemented | green CI ≠ branch protection or runtime safety |
| P0-013 R1 Deterministic Replay | ✅ Implemented | deterministic replay ≠ epistemic truth |
| P0-014 Minimal Belief Lifecycle | ✅ Implemented | belief status ≠ truth or runtime authority |
| P0-015 Deterministic Evidence Gate | ✅ Implemented | gate receipt ≠ externally verified fact |

---

# 🔗 P0-009 — принятый инженерный предел

Merged PR:

```text
PR:       #15
Title:    P0-009: trusted commit boundary and full R0 integrity
Merged:   YES
Main SHA: 08c0e8b5b33aeaa283de4d9ece1f65669d09afd2
```

Реализовано:

- mandatory `SchemaRegistry` admission для production writes;
- canonical payload bytes shared by validation, hashing and persistence;
- payload digest, previous hash и event hash allocated in the trusted transaction boundary;
- transactional `stream_meta` schema v3;
- full R0 verification of canonical payload bytes, schema, digest, chain, versions, batches and metadata;
- explicit caller-supplied `VerificationBudget` for R0 and populated migration;
- fail-closed populated v2 → v3 migration;
- rollback on busy and unexpected `COMMIT` failures;
- exact-one `OneOfSpec` semantics;
- controlled cyclic-payload rejection.

Финальная validation-only проверка exact PR head:

```text
PR head             → 6f8ff1663e161e554c8d4610f1692187c2129b45
Run                  → 31023788916
Python 3.13          → PASS
Locked dependencies  → PASS
Structural validator → PASS
Full pytest          → PASS
Compileall            → PASS
```

Workflow существовал только на отдельной validation-ветке и не был добавлен в
PR #15 или `main`.

```text
R0 consistency ≠ epistemic truth
Schema admission ≠ authority approval
Hash continuity ≠ authorization
Resource budget ≠ Canonical threshold
Validation-only workflow ≠ P0-012
R0 PASS ≠ R1 replay equivalence
```

---

# ✅ P0-010 — Atomic Same-Stream Redaction

Merged PR:

```text
PR:                #19
Final tested head: e141e31f60f7a9aee78642fe3fe3b44570ced733
Merge SHA:         7f78dd2c7db45206f293f0278a51033474db4918
Validation run:    31074885346
Python:            CPython 3.13.14
Full pytest:       144 passed
Review:            Copilot 9/9 files, 0 new comments
```

Реализовано:

- immutable schema-v4 `redactions` evidence;
- one-transaction payload removal, audit append, `stream_meta` update and linkage write;
- preservation of the immutable target event row and original hash chain;
- complete R0 verification of redaction row → target event → audit event → canonical audit payload;
- fail-closed handling for forged, missing, cross-stream or inconsistent evidence;
- caller-supplied `VerificationBudget` applied before linked audit-payload decoding;
- authority-scoped semantic idempotency and deterministic rollback behavior;
- focused concurrency and adversarial regression coverage.

```text
Governed redaction ≠ epistemic truth
Payload removal ≠ event-provenance deletion
SQLite deletion ≠ backup-wide erasure proof
R0 PASS ≠ R1 replay equivalence
P0-010 merged ≠ domain consent/privacy runtime
```

---


# ✅ P0-011 — Adversarial Integrity Suite

Merged PR:

```text
PR:                #21
Final tested head: c21fe2503a31a73e1fe17e89dc92841ed35a65f3
Merge SHA:         5640bd6ce650818c731e09391434ac12a0aec5e6
Validation run:    31084297081
Python:            CPython 3.13.14
Full pytest:       163 passed
Review:            two-pass exact-head audit; automated review quota unavailable
```

Реализовано:

- 19 adversarial attack families across R0, governed redaction and idempotency receipts;
- actual middle/tail event-deletion detection;
- malformed, noncanonical and forged payload/chain proofs;
- redacted-payload reappearance and linked-audit corruption proofs;
- controlled `IdempotencyReceiptIntegrityError`;
- canonical stored receipt shape and version-span validation;
- receipt binding to command target, expected version and fingerprinted pending batch;
- event existence, batch shape/order, semantics, payload digest, initiator and authority checks;
- rollback without replacement writes on corrupted replay evidence.

```text
Adversarial R0 PASS ≠ epistemic truth
Idempotency receipt verification ≠ full R0 verification
Local unkeyed hash chain ≠ total-database authenticity
P0-011 merged ≠ permanent CI
P0-011 merged ≠ R1 replay
```

---


# ✅ P0-012 — Permanent GitHub Actions CI

Merged PR and retained workflow:

```text
PR:                  #25
Final tested head:   49d752285e4c1c3fdb59382e916e32e9862d5f89
Merge SHA:           a536ea0afa526e86827f5ce9d5aa6fd5b7170fab
PR workflow run:     31085542227
Main push run:       31085727308
Python:              CPython 3.13.14
Full pytest:         163 passed on PR and main
Token permissions:  contents: read · metadata: read
```

Реализовано:

- retained `.github/workflows/ci.yml` on pull requests and pushes to `main`;
- explicit immutable PR-head or push-SHA checkout;
- `persist-credentials: false`;
- full commit-SHA pins for checkout and Python setup actions;
- locked development-tool installation and `pip check`;
- structural validator, complete pytest and compileall;
- concurrency cancellation and bounded job timeout;
- no secrets, artifacts, deployments or repository writes.

```text
Green CI ≠ epistemic truth
Green CI ≠ authority approval
P0-012 ≠ branch-protection enforcement
GitHub-hosted runner ≠ production substrate
P0-012 merged ≠ R1 deterministic replay
P0-012 merged ≠ domain runtime authorization
```

---


# ✅ P0-013 — R1 Deterministic Replay

Merged PR and retained workflow evidence:

```text
PR:                  #27
Final tested head:   d5be2702f71a800c6d171a2c4cbea2cd449a2e64
Merge SHA:           cd069e97200d6381806642a438ec2bc64b71571e
PR workflow run:     31087648122
Main push run:       31087777833
Python:              CPython 3.13.14
Full pytest:         186 passed on PR and main
Review:              exact-head two-pass audit 4872928159
```

Реализовано:

- neutral versioned `ReplayReducer`, immutable `ReplaySnapshot`, `ReplayStateBudget` and `R1ReplayReport`;
- bounded R0 prerequisite and domain-separated canonical projection-state hash;
- one SQLite read snapshot across R0, event capture, metadata, payload reads and replay;
- fail-closed refusal to certify outer uncommitted transactions;
- exact verified-prefix version and tail-event-hash reporting under concurrent append;
- snapshot reducer/stream/version/anchor/hash verification;
- full-replay checkpoint equality before snapshot-tail replay;
- replay-time canonical payload and immutable digest verification;
- fail-closed state-affecting redaction boundary;
- immutable reducer inputs and dual transition execution;
- observable nondeterminism, input reuse, reducer exception and invalid-state rejection;
- caller-supplied event/payload and projection-state resource budgets;
- 23 replay-specific tests within the permanent 186-test suite.

```text
R1 PASS ≠ epistemic truth
R1 PASS ≠ reducer semantic correctness
R1 PASS ≠ hidden-side-effect proof
R1 PASS ≠ snapshot persistence authorization
P0-013 merged ≠ P0-014 belief lifecycle
P0-013 merged ≠ domain runtime authorization
```

Automated external code review remained unavailable because the connected review
quota was exhausted. Review `4872928159` records a second-pass exact-head audit
without claiming independent external approval.

---

# ✅ P0-014 — Minimal Belief Lifecycle

```text
PR:                  #29
Final tested head:   fe3ae74d4ef92fc06ab1bee4def88066ded402a5
Merge SHA:           3ff90816b8d095987a8adcdc2cb633c128877212
PR workflow run:     31090898077
Main push run:       31091006506
Python:              CPython 3.13.14
Full pytest:         208 passed on PR and main
Review:              exact-head audit 4873291547
```

Реализовано:

- strict belief-domain and non-state decision schemas;
- pure create, evidence-attach, contradiction and revision decisions;
- immutable revision, evidence and contradiction history;
- shared lifecycle/reducer status policy and terminal supersession;
- fail-closed direct-event policy enforcement;
- explicit separation of stream CAS version and belief revision;
- R1-compatible projection where audit events do not mutate domain state;
- `supported` and `contradicted` reserved for P0-015.

```text
Belief projection ≠ truth
AuthorityRef ≠ validated capability lease
P0-014 merged ≠ domain runtime authorization
```

---

# ✅ P0-015 — Deterministic Evidence Gate

```text
PR:                  #30
Final tested head:   71acd7410c5080e4ac3245b53534b512b871bae5
Merge SHA:           d6a07336b5167c5fc1cc8e2f05413a7284bea0ec
Audit hardening run: 31093091082
PR workflow run:     31093258104
Main push run:       31093382362
Python:              CPython 3.13.14
Full pytest:         232 passed on PR and main
Review:              exact-head two-pass audit 4873644214
```

Реализовано:

- immutable evidence records and closed approved-policy registry;
- deterministic content-addressed receipts bound to belief, revision, statement, policy, time and complete evidence set;
- complete record coverage, freshness, revocation, quality and 256-record budget;
- content/provenance uniqueness and source-group independence controls;
- fail-closed conflict when qualifying evidence exists on both sides;
- shipped policy limited to classified contextual claims;
- pure gate decisions and non-state rejection audits;
- reducer v2 that binds stream/time/state semantics and recomputes the full receipt during R1 replay;
- adversarial receipt, policy, record, ordering, time, stream and status tests.

```text
Evidence Gate receipt ≠ objective truth
Evidence record ≠ externally authenticated source
P0-015 merged ≠ M3 update, autonomous learning or runtime authority
```

---

# ✅ P0 implementation line complete

```text
P0-001…P0-015 → IMPLEMENTED, MERGED AND RETAINED-CI VALIDATED
```

This closes the current P0 implementation plan. It does not authorize a
long-running agent, domain service, M3 mutation path, tool execution or external
action boundary.

---

# ✅ Post-P0-015 audit hardening — PR #32

Merged PR:

```text
PR:                  #32
Merge SHA:           e15864e7837b2c12e7574b55678340c25e15c003
Main push run:       31150100906
Python:              CPython 3.13.14
Full pytest:         277 passed on main
Scope:               hardening + derived-doc sync; no new P0 milestone
```

Реализовано после внешнего аудита линии P0-014/P0-015:

- lifecycle/reducer invariant: `BeliefLifecycle.decide()` now rejects
  `ATTACH_EVIDENCE` / `REGISTER_CONTRADICTION` / `REVISE_BELIEF` on Evidence
  Gate-owned (`supported` / `contradicted`) beliefs via
  `BeliefRejectionCode.EVIDENCE_GATE_OWNED_BELIEF`, matching
  `BeliefReducer.apply()`;
- structural `StringSpec.pattern` + shared `sha256_digest_spec()` for all
  Evidence Gate digest fields at schema-admission boundary;
- derived-status doc freshness gate (`scripts/check_doc_freshness.py`) wired
  into permanent CI and `make check`;
- CI job `timeout-minutes` raised to 30 after a GitHub Actions platform outage
  left jobs queued with `runner_id=0` and cancelled before any step ran;
- governance findings initially recorded as recommendations pending owner
  decision (later adopted as policy in PR #34).

```text
Audit hardening merged ≠ new P0 milestone
Green post-merge CI ≠ POST-P0 roadmap authorization
Governance recommendations ≠ adopted policy
```

---

# 🚫 Domain runtime не авторизован

Пока отсутствуют:

- M0/M1/M2/M3 domain runtime;
- belief lifecycle runtime;
- Identity Continuity runtime;
- relationship and commitment runtime;
- Controlled Origin ingestion;
- Genesis Heritage and Human Paths Atlas runtime;
- Governed Synthesis engine;
- Capability Lease resolver;
- Tool Receipt / Action Gate runtime;
- Character Engine;
- Curiosity controller;
- Titan, Crystal или Native Kernel runtime integration;
- LLM integration и autonomous goals.

Документация этих областей существует как `DOCS_ONLY`, `NON_CANONICAL` или
`PRESENTATION_ONLY` research. Она не является работающим domain runtime.

---

# 🗺️ Контролируемая последовательность

```text
P0-001…P0-015 ✅ merged and validated in main
→ define a separate post-P0 roadmap before additional implementation
→ preserve DOMAIN_RUNTIME_NOT_AUTHORIZED
```

# 🔍 Governance gap identified by audit (2026-08-06)

Every merged PR from P0-001 through P0-015 was authored, self-reviewed and
merged by the same operator account (`velantrian`). Starting with PR #27,
review text has honestly disclosed this: "This is a same-operator audit, not
an independent third-party approval" (PR #30), and "Automated external code
review remained unavailable because the connected review quota was
exhausted" (PR #27, #29). This transparency is good, but the gap itself is
unresolved, and it already produced a real defect: a P0-014/P0-015 boundary
bug where `BeliefLifecycle.decide()` accepted `ATTACH_EVIDENCE` and
`REGISTER_CONTRADICTION` commands against an already Evidence Gate-owned
(`supported`/`contradicted`) belief, while `BeliefReducer.apply()` correctly
rejected the same event — a decision/reducer boundary mismatch that the
same-operator review across two adjacent same-day PRs did not catch. Fixed
under this audit with a matching lifecycle-side rejection and a whole-status
matrix regression test; see the belief lifecycle module history for detail.

```text
Same-operator review ≠ independent third-party approval
Self-audit passing ≠ absence of cross-PR boundary regressions
Documented gap ≠ closed gap
```

# ✅ Owner decisions (2026-08-07) — governance + post-P0 path

Repository owner explicitly accepted the 2026-08-06 audit recommendations
and authorized the docs-only post-P0 path below. This section is now
**adopted project policy**, not a pending proposal.

## A. Independent review policy (adopted)

**Rule:** changes that touch any of the following paths require a
merge-blocking review from someone (human or automated reviewer) who is
**not** the same operator that authored the change:

```text
src/mentaury/beliefs/**
src/mentaury/evidence/**
src/mentaury/replay/**
src/mentaury/**/authority/**          # if/when created
src/mentaury/**/lease/**              # if/when created
docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
docs/research/POST_P0_ROADMAP_V0.1.md
```

Resolved owner answers:

```text
Review mode:              merge-blocking (not advisory-only)
Path scope:               paths listed above
Second AI reviewer:       counts as interim independent review
                          when distinct from the authoring operator;
                          human review preferred when available
Fallback if unavailable:  do not merge protected-path changes
Emergency security fix:   allowed with public disclosure in the PR
                          and mandatory post-hoc independent review
                          within 7 days
Who may lift / amend:     repository owner (velantrian) only, via
                          explicit CURRENT_STATUS amendment
```

```text
Adopted policy ≠ GitHub branch-protection already configured
Docs policy MUST still be enforced in review practice until
repository settings mirror it
```

## B. Post-P0 Roadmap v0.1 (adopted, docs-only)

Authoritative roadmap:

[`docs/research/POST_P0_ROADMAP_V0.1.md`](research/POST_P0_ROADMAP_V0.1.md)

```text
POST-P0 ROADMAP REVIEW → CLOSED by adoption of v0.1
First bounded milestone → P1-001 Capability Lease Resolution (docs-first)
Domain runtime          → still NOT AUTHORIZED
```

## C. Capability Lease resolution notes (docs-only, NOT IMPLEMENTED)

Authoritative notes:

[`docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)

```text
P1-001 status:     DOCS_ONLY · NOT IMPLEMENTED
Freshness markers: remain P0-001…P0-015_IMPLEMENTED_IN_MAIN
Resolver in src/:  NOT AUTHORIZED until separate owner GO after
                   docs freeze + independent review
```

As implemented through P0-015 / audit hardening, `capability_lease_id` is
still only recorded and equality-checked. These notes define how a future
fail-closed resolver MUST behave; they do not make `AuthorityRef` a
validated permission grant.

### Merge evidence — PR #34

```text
PR:                  #34
Merge SHA:           0e29c9ebc9c9f2ab9a228a32899e9db8021923c1
Main push run:       31153454503
Python:              CPython 3.13.14
Full pytest:         277 passed on main
Scope:               docs/policy only; no src/ lease resolver
Copilot review:      4 consistency nits addressed before merge
```

```text
Owner path merged ≠ P1-001 Implemented
Docs adopted ≠ capability lease resolver authorized
Green CI ≠ domain runtime GO
```

---

# 🏁 Следующее действие

```text
P1-001 Capability Lease Resolution
Status:              DOCS_ONLY · NOT IMPLEMENTED · MERGED IN MAIN (PR #34)
Roadmap:             POST_P0_ROADMAP_V0.1 adopted
Docs:                research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
Next concrete step:  independent review + docs freeze of lease notes
Ops follow-up:       mirror independent-review policy in GitHub branch protection
Forbidden until GO:  src/ lease registry, resolve(), Action Gate, domain runtime
```

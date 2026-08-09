# Mentaury Soul — Governance risk-tier policy

**Status:** ADOPTED  
**Current operating mode:** SOLO MAINTAINER  
**Canonical merge-gate authority:** this document, the live GitHub ruleset, and `docs/governance/solo-maintainer-mode.md`  
**Maturity authority:** `docs/CURRENT_STATUS.md` plus verified live GitHub state

The repository currently has one maintainer and no genuinely independent human reviewer.
That is an explicit operating condition, not a defect to conceal and not a reason to stop
all work indefinitely.

```text
solo maintainer review ≠ independent human review
review automation ≠ independent human approval
green CI ≠ proof of semantic correctness
merge authority ≠ runtime authority
```

Any older repository text that requires an unavailable independent approval for current
solo operation is superseded by this policy. Historical statements remain provenance,
not an active merge blocker.

---

## 1. Authority order

For merge decisions, use this order:

1. live GitHub ruleset and required checks;
2. `docs/GOVERNANCE.md`;
3. `docs/governance/solo-maintainer-mode.md`;
4. `CODEOWNERS` as ownership/navigation metadata;
5. PR-local status notes.

PR-local text may not invent a permanent gate that contradicts this policy. A stale
`BLOCKED_BY_INDEPENDENT_REVIEW` or `BLOCKED_BY_GOVERNANCE_IDENTITY` statement must be
reconciled before merge.

The current live ruleset requires:

- pull requests before merging to `main`;
- the required CI check;
- the PR branch to be up to date with `main`;
- all review conversations to be resolved;
- force-push protection;
- deletion protection;
- no bypass actors;
- `required approvals = 0` during solo-maintainer operation.

---

## 2. Standard merge statuses

Use only clear, evidence-based statuses:

```text
DRAFT
READY_FOR_MAINTAINER_REVIEW
BLOCKED_BY_CI
BLOCKED_BY_CONFLICT
BLOCKED_BY_CHANGES_REQUESTED
BLOCKED_BY_UNRESOLVED_CONVERSATION
BLOCKED_BY_AUTHORIZATION_BOUNDARY
ACCEPTED_FOR_MERGE
MERGED
```

Do not use missing reviewer identity as a current blocker while the repository remains in
solo-maintainer mode.

---

## 3. Risk classification

A PR is classified by its highest-risk file or semantic effect.

### 3.1 Tier A — integrity, authority, security, governance, or runtime-capable core

Typical Tier A paths include:

```text
src/mentaury/storage/**
src/mentaury/replay/**
src/mentaury/beliefs/**
src/mentaury/evidence/**
src/mentaury/**/authority/**
src/mentaury/**/lease/**
src/mentaury/contracts/canonical_json.py
scripts/validate.py
scripts/check_doc_freshness.py
.github/workflows/**
requirements*.lock
pyproject.toml
CODEOWNERS
docs/CURRENT_STATUS.md
docs/GOVERNANCE.md
docs/governance/**
docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
docs/research/POST_P0_ROADMAP_V0.1.md
```

Tier A requirements in solo mode:

- exact current head SHA recorded;
- complete final diff inspected;
- required exact-head CI green;
- branch up to date with `main`;
- all review conversations resolved;
- two-pass maintainer review completed;
- architecture, invariant, fail-closed, security, and authorization boundaries checked;
- no unresolved material concern hidden behind a green test suite;
- explicit maintainer decision recorded before merge;
- post-merge `main` CI verified.

The two passes must be meaningfully different:

1. **Correctness pass** — design, behavior, compatibility, tests, and scope.
2. **Adversarial pass** — failure modes, integrity, authorization, rollback, security,
   misleading claims, and hidden privilege expansion.

Automated analysis may support either pass, but the repository must not label it as
independent human review.

### 3.2 Tier B — bounded tooling and non-authoritative project documentation

Typical Tier B examples:

```text
docs/ENVIRONMENT_MANIFEST.md
docs/MENTAURY_QUICK_REFERENCE.md
non-authoritative architecture documentation
developer tooling outside validation/security boundaries
```

Requirements:

- final diff inspected;
- green CI where applicable;
- no unresolved conversations;
- no runtime, authority, security, or maturity escalation hidden in the change;
- maintainer acceptance recorded.

### 3.3 Tier C — editorial, navigation, and research capture

Typical Tier C examples:

```text
spelling and formatting
navigation-only changes
non-authoritative research notes
candidate capture without implementation selection
```

Requirements:

- scope remains editorial or research-only;
- no Canon, roadmap, backend, runtime, truth, or authority promotion is implied;
- green CI where applicable;
- maintainer acceptance recorded.

A nominal Tier B or Tier C PR automatically escalates to Tier A when it changes Tier A
paths or has Tier A semantic effect.

---

## 4. Solo-maintainer review record

For Tier A, the PR or linked issue should record:

```text
Review mode: SOLO_MAINTAINER
Independent human review claimed: NO
Reviewed head: <SHA>
Changed files: <LIST>
Exact-head CI: <RUN / RESULT>
Correctness pass: PASS / CONCERNS
Adversarial pass: PASS / CONCERNS
Authorization boundary: PRESERVED / CHANGED
Decision: ACCEPTED_FOR_MERGE / STOP
```

The reusable checklist is maintained in
`docs/governance/solo-maintainer-review-checklist.md`.

A self-review must not be described as independent, external, second-party, or certified.
Honest attribution is mandatory.

---

## 5. Security and emergency maintenance

A narrowly scoped security or dependency update may be merged after:

- exact scope confirmation;
- affected/fixed boundary confirmation;
- exact-head CI;
- runtime-impact assessment;
- maintainer security review;
- post-merge CI.

A post-hoc review issue may be used when necessary, but it must be completable under the
current solo mode. It must not require a reviewer who does not exist.

---

## 6. Bots and automation

Cursor, Codex, Copilot, ChatGPT, and other agents may:

- inspect repository state;
- create branches and commits;
- open and update PRs;
- run or inspect validation;
- prepare review evidence;
- respond to review feedback;
- merge only when the live ruleset and this policy are satisfied and the operator has
  authorized autonomous completion.

They may not:

- claim independent human approval;
- bypass required checks or unresolved conversations;
- silently broaden scope;
- interpret green CI as proof of production readiness or runtime authorization;
- weaken epistemic, integrity, safety, or authorization boundaries merely to merge a PR.

---

## 7. Transition to public or team operation

Independent approval becomes a real gate only when a genuine independent collaborator or
review team exists.

Before public or multi-contributor operation:

- add a genuinely independent trusted reviewer or team;
- set required approvals to `1`;
- enable dismissal of stale approvals;
- require approval of the latest reviewable push by someone other than its author;
- enable CODEOWNER review only when CODEOWNERS maps to a distinct trusted identity/team;
- retain CI, up-to-date branch, conversation-resolution, force-push, and deletion gates;
- verify the upgraded ruleset with a harmless probe;
- update GitHub documentation and synchronize Notion.

This transition is tracked by issue #39. Until those conditions exist, issue #39 is a
future lifecycle trigger, not a current development blocker.

---

## 8. Explicit non-claims

This governance policy does not authorize:

```text
identity runtime
Character runtime
M3 writes
Action Gate or external tool execution
P1-001 resolver implementation
backend selection or integration
production deployment claims
objective truth claims
```

Use precise terms such as `docs-only`, `research`, `runtime-capable`,
`integrity-sensitive`, `not implemented`, and `not authorized` according to the verified
state.
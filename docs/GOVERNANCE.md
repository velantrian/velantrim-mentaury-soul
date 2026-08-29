# Mentaury Soul — Governance risk-tier policy

**Status:** ADOPTED  
**Current operating mode:** SOLO MAINTAINER  
**Canonical merge-gate authority:** this document, the live GitHub ruleset, `docs/governance/solo-maintainer-mode.md`, and `docs/governance/multi-agent-serialized-execution.md`  
**Maturity authority:** `docs/CURRENT_STATUS.md` plus verified live GitHub state

The repository currently has one maintainer and no genuinely independent human reviewer.
That is an explicit operating condition, not a defect to conceal and not a reason to stop
all work indefinitely.

```text
solo maintainer review ≠ independent human review
review automation ≠ independent human approval
green CI ≠ proof of semantic correctness
merge authority ≠ runtime authority
separate AI session ≠ independent reviewer
shared GitHub identity ≠ shared live context
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
4. `docs/governance/multi-agent-serialized-execution.md`;
5. `CODEOWNERS` as ownership/navigation metadata;
6. PR-local status notes.

PR-local text may not invent a permanent gate that contradicts this policy. A stale
`BLOCKED_BY_INDEPENDENT_REVIEW` or `BLOCKED_BY_GOVERNANCE_IDENTITY` statement must be
reconciled before merge and must not be used as an active solo-mode status.

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

Use only these active statuses in current PR-local checkpoints:

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

Missing reviewer identity is not a current blocker while the repository remains in
solo-maintainer mode.

---

## 3. Risk classification

A PR is classified by its highest-risk file or semantic effect.

### 3.1 Automatic escalation

A nominal Tier B or Tier C PR that changes a Tier A path or has a Tier A semantic effect
is governed as Tier A: **the entire PR becomes Tier A**.

### 3.2 Tier A — integrity, authority, security, governance, or runtime-capable core

#### Existing protected / high-risk paths

```text
src/mentaury/storage/**
src/mentaury/replay/**
src/mentaury/beliefs/**
src/mentaury/evidence/**
src/mentaury/capabilities/lease/**
src/mentaury/privacy/reconciliation/**
src/mentaury/non_projection/**
src/mentaury/composition/governed_constraints/**
src/mentaury/composition/non_projection_shadow/**
src/mentaury/claims/**
src/mentaury/claim_belief_binding/**
src/mentaury/epistemic_change/**
src/mentaury/relations/**
src/mentaury/discrimination/**
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
docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md
docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md
docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md
docs/research/POST_P0_ROADMAP_V0.1.md
```

#### Paths reserved if/when created

```text
src/mentaury/**/authority/**          # if/when created
src/mentaury/**/lease/**              # if/when created outside active exact paths
src/mentaury/schema/**                # if/when created
src/mentaury/canonical.py             # if/when created
src/mentaury/canonical/**             # if/when created
src/mentaury/integrity/**             # if/when created
src/mentaury/redaction/**             # if/when created
```

The exact `src/mentaury/capabilities/lease/**` path is active only for the
completed bounded P1-001 pure resolver recorded in
`docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`.

The exact `src/mentaury/privacy/reconciliation/**` path is active only for the
bounded pure P1-002 classifier recorded in
`docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md`. It may classify caller-supplied
records but may not persist, scan, delete, redact, quarantine, rebuild, retrieve,
append events, invoke P1-001 internally, mutate relationship/identity/M3 state,
execute tools, select backends or deploy.

The implemented `non_projection`, governed-composition, claim, claim-to-belief binding,
epistemic-change routing, relation and hypothesis-discrimination packages are also Tier A
because semantic changes in those paths can alter attribution, authority ceilings,
claim/belief separation, provenance binding, epistemic owner routing, relation/truth
separation or the boundary between structural discrimination and Evidence Gate verdicts.
Their current implementation remains bounded and grants no runtime authority.

#### Tier A requirements

In solo mode:

- exact current head SHA recorded;
- complete final diff inspected;
- required exact-head CI green;
- branch up to date with `main`;
- all review conversations resolved;
- two-pass maintainer review completed;
- architecture, invariant, fail-closed, security, and authorization boundaries checked;
- multi-agent active-writer and main-drift preflight satisfied when applicable;
- no unresolved material concern hidden behind a green test suite;
- explicit maintainer decision recorded before merge;
- post-merge `main` CI verified.

The two passes must be meaningfully different:

1. **Correctness pass** — design, behavior, compatibility, tests, and scope.
2. **Adversarial pass** — failure modes, integrity, authorization, rollback, security,
   misleading claims, and hidden privilege expansion.

Automated analysis may support either pass, but the repository must not label it as
independent human review.

### 3.3 Tier B — bounded tooling and non-authoritative project documentation

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

### 3.4 Tier C — editorial, navigation, and research capture

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
Multi-agent writer state: SERIALIZED / NOT_APPLICABLE / CONCERN
Main drift reconciled: YES / NOT_APPLICABLE / NO
Decision: ACCEPTED_FOR_MERGE / STOP
```

The reusable checklist is maintained in
`docs/governance/solo-maintainer-review-checklist.md`.

A self-review must not be described as independent, external, second-party, or certified.
Honest attribution is mandatory.

---

## 5. Security and emergency maintenance

A narrowly scoped security or dependency update may be merged after exact scope,
exact-head CI, runtime-impact assessment, maintainer security review and post-merge CI.
A post-hoc review issue must remain completable under current solo mode.

---

## 6. Bots and automation

Cursor, Codex, Copilot, ChatGPT, Claude Code, and other agents may inspect, create branches,
open/update PRs, prepare evidence and merge only when live rules and this policy
are satisfied and the operator authorized autonomous completion.

They may not claim independent human approval, bypass checks, silently broaden
scope, treat green CI as production readiness, or weaken integrity and authority
boundaries merely to merge.

### 6.1 Serialized multi-agent execution

When more than one AI or automation session can write through the operator's GitHub
authority, execution is serialized by bounded milestone according to
`docs/governance/multi-agent-serialized-execution.md`.

```text
MULTI_AGENT_EXECUTION_MODE = SERIALIZED_BY_BOUNDED_MILESTONE
ONE_BOUNDED_MILESTONE = ONE_ACTIVE_WRITER
PARALLEL_READ_AUDIT = ALLOWED
PARALLEL_WRITE_SAME_MILESTONE = FORBIDDEN
AUTHORITY_MILESTONES = STRICTLY_SERIALIZED
MAIN_DRIFT = REVERIFY_BEFORE_CONTINUING
UNKNOWN_OR_CONFLICTING_WRITER_STATE = STOP_AND_RECONCILE
```

The active writer is a coordination role, not a distinct GitHub security principal or an
independent reviewer. A second agent may inspect, test, audit, challenge, or report
concerns, but it must not race a competing write/PR/merge for the same bounded milestone.

Before the first write, the active writer must establish the current `main` SHA, relevant
open PRs/issues, current contract/authorization state, intended scope and branch. Before
merge it must re-resolve `main`, exact PR head, up-to-date state, final diff, required CI,
review threads and authorization boundary.

If `main` changes after the baseline, if competing work appears on the same bounded scope,
or if writer state becomes uncertain, repository mutation stops until live state is read
and reconciled. A clean textual merge does not by itself prove semantic compatibility.

Contract freeze/revision, Owner GO, implementation authorization, runtime-capable core
implementation, runtime activation, governance/security authority changes and deployment
authorization are always strictly serialized. Each such transition must reach merged
`main` plus verified resulting-main CI before the next authority transition begins.

A writer transfer requires the previous writer to stop mutations and the new writer to
reverify live GitHub state before making new commits. Transfer or cross-agent review does
not create independent human assurance.

---

## 7. Transition to public or team operation

Before public or multi-contributor operation:

- add a genuinely independent trusted reviewer or team;
- set required approvals to `1`;
- enable dismissal of stale approvals;
- require approval of the latest reviewable push by someone other than its author;
- enable CODEOWNER review only for a distinct trusted identity/team;
- retain CI, up-to-date, conversation, force-push and deletion gates;
- verify the upgraded ruleset and synchronize GitHub/Notion.

Issue #39 is the future lifecycle trigger, not a current solo-mode blocker.

---

## 8. Explicit non-claims

Current bounded authorizations do not authorize:

```text
identity or Character runtime
M3 writes
Action Gate or external tool execution
Capability Lease registry persistence or service
P1-001 authority outside the pure resolver scope
P1-002 authority outside the pure classifier scope
privacy persistence, scanning, deletion, redaction, quarantine, rebuild or retrieval runtime
backend selection or integration
production deployment
objective truth claims
```

The multi-agent serialization policy also does not grant P1-003 Owner GO, implementation
authority, runtime authority, deployment authority, or independent-review status.

Use precise statuses such as `FROZEN_DOCS`, `AUTHORIZED_BOUNDED`,
`IMPLEMENTED_BOUNDED`, `not implemented`, and `not authorized` according to
verified state.
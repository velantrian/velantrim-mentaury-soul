# Mentaury Soul — Governance risk-tier policy

**Status:** proposed for adoption via dedicated governance PR  
**Authority:** once merged, this document is the canonical merge-gate policy for risk tiers.  
**Companion:** `docs/CURRENT_STATUS.md` remains the maturity / implementation status authority.  
**CODEOWNERS:** path ownership markers aligned with Tier A (review assignment ≠ automatic independent approval).

```text
Adopted docs policy ≠ GitHub branch-protection already configured
Docs policy MUST still be enforced in review practice until
repository rulesets mirror it (tracked in issue #39)
```

---

## 1. Audit reconciliation (2026-08-08)

### 1.1 Old path-scoped policy interpretation

The previously adopted independent-review rule in `docs/CURRENT_STATUS.md`
was **path-scoped**, not universal. It required merge-blocking independent
review only for:

```text
src/mentaury/beliefs/**
src/mentaury/evidence/**
src/mentaury/replay/**
src/mentaury/**/authority/**          # if/when created
src/mentaury/**/lease/**              # if/when created
docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
docs/research/POST_P0_ROADMAP_V0.1.md
```

### 1.2 Classification of merges #45 / #46 / #50 / #51

| Object | Canonical policy violation | Process inconsistency | Review coverage gap |
|---|---|---|---|
| PR #45 | NOT ESTABLISHED | CONFIRMED (PR-local STOP broader than Canon) | n/a for old path rule |
| PR #46 | NOT ESTABLISHED | CONFIRMED (PR-local STOP broader than Canon) | n/a for old path rule |
| PR #50 | NOT ESTABLISHED | — | CONFIRMED (0 formal reviews) |
| PR #51 | NOT ESTABLISHED | — | CONFIRMED (0 formal reviews; integrity-sensitive storage) |

```text
Technical enforcement gap: CONFIRMED repository-wide
Branch protection: disabled at audit time
Bot / automation merge authority: not constrained by repository settings
```

Do **not** rewrite history as “all four PRs violated adopted policy”.
Do **not** claim governance was fully obeyed.
Do **not** treat PR-local STOP text as meaningless.

Post-hoc review obligations:
- PR #40 → issue #42 (deadline 2026-08-14)
- PR #50 → issue #52
- PR #51 → issue #53

---

## 2. Canonical merge-gate authority

Order of authority:

1. repository ruleset / branch protection;
2. `docs/GOVERNANCE.md` risk-tier policy;
3. `CODEOWNERS`;
4. PR-local status comment.

PR-local comments may explain the gate but may **not** silently create,
remove or broaden permanent governance policy.

If PR-local status conflicts with the canonical policy:

- treat the stricter state as temporary STOP;
- resolve the contradiction before merge;
- record the resolution in the PR.

### 2.1 Standard merge-status vocabulary

Use only these statuses in PR-local checkpoints:

```text
READY_FOR_REVIEW
BLOCKED_BY_CI
BLOCKED_BY_CHANGES_REQUESTED
BLOCKED_BY_INDEPENDENT_REVIEW
BLOCKED_BY_STALE_REVIEW
BLOCKED_BY_ADMIN_ENFORCEMENT
ACCEPTED_FOR_MERGE
```

Vague `BLOCKED_BY_GOVERNANCE_IDENTITY` must not be used without specifying:

- required tier;
- protected files;
- current exact head;
- missing reviewer identity;
- required review state.

---

## 3. Risk tiers

A change is classified by the **highest-risk file or semantic effect** in the PR.

### 3.1 Automatic escalation

If a Tier C (or Tier B) PR also modifies any Tier A path — including
`docs/CURRENT_STATUS.md`, `docs/GOVERNANCE.md`, `CODEOWNERS`, workflows,
validators, lockfiles/dependencies, or runtime-capable core code — the
**entire PR becomes Tier A**.

### 3.2 Tier A — independent APPROVED required

#### Existing protected / high-risk paths

```text
src/mentaury/storage/**
src/mentaury/replay/**
src/mentaury/beliefs/**
src/mentaury/evidence/**
src/mentaury/contracts/canonical_json.py
scripts/validate.py
scripts/check_doc_freshness.py
.github/workflows/**
requirements*.lock
pyproject.toml
CODEOWNERS
docs/CURRENT_STATUS.md
docs/GOVERNANCE.md
docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
docs/research/POST_P0_ROADMAP_V0.1.md
```

#### Paths reserved if/when created

```text
src/mentaury/**/authority/**          # if/when created
src/mentaury/**/lease/**              # if/when created
src/mentaury/schema/**                # if/when created
src/mentaury/canonical.py             # if/when created
src/mentaury/canonical/**             # if/when created
src/mentaury/integrity/**             # if/when created (top-level package)
src/mentaury/redaction/**             # if/when created (top-level package)
```

Note: integrity and redaction logic currently live under
`src/mentaury/storage/**` and are already Tier A via that glob.

#### Tier A requirements

- green exact-head CI;
- at least one independent APPROVED;
- reviewer distinct from the authoring operator;
- latest reviewed head equals current PR head;
- stale approvals invalid after any new commit;
- all review conversations resolved;
- no merge by automation before the gate is satisfied;
- emergency security exception only under separately documented carve-out
  with mandatory post-hoc independent review.

Until branch protection/ruleset enforcement exists (issue #39),
all Tier A PRs remain draft or explicitly non-mergeable by process.

### 3.3 Tier B — owner review + green CI

Examples:

```text
docs/ENVIRONMENT_MANIFEST.md
docs/MENTAURY_QUICK_REFERENCE.md
non-authoritative architecture documentation
developer tooling outside validation/security boundaries
```

Requirements:

- green CI;
- at least one formal review or documented owner audit;
- no unresolved blocking comments;
- no runtime or authority semantic changes.

### 3.4 Tier C — editorial / research

Examples:

```text
non-authoritative research notes
navigation-only changes
spelling and formatting
candidate capture without selection
```

Requirements:

- green CI where applicable;
- editorial review may be sufficient;
- no Canon, roadmap, policy, authority, runtime or backend selection change.

---

## 4. Independent reviewer identity

### 4.1 Qualifying independent reviewer

- separate human/operator identity; **or**
- genuinely separately controlled automated reviewer;
- not the author;
- not a same-operator service account;
- not owner self-review;
- formal GitHub `APPROVED` state required for Tier A.

### 4.2 Second AI reviewer

A second AI reviewer may count only if:

- it is operated independently from the authoring agent/operator;
- it performs an actual review of the exact head;
- its GitHub identity can submit `APPROVED`;
- its evidence is auditable;
- it is not merely another tool call controlled by the same operator.

If those conditions are not met:

```text
AI assessment = technical evidence
AI assessment ≠ independent approval
```

Non-qualifying examples:

```text
Cursor / Copilot / Codex COMMENT
owner COMMENTED packet
self-approval
approval of a superseded head
```

---

## 5. Bot / automation merge restrictions

Cursor, Codex, Copilot and other automated agents may:

- create branches;
- push commits;
- open PRs;
- run validation;
- update PR descriptions;
- prepare review packets;
- respond to review comments.

They may **not** merge Tier A PRs unless all GitHub-enforced gates are
visibly satisfied.

Bots must not rely only on text parsing of STOP comments.
The authoritative decision must include:

- changed-file classification;
- exact current head;
- current CI conclusion;
- formal GitHub review state;
- branch protection / ruleset result.

---

## 6. Explicit non-claims

This governance document does **not** authorize:

```text
identity runtime
Character runtime
M3 writes
Action Gate
P1-001 resolver implementation
PostgreSQL / Graphiti / LadybugDB selection or integration
production deployment claims
```

Use “runtime-capable” / “integrity-sensitive” rather than “production”
unless a production deployment is separately confirmed.

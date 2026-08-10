# Solo maintainer mode

## Status

The repository currently operates in **solo maintainer mode**.

There is no genuinely independent human reviewer at this stage. Independent approval is
therefore not required by the active GitHub ruleset (`required approvals = 0`). This is an
explicit operating model, not a claim that independent review occurred.

During this phase:

- pull requests are required for changes to `main`;
- the required CI check must pass;
- pull request branches must be up to date with `main` before merge;
- review conversations must be resolved;
- force pushes and deletion of `main` are blocked;
- the bypass list remains empty;
- the maintainer performs and records the final review and merge decision.

## Operating principle

```text
no independent reviewer available
≠ fabricate an approval
≠ freeze the repository indefinitely
= use honest, evidence-backed solo review
```

Automated assistance may inspect, test, challenge, or prepare changes. It is supporting
technical evidence and must not be described as independent human approval.

## Review depth

Changes are reviewed according to risk, not merely file extension.

For integrity-sensitive, security-sensitive, governance, authority, or runtime-capable
changes, the maintainer performs two passes:

1. **Correctness pass** — scope, design, behavior, compatibility, and tests.
2. **Adversarial pass** — failure modes, security, integrity, rollback, authorization,
   fail-closed behavior, and misleading maturity claims.

The final review is bound to the exact PR head SHA. Any new commit invalidates the earlier
head-specific conclusion and requires rechecking the changed result.

The reusable evidence checklist is in
`docs/governance/solo-maintainer-review-checklist.md`.

## Merge conditions

A PR may be accepted in solo mode only when:

- its final diff is understood;
- its current head SHA is recorded;
- required exact-head CI is green;
- the branch is current with `main`;
- all conversations are resolved;
- applicable correctness and adversarial checks pass;
- no authorization boundary is silently widened;
- the maintainer records `ACCEPTED_FOR_MERGE` or an equivalent explicit decision;
- post-merge `main` CI is verified.

Green CI alone is insufficient when a material architectural or security concern remains.

## Supersession rule

This document and `docs/GOVERNANCE.md` supersede older active-looking statements that
require unavailable independent approval during the current solo phase. Older text may be
retained as historical provenance, but it must not be treated as a current merge blocker.

Issue #39 is retained only as a future transition trigger. It does not block current solo
work.

## Exit criteria

Before the project enters a public or multi-contributor stage:

- add a genuinely independent trusted reviewer or review team;
- set required approving reviews to `1`;
- enable dismissal of stale approvals when new commits are pushed;
- require approval of the latest reviewable push by someone other than its author;
- enable CODEOWNER review only when a distinct trusted reviewer/team owns the paths;
- keep required CI, up-to-date branches, resolved conversations, deletion protection, and
  force-push protection enabled;
- verify the transition against the live GitHub ruleset;
- update repository documentation and synchronize Notion.

Until those conditions exist, the project remains honestly governed as a solo-maintainer
repository.
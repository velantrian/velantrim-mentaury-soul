# Solo maintainer mode

## Status

The repository currently operates in **solo maintainer mode**.

During this phase:

- pull requests are required for changes to `main`;
- the required CI check must pass;
- pull request branches must be up to date with `main` before merge;
- review conversations must be resolved;
- force pushes and deletion of `main` are blocked;
- independent approving reviews are not required (`required approvals = 0`).

This is an explicit temporary governance choice, not a claim of independent review.

## Responsibility

The maintainer remains responsible for reviewing proposed changes, checking CI results, and deciding whether a pull request is safe to merge. Automated assistance may analyze or prepare changes, but it does not constitute independent human approval.

## Exit criteria

Before the project enters a public or multi-contributor stage, governance should be upgraded to require independent review. At minimum:

- set required approving reviews to `1`;
- enable dismissal of stale approvals when new commits are pushed;
- require approval of the most recent reviewable push by someone other than its author;
- keep required CI, up-to-date branches, resolved conversations, deletion protection, and force-push protection enabled;
- add an appropriate independent reviewer or team.

The transition should be verified against the live GitHub ruleset before relying on it.

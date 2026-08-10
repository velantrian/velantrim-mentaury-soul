# Multi-agent serialized execution

## Status

```text
MULTI_AGENT_EXECUTION_MODE = SERIALIZED_BY_BOUNDED_MILESTONE
ONE_BOUNDED_MILESTONE = ONE_ACTIVE_WRITER
PARALLEL_READ_AUDIT = ALLOWED
PARALLEL_WRITE_SAME_MILESTONE = FORBIDDEN
AUTHORITY_MILESTONES = STRICTLY_SERIALIZED
MAIN_DRIFT = REVERIFY_BEFORE_CONTINUING
UNKNOWN_OR_CONFLICTING_WRITER_STATE = STOP_AND_RECONCILE
```

This policy applies while the repository remains in `SOLO_MAINTAINER` mode and more than
one AI or automation session may possess write-capable access through the same operator
identity.

It exists because GitHub attribution to the shared operator account does not reliably
identify which agent session initiated a write, review, or merge. Multiple agents using the
same GitHub principal are therefore separate execution sessions, not independent reviewers
and not separate governance authorities.

```text
shared GitHub identity ≠ shared live context
separate AI agent ≠ independent human reviewer
second AI analysis ≠ second-party approval
merge-capable access ≠ permission to write concurrently
```

---

## 1. Bounded milestone ownership

Every bounded milestone that can write to the repository has exactly one **active writer**
at a time.

The active writer is an operational coordination role. It is not a new GitHub identity,
security principal, reviewer class, or source of independent assurance.

The active writer may:

- create or update the milestone branch;
- change files inside the authorized milestone scope;
- open or update its pull request;
- prepare exact-head evidence;
- perform the recorded solo-maintainer review workflow when authorized by the operator;
- merge only after all live governance gates are satisfied.

Any other agent may concurrently:

- read the repository and PR;
- inspect the complete diff;
- run or inspect tests and CI evidence;
- perform correctness or adversarial analysis;
- report concerns to the operator or active writer.

A non-active agent must not concurrently mutate the same bounded milestone, push a
competing implementation of the same decision, update the same authority state, or merge a
parallel PR for that milestone unless the operator explicitly transfers the active-writer
role first.

---

## 2. Mandatory live-state preflight

Before the first repository write for a bounded milestone, the active writer must resolve
and record at least:

```text
baseline main SHA
open pull requests relevant to the scope
open issues relevant to the scope
current authorization / contract state
intended branch and milestone scope
active writer identity at the session/tool level when known
```

The GitHub account name alone is not sufficient session attribution when multiple agents
share the operator's OAuth/app authority.

Before merge, the active writer must re-resolve:

- current `main` SHA;
- current PR head SHA;
- whether the branch is up to date with `main`;
- complete final changed-file list and diff;
- required exact-head CI;
- review-thread state;
- authorization boundary.

---

## 3. Main-drift rule

If `main` changes after the milestone baseline was established, the previous plan is not
automatically authoritative.

The active writer must:

```text
STOP MUTATION
→ READ NEW MAIN
→ COMPARE / RECONCILE
→ RE-EVALUATE SCOPE AND AUTHORIZATION
→ UPDATE BRANCH SAFELY
→ RE-RUN REQUIRED EVIDENCE
→ CONTINUE ONLY IF THE BOUNDED DECISION STILL HOLDS
```

A merge conflict is only one visible form of drift. A clean textual merge does not prove
that two parallel architectural decisions remain semantically compatible.

An agent must not preserve its earlier design merely because its branch predates a newer
accepted decision on `main`.

---

## 4. Competing-work detection

If the active writer discovers another open branch, pull request, or agent session changing
the same bounded milestone or authority surface, the default action is:

```text
STOP_AND_RECONCILE
```

Do not race the other writer to merge.
Do not duplicate the decision in a second PR.
Do not treat a clean CI result as proof that parallel decisions are compatible.

The operator may explicitly partition truly non-overlapping work, but the partition must
identify separate scopes and neither agent may independently change the other's authority
boundary.

---

## 5. Strictly serialized authority milestones

The following transitions are always strictly serialized in this repository:

```text
contract freeze or contract revision
Owner GO
implementation authorization
runtime-capable implementation of an authorized core slice
runtime activation
governance authority changes
security / integrity authority changes
deployment authorization
```

For these transitions, only one active writer may perform repository mutations at a time,
even when two agents appear to be working on different files.

A completed transition must reach merged `main` plus verified resulting-main CI before the
next authority transition begins.

In particular:

```text
CONTRACT FROZEN ≠ OWNER GO
OWNER GO ≠ IMPLEMENTATION COMPLETE
```

An agent completing an Owner GO milestone must stop after the verified authorization merge.
Implementation begins only as a new bounded milestone after a fresh live-state preflight.

---

## 6. Writer transfer

The operator may transfer a bounded milestone from one agent to another.

A safe transfer requires:

1. the previous active writer stops repository mutations for that milestone;
2. the new writer re-reads current `main`, open PRs, the existing branch/PR, and current
   authorization state;
3. the new writer does not trust a handoff summary over verified live GitHub state;
4. any stale assumptions are reconciled before new commits;
5. exact-head review and CI bind only to the final head produced after transfer.

Transfer does not create independent review. If the second agent reviews work produced by
the first, that review remains automated supporting analysis unless a genuinely independent
human reviewer exists.

---

## 7. Failure and uncertainty

If agent coordination state is unknown, contradictory, or cannot be verified, fail closed
for writes:

```text
READ / AUDIT = ALLOWED
NEW WRITE / MERGE = STOPPED_PENDING_RECONCILIATION
```

Uncertainty about which agent performed an earlier action is not itself a reason to revert
a verified merged change. It is a reason to re-establish live state and a single active
writer before the next mutation.

---

## 8. Current P1-003 boundary

Adoption of this policy does not grant any P1-003 authority.

```text
P1_003_CONTRACT = FROZEN_DOCS
P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
P1_003_OWNER_GO = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

The next possible P1-003 state transition remains a separate explicit Owner GO decision
after this governance hardening is merged and resulting-main CI is verified.

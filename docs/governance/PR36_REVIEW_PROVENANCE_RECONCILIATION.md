# PR #36 Review Provenance Reconciliation

**Status:** GOVERNANCE_RECONCILIATION · CURRENT  
**Scope:** historical review labels associated with PR #36 only  
**Governing authority:** `docs/GOVERNANCE.md` + `docs/governance/solo-maintainer-mode.md`  
**Runtime authority:** NONE  
**Truth authority:** NONE  
**Capability authority:** NONE  

This note reconciles legacy review terminology left by PR #36 with the repository's
current adopted solo-maintainer governance model.

```text
HISTORICAL_REVIEW_LABEL_RECONCILED
INDEPENDENT_HUMAN_REVIEW_CLAIMED: NO
PR36_TECHNICAL_FINDINGS_RETAINED: YES
PR36_MERGE_VALIDITY_REVOKED: NO
RUNTIME_AUTHORITY_CREATED: NO
```

---

## 1. Verified provenance

PR #36 (`docs: define contextual cognition research contracts`) contains review
submissions historically titled or described as:

```text
Independent architecture review — changes required
Independent architecture review — round 2 PASS
independent review round 2
```

The live GitHub review records for that PR are attributed to the repository owner
account `velantrian`, the same maintainer identity that authored and merged the work.
Under the governance model adopted later, that attribution does **not** qualify as a
genuinely independent human review.

Therefore, wherever the active research documentation still preserves the historical
phrase `independent review`, its assurance meaning is reconciled as follows:

```text
historical label: independent review / independent architecture review
current assurance interpretation: historical architecture review / same-maintainer review
independent human assurance: NOT CLAIMED
```

This is an assurance-attribution correction, not a finding reversal.

---

## 2. Documents carrying legacy wording

Known active or historical documentation surfaces that preserve PR #36 terminology
include:

- `docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`;
- `docs/research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`;
- `docs/research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`;
- `docs/research/MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md`.

Those documents remain useful provenance. Their legacy `independent review` wording
must not be read as contradicting current `docs/GOVERNANCE.md`.

```text
legacy wording ≠ current independent-human assurance
historical review result ≠ independent human approval
same operator self-review ≠ independent review
AI-assisted review ≠ independent human review
```

Future edits SHOULD use `historical architecture review`, `solo-maintainer review`, or
another attribution that matches the verified reviewer identity.

---

## 3. Technical findings retained

This reconciliation does not erase or weaken the technical findings recorded around
PR #36. In particular, the historical review process still records that the branch was
changed to address issues including:

- tool planning / authorization / execution ordering;
- duplicate normative schemas and scenario IDs;
- stable Genesis section numbering;
- separation of research side-tracks from execution milestones;
- preservation of runtime, truth, capability, identity and M3 boundaries.

The technical outcome may remain accepted while the assurance label is corrected.

```text
review finding retained
+
reviewer independence reclassified honestly
```

---

## 4. Current authorization boundary

Nothing in this note authorizes implementation or runtime activation.

```text
P1-001 = IMPLEMENTED_BOUNDED
P1-002 = IMPLEMENTED_BOUNDED
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
SOLO_MAINTAINER
INDEPENDENT_HUMAN_REVIEW = NOT CLAIMED
merge authority ≠ runtime authority
```

Specifically not authorized by this reconciliation:

- P1-003 selection or implementation;
- Character runtime;
- identity or relationship runtime;
- direct or indirect M3 writes;
- Action Gate or external tool execution;
- retrieval or privacy remediation execution;
- backend integration or deployment.

---

## 5. Operating rule

When a historical document and current governance use different review terminology,
retain the historical text as provenance but evaluate assurance using the current
verified reviewer identity and `docs/GOVERNANCE.md`.

```text
historical wording may be preserved
verified identity controls assurance classification
current governance controls merge semantics
runtime authority still requires separate explicit authorization
```

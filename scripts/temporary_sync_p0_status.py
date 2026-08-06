from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


readme = Path("README.md")
replace_once(
    readme,
    """P0-001…P0-013_IMPLEMENTED_IN_MAIN
P0-013_R1_PR_AND_MAIN_VALIDATION_PASS
P0-014…P0-015_NOT_IMPLEMENTED
""",
    """P0-001…P0-015_IMPLEMENTED_IN_MAIN
P0-014_BELIEF_LIFECYCLE_PR_AND_MAIN_VALIDATION_PASS
P0-015_EVIDENCE_GATE_PR_AND_MAIN_VALIDATION_PASS
""",
)
replace_once(
    readme,
    "├── 🛡️ P0 Event Substrate — implementation in progress",
    "├── 🛡️ P0 Event + Belief Foundation — implemented",
)
replace_once(readme, "│   ├── P0-014 belief lifecycle\n", "│   ├── P0-014 belief lifecycle ✅\n")
replace_once(readme, "│   └── P0-015 Evidence Gate\n", "│   └── P0-015 Evidence Gate ✅\n")
replace_once(
    readme,
    "├── 🧠 Memory & Belief — architecture documented, runtime absent",
    "├── 🧠 Memory & Belief — minimal M2 contracts implemented; runtime absent",
)
replace_once(
    readme,
    """P0-013 → neutral R1 deterministic full-replay ↔ snapshot-tail equivalence
```""",
    """P0-013 → neutral R1 deterministic full-replay ↔ snapshot-tail equivalence
P0-014 → evidence-referenced minimal belief lifecycle + deterministic reducer
P0-015 → approved-policy deterministic Evidence Gate + replay-verified receipts
```""",
)
replace_once(
    readme,
    """P0-001…P0-013 ✅
→ P0-014 Minimal Belief Lifecycle
→ P0-015 Evidence Gate
""",
    """P0-001…P0-015 ✅ merged and validated in main
→ next work requires a separately reviewed post-P0 roadmap
→ domain runtime remains NOT AUTHORIZED
""",
)
replace_once(
    readme,
    "- [🔁 P0-013 R1 Deterministic Replay](docs/P0_013_R1_DETERMINISTIC_REPLAY.md)\n",
    """- [🔁 P0-013 R1 Deterministic Replay](docs/P0_013_R1_DETERMINISTIC_REPLAY.md)
- [🧠 P0-014 Minimal Belief Lifecycle](docs/P0_014_MINIMAL_BELIEF_LIFECYCLE.md)
- [⚖️ P0-015 Deterministic Evidence Gate](docs/P0_015_EVIDENCE_GATE.md)
""",
)
replace_once(readme, "❌ deterministic R1 replay", "❌ R1 proof of semantic or epistemic truth")
replace_once(
    readme,
    "> **Mentaury уже имеет подробную архитектуру цифровой индивидуальности и работающий инфраструктурный P0-фундамент до P0-013. Identity, beliefs, relationships, Character и Exo-Cortex пока остаются документированными, но не реализованными runtime-областями.** 🧬🔐⚙️",
    "> **Mentaury имеет подробную архитектуру цифровой индивидуальности и реализованную, replay-проверяемую P0-линию до P0-015, включая минимальный belief lifecycle и Evidence Gate. Это инженерный фундамент: полноценные Memory/Identity/Relationship runtime, authority resolution, Character и Exo-Cortex остаются не авторизованными runtime-областями.** 🧬🔐⚙️",
)

status = Path("docs/CURRENT_STATUS.md")
replace_once(
    status,
    """Verified implementation head:  cd069e97200d6381806642a438ec2bc64b71571e

CANON_V0.1_FROZEN
P0-001…P0-013_IMPLEMENTED_IN_MAIN
P0-013_R1_PR_AND_MAIN_VALIDATION_PASS
P0-014…P0-015_NOT_IMPLEMENTED
""",
    """Verified implementation head:  d6a07336b5167c5fc1cc8e2f05413a7284bea0ec

CANON_V0.1_FROZEN
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P0-014_BELIEF_LIFECYCLE_PR_AND_MAIN_VALIDATION_PASS
P0-015_EVIDENCE_GATE_PR_AND_MAIN_VALIDATION_PASS
""",
)
replace_once(
    status,
    "| P0-013 R1 Deterministic Replay | ✅ Implemented | deterministic replay ≠ epistemic truth |\n",
    """| P0-013 R1 Deterministic Replay | ✅ Implemented | deterministic replay ≠ epistemic truth |
| P0-014 Minimal Belief Lifecycle | ✅ Implemented | belief status ≠ truth or runtime authority |
| P0-015 Deterministic Evidence Gate | ✅ Implemented | gate receipt ≠ externally verified fact |
""",
)
marker = "\n---\n\n# 🔴 Не реализовано\n"
if status.read_text(encoding="utf-8").count(marker) != 1:
    raise RuntimeError("CURRENT_STATUS: completion insertion marker not found exactly once")
completion = """
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
"""
status.write_text(status.read_text(encoding="utf-8").replace(marker, completion, 1), encoding="utf-8")
replace_once(
    status,
    """```text
P0-014 Minimal Belief Lifecycle        → NOT IMPLEMENTED
P0-015 Evidence Gate Report            → NOT IMPLEMENTED
```
""",
    """```text
P0-001…P0-015 → IMPLEMENTED, MERGED AND RETAINED-CI VALIDATED
```

This closes the current P0 implementation plan. It does not authorize a
long-running agent, domain service, M3 mutation path, tool execution or external
action boundary.
""",
)
replace_once(
    status,
    """P0-001…P0-013 ✅ merged in main
→ P0-014 minimal belief lifecycle
→ P0-015 Evidence Gate report
""",
    """P0-001…P0-015 ✅ merged and validated in main
→ define a separate post-P0 roadmap before additional implementation
→ preserve DOMAIN_RUNTIME_NOT_AUTHORIZED
""",
)
replace_once(
    status,
    """P0-014 MINIMAL BELIEF LIFECYCLE
Status: NOT IMPLEMENTED
Precondition: define evidence-referenced belief commands/events, deterministic lifecycle transitions and R1-compatible projection state without granting truth or identity authority
""",
    """POST-P0 ROADMAP REVIEW
Status: NOT YET AUTHORIZED
Precondition: define the next bounded milestone, threat model, authority boundary, resource budgets and rollback/replay criteria before adding runtime wiring
""",
)

p014 = Path("docs/P0_014_MINIMAL_BELIEF_LIFECYCLE.md")
replace_once(
    p014,
    """Status: IMPLEMENTATION PR
Base: main@024deeec456549584273c79ccfc5e1442d480add
""",
    """Status: MERGED IN MAIN · PR AND MAIN CI PASS
Implementation base: main@024deeec456549584273c79ccfc5e1442d480add
Merge SHA: 3ff90816b8d095987a8adcdc2cb633c128877212
""",
)
replace_once(
    p014,
    """## 🧪 Required validation

```text
retained Mentaury CI on exact PR head
CPython 3.13.x
locked install + pip check
structural validator
complete pytest
compileall
exact diff audit
unresolved review threads = 0
```

The test matrix must cover accepted lifecycle transitions, duplicate and unknown
reference rejection, contradiction state, immutable revision history, terminal
supersession, strict event/audit schemas and P0-013 replay compatibility.

## ➡️ Next controlled milestone

After P0-014 is merged, passes retained CI on `main`, and documentation/Notion
are synchronized:

```text
P0-015 → Evidence Gate
```

P0-015 may restrict `supported` and revision decisions based on governed evidence
policy, but must not rewrite P0-014 history or grant direct truth/identity
authority.
""",
    """## ✅ Validation evidence

```text
PR:                  #29
Final tested head:   fe3ae74d4ef92fc06ab1bee4def88066ded402a5
Merge SHA:           3ff90816b8d095987a8adcdc2cb633c128877212
PR workflow run:     31090898077
Main push run:       31091006506
Python:              CPython 3.13.14
Full pytest:         208 passed on PR and main
Compileall:          PASS
Changed files:       7 intended files
Review threads:      0
Review:              4873291547
```

P0-015 was subsequently implemented as a separate reviewed milestone. P0-014
history and reducer-v1 boundaries remain unchanged; the gated reducer is a new
versioned profile rather than a rewrite of prior events.
""",
)

p015 = Path("docs/P0_015_EVIDENCE_GATE.md")
replace_once(
    p015,
    """Status: FINAL VALIDATED PR CANDIDATE
Base: main@3ff90816b8d095987a8adcdc2cb633c128877212
Validated implementation head: 246b7ad9e64f8c70777baf0f12202899747eb5be
""",
    """Status: MERGED IN MAIN · PR AND MAIN CI PASS
Base: main@3ff90816b8d095987a8adcdc2cb633c128877212
Final tested head: 71acd7410c5080e4ac3245b53534b512b871bae5
Merge SHA: d6a07336b5167c5fc1cc8e2f05413a7284bea0ec
""",
)
replace_once(
    p015,
    """Audit hardening run: 31093091082
Validated head:      246b7ad9e64f8c70777baf0f12202899747eb5be
Python:              CPython 3.13.14
Structural validator: PASS
Full pytest:         232 passed
Compileall:          PASS
Final target diff:   9 files
Temporary files:     absent
""",
    """Audit hardening run: 31093091082
PR workflow run:     31093258104
Main push run:       31093382362
Final tested head:   71acd7410c5080e4ac3245b53534b512b871bae5
Merge SHA:           d6a07336b5167c5fc1cc8e2f05413a7284bea0ec
Python:              CPython 3.13.14
Structural validator: PASS
Full pytest:         232 passed on PR and main
Compileall:          PASS
Final target diff:   9 files
Temporary files:     absent
Review threads:      0
Review:              4873644214
""",
)
replace_once(
    p015,
    """The retained read-only `Mentaury CI` must still pass the final owner-authored PR
head before merge. The validation checkpoint records the implementation proof;
it is not a substitute for the retained exact-head gate.
""",
    """The retained read-only `Mentaury CI` passed both the final owner-authored PR
head and the resulting merge SHA. This validates the repository contract; it
does not authenticate external evidence or authorize runtime deployment.
""",
)

print("P0-014/P0-015 authoritative status sync applied")

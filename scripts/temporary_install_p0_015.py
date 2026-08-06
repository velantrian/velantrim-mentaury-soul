from __future__ import annotations

import base64
import io
import zipfile
from pathlib import Path

PARTS_DIR = Path("scripts/p015_payload")
EXPECTED = {
    "src/mentaury/evidence/__init__.py",
    "src/mentaury/evidence/contracts.py",
    "src/mentaury/evidence/gate.py",
    "src/mentaury/evidence/schemas.py",
    "src/mentaury/beliefs/__init__.py",
    "src/mentaury/beliefs/evidence_gate.py",
    "src/mentaury/beliefs/gated_reducer.py",
    "tests/test_evidence_gate.py",
    "docs/P0_015_EVIDENCE_GATE.md",
}

parts = sorted(PARTS_DIR.glob("part-*.txt"))
expected_names = [f"part-{index:02d}.txt" for index in range(10)]
if [part.name for part in parts] != expected_names:
    raise RuntimeError(
        f"expected payload parts {expected_names!r}, got {[part.name for part in parts]!r}"
    )

encoded = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
raw = base64.b64decode(encoded, validate=True)
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    names = set(archive.namelist())
    if names != EXPECTED:
        raise RuntimeError(f"unexpected archive members: {sorted(names ^ EXPECTED)!r}")
    bad_member = archive.testzip()
    if bad_member is not None:
        raise RuntimeError(f"corrupt archive member: {bad_member}")
    for name in sorted(names):
        target = Path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(name))

# Bind the R1 integration test to the accepted P0-013 snapshot contract.
test_path = Path("tests/test_evidence_gate.py")
test_text = test_path.read_text(encoding="utf-8")
replacements = (
    (
        "from mentaury.replay import R1ReplayVerifier, ReplayStateBudget",
        "from mentaury.replay import (\n"
        "    R1ReplayVerifier,\n"
        "    ReplayStateBudget,\n"
        "    make_replay_snapshot,\n"
        ")",
    ),
    (
        '    assert create.accepted\n'
        '    state = _apply(base_reducer, state, create.domain_events[0], 1, "EVT-R1-CREATE")\n',
        '    assert create.accepted\n'
        '    state = _apply(base_reducer, state, create.domain_events[0], 1, "EVT-R1-CREATE")\n'
        '    snapshot_state = state\n',
    ),
    (
        '        for version, event_id, pending in (\n'
        '            (1, "EVT-R1-CREATE", create.domain_events[0]),\n'
        '            (2, "EVT-R1-ATTACH-1", attach_one.domain_events[0]),\n'
        '            (3, "EVT-R1-ATTACH-2", attach_two.domain_events[0]),\n'
        '            (4, "EVT-R1-GATED", gated.domain_events[0]),\n'
        '        ):\n'
        '            store.append_one(\n'
        '                _event(pending, version, event_id),\n'
        '                pending.payload,\n'
        '                registry=registry,\n'
        '            )\n'
        '        report = R1ReplayVerifier(\n',
        '        committed_create = None\n'
        '        for version, event_id, pending in (\n'
        '            (1, "EVT-R1-CREATE", create.domain_events[0]),\n'
        '            (2, "EVT-R1-ATTACH-1", attach_one.domain_events[0]),\n'
        '            (3, "EVT-R1-ATTACH-2", attach_two.domain_events[0]),\n'
        '            (4, "EVT-R1-GATED", gated.domain_events[0]),\n'
        '        ):\n'
        '            committed = store.append_one(\n'
        '                _event(pending, version, event_id),\n'
        '                pending.payload,\n'
        '                registry=registry,\n'
        '            )\n'
        '            if version == 1:\n'
        '                committed_create = committed\n'
        '        assert committed_create is not None\n'
        '        snapshot = make_replay_snapshot(\n'
        '            reducer_id=gated_reducer.reducer_id,\n'
        '            reducer_version=gated_reducer.reducer_version,\n'
        '            stream_id=STREAM_ID,\n'
        '            through_stream_version=1,\n'
        '            through_event_hash=committed_create.event_hash,\n'
        '            state=snapshot_state,\n'
        '        )\n'
        '        report = R1ReplayVerifier(\n',
    ),
    (
        ").verify_stream(STREAM_ID)\n\n        assert report.ok\n",
        ").verify_stream(STREAM_ID, snapshot)\n\n        assert report.ok\n",
    ),
)
for old, new in replacements:
    if test_text.count(old) != 1:
        raise RuntimeError(f"expected one R1 test marker, found {test_text.count(old)}")
    test_text = test_text.replace(old, new, 1)
test_path.write_text(test_text, encoding="utf-8")

print(f"installed {len(EXPECTED)} P0-015 target files from {len(parts)} verified chunks")

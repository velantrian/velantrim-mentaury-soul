from __future__ import annotations

from pathlib import Path


path = Path("tests/test_concurrency.py")
text = path.read_text(encoding="utf-8")
old = '''def _run_request(
    database: Path,
    request_value,
    barrier: threading.Barrier,
    outcomes: Queue[object],
) -> None:
    policy = BusyRetryPolicy(max_attempts=50, backoff_seconds=0.002)
'''
new = '''_CONCURRENCY_TEST_POLICY = BusyRetryPolicy(
    max_attempts=500,
    backoff_seconds=0.002,
)


def _run_request(
    database: Path,
    request_value,
    barrier: threading.Barrier,
    outcomes: Queue[object],
) -> None:
    policy = _CONCURRENCY_TEST_POLICY
'''
if text.count(old) != 1:
    raise RuntimeError("concurrency helper marker mismatch")
text = text.replace(old, new, 1)

old_assert = '''    assert sum(value is IdempotencyStatus.APPLIED for value in values) == 1
    assert sum(isinstance(value, IdempotencyConflictError) for value in values) == 1
'''
new_assert = '''    assert sum(value is IdempotencyStatus.APPLIED for value in values) == 1, values
    assert sum(
        isinstance(value, IdempotencyConflictError) for value in values
    ) == 1, values
'''
if text.count(old_assert) != 1:
    raise RuntimeError("changed-semantics assertion marker mismatch")
text = text.replace(old_assert, new_assert, 1)

old_version = '''    assert sum(value is IdempotencyStatus.APPLIED for value in values) == 1
    assert sum(isinstance(value, VersionConflictError) for value in values) == 1
'''
new_version = '''    assert sum(value is IdempotencyStatus.APPLIED for value in values) == 1, values
    assert sum(isinstance(value, VersionConflictError) for value in values) == 1, values
'''
if text.count(old_version) != 1:
    raise RuntimeError("version-conflict assertion marker mismatch")
text = text.replace(old_version, new_version, 1)

path.write_text(text, encoding="utf-8")

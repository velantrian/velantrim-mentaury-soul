from __future__ import annotations

import sys
import tempfile
import threading
from collections import Counter
from pathlib import Path
from queue import Queue

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests"))

from mentaury.storage import (  # noqa: E402
    BusyRetryPolicy,
    IdempotencyConflictError,
    IdempotencyStatus,
    SQLiteEventPayloadStore,
    SQLiteIdempotentBatchAppender,
    StoreBusyError,
)
from test_idempotency import command, pending_batch, registry, request  # noqa: E402


def run_request(
    database: Path,
    request_value: object,
    barrier: threading.Barrier,
    outcomes: Queue[object],
) -> None:
    policy = BusyRetryPolicy(max_attempts=50, backoff_seconds=0.002)
    try:
        with SQLiteEventPayloadStore.connect(database, busy_policy=policy) as store:
            barrier.wait()
            result = SQLiteIdempotentBatchAppender(
                store,
                registry(),
                policy,
            ).append(request_value)
            outcomes.put(result.status)
    except BaseException as exc:
        outcomes.put(exc)


def classify(value: object) -> str:
    if value is IdempotencyStatus.APPLIED:
        return "APPLIED"
    if isinstance(value, IdempotencyConflictError):
        return "IDEMPOTENCY_CONFLICT"
    if isinstance(value, StoreBusyError):
        return f"STORE_BUSY:{value.attempts}"
    return f"{type(value).__name__}:{value}"


def main() -> None:
    counts: Counter[tuple[str, str]] = Counter()
    unexpected: list[tuple[int, tuple[str, str]]] = []
    for iteration in range(100):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "conflict.sqlite3"
            with SQLiteEventPayloadStore.connect(database) as setup:
                setup.initialize_schema()

            first = request(generation="A")
            changed = request(
                command(payload_value="beta"),
                pending_batch(first_payload="beta"),
                generation="B",
            )
            barrier = threading.Barrier(2)
            outcomes: Queue[object] = Queue()
            threads = [
                threading.Thread(
                    target=run_request,
                    args=(database, first, barrier, outcomes),
                ),
                threading.Thread(
                    target=run_request,
                    args=(database, changed, barrier, outcomes),
                ),
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=5)
                if thread.is_alive():
                    raise RuntimeError("diagnostic thread did not terminate")

            result = tuple(sorted(classify(outcomes.get_nowait()) for _ in range(2)))
            counts[result] += 1
            if result != ("APPLIED", "IDEMPOTENCY_CONFLICT"):
                unexpected.append((iteration, result))

    print("OUTCOME_COUNTS")
    for outcome, count in sorted(counts.items()):
        print(count, outcome)
    print("UNEXPECTED", unexpected[:20])


if __name__ == "__main__":
    main()

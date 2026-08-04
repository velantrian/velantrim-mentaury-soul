# 🔗 P0-009 — Full R0 + Stream Metadata Verification

```text
Status:             P0-009
Storage schema:     v3
Integrity profile:  R0 diagnostic verification
Failure mode:       first actionable failure
Payload redaction:  NOT IMPLEMENTED
Replay:             NOT IMPLEMENTED
Domain truth:       NOT CLAIMED
```

## Purpose

P0-009 independently verifies that persisted event history, external payload
material and mutable stream metadata remain mutually consistent.

```text
payload bytes → recompute payload_digest
event envelope → recompute event_hash
ordered stream → verify previous_hash + versions + batches
stream_meta → verify tail version + tail hash + event count
```

Schema v3 adds `stream_meta(stream_id, current_version, last_event_hash,
event_count)`. Every write updates it in the same transaction; R0 independently
recomputes the ledger tail and compares it with metadata.

`compute_payload_digest`, `compute_event_hash` and `seal_event` provide the
canonical hash profile. `event_hash` itself is excluded from its hash input.

Stable first-failure codes cover stream gaps, incomplete or out-of-order batches,
schema defects, missing or undecodable payloads, payload digest mismatch,
previous-hash mismatch, event-hash mismatch and all stream-meta tail mismatches.

Adversarial tests bypass normal guards to mutate payload bytes, event hashes,
previous hashes, stream versions, batch indexes and stream metadata.

```text
structural validator → PASS
pytest → 88 passed
compileall → PASS
```

```text
R0 consistency ≠ epistemic truth
Hash continuity ≠ authorization
SQLite metadata ≠ tamper-proof hardware
Valid schema ≠ correct belief
R0 PASS ≠ R1 replay equivalence
```

## Next milestone

```text
P0-010 ATOMIC SAME-STREAM REDACTION
```

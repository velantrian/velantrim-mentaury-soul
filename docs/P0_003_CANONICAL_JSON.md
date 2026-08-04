# 🔤 P0-003 — MENTAURY_CANONICAL_JSON_V1

```text
Status:             P0-003
Profile:            MENTAURY_CANONICAL_JSON_V1
Scope:              deterministic serialization only
Runtime deps:       NONE
Hash computation:   NOT IMPLEMENTED
Persistence:        NOT IMPLEMENTED
Domain authority:   NONE
```

## Purpose

P0-003 defines one deterministic byte representation for portable JSON-like
values and the typed P0-002 envelopes. It is intentionally narrower than a
complete JSON canonicalization standard and does not claim RFC 8785 compliance.

```text
Same admitted value tree
→ same canonical JSON text
→ same UTF-8 bytes
```

## Profile rules

```text
Encoding             = UTF-8
Object key order     = Unicode scalar/code-point order
Whitespace           = none outside strings
Unicode normalization= none; exact scalar sequence is preserved
Lone surrogates      = forbidden
Object keys          = strings only
Float                 = forbidden
NaN / Infinity       = forbidden
Integer range         = -(2^53-1) … +(2^53-1)
Decimal object        = forbidden implicitly
Decimal string        = explicit schema-controlled helper
Cycles                = forbidden
Timestamp output      = RFC 3339 UTC using Z
Timestamp precision   = seconds or exactly 3 fractional digits
Sub-millisecond input = rejected, never rounded
```

Visually equivalent Unicode strings may produce different bytes when their code
point sequences differ. The profile does not silently normalize text.

## Decimal rule

`Decimal` values never enter JSON as implicit JSON numbers. The
`canonical_decimal_string()` helper produces a finite fixed-point string:

```text
1.2300  → "1.23"
-0.000  → "0"
1E+3    → "1000"
.500    → "0.5"
```

The receiving payload schema must explicitly declare that field as a decimal
string. A normal JSON string is not automatically interpreted as a decimal.

## Timestamp rule

`canonical_timestamp()` accepts strict RFC 3339 strings or timezone-aware
`datetime` values, converts them to UTC, and emits:

```text
2026-08-04T22:00:00Z
2026-08-04T22:00:00.120Z
```

Offsets are normalized to `Z`. `-00:00` is rejected because it represents an
ambiguous/unknown offset. Precision finer than milliseconds is rejected.

## Envelope projections

P0-003 adds deterministic projections for:

```text
CommandEnvelope
PendingEvent
ordered PendingEvent batch
EventEnvelope
EventEnvelope hash input
```

The event hash-input projection obeys:

```text
previous_hash → INCLUDED
event_hash    → EXCLUDED
```

This defines bytes that a later hashing milestone may use. P0-003 itself does
not calculate, verify, store, or trust any hash.

## Conformance vectors

Language-neutral vectors are stored at:

```text
tests/fixtures/canonical_json_v1_vectors.json
```

They include canonical text, UTF-8 hex, timestamp normalization, and decimal
string normalization. Invalid-value rules are covered by executable tests.

## Explicit non-claims

```text
Canonical bytes ≠ valid schema
Canonical bytes ≠ correct authority
Canonical bytes ≠ persisted immutability
Canonical bytes ≠ cryptographic integrity
Canonical bytes ≠ epistemic truth
```

P0-004 owns immutable event/payload storage. P0-005 owns structural schema
validation. Later milestones own hashes, batch atomicity, idempotency,
concurrency, R0, redaction, and replay.

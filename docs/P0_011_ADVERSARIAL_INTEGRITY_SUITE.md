# 🧨 P0-011 — Adversarial Integrity Suite

```text
Status: DRAFT IMPLEMENTATION
Base: main@d05319cdcae0eb6421c6ad60649fb8ed57feba08
Scope: P0-011 only
P0-012 permanent GitHub Actions: NOT INCLUDED
R1 replay / belief lifecycle: NOT INCLUDED
Domain runtime: NOT AUTHORIZED
```

## 🎯 Goal

P0-011 converts the existing R0, redaction and idempotency guarantees into an
explicit attacker-oriented gate. The suite must prove that corruption is
detected through a stable, actionable failure code rather than merely causing
an incidental SQLite or JSON exception.

The gate attacks persisted material after intentionally removing the local
immutability trigger that would normally prevent the mutation. Removing a test
guard is not a production capability; it models storage corruption, privileged
operator error or an offline database rewrite.

## 🛡️ Executable threat matrix

| Case | Adversarial mutation | Required result |
|---|---|---|
| `ADV-R0-001` | delete a middle immutable event row | `STREAM_VERSION_GAP` |
| `ADV-R0-002` | delete the ledger tail while leaving `stream_meta` | `STREAM_META_VERSION_MISMATCH` |
| `ADV-R0-003` | replace payload material with invalid UTF-8 | `PAYLOAD_DECODE_ERROR` |
| `ADV-R0-004` | replace object payload with a top-level array | `SCHEMA_INVALID` |
| `ADV-R0-005` | store JSON with duplicate object keys | `PAYLOAD_NOT_CANONICAL` |
| `ADV-R0-006` | forge a self-consistent event hash over a wrong predecessor | `PREVIOUS_HASH_MISMATCH` |
| `ADV-RED-001` | restore payload material after governed redaction | `REDACTED_PAYLOAD_STILL_PRESENT` |
| `ADV-RED-002` | corrupt linked audit payload UTF-8 | `REDACTION_AUDIT_PAYLOAD_DECODE_ERROR` |
| `ADV-RED-003` | rewrite linked audit payload noncanonically | `REDACTION_AUDIT_PAYLOAD_NOT_CANONICAL` |
| `ADV-RED-004` | alter linked audit payload digest | `REDACTION_AUDIT_PAYLOAD_DIGEST_MISMATCH` |
| `ADV-RED-005` | link a redaction to an audit event that precedes its target | `REDACTION_AUDIT_ORDER_MISMATCH` |
| `ADV-IDEM-001` | corrupt stored `event_ids_json` | controlled receipt-integrity error |
| `ADV-IDEM-002` | reference a nonexistent event from a replay receipt | controlled receipt-integrity error |
| `ADV-IDEM-003` | reverse receipt event order | controlled receipt-integrity error |
| `ADV-IDEM-004` | forge receipt version span | controlled receipt-integrity error |

## 🔗 Stored idempotency receipt hardening

A matching semantic fingerprint is necessary but not sufficient for
`ALREADY_APPLIED`. Before returning a stored receipt, the implementation now
verifies:

```text
event_ids_json
├── valid UTF-8 JSON
├── canonical encoding
├── non-empty unique string IDs
└── count equals [first_stream_version..last_stream_version]

receipt ↔ fingerprinted request
├── stream matches command target
├── first version follows expected version
└── event count matches pending batch

each referenced event
├── exists
├── batch ID, index and size match
├── stream and version order match
├── type, schema and state-affecting flag match
├── payload digest matches canonical proposed payload
└── initiator and authority match the command
```

A corrupted receipt raises `IdempotencyReceiptIntegrityError`. No replacement
events, payloads, metadata or idempotency rows are written.

## ⚖️ Failure-order contract

The suite asserts the first security-relevant failure. Examples:

- a recomputed `event_hash` cannot conceal a wrong `previous_hash`;
- audit payload decoding cannot occur successfully when UTF-8 is invalid;
- redaction linkage is checked before the deleted target is accepted;
- a matching idempotency fingerprint cannot authorize a forged replay receipt.

Failure ordering is diagnostic policy, not epistemic truth.

## 🚧 Preserved boundaries

```text
Adversarial R0 PASS ≠ cryptographic authenticity against a total database rewrite
Trigger removal in tests ≠ production mutation API
Idempotency receipt verification ≠ authority validation
P0-011 ≠ permanent CI
P0-011 ≠ R1 deterministic replay
P0-011 ≠ domain runtime authorization
```

An attacker able to rewrite the entire ledger, all hashes and every external
trust anchor remains outside the guarantee of an unkeyed local hash chain.
External anchoring, signatures and independent replicas require separate
architecture.

## 🧪 Required validation

```text
CPython 3.13.x
python scripts/validate.py
full pytest
python -m compileall -q src tests scripts
independent final-head review
temporary validation workflow absent from final diff
```

## ➡️ Next controlled milestone

After P0-011 is merged and post-merge status is synchronized:

```text
P0-012 → permanent GitHub Actions CI
```

P0-012 must convert the validated commands into a retained workflow rather than
reusing the temporary P0-011 patch workflow.

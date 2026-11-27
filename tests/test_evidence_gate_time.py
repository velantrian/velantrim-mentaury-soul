"""Stage 05 (ARCH-001): Evidence Gate time consistency at the write boundary.

Contract (docs/P0_015_EVIDENCE_GATE.md): canonical CommandEnvelope.issued_at ==
payload/receipt ``evaluated_at`` == immutable EventEnvelope.occurred_at. Moments
are compared as canonical UTC instants, never as raw text. Consistency of these
timestamps does not prove the issuer's clock or the evidence is honest.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

import test_evidence_gate as eg
from mentaury.beliefs import (
    ATTACH_EVIDENCE,
    CREATE_BELIEF,
    BeliefLifecycle,
    BeliefReducer,
    EvidenceGatedBeliefLifecycle,
    EvidenceGatedBeliefReducer,
    EvidenceSide,
    ClaimType,
    belief_schema_definitions,
)
from mentaury.contracts import (
    CommandEnvelope,
    EventEnvelope,
    OperationAdmissionBudget,
    OperationAdmissionState,
    PayloadAdmissionBudget,
    PendingEvent,
)
from mentaury.contracts.primitives import freeze_payload
from mentaury.evidence import evidence_gate_schema_definitions
from mentaury.evidence.temporal import EvidenceGateTemporalError
from mentaury.validation import SchemaValidationError
import mentaury.storage.sealing as sealing_module
import test_idempotency as idem
from mentaury.replay import R1ReplayVerifier, ReplayStateBudget, make_replay_snapshot
from mentaury.storage import (
    BatchEntry,
    IdempotencyStatus,
    R0IntegrityVerifier,
    SQLiteAtomicBatchAppender,
    SQLiteEventPayloadStore,
    SQLiteIdempotentBatchAppender,
    TransactionOwnershipError,
    VerificationBudget,
)
from mentaury.storage.idempotency import IdempotentBatchRequest
from mentaury.validation import SchemaRegistry

PATHS = ["append_one", "atomic", "idempotent"]
ADMISSIONS = ["legacy", "admitted"]
LATER = "2026-08-06T13:00:00Z"


def registry() -> SchemaRegistry:
    return SchemaRegistry((*belief_schema_definitions(), *evidence_gate_schema_definitions()))


def admission(kind: str):
    if kind == "legacy":
        return None
    budget = OperationAdmissionBudget(8, PayloadAdmissionBudget(16, 2_000, 512, 64), 20_000, 200_000, 400_000)
    return OperationAdmissionState(budget)


class Journal:
    """Real SQLite journal with a valid create/attach/attach prefix and the gate decision ready."""

    def __init__(self) -> None:
        self.registry = registry()
        base, lifecycle = BeliefReducer(), BeliefLifecycle()
        state = freeze_payload(base.initial_state())
        create = lifecycle.decide(eg._command(CREATE_BELIEF, {
            "belief_id": eg.BELIEF_ID, "statement": "The governed claim is supported by independent evidence.",
            "claim_type": ClaimType.CONTEXTUAL.value}), state)
        state = eg._apply(base, state, create.domain_events[0], 1, "EVT-CREATE")
        prefix = [(1, "EVT-CREATE", create.domain_events[0])]
        for n in (1, 2):
            attach = lifecycle.decide(eg._command(ATTACH_EVIDENCE, {
                "belief_id": eg.BELIEF_ID, "evidence_ref": f"evidence:for:{n}", "side": EvidenceSide.FOR.value},
                expected_stream_version=n, command_id=f"CMD-ATTACH-{n}"), state)
            state = eg._apply(base, state, attach.domain_events[0], n + 1, f"EVT-ATTACH-{n}")
            prefix.append((n + 1, f"EVT-ATTACH-{n}", attach.domain_events[0]))
        records = (eg._record("evidence:for:1", EvidenceSide.FOR, "source:a"),
                   eg._record("evidence:for:2", EvidenceSide.FOR, "source:b"))
        self.prefix = prefix
        self.command = eg._gate_command(state, records)
        decision = EvidenceGatedBeliefLifecycle().decide(self.command, state)
        assert decision.accepted
        self.pending: PendingEvent = decision.domain_events[0]
        self.payload = dict(self.pending.payload)

    def store(self) -> SQLiteEventPayloadStore:
        store = SQLiteEventPayloadStore.in_memory()
        store.initialize_schema()
        for version, event_id, pending in self.prefix:
            store.append_one(eg._event(pending, version, event_id), pending.payload, registry=self.registry)
        return store

    def event(self, **changes) -> EventEnvelope:
        base = replace(
            eg._event(self.pending, 4, "EVT-GATED"),
            causation_id=self.command.command_id, correlation_id=self.command.correlation_id,
        )
        return replace(base, **changes)

    def payload_with(self, *, evaluated_at: str | None = None, receipt_evaluated_at: str | None = None) -> dict:
        payload = {**self.payload, "receipt": dict(self.payload["receipt"])}
        if evaluated_at is not None:
            payload["evaluated_at"] = evaluated_at
        if receipt_evaluated_at is not None:
            payload["receipt"]["evaluated_at"] = receipt_evaluated_at
        return payload

    def write(self, store, path: str, kind: str, *, event=None, payload=None, command=None):
        event = event or self.event()
        payload = payload if payload is not None else self.payload
        adm = admission(kind)
        if path == "append_one":
            return store.append_one(event, payload, registry=self.registry, admission=adm)
        if path == "atomic":
            return SQLiteAtomicBatchAppender(store, self.registry).append(
                [BatchEntry(event, payload)], admission=adm)
        pending = replace(self.pending, payload=payload) if payload is not self.payload else self.pending
        request = IdempotentBatchRequest(command or self.command, (pending,), (BatchEntry(event, payload),))
        return SQLiteIdempotentBatchAppender(store, self.registry).append(request, admission=adm)

    def count(self, store) -> int:
        return len(store.list_stream(eg.STREAM_ID))


def r0(store):
    return R0IntegrityVerifier(store, registry(), VerificationBudget(100, 100_000, 1_000_000)).verify_stream(eg.STREAM_ID)


def r1(store):
    reducer = EvidenceGatedBeliefReducer()
    events = store.list_stream(eg.STREAM_ID)
    snapshot = make_replay_snapshot(
        reducer_id=reducer.reducer_id, reducer_version=reducer.reducer_version, stream_id=eg.STREAM_ID,
        through_stream_version=1, through_event_hash=events[0].event_hash,
        state=_state_after_create(events))
    return R1ReplayVerifier(store, registry(), VerificationBudget(100, 100_000, 1_000_000),
                            ReplayStateBudget(100_000, 1_000_000), reducer).verify_stream(eg.STREAM_ID, snapshot)


def _state_after_create(events):
    base, lifecycle = BeliefReducer(), BeliefLifecycle()
    state = freeze_payload(base.initial_state())
    create = lifecycle.decide(eg._command(CREATE_BELIEF, {
        "belief_id": eg.BELIEF_ID, "statement": "The governed claim is supported by independent evidence.",
        "claim_type": ClaimType.CONTEXTUAL.value}), state)
    return eg._apply(base, state, create.domain_events[0], 1, "EVT-CREATE")


def refused_clean(journal: Journal, store, error=EvidenceGateTemporalError) -> None:
    """Nothing about the refused gate event was persisted."""

    assert journal.count(store) == 3
    c = store.raw_connection_for_tests()
    assert c.execute("SELECT COUNT(*) FROM event_payloads WHERE payload_ref = 'PAYLOAD-EVT-GATED'").fetchone()[0] == 0
    assert c.execute("SELECT COUNT(*) FROM idempotency_records").fetchone()[0] == 0
    assert store.load_stream_meta(eg.STREAM_ID).current_version == 3
    assert not c.in_transaction


# --- consistent decisions ---------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ADMISSIONS)
@pytest.mark.parametrize("path", PATHS)
def test_consistent_decision_is_written_and_passes_r0_and_r1(path, kind) -> None:
    journal = Journal()
    with journal.store() as store:
        journal.write(store, path, kind)
        assert journal.count(store) == 4
        assert r0(store).ok
        report = r1(store)
        assert report.ok and report.applied_events == 4


@pytest.mark.parametrize("kind", ADMISSIONS)
@pytest.mark.parametrize("path", PATHS)
def test_equivalent_time_zones_are_compared_as_instants(path, kind) -> None:
    journal = Journal()
    zoned = "2026-08-06T14:00:00+02:00"  # the same instant as 12:00:00Z
    command = replace(journal.command, issued_at=zoned)
    with journal.store() as store:
        journal.write(store, path, kind, event=journal.event(occurred_at=zoned), command=command,
                      payload=journal.payload_with(evaluated_at="2026-08-06T10:00:00-02:00"))
        assert r0(store).ok and r1(store).ok


# --- inconsistent decisions are refused before persistence -----------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ADMISSIONS)
@pytest.mark.parametrize("path", PATHS)
def test_mismatched_occurred_at_is_refused_before_anything_is_stored(path, kind) -> None:
    journal = Journal()
    with journal.store() as store:
        with pytest.raises(EvidenceGateTemporalError, match="evaluated_at must equal immutable event occurred_at"):
            journal.write(store, path, kind, event=journal.event(occurred_at=LATER))
        refused_clean(journal, store)
        journal.write(store, path, kind)  # the corrected decision is accepted afterwards
        assert journal.count(store) == 4


@pytest.mark.parametrize("kind", ADMISSIONS)
@pytest.mark.parametrize("path", PATHS)
def test_mismatched_receipt_evaluated_at_is_refused(path, kind) -> None:
    journal = Journal()
    with journal.store() as store:
        with pytest.raises(EvidenceGateTemporalError, match="receipt evaluated_at must equal payload evaluated_at"):
            journal.write(store, path, kind, payload=journal.payload_with(receipt_evaluated_at=LATER))
        refused_clean(journal, store)


@pytest.mark.parametrize("kind", ADMISSIONS)
@pytest.mark.parametrize("path", PATHS)
def test_mismatched_payload_evaluated_at_is_refused(path, kind) -> None:
    journal = Journal()
    with journal.store() as store:
        with pytest.raises(EvidenceGateTemporalError, match="evaluated_at must equal immutable event occurred_at"):
            journal.write(store, path, kind,
                          payload=journal.payload_with(evaluated_at=LATER, receipt_evaluated_at=LATER))
        refused_clean(journal, store)


@pytest.mark.parametrize("kind", ADMISSIONS)
def test_mismatched_command_issued_at_is_refused_at_first_application(kind) -> None:
    journal = Journal()
    with journal.store() as store:
        late_command = replace(journal.command, issued_at=LATER)  # event/payload/receipt agree at 12:00Z
        with pytest.raises(EvidenceGateTemporalError, match="command issued_at must equal"):
            journal.write(store, "idempotent", kind, command=late_command)
        refused_clean(journal, store)  # no event, no payload, no idempotency record, no open transaction


@pytest.mark.parametrize("kind", ADMISSIONS)
@pytest.mark.parametrize("path", PATHS)
def test_invalid_timestamps_are_controlled_refusals(path, kind) -> None:
    journal = Journal()
    with journal.store() as store:
        with pytest.raises((EvidenceGateTemporalError, SchemaValidationError, ValueError)):
            journal.write(store, path, kind, event=journal.event(occurred_at="not-a-timestamp"))
        refused_clean(journal, store)
        with pytest.raises((EvidenceGateTemporalError, SchemaValidationError)):
            journal.write(store, path, kind, payload=journal.payload_with(evaluated_at="yesterday-ish"))
        refused_clean(journal, store)
        with pytest.raises((EvidenceGateTemporalError, SchemaValidationError)):
            journal.write(store, path, kind, payload=journal.payload_with(receipt_evaluated_at="2026-13-45T99:00:00Z"))
        refused_clean(journal, store)


# --- batch atomicity and idempotency -------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ADMISSIONS)
def test_one_bad_gate_event_rejects_the_whole_batch(kind) -> None:
    journal = Journal()
    attach_pending = journal.prefix[2][2]
    shared = dict(batch_id="BATCH-PAIR", batch_size=2, causation_id="CMD-PAIR", correlation_id="CORR-PAIR")
    first = replace(eg._event(attach_pending, 4, "EVT-PAIR-1"), batch_index=0, **shared)
    second = replace(journal.event(occurred_at=LATER), event_id="EVT-PAIR-2", stream_version=5,
                     batch_index=1, payload_ref="PAYLOAD-PAIR-2", **shared)
    with journal.store() as store:
        with pytest.raises(EvidenceGateTemporalError):
            SQLiteAtomicBatchAppender(store, journal.registry).append(
                [BatchEntry(first, attach_pending.payload), BatchEntry(second, journal.payload)],
                admission=admission(kind))
        refused_clean(journal, store)  # the valid first entry was not written either


@pytest.mark.parametrize("kind", ADMISSIONS)
def test_refused_first_application_leaves_no_receipt_and_a_corrected_retry_applies(kind) -> None:
    journal = Journal()
    with journal.store() as store:
        with pytest.raises(EvidenceGateTemporalError):
            journal.write(store, "idempotent", kind, event=journal.event(occurred_at=LATER))
        refused_clean(journal, store)
        result = journal.write(store, "idempotent", kind)
        assert result.status is IdempotencyStatus.APPLIED  # no false receipt blocked it


@pytest.mark.parametrize("kind", ADMISSIONS)
def test_semantic_replay_returns_the_original_result_without_rebinding_historical_time(kind) -> None:
    journal = Journal()
    with journal.store() as store:
        first = journal.write(store, "idempotent", "legacy")
        stored_before = store.load_event("EVT-GATED")
        # an exact retry
        again = journal.write(store, "idempotent", kind, event=journal.event(event_id="EVT-RETRY-1",
                                                                              payload_ref="PAYLOAD-RETRY-1"))
        assert again.status is IdempotencyStatus.ALREADY_APPLIED and again.receipt == first.receipt
        # a retry whose volatile time fields differ (fingerprints exclude them): still the original
        # receipt, nothing is written and the stored occurred_at is not rebound to the new time
        late = replace(journal.command, issued_at=LATER)
        replay = journal.write(store, "idempotent", kind, command=late,
                               event=journal.event(event_id="EVT-RETRY-2", payload_ref="PAYLOAD-RETRY-2",
                                                   occurred_at=LATER))
        assert replay.status is IdempotencyStatus.ALREADY_APPLIED and replay.receipt == first.receipt
        assert journal.count(store) == 4
        assert store.load_event("EVT-GATED") == stored_before
        assert store.load_event("EVT-GATED").occurred_at == "2026-08-06T12:00:00Z"
        assert r0(store).ok and r1(store).ok


# --- scope: only Evidence Gate decisions, existing paths and transactions --------------------------------------------------------------------

def test_other_event_types_are_not_bound_to_command_time() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    entries = tuple(BatchEntry(replace(e.event, occurred_at="2031-01-01T00:00:00Z"), e.payload)
                    for e in idem.entries_for(cmd, pending))
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        result = SQLiteIdempotentBatchAppender(store, idem.registry()).append(
            IdempotentBatchRequest(cmd, pending, entries))
        assert result.status is IdempotencyStatus.APPLIED  # occurred_at != command.issued_at is fine here


@pytest.mark.parametrize("path", PATHS)
def test_foreign_transaction_is_never_touched(path) -> None:
    journal = Journal()
    with journal.store() as store:
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        # inconsistent: refused (before the transaction for append_one/atomic, by ownership for idempotent)
        with pytest.raises((EvidenceGateTemporalError, TransactionOwnershipError)):
            journal.write(store, path, "legacy", event=journal.event(occurred_at=LATER))
        with pytest.raises(TransactionOwnershipError):  # consistent: the Stage 01 ownership refusal
            journal.write(store, path, "legacy")
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")


# --- historical records and the reducer ---------------------------------------------------------------------------------------------------------

def test_a_historical_violating_record_is_still_rejected_by_the_reducer(monkeypatch) -> None:
    journal = Journal()
    with journal.store() as store:
        with monkeypatch.context() as patch:  # simulate a record written before this check existed
            patch.setattr(sealing_module, "_require_gate_time", lambda *a, **k: None)
            journal.write(store, "append_one", "legacy", event=journal.event(occurred_at=LATER))
        assert journal.count(store) == 4
        assert r0(store).ok  # R0 semantics are unchanged: it does not judge gate timestamps
        report = r1(store)
        assert not report.ok and "evaluated_at must equal" in report.failure.message  # reducer still refuses
        with pytest.raises(EvidenceGateTemporalError):  # and new violating writes are refused again
            journal.write(store, "atomic", "legacy",
                          event=journal.event(event_id="EVT-GATED-2", stream_version=5,
                                              payload_ref="PAYLOAD-GATED-2", occurred_at=LATER))


# --- the persisted representation is the one that is checked -------------------------------------------------------------------------------------

class _Alternating(dict):
    """Reports a different ``evaluated_at`` on successive reads of the mapping."""

    def __init__(self, good: dict, bad_value: str, start: int) -> None:
        super().__init__(good)
        self.good_value = good["evaluated_at"]
        self.bad_value = bad_value
        self.reads = start

    def items(self):
        self.reads += 1
        flip = self.bad_value if self.reads % 2 == 0 else self.good_value
        return iter([(k, flip if k == "evaluated_at" else v) for k, v in super().items()])

    def __iter__(self):
        return iter(super().keys())

    def __getitem__(self, key):
        return dict.__getitem__(self, key)


@pytest.mark.parametrize("kind", ADMISSIONS)
@pytest.mark.parametrize("start", [0, 1, 2, 3])
def test_whatever_bytes_are_stored_satisfy_the_time_contract_even_for_a_mutating_mapping(kind, start) -> None:
    journal = Journal()
    mutating = _Alternating(journal.payload, LATER, start)
    with journal.store() as store:
        try:
            journal.write(store, "append_one", kind, payload=mutating)
        except (EvidenceGateTemporalError, SchemaValidationError, ValueError):
            refused_clean(journal, store)
            return
        stored = store.load_payload("PAYLOAD-EVT-GATED").payload_bytes
        import json as _json

        decoded = _json.loads(stored)
        assert decoded["evaluated_at"] == journal.event().occurred_at  # the stored bytes are consistent
        assert r1(store).ok

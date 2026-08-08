"""Независимые leaf-типы для epistemic contracts.

Этот модуль намеренно не живёт внутри ``mentaury.beliefs`` и
``mentaury.evidence``: импорт submodule пакета выполняет package
``__init__``, что и создаёт circular ImportError при
``import mentaury.evidence`` → ``beliefs.contracts`` →
``beliefs.__init__`` → ``evidence_gate`` → частично инициализированный
``mentaury.evidence``.

``ClaimType`` и ``EvidenceSide`` имеют единую type identity и
реэкспортируются из ``mentaury.beliefs.contracts`` для совместимости.
"""

from __future__ import annotations

from enum import StrEnum


class ClaimType(StrEnum):
    UNIVERSAL = "universal"
    STATISTICAL = "statistical"
    CAUSAL = "causal"
    CONTEXTUAL = "contextual"
    EXISTENTIAL = "existential"
    UNSPECIFIED = "unspecified"


class EvidenceSide(StrEnum):
    FOR = "for"
    AGAINST = "against"

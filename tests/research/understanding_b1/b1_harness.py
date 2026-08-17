from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
import re
from pathlib import Path
from typing import Any, Iterable

IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

TOP_LEVEL_KEYS = {
    "scenario_id",
    "run_id",
    "mode",
    "semantic_payload_digest",
    "situation_model",
    "material_constraints",
    "alternatives",
    "consequences",
    "critical_unknowns",
    "next_discrimination_need",
    "governed_conclusion",
}
ID_COLLECTIONS = (
    "situation_model",
    "material_constraints",
    "alternatives",
    "consequences",
    "critical_unknowns",
)
SET_DRIFT_CODES = {
    "situation_model": "B1-SITUATION-SET-DRIFT",
    "material_constraints": "B1-CONSTRAINT-SET-DRIFT",
    "alternatives": "B1-ALTERNATIVES-SET-DRIFT",
    "consequences": "B1-CONSEQUENCES-SET-DRIFT",
    "critical_unknowns": "B1-CRITICAL-UNKNOWNS-SET-DRIFT",
}
CONCLUSION_KINDS = {"CONDITIONAL", "DEFER", "NONE"}
NDN_KINDS = {"JUSTIFIED_STOP", "REQUESTED_OBSERVATION", "DEFER"}

# This vocabulary is secondary defense and error classification only.
# Closed object schemas are the primary defense.
POLICY_AUTHORITY_KEYS = {
    "authorization",
    "authorized",
    "authorized_action",
    "action",
    "permission",
    "decision_rule",
    "rank",
    "ranking",
    "score",
    "priority",
    "probability",
    "confidence",
    "confidence_score",
    "selected",
    "preferred",
    "verdict",
    "supported",
    "contradicted",
    "recommended",
    "recommendation",
    "tool",
    "tool_plan",
    "retrieval",
    "runtime",
    "deployment",
    "truth",
    "belief",
    "identity_update",
    "relationship_update",
    "query",
}

@dataclass(frozen=True)
class Issue:
    code: str
    path: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def semantic_payload_digest(source_frame: dict[str, Any]) -> str:
    return "sha256:" + sha256(canonical_json(source_frame["semantic_payload"])).hexdigest()


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _is_policy_authority_key(key: str) -> bool:
    normalized = _normalize_key(key)
    if normalized in POLICY_AUTHORITY_KEYS:
        return True
    return any(
        token in normalized
        for token in (
            "authoriz",
            "permission",
            "probab",
            "confidence",
            "verdict",
            "recommend",
            "selected",
            "preferred",
            "ranking",
            "runtime",
            "deploy",
            "retriev",
            "tool_plan",
            "identity_update",
            "relationship_update",
        )
    )


def _identifier_ok(value: Any) -> bool:
    return isinstance(value, str) and IDENTIFIER_RE.fullmatch(value) is not None


def _append_unique(issues: list[Issue], issue: Issue) -> None:
    if issue not in issues:
        issues.append(issue)


def verify_source_frame(source: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    required = {"scenario_id", "semantic_payload", "semantic_payload_digest"}
    missing = sorted(required - set(source))
    for key in missing:
        issues.append(Issue("B1-SOURCE-INVALID", f"source.{key}", "missing required source field"))
    if missing:
        return issues

    if not _identifier_ok(source["scenario_id"]):
        issues.append(Issue("B1-SOURCE-INVALID", "source.scenario_id", "invalid identifier"))

    expected = semantic_payload_digest(source)
    if source["semantic_payload_digest"] != expected:
        issues.append(
            Issue(
                "B1-SOURCE-DIGEST-MISMATCH",
                "source.semantic_payload_digest",
                f"declared={source['semantic_payload_digest']!r} recomputed={expected!r}",
            )
        )

    payload = source.get("semantic_payload")
    if not isinstance(payload, dict):
        issues.append(Issue("B1-SOURCE-INVALID", "source.semantic_payload", "must be object"))
        return issues

    for name in ID_COLLECTIONS:
        items = payload.get(name)
        if not isinstance(items, list):
            issues.append(Issue("B1-SOURCE-INVALID", f"source.semantic_payload.{name}", "must be list"))
            continue
        seen: set[str] = set()
        for idx, item in enumerate(items):
            path = f"source.semantic_payload.{name}[{idx}]"
            if not isinstance(item, dict) or set(item) != {"id", "text"}:
                issues.append(Issue("B1-SOURCE-INVALID", path, "source item must contain exactly id,text"))
                continue
            item_id = item.get("id")
            if not _identifier_ok(item_id):
                issues.append(Issue("B1-SOURCE-INVALID", f"{path}.id", "invalid identifier"))
                continue
            if item_id in seen:
                issues.append(Issue("B1-SOURCE-INVALID", f"{path}.id", "duplicate source id"))
            seen.add(item_id)
            if not isinstance(item.get("text"), str) or not item["text"].strip():
                issues.append(Issue("B1-SOURCE-INVALID", f"{path}.text", "source text must be non-empty"))

    allowed_ndn = payload.get("allowed_discrimination_kinds")
    if (
        not isinstance(allowed_ndn, list)
        or not allowed_ndn
        or len(set(allowed_ndn)) != len(allowed_ndn)
        or any(kind not in NDN_KINDS for kind in allowed_ndn)
    ):
        issues.append(
            Issue(
                "B1-SOURCE-INVALID",
                "source.semantic_payload.allowed_discrimination_kinds",
                "must be a non-empty unique subset of the frozen B1 discrimination enum",
            )
        )

    scope = payload.get("governed_conclusion_scope")
    if not _identifier_ok(scope):
        issues.append(
            Issue(
                "B1-SOURCE-INVALID",
                "source.semantic_payload.governed_conclusion_scope",
                "must be a source-bound scope identifier",
            )
        )

    return issues


def _source_ids(source: dict[str, Any], name: str) -> list[str]:
    return [item["id"] for item in source["semantic_payload"][name]]


def validate_b1(source: dict[str, Any], candidate: Any) -> list[Issue]:
    source_issues = verify_source_frame(source)
    if source_issues:
        return source_issues

    issues: list[Issue] = []
    if not isinstance(candidate, dict):
        return [Issue("B1-TYPE-ERROR", "$", "candidate must be object")]

    candidate_keys = set(candidate)
    extra_top = sorted(candidate_keys - TOP_LEVEL_KEYS)
    for key in extra_top:
        path = f"$.{key}"
        if key == "final_presentation":
            issues.append(Issue("B1-PRESENTATION-LEAK", path, "free-form presentation is forbidden in B1"))
        elif key == "decision_rule":
            issues.append(Issue("B1-UNEXPECTED-TOP-LEVEL", path, "unexpected top-level field"))
            issues.append(Issue("B1-POLICY-OR-AUTHORITY-LEAK", path, "decision policy is forbidden"))
        elif _is_policy_authority_key(key):
            issues.append(Issue("B1-POLICY-OR-AUTHORITY-LEAK", path, "policy/authority-shaped field is forbidden"))
        else:
            issues.append(Issue("B1-UNEXPECTED-TOP-LEVEL", path, "unexpected top-level field"))

    missing_top = sorted(TOP_LEVEL_KEYS - candidate_keys)
    for key in missing_top:
        issues.append(Issue("B1-MISSING-FIELD", f"$.{key}", "required top-level field missing"))

    # Continue only for fields that exist; this keeps diagnostics deterministic and crash-free.
    if "scenario_id" in candidate:
        if candidate["scenario_id"] != source["scenario_id"]:
            issues.append(Issue("B1-SCENARIO-DRIFT", "$.scenario_id", "scenario id must exactly match source"))
        elif not _identifier_ok(candidate["scenario_id"]):
            issues.append(Issue("B1-IDENTIFIER-INVALID", "$.scenario_id", "invalid identifier syntax"))

    if "run_id" in candidate and not _identifier_ok(candidate["run_id"]):
        issues.append(Issue("B1-IDENTIFIER-INVALID", "$.run_id", "run id must be a bounded identifier, not prose"))

    if "mode" in candidate and candidate["mode"] != "B1":
        issues.append(Issue("B1-MODE-DRIFT", "$.mode", "mode must equal B1"))

    if "semantic_payload_digest" in candidate:
        digest = candidate["semantic_payload_digest"]
        if not isinstance(digest, str) or DIGEST_RE.fullmatch(digest) is None or digest != source["semantic_payload_digest"]:
            issues.append(Issue("B1-PAYLOAD-DRIFT", "$.semantic_payload_digest", "digest must exactly match verified source payload"))

    for name in ID_COLLECTIONS:
        if name not in candidate:
            continue
        value = candidate[name]
        if not isinstance(value, list):
            issues.append(Issue("B1-TYPE-ERROR", f"$.{name}", "must be list"))
            continue

        ids: list[str] = []
        duplicate_seen = False
        for idx, item in enumerate(value):
            path = f"$.{name}[{idx}]"
            if not isinstance(item, dict):
                issues.append(Issue("B1-TYPE-ERROR", path, "item must be object"))
                continue
            extra = sorted(set(item) - {"id"})
            for key in extra:
                key_path = f"{path}.{key}"
                if _is_policy_authority_key(key):
                    issues.append(Issue("B1-POLICY-OR-AUTHORITY-LEAK", key_path, "nested policy/authority field forbidden"))
                else:
                    issues.append(Issue("B1-INVENTED-SEMANTIC-CONTENT", key_path, "B1 items are ID-only; free semantic content forbidden"))
            if "id" not in item:
                issues.append(Issue("B1-MISSING-FIELD", f"{path}.id", "id required"))
                continue
            item_id = item["id"]
            if not _identifier_ok(item_id):
                issues.append(Issue("B1-IDENTIFIER-INVALID", f"{path}.id", "invalid identifier syntax"))
                continue
            if item_id in ids and not duplicate_seen:
                issues.append(Issue("B1-DUPLICATE-ID", f"$.{name}", f"duplicate id {item_id}"))
                duplicate_seen = True
            ids.append(item_id)

        expected_ids = _source_ids(source, name)
        if set(ids) != set(expected_ids):
            issues.append(
                Issue(
                    SET_DRIFT_CODES[name],
                    f"$.{name}",
                    f"expected ids={sorted(expected_ids)!r}; observed ids={sorted(set(ids))!r}",
                )
            )

    if "next_discrimination_need" in candidate:
        ndn = candidate["next_discrimination_need"]
        path = "$.next_discrimination_need"
        if not isinstance(ndn, dict):
            issues.append(Issue("B1-TYPE-ERROR", path, "must be object"))
        else:
            extra = sorted(set(ndn) - {"kind", "basis_refs"})
            for key in extra:
                key_path = f"{path}.{key}"
                if _is_policy_authority_key(key):
                    issues.append(Issue("B1-POLICY-OR-AUTHORITY-LEAK", key_path, "generated inquiry/policy field forbidden"))
                else:
                    issues.append(Issue("B1-INVENTED-SEMANTIC-CONTENT", key_path, "unexpected nested field"))
            if not extra and set(ndn) == {"kind", "basis_refs"}:
                allowed_kinds = set(source["semantic_payload"]["allowed_discrimination_kinds"])
                if ndn.get("kind") not in allowed_kinds:
                    issues.append(Issue("B1-DISCRIMINATION-NEED-DRIFT", f"{path}.kind", "kind is outside source-declared frozen enum"))
                refs = ndn.get("basis_refs")
                allowed_refs = set(_source_ids(source, "critical_unknowns"))
                if not isinstance(refs, list) or any(not _identifier_ok(v) for v in refs):
                    issues.append(Issue("B1-TYPE-ERROR", f"{path}.basis_refs", "basis refs must be identifier list"))
                else:
                    if len(refs) != len(set(refs)):
                        issues.append(Issue("B1-DUPLICATE-ID", f"{path}.basis_refs", "duplicate basis ref"))
                    if not set(refs).issubset(allowed_refs):
                        issues.append(Issue("B1-DISCRIMINATION-BASIS-DRIFT", f"{path}.basis_refs", "basis refs must be source critical-unknown IDs"))

    if "governed_conclusion" in candidate:
        conclusion = candidate["governed_conclusion"]
        path = "$.governed_conclusion"
        if not isinstance(conclusion, dict):
            issues.append(Issue("B1-TYPE-ERROR", path, "must be object"))
        else:
            extra = sorted(set(conclusion) - {"kind", "scope"})
            for key in extra:
                key_path = f"{path}.{key}"
                if _is_policy_authority_key(key):
                    issues.append(Issue("B1-POLICY-OR-AUTHORITY-LEAK", key_path, "authority/action field forbidden"))
                else:
                    issues.append(Issue("B1-INVENTED-SEMANTIC-CONTENT", key_path, "unexpected nested field"))
            if "kind" in conclusion and conclusion["kind"] not in CONCLUSION_KINDS:
                issues.append(Issue("B1-CONCLUSION-OVERCLAIM", f"{path}.kind", "only CONDITIONAL|DEFER|NONE allowed"))
            if "scope" in conclusion and conclusion["scope"] != source["semantic_payload"]["governed_conclusion_scope"]:
                issues.append(Issue("B1-CONCLUSION-SCOPE-DRIFT", f"{path}.scope", "scope must exactly match source-bound scope"))

    return issues


def validate_or_raise(source: dict[str, Any], candidate: Any) -> None:
    issues = validate_b1(source, candidate)
    if issues:
        codes = ", ".join(issue.code for issue in issues)
        raise ValueError(f"B1 validation failed: {codes}")


def render_b1(source: dict[str, Any], candidate: dict[str, Any]) -> str:
    """Render only after validation. Candidate free prose is never accepted or rendered."""
    validate_or_raise(source, candidate)
    payload = source["semantic_payload"]

    source_maps: dict[str, dict[str, str]] = {
        name: {item["id"]: item["text"] for item in payload[name]} for name in ID_COLLECTIONS
    }
    headings = {
        "situation_model": "Situation model",
        "material_constraints": "Material constraints",
        "alternatives": "Alternatives",
        "consequences": "Consequences",
        "critical_unknowns": "Critical unknowns",
    }
    lines = [f"B1 neutral control · {candidate['scenario_id']}"]
    for name in ID_COLLECTIONS:
        lines.append("")
        lines.append(headings[name])
        order = _source_ids(source, name)
        observed = {item["id"] for item in candidate[name]}
        for item_id in order:
            if item_id in observed:
                lines.append(f"- {item_id}: {source_maps[name][item_id]}")

    ndn = candidate["next_discrimination_need"]
    lines.extend([
        "",
        "Next discrimination need",
        f"- {ndn['kind']} · basis: {', '.join(ndn['basis_refs']) or 'NONE'}",
    ])
    conclusion = candidate["governed_conclusion"]
    lines.extend([
        "",
        "Governed conclusion",
        f"- {conclusion['kind']} · scope: {conclusion['scope']}",
    ])
    return "\n".join(lines) + "\n"


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def file_sha256(path: str | Path) -> str:
    return sha256(Path(path).read_bytes()).hexdigest()


def codes(issues: Iterable[Issue]) -> list[str]:
    return [issue.code for issue in issues]

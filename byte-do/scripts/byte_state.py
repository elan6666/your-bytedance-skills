#!/usr/bin/env python3
"""Inspect and update Byte OS state without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLAN_STATUSES = {"pending", "ready", "in_progress", "complete", "blocked"}
REVIEW_VERDICTS = {"ship", "iterate", "block"}
STATUS_ENUMS = {
    "mode": {"step", "auto"},
    "project_kind": {"greenfield", "existing_codebase", "unknown"},
    "stage": {
        "discussing",
        "started",
        "researched",
        "shaped",
        "planned",
        "building",
        "reviewed",
        "iterating",
        "delivered",
        "blocked",
    },
    "review_verdict": {"none", *REVIEW_VERDICTS},
    "harness_status": {"not_required", "required", "partial", "ready", "blocked"},
}
STATUS_KEY_ORDER = (
    "schema_version",
    "mode",
    "project_kind",
    "stage",
    "current_workflow",
    "next_workflow",
    "review_verdict",
    "iteration_count",
    "harness_status",
    "hard_blocked",
    "updated_at",
)
STATUS_KEYS = set(STATUS_KEY_ORDER)


def _coerce(value: str) -> Any:
    value = value.strip().strip('"').strip("'")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [_coerce(item) for item in inner.split(",")]
    return value


def _read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    if not path.exists():
        return {}, ""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    values: dict[str, Any] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = _coerce(value)
    return values, text[end + 5 :]


def _legacy_status(body: str) -> dict[str, Any]:
    aliases = {
        "mode": "mode",
        "stage": "stage",
        "current command": "current_workflow",
        "current workflow": "current_workflow",
        "next recommended command": "next_workflow",
        "next workflow": "next_workflow",
        "review verdict": "review_verdict",
        "iteration count": "iteration_count",
        "hard blocked": "hard_blocked",
        "project kind": "project_kind",
        "harness": "harness_status",
        "harness status": "harness_status",
    }
    values: dict[str, Any] = {}
    for line in body.splitlines():
        match = re.match(r"^\s*[-*]?\s*([^:#]+):\s*(.+?)\s*$", line)
        if not match:
            continue
        key = aliases.get(match.group(1).strip().lower())
        if key and key not in values:
            values[key] = _coerce(match.group(2))
    return values


def _event_time(path: Path, metadata: dict[str, Any]) -> float:
    value = metadata.get("created_at") or metadata.get("updated_at")
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        except ValueError:
            pass
    return path.stat().st_mtime


def _latest_event(paths: list[Path]) -> dict[str, Any] | None:
    events = []
    for path in paths:
        metadata, body = _read_frontmatter(path)
        events.append(
            {
                "path": str(path),
                "time": _event_time(path, metadata),
                "metadata": metadata,
                "body": body,
            }
        )
    return max(events, key=lambda event: event["time"]) if events else None


def _review_verdict(event: dict[str, Any] | None) -> str | None:
    if not event:
        return None
    metadata = event["metadata"]
    candidate = str(metadata.get("verdict", "")).lower()
    if candidate in REVIEW_VERDICTS:
        return candidate
    body = event["body"]
    patterns = [
        r"(?im)^\s*review verdict:\s*(ship|iterate|block)\s*$",
        r"(?ims)^#\s*verdict\s*\n+\s*(ship|iterate|block)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, body)
        if match:
            return match.group(1).lower()
    return None


def scan(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state_dir = root / ".byte-os"
    if not state_dir.is_dir():
        return {"root": str(root), "byte_os_exists": False}

    status_meta, status_body = _read_frontmatter(state_dir / "STATUS.md")
    status = {**_legacy_status(status_body), **status_meta}

    plans = []
    for path in sorted((state_dir / "plans").glob("*.plan.md")):
        metadata, _ = _read_frontmatter(path)
        plan_status = str(metadata.get("status", "unknown"))
        plans.append(
            {
                "path": str(path),
                "id": str(metadata.get("id", path.name.split("-", 1)[0])),
                "status": plan_status,
                "time": _event_time(path, metadata),
            }
        )

    review = _latest_event(list((state_dir / "reviews").glob("review-*.md")))
    iteration = _latest_event(
        list((state_dir / "iterations").glob("iteration-*.md"))
    )
    artifacts = {
        name: (state_dir / name).exists()
        for name in [
            "BYTE.md",
            "RESEARCH.md",
            "COMPETITORS.md",
            "PRODUCT_SPEC.md",
            "UX_SPEC.md",
            "TECH_SPEC.md",
            "CODEBASE_MAP.md",
            "HARNESS.md",
            "AGENTS_AUDIT.md",
            "DELIVERY.md",
            "DISCUSSION.md",
            "BRAINSTORM.md",
        ]
    }
    latest_plan_time = max((plan["time"] for plan in plans), default=0.0)
    latest_review_time = review["time"] if review else 0.0
    latest_iteration_time = iteration["time"] if iteration else 0.0

    return {
        "root": str(root),
        "byte_os_exists": True,
        "status": status,
        "artifacts": artifacts,
        "plans": plans,
        "plan_counts": {
            value: sum(plan["status"] == value for plan in plans)
            for value in sorted(PLAN_STATUSES)
        },
        "latest_review": {
            "path": review["path"],
            "time": latest_review_time,
            "verdict": _review_verdict(review),
        }
        if review
        else None,
        "latest_iteration": {
            "path": iteration["path"],
            "time": latest_iteration_time,
        }
        if iteration
        else None,
        "evidence_newer_than_review": bool(
            review
            and max(latest_plan_time, latest_iteration_time) > latest_review_time
        ),
    }


def next_workflow(state: dict[str, Any]) -> tuple[str, str]:
    if not state.get("byte_os_exists"):
        return "byte-start", "Byte OS state does not exist"

    status = state["status"]
    artifacts = state["artifacts"]
    if status.get("hard_blocked") is True or status.get("stage") == "blocked":
        return "byte-status", "A hard blocker requires explicit user or external action"
    specs_complete = all(
        artifacts[name]
        for name in ["PRODUCT_SPEC.md", "UX_SPEC.md", "TECH_SPEC.md"]
    )
    if artifacts["BRAINSTORM.md"] and not artifacts["DISCUSSION.md"] and not specs_complete:
        return "byte-discuss", "A brainstorm exists without a confirmed direction"
    if artifacts["DISCUSSION.md"] and not specs_complete:
        return "byte-shape", "Discussion exists but product specs are incomplete"

    harness_expected = status.get("project_kind") == "existing_codebase" or status.get(
        "harness_status"
    ) in {"required", "partial", "ready", "blocked"}
    if harness_expected:
        harness_complete = all(
            artifacts[name]
            for name in ["CODEBASE_MAP.md", "HARNESS.md", "AGENTS_AUDIT.md"]
        )
        if not harness_complete:
            return "byte-codebase-harness", "Existing codebase harness is incomplete"

    if not specs_complete:
        return "byte-shape", "Product, UX, or technical specs are incomplete"
    if not state["plans"]:
        return "byte-plan", "Specs exist but no executable plans exist"
    if any(plan["status"] != "complete" for plan in state["plans"]):
        return "byte-build", "At least one plan is incomplete"
    if not state["latest_review"]:
        return "byte-review", "Completed plans have not been reviewed"
    if state["evidence_newer_than_review"]:
        return "byte-review", "Build or iteration evidence is newer than the latest review"

    verdict = state["latest_review"]["verdict"]
    if verdict in {"iterate", "block"}:
        return "byte-iterate", f"Latest current review verdict is {verdict}"
    if verdict == "ship" and not artifacts["DELIVERY.md"]:
        return "byte-deliver", "Latest review is ship and delivery is missing"
    if artifacts["DELIVERY.md"]:
        return "byte-status", "Delivery exists; wait for explicit real user evidence"
    return "byte-review", "Latest review verdict is missing or invalid"


def validate(state: dict[str, Any]) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not state.get("byte_os_exists"):
        return {"errors": [".byte-os directory is missing"], "warnings": []}

    status = state["status"]
    unknown_keys = sorted(set(status) - STATUS_KEYS)
    if unknown_keys:
        warnings.append(f"Unknown STATUS.md frontmatter keys: {', '.join(unknown_keys)}")
    if status.get("schema_version") != 1:
        warnings.append("STATUS.md does not declare schema_version: 1")
    for key, allowed in STATUS_ENUMS.items():
        value = status.get(key)
        if value is not None and value not in allowed:
            errors.append(f"Invalid {key} value: {value!r}")
    for plan in state["plans"]:
        if plan["status"] not in PLAN_STATUSES:
            errors.append(f"Invalid plan status {plan['status']!r}: {plan['path']}")
    review = state.get("latest_review")
    if review and review["verdict"] not in REVIEW_VERDICTS:
        errors.append(f"Latest review has no valid verdict: {review['path']}")
    return {"errors": errors, "warnings": warnings}


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    value = str(value)
    if re.fullmatch(r"[A-Za-z0-9_.:/+-]+", value):
        return value
    return json.dumps(value, ensure_ascii=True)


def update(root: Path, assignments: list[str]) -> dict[str, Any]:
    state_dir = root.resolve() / ".byte-os"
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / "STATUS.md"
    metadata, body = _read_frontmatter(path)
    metadata = {**_legacy_status(body), **metadata}
    for assignment in assignments:
        if "=" not in assignment:
            raise ValueError(f"Expected key=value, got {assignment!r}")
        key, value = assignment.split("=", 1)
        if key not in STATUS_KEYS:
            raise ValueError(f"Unsupported status key: {key}")
        metadata[key] = _coerce(value)
    metadata.setdefault("schema_version", 1)
    metadata["updated_at"] = datetime.now(timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )
    ordered = [key for key in STATUS_KEY_ORDER if key in metadata]
    lines = (
        ["---"]
        + [f"{key}: {_yaml_scalar(metadata[key])}" for key in ordered]
        + ["---", ""]
    )
    path.write_text("\n".join(lines) + body.lstrip("\n"), encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ["scan", "next", "validate"]:
        child = subparsers.add_parser(command)
        child.add_argument("--root", type=Path, default=Path.cwd())
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--root", type=Path, default=Path.cwd())
    update_parser.add_argument("--set", action="append", default=[], dest="assignments")
    args = parser.parse_args()

    if args.command == "update":
        result: Any = update(args.root, args.assignments)
    else:
        state = scan(args.root)
        if args.command == "scan":
            result = state
        elif args.command == "next":
            workflow, reason = next_workflow(state)
            result = {"workflow": workflow, "reason": reason}
        else:
            result = validate(state)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if args.command == "validate" and result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

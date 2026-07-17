#!/usr/bin/env python3
"""Validate an AI Tutor v4 state.json using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MODES = {"course", "quick-explain", "practice", "review", "diagnosis"}
STATES = {
    "intake",
    "diagnose",
    "teach",
    "check",
    "evaluate",
    "remediate",
    "apply",
    "review",
    "paused",
    "completed",
}
MASTERY = {
    "introduced",
    "assisted",
    "provisional",
    "retained",
    "transferred",
    "mastered",
}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]

    required = {
        "schema_version": int,
        "skill_version": str,
        "topic": dict,
        "goal": dict,
        "mode": str,
        "current_state": str,
        "next_actions": list,
        "mastery": dict,
        "weak_points": list,
        "review_queue": list,
        "application_queue": list,
        "session": dict,
    }
    for key, expected in required.items():
        if key not in data:
            fail(errors, f"missing required field: {key}")
        elif not isinstance(data[key], expected):
            fail(errors, f"{key} must be {expected.__name__}")

    if errors:
        return errors

    if data["schema_version"] != 1:
        fail(errors, "schema_version must be 1")
    if data["skill_version"] != "4.0.0":
        fail(errors, "skill_version must be 4.0.0")
    if data["mode"] not in MODES:
        fail(errors, f"invalid mode: {data['mode']}")
    if data["current_state"] not in STATES:
        fail(errors, f"invalid current_state: {data['current_state']}")

    topic = data["topic"]
    for key in ("title", "slug", "scope"):
        if key not in topic or not isinstance(topic[key], str):
            fail(errors, f"topic.{key} must be a string")
    slug = topic.get("slug", "")
    if slug and not SLUG.fullmatch(slug):
        fail(errors, "topic.slug must use lowercase letters, digits, and single hyphens")

    goal = data["goal"]
    for key in ("purpose", "observable_outcome", "time_constraints"):
        if key not in goal or not isinstance(goal[key], str):
            fail(errors, f"goal.{key} must be a string")
    if not isinstance(goal.get("success_criteria"), list):
        fail(errors, "goal.success_criteria must be a list")

    for concept, record in data["mastery"].items():
        if not isinstance(concept, str) or not concept:
            fail(errors, "mastery keys must be non-empty strings")
            continue
        if not isinstance(record, dict):
            fail(errors, f"mastery.{concept} must be an object")
            continue
        status = record.get("status")
        if status not in MASTERY:
            fail(errors, f"mastery.{concept}.status is invalid: {status}")
        score = record.get("last_score")
        if score is not None and (not isinstance(score, int) or not 0 <= score <= 8):
            fail(errors, f"mastery.{concept}.last_score must be null or 0..8")
        hint = record.get("hint_level")
        if hint is not None and (not isinstance(hint, int) or not 0 <= hint <= 4):
            fail(errors, f"mastery.{concept}.hint_level must be null or 0..4")

    for key in ("weak_points", "review_queue", "application_queue"):
        for index, item in enumerate(data[key]):
            if not isinstance(item, dict):
                fail(errors, f"{key}[{index}] must be an object")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="state.json file or course directory")
    args = parser.parse_args()

    path = Path(args.path).expanduser()
    if path.is_dir():
        path = path / "state.json"
    if not path.is_file():
        print(f"ERROR: state file not found: {path}", file=sys.stderr)
        return 2

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: valid AI Tutor v4 state: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate and append one assessment JSON object to assessments.jsonl."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


STATUSES = {"introduced", "assisted", "provisional", "retained", "transferred", "mastered"}


def validate(entry: object) -> list[str]:
    if not isinstance(entry, dict):
        return ["entry must be a JSON object"]
    errors: list[str] = []
    for key in ("timestamp", "concept", "status_after", "evidence", "next_action"):
        if not isinstance(entry.get(key), str) or not entry[key].strip():
            errors.append(f"{key} must be a non-empty string")
    if entry.get("status_after") not in STATUSES:
        errors.append("status_after is invalid")
    scores = entry.get("scores")
    if not isinstance(scores, dict):
        errors.append("scores must be an object")
    else:
        for key in ("accuracy", "reasoning", "transfer", "independence"):
            value = scores.get(key)
            if not isinstance(value, int) or not 0 <= value <= 2:
                errors.append(f"scores.{key} must be an integer from 0 to 2")
    hint = entry.get("hint_level")
    if not isinstance(hint, int) or not 0 <= hint <= 4:
        errors.append("hint_level must be an integer from 0 to 4")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="assessments.jsonl file or course directory")
    parser.add_argument("--entry", help="assessment JSON; read stdin when omitted")
    args = parser.parse_args()

    target = Path(args.path).expanduser()
    if target.is_dir() or target.suffix != ".jsonl":
        target = target / "assessments.jsonl"

    raw = args.entry if args.entry is not None else sys.stdin.read()
    try:
        entry = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON entry: {exc}", file=sys.stderr)
        return 2

    errors = validate(entry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    target.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    print(f"OK: appended assessment: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

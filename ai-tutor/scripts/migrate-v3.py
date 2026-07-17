#!/usr/bin/env python3
"""Create a non-destructive AI Tutor v4 preview from a legacy v3 course directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            return title.split("·", 1)[0].strip() or fallback
    return fallback


def extract_value(text: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}[：:]\s*([^\n｜|]+)", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def section_lines(text: str, heading_pattern: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.search(heading_pattern, line):
            start = index + 1
            break
    if start is None:
        return []
    result: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        result.append(line)
    return result


def extract_actions(text: str) -> list[str]:
    actions: list[str] = []
    for line in section_lines(text, r"续学.*3 件事|下次续学"):
        match = re.match(r"\s*(?:\d+[.)]|[-*])\s+(.+)", line)
        if match and "[" not in match.group(1):
            actions.append(match.group(1).strip())
    if not actions:
        value = extract_value(text, "下一次从这里开始")
        if value:
            actions.append(value)
    return actions[:3]


def extract_mastery(text: str) -> dict[str, dict[str, object]]:
    mastery: dict[str, dict[str, object]] = {}
    for line in section_lines(text, r"单元记录"):
        if not line.lstrip().startswith("|") or "---" in line or "单元" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not cells[0]:
            continue
        raw_status = " ".join(cells[2:])
        if "已巩固" in raw_status:
            status = "retained"
        elif "✅" in raw_status or "掌握" in raw_status or "完成" in raw_status:
            status = "provisional"
        elif "⚠" in raw_status or "部分" in raw_status:
            status = "assisted"
        else:
            status = "introduced"
        base = re.sub(r"[^a-z0-9]+", "-", cells[0].lower()).strip("-") or f"legacy-{len(mastery)+1}"
        key = base
        suffix = 2
        while key in mastery:
            key = f"{base}-{suffix}"
            suffix += 1
        mastery[key] = {
            "status": status,
            "last_score": None,
            "hint_level": None,
            "evidence": f"Migrated from v3 unit row: {' | '.join(cells)}",
            "updated_at": "",
        }
    return mastery


def stable_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if slug:
        return slug
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]
    return f"topic-{digest}"


def write_progress(source_text: str, output: Path) -> None:
    banner = (
        "<!-- AI Tutor v4 migration preview. The original v3 directory remains unchanged. -->\n"
        "<!-- Review state.json before adopting this preview. -->\n\n"
    )
    output.write_text(banner + source_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("legacy_dir", help="legacy v3 topic directory")
    parser.add_argument("--output", help="preview directory; defaults to <legacy>-v4-preview")
    args = parser.parse_args()

    legacy = Path(args.legacy_dir).expanduser().resolve()
    progress = legacy / "progress.md"
    if not legacy.is_dir() or not progress.is_file():
        print("ERROR: legacy directory must contain progress.md", file=sys.stderr)
        return 2

    output = Path(args.output).expanduser().resolve() if args.output else legacy.with_name(legacy.name + "-v4-preview")
    if output.exists():
        print(f"ERROR: output already exists; refusing to overwrite: {output}", file=sys.stderr)
        return 2

    text = progress.read_text(encoding="utf-8")
    title = first_heading(text, legacy.name)
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    actions = extract_actions(text)
    units = sorted([*legacy.glob("unit-*.md"), *legacy.glob("review-*.md")])
    profile_candidates = [legacy / "user-profile.md", legacy.parent / "user-profile.md"]
    profile = next((path for path in profile_candidates if path.is_file()), None)

    state = {
        "schema_version": 1,
        "skill_version": "4.0.0",
        "created_at": now,
        "updated_at": now,
        "recovered": True,
        "topic": {"title": title, "slug": stable_slug(legacy.name), "scope": "Migrated from AI Tutor v3"},
        "goal": {
            "purpose": extract_value(text, "学习目的"),
            "observable_outcome": "",
            "success_criteria": [],
            "time_constraints": "",
        },
        "mode": "review",
        "current_state": "paused",
        "current_unit": f"units/{units[-1].name}" if units else None,
        "next_actions": actions or ["Review migrated state and choose the next learning action"],
        "learner": {"prior_knowledge": "unknown", "notes": []},
        "curriculum": {
            "core_units": [f"units/{path.name}" for path in units],
            "optional_units": [],
            "prerequisites": [],
        },
        "mastery": extract_mastery(text),
        "weak_points": [],
        "review_queue": [],
        "application_queue": [],
        "session": {"last_session_file": "", "last_assessment_at": ""},
    }

    output.mkdir(parents=True)
    (output / "sessions").mkdir()
    if units:
        (output / "units").mkdir()
        for unit in units:
            shutil.copy2(unit, output / "units" / unit.name)
    if profile:
        shutil.copy2(profile, output / "learner-profile.md")
    (output / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_progress(text, output / "progress.md")
    migration = {
        "source": str(legacy),
        "created_at": now,
        "source_files_preserved": True,
        "detected_units": len(units),
        "copied_units": len(units),
        "detected_profile": str(profile) if profile else None,
        "copied_profile": "learner-profile.md" if profile else None,
        "manual_review_required": [
            "observable learning outcome and success criteria",
            "weak points and application intentions",
            "mastery evidence inferred from legacy status labels",
        ],
    }
    (output / "migration.json").write_text(json.dumps(migration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"OK: created non-destructive migration preview: {output}")
    print(f"Detected {len(units)} unit files; original directory was not changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

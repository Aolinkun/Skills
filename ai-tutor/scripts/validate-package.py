#!/usr/bin/env python3
"""Validate the AI Tutor v4 skill package without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/socratic-questioning.md",
    "references/teaching-patterns.md",
    "references/assessment-and-review.md",
    "references/difficulty-levels.md",
    "references/state-and-files.md",
    "references/theory.md",
    "assets/templates/state.json",
    "assets/templates/progress.md",
    "assets/templates/session.md",
    "assets/templates/curriculum.md",
    "assets/templates/summary.md",
    "scripts/validate-package.py",
    "scripts/validate-state.py",
    "scripts/migrate-v3.py",
    "scripts/append-assessment.py",
    "tests/eval-cases.json",
]
FORBIDDEN_NAMES = {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=Path(__file__).resolve().parent.parent,
        help="AI Tutor package directory (defaults to the package containing this script)",
    )
    parser.add_argument(
        "--allow-grok-frontmatter",
        action="store_true",
        help="accept and require Grok's user_invocable: true frontmatter field",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) >= 500:
            errors.append(f"SKILL.md must stay under 500 lines; found {len(lines)}")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append("SKILL.md frontmatter is missing or malformed")
        else:
            frontmatter = match.group(1)
            if not re.search(r"^name:\s*ai-tutor\s*$", frontmatter, re.MULTILINE):
                errors.append("frontmatter name must be ai-tutor")
            if not re.search(r"^description:\s*>?\s*$", frontmatter, re.MULTILINE):
                errors.append("frontmatter description is missing")
            top_level_keys = re.findall(r"^([a-zA-Z0-9_-]+):", frontmatter, re.MULTILINE)
            expected_keys = {"name", "description"}
            if args.allow_grok_frontmatter:
                expected_keys.add("user_invocable")
                if not re.search(r"^user_invocable:\s*true\s*$", frontmatter, re.MULTILINE):
                    errors.append("Grok package frontmatter must contain user_invocable: true")
            if set(top_level_keys) != expected_keys:
                allowed = ", ".join(sorted(expected_keys))
                errors.append(f"frontmatter may only contain {allowed}; found {top_level_keys}")
        if "# Version: v4.0.0" not in text:
            errors.append("SKILL.md version marker must be v4.0.0")

        references = set(re.findall(r"(?<![A-Za-z0-9_.-])((?:references|assets|scripts|tests)/[A-Za-z0-9_.\-/]+)", text))
        for relative in references:
            clean = relative.rstrip(".,;:)")
            if not (root / clean).exists():
                errors.append(f"SKILL.md references missing path: {clean}")

    if root.name != "ai-tutor":
        errors.append(f"skill directory must be named ai-tutor; found {root.name}")

    for path in root.rglob("*"):
        if path.is_file() and path.name in FORBIDDEN_NAMES:
            errors.append(f"extraneous documentation file: {path.relative_to(root)}")

    try:
        state = json.loads((root / "assets/templates/state.json").read_text(encoding="utf-8"))
        if state.get("skill_version") != "4.0.0":
            errors.append("state template skill_version must be 4.0.0")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid state template JSON: {exc}")

    try:
        cases = json.loads((root / "tests/eval-cases.json").read_text(encoding="utf-8"))
        if not isinstance(cases, list) or len(cases) < 20:
            errors.append("tests/eval-cases.json must contain at least 20 cases")
        else:
            seen: set[str] = set()
            for index, case in enumerate(cases):
                if not isinstance(case, dict):
                    errors.append(f"eval case {index} must be an object")
                    continue
                for key in ("id", "prompt", "expected_mode", "must", "must_not"):
                    if key not in case:
                        errors.append(f"eval case {index} missing {key}")
                case_id = case.get("id")
                if case_id in seen:
                    errors.append(f"duplicate eval case id: {case_id}")
                seen.add(case_id)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid eval cases JSON: {exc}")

    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.is_file():
        metadata = openai_yaml.read_text(encoding="utf-8")
        for key in ("display_name:", "short_description:", "default_prompt:", "$ai-tutor"):
            if key not in metadata:
                errors.append(f"agents/openai.yaml missing {key}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: valid AI Tutor v4 package: {root}")
    print(f"SKILL.md lines: {len((root / 'SKILL.md').read_text(encoding='utf-8').splitlines())}")
    print(f"Evaluation cases: {len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

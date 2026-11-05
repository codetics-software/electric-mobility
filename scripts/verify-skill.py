#!/usr/bin/env python3
"""Verify the skill is self-contained, safe to install, and well formed.

Uses only the standard library, and makes no network calls. It simulates an install
by copying the skill folder alone to a temporary directory, the way skill installers
do, then checks that everything the skill refers to is still there.

Usage: python3 scripts/verify-skill.py
"""

import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "electric-mobility"

ALLOWED_SUFFIXES = {".md"}
IGNORED_NAMES = {".DS_Store"}
# Installers skip these names, so the skill must not depend on them.
INSTALLER_EXCLUDED = {"metadata.json", ".git", "__pycache__", "__pypackages__"}
MAX_DESCRIPTION = 1024
# Context budgets. The description loads in every session, SKILL.md on every activation.
# Tokens are estimated at 4 characters each, so treat these as guide rails.
BUDGET_DESCRIPTION_CHARS = 450
BUDGET_SKILL_TOKENS = 3500
BUDGET_SKILL_LINES = 200
BUDGET_REFERENCE_TOKENS = 4500
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\]\(([^)\s]+)\)")
# File paths written in backticks in SKILL.md, for example `references/rules/go.md`.
CODE_PATH_PATTERN = re.compile(r"`((?:references|examples)/[^`*<>\s]+\.md)`")
FENCE_PATTERN = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)

HIDDEN_CHARACTERS = re.compile(
    "["
    "­"  # soft hyphen
    "​‌‎‏"  # zero-width and directional marks
    "‪-‮"  # bidirectional embedding and override
    "⁠-⁤"  # word joiner and invisible operators
    "⁦-⁩"  # bidirectional isolates
    "﻿"  # byte order mark
    "\U000e0000-\U000e007f"  # tag characters, which can hide text
    "]"
)

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "Stripe live key": re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}\b"),
    "Stripe webhook secret": re.compile(r"\bwhsec_[A-Za-z0-9]{24,}\b"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "JSON Web Token": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
}


def frontmatter(text):
    """Return simple top-level frontmatter fields, including folded descriptions."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    fields = {}
    key = None
    for line in match.group(1).split("\n"):
        field = re.match(r"^([a-z-]+):\s*(.*)$", line)
        if field:
            key = field.group(1)
            value = field.group(2).strip()
            fields[key] = "" if value in (">", "|", ">-", "|-") else value
        elif key and line.startswith(" "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def check_frontmatter(errors):
    skill_file = SKILL / "SKILL.md"
    if not skill_file.is_file():
        errors.append(f"missing {skill_file.relative_to(REPO)}")
        return
    fields = frontmatter(skill_file.read_text(encoding="utf-8"))
    if fields is None:
        errors.append("SKILL.md has no frontmatter")
        return
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not NAME_PATTERN.match(name) or len(name) > 64:
        errors.append(f"invalid skill name: {name!r}")
    if name != SKILL.name:
        errors.append(f"skill name {name!r} does not match folder {SKILL.name!r}")
    if not description:
        errors.append("description is empty")
    if len(description) > MAX_DESCRIPTION:
        errors.append(f"description is {len(description)} characters; the limit is {MAX_DESCRIPTION}")
    if len(description) > BUDGET_DESCRIPTION_CHARS:
        errors.append(f"description is {len(description)} characters; the budget is {BUDGET_DESCRIPTION_CHARS}")


def estimate_tokens(text):
    return len(text) // 4


def check_budgets(errors):
    """Keep the always-loaded text small, so the skill cannot quietly grow back."""
    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    tokens = estimate_tokens(entry)
    lines = entry.count("\n")
    if tokens > BUDGET_SKILL_TOKENS:
        errors.append(f"SKILL.md is about {tokens} tokens; the budget is {BUDGET_SKILL_TOKENS}. Move detail to references")
    if lines > BUDGET_SKILL_LINES:
        errors.append(f"SKILL.md is {lines} lines; the budget is {BUDGET_SKILL_LINES}. Move detail to references")
    for path in SKILL.rglob("*.md"):
        if path.name == "SKILL.md":
            continue
        tokens = estimate_tokens(path.read_text(encoding="utf-8"))
        if tokens > BUDGET_REFERENCE_TOKENS:
            errors.append(f"{path.relative_to(REPO)} is about {tokens} tokens; the budget is {BUDGET_REFERENCE_TOKENS}. Split it")
    return estimate_tokens(entry), lines


def payload_files(root):
    return [p for p in root.rglob("*") if p.name not in IGNORED_NAMES]


def check_payload(errors):
    for path in payload_files(SKILL):
        relative = path.relative_to(REPO)
        if path.is_symlink():
            errors.append(f"symlink in skill: {relative}")
            continue
        if path.name in INSTALLER_EXCLUDED:
            errors.append(f"installers skip this name: {relative}")
        if not path.is_file():
            continue
        if path.suffix not in ALLOWED_SUFFIXES:
            errors.append(f"non-Markdown file in skill: {relative}")
        if path.stat().st_mode & 0o111:
            errors.append(f"executable file in skill: {relative}")


def check_content(errors):
    for path in SKILL.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(REPO)
        for line_number, line in enumerate(text.splitlines(), 1):
            hidden = HIDDEN_CHARACTERS.search(line)
            if hidden:
                errors.append(f"hidden character U+{ord(hidden.group()):04X}: {relative}:{line_number}")
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    errors.append(f"possible {label}: {relative}:{line_number}")


def is_external(target):
    return re.match(r"^[a-z][a-z0-9+.-]*:", target) is not None or target.startswith("#")


def check_references(root, errors, label):
    """Every relative link must resolve inside the given skill root."""
    checked = 0
    resolved_root = root.resolve()
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        for target in LINK_PATTERN.findall(FENCE_PATTERN.sub("", text)):
            if is_external(target):
                continue
            checked += 1
            clean = target.split("#", 1)[0]
            resolved = (path.parent / clean).resolve()
            if resolved_root not in resolved.parents and resolved != resolved_root:
                errors.append(f"{label}: link leaves the skill folder: {relative} -> {target}")
            elif not resolved.exists():
                errors.append(f"{label}: broken link: {relative} -> {target}")
    entry = root / "SKILL.md"
    if entry.is_file():
        for target in CODE_PATH_PATTERN.findall(entry.read_text(encoding="utf-8")):
            checked += 1
            if not (root / target).is_file():
                errors.append(f"{label}: SKILL.md names a missing file: {target}")
    return checked


def check_routed(errors):
    """Each top-level guide must be reachable from SKILL.md, or agents will never load it."""
    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    references = SKILL / "references"
    for path in sorted(references.glob("*.md")) + sorted((references / "security").glob("*.md")):
        relative = path.relative_to(SKILL).as_posix()
        if relative not in entry:
            errors.append(f"SKILL.md does not route to {relative}")
    # These folders are routed by name, for example `references/rules/<language>.md`.
    for folder in ("rules", "ocpi", "ocpp"):
        for path in sorted((references / folder).glob("*.md")):
            versioned = folder == "ocpp" and path.stem.startswith("ocpp-")
            if not versioned and path.stem != "README" and path.stem not in entry:
                errors.append(f"SKILL.md does not route to {path.relative_to(SKILL).as_posix()}")


def simulate_install(errors):
    """Copy only the skill folder, as an installer does, then recheck every reference."""
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / "installed" / SKILL.name
        shutil.copytree(
            SKILL,
            target,
            ignore=lambda _, names: [n for n in names if n in INSTALLER_EXCLUDED],
        )
        checked = check_references(target, errors, "after install")
        files = sum(1 for p in target.rglob("*") if p.is_file())
    return checked, files


def main():
    errors = []
    check_frontmatter(errors)
    skill_tokens, skill_lines = check_budgets(errors)
    check_payload(errors)
    check_content(errors)
    checked = check_references(SKILL, errors, "source")
    check_routed(errors)
    installed_checked, installed_files = simulate_install(errors)

    if errors:
        print(f"FAILED: {len(errors)} problem(s)")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: SKILL.md is about {skill_tokens} tokens and {skill_lines} lines")
    print(f"OK: {checked} references checked in the source")
    print(f"OK: simulated install has {installed_files} files, and all {installed_checked} references resolve")
    print("Next: read the changes yourself. This script cannot judge whether the text is safe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

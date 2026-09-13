#!/usr/bin/env python3
"""Validate the structure and safety boundaries of the portfolio demo."""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOTS = {"docs", "examples"}
REQUIRED = ("type", "status", "date", "classification", "owner_role", "description")
ALLOWED_STATUS = {"proposed", "approved", "retired"}
ALLOWED_CLASSIFICATION = {"public-demo", "synthetic"}
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".py", ".txt", ".csv", ".json"}

FORBIDDEN = (
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"), "API key"),
    (re.compile(r"send\.bitwarden\.com/", re.I), "secret sharing link"),
    (re.compile(r"\brec[A-Za-z0-9]{14}\b"), "record identifier"),
)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PRIVATE_URL = re.compile(r"https?://(?:localhost|[^/\s]+\.(?:local|internal))(?:/[^\s]*)?", re.I)


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "frontmatter missing"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, "frontmatter closing marker missing"
    data: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z_][a-z0-9_]*):\s*(.*?)\s*", raw)
        if not match:
            return None, f"unsupported frontmatter line: {raw!r}"
        key, value = match.groups()
        data[key] = value.strip("\"'")
    return data, None


def content_markdown(root: Path) -> list[Path]:
    found: list[Path] = []
    for base in CONTENT_ROOTS:
        path = root / base
        if path.exists():
            found.extend(sorted(path.rglob("*.md")))
    return found


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    for path in content_markdown(root):
        rel = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{rel}: file is not UTF-8")
            continue
        metadata, problem = parse_frontmatter(text)
        if problem:
            errors.append(f"{rel}: {problem}")
            continue
        assert metadata is not None
        for field in REQUIRED:
            if not metadata.get(field):
                errors.append(f"{rel}: missing metadata field {field}")
        if metadata.get("status") not in ALLOWED_STATUS:
            errors.append(f"{rel}: invalid status {metadata.get('status')!r}")
        if metadata.get("classification") not in ALLOWED_CLASSIFICATION:
            errors.append(f"{rel}: invalid classification {metadata.get('classification')!r}")
        date = metadata.get("date", "")
        try:
            dt.date.fromisoformat(date)
        except ValueError:
            errors.append(f"{rel}: invalid ISO date {date!r}")

    for path in sorted(root.rglob("*")):
        if path.is_dir() or ".git" in path.parts or path.suffix not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{rel}: text-like file is not UTF-8")
            continue
        for pattern, label in FORBIDDEN:
            if pattern.search(text):
                errors.append(f"{rel}: forbidden pattern detected ({label})")
        if EMAIL.search(text):
            errors.append(f"{rel}: email address detected")
        if PRIVATE_URL.search(text):
            errors.append(f"{rel}: private/internal URL detected")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed: {len(errors)} issue(s).")
        return 1
    print(f"Validation passed: {len(content_markdown(ROOT))} governed Markdown document(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())


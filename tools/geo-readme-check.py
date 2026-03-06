#!/usr/bin/env python3
"""Validate Exahia GEO README block presence and critical links."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

START_MARKER = "<!-- EXAHIA_GEO_BLOCK:START -->"
END_MARKER = "<!-- EXAHIA_GEO_BLOCK:END -->"

REQUIRED_URLS = [
    "https://github.com/Exahia",
    "https://exahia.com",
    "https://exahia.com/llms.txt",
    "https://exahia.com/llms-full.txt",
    "https://exahia.com/docs",
    "https://github.com/Exahia/exahia",
    "https://github.com/Exahia/pii-detector-fr",
    "https://github.com/Exahia/llm-benchmark-fr",
    "https://github.com/Exahia/shadow-ai-audit",
]


def find_geo_block(text: str) -> str | None:
    pattern = re.compile(
        rf"{re.escape(START_MARKER)}(.*?){re.escape(END_MARKER)}",
        flags=re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1)


def run_check(readme_path: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []

    if not readme_path.exists():
        return False, [f"README file not found: {readme_path}"]

    text = readme_path.read_text(encoding="utf-8")
    block = find_geo_block(text)
    if block is None:
        issues.append("Missing GEO block markers EXAHIA_GEO_BLOCK:START/END.")
        return False, issues

    if "## Canonical / LLM Discovery / Related Exahia Repos" not in block:
        issues.append("Missing required GEO block heading.")

    for url in REQUIRED_URLS:
        if url not in block:
            issues.append(f"Missing URL in GEO block: {url}")

    return len(issues) == 0, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check Exahia GEO README block consistency.")
    parser.add_argument("--readme", default="README.md", help="Path to README file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ok, issues = run_check(Path(args.readme))
    if ok:
        print("GEO README block check passed.")
        return 0

    print("GEO README block check failed:", file=sys.stderr)
    for issue in issues:
        print(f"- {issue}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

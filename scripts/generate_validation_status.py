#!/usr/bin/env python3
"""Generate tutorial validation status dashboard from frontmatter metadata.

Scans all tutorial markdown files for validation frontmatter and generates
a dashboard page showing which tutorials have been tested, when, and with
which tools.

Usage:
    python3 scripts/generate_validation_status.py
    python3 scripts/generate_validation_status.py --docs-dir docs --output docs/reference/validation-status.md
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

STALENESS_DAYS = 90
TUTORIAL_GLOB = "language-guides/*/0*.md"

ICON_PASS = "✅ Pass"
ICON_FAIL = "❌ Fail"
ICON_STALE = "⚠️ Stale"
ICON_NOT_TESTED = "➖ Not Tested"
ICON_NO_DATA = "➖ No Data"


def parse_frontmatter(filepath: Path) -> dict[str, Any] | None:
    """Extract YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def extract_tutorial_info(filepath: Path, docs_dir: Path) -> dict[str, Any]:
    rel = filepath.relative_to(docs_dir)
    parts = rel.parts
    language = parts[1] if len(parts) > 1 else "unknown"
    filename = filepath.stem

    frontmatter = parse_frontmatter(filepath)
    validation = {}
    if frontmatter and isinstance(frontmatter, dict):
        validation = frontmatter.get("validation", {}) or {}

    return {
        "filepath": filepath,
        "rel_path": str(rel),
        "language": language,
        "filename": filename,
        "title": filename.replace("-", " ").title(),
        "validation": validation,
    }


def get_method_status(
    method_data: dict[str, Any] | None, today: date
) -> tuple[str, str | None]:
    if not method_data or not isinstance(method_data, dict):
        return ICON_NO_DATA, None

    result = method_data.get("result", "not_tested")
    last_tested = method_data.get("last_tested")

    if result == "not_tested" or last_tested is None:
        return ICON_NOT_TESTED, None

    if isinstance(last_tested, date):
        test_date = last_tested
    else:
        try:
            test_date = date.fromisoformat(str(last_tested))
        except (ValueError, TypeError):
            return ICON_NO_DATA, str(last_tested)

    date_str = test_date.isoformat()
    age = (today - test_date).days

    if result == "fail":
        return ICON_FAIL, date_str
    if age > STALENESS_DAYS:
        return ICON_STALE, date_str
    return ICON_PASS, date_str


def generate_dashboard(tutorials: list[dict[str, Any]], today: date) -> str:
    methods = ("aws_cli", "cloudformation")

    total = len(tutorials)
    validated = 0
    stale = 0
    failed = 0
    not_tested = 0

    for tutorial in tutorials:
        validation = tutorial["validation"]
        has_any_pass = False
        has_stale = False
        has_fail = False

        for method in methods:
            method_data = validation.get(method)
            status, _ = get_method_status(method_data, today)
            if status == ICON_PASS:
                has_any_pass = True
            elif status == ICON_STALE:
                has_stale = True
            elif status == ICON_FAIL:
                has_fail = True

        if has_fail:
            failed += 1
        elif has_stale:
            stale += 1
        elif has_any_pass:
            validated += 1
        else:
            not_tested += 1

    by_language: dict[str, list[dict[str, Any]]] = {}
    for tutorial in tutorials:
        language = tutorial["language"]
        by_language.setdefault(language, []).append(tutorial)

    lines: list[str] = []
    lines.append("# Tutorial Validation Status")
    lines.append("")
    lines.append(
        "This page tracks which tutorials have been validated against real AWS deployments. "
        "Each tutorial can be tested via **aws-cli** (manual CLI commands) or **CloudFormation** (infrastructure as code). "
        f"Tutorials not tested within {STALENESS_DAYS} days are marked as stale."
    )
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"*Generated: {today.isoformat()}*")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Total tutorials | {total} |")
    lines.append(f"| ✅ Validated | {validated} |")
    lines.append(f"| ⚠️ Stale (>{STALENESS_DAYS} days) | {stale} |")
    lines.append(f"| ❌ Failed | {failed} |")
    lines.append(f"| ➖ Not tested | {not_tested} |")
    lines.append("")

    lines.append("```mermaid")
    lines.append('pie title Tutorial Validation Status')
    if validated > 0:
        lines.append(f'    "Validated" : {validated}')
    if stale > 0:
        lines.append(f'    "Stale" : {stale}')
    if failed > 0:
        lines.append(f'    "Failed" : {failed}')
    if not_tested > 0:
        lines.append(f'    "Not Tested" : {not_tested}')
    lines.append("```")
    lines.append("")

    lines.append("## Validation Matrix")
    lines.append("")

    for language in sorted(by_language.keys()):
        language_tutorials = by_language[language]
        language_display = language.replace("-", " ").title()
        if language == "nodejs":
            language_display = "Node.js"
        elif language == "dotnet":
            language_display = ".NET"

        lines.append(f"### {language_display}")
        lines.append("")
        lines.append(
            "| Tutorial | aws-cli | CloudFormation | Last Tested | Status |"
        )
        lines.append("|---|---|---|---|---|")

        language_tutorials.sort(key=lambda tutorial: tutorial["filename"])

        for tutorial in language_tutorials:
            validation = tutorial["validation"]
            aws_cli_data = validation.get("aws_cli")
            cloudformation_data = validation.get("cloudformation")

            aws_cli_status, aws_cli_date = get_method_status(aws_cli_data, today)
            cloudformation_status, cloudformation_date = get_method_status(
                cloudformation_data, today
            )

            dates = [d for d in [aws_cli_date, cloudformation_date] if d]
            last_tested = max(dates) if dates else "—"

            statuses = [aws_cli_status, cloudformation_status]
            if ICON_FAIL in statuses:
                overall = ICON_FAIL
            elif ICON_STALE in statuses:
                overall = ICON_STALE
            elif ICON_PASS in statuses:
                overall = ICON_PASS
            else:
                overall = ICON_NOT_TESTED

            tutorial_link = f"[{tutorial['title']}](../{tutorial['rel_path']})"

            lines.append(
                f"| {tutorial_link} | {aws_cli_status} | {cloudformation_status} | {last_tested} | {overall} |"
            )

        lines.append("")

    lines.append("## How to Update")
    lines.append("")
    lines.append(
        "To mark a tutorial as validated, add a `validation` block to its YAML frontmatter:"
    )
    lines.append("")
    lines.append("```yaml")
    lines.append("---")
    lines.append("hide:")
    lines.append("  - toc")
    lines.append("validation:")
    lines.append("  aws_cli:")
    lines.append("    last_tested: 2026-04-09")
    lines.append('    cli_version: "2.83.0"')
    lines.append("    result: pass")
    lines.append("  cloudformation:")
    lines.append("    last_tested: null")
    lines.append("    result: not_tested")
    lines.append("---")
    lines.append("```")
    lines.append("")
    lines.append("Then regenerate this page:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/generate_validation_status.py")
    lines.append("```")
    lines.append("")
    lines.append("!!! info \"Validation fields\"")
    lines.append("    - `result`: `pass`, `fail`, or `not_tested`")
    lines.append("    - `last_tested`: ISO date (YYYY-MM-DD) or `null`")
    lines.append("    - `cli_version`: AWS CLI version used")
    lines.append(
        f"    - Tutorials older than {STALENESS_DAYS} days are flagged as **stale**"
    )
    lines.append("")

    lines.append("## See Also")
    lines.append("")
    lines.append("- [Language Guides](../language-guides/index.md)")
    lines.append("- [EB CLI Cheatsheet](eb-cli-cheatsheet.md)")
    lines.append("- [Platform Limits](platform-limits.md)")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate tutorial validation status dashboard"
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path("docs"),
        help="Path to docs directory (default: docs)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/reference/validation-status.md"),
        help="Output file path (default: docs/reference/validation-status.md)",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    docs_dir = project_root / args.docs_dir
    output_path = project_root / args.output

    if not docs_dir.exists():
        print(f"Error: docs directory not found: {docs_dir}")
        raise SystemExit(1)

    tutorial_files = sorted(docs_dir.glob(TUTORIAL_GLOB))

    tutorial_files = [f for f in tutorial_files if f.name != "index.md"]

    tutorials = [extract_tutorial_info(f, docs_dir) for f in tutorial_files]

    today = date.today()
    dashboard = generate_dashboard(tutorials, today)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dashboard, encoding="utf-8")

    validated = sum(
        1
        for tutorial in tutorials
        if any(
            get_method_status(tutorial["validation"].get(method), today)[0] == ICON_PASS
            for method in ("aws_cli", "cloudformation")
        )
    )
    print(
        f"Scanned {len(tutorials)} tutorials, "
        f"{validated} validated, "
        f"generated {output_path}"
    )


if __name__ == "__main__":
    main()

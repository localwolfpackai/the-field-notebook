#!/usr/bin/env python3
"""Lock the health dashboard to notebook tokens and the one-word pill rule.

Daily facts may change. The September 2026 story must not come back, and
the page must not invent a second red or a fixed 240px card track.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "smart-project-analysis" / "health-dashboard.html"
NOTES = ROOT / "smart-project-analysis" / "ANALYSIS.md"
SKILL = ROOT / "SKILL.md"

STALE = (
    "0 open PRs",
    "0 open pull",
    "no automated CI",
    "No `.github/workflows`",
    "not yet under version control",
    "July 30, 2026",
)

STYLE_BANS = (
    "minmax(240px",
    "minmax(280px",
    "--red:",
    "--red-wash:",
)

PILL = re.compile(r'<span class="pill[^"]*">([^<]*)</span>')
HEX = re.compile(r"#[0-9A-Fa-f]{3,8}\b")


def fail(errors: list[str]) -> None:
    for item in errors:
        print(f"dashboard: {item}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    errors: list[str] = []
    html = DASH.read_text(encoding="utf-8")
    notes = NOTES.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")

    style = html.split("</style>", 1)[0]
    for phrase in STYLE_BANS:
        if phrase in style:
            errors.append(f"dashboard CSS still has {phrase!r}")

    for label, text in (("dashboard", html), ("notes", notes)):
        for phrase in STALE:
            if phrase in text:
                errors.append(f"{label} still says {phrase!r}")
        hex_hit = HEX.search(text)
        if hex_hit:
            errors.append(f"{label} has a hex color {hex_hit.group(0)}")

    for match in PILL.finditer(html):
        label = " ".join(match.group(1).split())
        if " " in label:
            errors.append(f"pill holds more than one word: {label!r}")

    required = (
        "--line:",
        "minmax(min(100%, 15rem), 1fr)",
        ":focus-visible",
        "background-attachment: scroll",
        "max-width: 760px",
        "var(--margin)",
    )
    for token in required:
        if token not in html:
            errors.append(f"missing {token}")

    if re.search(r"aren'?t pushing to git|arent pushing to git", skill, re.I):
        errors.append("SKILL.md still says the repo is not on git")

    if errors:
        fail(errors)
    print("dashboard ok")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Catch layout CSS the browser silently throws away.

A focus ring that names --accent only paints if that page defines --accent.
A phone rule written as `@container, @media` is invalid, so the browser
drops it and the two-column layout stays on a phone.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)
COMMENT = re.compile(r"/\*.*?\*/", re.S)
BAD_QUERY = re.compile(r"@container\s*,\s*@media|@media\s*,\s*@container")
FOCUS_ACCENT = re.compile(r":focus-visible\s*\{[^}]*var\(\s*--accent\s*\)", re.S)
DEFINES_ACCENT = re.compile(r"--accent\s*:")


def main() -> int:
    errors = []
    html_files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)

    for path in html_files:
        text = path.read_text()
        rel = path.relative_to(ROOT)
        css = COMMENT.sub("", "\n".join(STYLE.findall(text)))
        if BAD_QUERY.search(css):
            errors.append(
                f"{rel}: phone rule is `@container, @media`, which browsers drop"
            )
        if FOCUS_ACCENT.search(css) and not DEFINES_ACCENT.search(css):
            errors.append(
                f"{rel}: focus ring uses var(--accent), but --accent is not defined"
            )

    if errors:
        print("\n".join(errors))
        return 1

    print(f"layout sanity ok ({len(html_files)} html files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

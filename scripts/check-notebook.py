#!/usr/bin/env python3
"""Catch the UI drifts this notebook's agents keep reintroducing.

Zero dependencies on purpose: the site has no build step, and this check
should run the same way in GitHub Actions and on a laptop.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

FOCUS = ":focus-visible"
PILL = re.compile(r'<span class="pill[^"]*">([^<]*)</span>')


def main() -> int:
    errors = []
    html_files = sorted(ROOT.rglob("*.html"))

    for path in html_files:
        text = path.read_text()
        rel = path.relative_to(ROOT)
        if "<style" in text and FOCUS not in text:
            errors.append(f"{rel}: missing :focus-visible")
        if re.search(r"\.toc ol\s*\{[^}]*gap:\s*0\.32rem", text):
            errors.append(f"{rel}: TOC list is still cramped at 0.32rem")
        if re.search(r"\.toc li\s*\{[^}]*1\.6rem", text):
            errors.append(f"{rel}: TOC numbers still use a 1.6rem column")

    index = (ROOT / "index.html").read_text()
    for match in PILL.finditer(index):
        label = match.group(1).strip()
        if re.search(r"\s", label):
            errors.append(f"index.html: pill has more than one word: {label!r}")

    if errors:
        print("\n".join(errors))
        return 1

    print(f"notebook check ok ({len(html_files)} html files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

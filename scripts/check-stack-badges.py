#!/usr/bin/env python3
"""Fail when stack badges drift back to hex colors or multi-word labels.

The notebook has no build step. This check is stdlib-only so it runs in
GitHub Actions and in a local terminal the same way.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOWED = {"ink", "accent", "sage", "amber", "violet", "margin"}
SPAN = re.compile(
    r'<span class="sbadge(?P<classes>[^"]*)">(?P<body>.*?)</span>',
    re.S,
)
TAG = re.compile(r"<[^>]+>")
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)
RULE = re.compile(r"\.sbadge\s*\{([^}]*)\}", re.S)
HEX = re.compile(r"#[0-9A-Fa-f]{3,8}")


def main() -> int:
    errors = []
    seen = 0

    for path in sorted(ROOT.rglob("*.html")):
        text = path.read_text()
        if 'class="sbadge' not in text:
            continue
        rel = path.relative_to(ROOT)
        seen += 1

        if 'style="--pill-c:#' in text:
            errors.append(f"{rel}: stack badge still sets --pill-c with a hex color")

        for match in SPAN.finditer(text):
            classes = match.group("classes").split()
            unknown = [c for c in classes if c not in ALLOWED]
            if unknown:
                errors.append(f"{rel}: unknown sbadge class {unknown!r}")
            if not classes:
                errors.append(f"{rel}: sbadge is missing a palette class")
            label = TAG.sub("", match.group("body"))
            label = label.replace("&amp;", "&").strip()
            if re.search(r"\s", label):
                errors.append(f"{rel}: stack badge has more than one word: {label!r}")

        css = "\n".join(STYLE.findall(text))
        rules = RULE.findall(css)
        if not rules:
            errors.append(f"{rel}: missing a .sbadge rule")
        for block in rules:
            if HEX.search(block) or "nowrap" in block:
                errors.append(f"{rel}: .sbadge CSS uses hex or nowrap")
                break

    if seen == 0:
        errors.append("no stack badges found")

    if errors:
        print("\n".join(errors))
        return 1

    print(f"stack badges ok ({seen} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

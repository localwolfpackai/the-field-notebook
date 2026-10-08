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
HEX_IN_CSS = re.compile(r"#[0-9A-Fa-f]{3,8}")
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)
PILL_FILES = (
    "index.html",
    "smart-project-analysis/health-dashboard.html",
    "ship-2026-07-25-launch/social-card.html",
)
BADGE_COLORS = {"ink", "accent", "sage", "amber", "violet", "margin"}
BADGE_SPAN = re.compile(
    r'<span class="sbadge(?P<classes>[^"]*)"(?P<rest>[^>]*)>(?P<body>.*?)</span>',
    re.S,
)
BADGE_TAG = re.compile(r"<[^>]+>")
BADGE_RULE = re.compile(r"\.sbadge\s*\{([^}]*)\}", re.S)


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

    for rel in PILL_FILES:
        text = (ROOT / rel).read_text()
        for match in PILL.finditer(text):
            label = match.group(1).strip()
            if re.search(r"\s", label):
                errors.append(f"{rel}: pill has more than one word: {label!r}")

    card = ROOT / "ship-2026-07-25-launch" / "social-card.html"
    css = "\n".join(STYLE.findall(card.read_text()))
    if HEX_IN_CSS.search(css):
        errors.append(
            "ship-2026-07-25-launch/social-card.html: launch card CSS still uses a hex color"
        )

    badge_pages = 0
    for path in html_files:
        text = path.read_text()
        if 'class="sbadge' not in text:
            continue
        rel = path.relative_to(ROOT)
        badge_pages += 1
        if 'style="--pill-c:#' in text:
            errors.append(f"{rel}: stack badge still sets --pill-c with a hex color")
        for match in BADGE_SPAN.finditer(text):
            rest = match.group("rest")
            if "style=" in rest or "--pill-c" in rest:
                errors.append(f"{rel}: stack badge uses an inline style")
            classes = match.group("classes").split()
            unknown = [c for c in classes if c not in BADGE_COLORS]
            if unknown:
                errors.append(f"{rel}: unknown sbadge class {unknown!r}")
            if not classes:
                errors.append(f"{rel}: sbadge is missing a palette class")
            label = BADGE_TAG.sub("", match.group("body"))
            label = label.replace("&amp;", "&").strip()
            if re.search(r"\s", label):
                errors.append(f"{rel}: stack badge has more than one word: {label!r}")
        rules = BADGE_RULE.findall("\n".join(STYLE.findall(text)))
        if not rules:
            errors.append(f"{rel}: missing a .sbadge rule")
        for block in rules:
            if HEX_IN_CSS.search(block) or "nowrap" in block:
                errors.append(f"{rel}: .sbadge CSS uses hex or nowrap")
                break
    if badge_pages == 0:
        errors.append("no stack badges found")

    if errors:
        print("\n".join(errors))
        return 1

    print(f"notebook check ok ({len(html_files)} html files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

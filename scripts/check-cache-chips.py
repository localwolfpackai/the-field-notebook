#!/usr/bin/env python3
"""Lock the title chips on the prompt-caching guide.

Other guides still use hex chips. This check stays on one page so a
pull request cannot quietly recolor the whole notebook.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = "2026-06/the-90-percent-off-dial-prompt-caching-2026-06-29.html"
HEX = re.compile(r"#[0-9A-Fa-f]{3,8}")
CHIP = re.compile(r'<span class="sbadge([^"]*)"[^>]*>(.*?)</span>', re.S)
RULE = re.compile(r"\.sbadge[^{]*\{[^}]*\}", re.S)
MEDIA = re.compile(r"@media \(max-width:\s*760px\)\s*\{")
WANTED = ("margin", "accent", "sage", "amber")


def media_760(text: str) -> str:
    match = MEDIA.search(text)
    if not match:
        return ""
    start = match.end() - 1
    depth = 0
    for index, char in enumerate(text[start:], start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return ""


def visible(fragment: str) -> str:
    return re.sub(r"<[^>]+>", "", fragment).strip()


def main() -> int:
    errors = []
    text = (ROOT / PAGE).read_text()

    if "--pill-c" in text:
        errors.append(f"{PAGE}: title chip still sets --pill-c")
    if "background-attachment: scroll" not in media_760(text):
        errors.append(f"{PAGE}: phone width still pins the ruled paper")
    if "flex-wrap: wrap" not in text:
        errors.append(f"{PAGE}: chip row does not wrap")
    if "--line:" not in text:
        errors.append(f"{PAGE}: --line is missing, so the chip border has no token")

    seen = []
    for match in CHIP.finditer(text):
        classes = match.group(1).split()
        raw = match.group(0)
        label = visible(match.group(2))
        seen.append(classes[0] if classes else "")
        if "style=" in raw:
            errors.append(f"{PAGE}: chip {label!r} still has an inline style")
        if re.search(r"\s", label):
            errors.append(f"{PAGE}: chip has more than one word: {label!r}")

    if seen != list(WANTED):
        errors.append(f"{PAGE}: chips should be {', '.join(WANTED)} (got {seen})")

    for rule in RULE.findall(text):
        if HEX.search(rule) or "--pill-c" in rule or "nowrap" in rule:
            errors.append(f"{PAGE}: .sbadge rule still has a hex color, --pill-c, or nowrap")
            break

    if errors:
        print("\n".join(errors))
        return 1

    print(f"title chips ok ({PAGE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

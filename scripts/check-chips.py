#!/usr/bin/env python3
"""Check the title chips (.sbadge) on every guide.

DONE lists the guides whose chips use the notebook color tokens, with the
chip colors in order. LEGACY lists the guides that still use hex chips.
Every other guide with chips must already follow the rules, so a new guide
cannot ship hex or multi-word chips.

To finish a guide, restyle its chips, then move its line from LEGACY to
DONE with its chip colors.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HEX = re.compile(r"#[0-9A-Fa-f]{3,8}")
CHIP = re.compile(r'<span class="sbadge([^"]*)"[^>]*>(.*?)</span>', re.S)
RULE = re.compile(r"\.sbadge[^{]*\{[^}]*\}", re.S)
MEDIA = re.compile(r"@media \(max-width:\s*760px\)\s*\{")

DONE = {
    "2026-06/cost-and-latency-two-dials-2026-06-25.html": (
        "margin", "accent", "sage", "violet",
    ),
    "2026-06/the-90-percent-off-dial-prompt-caching-2026-06-29.html": (
        "margin", "accent", "sage", "amber",
    ),
    "2026-06/ship-the-tokens-first-design-systems-2026-06-30.html": (
        "margin", "accent", "sage", "amber",
    ),
}

LEGACY = (
    "2026-06/grade-it-before-they-do-evals-2026-06-24.html",
    "2026-06/make-the-model-hand-you-json-2026-06-23.html",
    "2026-06/retrieval-without-the-hype-2026-06-26.html",
    "2026-06/same-prompt-two-souls-claude-vs-gemini-design-2026-06-27.html",
    "2026-06/show-the-model-a-picture-multimodal-2026-06-28.html",
    "2026-06/show-your-work-extended-thinking-2026-06-27.html",
    "2026-07/ship-it-to-the-world-deploy-your-ai-app-2026-07-01.html",
    "2026-07/the-answer-you-never-see-observability-2026-07-06.html",
    "2026-07/the-first-weird-input-prompt-injection-2026-07-05.html",
    "2026-07/the-prompt-is-the-product-version-your-prompt-2026-07-07.html",
    "2026-07/when-the-model-gets-a-verb-tool-use-2026-07-08.html",
)


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


def check_chips(page: str, text: str, errors: list) -> list:
    """Shared rules for any chip row. Returns the first class of each chip."""
    seen = []
    if "--pill-c" in text:
        errors.append(f"{page}: title chip still sets --pill-c")
    for match in CHIP.finditer(text):
        classes = match.group(1).split()
        label = visible(match.group(2))
        seen.append(classes[0] if classes else "")
        if "style=" in match.group(0):
            errors.append(f"{page}: chip {label!r} still has an inline style")
        if re.search(r"\s", label):
            errors.append(f"{page}: chip has more than one word: {label!r}")
    return seen


def check_done(page: str, text: str, wanted: tuple, errors: list) -> None:
    seen = check_chips(page, text, errors)
    if "background-attachment: scroll" not in media_760(text):
        errors.append(f"{page}: phone width still pins the ruled paper")
    if "flex-wrap: wrap" not in text:
        errors.append(f"{page}: chip row does not wrap")
    if "--line:" not in text:
        errors.append(f"{page}: --line is missing, so the chip border has no token")
    if seen != list(wanted):
        errors.append(f"{page}: chips should be {', '.join(wanted)} (got {seen})")
    for rule in RULE.findall(text):
        if HEX.search(rule) or "--pill-c" in rule or "nowrap" in rule:
            errors.append(
                f"{page}: .sbadge rule still has a hex color, --pill-c, or nowrap"
            )
            break


def main() -> int:
    errors = []

    for page in list(DONE) + list(LEGACY):
        if not (ROOT / page).is_file():
            errors.append(f"{page}: listed in check-chips.py but missing on disk")

    for page, wanted in DONE.items():
        path = ROOT / page
        if path.is_file():
            check_done(page, path.read_text(), wanted, errors)

    for page in LEGACY:
        path = ROOT / page
        if path.is_file() and "--pill-c" not in path.read_text():
            errors.append(
                f"{page}: no hex chips left, move it into DONE with its chip colors"
            )

    for path in sorted(ROOT.glob("20*/*.html")):
        page = path.relative_to(ROOT).as_posix()
        if page in DONE or page in LEGACY:
            continue
        text = path.read_text()
        if 'class="sbadge' in text:
            check_chips(page, text, errors)

    if errors:
        print("\n".join(errors))
        return 1

    print(f"chip check ok ({len(DONE)} done, {len(LEGACY)} legacy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

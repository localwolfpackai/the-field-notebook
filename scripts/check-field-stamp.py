#!/usr/bin/env python3
"""Keep the May field notebook's stamp off the headline.

The page used to pin .stamp with position:absolute, so at about 760px
the rubber stamp sat on the title. A stray closing brace also applied
the phone-only 0.56rem tag size on every screen. This check fails if
either mistake comes back.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "2026-05" / "github-field-notebook-2026-05-28.html"
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)
STAMP = re.compile(r"\.masthead \.stamp\s*\{([^}]*)\}")
TAG = re.compile(r'<span class="(?:pill|entry-tag)[^"]*">([^<]*)</span>')


def strip_at_blocks(css: str) -> str:
    """Drop @media / @container / @supports blocks, leave the rest."""
    out = []
    i = 0
    while i < len(css):
        if css.startswith("@", i):
            brace = css.find("{", i)
            if brace == -1:
                out.append(css[i:])
                break
            depth = 0
            k = brace
            while k < len(css):
                if css[k] == "{":
                    depth += 1
                elif css[k] == "}":
                    depth -= 1
                    if depth == 0:
                        k += 1
                        break
                k += 1
            i = k
        else:
            out.append(css[i])
            i += 1
    return "".join(out)


def main() -> int:
    errors = []
    text = PAGE.read_text()
    css = "\n".join(STYLE.findall(text))
    rel = PAGE.relative_to(ROOT)

    stamp_rules = STAMP.findall(css)
    if not stamp_rules:
        errors.append(f"{rel}: missing .masthead .stamp rule")
    for rule in stamp_rules:
        if re.search(r"position:\s*absolute", rule):
            errors.append(f"{rel}: .stamp is position:absolute and will cover the headline")

    outside = strip_at_blocks(css)
    if "0.56rem" in outside:
        errors.append(f"{rel}: 0.56rem tag size applies outside a media query")

    if "@container" in css and "container-type" not in css:
        errors.append(f"{rel}: @container query has no container-type, so it never runs")

    if "background-attachment: scroll" not in css:
        errors.append(f"{rel}: phone view still keeps a fixed notebook background")

    if re.search(r"\sstyle\s*=", text):
        errors.append(f"{rel}: inline style attribute — put it in the style block")

    for match in TAG.finditer(text):
        label = match.group(1).strip()
        if re.search(r"\s", label):
            errors.append(f"{rel}: tag has more than one word: {label!r}")

    if errors:
        print("\n".join(errors))
        return 1

    print("field stamp check ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Lock the chrome on the two May entries that are not in another open pull request.

The collaboration loop and the undo book still used a hard-coded back link,
a faint card edge, and a ruled background that stays fixed on a phone.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

FILES = (
    "2026-05/github-collaboration-loop-2026-05-31.html",
    "2026-05/github-undo-book-2026-05-30.html",
)
UNDO = "2026-05/github-undo-book-2026-05-30.html"
BACK_PAD = "padding: 0.9rem clamp(1rem, 7vw, 5rem) 0;"
CARD_BORDER = re.compile(r"\.card\s*\{[^}]*border:\s*1px solid var\(--line\)", re.S)
TAG = re.compile(r'<span class="tag">([^<]*)</span>')
SCROLL = re.compile(
    r"@media \(max-width:\s*760px\)\s*\{[^}]*background-attachment:\s*scroll",
    re.S,
)


def main() -> int:
    errors = []

    for rel in FILES:
        text = (ROOT / rel).read_text()
        if "style=" in text:
            errors.append(f"{rel}: still has an inline style")
        if "--line:" not in text:
            errors.append(f"{rel}: missing the --line token")
        if not CARD_BORDER.search(text):
            errors.append(f"{rel}: .card does not use border: 1px solid var(--line)")
        if 'class="back"' not in text:
            errors.append(f"{rel}: back link is not class=\"back\"")
        if BACK_PAD not in text:
            errors.append(f"{rel}: back row does not share the page's side padding")
        if not SCROLL.search(text):
            errors.append(f"{rel}: phone width still pins the ruled paper")
        for match in TAG.finditer(text):
            label = match.group(1).strip()
            if re.search(r"\s", label):
                errors.append(f"{rel}: tag has more than one word: {label!r}")

    undo = (ROOT / UNDO).read_text()
    if not re.search(r"\.signoff\s*\{[^}]*flex-wrap:\s*wrap", undo, re.S):
        errors.append(f"{UNDO}: .signoff does not wrap")
    if "max-width: 640px" in undo:
        errors.append(f"{UNDO}: compass still has a 640px-only stack")
    if "grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)" not in undo:
        errors.append(f"{UNDO}: compass columns are not minmax(0, 1fr)")
    if not re.search(
        r"@media \(max-width:\s*760px\)\s*\{.*\.compass \.two\s*\{[^}]*minmax\(0,\s*1fr\)",
        undo,
        re.S,
    ):
        errors.append(f"{UNDO}: compass does not stack at 760px")

    if errors:
        print("\n".join(errors))
        return 1

    print(f"entry chrome ok ({len(FILES)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

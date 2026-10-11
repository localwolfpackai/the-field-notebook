#!/usr/bin/env python3
"""Fail if the notebook index drifts off the density and phone-safe rules."""

import re
import sys
from pathlib import Path

html = Path("index.html").read_text(encoding="utf-8")
errors = []

pills = re.findall(r'class="pill(?:\s[^"]*)?">([^<]*)<', html)
for label in pills:
    words = label.split()
    if len(words) != 1:
        errors.append(f"pill must be one word, found {label!r}")

if "minmax(280px" in html:
    errors.append("card grid still uses a fixed 280px track")

if "minmax(min(100%, 16rem), 1fr)" not in html:
    errors.append("card grid is missing minmax(min(100%, 16rem), 1fr)")

if "var(--line)" not in html:
    errors.append("index is missing var(--line)")

if re.search(r"\sstyle\s*=", html):
    errors.append("index has an inline style")

style = re.search(r"<style>(.*)</style>", html, re.S)
if not style:
    errors.append("index is missing a <style> block")
else:
    hexes = re.findall(r"#[0-9A-Fa-f]{3,8}\b", style.group(1))
    if hexes:
        errors.append(f"style block has hex colors: {', '.join(hexes)}")

if errors:
    print("index check failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"index check ok ({len(pills)} one-word pills)")

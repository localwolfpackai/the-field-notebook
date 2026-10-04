# Agent Instructions for The Field Notebook

Agents operating within this repository must adhere strictly to these structural and workflow constraints.

## 1. Architectural Integrity
- **No external frameworks or libraries:** This is a zero-build-step static site. Do not introduce npm, React, Vue, tailwind, or any external CDNs (other than Google Fonts).
- **Single-File Structure:** Every HTML page is entirely self-contained. CSS must reside in `<style>` tags within the `<head>`. Do not extract CSS to external stylesheets.
- **Vanilla HTML/CSS/JS:** Use strictly vanilla HTML and CSS.

## 2. Design Constraints
- **Adhere to `DESIGN.md`:** All color values must use the defined OKLCH `:root` variables. Do not use hex codes or standard CSS colors (e.g., `red`, `#FFFFFF`) unless unavoidable.
- **Typography:** You must respect the established font families: `Geist` (headings), `Inter` (body), `Geist Mono` (code/tags), and `Caveat` (accents).
- **Density Rules:** Badges, tags, and pills must contain exactly ONE word, number, or category. Do not insert phrases into pills (e.g., `<span class="pill">machine learning</span>` is invalid; it should be `<span class="pill">ml</span>`).

## 3. Creating New Entries
- When creating a new page, you **must** use the most recent entry in the corresponding `YYYY-MM` directory as a skeleton to preserve the design system layout.
- Naming convention: `kebab-slug-YYYY-MM-DD.html`.
- Maintain the signature format defined in `DOCS.md` ("—Lupo · The Mess is the Method"). Do not alter the author's voice or sign-off format.

## 4. Spacing and Layout
- Ensure the max-width of paragraphs strictly adheres to `var(--measure)` (`68ch`) to preserve the notebook aesthetic.
- Do not utilize hard-coded margin spacing if sibling grid `gap` can be utilized instead.
- Avoid introducing inline styles. Use the documented class utility structure (e.g., `.hack`, `.toc`, `.term`).

## 5. Reviewing Output
- Check for regression in visual spacing. Specifically, verify that lists (like `.toc ol`) have adequate breathing room for pill badges without crowding lines.
- Always check that responsive layout breakpoints (`760px`, `640px`) collapse cleanly into `1fr` single-column layouts for mobile.

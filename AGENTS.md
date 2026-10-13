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

## 6. Branches and Pull Requests
- One branch per pull request. Once that pull request merges or closes, never push to its branch again. Start a fresh branch from `main`. A merged branch that gets new commits looks unmerged and blocks cleanup.
- Restyle one guide per pull request. A change that touches every guide at once collides with `main` and gets closed.
- Do not delete branches or tags yourself. `scripts/branch-cleanup.sh report` lists every branch with its pull request, diff, checks, and a verdict. Paste that table into your digest when branches pile up.
- Tags under `archive/cleanup/` are backups of deleted branches. Read them for reference. Never push to them or open a pull request from them.

## 7. Labels
Labels let Lupo scan the pull request list and see what each one is, who made it, and whether he needs to do anything. Most of them get added on their own from the branch name and the files changed. Two are up to you.

**Add these yourself when they fit:**
- `needs-lupo`: he has to look at the page or click merge before this moves. Put it on any pull request whose description has a DO THIS section. Take it off once he has done it.
- `new-guide`: the pull request adds a new field guide.

**These show up on their own, so leave them alone:**
- `by-cursor`, `by-claude`, `by-jules`: who opened it. They come from the branch name, so start your branch with `cursor/`, `claude/`, or `jules`.
- `page-fix`: a guide or the index looks or reads better.
- `checks`: the automatic checks or their scripts changed.
- `documentation`: notes for people and agents changed, like this file.
- `dependencies`: the tools the checks run on got updated.

**Also available:** `bug` for something broken on the live site, and `repo-hygiene` for branch and repo cleanup.

Use only these. If none fits, say so in the description instead of making a new label.

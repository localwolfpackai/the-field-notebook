# Comprehensive Front-End and Design Audit

## Shipped from this audit (2026-10-05)

The write-up landed before the CSS did. These pieces of it are now in the pages:

- The 27 guides that share `.toc` use `gap: 0.6rem` and a `1.8rem` number column. The older GitHub field notebook (`.toc-card`) uses the same `0.6rem` list gap.
- Every HTML page draws a `:focus-visible` ring in `--accent`.
- The index names `--line`, `--on-accent`, and a `--space-*` scale, wraps the catalog in `<main>`, and keeps pills to one word.
- Step blocks (`.hack`) use `minmax(0, 1fr)` plus `min-width: 0` on the text cell, so a long terminal line scrolls inside the card on a phone instead of dragging the whole page sideways.

Still open, on purpose: entry pages still repeat their CSS instead of sharing a file (that is the zero-build rule), and `ship-2026-07-25-launch/social-card.html` still uses hex. Do not "fix" that card by adding a build step.

## 1. STRUCTURE & SEMANTICS

*   **Finding:** The markup uses logical semantic tags across pages (`<header>`, `<section>`, `<article>`, `<aside>`, `<footer>`).
*   **Current state:** Tags like `<aside class="toc">`, `<header class="masthead">`, and `<article class="hack">` are utilized properly. Breakpoints are typically around `760px` and `640px`/`560px` for mobile collapsing.
*   **Assessment:** The semantic usage provides a good structural foundation. Accessibility attributes like `aria-label="Table of contents"` on the TOC `<aside>` and `aria-hidden="true"` on decorative elements (`.holes`) are present.
*   **Recommended fix:** No major structural overhauls are needed. However, ensure that all main content blocks are wrapped in a `<main>` tag for better landmark navigation. Verify all heading hierarchies scale down logically from `h1` directly to `h2` and `h3` without skipping levels.

## 2. SPACING & PADDING SYSTEM AUDIT

*   **Finding:** The design leverages CSS properties primarily clamped and set via rem/vw. It has a rigid scale of variables for colors and radii, but lacks a strict unified variable scale for spacing (`--space-*`).
*   **Current state:**
    *   `.page` container padding: `clamp(1.25rem, 2vw + 1rem, 3rem) clamp(1rem, 7vw, 5rem) clamp(2rem, 5vw, 5rem)`
    *   `header.masthead` padding/margin: `padding-top: 2.75rem; margin-bottom: 2.5rem;`
    *   `.intro` grid gap: `clamp(1.5rem, 3vw, 3rem)`
    *   `.toc` padding: `1.25rem 1.4rem`
    *   `.hack` grid gap: `clamp(0.5rem, 1vw, 1rem)`
    *   `Line height`: `1.62` for body.
*   **Assessment:** The layout employs fluid typography and spacing via `clamp()`, which provides a dynamic layout. However, the exact rem values feel manually tuned rather than strictly systemic (e.g., `2.75rem`, `1.25rem`, `3rem`).
*   **Recommended fix:** Consider establishing a unified spacing token system to ensure more robust predictability. Example: `--space-sm: 0.5rem; --space-md: 1.25rem; --space-lg: 3rem;`. Introduce explicit `--gap` tokens for grid layouts.

## 3. "THE TEN MOVES" (TOC) SECTION DEEP-DIVE

*   **Finding:** The Table of Contents (`.toc`) component provides a sticky-note card layout but spacing internal to the list items can feel cramped.
*   **Current state:**
    *   Container padding: `1.25rem 1.4rem`
    *   Transform: `rotate(-0.4deg)`
    *   List `ol` gap: `0.32rem`
    *   List `li` grid: `grid-template-columns: 1.6rem 1fr`, gap `0.4rem`
    *   Counters: `font-size: 0.72rem`, color: `var(--margin)`
*   **Assessment:** The card's outer padding (`1.25rem`) provides enough visual weight, and the quirky `-0.4deg` rotation reinforces the "notebook" feel nicely. However, the list's vertical gap (`0.32rem`) is somewhat tight, particularly when pill badges are presented within the same line, causing vertical crowding.
*   **Recommended fix:** Increase the list `gap` to `0.6rem` to allow the pill badges to breathe. Adjust `.toc li` column sizing to `1.8rem` to give the numbers slightly more width, preventing alignment issues with double digits.
    ```css
    .toc ol { gap: 0.6rem; }
    .toc li { grid-template-columns: 1.8rem 1fr; gap: 0.5rem; }
    ```

## 4. VISUAL HIERARCHY & TYPOGRAPHY

*   **Finding:** Good typography hierarchy leveraging font combinations.
*   **Current state:**
    *   Headings (`h1`, `h2`): `clamp()` values (e.g., `h1` is `clamp(2.4rem, 1.4rem + 4.2vw, 4.6rem)`).
    *   Body text: `clamp(1rem, 0.96rem + 0.18vw, 1.08rem)`, line-height: `1.62`. Max-width constraint is standard `68ch`.
    *   Fonts: Inter (body), Geist (display), Geist Mono (code), Caveat (accents).
*   **Assessment:** The fluid `clamp` for body and headings is excellently tuned for responsiveness. Contrast utilizes `.ink-soft`, `.ink-mute`, and `.ink` to guide visual importance over a `.paper` background.
*   **Recommended fix:** The setup is sound. Ensure links (`--accent-ink` on `--paper`) meet the WCAG 4.5:1 ratio, which `oklch(0.40 0.18 264)` does well against `oklch(0.985 0.012 85)`.

## 5. LAYOUT & RESPONSIVE BREAKPOINTS

*   **Finding:** Responsive thresholds are manually distributed based on element layout constraints.
*   **Current state:**
    *   Desktop (`> 760px`): `.intro` uses `minmax(0, 1fr) minmax(0, 0.85fr)`.
    *   Mobile (`<= 760px`, `<= 640px`): Elements snap to `1fr`.
*   **Assessment:** The use of `minmax(0, ...)` is an excellent defensive CSS strategy to prevent grid blowouts. The snapping points are logical for tablet/mobile crossover.
*   **Recommended fix:** No major fixes needed; the breakpoints properly condense to a single column cleanly, preventing horizontal scrolling.

## 6. COMPONENT SPACING (DETAILED)

*   **Finding:** Component internal spacing is relatively consistent but uses hardcoded padding instead of utility or generic tokens.
*   **Current state:**
    *   Cards (`.demo`, `.toc`): `padding: 0;` (demo container) vs `1.25rem 1.4rem` (toc).
    *   Code blocks (`.term`): `padding: 1rem 1.1rem`.
    *   Sidecards (`.tryit`, `.heads-up`): `gap: 0.85rem; padding: 0.85rem 1rem`.
*   **Assessment:** Cards are adequately padded, but `.demo` utilizes inner padding differently from generic cards.
*   **Recommended fix:** Align `.tryit`, `.heads-up`, and standard `.term` pre blocks to a uniform spacing factor, possibly transitioning from `1rem` and `1.1rem` variants to exactly `1.25rem`.

## 7. BACKGROUND & STYLING DETAILS

*   **Finding:** Distinctive background patterns provide a notebook feel.
*   **Current state:**
    *   `background-image: repeating-linear-gradient(...)` for ruled lines.
    *   `.toc::before` sticky note uses transform/rotation, `.holes` provides visual flair.
*   **Assessment:** The fixed background attachments and repeating gradients give character without distracting from the text, due to subtle colors (`--rule-soft`). The transforms (e.g., `-2deg`) are intentional.
*   **Recommended fix:** Ensure the notebook background `background-attachment: fixed` does not cause excessive scrolling repaint performance hits on lower-end devices.

## 8. INTERACTIVE ELEMENTS & FEEDBACK

*   **Finding:** Standard hover interactions exist on links and buttons.
*   **Current state:**
    *   Links: `text-decoration-thickness: 1px`, thickens to `2px` on hover.
    *   Hover effects use `--ease-paper: cubic-bezier(0.22, 1, 0.36, 1)`.
*   **Assessment:** Interactive feedback is present and tactile. However, explicit `:focus-visible` styles are absent.
*   **Recommended fix:** Define a global `:focus-visible` outline utilizing `--accent` to improve keyboard accessibility.
    ```css
    :focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 4px;
    }
    ```

## 9. ANIMATION & MOTION

*   **Finding:** Animations are properly guarded.
*   **Current state:** Usage of `@keyframes pulse` in `.demo`. Media query `@media (prefers-reduced-motion: reduce)` is applied globally.
*   **Assessment:** The animations have appropriate duration and easing, and the reduction query ensures accessibility compliance.
*   **Recommended fix:** None required.

## 10. GAPS & SPACING ANOMALIES TO FLAG

*   **Finding:** Minor anomalies in layout logic.
*   **Current state:** Mixture of specific margins (e.g. `margin-top: 0.7rem`) vs grid `gap` usage.
*   **Assessment:** Orphaned margins can occasionally lead to inconsistent rendering if siblings are hidden or reordered.
*   **Recommended fix:** Consistently use CSS grid `gap` or flex `gap` for layout clustering instead of sibling margins (`+ * { margin-top: X }`).

## 11. MISCELLANEOUS POLISH

*   **Finding:** Standardized borders and shadows.
*   **Current state:**
    *   Border: `1px solid oklch(0.86 0.03 80)` frequently used.
    *   Radii: Variables `--radius-sm`, `-md`, `-lg` consistently used.
*   **Assessment:** Shadows and borders are highly uniform and define the "paper" aesthetic flawlessly.
*   **Recommended fix:** Consolidate the specific border color string into a `--border-color` variable for easier theme swapping if a true dark mode is ever added.

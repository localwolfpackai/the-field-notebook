# Field Notebook Design System

## Core Aesthetic
The Field Notebook utilizes a strictly enforced design system aiming to replicate the feel of a physical, slightly messy notebook. The aesthetic relies heavily on specific OKLCH color palettes mimicking ink on paper, distinct typography combining serif, sans-serif, monospace, and handwriting styles, and subtle textures like ruled lines and paper holes.

## 1. Palette & Colors (OKLCH)
Color values are strictly set in `:root` variables using `oklch()`. Do not deviate from these predefined palettes.

### Ink (Text & Borders)
- `--ink`: `oklch(0.20 0.01 60)` - Primary text (deep dark gray/black)
- `--ink-soft`: `oklch(0.42 0.015 60)` - Secondary text
- `--ink-mute`: `oklch(0.60 0.012 60)` - Tertiary, small, or meta text
- `--line`: `oklch(0.86 0.03 80)` - Default card and panel border
- `--line-strong`: `oklch(0.84 0.03 80)` - Entry-card border
- `--line-hot`: `oklch(0.78 0.06 264)` - Border when a card is hovered
- `--on-accent`: `oklch(0.99 0.008 85)` - Text sitting on `--accent` (the blue pill button)
- `--paper-glass`: `oklch(0.99 0.008 85 / 0.92)` - Warm paper at partial opacity, for labels on a colored header

### Paper (Backgrounds)
- `--paper`: `oklch(0.985 0.012 85)` - Main background (warm cream)
- `--paper-alt`: `oklch(0.96 0.018 85)` - Card and secondary backgrounds
- `--paper-deep`: `oklch(0.93 0.022 85)` - Deeper accents and tooltips

### Accents & Brands
- `--margin`: `oklch(0.70 0.13 27)` - The "red pen" accent
- `--margin-soft`: `oklch(0.92 0.06 27)` - Faded red background for highlights
- `--accent`: `oklch(0.49 0.19 264)` - Bright electric blue (primary action)
- `--accent-ink`: `oklch(0.40 0.18 264)` - Darker blue for links
- `--accent-wash`: `oklch(0.93 0.05 250)` - Faded blue for pill backgrounds

### Secondary Washes (Pills & Categorization)
- `--sage` & `--sage-wash`: Greens (145 hue)
- `--amber` & `--amber-wash`: Oranges/Yellows (68 hue)
- `--violet` & `--violet-wash`: Purples (300 hue)

### Code (Dark Mode Blocks)
- `--code-bg`: `oklch(0.22 0.012 60)`
- `--code-ink`: `oklch(0.93 0.01 80)`
- Syntax highlighting variables: `--code-mute`, `--code-accent`, `--code-blue`, `--code-green`, `--code-pink`.

## 2. Typography

- **Display & Headings:** `Geist`, `Times New Roman`, serif
  - `font-weight: 700` or `800`.
  - `letter-spacing` is slightly tightened (e.g., `-0.018em` to `-0.03em`).
  - `text-wrap: balance` for h1, h2, h3.
- **Body & Paragraphs:** `Inter`, `-apple-system`, `sans-serif`
  - Body size uses a fluid scale: `clamp(1rem, 0.96rem + 0.18vw, 1.08rem)`.
  - `line-height: 1.62`.
  - Max width constraint is strictly maintained on paragraphs using `--measure` (`68ch`).
- **Code, Metadata, & Small UI:** `Geist Mono`, `monospace`
  - Used for tags, pills, dates, and code snippets.
- **Accents (The "Red Pen"):** `Caveat`, cursive
  - Used sparingly for handwritten annotations, step numbers (`.hack .nbr`), and specific badges (`.tryit .badge`).

## 3. Spacing & Padding
Name the step, then use it. The index defines the scale. Older entry pages still have one-off rem values; when you touch one, switch the value you are already changing over to a token instead of adding another magic number.

- `--space-xs`: `0.4rem` — pill rows
- `--space-sm`: `0.8rem` — tight stacks inside a card
- `--space-md`: `1.25rem` — the catalog grid
- `--space-lg`: `2.5rem` — a feature column gap
- `--space-xl`: `3rem` — space between month sections

Other rhythm that stays:
- **Global Page Padding:** Fluid. `clamp(1.25rem, 2vw + 1rem, 3rem) clamp(1rem, 7vw, 5rem) clamp(2rem, 5vw, 5rem)`.
- **Card Padding (e.g., `.toc`, `.tryit`):** Typically around `1.25rem` to `1.4rem` internally.
- **Small Component Padding (Pills/Tags):** Very tight, e.g., `padding: 0.15em 0.55em;`. One word or one number per pill.
- **TOC lists:** `.toc ol { gap: 0.6rem; }` and `.toc li { grid-template-columns: 1.8rem 1fr; gap: 0.5rem; }` so a pill on the line does not crash into the next move.

## 4. Visual Elements & Shapes
- **Radii:** Strictly controlled via variables:
  - `--radius-sm`: `6px`
  - `--radius-md`: `12px`
  - `--radius-lg`: `18px`
- **Borders:** Paper cards use `1px solid var(--line)`. Do not paste the raw `oklch()` value again.
- **Shadows:** Cards use deep, soft, colorful shadows (e.g., `0 12px 28px -20px oklch(0.40 0.06 80 / 0.4)` on `.toc`).
- **Texture:** The `.page` background implements CSS gradients to simulate ruled notebook lines.

## 5. Specific Components
- **`.toc` (Table of Contents):** Styled like an attached sticky note, complete with a pseudo-element "tape" (`.toc::before`) and a slight rotation (`transform: rotate(-0.4deg)`). The list inside breathes at `0.6rem`.

## 6. Keyboard focus
Every page includes this, placed with the reset so a tab stop is visible on cream paper:

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 4px;
}
```
- **`.hack` (Step Modules):** A two-column grid. Left column houses a large Caveat number (`.nbr`); right column holds the header, tags, and body copy. The text column is `minmax(0, 1fr)` and `.hack > .body` sets `min-width: 0`, so a long code line scrolls inside `.term` instead of stretching the page sideways. At `640px` the whole step stacks to one `minmax(0, 1fr)` column.
- **`.term` (Code Terminal):** A dark-mode block simulating a MacOS window, complete with a title bar (`.term .bar`) containing three colored dots (red, yellow, green).

## 7. Stack badges
The chips under a guide's byline (`.badges` / `.sbadge`) are one word. The row wraps. The left edge is a palette token, not a logo color.

```html
<span class="sbadge margin"><b>Claude</b></span>
<span class="sbadge accent"><b>Gemini</b></span>
```

`margin` is Claude (the red pen). `accent` is Gemini. `sage`, `amber`, `violet`, and `ink` cover the rest. Do not set `--pill-c` to a hex value, and do not set `white-space: nowrap` on the chip. On a phone the notebook background scrolls (`background-attachment: scroll` at `760px`) so the ruled lines do not hitch to the viewport.

## 8. Launch card
`ship-2026-07-25-launch/social-card.html` is a 1200×630 artboard, not a flowing page. Pixel sizes stay on the board so a screenshot of `.card` is the social image. `.stage` uses `aspect-ratio: 1200 / 630` and `container-type: inline-size`. The card is `position: absolute` inside that stage and scaled with `scale(calc(100cqw / 1200px))`, so the unscaled 1200px box does not widen the page and a phone shows the whole card. Colors on that file are the tokens above. Tape and shadow are the same hues at partial opacity (`oklch(... / 0.55)`), not a new palette and not hex.

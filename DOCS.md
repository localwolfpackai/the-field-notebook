# The Field Notebook — Docs

An open-notebook collection of step-by-step field guides on building with AI. Casual,
visual, practical. Each entry is a single self-contained HTML file in the cream-notebook
aesthetic — ruled paper, red margin, Caveat handwritten accents, dark terminal blocks.

**Live index:** [`index.html`](index.html) — the landing page that links every entry.

---

## What's in here

34 entries, May–July 2026, organized into month folders. The collection moves through
three eras — see the catalog below for the full per-entry breakdown.

**May — GitHub for AI-era builders.** The basics for people who learned to build with AI
before they learned the platform: branches, PRs, the collaboration loop, and the undo book.

**June — building with Claude & Gemini.** The core craft — wiring frontends to models,
Claude Design, agents and MCP, streaming and structured output, evals, cost and latency,
retrieval, extended thinking, vision, prompt caching, and design-system tokens.

**July — ship it and defend it.** Taking the built app to the world and keeping it there:
deploying safely, defending against prompt injection, observability, versioning the prompt
like code, and finally handing the model real verbs with tool use.

```
.
├── index.html          ← landing page (start here)
├── DOCS.md             ← this file
├── SKILL.md            ← the scheduled-task brief that generates these
├── 2026-05/            ← 6 entries (GitHub for AI-era builders)
├── 2026-06/            ← 23 entries (building with Claude & Gemini)
└── 2026-07/            ← 5 entries (ship it, defend it, watch it, version it, give it hands)
```

## Folder convention

Entries live in `YYYY-MM/` folders by their **internal publish date** (not file mtime).
`github-tips-for-beginners.html` carries an internal date of 2026-05-19, so it sits in
`2026-05/` even though its filename has no date.

Filenames are `kebab-slug-YYYY-MM-DD.html`. The single legacy exception
(`github-tips-for-beginners.html`, the origin entry) keeps its original name.

## The catalog

### 2026-07 — ship it, defend it, watch it, version it, give it hands

| Vol. | Date | Entry | Theme |
|---|---|---|---|
| 36 | 07-08 | When the Model Gets a Verb | tool use — the switch that lets a talk-only model *act*, without ever handing it the keys. Describe a tool as a `{name, description, input_schema}` JSON contract and pass it on the same call; let the model choose it (it returns a `tool_use` block, not text); run the real function yourself and feed the result back as a `tool_result` tied to the call id; loop the ask→run→feed→ask cycle (the Vol. 10 agent loop with real verbs) until it stops raising its hand. Then the seatbelt half: tag every tool `mutates: true|false` to split read from write, whitelist verbs in a hard-coded `HANDLERS` map so nothing runs off-menu (the Vol. 33 injection firewall for tools), pause the loop and require a human OK before any irreversible write, ship new write tools behind `DRY_RUN` and cap loop turns so it can't run away, and log every call with the Vol. 34 request id + who approved it so an action is a one-line audit lookup. A live approve/deny agent loop: a read tool auto-runs, and a $340 refund parks at a gate until you tap — deny it and the model recovers gracefully |
| 35 | 07-07 | The Prompt Is the Product | version — treat the system prompt as code: pull it out of the route into its own file, register versions with a single `ACTIVE` pointer, stamp `promptVersion` into every trace (Vol. 34) so a regression is a lookup not a mystery, `git diff` two versions like a PR to catch silent drops, score champion vs challenger against the golden evals (Vol. 24) before shipping, A/B a small deterministic canary on real traffic and compare 👎-rate per version, promote the winner via an env-var flag (default = last known-good), roll back in one line, and keep a `CHANGELOG.md` tying each version to the trace/eval that justified it. A live A/B bench that scores three challengers against the v2 champion — including two that lose or tie, to show the eval catching a regression |
| 34 | 07-06 | The Answer You Never See | observe — the feedback loop for a live AI app: silence isn't success, log the one structured line that matters, tag every call with a short request ID and hand it to the UI, add a 👍/👎 so users label the misses for you, trace multi-step calls as spans, sample ten random real sessions daily, replay the exact failing input before you claim a fix, chart the drift (p95 latency, tokens/call, refusal + cut-off rate), alarm on the spike not the average, then close the loop by turning the downvoted trace into a golden eval case (Vol. 24) so the exact miss can never ship again. A live conversation-replay panel you scrub, with a feedback-loop toggle to compare instrumented vs blind |
| 33 | 07-05 | The First Weird Input | defend — prompt injection in plain language: one stream with no wall, split rules from input, fence untrusted text in delimiters, name the attack, sanitize tool/page output (indirect injection), scope the model's powers so a hijacked model reaches nothing, output tripwire + canary, log the weird ones, red-team pass. A live injection sandbox you attack yourself, with a fence toggle to compare held vs breached |
| 32 | 07-01 | Ship It to the World | deploy — move the key server-side into a serverless route, rate-limit the endpoint, cap daily spend, add a timeout + max-tokens ceiling, deploy in one command, watch the logs/spend, run a four-guard pre-ship gate. A live deploy-readiness gate that flips green as you toggle the guards |

### 2026-06 — building with Claude & Gemini

| Vol. | Date | Entry | Theme |
|---|---|---|---|
| 31 | 06-30 | Ship the Tokens First | design system — make the model author a token contract (scale, ramp, 8pt spacing, radius, motion) before any component, so the UI stops looking like AI slop |
| 30 | 06-29 | The 90%-Off Dial | prompt caching — mark the stable prefix, order stable-first, read the hit counters, cut a repetitive bill ~90% |
| 29 | 06-28 | Show the Model a Picture | multimodal vision — attach an image, ask for typed findings, point at a region, tune resolution, screenshot → build spec |
| 28 | 06-27 | Show Your Work | extended thinking — enable, budget, stream, preserve across tools, when not to think |
| 27 | 06-27 | Same Prompt, Two Souls | Claude vs Gemini design — warmth vs density, the steering words, the remix |
| 26 | 06-26 | Retrieval Without the Hype | RAG in plain language — chunk, embed, search by meaning, cite |
| 25 | 06-25 | The Two Dials | cost & latency — tiers, routing, caching, streaming, budget |
| 24 | 06-24 | Grade It Before They Do | eval harness — golden cases, judge, CI gate |
| 23 | 06-23 | Make the Model Hand You JSON | structured output → typed UI |
| 22 | 06-23 | Make It Feel Alive — Streaming | token-by-token rendering |
| 21 | 06-22 | Steal a Site's Soul | tokens-first agent cloning |
| 20 | 06-21 | The Texture Layer | CSS effects that de-generate UI |
| 19 | 06-19 | Give the Agent Hands — MCP | wiring agents to real tools |
| 18 | 06-18 | The Prompt That Stops Guessing | constraint-first prompting |
| 17 | 06-17 | Build an AI App in an Afternoon | frontend + model, non-dev way |
| 16 | 06-09 | The Console Is a Context Machine | DevTools context extraction |
| 15 | 06-08 | Fan Out the Fleet | parallel sub-agents |
| 14 | 06-07 | The Token Trap | context compression |
| 13 | 06-05 | Context Before Code | context-driven development |
| 12 | 06-03 | Prompt → Config → UI | model-driven frontend |
| 11 | 06-02 | Designed, Not Generated | directing Claude Design |
| 10 | 06-01 | The Agent Loop | build an agent from scratch |
| 09 | 06-01 | Prompt to Product | prompt → working frontend |

### 2026-05 — GitHub for AI-era builders

| Vol. | Date | Entry | Theme |
|---|---|---|---|
| 08 | 05-31 | The Collaboration Loop | fork → PR → merge |
| 07 | 05-30 | The GitHub Undo Book | rescue commands |
| 06 | 05-29 | GitHub Power Moves | shortcuts, CLI, extensions |
| 03 | 05-28 | GitHub Field Notebook | habits that stick |
| 02 | 05-20 | The GitHub Handbook | beginner handbook |
| 01 | 05-19 | GitHub Tips for Beginners | the origin entry |

> Vol. numbers are the author's own sequence and aren't perfectly contiguous — a couple
> of early drafts (Vol. 04–05) never shipped. The numbering is left as-is on purpose.

## House style

Every entry shares one design system so the collection reads as a single notebook:

- **Type** — Geist (display), Inter (body), Geist Mono (code), Caveat (handwritten accents).
- **Palette** — OKLCH cream paper, electric-blue accent, warm-red margin, sage / amber /
  violet washes. Defined as CSS custom properties in each file's `:root`.
- **Anatomy** — hole-punch row, masthead with crumbs + deck + byline, a table-of-contents
  card, numbered "moves," dark terminal code blocks, try-it / heads-up sidecards, margin
  scribbles, a one-page cheat sheet, and a signed footer.
- **Density rules** — a pill/tag/badge holds exactly ONE word, number, or category (no
  dots, no phrases; split or demote to caption text instead). Index cards are 1–2 sentence
  teasers, never paragraphs. No code walls in hero sections. Label copy in plain words a
  non-developer understands.
- **Motion** — restrained; every animation respects `prefers-reduced-motion`.
- **Self-contained** — no build step, no external JS. Open the HTML and it runs. Fonts come
  from Google Fonts; badges from shields.io; everything else is inline.

## Voice

Open-notebook and casual — the four reference voices the brief points at: modular code
breakdowns (Ashi), high-energy frontend-plus-model prototyping (Bailey), daily LLM
experimentation diaries (Cal), and AI-engineer workflow in plain developer language (Dray).
Numbered moves, real commands, honest commentary, no fluff.

## Sign-off

The signature is **—Lupo**, with **"The Mess is the Method"** as a secondary motto.

- Byline: `—Lupo · The Mess is the Method` (motto in a muted secondary style)
- Footer: `—Lupo` bold in the display font (Geist); motto lives in the adjacent small/meta line
- **Never set the signature in Caveat/cursive** (retired 2026-07-21). Caveat stays for
  margin scribbles and kickers only — not for Lupo's name.

> History: entries originally closed with "Still Human" (retired 2026-06-23), then a
> cursive "Lupo / The Mess is the Method" (cursive retired 2026-07-21).

## Adding an entry

1. Copy the most recent entry as a skeleton (it carries the current design system).
2. Save as `your-slug-YYYY-MM-DD.html` in the matching `YYYY-MM/` folder (create it if the
   month is new).
3. Set the masthead crumbs (`Vol. N`, date, tag) and the `← all entries` link to
   `../index.html`.
4. Sign off per the Sign-off section: `—Lupo` + the motto in byline and footer, motto in the `<title>`.
5. Add a feature swap + a card to `index.html` (newest first) and bump the entry count.
6. Update the catalog table above.

## Status

Not yet under version control — a git push is coming. When it lands, `index.html` is the
intended entry point and this file is the contributor guide.

—Lupo · The Mess is the Method · 2026-07-21

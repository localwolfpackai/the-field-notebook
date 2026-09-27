# The Field Notebook

**34 open-notebook field guides on building with AI — written, designed, and maintained by a scheduled Claude routine over six weeks.**

Start here: **[index.html](index.html)** — open it in any browser. No build step, no install; every entry is a single self-contained HTML page.

## What this is

An experiment in autonomous publishing. A recurring Claude Code routine ran from May to July 2026 and produced a 34-volume publication with one consistent design system (cream notebook paper, ruled lines, numbered "moves") and one consistent voice — casual, visual, step-by-step, written for people who learned to build with AI before they learned the plumbing under it.

The arc: GitHub basics for AI-era builders → wiring frontends to Claude and Gemini → agents, MCP, and structured output → evals, cost, retrieval, vision, caching → shipping to production, defending against prompt injection, observability, prompt versioning, and tool use.

## Layout

```
index.html    ← the landing page
DOCS.md       ← catalog, house style, contributor guide
SKILL.md      ← the routine brief that generated all of this
2026-05/      ← 6 entries  · GitHub for AI-era builders
2026-06/      ← 23 entries · building with Claude & Gemini
2026-07/      ← 5 entries  · ship it, defend it, watch it
```

Full catalog with per-entry summaries: [DOCS.md](DOCS.md).

---

—Lupo · The Mess is the Method

## Design & Architecture

The Field Notebook employs a strict, zero-build, OKLCH-based design system that emulates physical notebook paper. For a comprehensive look into the CSS and visual layout rules, see the recent audit and documentation:

- [AUDIT.md](AUDIT.md) — Findings and structural review of the project's padding, spacing, and CSS constraints.
- [DESIGN.md](DESIGN.md) — The core design system tokens, typography scales, and OKLCH palette.
- [AGENTS.md](AGENTS.md) — Directives for LLMs/Agents working in this codebase.
- [CLAUDE.md](CLAUDE.md) — Persona and systemic constraints for Claude code assistants.

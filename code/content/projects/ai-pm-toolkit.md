---
title: "AI PM Toolkit"
description: "Generate PRDs, roadmaps, and user stories from a product brief using AI."
tech_stack: [FastAPI, OpenAI API, HTMX, Markdown Export, PDF Export]
status: "planned"
featured: false
display_order: 4
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/ai-pm-toolkit"
problem: "PMs spend significant time writing formulaic documents (PRDs, roadmaps, user stories) but get stuck on structure, completeness, and clarity. Ad-hoc ChatGPT prompts produce mediocre results because they lack structure and rigor."
approach: "Build an AI toolkit with carefully engineered prompts that generate high-quality, structured PM artifacts. Provide three specialized modes: PRD Generator, Roadmap Builder, and Story Writer. Make output editable and exportable."
solution: "A web-based AI PM Toolkit that takes a product brief and generates professional PRDs, phased roadmaps, and user stories with acceptance criteria. All output is structured, editable, and exportable to Markdown or PDF."
---

## What

An AI-powered toolkit that generates structured PM artifacts (PRDs, roadmaps, user stories) from a product brief.

**Three Modes:**

1. **PRD Generator** — Input: product name, target user, problem, market context, constraints, goals
   - Output: Problem statement, target user + JTBD, success metrics, MVP scope, technical considerations, risks, open questions

2. **Roadmap Builder** — Input: product vision and timeline constraints
   - Output: Phased roadmap (Now/Next/Later or quarterly), milestones, dependencies, success criteria per phase

3. **Story Writer** — Input: features from the roadmap
   - Output: User stories with acceptance criteria, edge cases, technical notes, grouped by epic

**Additional Features:**
- Inline markdown editor for outputs
- Export to Markdown (.md) or PDF
- Save and browse generation history
- Copy-to-clipboard for each artifact

## Why

**The Problem:**
Most PMs use ChatGPT with ad-hoc prompts and get inconsistent results. PRDs are either too vague or bloated. Roadmaps lack clear dependencies. User stories miss edge cases.

**Why This Toolkit Matters:**
- **Consistency:** Engineered prompts ensure every artifact follows the same structure
- **Speed:** Go from idea to detailed PRD in 5 minutes instead of 2 hours
- **Quality:** Forces PMs to think through context (market, risks, constraints) upfront
- **Learning:** Reverse-engineer the prompts to understand PM best practices
- **Demonstration:** Shows both AI fluency AND PM rigor (the outputs are opinionated, not generic)

**Who Needs This:**
- PMs who want AI-assisted drafting without losing rigor
- Interviewers evaluating your AI + PM thinking
- Founders building products quickly with structured thinking
- You, demonstrating prompt engineering depth

## How

**Architecture:**

```
User Input Form (product brief)
    ↓
FastAPI Route receives data
    ↓
Calls OpenAI with engineered prompt (includes examples + constraints)
    ↓
Streams response to frontend (real-time generation UI)
    ↓
Parses output into structured markdown
    ↓
Renders in editor + export options
    ↓
Save to SQLite history
```

**Key Design Decisions:**

1. **Engineered Prompts:** Each mode has a detailed system prompt that:
   - Specifies output format (markdown with heading structure)
   - Provides examples of good outputs
   - Lists what NOT to do (avoid generic fluff, be specific)
   - Includes context (who the user is, why structure matters)

2. **Streaming UI:** Show generation in real-time so users feel the AI is "thinking" (better UX than waiting for completion)

3. **Editable Output:** Generated content is starting point, not final answer. Users edit inline before export.

4. **Export Options:** Markdown for version control, PDF for sharing with executives.

5. **History:** SQLite stores previous generations so users can compare versions and iterate.

**Build Path:**

- **Phase 1 (Week 1-2):** PRD Generator only
  - Form input → OpenAI call → markdown output → export
  - Test prompt quality with 5+ examples

- **Phase 2 (Week 3):** Roadmap Builder + Story Writer
  - Reuse prompt patterns from PRD generator
  - Add dependency visualization (roadmap view)

- **Phase 3 (Week 4):** Polish
  - Inline editor
  - History/versioning
  - Export to PDF
  - Dark mode

## Technical Stack

- **Backend:** FastAPI (async, streaming support)
- **AI:** OpenAI API (gpt-4o-mini for cost efficiency)
- **Frontend:** HTMX + Tailwind (real-time updates without page reloads)
- **Storage:** SQLite (save history and past generations)
- **Export:** Python markdown + weasyprint (PDF generation)
- **Editor:** Monaco Editor (code/markdown editing experience)

---

## Why Build This Project

1. **Demonstrates Prompt Engineering** — Anyone can call ChatGPT. Few can engineer prompts that consistently produce high-quality output.

2. **Shows PM + Technical Thinking** — Not just "AI is cool." You're thinking about structure, completeness, edge cases—pure PM thinking implemented through AI.

3. **Immediately Useful** — You'll use this for your own product planning. Other PMs will want it.

4. **Portfolio Differentiator** — Most portfolios show what you've shipped. This shows how you think + accelerate thinking with AI.

---

## Next Steps

See `strategy/04_AI_PM_TOOLKIT.md` for detailed technical specification and v2 roadmap.

**Expected Timeline:** 3-4 weeks for full build
**Complexity:** Medium (prompt engineering + FastAPI + export logic)
**Impact:** High (most reusable PM tool)

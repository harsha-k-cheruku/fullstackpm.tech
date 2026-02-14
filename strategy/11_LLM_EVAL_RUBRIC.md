# LLM Component Evaluation Rubric & Test Harness

## Purpose

When you give the same component spec to Claude, GPT-4, Gemini, etc., you need a consistent way to evaluate and compare the results. This document defines:

1. **The evaluation rubric** — How to score each LLM's output
2. **The testing protocol** — How to run a fair test
3. **The test harness** — A page that renders outputs side-by-side

This is essentially **Project 5 (LLM Prompt Eval Framework) applied to your own build process** — dogfooding the concept.

---

## Evaluation Rubric

### Scoring Dimensions

Each LLM output is scored across 8 dimensions on a 1-5 scale.

| # | Dimension | What It Measures | 1 (Poor) | 3 (Acceptable) | 5 (Excellent) |
|---|-----------|-----------------|----------|-----------------|---------------|
| 1 | **Design System Adherence** | Does the output use the correct tokens, colors, spacing from `09_DESIGN_SYSTEM.md`? | Uses hardcoded colors, ignores tokens | Mostly correct, a few deviations | Perfect adherence to every token |
| 2 | **Spec Compliance** | Does the output meet ALL acceptance criteria from the component spec? | Misses multiple criteria | Meets most criteria, minor gaps | Meets every acceptance criterion |
| 3 | **HTML Semantics** | Are correct HTML5 elements used? (`<nav>`, `<article>`, `<section>`, etc.) | Divs everywhere | Mostly semantic, some misuses | Perfect semantic structure |
| 4 | **Accessibility** | ARIA attributes, keyboard nav, focus management, contrast | No accessibility consideration | Basic ARIA, some gaps | Full ARIA, keyboard, screen reader support |
| 5 | **Tailwind Correctness** | Are Tailwind classes used properly? No conflicting classes, correct responsive prefixes | Incorrect classes, CSS overrides | Mostly correct, minor class issues | Clean, idiomatic Tailwind |
| 6 | **Responsive Design** | Does it work at all breakpoints (mobile, tablet, desktop)? | Broken on mobile | Works but has layout issues at some breakpoints | Flawless at every breakpoint |
| 7 | **Code Quality** | Clean, readable, maintainable code. No unnecessary complexity. | Messy, duplicate code, over-engineered | Functional but could be cleaner | Clean, DRY, well-structured |
| 8 | **Dark Mode** | Does it work correctly in both light and dark mode? | Only works in one mode | Mostly works, minor color issues in other mode | Perfect in both modes |

### Scoring Scale

```
1 = Poor       — Fails to meet the requirement
2 = Below Avg  — Partially meets, significant issues
3 = Acceptable — Meets basic requirements, minor issues
4 = Good       — Meets requirements well, minimal issues
5 = Excellent  — Exceeds requirements, production-ready
```

### Aggregate Scores

| Metric | Formula |
|--------|---------|
| **Component Score** | Average of all 8 dimensions (1.0 - 5.0) |
| **Pass/Fail** | Pass if ALL dimensions >= 3 AND overall >= 3.5 |
| **LLM Rank** | Rank LLMs by average component score across all components tested |

### Bonus Points (Not Scored, But Noted)

- Did the LLM add helpful comments in the code?
- Did it handle edge cases not explicitly stated in the spec?
- Did it suggest improvements to the spec itself?
- Was the code immediately runnable without edits?

---

## Testing Protocol

### Pre-Test Setup

1. **Choose components to test.** Start with 3 components of varying complexity:
   - Simple: Component 08 (Stats Card Grid)
   - Medium: Component 03 (Project Card)
   - Complex: Component 01 (Navigation Bar)

2. **Prepare the prompt.** Each LLM receives the EXACT same prompt:

```
Prompt Template:
---
You are building a component for a FastAPI + Jinja2 + Tailwind CSS + HTMX web application.

## Design System
{paste full content of 09_DESIGN_SYSTEM.md}

## Component Specification
{paste the specific component spec from 10_COMPONENT_SPECS.md}

## Instructions
Build this component as a Jinja2 template partial (HTML file with Tailwind classes).
Follow the Design System exactly. Meet every acceptance criterion.
Return ONLY the HTML/Jinja2 code. No explanation needed.
---
```

3. **Control variables:**
   - Same prompt to every LLM (copy-paste, no edits)
   - Same model tier from each provider (e.g., Claude Opus, GPT-4, Gemini Ultra)
   - Default temperature (don't override)
   - Single attempt (no retries or "try again")
   - Record: model name, timestamp, raw output

### Test Execution

For each component × each LLM:

1. Send the prompt
2. Copy the raw output (code only)
3. Save to file: `test_harness/outputs/{component_name}/{llm_name}.html`
4. Score against rubric (either manually or via LLM-as-judge)
5. Record scores in the evaluation spreadsheet

### LLM-as-Judge Option

For faster (but less reliable) scoring, use Claude to evaluate the other LLMs' outputs:

```
Prompt for Judge:
---
You are evaluating an HTML/Jinja2 component built by an LLM.

## Design System (the rules it should follow)
{design system}

## Component Specification (what it should build)
{component spec}

## LLM Output (what it actually built)
{llm output code}

Score the output on these 8 dimensions (1-5 each):
1. Design System Adherence
2. Spec Compliance
3. HTML Semantics
4. Accessibility
5. Tailwind Correctness
6. Responsive Design
7. Code Quality
8. Dark Mode

For each dimension, provide:
- Score (1-5)
- Brief reasoning (1-2 sentences)

Return as JSON:
{
  "scores": {
    "design_system_adherence": {"score": N, "reasoning": "..."},
    ...
  },
  "overall_score": N.N,
  "passed": true/false,
  "summary": "One paragraph overall assessment"
}
---
```

**Important:** If using Claude as judge, note the bias. Claude may score its own output higher. For fairness, also use GPT-4 as a judge and average the scores.

---

## Test Harness

### What It Is

A standalone HTML page that renders each LLM's component output side-by-side for visual comparison. Not part of the main portfolio site — it's a development tool.

### File Structure

```
test_harness/
├── index.html              — Side-by-side comparison page
├── rubric.html             — Interactive scoring form
├── results.json            — Stored evaluation scores
├── outputs/
│   ├── navbar/
│   │   ├── claude.html
│   │   ├── gpt4.html
│   │   └── gemini.html
│   ├── project_card/
│   │   ├── claude.html
│   │   ├── gpt4.html
│   │   └── gemini.html
│   └── stats_grid/
│       ├── claude.html
│       ├── gpt4.html
│       └── gemini.html
├── styles/                 — Shared Tailwind CDN + design system CSS
│   └── design-tokens.css
└── README.md
```

### Test Harness Page (`index.html`)

**Layout:**
- Top: Component selector dropdown (Navbar, Project Card, Stats Grid, etc.)
- Below: Side-by-side panels (2 or 3 columns depending on LLMs tested)
- Each panel:
  - Header: LLM name + model version
  - Rendered component (loaded via iframe or injected HTML)
  - Score summary badges (if scored)
- Bottom: "Score This" button → opens rubric form

**Features:**
- Toggle dark mode to see all outputs switch simultaneously
- Toggle viewport width (mobile/tablet/desktop) to test responsiveness
- Panels are equal width for fair visual comparison
- Optional: "View Source" toggle to see raw HTML of each output

### Rubric Page (`rubric.html`)

**Layout:**
- Select: Component + LLM being scored
- 8 dimension rows, each with:
  - Dimension name and description
  - 1-5 radio buttons (visual scale)
  - Text area for reasoning notes
- Submit → saves to `results.json`
- Summary at bottom: total score, pass/fail

### Implementation Notes

- Pure HTML + Tailwind CDN + vanilla JS. No framework needed.
- `results.json` is a flat file updated via JavaScript (or manually).
- Iframes are the simplest way to isolate each LLM's output (prevents CSS conflicts).
- The design system CSS (`design-tokens.css`) is shared across all iframes.

### Building the Harness

This is a **1-day build**. It's a development tool, not a production app.

```
Phase 1 (2 hours): Create index.html with side-by-side iframe layout
Phase 2 (2 hours): Create rubric.html with scoring form
Phase 3 (2 hours): Add dark mode toggle, viewport width toggle, "View Source"
Phase 4 (2 hours): Test with sample outputs, refine layout
```

---

## Evaluation Workflow (Step by Step)

### Round 1: Build 3 Components with 3 LLMs

```
Step 1: Pick 3 components (simple, medium, complex)
Step 2: Prepare prompt for each (design system + spec)
Step 3: Send identical prompt to Claude, GPT-4, Gemini
Step 4: Save outputs to test_harness/outputs/
Step 5: Open test harness, visually inspect side-by-side
Step 6: Score each output using rubric (manually or LLM-as-judge)
Step 7: Record scores in results.json
Step 8: Pick the winner for each component
```

### Round 2: Full Site Build

After Round 1, you'll know which LLM is strongest for:
- Layout/structural components (nav, footer)
- Content display (cards, blog posts)
- Interactive elements (filters, forms)
- Data visualization (charts, dashboards)

Use the best LLM for each category going forward. Or continue benchmarking as you build new components.

---

## Results Template

```json
{
  "evaluations": [
    {
      "component": "navbar",
      "llm": "claude-opus-4-6",
      "date": "2026-02-15",
      "scores": {
        "design_system_adherence": { "score": 5, "notes": "" },
        "spec_compliance": { "score": 4, "notes": "Missing aria-current" },
        "html_semantics": { "score": 5, "notes": "" },
        "accessibility": { "score": 4, "notes": "" },
        "tailwind_correctness": { "score": 5, "notes": "" },
        "responsive_design": { "score": 4, "notes": "Mobile menu toggle needs work" },
        "code_quality": { "score": 5, "notes": "" },
        "dark_mode": { "score": 5, "notes": "" }
      },
      "overall_score": 4.6,
      "passed": true,
      "notes": "Strong output. Minor accessibility gaps."
    }
  ]
}
```

---

## How This Becomes a Portfolio Story

When you're done, you'll have:

1. A **Design System** you authored (shows product/design thinking)
2. **Component Specs** that are precise enough to benchmark LLMs (shows spec-writing rigor)
3. **A rubric and scoring methodology** for evaluating AI outputs (shows AI PM judgment)
4. **Quantified results** comparing LLMs on real tasks (shows analytical depth)
5. **A test harness** you built for side-by-side comparison (shows you build tools)

This ties directly into **Project 5 (LLM Prompt Eval Framework)** and makes for an incredible interview story: *"Before I built my portfolio site, I created a design system and used it to benchmark three different LLMs building the same components. Here's what I found..."*

---

## Next Step

Build the test harness (`test_harness/index.html`) first — it's a simple HTML page. Then run Round 1 with 3 components across 3 LLMs. Use the results to decide which LLM to use for the full portfolio site build.

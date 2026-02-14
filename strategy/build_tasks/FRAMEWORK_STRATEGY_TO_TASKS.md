# Framework: Turning Strategy Docs into Build Tasks

## Purpose

This is a **meta-framework** — a set of instructions you give to any LLM so it can read a project strategy document and produce a set of self-contained, parallelizable build task files. Each output task file can then be handed to a different LLM (or the same one) to generate working code.

**The pipeline:**
```
Strategy Doc (e.g., 02_PM_INTERVIEW_COACH.md)
    ↓  [give to LLM with this framework]
Build Task Files (e.g., BUILD_01_DATABASE.md, BUILD_02_API.md, ...)
    ↓  [give each to any LLM]
Working Code
```

---

## How to Use

1. Copy the **LLM Prompt** section below
2. Attach the strategy doc for the project you want to break down
3. Attach this framework file
4. Attach the **Reference Files** section (design system, tech stack, conventions)
5. Send to any capable LLM (Claude, GPT-4, Gemini)
6. Review the output task files, adjust if needed
7. Hand each task file to an LLM to generate code

---

## LLM Prompt

Copy everything below and paste it into any LLM, along with the strategy doc.

```
---START PROMPT---

You are a senior software architect. Your job is to read the attached project strategy document and produce a set of **self-contained build task files** — one per feature or module — that can each be given to a different LLM to generate working code.

## Input

I am giving you:
1. A **project strategy document** — contains product brief, features, technical architecture, data models, API endpoints, and UI specs
2. A **framework document** — explains the output format and rules
3. **Reference files** — design system, tech stack, coding conventions

## Output

Produce the following:

### A. A README.md

A summary file containing:
- Project name and one-line description
- A numbered task list table with columns: #, File, What It Builds, Depends On, Complexity
- A dependency graph showing which tasks can run in parallel
- Recommended build order

### B. One BUILD_XX_NAME.md file per task

Each file must follow the **8-Section Template** below. Every file must be fully self-contained — an LLM reading it should need ZERO external context.

---

## 8-Section Template

Every build task file MUST have these 8 sections, in this order:

### Section 1: Project Overview
Standard boilerplate identifying the project:
- Project name
- Purpose (one sentence)
- Owner
- How this task fits into the larger project

### Section 2: Tech Stack (Mandatory Constraints)
A table of required technologies. Include a "Do NOT use" list.

The standard stack for all projects is:
| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | **FastAPI** (Python 3.11+) | Async route handlers, Pydantic models |
| Templating | **Jinja2** | Server-side rendering, no client-side frameworks |
| Styling | **Tailwind CSS** (CDN) | Utility classes only |
| Interactivity | **HTMX** (CDN) | Dynamic partial updates |
| Icons | **Heroicons** (inline SVG) | Outline style, 24px viewBox |
| Fonts | **Geist Sans** + **JetBrains Mono** | Geist Sans via jsDelivr CDN, JetBrains Mono via Google Fonts |
| Database | **SQLite** + **SQLAlchemy** (async) | For projects that need persistence |
| AI | **Claude API** (Anthropic SDK) | For projects that need AI |
| Charts | **Chart.js** (CDN) | For projects that need visualization |
| Deployment | **Render** | Procfile included |

**Do NOT use:** React, Vue, Angular, Svelte, Next.js, npm/node, webpack, any JS framework, Bootstrap, SCSS/LESS.

Adjust this table per project — not every project needs database, AI, or charts.

### Section 3: Design System
The full CSS custom properties (color tokens) for both light and dark mode. Paste inline so the LLM has the exact values. Current design system:

```css
:root {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8FAFC;
  --color-bg-tertiary: #F1F5F9;
  --color-text-primary: #000000;
  --color-text-secondary: #1D1D1F;
  --color-text-tertiary: #48484A;
  --color-border: #E2E8F0;
  --color-border-hover: #CBD5E1;
  --color-accent: #2E8ECE;
  --color-accent-hover: #2577AD;
  --color-accent-light: #E8F4FB;
  --color-accent-dark: #1A3A52;
  --color-success: #27AE60;
  --color-success-bg: #D5F5E3;
  --color-warning: #F1C40F;
  --color-warning-bg: #FEF9E7;
  --color-danger: #E74C3C;
  --color-danger-bg: #FADBD8;
  --color-info: #2E8ECE;
}

.dark {
  --color-bg-primary: #030712;
  --color-bg-secondary: #0F172A;
  --color-bg-tertiary: #1E293B;
  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-text-tertiary: #64748B;
  --color-border: #1E293B;
  --color-border-hover: #334155;
  --color-accent-light: #172554;
  --color-success-bg: #052E16;
  --color-warning-bg: #422006;
  --color-danger-bg: #450A0A;
}
```

Also include the typography scale classes (text-display, text-h1, text-h2, text-h3, text-h4, text-body-lg, text-body, text-small, text-xs) with their font-size, line-height, font-weight, and letter-spacing values.

### Section 4: Coding Conventions
Rules the LLM must follow:
- Python: type hints, Pydantic models, async handlers, import ordering (stdlib → third-party → local)
- HTML/Jinja2: extends base.html, CSS variables for colors (never hardcode hex), Tailwind utilities, no `dark:` prefix
- HTMX: hx-get/hx-post, hx-target, hx-swap, hx-indicator
- Accessibility: aria-labels, focus rings, semantic HTML

### Section 5: The Task
This is the unique section per file. It must include:

**a) What to build** — Clear description of the feature/module
**b) Scope boundaries** — What's IN and what's OUT
**c) Data models** — Pydantic models or SQLAlchemy models with every field described
**d) API endpoints** — Route, method, request params, response format
**e) Template specs** — Page layout, component hierarchy, visual requirements
**f) Business logic** — Algorithms, scoring rules, validation rules
**g) Inline reference files** — Full text of every existing file the LLM needs to read (not file paths — paste the actual content)
**h) Sample data** — Example inputs and expected outputs

### Section 6: Expected Output
List every file the LLM should produce, with full paths. Include output rules:
- Return COMPLETE files, not snippets
- Include file path as comment at top
- No features beyond spec
- All colors via CSS variables

### Section 7: Project Structure
ASCII tree showing the full project directory, annotating which files exist, which are created by this task, and which come from other tasks.

### Section 8: Acceptance Test
5-12 concrete, verifiable tests. Each test should have:
- What to do (a command or browser action)
- What to expect (specific output or visual result)
- Use curl commands, browser checks, or code assertions

---

## Rules for Task Decomposition

### Sizing
- Each task should take an LLM 1 response to produce (not a multi-turn conversation)
- If a feature needs >6 files, split it into sub-tasks
- If a feature needs <2 files, combine it with a related feature
- Target: 3-6 output files per task

### Dependencies
- Minimize dependencies between tasks — maximize parallelism
- Common pattern: Database/Models task has no deps → Service tasks depend on it → Route/Template tasks depend on services
- Always make the data layer (models + seed data) a standalone task with no dependencies
- UI-only tasks can often run in parallel

### Dependency Patterns by Project Type

**For AI-powered projects (Interview Coach, PM Toolkit, Decision System):**
```
Task 1: Database models + migrations + seed data  (no deps)
Task 2: Base templates + layout + shared partials  (no deps)
Task 3: Core service logic (no AI)                 (depends on 1)
Task 4: AI integration (prompts + Claude API)      (depends on 1)
Task 5: Main UI pages + routes                     (depends on 1, 2, 3)
Task 6: AI-powered UI (streaming, feedback)        (depends on 2, 4, 5)
Task 7: Dashboard / analytics views                (depends on 1, 2, 3)
Task 8: HTMX interactions + polish                 (depends on 5, 6, 7)
```

**For data/analytics projects (Marketplace Dashboard, A/B Test Analyzer):**
```
Task 1: Database models + synthetic data generator  (no deps)
Task 2: Base templates + layout + shared partials   (no deps)
Task 3: Data processing services + aggregations     (depends on 1)
Task 4: Chart/visualization components              (depends on 2)
Task 5: Main pages + routes + filters               (depends on 1, 2, 3, 4)
Task 6: HTMX interactions + real-time updates       (depends on 5)
```

**For content/tool projects (LLM Eval Framework, AI Bootcamp Case Study):**
```
Task 1: Data models + storage                      (no deps)
Task 2: Base templates + layout                    (no deps)
Task 3: Core business logic                        (depends on 1)
Task 4: Input forms + validation                   (depends on 1, 2)
Task 5: Output display + export                    (depends on 2, 3)
Task 6: Dashboard + history views                  (depends on 1, 2, 3)
```

### Self-Containment Checklist
Before finalizing each task file, verify:
- [ ] An LLM with NO project context can produce working code from this file alone
- [ ] All referenced existing files are pasted inline (not just file paths)
- [ ] All data models are fully defined (not "see other task")
- [ ] API endpoints from other tasks that this task calls are documented with request/response format
- [ ] The acceptance test can be run without completing other tasks (or states what stubs are needed)

### What to Inline

Each task file should include the full text of:
- Any config files (settings, database config)
- Any base templates the task's templates extend
- Any shared partials the task's templates include
- Any service interfaces the task's code calls (even if implemented in another task)
- The full CSS custom properties (design system)

Do NOT inline:
- Strategy docs (summarize the relevant parts instead)
- Other task files
- Test files from other tasks

---

## Naming Convention

```
strategy/build_tasks/{project_name}/
├── README.md
├── BUILD_01_{MODULE_NAME}.md
├── BUILD_02_{MODULE_NAME}.md
├── ...
└── BUILD_XX_{MODULE_NAME}.md
```

Project folder names:
- `pm_interview_coach/`
- `marketplace_dashboard/`
- `ai_pm_toolkit/`
- `ai_pm_decision_system/`
- `llm_prompt_eval/`
- `ab_test_analyzer/`
- `ai_bootcamp_case_study/`

Module names should be short, descriptive, and uppercase:
- `DATABASE_MODELS`
- `BASE_TEMPLATES`
- `QUESTION_SERVICE`
- `AI_EVALUATION`
- `PRACTICE_UI`
- `DASHBOARD`
- `HTMX_INTERACTIONS`

---

## Example: Applying This to PM Interview Coach

Given strategy doc `02_PM_INTERVIEW_COACH.md`, the expected output would be:

```
strategy/build_tasks/pm_interview_coach/
├── README.md
├── BUILD_01_DATABASE_MODELS.md      — SQLite schema, SQLAlchemy models, seed questions
├── BUILD_02_BASE_TEMPLATES.md       — Base layout, nav, footer, shared partials
├── BUILD_03_QUESTION_SERVICE.md     — Question CRUD, category filtering, random selection
├── BUILD_04_AI_EVALUATION.md        — Claude API integration, prompt templates, scoring logic
├── BUILD_05_PRACTICE_UI.md          — Question display, answer form, timer, results page
├── BUILD_06_HISTORY_DASHBOARD.md    — Practice history table, progress charts, score trends
├── BUILD_07_HTMX_INTERACTIONS.md    — Category filtering, live timer, streaming AI feedback
└── BUILD_08_CHART_COMPONENTS.md     — Radar chart, score trend line chart, category breakdown
```

Dependency graph:
```
Independent (start anytime):
  Task 1: Database Models
  Task 2: Base Templates

After Task 1:
  Task 3: Question Service
  Task 4: AI Evaluation

After Tasks 1, 2, 3:
  Task 5: Practice UI

After Tasks 1, 2, 3:
  Task 6: History Dashboard

After Task 2:
  Task 8: Chart Components

After Tasks 5, 6, 8:
  Task 7: HTMX Interactions
```

Recommended order: 1 & 2 in parallel → 3 & 4 in parallel → 5 & 6 & 8 in parallel → 7

---END PROMPT---
```

---

## Reference Files to Attach

When using this framework, always attach these alongside the strategy doc:

1. **This file** (`FRAMEWORK_STRATEGY_TO_TASKS.md`) — the framework itself
2. **The strategy doc** for the specific project (e.g., `02_PM_INTERVIEW_COACH.md`)
3. **`00_MASTER_PLAN.md`** — for overall context and tech stack rationale
4. **`code/app/static/css/custom.css`** — current design system tokens and typography
5. **`code/app/templates/base.html`** — if the project shares the portfolio site's layout (optional — standalone projects may have their own base template)

---

## Quality Checklist for Generated Task Files

After the LLM generates the build task files, review each against:

| Check | What to Verify |
|-------|---------------|
| Self-contained | Can you paste this into a fresh LLM chat and get working code? |
| No dangling refs | Every file/model/service referenced is either inlined or clearly marked as "from Task X" |
| Scope is clear | IN/OUT boundaries are explicit — no ambiguity about what to build |
| Acceptance tests work | Each test can be run independently (or states what stubs are needed) |
| File paths match | Expected output paths match the project structure tree |
| Dependencies minimal | The task has the fewest possible dependencies on other tasks |
| No over-engineering | The task builds exactly what's specified, nothing more |
| Design system included | Color tokens, typography scale, and font loading are pasted inline |
| Conventions documented | Python style, Jinja2 patterns, HTMX usage rules are explicit |

---

## Tips for Best Results

1. **Start with the data layer** — Task 1 should always be database models + seed data. Everything else depends on it.
2. **Separate AI from UI** — AI integration (prompts, API calls, scoring) should be its own task, not mixed into UI tasks. This lets you iterate on prompts independently.
3. **Templates are cheap, logic is expensive** — If in doubt, put more logic into service tasks and keep template tasks focused on layout.
4. **Include sample data** — Every task that touches data should include realistic sample inputs and expected outputs.
5. **Test at boundaries** — Acceptance tests should verify the interfaces between tasks (e.g., "the service returns data in this shape") not just internal logic.
6. **One task = one `uvicorn` start** — After completing any task, `python3 -m uvicorn app.main:app --reload` should start without errors (even if other tasks aren't done yet, those routes just won't exist).

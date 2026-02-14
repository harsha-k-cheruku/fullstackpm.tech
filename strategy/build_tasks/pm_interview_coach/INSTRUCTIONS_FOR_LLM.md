# Instructions for LLM Agent

## Your Task

You are being asked to generate **BUILD_02 through BUILD_08** for the PM Interview Coach project. BUILD_01 has already been created as a reference example.

## What to Read First

Read these files IN THIS ORDER:

1. **`/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/FRAMEWORK_STRATEGY_TO_TASKS.md`**
   - This explains the 8-section template you MUST follow
   - Read the entire file carefully — it contains all the rules

2. **`/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/02_PM_INTERVIEW_COACH.md`**
   - The product strategy for this project
   - Contains features, data models, API endpoints, UI specs

3. **`/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/README.md`**
   - The task breakdown and dependency graph
   - Shows what each BUILD file should contain

4. **`/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/BUILD_01_DATABASE_MODELS.md`**
   - Reference example showing the exact format
   - Study this carefully — your output should match this quality and structure

5. **`/Users/sidc/Projects/claude_code/fullstackpm.tech/code/app/static/css/custom.css`**
   - The design system (color tokens, typography)
   - You MUST paste these values inline in Section 3 of each BUILD file

## What to Generate

Create these 7 files in this folder:

- `BUILD_02_BASE_TEMPLATES.md`
- `BUILD_03_QUESTION_LOADER.md`
- `BUILD_04_AI_EVALUATOR.md`
- `BUILD_05_PRACTICE_UI.md`
- `BUILD_06_LANDING_HISTORY.md`
- `BUILD_07_PROGRESS_DASHBOARD.md`
- `BUILD_08_HTMX_INTERACTIONS.md`

## Critical Rules

### 1. Follow the 8-Section Template EXACTLY

Every BUILD file MUST have these sections in this order:

1. **Project Overview** (standard boilerplate)
2. **Tech Stack** (mandatory constraints table)
3. **Design System** (full CSS variables pasted inline)
4. **Coding Conventions** (Python, HTML/Jinja2, HTMX rules)
5. **The Task** (unique per file — the actual spec)
6. **Expected Output** (list of files to produce)
7. **Project Structure** (ASCII tree)
8. **Acceptance Test** (5-12 concrete tests)

### 2. Self-Contained Files

Each BUILD file must be **completely self-contained**:
- Include FULL text of any existing files the task references
- Paste color tokens inline (never say "see custom.css")
- Paste data models inline (never say "see Task 1")
- Include sample data inline
- No external links or references

### 3. Use the Exact Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | **FastAPI** (Python 3.11+) | Async route handlers, Pydantic models |
| Templating | **Jinja2** | Server-side rendering |
| Styling | **Tailwind CSS** (CDN) | Utility classes only |
| Interactivity | **HTMX** (CDN) | Dynamic partial updates |
| Icons | **Heroicons** (inline SVG) | Outline style, 24px viewBox |
| Fonts | **Geist Sans** + **JetBrains Mono** | Via CDN |
| Database | **SQLite** + **SQLAlchemy** (async) | For persistence |
| AI | **Claude API** (Anthropic SDK) | For AI evaluation |
| Charts | **Chart.js** (CDN) | For visualizations |

**Do NOT use:** React, Vue, Angular, Next.js, npm/node, webpack, Bootstrap, SCSS.

### 4. Color System (MUST paste inline in Section 3)

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

### 5. Typography Classes (MUST paste inline in Section 3)

```css
.text-display { font-size: 3.5rem; line-height: 1.05; font-weight: 700; letter-spacing: -0.04em; }
.text-h1 { font-size: 2.5rem; line-height: 1.1; font-weight: 700; letter-spacing: -0.03em; }
.text-h2 { font-size: 1.75rem; line-height: 1.2; font-weight: 600; letter-spacing: -0.02em; }
.text-h3 { font-size: 1.375rem; line-height: 1.25; font-weight: 600; letter-spacing: -0.015em; }
.text-h4 { font-size: 1.125rem; line-height: 1.3; font-weight: 600; letter-spacing: -0.01em; }
.text-body-lg { font-size: 1.125rem; line-height: 1.5; letter-spacing: -0.011em; }
.text-body { font-size: 1rem; line-height: 1.5; letter-spacing: -0.011em; }
.text-small { font-size: 0.875rem; line-height: 1.4; letter-spacing: -0.006em; }
.text-xs { font-size: 0.75rem; line-height: 1.4; letter-spacing: -0.003em; }
```

### 6. Acceptance Tests

Each BUILD file MUST include 5-12 concrete, verifiable tests:
- Use curl commands for API endpoints
- Use browser checks for UI
- Specify exact expected output
- Make tests independent (runnable in any order)

### 7. File Paths

All file paths are relative to `pm-interview-coach/` root:

```
pm-interview-coach/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── static/
├── data/
├── scripts/
├── tests/
└── requirements.txt
```

## Task Specifications (What Each BUILD File Contains)

### BUILD_02_BASE_TEMPLATES.md
**What to build:**
- Base layout template (extends portfolio base.html)
- App-specific nav (Home | History | Progress)
- Footer
- Shared CSS overrides (app.css)

**Dependencies:** None
**Complexity:** Simple (~400 lines)

### BUILD_03_QUESTION_LOADER.md
**What to build:**
- Python script: `scripts/load_questions.py`
- Parse Munna Kaka markdown files (7 categories)
- Parse PM Questions.xlsx
- Extract: question text, category, difficulty, frameworks
- Bulk insert into database

**Dependencies:** Task 1 (needs Question model)
**Complexity:** Medium-High (~600 lines)

### BUILD_04_AI_EVALUATOR.md
**What to build:**
- Service: `app/services/evaluator.py`
- Claude API integration (Anthropic SDK)
- 7 category-specific system prompts (Product Design, Strategy, Execution, Analytical, Project Management, App Critique, Cross-Functional)
- JSON response schema: `{overall_score, framework_score, structure_score, completeness_score, strengths[], improvements[], suggested_framework, example_point}`
- Error handling + retry logic

**Dependencies:** Task 1 (needs Attempt model)
**Complexity:** High (~900 lines)

### BUILD_05_PRACTICE_UI.md
**What to build:**
- Template: `app/templates/practice.html`
- Router: `app/routers/practice.py`
- Service: `app/services/question_selector.py` (random weighted selection)
- Question display component
- Timer component (optional 5/10/15 min countdown)
- Answer textarea + validation (min 50 chars)
- Submit route → calls AI evaluator → returns feedback
- Feedback section: scores, radar chart (Chart.js), strengths/improvements
- Try Again / Next Question buttons

**Dependencies:** Tasks 1, 2, 4
**Complexity:** High (~1100 lines)

### BUILD_06_LANDING_HISTORY.md
**What to build:**
- Template: `app/templates/index.html` (landing page)
- Template: `app/templates/history.html`
- Router: `app/routers/pages.py`
- Landing: 7 category cards (icon, name, question count, avg score progress ring)
- History: filterable table (category, date range, score range)
- Empty states

**Dependencies:** Tasks 1, 2
**Complexity:** Medium (~800 lines)

### BUILD_07_PROGRESS_DASHBOARD.md
**What to build:**
- Template: `app/templates/progress.html`
- Router: `app/routers/stats.py`
- Service: `app/services/stats_engine.py`
- Summary cards: Total Practiced, Avg Score, Practice Streak, Weakest Category
- Chart.js visualizations:
  - Score trend line chart (per category, toggleable)
  - Category performance bar chart
  - Practice heatmap (GitHub-style)

**Dependencies:** Tasks 1, 2
**Complexity:** Medium-High (~900 lines)

### BUILD_08_HTMX_INTERACTIONS.md
**What to build:**
- Partial templates:
  - `app/templates/partials/question_card.html`
  - `app/templates/partials/feedback.html`
  - `app/templates/partials/history_table.html`
- HTMX attributes on existing templates
- Next Question (swap question card)
- Try Again (reset form)
- Filter History (update table)
- Loading indicators

**Dependencies:** Tasks 5, 6, 7
**Complexity:** Medium (~700 lines)

## Quality Checklist

Before submitting each BUILD file, verify:

- [ ] All 8 sections are present in the correct order
- [ ] Color system is pasted inline in Section 3 (not referenced)
- [ ] Typography classes are pasted inline in Section 3
- [ ] All referenced files are included with FULL text (not file paths)
- [ ] Sample data is included inline
- [ ] Acceptance tests are concrete and runnable
- [ ] File paths match the project structure tree
- [ ] No external dependencies (React, npm, webpack, etc.)
- [ ] All colors use CSS variables (no hardcoded hex values)

## Output Format

Create each BUILD file as a standalone markdown file in this folder:
- `BUILD_02_BASE_TEMPLATES.md`
- `BUILD_03_QUESTION_LOADER.md`
- etc.

Each file should be 400-1100 lines (see complexity estimates above).

## Example Reference

Study `BUILD_01_DATABASE_MODELS.md` in this folder to see the exact format, tone, and level of detail expected.

## Questions?

If anything is unclear, refer back to:
1. `FRAMEWORK_STRATEGY_TO_TASKS.md` (the meta-framework)
2. `BUILD_01_DATABASE_MODELS.md` (the reference example)
3. `02_PM_INTERVIEW_COACH.md` (the product strategy)

Do NOT deviate from the template structure. Do NOT skip sections. Do NOT reference external files — paste everything inline.

---

**Start with BUILD_02_BASE_TEMPLATES.md and work through BUILD_08 in order.**

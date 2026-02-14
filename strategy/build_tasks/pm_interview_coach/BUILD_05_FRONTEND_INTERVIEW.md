# BUILD_05_FRONTEND_INTERVIEW.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task builds the core interview practice UI and routes. It renders questions, accepts answers, calls the evaluator, and shows feedback.

**Preparation (Required Reading):**
1. Read `README.md`
2. Read `BUILD_01_DATABASE_MODELS.md`
3. Read `BUILD_03_INTERVIEW_SESSIONS.md`
4. Read `BUILD_04_CLAUDE_EVALUATOR.md`

**Dependency Graph (Build Order):**
```
Phase 1: BUILD_01, BUILD_02
Phase 2: BUILD_03, BUILD_04
Phase 3: BUILD_05 (this task)
Phase 4: BUILD_06, BUILD_07, BUILD_08
```

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | FastAPI | Async routes |
| Templates | Jinja2 | Server-rendered |
| Styling | Tailwind (CDN) | Utility classes only |
| Interactivity | HTMX (CDN) | Partial swaps |
| Charts | Chart.js (CDN) | Radar chart |
| DB | SQLAlchemy async | Session + Attempts |
| AI | Anthropic SDK | Evaluator |

**Do NOT use:** React/Vue, client-side routers, or JS build tools.

---

## Section 3: Design System

### Color Tokens
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

### Typography Scale
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

---

## Section 4: Coding Conventions

- No business logic in templates
- Use HTMX for form submission + feedback swap
- Chart.js initialization in `static/js/main.js`
- Keep routes thin, delegate to services

---

## Section 5: The Task

### Overview

Implement the practice interview flow:
- Render a question
- Start optional timer
- Accept answer
- Evaluate with Claude
- Save attempt + update session stats
- Render feedback

### Routes

**Pages:**
- `GET /practice/{category}`
- `GET /practice/random`

**API:**
- `POST /api/practice/submit`

### Files to Create / Update

- `app/routers/practice.py`
- `app/services/question_selector.py`
- `app/templates/practice.html`
- `app/templates/partials/feedback.html`
- `app/static/js/main.js`
- `app/routers/__init__.py`
- `app/main.py`

### Inline Reference Files

#### `app/services/evaluator.py` (from BUILD_04)
```python
# full evaluator file from BUILD_04
```

#### `app/services/session_manager.py` (from BUILD_03)
```python
# full session manager file from BUILD_03
```

---

## Section 6: Expected Output

1. `app/routers/practice.py`
2. `app/services/question_selector.py`
3. `app/templates/practice.html`
4. `app/templates/partials/feedback.html`
5. `app/static/js/main.js`
6. `app/routers/__init__.py`
7. `app/main.py`

---

## Section 7: Project Structure

```
pm-interview-coach/
├── app/
│   ├── routers/
│   │   ├── practice.py
│   │   └── __init__.py
│   ├── services/
│   │   └── question_selector.py
│   ├── templates/
│   │   ├── practice.html
│   │   └── partials/
│   │       └── feedback.html
│   └── static/
│       └── js/
│           └── main.js
```

---

## Section 8: Acceptance Test

### Test 1: Practice Page
- Visit `/practice/product_design`
- Question card renders

### Test 2: Submit Answer
- Enter >50 chars
- Feedback partial loads

### Test 3: Random Question
- Visit `/practice/random`
- Question renders

---

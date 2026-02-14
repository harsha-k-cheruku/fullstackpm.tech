# BUILD_08_HTMX_INTERACTIONS.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task adds HTMX partials and interactions for a smoother UI: next question swaps, feedback swaps, history filtering, and stats card refresh.

**What This Task Builds:**
- HTMX endpoints in `app/routers/api.py`
- Partial templates for question cards, history table, stats cards
- Wiring into existing pages (practice, history, progress)

This task **depends on Tasks 5, 6, 7**.

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Notes |
|-------|-----------|-------|
| HTMX | htmx.org | CDN |
| Backend | FastAPI | Async routes |
| Templates | Jinja2 | Partials |

**Do NOT use:** JS frameworks.

---

## Section 3: Design System

(identical to previous tasks)

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

- Partials must be self-contained
- HTMX requests should return partial HTML only
- Use `hx-target` and `hx-swap` explicitly

---

## Section 5: The Task

### Overview

Add HTMX-driven partial updates for:
1. Next Question (practice page)
2. Try Again (feedback reset)
3. Filter History (history page)
4. Refresh Stats Cards (progress page)

### Endpoints

**HTMX Partials:**
- `GET /partials/question-card/{id}`
- `POST /partials/feedback`
- `GET /partials/history-table`
- `GET /partials/stats-cards`

### Files to Create / Update

- `app/routers/api.py`
- `app/templates/partials/question_card.html`
- `app/templates/partials/history_table.html`
- `app/templates/partials/stats_cards.html` (ensure HTMX compatibility)
- `app/templates/partials/feedback.html` (update with Try Again button)
- `app/templates/history.html` (wire filters)
- `app/templates/practice.html` (wire next/try again)
- `app/templates/progress.html` (wire stats refresh)
- `app/routers/__init__.py` (update)
- `app/main.py` (include api router)

### Behavior Details

**Next Question:**
- Button triggers `hx-get` to `/partials/question-card/{id}`
- Swap the question card only

**Try Again:**
- Button clears feedback and keeps question
- Should re-enable the form

**History Filter:**
- Filter selects trigger `hx-get` to `/partials/history-table`
- Swap table body only

**Stats Refresh:**
- On page load, `hx-get` to `/partials/stats-cards`
- Swap cards partial

---

## Section 6: Expected Output

1. `app/routers/api.py`
2. `app/templates/partials/question_card.html`
3. `app/templates/partials/history_table.html`
4. `app/templates/partials/stats_cards.html` (updated)
5. `app/templates/partials/feedback.html` (updated)
6. `app/templates/history.html` (updated)
7. `app/templates/practice.html` (updated)
8. `app/templates/progress.html` (updated)
9. `app/routers/__init__.py` (updated)
10. `app/main.py` (updated)

---

## Section 7: Project Structure

```
pm-interview-coach/
├── app/
│   ├── routers/
│   │   └── api.py
│   ├── templates/
│   │   └── partials/
│   │       ├── question_card.html
│   │       ├── history_table.html
│   │       └── stats_cards.html
```

---

## Section 8: Acceptance Test

### Test 1: HTMX Loads
- Visit `/practice/product_design`
- Click "Next Question" and verify swap

### Test 2: History Filter
- Visit `/history` and change category filter
- Table updates without full page reload

### Test 3: Stats Cards
- Visit `/progress`
- Cards render after HTMX request

---

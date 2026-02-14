# BUILD_06_FRONTEND_DASHBOARD.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task builds the user dashboard and history pages powered by session/attempt data. It depends on auth + sessions.

**Preparation (Required Reading):**
1. README.md
2. BUILD_02_AUTH_SYSTEM.md
3. BUILD_03_INTERVIEW_SESSIONS.md

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | FastAPI | Async routes |
| Templates | Jinja2 | Server-rendered |
| Styling | Tailwind (CDN) | Utility classes only |
| Charts | Chart.js (CDN) | Dashboard charts |

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

- Routes must require auth
- Use services for aggregation
- No heavy logic in templates

---

## Section 5: The Task

Build the dashboard and history pages:
- `/history` filterable table
- `/progress` with stats cards + charts

Files:
- `app/routers/pages.py`
- `app/routers/stats.py`
- `app/services/stats_engine.py`
- `app/templates/history.html`
- `app/templates/progress.html`

Inline references:
- session_manager, auth middleware, base template

---

## Section 6: Expected Output

1. `app/routers/pages.py`
2. `app/routers/stats.py`
3. `app/services/stats_engine.py`
4. `app/templates/history.html`
5. `app/templates/progress.html`

---

## Section 7: Project Structure

```
pm-interview-coach/
 app/
 routers/
 pages.py
 stats.py
 services/
 stats_engine.py
 templates/
 history.html
 progress.html
```

---

## Section 8: Acceptance Test

### Test 1
Visit `/history` and see table

### Test 2
Visit `/progress` and see charts

---

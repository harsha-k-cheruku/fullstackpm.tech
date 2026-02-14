# BUILD_07_PROGRESS_DASHBOARD.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task builds the progress dashboard with aggregate stats and charts. It provides visibility into improvement trends, weakest areas, and practice streaks.

**What This Task Builds:**
- `app/services/stats_engine.py` for aggregated stats queries
- `app/routers/stats.py` for progress page + JSON endpoints
- `app/templates/progress.html` dashboard UI
- `app/templates/partials/stats_cards.html` HTMX-ready partial
- Update `app/static/js/main.js` to initialize charts

This task **depends on Tasks 1 and 2**.

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | FastAPI | Async routes |
| DB | SQLAlchemy async | aggregation queries |
| Templates | Jinja2 | Server-rendered |
| Charts | Chart.js | CDN |

**Do NOT use:** D3, Plotly, React-based chart libs.

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

- Aggregations in service layer only
- Use SQLAlchemy `func.avg`, `func.count`, `func.date`
- Chart data should be simple arrays (labels + values)

---

## Section 5: The Task

### Overview

Build the progress dashboard UI and data services.

### Stats Required

1. **Overview Stats**
   - Total Practiced (count of attempts)
   - Average Score
   - Practice Streak (consecutive days with attempts)
   - Weakest Category (lowest avg score)

2. **Trends**
   - Score trend over time (daily avg)
   - Category breakdown (avg score per category)
   - Practice heatmap (count per day, GitHub-style)

### Endpoints

**Pages:**
- `GET /progress` — render dashboard

**API (JSON):**
- `GET /api/stats/overview`
- `GET /api/stats/by-category`
- `GET /api/stats/trend`
- `GET /api/stats/heatmap`

### Files to Create / Update

- `app/services/stats_engine.py`
- `app/routers/stats.py`
- `app/templates/progress.html`
- `app/templates/partials/stats_cards.html`
- `app/static/js/main.js` (chart init)
- `app/routers/__init__.py` (update)
- `app/main.py` (update)

### Inline Reference Files (Existing)

#### `app/models/attempt.py` (snippet)
```python
class Attempt(Base):
    __tablename__ = "practice_attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("practice_sessions.id"), nullable=False, index=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
```

---

## Section 6: Expected Output

1. `app/services/stats_engine.py`
2. `app/routers/stats.py`
3. `app/templates/progress.html`
4. `app/templates/partials/stats_cards.html`
5. `app/static/js/main.js` (updated)
6. `app/routers/__init__.py` (updated)
7. `app/main.py` (updated)

---

## Section 7: Project Structure

```
pm-interview-coach/
├── app/
│   ├── services/
│   │   └── stats_engine.py
│   ├── routers/
│   │   └── stats.py
│   ├── templates/
│   │   ├── progress.html
│   │   └── partials/
│   │       └── stats_cards.html
│   └── static/
│       └── js/
│           └── main.js
```

---

## Section 8: Acceptance Test

### Test 1: Start Server
```bash
python -m uvicorn app.main:app --reload --port 8002
```

### Test 2: Progress Page
- Visit `/progress` and verify charts render
- Stats cards show totals (not zeros after attempts exist)

---

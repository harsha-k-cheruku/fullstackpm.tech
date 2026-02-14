# BUILD_06_LANDING_HISTORY.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task builds the landing page (category cards) and the practice history page (filterable table). It is the first user-facing view of question coverage and past attempts.

**What This Task Builds:**
- `app/routers/pages.py` for landing + history routes
- `app/templates/index.html` landing page
- `app/templates/history.html` history page
- Query helpers for category counts and recent attempts

This task **depends on Tasks 1 and 2**.

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | FastAPI | Async routes |
| Templates | Jinja2 | Server-rendered |
| DB | SQLAlchemy async | via Task 1 |
| Styling | Tailwind CSS | CDN |

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

- Routes should be slim: move data aggregation to helper functions
- Use SQLAlchemy `select` + `func.count`
- Use timezone-aware dates for display

---

## Section 5: The Task

### Overview

Build the landing and history pages.

### Landing Page Requirements (`/`)

- Hero heading: "PM Interview Coach"
- 7 category cards in grid
- Each card shows category name, question count, average score
- "Surprise Me" button links to `/practice/random`

### History Page Requirements (`/history`)

- Filter bar (category + score range)
- Table columns: Date, Category, Question (truncated), Score, Time Spent
- Empty state when no attempts

### Files to Create

- `app/routers/pages.py`
- `app/templates/index.html`
- `app/templates/history.html`
- Update `app/routers/__init__.py` to export router
- Update `app/main.py` to include pages router

### Inline Reference Files (Existing)

#### `app/templates/base.html`
```html
{% extends "base.html" %}

{% block title %}PM Interview Coach{% endblock %}

{% block head %}
  <link rel="stylesheet" href="/static/css/app.css">
{% endblock %}

{% block content %}
  <div class="container py-8">
    {% block page_content %}{% endblock %}
  </div>
{% endblock %}

{% block scripts %}
  <script src="/static/js/main.js"></script>
{% endblock %}
```

#### `app/models/question.py`
```python
from sqlalchemy import Integer, String, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    subcategory: Mapped[str | None] = mapped_column(String(100), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    frameworks: Mapped[str | None] = mapped_column(Text, nullable=True)
    hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    sample_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_category_difficulty', 'category', 'difficulty'),
        Index('idx_source', 'source'),
    )
```

#### `app/models/attempt.py`
```python
from sqlalchemy import Integer, String, Text, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base

class Attempt(Base):
    __tablename__ = "practice_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("practice_sessions.id"), nullable=False, index=True)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    time_spent_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
        Index('idx_question_score', 'question_id', 'overall_score'),
    )
```

---

## Section 6: Expected Output

1. `app/routers/pages.py`
2. `app/templates/index.html`
3. `app/templates/history.html`
4. `app/routers/__init__.py` (updated)
5. `app/main.py` (updated)

---

## Section 7: Project Structure

```
pm-interview-coach/
—— app/
———— routers/
—————— pages.py
———— templates/
—————— index.html
—————— history.html
```

---

## Section 8: Acceptance Test

### Test 1: Landing Page
- Visit `/` and verify 7 category cards

### Test 2: History Page
- Visit `/history` and confirm table renders
- With no attempts, empty state message appears

---

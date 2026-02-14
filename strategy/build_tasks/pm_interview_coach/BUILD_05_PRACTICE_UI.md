# BUILD_05_PRACTICE_UI.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This is the core practice loop: display a question, accept an answer, run AI evaluation, and show feedback. It wires together models, evaluator service, and templates.

**What This Task Builds:**
- Practice routes (`app/routers/practice.py`)
- Question selection service (`app/services/question_selector.py`)
- Practice page template (`app/templates/practice.html`)
- Feedback partial (`app/templates/partials/feedback.html`)
- Timer + UI JS (`app/static/js/main.js`)
- Router wiring in `app/main.py` and `app/routers/__init__.py`

This task **depends on Tasks 1, 2, 4**.

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Version/Notes |
|-------|-----------|---------------|
| Backend | FastAPI | Async routes |
| Templates | Jinja2 | Server rendering |
| Interactivity | HTMX | Partial swaps |
| Charts | Chart.js | Reserved for later tasks |
| AI | Anthropic SDK | via evaluator service |
| DB | SQLAlchemy async | models from Task 1 |

**Do NOT use:** React/Vue, synchronous SQLAlchemy, or JS build tooling.

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

- All routes async
- No business logic in templates
- Templates should be readable: break sections with comments
- JS should be vanilla (no frameworks)

---

## Section 5: The Task

### Overview

Implement the practice flow:
1. Select a random question (category-based or weighted)
2. Render practice page with question details
3. Accept answer submission (HTMX POST)
4. Call evaluator and store attempt
5. Render feedback partial

### Endpoints

**Pages:**
- `GET /practice/{category}` — render practice page
- `GET /practice/random` — random question (weighted)

**API:**
- `POST /api/practice/submit` — evaluate answer and return feedback partial

### Question Selection Logic

Implement in `app/services/question_selector.py`:
- If category provided: random question from that category
- If no category: weighted random favoring lowest average score category
- Weight calculation: `weight = max(1, 10 - avg_score)`

### Practice Page UI

**Layout:**
- Centered column (max 768px)
- Question card with category badge + difficulty pill
- Optional timer (5/10/15 select)
- Textarea (min 6 rows, auto expand)
- Submit button with loading indicator

**Feedback Partial:**
- Overall score (large)
- Radar chart placeholder (Chart.js later)
- Strengths list (green)
- Improvements list (orange)
- Suggested framework callout

### Files to Create / Update

- `app/routers/practice.py` (new)
- `app/services/question_selector.py` (new)
- `app/templates/practice.html` (new)
- `app/templates/partials/feedback.html` (new)
- `app/static/js/main.js` (new or updated)
- `app/routers/__init__.py` (update)
- `app/main.py` (update to include router)

### Inline Reference Files (Existing)

#### `app/templates/base.html` (from Task 2)
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

#### `app/services/evaluator.py` (from Task 4)
```python
from dataclasses import dataclass
from typing import List
import json
import logging
from anthropic import AsyncAnthropic
from pydantic import BaseModel, Field, ValidationError
from app.config import settings

logger = logging.getLogger(__name__)

class EvaluationSchema(BaseModel):
    overall_score: float = Field(..., ge=1.0, le=10.0)
    framework_score: float = Field(..., ge=1.0, le=10.0)
    structure_score: float = Field(..., ge=1.0, le=10.0)
    completeness_score: float = Field(..., ge=1.0, le=10.0)
    strengths: List[str]
    improvements: List[str]
    suggested_framework: str | None = None
    example_point: str | None = None

@dataclass
class EvaluationResult:
    overall_score: float
    framework_score: float
    structure_score: float
    completeness_score: float
    strengths: list[str]
    improvements: list[str]
    suggested_framework: str | None
    example_point: str | None
    raw_json: str

class EvaluationError(RuntimeError):
    pass

async def evaluate_answer(category: str, question: str, answer: str) -> EvaluationResult:
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    system_prompt = f"You are an expert PM interviewer. Category: {category}. Return JSON only."
    user_prompt = f"Question: {question}\nAnswer: {answer}\nReturn JSON." 

    try:
        response = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=settings.anthropic_max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw_text = response.content[0].text
        payload = json.loads(raw_text)
        parsed = EvaluationSchema(**payload)
    except (ValidationError, json.JSONDecodeError, Exception) as exc:
        logger.error("Evaluation failed", exc_info=True)
        raise EvaluationError("Claude response invalid") from exc

    return EvaluationResult(
        overall_score=parsed.overall_score,
        framework_score=parsed.framework_score,
        structure_score=parsed.structure_score,
        completeness_score=parsed.completeness_score,
        strengths=parsed.strengths,
        improvements=parsed.improvements,
        suggested_framework=parsed.suggested_framework,
        example_point=parsed.example_point,
        raw_json=json.dumps(payload),
    )
```

---

## Section 6: Expected Output

1. `app/routers/practice.py`
2. `app/services/question_selector.py`
3. `app/templates/practice.html`
4. `app/templates/partials/feedback.html`
5. `app/static/js/main.js`
6. `app/routers/__init__.py` (updated)
7. `app/main.py` (updated)

---

## Section 7: Project Structure

```
pm-interview-coach/
—— app/
———— routers/
—————— practice.py
———— services/
—————— question_selector.py
———— templates/
—————— practice.html
—————— partials/
———————— feedback.html
———— static/
—————— js/
———————— main.js
```

---

## Section 8: Acceptance Test

### Test 1: Start Server
```bash
python -m uvicorn app.main:app --reload --port 8002
```

### Test 2: Practice Page
- Visit `http://localhost:8002/practice/product_design`
- You should see a question card + answer box

### Test 3: Submit Answer
- Enter at least 50 chars and submit
- Feedback section should render without page reload

---

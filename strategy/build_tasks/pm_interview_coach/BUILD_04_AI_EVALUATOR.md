# BUILD_04_AI_EVALUATOR.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task implements the AI evaluation layer. It provides a service that calls Anthropic Claude, validates structured JSON output, and stores the evaluation results for each attempt. All practice UI work depends on this service.

**What This Task Builds:**
- `app/services/evaluator.py` for prompt construction + Claude calls
- Evaluation JSON schema + validation
- `tests/test_evaluator.py` with mocked Anthropic responses

This task **depends on Task 1** (database models + config).

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Version/Notes |
|-------|-----------|---------------|
| **Runtime** | Python | 3.11+ |
| **AI SDK** | anthropic | 0.18.x |
| **Validation** | Pydantic | v2 |
| **HTTP** | httpx | already in requirements |
| **Testing** | pytest + pytest-asyncio | async mocks |

**Do NOT use:** OpenAI SDK, LangChain, or any prompt templating library.

---

## Section 3: Design System

This section defines the complete design system used across the PM Interview Coach project. All UI components in subsequent tasks must use these tokens.

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

### Font Loading

```html
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5/index.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## Section 4: Coding Conventions

### Python
- Type hints mandatory
- Async functions only
- Use `pydantic.BaseModel` for validation
- Log errors with context

### JSON Parsing
- Strictly parse the model output with Pydantic
- If parsing fails: raise a custom `EvaluationError`
- Store raw JSON response in `raw_eval_json`

---

## Section 5: The Task

### Overview

Build the AI evaluation service for PM Interview Coach:
1. Construct category-specific prompts
2. Call Anthropic Claude API
3. Parse structured JSON response
4. Return strongly-typed evaluation result

### Required JSON Response Format

```json
{
  "overall_score": 7.5,
  "framework_score": 8.0,
  "structure_score": 7.0,
  "completeness_score": 6.5,
  "strengths": ["Clear framing", "Good tradeoff analysis"],
  "improvements": ["Missing metrics", "No competitive analysis"],
  "suggested_framework": "CIRCLES",
  "example_point": "Mention how you'd validate demand with a prototype"
}
```

### Prompt Template

- System prompt: evaluator persona + category-specific framework focus
- User prompt: question + answer + time spent
- Enforce JSON-only response (no markdown)

### Categories + Frameworks

| Category | Frameworks | Focus |
|----------|-----------|-------|
| product_design | CIRCLES, Design Thinking | User empathy, solution breadth |
| strategy | SWOT, Porter's | Market analysis, strategy clarity |
| execution | RICE, MoSCoW | Prioritization rigor |
| analytical | Fermi, Hypothesis | Decomposition, assumptions |
| project_management | Agile, RACI | Planning, risks, dependencies |
| app_critique | HEART, Heuristics | Systematic critique |
| cross_functional | STAR, Stakeholder Mapping | Conflict resolution |

### Files to Create

1. `app/services/evaluator.py`
2. `tests/test_evaluator.py`
3. Update `app/services/__init__.py`

### Inline Reference Files (Existing)

#### `app/config.py`
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PM Interview Coach"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./pm_interview_coach.db"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_max_tokens: int = 2000
    host: str = "0.0.0.0"
    port: int = 8002
    reload: bool = True
    cors_origins: list[str] = ["http://localhost:8002", "http://127.0.0.1:8002"]
    session_cookie_name: str = "pm_coach_session"
    session_max_age: int = 86400 * 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
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
    framework_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    structure_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    completeness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    improvements: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggested_framework: Mapped[str | None] = mapped_column(String(100), nullable=True)
    example_point: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_eval_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
        Index('idx_question_score', 'question_id', 'overall_score'),
    )
```

---

## Section 6: Expected Output

1. **`app/services/evaluator.py`** — Claude evaluation service
2. **`app/services/__init__.py`** — export evaluator
3. **`tests/test_evaluator.py`** — pytest coverage

### Output Rules
- Return COMPLETE files
- File path as comment at top
- JSON parsing must be strict
- Errors must be logged

---

## Section 7: Project Structure

```
pm-interview-coach/
—— app/
———— services/
—————— evaluator.py        [THIS TASK]
—————— __init__.py          [UPDATED]
—— tests/
———— test_evaluator.py      [THIS TASK]
```

---

## Section 8: Acceptance Test

### Test 1: Unit Tests
```bash
pytest tests/test_evaluator.py
```

### Test 2: Manual Prompt Smoke Test
```bash
python - <<'PY'
import asyncio
from app.services.evaluator import evaluate_answer

async def main():
    result = await evaluate_answer(
        category="product_design",
        question="Design a parking app for shopping malls",
        answer="I would start by understanding user journeys..."
    )
    print(result)

asyncio.run(main())
PY
```

Expected: prints valid evaluation object with scores 1-10.

---

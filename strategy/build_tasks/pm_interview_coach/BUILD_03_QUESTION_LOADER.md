# BUILD_03_QUESTION_LOADER.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task populates the database by parsing the Munna Kaka markdown docs and the PM Questions XLSX into the `questions` table. It is the critical data-ingestion step that makes the question bank usable.

**What This Task Builds:**
- `scripts/load_questions.py` for end-to-end ingestion
- `tests/test_question_loader.py` for parsing + insertion sanity checks
- Updates `requirements.txt` to include XLSX dependencies

This task **depends on Task 1** (database models + config + DB setup).

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Version/Notes |
|-------|-----------|---------------|
| **Runtime** | Python | 3.11+ |
| **ORM** | SQLAlchemy | Async (from Task 1) |
| **Data Parsing** | pandas | XLSX ingestion |
| **XLSX Engine** | openpyxl | Required for pandas Excel reading |
| **Markdown Parsing** | regex / string ops | No extra deps |

**Do NOT use:** LLMs, external APIs, synchronous SQLAlchemy, or fuzzy matching libraries.

---

## Section 3: Design System

This section defines the complete design system used across the PM Interview Coach project. All UI components in subsequent tasks must use these tokens.

### Color Tokens

```css
:root {
  /* Backgrounds (cool-tinted, Slate palette) */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8FAFC;
  --color-bg-tertiary: #F1F5F9;

  /* Text (black, high contrast) */
  --color-text-primary: #000000;
  --color-text-secondary: #1D1D1F;
  --color-text-tertiary: #48484A;

  /* Borders */
  --color-border: #E2E8F0;
  --color-border-hover: #CBD5E1;

  /* Accent (Blue) */
  --color-accent: #2E8ECE;
  --color-accent-hover: #2577AD;
  --color-accent-light: #E8F4FB;
  --color-accent-dark: #1A3A52;

  /* Semantic */
  --color-success: #27AE60;
  --color-success-bg: #D5F5E3;
  --color-warning: #F1C40F;
  --color-warning-bg: #FEF9E7;
  --color-danger: #E74C3C;
  --color-danger-bg: #FADBD8;
  --color-info: #2E8ECE;
}

.dark {
  /* Backgrounds (deep navy) */
  --color-bg-primary: #030712;
  --color-bg-secondary: #0F172A;
  --color-bg-tertiary: #1E293B;

  /* Text */
  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-text-tertiary: #64748B;

  /* Borders */
  --color-border: #1E293B;
  --color-border-hover: #334155;

  /* Accent overrides for dark */
  --color-accent-light: #172554;

  /* Semantic overrides for dark */
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
- Type hints for all functions
- Async database operations only
- Use `pathlib.Path` for filesystem paths
- Use structured logging (logging module)

### Parsing Rules
- Normalize whitespace to single spaces
- Strip leading numbering (`1.`, `-`, `Q:`)
- Ignore empty lines and section headers
- Deduplicate by `question_text` + `category`

---

## Section 5: The Task

### Overview

Build the ingestion pipeline that loads questions from:
- `data/munna_kaka/*.md`
- `data/pm_questions.xlsx`

And inserts them into the `questions` table using async SQLAlchemy.

### Input Data Requirements

**Munna Kaka Markdown Format (robust parsing):**
- Questions may appear as:
  - `Q: How would you design X?`
  - `1. Design a calendar app for students.`
  - `- What metrics matter for a ride-sharing marketplace?`
  - `### Design a payments flow for freelancers`
- Ignore lines that are:
  - Markdown headings that are NOT questions (e.g., `## Frameworks`)
  - Short lines (< 15 characters)
  - Lines containing only URLs

**XLSX Format (`pm_questions.xlsx`):**
- Required columns: `category`, `question`
- Optional columns: `subcategory`, `difficulty`, `source`, `frameworks`, `hint`
- If optional columns missing, fill with sensible defaults

### Category Normalization

Map file names to categories:
- `product_design.md` -> `product_design`
- `strategy.md` -> `strategy`
- `execution.md` -> `execution`
- `analytical.md` -> `analytical`
- `project_management.md` -> `project_management`
- `app_critique.md` -> `app_critique`
- `cross_functional.md` -> `cross_functional`

### Loader Rules

1. Parse all markdown questions
2. Parse all XLSX questions
3. Normalize fields (trim, lower category, default difficulty)
4. Validate question length >= 15 chars
5. Deduplicate within run (set of `(category, question_text)`)
6. Insert only new questions (skip existing in DB)
7. Print summary: loaded/inserted/skipped counts

### Files to Create

1. `scripts/load_questions.py`
2. `tests/test_question_loader.py`
3. Update `requirements.txt`

### Inline Reference Files (Existing)

#### `app/config.py`
```python
"""
Application configuration using Pydantic Settings.
Loads from environment variables and .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""

    # App metadata
    app_name: str = "PM Interview Coach"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./pm_interview_coach.db"
    # For PostgreSQL: "postgresql+asyncpg://user:password@localhost/pm_interview_coach"

    # Anthropic API
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_max_tokens: int = 2000

    # Server
    host: str = "0.0.0.0"
    port: int = 8002
    reload: bool = True

    # CORS (for local development)
    cors_origins: list[str] = ["http://localhost:8002", "http://127.0.0.1:8002"]

    # Session management
    session_cookie_name: str = "pm_coach_session"
    session_max_age: int = 86400 * 30  # 30 days

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

# Global settings instance
settings = Settings()
```

#### `app/database.py`
```python
"""
Database connection and session management.
Uses async SQLAlchemy with SQLite (dev) or PostgreSQL (prod).
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.config import settings

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db() -> None:
    await engine.dispose()
```

#### `app/models/question.py`
```python
from sqlalchemy import Integer, String, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base

class Question(Base):
    """Interview question from question bank."""
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        Index('idx_category_difficulty', 'category', 'difficulty'),
        Index('idx_source', 'source'),
    )

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, category='{self.category}', difficulty='{self.difficulty}')>"
```

#### `requirements.txt` (current from Task 1)
```txt
fastapi==0.109.2
uvicorn[standard]==0.27.1
sqlalchemy[asyncio]==2.0.27
alembic==1.13.1
aiosqlite==0.19.0
asyncpg==0.29.0
pydantic==2.6.1
pydantic-settings==2.1.0
python-dotenv==1.0.1
anthropic==0.18.1
jinja2==3.1.3
httpx==0.26.0
pytest==8.0.0
pytest-asyncio==0.23.4
pytest-cov==4.1.0
```

---

## Section 6: Expected Output

After completing this task, you should produce the following files:

1. **`scripts/load_questions.py`** — End-to-end ingestion script
2. **`tests/test_question_loader.py`** — Unit tests for parsing + DB insertion
3. **`requirements.txt`** — Updated to include `pandas` and `openpyxl`

### Output Rules

- Return COMPLETE files
- Include file path as a comment at the top of each file
- All database operations async
- No raw SQL

---

## Section 7: Project Structure

```
pm-interview-coach/
├── scripts/
│   └── load_questions.py          [THIS TASK]
├── tests/
│   └── test_question_loader.py    [THIS TASK]
└── requirements.txt               [UPDATED]
```

---

## Section 8: Acceptance Test

### Test 1: Install New Deps
```bash
pip install -r requirements.txt
```

### Test 2: Run Loader
```bash
python scripts/load_questions.py
```
Expected output:
```
Loaded 200 questions from munna_kaka docs
Loaded 150 questions from pm_questions.xlsx
Inserted 320 new questions
Skipped 30 duplicates
```

### Test 3: Query DB
```bash
sqlite3 pm_interview_coach.db "SELECT category, COUNT(*) FROM questions GROUP BY category;"
```

Expected: 7 categories with non-zero counts.

---

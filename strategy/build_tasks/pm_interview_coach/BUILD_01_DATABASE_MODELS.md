# BUILD_01_DATABASE_MODELS.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This is the foundational task for the entire PM Interview Coach project. It establishes the database schema, creates SQLAlchemy models for questions, practice attempts, and practice sessions, sets up Alembic for migrations, configures the database connection layer, and scaffolds the FastAPI application structure. Every subsequent task depends on these models being in place.

**What This Task Builds:**
- SQLAlchemy async models (Question, Attempt, Session)
- Alembic migration configuration and initial migration
- Database connection setup with async SQLAlchemy
- Application configuration with Pydantic Settings
- FastAPI app scaffold with lifespan context manager
- Requirements.txt with all dependencies
- Sample seed data script for testing

This task has **zero dependencies** — it can be built immediately. After completion, the FastAPI app will start successfully (with no routes yet), and the database tables will exist.

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Version/Notes |
|-------|-----------|---------------|
| **Runtime** | Python | 3.11+ (required for async features) |
| **Backend Framework** | FastAPI | Latest (0.109+), async route handlers |
| **Database** | SQLite | For development (PostgreSQL for production) |
| **ORM** | SQLAlchemy | 2.0+ with async support (`AsyncSession`) |
| **Migrations** | Alembic | Latest, async engine support |
| **Validation** | Pydantic | 2.0+ (via FastAPI dependency) |
| **Settings** | Pydantic Settings | For environment variable management |
| **AI API** | Anthropic SDK | For Claude API (not used in this task, but included in requirements) |
| **Templating** | Jinja2 | Via FastAPI dependency |
| **ASGI Server** | Uvicorn | With `--reload` for development |

**Do NOT use:**
- Django ORM or any other ORM
- Synchronous SQLAlchemy patterns (use async/await)
- MongoDB, NoSQL databases
- TypeORM, Prisma, or any Node.js tools
- Flask, Django, or any other Python web framework
- Raw SQL queries (use SQLAlchemy ORM)

**Development Tools:**
- `python-dotenv` for environment variable loading
- `aiosqlite` for async SQLite support

---

## Section 3: Design System

This section defines the complete design system used across the PM Interview Coach project. All UI components in subsequent tasks will reference these tokens.

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
.text-display {
  font-size: 3.5rem;        /* 56px */
  line-height: 1.05;
  font-weight: 700;
  letter-spacing: -0.04em;
}

.text-h1 {
  font-size: 2.5rem;        /* 40px */
  line-height: 1.1;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.text-h2 {
  font-size: 1.75rem;       /* 28px */
  line-height: 1.2;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.text-h3 {
  font-size: 1.375rem;      /* 22px */
  line-height: 1.25;
  font-weight: 600;
  letter-spacing: -0.015em;
}

.text-h4 {
  font-size: 1.125rem;      /* 18px */
  line-height: 1.3;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.text-body-lg {
  font-size: 1.125rem;      /* 18px */
  line-height: 1.5;
  letter-spacing: -0.011em;
}

.text-body {
  font-size: 1rem;          /* 16px */
  line-height: 1.5;
  letter-spacing: -0.011em;
}

.text-small {
  font-size: 0.875rem;      /* 14px */
  line-height: 1.4;
  letter-spacing: -0.006em;
}

.text-xs {
  font-size: 0.75rem;       /* 12px */
  line-height: 1.4;
  letter-spacing: -0.003em;
}
```

### Font Loading

```html
<!-- Geist Sans (primary font) via jsDelivr/Fontsource CDN -->
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5/index.css">

<!-- JetBrains Mono (monospace) via Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**Font Stack:**
- Body: `font-family: 'Geist Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;`
- Monospace: `font-family: 'JetBrains Mono', 'Courier New', monospace;`

---

## Section 4: Coding Conventions

### Python Style

**Type Hints (Mandatory):**
```python
from typing import Optional, List
from datetime import datetime

async def get_question_by_id(question_id: int) -> Optional[Question]:
    """Fetch a question by ID."""
    pass

async def get_attempts_by_session(session_id: str) -> List[Attempt]:
    """Fetch all attempts for a session."""
    pass
```

**Import Ordering:**
```python
# 1. Standard library
import os
from datetime import datetime, timezone
from typing import Optional, List

# 2. Third-party packages
from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# 3. Local application imports
from app.database import get_db
from app.models.question import Question
```

**Async/Await Patterns:**
```python
# ✅ Correct: Use async with async engines
async def create_question(db: AsyncSession, data: dict) -> Question:
    question = Question(**data)
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question

# ❌ Wrong: Don't mix sync and async
def create_question(db: AsyncSession, data: dict) -> Question:
    db.add(question)
    db.commit()  # This will fail
```

**Pydantic Models:**
```python
from pydantic import BaseModel, Field
from datetime import datetime

class QuestionCreate(BaseModel):
    category: str = Field(..., description="Question category")
    question_text: str = Field(..., min_length=10)

class QuestionResponse(BaseModel):
    id: int
    category: str
    question_text: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
```

**SQLAlchemy 2.0 Patterns:**
```python
# ✅ Use declarative_base and mapped_column
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
```

**Datetime Handling:**
```python
from datetime import datetime, timezone

# ✅ Always use timezone-aware datetimes
created_at = datetime.now(timezone.utc)

# ✅ Store UTC in database, convert to local in templates
def utc_now() -> datetime:
    return datetime.now(timezone.utc)
```

**Environment Variables:**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./pm_interview_coach.db"
    anthropic_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
```

### Database Conventions

**Table Naming:**
- Use plural, lowercase, snake_case: `questions`, `practice_attempts`, `practice_sessions`

**Column Naming:**
- Use snake_case: `question_text`, `created_at`, `overall_score`
- Suffix foreign keys with `_id`: `question_id`, `session_id`

**Indexes:**
- Always index foreign keys
- Index columns used in WHERE clauses frequently: `category`, `session_id`, `created_at`

**JSON Columns:**
- Use SQLAlchemy's `JSON` type for PostgreSQL, `Text` with manual JSON encoding for SQLite
- Store arrays as JSON: `frameworks`, `strengths`, `improvements`

### Error Handling

```python
from fastapi import HTTPException

# ✅ Use HTTPException for API errors
async def get_question(question_id: int, db: AsyncSession):
    question = await db.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

# ✅ Log errors before raising
import logging
logger = logging.getLogger(__name__)

try:
    result = await some_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Testing Conventions

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_question(client: AsyncClient, db: AsyncSession):
    """Test question creation endpoint."""
    response = await client.post("/api/questions", json={
        "category": "product_design",
        "question_text": "Design a parking app for shopping malls."
    })
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "product_design"
```

---

## Section 5: The Task

### Overview

Build the complete database layer for PM Interview Coach, including:
1. SQLAlchemy async models (Question, Attempt, Session)
2. Alembic migration setup with initial schema
3. Database connection utilities (async engine, session factory)
4. Application configuration (Pydantic Settings)
5. FastAPI application scaffold with lifespan management
6. Requirements.txt with all dependencies
7. Sample seed data for testing database setup

### Scope Boundaries

**IN SCOPE:**
- SQLAlchemy model definitions with all fields, relationships, and indexes
- Alembic configuration for async migrations
- Initial migration file creating all tables
- Database connection pattern with async context manager
- Settings class with environment variable validation
- FastAPI app initialization with lifespan (startup/shutdown)
- Requirements.txt with pinned versions
- `.env.example` file with all required variables
- Sample seed script to populate 5-10 questions for testing
- README.md with setup instructions

**OUT OF SCOPE:**
- Question loading from Munna Kaka docs or XLSX (Task 3)
- API routes for CRUD operations (Tasks 5, 6, 7)
- AI evaluation logic (Task 4)
- Templates and UI (Tasks 2, 5, 6, 7)
- Production deployment configuration (later task)

### Data Models

#### 1. Question Model

Represents a single interview question from the question bank.

**SQLAlchemy Model (`app/models/question.py`):**

```python
from sqlalchemy import Integer, String, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base

class Question(Base):
    """Interview question from question bank."""
    __tablename__ = "questions"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Core fields
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # Categories: product_design, strategy, execution, analytical,
    #             project_management, app_critique, cross_functional

    subcategory: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Example: "Mobile App Design", "Prioritization", "Metrics"

    difficulty: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    # Values: "easy", "medium", "hard"

    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    # The actual question (can be long, multi-paragraph)

    source: Mapped[str] = mapped_column(String(100), nullable=False)
    # Where this question came from: "munna_kaka_design", "pm_questions_xlsx", "manual"

    # Optional fields
    frameworks: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON array of relevant frameworks: '["CIRCLES", "STAR"]'

    hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Optional hint to guide the candidate

    sample_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Optional reference answer (for seed data)

    # Metadata
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

    # Indexes
    __table_args__ = (
        Index('idx_category_difficulty', 'category', 'difficulty'),
        Index('idx_source', 'source'),
    )

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, category='{self.category}', difficulty='{self.difficulty}')>"
```

**Pydantic Schema (`app/schemas/question.py`):**

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import json

class QuestionBase(BaseModel):
    category: str = Field(..., description="Question category")
    subcategory: Optional[str] = None
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    question_text: str = Field(..., min_length=10)
    source: str
    frameworks: Optional[str] = None
    hint: Optional[str] = None
    sample_answer: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @property
    def frameworks_list(self) -> List[str]:
        """Parse frameworks JSON string to list."""
        if not self.frameworks:
            return []
        try:
            return json.loads(self.frameworks)
        except json.JSONDecodeError:
            return []

    model_config = {"from_attributes": True}
```

#### 2. Attempt Model

Represents a single practice attempt (one question answered).

**SQLAlchemy Model (`app/models/attempt.py`):**

```python
from sqlalchemy import Integer, String, Text, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database import Base

class Attempt(Base):
    """A single practice attempt (one question answered)."""
    __tablename__ = "practice_attempts"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("practice_sessions.id"), nullable=False, index=True)

    # User's answer
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Practice metadata
    time_spent_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # How many seconds the user took to answer

    # AI Evaluation scores (1.0 to 10.0)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    framework_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    structure_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    completeness_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # AI Evaluation feedback (JSON arrays stored as text)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON: ["Strong use of CIRCLES framework", "Clear prioritization"]

    improvements: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON: ["Missing competitive analysis", "Could add metrics"]

    suggested_framework: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Example: "CIRCLES", "STAR", "RICE"

    example_point: Mapped[str | None] = mapped_column(Text, nullable=True)
    # A specific example of what was missed

    # Raw AI response (for debugging/reprocessing)
    raw_eval_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    # Relationships
    # question = relationship("Question", backref="attempts")  # Uncomment if you need reverse lookup
    # session = relationship("PracticeSession", back_populates="attempts")

    # Indexes
    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
        Index('idx_question_score', 'question_id', 'overall_score'),
    )

    def __repr__(self) -> str:
        return f"<Attempt(id={self.id}, question_id={self.question_id}, score={self.overall_score})>"
```

**Pydantic Schema (`app/schemas/attempt.py`):**

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import json

class AttemptBase(BaseModel):
    question_id: int
    session_id: str
    answer_text: str = Field(..., min_length=50)
    time_spent_sec: Optional[int] = None

class AttemptCreate(AttemptBase):
    pass

class AttemptEvaluationUpdate(BaseModel):
    """Schema for updating attempt with AI evaluation results."""
    overall_score: float = Field(..., ge=1.0, le=10.0)
    framework_score: float = Field(..., ge=1.0, le=10.0)
    structure_score: float = Field(..., ge=1.0, le=10.0)
    completeness_score: float = Field(..., ge=1.0, le=10.0)
    strengths: str  # JSON array as string
    improvements: str  # JSON array as string
    suggested_framework: Optional[str] = None
    example_point: Optional[str] = None
    raw_eval_json: Optional[str] = None

class AttemptResponse(AttemptBase):
    id: int
    overall_score: Optional[float] = None
    framework_score: Optional[float] = None
    structure_score: Optional[float] = None
    completeness_score: Optional[float] = None
    strengths: Optional[str] = None
    improvements: Optional[str] = None
    suggested_framework: Optional[str] = None
    example_point: Optional[str] = None
    created_at: datetime

    @property
    def strengths_list(self) -> List[str]:
        """Parse strengths JSON string to list."""
        if not self.strengths:
            return []
        try:
            return json.loads(self.strengths)
        except json.JSONDecodeError:
            return []

    @property
    def improvements_list(self) -> List[str]:
        """Parse improvements JSON string to list."""
        if not self.improvements:
            return []
        try:
            return json.loads(self.improvements)
        except json.JSONDecodeError:
            return []

    model_config = {"from_attributes": True}
```

#### 3. PracticeSession Model

Represents a practice session (collection of attempts in one sitting).

**SQLAlchemy Model (`app/models/session.py`):**

```python
from sqlalchemy import Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base

class PracticeSession(Base):
    """A practice session (collection of attempts in one sitting)."""
    __tablename__ = "practice_sessions"

    # Primary key (UUID as string)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    # UUID4 generated client-side or server-side

    # Session configuration
    category_filter: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    # If user chose a specific category, otherwise NULL for random

    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="standard")
    # Future: "standard", "timed", "exam", "review"

    timer_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # If user set a timer (5, 10, 15), otherwise NULL

    # Session lifecycle
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Aggregate stats (computed from attempts)
    questions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Relationships
    # attempts = relationship("Attempt", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<PracticeSession(id='{self.id}', category='{self.category_filter}', count={self.questions_count})>"
```

**Pydantic Schema (`app/schemas/session.py`):**

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class SessionBase(BaseModel):
    category_filter: Optional[str] = None
    mode: str = "standard"
    timer_minutes: Optional[int] = Field(None, ge=1, le=60)

class SessionCreate(SessionBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class SessionUpdate(BaseModel):
    """Schema for updating session stats after each attempt."""
    questions_count: int
    avg_score: Optional[float] = None
    ended_at: Optional[datetime] = None

class SessionResponse(SessionBase):
    id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    questions_count: int
    avg_score: Optional[float] = None

    model_config = {"from_attributes": True}
```

### Database Connection Setup

**File: `app/database.py`**

```python
"""
Database connection and session management.
Uses async SQLAlchemy with SQLite (dev) or PostgreSQL (prod).
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.config import settings

# Declarative base for all models
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI routes.

    Usage:
        @app.get("/questions")
        async def get_questions(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Question))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db() -> None:
    """
    Create all tables in the database.
    Called during app startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db() -> None:
    """
    Close database connections.
    Called during app shutdown.
    """
    await engine.dispose()
```

### Application Configuration

**File: `app/config.py`**

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

**File: `.env.example`**

```bash
# PM Interview Coach — Environment Variables
# Copy this file to .env and fill in your values

# App Configuration
APP_NAME="PM Interview Coach"
DEBUG=false

# Database
# For SQLite (development):
DATABASE_URL=sqlite+aiosqlite:///./pm_interview_coach.db

# For PostgreSQL (production):
# DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/pm_interview_coach

# Anthropic API (required for AI evaluation)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=2000

# Server
HOST=0.0.0.0
PORT=8002
RELOAD=true

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:8002,http://127.0.0.1:8002
```

### FastAPI Application Scaffold

**File: `app/main.py`**

```python
"""
PM Interview Coach — FastAPI Application
Main entry point for the application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from app.config import settings
from app.database import init_db, close_db

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    Replaces deprecated @app.on_event decorators.
    """
    # Startup
    logger.info("Starting PM Interview Coach...")
    logger.info(f"Database URL: {settings.database_url}")

    # Initialize database (create tables if they don't exist)
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down PM Interview Coach...")
    await close_db()
    logger.info("Database connections closed")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered PM interview practice with structured feedback",
    lifespan=lifespan,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB health check
        "anthropic_api": "configured" if settings.anthropic_api_key else "missing"
    }

# Import and include routers (will be added in subsequent tasks)
# from app.routers import pages, practice, stats
# app.include_router(pages.router)
# app.include_router(practice.router, prefix="/api/practice", tags=["practice"])
# app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
```

### Alembic Migration Setup

**File: `alembic.ini`**

```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
timezone = UTC

# max length of characters to apply to the
# "slug" field
truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
sourceless = false

# version location specification; This defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
version_locations = %(here)s/alembic/versions

# output encoding used when revision files
# are written from script.py.mako
output_encoding = utf-8

sqlalchemy.url = sqlite+aiosqlite:///./pm_interview_coach.db

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

**File: `alembic/env.py`**

```python
"""Alembic environment configuration for async migrations."""
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import your models' Base
from app.database import Base
from app.config import settings

# Import all models so Alembic can detect them
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.session import PracticeSession

# this is the Alembic Config object
config = context.config

# Override sqlalchemy.url from settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**File: `alembic/versions/20260212_1430_001_initial_schema.py`**

```python
"""Initial schema: questions, practice_attempts, practice_sessions

Revision ID: 001
Revises:
Create Date: 2026-02-12 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Create initial tables."""
    # Create questions table
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('subcategory', sa.String(length=100), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('source', sa.String(length=100), nullable=False),
        sa.Column('frameworks', sa.Text(), nullable=True),
        sa.Column('hint', sa.Text(), nullable=True),
        sa.Column('sample_answer', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_category_difficulty', 'questions', ['category', 'difficulty'])
    op.create_index('idx_source', 'questions', ['source'])
    op.create_index(op.f('ix_questions_category'), 'questions', ['category'])

    # Create practice_sessions table
    op.create_table(
        'practice_sessions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('category_filter', sa.String(length=50), nullable=True),
        sa.Column('mode', sa.String(length=20), nullable=False, server_default='standard'),
        sa.Column('timer_minutes', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('questions_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('avg_score', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_practice_sessions_category_filter'), 'practice_sessions', ['category_filter'])
    op.create_index(op.f('ix_practice_sessions_started_at'), 'practice_sessions', ['started_at'])

    # Create practice_attempts table
    op.create_table(
        'practice_attempts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=36), nullable=False),
        sa.Column('answer_text', sa.Text(), nullable=False),
        sa.Column('time_spent_sec', sa.Integer(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('framework_score', sa.Float(), nullable=True),
        sa.Column('structure_score', sa.Float(), nullable=True),
        sa.Column('completeness_score', sa.Float(), nullable=True),
        sa.Column('strengths', sa.Text(), nullable=True),
        sa.Column('improvements', sa.Text(), nullable=True),
        sa.Column('suggested_framework', sa.String(length=100), nullable=True),
        sa.Column('example_point', sa.Text(), nullable=True),
        sa.Column('raw_eval_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['practice_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_question_score', 'practice_attempts', ['question_id', 'overall_score'])
    op.create_index('idx_session_created', 'practice_attempts', ['session_id', 'created_at'])
    op.create_index(op.f('ix_practice_attempts_created_at'), 'practice_attempts', ['created_at'])
    op.create_index(op.f('ix_practice_attempts_question_id'), 'practice_attempts', ['question_id'])
    op.create_index(op.f('ix_practice_attempts_session_id'), 'practice_attempts', ['session_id'])

def downgrade() -> None:
    """Drop all tables."""
    op.drop_table('practice_attempts')
    op.drop_table('practice_sessions')
    op.drop_table('questions')
```

### Requirements File

**File: `requirements.txt`**

```txt
# PM Interview Coach — Python Dependencies

# Web Framework
fastapi==0.109.2
uvicorn[standard]==0.27.1

# Database
sqlalchemy[asyncio]==2.0.27
alembic==1.13.1
aiosqlite==0.19.0
asyncpg==0.29.0  # For PostgreSQL in production

# Data Validation
pydantic==2.6.1
pydantic-settings==2.1.0
python-dotenv==1.0.1

# AI API
anthropic==0.18.1

# Templating
jinja2==3.1.3

# HTTP Client (for API calls)
httpx==0.26.0

# Development Dependencies
pytest==8.0.0
pytest-asyncio==0.23.4
pytest-cov==4.1.0
```

### Sample Seed Data

**File: `scripts/seed_sample_data.py`**

```python
"""
Seed sample questions for testing database setup.
Run: python scripts/seed_sample_data.py
"""
import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, init_db
from app.models.question import Question
import json

SAMPLE_QUESTIONS = [
    {
        "category": "product_design",
        "subcategory": "Mobile App Design",
        "difficulty": "medium",
        "question_text": "Design a parking app for shopping malls.",
        "source": "sample_seed",
        "frameworks": json.dumps(["CIRCLES", "Design Thinking"]),
        "hint": "Consider user pain points at each stage: arrival, finding spot, payment, exit.",
        "sample_answer": None,
    },
    {
        "category": "strategy",
        "subcategory": "Market Entry",
        "difficulty": "hard",
        "question_text": "Should Netflix enter the live sports streaming market?",
        "source": "sample_seed",
        "frameworks": json.dumps(["Porter's Five Forces", "SWOT"]),
        "hint": "Analyze competitive landscape, cost structure, and strategic fit.",
        "sample_answer": None,
    },
    {
        "category": "execution",
        "subcategory": "Prioritization",
        "difficulty": "medium",
        "question_text": "You have 5 feature requests from major customers, but only resources for 2. How do you decide?",
        "source": "sample_seed",
        "frameworks": json.dumps(["RICE", "MoSCoW"]),
        "hint": "Consider impact, effort, strategic alignment, and customer value.",
        "sample_answer": None,
    },
    {
        "category": "analytical",
        "subcategory": "Estimation",
        "difficulty": "medium",
        "question_text": "How many pizzas are consumed in New York City each year?",
        "source": "sample_seed",
        "frameworks": json.dumps(["Fermi Estimation"]),
        "hint": "Break down into population, consumption frequency, and adjust for tourists.",
        "sample_answer": None,
    },
    {
        "category": "project_management",
        "subcategory": "Timeline Planning",
        "difficulty": "medium",
        "question_text": "Your engineering team says a feature will take 6 months. Sales promised it in 3. What do you do?",
        "source": "sample_seed",
        "frameworks": json.dumps(["Agile", "Stakeholder Management"]),
        "hint": "Focus on communication, scope negotiation, and risk mitigation.",
        "sample_answer": None,
    },
    {
        "category": "app_critique",
        "subcategory": "UX Evaluation",
        "difficulty": "easy",
        "question_text": "Critique the Uber app. What would you improve?",
        "source": "sample_seed",
        "frameworks": json.dumps(["HEART", "UX Heuristics"]),
        "hint": "Evaluate across multiple dimensions: usability, engagement, retention.",
        "sample_answer": None,
    },
    {
        "category": "cross_functional",
        "subcategory": "Conflict Resolution",
        "difficulty": "hard",
        "question_text": "Describe a time when you had to influence a stakeholder who disagreed with your approach.",
        "source": "sample_seed",
        "frameworks": json.dumps(["STAR"]),
        "hint": "Use concrete examples with measurable outcomes.",
        "sample_answer": None,
    },
]

async def seed_questions():
    """Insert sample questions into the database."""
    print("Initializing database...")
    await init_db()

    async with AsyncSessionLocal() as db:
        print(f"Seeding {len(SAMPLE_QUESTIONS)} sample questions...")

        for q_data in SAMPLE_QUESTIONS:
            question = Question(
                **q_data,
                created_at=datetime.now(timezone.utc)
            )
            db.add(question)

        await db.commit()
        print("Sample questions seeded successfully!")

        # Verify
        from sqlalchemy import select
        result = await db.execute(select(Question))
        count = len(result.scalars().all())
        print(f"Total questions in database: {count}")

if __name__ == "__main__":
    asyncio.run(seed_questions())
```

### Package Initialization Files

**File: `app/__init__.py`**

```python
"""PM Interview Coach application package."""
__version__ = "1.0.0"
```

**File: `app/models/__init__.py`**

```python
"""Database models."""
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.session import PracticeSession

__all__ = ["Question", "Attempt", "PracticeSession"]
```

**File: `app/schemas/__init__.py`**

```python
"""Pydantic schemas for request/response validation."""
from app.schemas.question import QuestionCreate, QuestionResponse
from app.schemas.attempt import AttemptCreate, AttemptResponse, AttemptEvaluationUpdate
from app.schemas.session import SessionCreate, SessionResponse, SessionUpdate

__all__ = [
    "QuestionCreate",
    "QuestionResponse",
    "AttemptCreate",
    "AttemptResponse",
    "AttemptEvaluationUpdate",
    "SessionCreate",
    "SessionResponse",
    "SessionUpdate",
]
```

---

## Section 6: Expected Output

After completing this task, you should produce the following files:

### Core Application Files

1. **`app/__init__.py`** — Package initialization with version
2. **`app/main.py`** — FastAPI application with lifespan management
3. **`app/config.py`** — Pydantic Settings configuration
4. **`app/database.py`** — Async SQLAlchemy engine and session factory

### Model Files

5. **`app/models/__init__.py`** — Models package initialization
6. **`app/models/question.py`** — Question SQLAlchemy model
7. **`app/models/attempt.py`** — Attempt SQLAlchemy model
8. **`app/models/session.py`** — PracticeSession SQLAlchemy model

### Schema Files

9. **`app/schemas/__init__.py`** — Schemas package initialization
10. **`app/schemas/question.py`** — Question Pydantic schemas
11. **`app/schemas/attempt.py`** — Attempt Pydantic schemas
12. **`app/schemas/session.py`** — Session Pydantic schemas

### Migration Files

13. **`alembic.ini`** — Alembic configuration
14. **`alembic/env.py`** — Alembic environment (async support)
15. **`alembic/versions/20260212_1430_001_initial_schema.py`** — Initial migration

### Scripts

16. **`scripts/seed_sample_data.py`** — Sample data seeding script

### Configuration Files

17. **`requirements.txt`** — Python dependencies
18. **`.env.example`** — Environment variables template
19. **`.gitignore`** — Git ignore patterns
20. **`README.md`** — Project documentation

### Output Rules

- Return COMPLETE files, not snippets or placeholders
- Include file path as a comment at the top of each file
- Use async/await throughout (no synchronous database operations)
- Follow all coding conventions from Section 4
- All models must have proper type hints (Mapped[type])
- All datetime fields must use timezone-aware datetimes (UTC)
- JSON fields (frameworks, strengths, improvements) stored as Text with manual serialization
- No features beyond this spec (no routes, no templates, no AI logic yet)

---

## Section 7: Project Structure

Below is the full project directory tree for PM Interview Coach. Files marked with `[THIS TASK]` are created in this task. Files marked with `[LATER]` will be created in subsequent tasks.

```
pm-interview-coach/
├── .env.example                      [THIS TASK]
├── .gitignore                        [THIS TASK]
├── README.md                         [THIS TASK]
├── requirements.txt                  [THIS TASK]
├── alembic.ini                       [THIS TASK]
├── pm_interview_coach.db             [Generated by app]
│
├── alembic/
│   ├── env.py                        [THIS TASK]
│   ├── script.py.mako                [Auto-generated by alembic init]
│   └── versions/
│       └── 20260212_1430_001_initial_schema.py  [THIS TASK]
│
├── app/
│   ├── __init__.py                   [THIS TASK]
│   ├── main.py                       [THIS TASK]
│   ├── config.py                     [THIS TASK]
│   ├── database.py                   [THIS TASK]
│   │
│   ├── models/
│   │   ├── __init__.py               [THIS TASK]
│   │   ├── question.py               [THIS TASK]
│   │   ├── attempt.py                [THIS TASK]
│   │   └── session.py                [THIS TASK]
│   │
│   ├── schemas/
│   │   ├── __init__.py               [THIS TASK]
│   │   ├── question.py               [THIS TASK]
│   │   ├── attempt.py                [THIS TASK]
│   │   └── session.py                [THIS TASK]
│   │
│   ├── routers/                      [LATER: Tasks 5, 6, 7]
│   │   ├── __init__.py
│   │   ├── pages.py
│   │   ├── practice.py
│   │   └── stats.py
│   │
│   ├── services/                     [LATER: Tasks 3, 4, 7]
│   │   ├── __init__.py
│   │   ├── evaluator.py
│   │   ├── question_selector.py
│   │   └── stats_engine.py
│   │
│   ├── templates/                    [LATER: Tasks 2, 5, 6, 7]
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── practice.html
│   │   ├── history.html
│   │   ├── progress.html
│   │   └── partials/
│   │       ├── question_card.html
│   │       ├── feedback.html
│   │       ├── history_table.html
│   │       └── stats_cards.html
│   │
│   └── static/                       [LATER: Tasks 2, 5, 7]
│       ├── css/
│       │   └── app.css
│       └── js/
│           └── main.js
│
├── data/                             [User-provided, not in build tasks]
│   ├── munna_kaka/
│   │   ├── product_design.md
│   │   ├── strategy.md
│   │   ├── execution.md
│   │   ├── analytical.md
│   │   ├── project_management.md
│   │   ├── app_critique.md
│   │   └── cross_functional.md
│   └── pm_questions.xlsx
│
├── scripts/
│   ├── seed_sample_data.py           [THIS TASK]
│   └── load_questions.py             [LATER: Task 3]
│
└── tests/                            [LATER: Tasks 3, 4, 7]
    ├── __init__.py
    ├── test_evaluator.py
    ├── test_question_loader.py
    └── test_stats.py
```

**Directory Counts:**
- **Created in this task:** 20 files
- **Created in later tasks:** ~25 files
- **Total project size:** ~45 files

---

## Section 8: Acceptance Test

After completing this task, run these tests to verify everything works correctly.

### Test 1: Install Dependencies

**Command:**
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed fastapi-0.109.2 uvicorn-0.27.1 sqlalchemy-2.0.27 ...
```

**Verification:** No errors during installation.

---

### Test 2: Environment Setup

**Command:**
```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY (optional for this task)
```

**Expected Output:**
- `.env` file exists with all required variables

**Verification:**
```bash
cat .env | grep DATABASE_URL
# Should output: DATABASE_URL=sqlite+aiosqlite:///./pm_interview_coach.db
```

---

### Test 3: Alembic Migrations

**Command:**
```bash
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema: questions, practice_attempts, practice_sessions
```

**Verification:**
- `pm_interview_coach.db` file created
- Tables exist in database

```bash
sqlite3 pm_interview_coach.db ".tables"
# Should output: alembic_version  practice_attempts  practice_sessions  questions
```

---

### Test 4: Database Schema Verification

**Command:**
```bash
sqlite3 pm_interview_coach.db ".schema questions"
```

**Expected Output:**
```sql
CREATE TABLE questions (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(100),
    difficulty VARCHAR(20) DEFAULT 'medium' NOT NULL,
    question_text TEXT NOT NULL,
    source VARCHAR(100) NOT NULL,
    frameworks TEXT,
    hint TEXT,
    sample_answer TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME
);
CREATE INDEX idx_category_difficulty ON questions (category, difficulty);
CREATE INDEX idx_source ON questions (source);
CREATE INDEX ix_questions_category ON questions (category);
```

**Verification:** All columns and indexes present.

---

### Test 5: Start FastAPI Server

**Command:**
```bash
python -m uvicorn app.main:app --reload --port 8002
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/pm-interview-coach']
INFO:     Uvicorn running on http://127.0.0.1:8002 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Starting PM Interview Coach...
INFO:     Database URL: sqlite+aiosqlite:///./pm_interview_coach.db
INFO:     Database initialized successfully
INFO:     Application startup complete.
```

**Verification:** No errors, server starts successfully.

---

### Test 6: Root Endpoint

**Command:**
```bash
curl http://localhost:8002/
```

**Expected Output:**
```json
{
  "app": "PM Interview Coach",
  "version": "1.0.0",
  "status": "running"
}
```

**Verification:** JSON response with correct app name and version.

---

### Test 7: Health Check Endpoint

**Command:**
```bash
curl http://localhost:8002/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "database": "connected",
  "anthropic_api": "missing"
}
```

**Verification:**
- `"status": "healthy"`
- `"database": "connected"`
- `"anthropic_api": "configured"` if you set the API key, otherwise `"missing"`

---

### Test 8: Seed Sample Data

**Command:**
```bash
python scripts/seed_sample_data.py
```

**Expected Output:**
```
Initializing database...
Seeding 7 sample questions...
Sample questions seeded successfully!
Total questions in database: 7
```

**Verification:** 7 questions inserted into database.

---

### Test 9: Query Sample Questions

**Command:**
```bash
sqlite3 pm_interview_coach.db "SELECT id, category, difficulty FROM questions LIMIT 5;"
```

**Expected Output:**
```
1|product_design|medium
2|strategy|hard
3|execution|medium
4|analytical|medium
5|project_management|medium
```

**Verification:** Questions exist with correct categories and difficulty levels.

---

### Test 10: Verify Foreign Key Relationships

**Command:**
```bash
sqlite3 pm_interview_coach.db "PRAGMA foreign_key_list(practice_attempts);"
```

**Expected Output:**
```
0|0|questions|question_id|id|NO ACTION|NO ACTION|NONE
1|0|practice_sessions|session_id|id|NO ACTION|NO ACTION|NONE
```

**Verification:** Foreign keys to `questions` and `practice_sessions` are defined.

---

### Test 11: Database Indexes

**Command:**
```bash
sqlite3 pm_interview_coach.db "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='questions';"
```

**Expected Output:**
```
idx_category_difficulty
idx_source
ix_questions_category
```

**Verification:** All indexes created correctly.

---

### Test 12: Python Model Import Test

**Command:**
```bash
python -c "from app.models import Question, Attempt, PracticeSession; print('Models imported successfully')"
```

**Expected Output:**
```
Models imported successfully
```

**Verification:** No import errors, all models accessible.

---

### Success Criteria Summary

All tests pass if:
1. ✅ Dependencies install without errors
2. ✅ Environment file created from template
3. ✅ Alembic migration runs successfully
4. ✅ Database tables created with correct schema
5. ✅ FastAPI server starts without errors
6. ✅ Root endpoint returns JSON with app info
7. ✅ Health check endpoint shows database connected
8. ✅ Sample data seeds successfully (7 questions)
9. ✅ Questions queryable via SQLite CLI
10. ✅ Foreign keys defined correctly
11. ✅ Indexes created on all specified columns
12. ✅ Python models import without errors

---

## Additional Notes

### Next Steps After This Task

Once all acceptance tests pass, you can proceed to:

- **Task 2: Base Templates** (can run in parallel with Task 3)
- **Task 3: Question Loader** (depends on Task 1)
- **Task 4: AI Evaluator** (depends on Task 1)

### Troubleshooting

**Issue: Alembic migration fails**
```bash
# Solution: Delete the database and retry
rm pm_interview_coach.db
alembic upgrade head
```

**Issue: Import errors for `app.models`**
```bash
# Solution: Ensure you're running from project root
cd pm-interview-coach/
python -c "from app.models import Question"
```

**Issue: Uvicorn not found**
```bash
# Solution: Reinstall uvicorn with standard extras
pip install "uvicorn[standard]==0.27.1"
```

**Issue: Database locked error**
```bash
# Solution: Close all database connections
# If using SQLite Browser or DB clients, close them
# Restart the FastAPI server
```

### Production Considerations (Not Required for This Task)

For production deployment:
- Replace SQLite with PostgreSQL (`DATABASE_URL=postgresql+asyncpg://...`)
- Set `DEBUG=false` in `.env`
- Use environment-specific settings (dev, staging, prod)
- Add database connection pooling configuration
- Implement database backup strategy
- Add health check for actual database connectivity (query test)

---

**End of BUILD_01_DATABASE_MODELS.md**

This task is now complete and ready to be handed to any LLM for code generation.

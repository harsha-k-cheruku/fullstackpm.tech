# BUILD_03_INTERVIEW_SESSIONS.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task implements interview session lifecycle APIs and services. It enables creating sessions, attaching attempts, updating session stats, and retrieving session history. It depends on the database models (BUILD_01) and authentication (BUILD_02).

**Preparation (Required Reading):**
1. Read `README.md` (task breakdown + dependency graph)
2. Read `BUILD_01_DATABASE_MODELS.md` (baseline models)
3. Read `BUILD_02_AUTH_SYSTEM.md` (users + auth)
4. Read `INSTRUCTIONS_FOR_LLM.md` (rules + quality standards)

**Dependency Graph (Build Order):**
```
Phase 1 (parallel):
  - BUILD_01_DATABASE_MODELS.md (done)
  - BUILD_02_AUTH_SYSTEM.md (done)

Phase 2 (after Phase 1):
  - BUILD_03_INTERVIEW_SESSIONS.md (this task)
  - BUILD_04_CLAUDE_EVALUATOR.md

Phase 3 (after Phase 2):
  - BUILD_05_FRONTEND_INTERVIEW.md
  - BUILD_06_FRONTEND_DASHBOARD.md

Phase 4 (final):
  - BUILD_07_TESTING_DEPLOYMENT.md
  - BUILD_08_INTEGRATION.md
```

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Version/Notes |
|-------|-----------|---------------|
| **Runtime** | Python | 3.11+ |
| **Backend** | FastAPI | Async route handlers |
| **ORM** | SQLAlchemy | 2.0 async |
| **DB** | SQLite | Dev; PostgreSQL in prod |
| **Templating** | Jinja2 | Server-side rendering |
| **Styling** | Tailwind (CDN) | Utility classes only |
| **Interactivity** | HTMX (CDN) | Partial updates |
| **Fonts** | Geist Sans + JetBrains Mono | Via CDN |

**Do NOT use:** React, Vue, Angular, Next.js, Flask, Django, Prisma, MongoDB, or npm tooling.

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

### Python
- Async-only route handlers
- Type hints on all functions
- Import order: stdlib → third-party → local
- Use Pydantic v2 schemas for request/response
- Datetimes are timezone-aware (UTC)

### API
- Use `/api/sessions` namespace for JSON routes
- Return 404 for missing session
- Require auth for session routes

---

## Section 5: The Task

### Overview

Build the interview session lifecycle layer:
- Create sessions
- Attach attempts
- Update session stats (questions_count, avg_score, ended_at)
- Fetch session details + attempts list

### Scope Boundaries

**IN SCOPE:**
- Session CRUD (create + get + end)
- Attempt creation linked to session
- Session stats update helper
- Auth-required endpoints

**OUT OF SCOPE:**
- AI evaluation (BUILD_04)
- UI templates (BUILD_05/06)
- HTMX partials (BUILD_08)

### Data Models (Existing)

#### `app/models/session.py` (from BUILD_02 with user_id)
```python
from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base

class PracticeSession(Base):
    """A practice session (collection of attempts in one sitting)."""
    __tablename__ = "practice_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    category_filter: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="standard")
    timer_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    questions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_score: Mapped[float | None] = mapped_column(Float, nullable=True)
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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
        Index('idx_question_score', 'question_id', 'overall_score'),
    )
```

### Pydantic Schemas

**File: `app/schemas/session.py`**
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class SessionCreate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category_filter: Optional[str] = None
    mode: str = "standard"
    timer_minutes: Optional[int] = Field(None, ge=1, le=60)

class SessionUpdate(BaseModel):
    questions_count: int
    avg_score: Optional[float] = None
    ended_at: Optional[datetime] = None

class SessionResponse(BaseModel):
    id: str
    user_id: Optional[int] = None
    category_filter: Optional[str] = None
    mode: str
    timer_minutes: Optional[int] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    questions_count: int
    avg_score: Optional[float] = None

    model_config = {"from_attributes": True}
```

**File: `app/schemas/attempt.py`**
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AttemptCreate(BaseModel):
    question_id: int
    session_id: str
    answer_text: str = Field(..., min_length=50)
    time_spent_sec: Optional[int] = None

class AttemptResponse(BaseModel):
    id: int
    question_id: int
    session_id: str
    answer_text: str
    time_spent_sec: Optional[int] = None
    overall_score: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Services

**File: `app/services/session_manager.py`**
- `create_session(user_id, payload)`
- `end_session(session_id)`
- `add_attempt(session_id, payload)`
- `recalculate_session_stats(session_id)`

### API Endpoints

**Router:** `app/routers/sessions.py`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/sessions` | Create a new practice session |
| GET | `/api/sessions/{session_id}` | Get session details |
| POST | `/api/sessions/{session_id}/attempts` | Add attempt (no AI eval yet) |
| POST | `/api/sessions/{session_id}/end` | End session + compute stats |
| GET | `/api/sessions/{session_id}/attempts` | List attempts for session |

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

#### `app/database.py`
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.config import settings

class Base(DeclarativeBase):
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
```

#### `app/middleware/auth.py` (from BUILD_02)
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.database import get_db
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
```

### Sample Data

**Create Session Request:**
```json
{
  "category_filter": "product_design",
  "mode": "standard",
  "timer_minutes": 10
}
```

**Create Attempt Request:**
```json
{
  "question_id": 1,
  "session_id": "<uuid>",
  "answer_text": "My structured answer with at least 50 characters...",
  "time_spent_sec": 420
}
```

---

## Section 6: Expected Output

Create or update the following files:

1. `app/services/session_manager.py`
2. `app/routers/sessions.py`
3. `app/schemas/session.py` (update to include user_id)
4. `app/schemas/attempt.py` (ensure AttemptCreate/Response present)
5. `app/routers/__init__.py` (include sessions router)
6. `app/main.py` (include sessions router)
7. `tests/test_sessions.py`

### Output Rules
- Return COMPLETE files, not snippets
- Include file path as a comment at the top of each file
- All database access async

---

## Section 7: Project Structure

```
pm-interview-coach/
├── app/
│   ├── services/
│   │   └── session_manager.py     [NEW]
│   ├── routers/
│   │   ├── sessions.py            [NEW]
│   │   └── __init__.py            [UPDATED]
│   ├── schemas/
│   │   ├── session.py             [UPDATED]
│   │   └── attempt.py             [UPDATED]
│   └── main.py                    [UPDATED]
├── tests/
│   └── test_sessions.py           [NEW]
```

---

## Section 8: Acceptance Test

### Test 1: Create Session
```bash
curl -X POST http://localhost:8002/api/sessions \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"category_filter":"product_design","mode":"standard","timer_minutes":10}'
```
Expected: JSON with session_id + started_at.

### Test 2: Get Session
```bash
curl http://localhost:8002/api/sessions/<SESSION_ID> \
  -H "Authorization: Bearer <TOKEN>"
```
Expected: Session details with questions_count.

### Test 3: Add Attempt
```bash
curl -X POST http://localhost:8002/api/sessions/<SESSION_ID>/attempts \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"question_id":1,"session_id":"<SESSION_ID>","answer_text":"Long enough answer...","time_spent_sec":120}'
```
Expected: Attempt JSON with id.

### Test 4: End Session
```bash
curl -X POST http://localhost:8002/api/sessions/<SESSION_ID>/end \
  -H "Authorization: Bearer <TOKEN>"
```
Expected: Session with ended_at + avg_score.

### Test 5: List Attempts
```bash
curl http://localhost:8002/api/sessions/<SESSION_ID>/attempts \
  -H "Authorization: Bearer <TOKEN>"
```
Expected: JSON list of attempts.

### Validation Checklist
- [ ] All 8 sections present
- [ ] Design system pasted inline
- [ ] Full file contents included
- [ ] 5+ concrete acceptance tests
- [ ] No external references

---

# BUILD_02_AUTH_SYSTEM.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task adds a complete authentication system (users + login/register + auth middleware). It enables multi-user sessions and protects user-specific practice history, and becomes a dependency for session tracking and dashboards.

**Preparation (Required Reading):**
1. Read `README.md` (task breakdown + dependency graph)
2. Read `BUILD_01_DATABASE_MODELS.md` (format + baseline models)
3. Read `INSTRUCTIONS_FOR_LLM.md` (rules, design system, acceptance tests)

**Dependency Graph (Build Order):**
```
Phase 1 (parallel):
  - BUILD_01_DATABASE_MODELS.md (done)
  - BUILD_02_AUTH_SYSTEM.md (this task)

Phase 2 (after Phase 1):
  - BUILD_03_INTERVIEW_SESSIONS.md (needs BUILD_01 + BUILD_02)
  - BUILD_04_CLAUDE_EVALUATOR.md (needs BUILD_01)

Phase 3 (after Phase 2):
  - BUILD_05_FRONTEND_INTERVIEW.md (needs BUILD_03 + BUILD_04)
  - BUILD_06_FRONTEND_DASHBOARD.md (needs BUILD_02 + BUILD_03)

Phase 4 (final):
  - BUILD_07_TESTING_DEPLOYMENT.md (needs everything)
  - BUILD_08_INTEGRATION.md (needs everything)
```

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Version/Notes |
|-------|-----------|---------------|
| **Runtime** | Python | 3.11+ |
| **Backend** | FastAPI | Async route handlers |
| **ORM** | SQLAlchemy | 2.0 async |
| **DB** | SQLite | Dev; PostgreSQL in prod |
| **Auth** | JWT (python-jose) | Access tokens |
| **Hashing** | passlib[bcrypt] | Password hashing |
| **Templating** | Jinja2 | Server-side rendering |
| **Styling** | Tailwind (CDN) | Utility classes only |
| **Interactivity** | HTMX (CDN) | Dynamic partials |
| **Fonts** | Geist Sans + JetBrains Mono | Via CDN |

**Do NOT use:** React, Vue, Angular, Next.js, Flask, Django, Prisma, MongoDB, OAuth providers, or any npm tooling.

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
- Use `async def` for all routes
- Full type hints everywhere
- Import order: stdlib → third-party → local
- Use Pydantic v2 models for request/response
- Use `passlib.context.CryptContext` for hashing
- Use `python-jose` for JWT encode/decode

### Templates
- All templates extend `app/templates/base.html`
- Use CSS variables for colors (no hex)
- Tailwind utilities only

### Security
- Never store raw passwords
- JWT tokens expire (default 30 minutes)
- Use `HTTPException` with clear error messages

### Quality Standard
- Aim for **90+/100** on VALIDATION_CHECKLIST.md

---

## Section 5: The Task

### Overview

Implement a complete email/password authentication system with JWT tokens and session-aware user context.

### Scope Boundaries

**IN SCOPE:**
- Email/password registration + login
- Password hashing with bcrypt
- JWT access tokens (Authorization: Bearer)
- Auth middleware dependency (`get_current_user`)
- Login/logout HTML pages
- Users table + migrations

**OUT OF SCOPE:**
- OAuth (Google/GitHub)
- Password reset/verification emails
- MFA/2FA
- Rate limiting

### Data Models

#### SQLAlchemy Model: `app/models/user.py`
```python
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class User(Base):
    """Authenticated user account."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
```

#### Update PracticeSession Model: `app/models/session.py`
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
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    questions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_score: Mapped[float | None] = mapped_column(Float, nullable=True)
```

### Pydantic Schemas

**File: `app/schemas/user.py`**
```python
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Auth Service

**File: `app/services/auth.py`**
- Password hashing + verification
- Token creation (JWT)
- User creation + lookup
- `get_current_user` dependency

### Auth Router

**File: `app/routers/auth.py`**

Routes:
- `GET /auth/register` → render register page
- `GET /auth/login` → render login page
- `POST /auth/register` → create user, return token
- `POST /auth/login` → validate credentials, return token
- `POST /auth/logout` → client clears token (return 204)
- `GET /auth/me` → return current user

### Auth Middleware

**File: `app/middleware/auth.py`**
- Extract Bearer token
- Decode JWT
- Load user from DB
- Raise 401 if invalid

### Templates

**File: `app/templates/auth/register.html`**
- Email, Full name, Password fields
- Submit button

**File: `app/templates/auth/login.html`**
- Email, Password fields
- Submit button

### Alembic Migration

**File: `alembic/versions/002_add_users_and_auth.py`**
- Create `users` table
- Add `user_id` to `practice_sessions`
- Add index on `users.email`

### Inline Reference Files (Existing)

#### `app/config.py`
```python
"""
Application configuration using Pydantic Settings.
Loads from environment variables and .env file.
"""
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

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db() -> None:
    await engine.dispose()
```

#### `app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from app.config import settings
from app.database import init_db, close_db

logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting PM Interview Coach...")
    logger.info(f"Database URL: {settings.database_url}")

    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

    yield

    logger.info("Shutting down PM Interview Coach...")
    await close_db()
    logger.info("Database connections closed")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered PM interview practice with structured feedback",
    lifespan=lifespan,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }
```

### Example Payloads

**Register Request:**
```json
{
  "email": "test@example.com",
  "full_name": "Test User",
  "password": "TestPass123!"
}
```

**Register Response:**
```json
{
  "user": {
    "id": 1,
    "email": "test@example.com",
    "full_name": "Test User",
    "is_active": true,
    "created_at": "2026-02-13T12:00:00Z"
  },
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

---

## Section 6: Expected Output

Create or update the following files:

1. `app/models/user.py`
2. `app/models/session.py` (add `user_id`)
3. `app/schemas/user.py`
4. `app/services/auth.py`
5. `app/routers/auth.py`
6. `app/middleware/auth.py`
7. `app/templates/auth/login.html`
8. `app/templates/auth/register.html`
9. `app/routers/__init__.py` (include auth router)
10. `app/main.py` (include auth router)
11. `alembic/versions/002_add_users_and_auth.py`
12. `requirements.txt` (add passlib[bcrypt], python-jose, python-multipart, email-validator)
13. `.env.example` (add JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES_MINUTES)
14. `tests/test_auth.py`

### Output Rules
- Return COMPLETE files, not snippets
- Include file path as comment at the top of each file
- All colors via CSS variables
- Async database access only

---

## Section 7: Project Structure

```
pm-interview-coach/
├── app/
│   ├── models/
│   │   ├── question.py
│   │   ├── attempt.py
│   │   ├── session.py              [UPDATED]
│   │   └── user.py                 [NEW]
│   ├── schemas/
│   │   └── user.py                 [NEW]
│   ├── services/
│   │   └── auth.py                 [NEW]
│   ├── middleware/
│   │   └── auth.py                 [NEW]
│   ├── routers/
│   │   ├── auth.py                 [NEW]
│   │   └── __init__.py             [UPDATED]
│   └── templates/
│       └── auth/
│           ├── login.html          [NEW]
│           └── register.html       [NEW]
├── alembic/
│   └── versions/
│       └── 002_add_users_and_auth.py
├── tests/
│   └── test_auth.py
├── requirements.txt               [UPDATED]
└── .env.example                   [UPDATED]
```

---

## Section 8: Acceptance Test

### Test 1: Install Dependencies
```bash
pip install -r requirements.txt
```
Expected: passlib, python-jose, python-multipart installed.

### Test 2: Migration
```bash
alembic upgrade head
```
Expected: users table created, user_id added to practice_sessions.

### Test 3: Register User (API)
```bash
curl -X POST http://localhost:8002/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"TestPass123!"}'
```
Expected: JSON with `access_token` and `user`.

### Test 4: Login User (API)
```bash
curl -X POST http://localhost:8002/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'
```
Expected: JSON with `access_token`.

### Test 5: Get Current User
```bash
curl http://localhost:8002/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```
Expected: JSON with user email.

### Test 6: Invalid Token
```bash
curl http://localhost:8002/auth/me -H "Authorization: Bearer BADTOKEN"
```
Expected: 401 Unauthorized.

### Validation Checklist
- [ ] All 8 sections present
- [ ] Design system pasted inline
- [ ] Full file contents included
- [ ] 5+ concrete acceptance tests
- [ ] No external references

---

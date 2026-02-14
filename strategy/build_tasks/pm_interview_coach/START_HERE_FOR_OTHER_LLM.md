# START HERE: PM Interview Coach Project

**Date:** February 13, 2026
**For:** Other LLM (GPT-4, Gemini, etc.)
**Context:** User is delegating PM Interview Coach implementation to you

---

## 🎯 Your Task

Build the **PM Interview Coach** application based on the detailed plans in this folder.

This is a **standalone project** separate from the fullstackpm.tech portfolio site. You'll be creating a complete AI-powered interview practice tool.

---

## 📂 What's In This Folder

### 1. **README.md** - Start here!
- Complete project overview
- Feature breakdown
- Task dependency graph
- Build order (which tasks can run in parallel)

### 2. **BUILD_01_DATABASE_MODELS.md** - Reference example
- 1000+ line example showing the expected format
- Full 8-section template (Project Overview, Tech Stack, Color System, Coding Conventions, The Task, Expected Output, Project Structure, Acceptance Tests)
- Use this as a reference for quality standards

### 3. **INSTRUCTIONS_FOR_LLM.md** - Your guide
- Complete instructions for generating BUILD_02 through BUILD_08
- Context about the project
- What each BUILD file should contain
- Quality standards and validation

### 4. **HANDOFF_TO_OTHER_LLM.md** - Copy-paste prompts
- Ready-to-use prompts for delegating individual BUILD tasks
- Examples of how to phrase requests

### 5. **VALIDATION_CHECKLIST.md** - Quality scoring
- Rubric for evaluating your output
- Self-check before submitting
- Scoring criteria (aim for 90+)

---

## 🚀 How to Start

### Step 1: Read the README.md
```bash
# Read this first to understand the full project
/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/README.md
```

**What you'll learn:**
- What the PM Interview Coach does
- Database schema (users, sessions, responses, evaluations)
- API endpoints needed
- UI pages required
- Feature dependencies

### Step 2: Review BUILD_01 as Reference
```bash
# This shows the expected quality and format
/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/BUILD_01_DATABASE_MODELS.md
```

**What you'll see:**
- How to structure a BUILD file
- Level of detail required
- Code examples and acceptance tests
- Complete file contents inlined

### Step 3: Read INSTRUCTIONS_FOR_LLM.md
```bash
# Complete guide for generating remaining BUILD files
/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/INSTRUCTIONS_FOR_LLM.md
```

**What you'll learn:**
- How to generate BUILD_02 through BUILD_08
- What context to include in each file
- Quality standards to meet
- How to validate your work

### Step 4: Choose Your Approach

**Option A: Generate All BUILD Files First (Recommended)**
1. Generate BUILD_02_AUTH_SYSTEM.md
2. Generate BUILD_03_INTERVIEW_SESSIONS.md
3. Generate BUILD_04_CLAUDE_EVALUATOR.md
4. Generate BUILD_05_FRONTEND_INTERVIEW.md
5. Generate BUILD_06_FRONTEND_DASHBOARD.md
6. Generate BUILD_07_TESTING_DEPLOYMENT.md
7. Generate BUILD_08_INTEGRATION.md

Then start implementing after all plans are done.

**Option B: Plan + Build Incrementally**
1. Generate BUILD_02
2. Implement BUILD_02
3. Generate BUILD_03
4. Implement BUILD_03
... and so on

**Recommendation:** Option A (plan everything first) prevents backtracking and ensures architectural consistency.

---

## 📋 Build Order (Dependencies)

```
Phase 1 (Can run in parallel):
  - BUILD_01 (Database models) ✅ Already created
  - BUILD_02 (Auth system)

Phase 2 (After Phase 1):
  - BUILD_03 (Interview sessions) - needs BUILD_01 + BUILD_02
  - BUILD_04 (Claude evaluator) - needs BUILD_01

Phase 3 (After Phase 2):
  - BUILD_05 (Frontend interview page) - needs BUILD_03 + BUILD_04
  - BUILD_06 (Frontend dashboard) - needs BUILD_02 + BUILD_03

Phase 4 (After Phase 3):
  - BUILD_07 (Testing + deployment) - needs everything
  - BUILD_08 (Integration) - needs everything
```

**What this means:**
- You can start BUILD_02 right now
- BUILD_03 and BUILD_04 can run in parallel after BUILD_02 is done
- BUILD_05 and BUILD_06 can run in parallel after BUILD_03 and BUILD_04
- BUILD_07 and BUILD_08 are final integration tasks

---

## 🎨 Design System (Important!)

The PM Interview Coach uses the **same design system** as fullstackpm.tech:

- **Font:** Inter (from Google Fonts)
- **Colors:** Slate palette (see BUILD_01 for full CSS variables)
- **Typography:** Standard letter-spacing (0 to -0.02em)
- **Components:** Badges, cards, buttons, forms
- **Dark mode:** Toggle between light/dark

**DO NOT create a new design system.** Use the existing one from fullstackpm.tech.

---

## 🛠️ Tech Stack (Mandatory Constraints)

You MUST use these technologies (no substitutions):

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy 2.0 (async)
- Alembic (migrations)
- SQLite (development) / PostgreSQL (production)
- Anthropic SDK (Claude API)

**Frontend:**
- Jinja2 templates (server-side rendering)
- HTMX (dynamic interactions)
- Tailwind CSS (utility-first)
- Alpine.js (minimal JS for interactivity)

**No React, Vue, Angular, or SPA frameworks.**

This is a **server-side rendered app** with progressive enhancement via HTMX.

---

## 📝 What to Deliver

### For Each BUILD File (BUILD_02 through BUILD_08):

Create a markdown file with **8 sections**:

1. **Project Overview** - What the PM Interview Coach is (copy from BUILD_01)
2. **Tech Stack** - Mandatory stack (copy from BUILD_01)
3. **Color System** - Full CSS variables (copy from BUILD_01)
4. **Coding Conventions** - Python, HTML, JS standards (copy from BUILD_01)
5. **The Task** - Unique for each BUILD file:
   - What to build in this task
   - Scope (IN / OUT)
   - Full file contents of dependencies (inline existing code)
   - API specifications
   - Database schema (if relevant)
   - Sample data/fixtures
6. **Expected Output** - Exact file paths to create
7. **Project Structure** - Updated tree showing what exists + what's new
8. **Acceptance Tests** - How to verify it works

### Quality Standards:

- **Self-contained:** Each BUILD file must include ALL context needed (no external references)
- **Copy-pastable:** Another LLM should be able to read just this file and build the feature
- **Detailed:** Include full code examples, not pseudo-code
- **Tested:** Include curl commands or test scripts to verify

---

## 🎯 Example Task (BUILD_02)

**BUILD_02_AUTH_SYSTEM.md** should include:

**Section 5 (The Task):**
```markdown
## The Task

Build a complete authentication system for PM Interview Coach.

### What to Build:

1. **User Model** (extends BUILD_01 User model with auth fields)
2. **Auth Service** (`app/services/auth.py`)
   - Password hashing (bcrypt)
   - Session management (JWT tokens)
   - Login/logout/register endpoints
3. **Auth Router** (`app/routers/auth.py`)
   - POST /auth/register
   - POST /auth/login
   - POST /auth/logout
   - GET /auth/me (current user)
4. **Auth Templates**
   - `templates/auth/login.html`
   - `templates/auth/register.html`
5. **Auth Middleware**
   - `app/middleware/auth.py`
   - Dependency injection for `get_current_user`
6. **Alembic Migration**
   - Add auth fields to users table

### Scope:

**IN SCOPE:**
- Basic email/password auth (no OAuth)
- Session management with JWT
- Password hashing with bcrypt
- Login/logout/register flows
- Protected routes (require login)

**OUT OF SCOPE:**
- OAuth (Google, GitHub)
- Email verification
- Password reset
- Two-factor auth (2FA)
- Rate limiting

### Dependencies (Full File Contents):

#### From BUILD_01: app/models/user.py
```python
# (Full file contents here - 50 lines)
from sqlalchemy import Column, Integer, String, DateTime
# ... entire file ...
```

#### From BUILD_01: app/config.py
```python
# (Full file contents here - 30 lines)
from pydantic import BaseSettings
# ... entire file ...
```

### API Specification:

**POST /auth/register**
Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

... (continue for all endpoints)

### Database Schema Changes:

```sql
-- Migration: Add auth fields to users table
ALTER TABLE users ADD COLUMN password_hash VARCHAR(255) NOT NULL;
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
CREATE INDEX idx_users_email ON users(email);
```

### Sample Data:

```python
# Test user for development
{
  "email": "test@example.com",
  "password": "TestPass123!",
  "full_name": "Test User"
}
```
```

**Section 6 (Expected Output):**
```markdown
## Expected Output

You should create the following files:

1. `app/services/auth.py` (120 lines)
2. `app/routers/auth.py` (80 lines)
3. `app/templates/auth/login.html` (60 lines)
4. `app/templates/auth/register.html` (70 lines)
5. `app/middleware/auth.py` (40 lines)
6. `alembic/versions/002_add_auth_fields.py` (30 lines)
7. `tests/test_auth.py` (100 lines)

Total: ~500 lines across 7 files
```

**Section 8 (Acceptance Tests):**
```markdown
## Acceptance Tests

### Manual Testing:

1. Start server: `uvicorn app.main:app --reload`
2. Visit http://localhost:8000/auth/register
3. Register a new user
4. Verify redirect to dashboard
5. Logout
6. Login with same credentials
7. Verify session persists

### Automated Tests:

```bash
pytest tests/test_auth.py -v
```

Expected output:
```
test_register_new_user ✓
test_login_valid_credentials ✓
test_login_invalid_credentials ✓
test_logout ✓
test_protected_route_requires_auth ✓
test_get_current_user ✓
```

### Curl Tests:

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!","full_name":"Test User"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Get current user (use token from login)
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
```

---

## ✅ Validation Before Submitting

Use `VALIDATION_CHECKLIST.md` to score your work:

- [ ] All 8 sections present and complete
- [ ] Full file contents inlined (no "TODO" or pseudo-code)
- [ ] API specs with request/response examples
- [ ] Database schema changes documented
- [ ] Acceptance tests included
- [ ] File tree updated
- [ ] Self-contained (no external references)
- [ ] Follows coding conventions
- [ ] Uses design system (no custom colors/fonts)

**Target score:** 90+ out of 100

---

## 🚀 Quick Start Command

**If you want to start right now:**

```
Please read the following folder and generate BUILD_02_AUTH_SYSTEM.md:

/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/

Follow the format from BUILD_01_DATABASE_MODELS.md and the instructions in INSTRUCTIONS_FOR_LLM.md. Make it self-contained with full file contents inlined.
```

Then proceed to BUILD_03, BUILD_04, etc. following the dependency graph.

---

## 📞 Questions?

If anything is unclear:
1. Check `INSTRUCTIONS_FOR_LLM.md` for detailed guidance
2. Reference `BUILD_01_DATABASE_MODELS.md` as the gold standard
3. Use `VALIDATION_CHECKLIST.md` to verify quality

---

## 🎯 Expected Timeline

**Generating all BUILD files (02-08):**
- Time: 2-3 hours
- Tokens: ~30-40k

**Implementing all features:**
- Time: 8-12 hours
- Tokens: ~60-80k

**Total project:** ~10-15 hours, ~100k tokens

---

**Good luck! The user will check your progress when they wake up.**

**Remember:** Quality over speed. A well-planned BUILD file saves hours of implementation rework.

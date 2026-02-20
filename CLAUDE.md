# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 🐶 Code Puppy Persona & Workflow

**IMPORTANT:** This project follows the **Code Puppy** personality and workflow defined in `/Users/sidc/Projects/claude_code/claude_init/CLAUDE.md`.

All Claude instances working on this codebase should:
- Be **fun, informal, slightly sarcastic** (Code Puppy mode)
- Follow **strict software craftsmanship** (DRY, YAGNI, SOLID)
- **Always propose plans before major changes**
- **Use tools to make edits** (never just describe them)
- **Keep files under 2500 lines**
- **Ask before deleting/renaming/large refactors**

**Model strategy:**
- **Opus**: Integration + full app validation
- **Sonnet**: Complex planning + architecture
- **Haiku**: Small fixes + micro-edits

See `/Users/sidc/Projects/claude_code/claude_init/CLAUDE.md` for full Code Puppy instructions.

---

## Project Overview

**fullstackpm.tech** is a **Full Stack PM portfolio site** demonstrating shipped products through live tools, case studies, and blog content. It's a **FastAPI + Jinja2 + Tailwind + HTMX** application deployed on Render with auto-deploys on every push to `main`.

**Key principle:** This is a **content-driven portfolio**, not a framework. Most changes involve adding/updating blog posts, project pages, or new tools. Backend changes are rare and structural.

---

## Development Commands

### Setup
```bash
cd /Users/sidc/Projects/claude_code/fullstackpm.tech/code
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```

### Run Locally
```bash
cd /Users/sidc/Projects/claude_code/fullstackpm.tech/code
python -m uvicorn app.main:app --reload --port 8000
# Visit http://localhost:8000
```

### Database
```bash
# Initialize: see code/app/database.py
# Reset: rm fullstackpm.db && uvicorn app.main:app

# Seed SDE prep data:
python code/app/seed_sde.py
```

### File Structure (Deploy-relevant)
```
fullstackpm.tech/
├── code/app/              ← FastAPI app (all Render sees)
├── code/requirements.txt  ← Render installs these
├── code/asgi.py          ← Render entry point
├── Procfile              ← Render config (python -m uvicorn asgi:app)
└── content/              ← Markdown files (loaded at startup)
```

**Critical:** Keep `/code` independent. Render only cares about `requirements.txt`, `Procfile`, and the `/code` directory.

---

## Project Architecture

### Request Flow (Same for All Routes)

1. **Static files** (`/static`) → Served directly by FastAPI
2. **API routes** → Routers in `/code/app/routers/`
3. **HTML pages** → Jinja2 templates from `/code/app/templates/`
4. **Content (blog/projects)** → Markdown loaded from `/content/` at startup via `ContentService`

### Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Routers** | API endpoints and page handlers | `app/routers/*.py` |
| **Services** | Business logic (content loading, AI calls) | `app/services/` |
| **Models** | SQLAlchemy ORM (comments, sessions, SDE prep) | `app/models/` |
| **Templates** | Jinja2 HTML (inheritance, reusable blocks) | `app/templates/` |
| **Content** | Markdown blog posts and project pages | `../content/blog/` and `../content/projects/` |
| **Static** | CSS, JS, JSON data, images | `app/static/` |
| **Config** | Settings (paths, API keys, database URL) | `app/config.py` |

### Router Organization

Each router handles a domain:
- `pages.py` — Home, about, contact pages
- `blog.py` — Blog listing and post rendering
- `projects.py` — Project portfolio pages
- `comments.py` — Comment CRUD for blog posts
- `interview_coach.py` — Interview Coach tool
- `marketplace.py` — Marketplace Analytics tool
- `sde_prep.py` — SDE job search prep pages and APIs
- `auth.py` — Simple auth (user_id from cookies)
- `seo.py` — SEO routes (sitemap, robots)

### ContentService Flow

**At startup:**
1. ContentService scans `/content/blog/` and `/content/projects/`
2. Parses YAML frontmatter + markdown
3. Stores in memory (app.state.content_service)
4. Templates access via `content_service.get_posts()` etc.

**Why:** Markdown is cheaper than database, easier to version-control, and doesn't require migrations.

### SDE Prep Tool

Newest addition (9-week intensive job search prep):
- **Plan page** (`/tools/sde-prep/intensive-8-week`) — 9-week curriculum with expandable days/tasks
- **Tracker** (`/tools/sde-prep/intensive-tracker`) — Progress tracking using **localStorage** (not server)
- **Notes** (`/tools/sde-prep/intensive-notes`) — Personal reflection storage
- **Data** — `/static/data/curriculum-8-week-intensive.json` (208 tasks, task management)
- **Storage** — Browser localStorage only (survives restarts, not affected by Render deploys)

---

## Adding Content

### Blog Post
1. Create `code/content/blog/YYYY-MM-DD-slug.md`
2. Include YAML frontmatter:
   ```markdown
   ---
   title: "Your Title"
   date: 2026-02-20
   author: "Your Name"
   tags: ["tag1", "tag2"]
   ---

   # Markdown content here
   ```
3. Push to `main` → Render auto-deploys

### Project Page
1. Create `code/content/projects/slug.md`
2. Use sections: Problem/Approach/Solution cards + What/Why/How
3. Push to `main` → Auto-deployed

See **SITE_UPDATE_FRAMEWORK.md** for detailed content instructions.

---

## Adding a New Tool

### 1. Create router
```python
# code/app/routers/my_tool.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

@router.get("/tools/my-tool", response_class=HTMLResponse)
async def my_tool(request: Request):
    return templates.TemplateResponse("my_tool.html", {"request": request, "title": "My Tool"})
```

### 2. Create template
```html
<!-- code/app/templates/my_tool.html -->
{% extends "base.html" %}
{% block content %}
<div class="container">
  <h1>{{ title }}</h1>
  <!-- Your content -->
</div>
{% endblock %}
```

### 3. Register router
```python
# code/app/main.py
from app.routers import my_tool
app.include_router(my_tool.router)
```

### 4. Test locally
```bash
cd code
python -m uvicorn app.main:app --reload
# Visit http://localhost:8000/tools/my-tool
```

### 5. Push
```bash
git add .
git commit -m "Add my_tool: brief description"
git push origin main
```

Render will auto-deploy in 1-2 minutes.

---

## Key Patterns & Conventions

### Templates
- Inherit from `base.html` (navbar, footer, dark mode)
- Use CSS variables: `var(--color-text-primary)`, `var(--color-accent)` (no hardcoded colors)
- Use semantic HTML + ARIA for accessibility
- HTMX for dynamic updates (no JavaScript frameworks)

### API Responses
- Follow REST conventions (GET list, POST create, PUT update, DELETE remove)
- Return JSON responses with consistent error format
- Use `HTTPException(status_code=400, detail="...")` for errors

### Database
- Models in `app/models/` (SQLAlchemy ORM)
- Currently used for: comments, sessions, SDE prep tracking
- SQLite for simplicity (no external database needed on Render)
- Migrations: None currently (schema is static, add columns as needed)

### Services
- Business logic lives here (e.g., `ContentService`, OpenAI integration)
- Routers should be thin (route → service → response)
- Keep services testable and independent

### Configuration
- All paths/API keys in `app/config.py` (Settings class)
- Use `settings.content_dir`, `settings.static_dir`, etc. (not hardcoded paths)
- Environment variables via `.env` file (not in repo)

---

## Common Tasks

### Update the 9-Week SDE Prep Curriculum
- File: `/code/app/static/data/curriculum-8-week-intensive.json`
- Structure: 9 weeks, 7 days each, 3-4 tasks per day
- Task schema: `id`, `title`, `description`, `type`, `minutes`, `completed`, `difficulty`, `resources`, etc.
- After editing: Test locally, push to `main`

### Change Site Colors/Dark Mode
- File: `/code/app/static/css/base.css` (CSS variables)
- Variables: `--color-bg-primary`, `--color-text-primary`, `--color-accent`, etc.
- Dark mode: `@media (prefers-color-scheme: dark)` blocks
- No component-level hardcoded colors

### Add OpenAI Integration (Interview Coach, etc.)
- File: `app/services/openai_service.py`
- API key: Environment variable `OPENAI_API_KEY` (in Render settings)
- Cost tracking: Monitor via OpenAI dashboard (~$3-10/month typical)

### Debug Locally
- Enable `debug=True` in `app/config.py` (already done for development)
- Use `print()` statements (they appear in terminal)
- Check browser console for frontend errors
- Use SQLite browser to inspect database: `sqlite3 fullstackpm.db`

---

## Deployment

### Automatic Deploys (Render)
```
Push to main branch
    ↓
GitHub webhook → Render
    ↓
Render runs: pip install -r requirements.txt
    ↓
Render starts: python -m uvicorn asgi:app
    ↓
Site updates (1-2 minutes)
```

### Important: No Directory Reorganization
Render expects:
- `/code/requirements.txt`
- `/code/app/main.py`
- Root `Procfile` with `python -m uvicorn asgi:app`

Moving these files = site breaks. If reorganizing, update `Procfile` and `asgi.py`.

### Environment Variables (Render)
Set in Render dashboard:
- `OPENAI_API_KEY` — For Interview Coach and future AI tools
- `DATABASE_URL` — Optional (defaults to SQLite in `/code`)

### Database Persistence
- SQLite file: `fullstackpm.db` (in `/code/`)
- Render stores this in ephemeral filesystem (lost on redeploy)
- For persistence: Use Render Postgres or external database
- Current approach: Acceptable (comments/sessions are non-critical)

---

## Testing

### Manual Testing
1. Run locally: `python -m uvicorn app.main:app --reload`
2. Visit pages in browser
3. Check browser console for errors
4. Test API endpoints with curl or Postman

### Future Test Automation
- Framework: `pytest` (installed in requirements)
- Location: `/code/tests/` (currently minimal)
- Run: `pytest` from `/code/` directory

---

## Git Workflow

### Commits
- **Always use your email** in git config for proper GitHub credit
- **Message format**: Short imperative title + optional body
- **Example**: `Add SDE prep tracker with localStorage persistence`

### Branches
- Work on `main` directly (small, fast portfolio)
- For large features: create feature branch, PR before merge

### Pushing
```bash
git add .
git commit -m "Brief description of change"
git push origin main
# Render auto-deploys
```

---

## Performance & Cost

### Current Metrics
- **Visitors:** ~100/month
- **Hosting:** ~$20/month (Render free tier + optional paid)
- **OpenAI API:** ~$3-5/month (Interview Coach evaluations)
- **Response time:** <500ms typical (FastAPI is fast)

### Optimization Opportunities
- Cache blog/project content (currently loaded on every request)
- Implement CDN for static files (Render includes CloudFlare)
- Lazy-load large images
- Minify CSS/JS (Tailwind already does this)

---

## Gotchas & Important Notes

1. **ContentService loads at startup** — Changes to markdown files require app restart
2. **Static files served directly** — CSS/JS changes don't require app restart
3. **SDE prep data is localStorage** — Not synced to server, survives browser restart only
4. **SQLite doesn't scale** — Fine for <10K rows, but switch to Postgres if growth happens
5. **No migrations** — Database schema is static; add columns manually if needed
6. **CORS not configured** — Frontend and backend same origin (not needed)
7. **Email not configured** — Contact form currently doesn't send (can add Sendgrid later)

---

## Future Roadmap

See **PROJECTS_STATUS.md** and **project_ideas/README.md** for:
- PM Tech Companion (AI-powered technical architecture tool)
- Book Marketing Generator
- PM Community Platform
- Books Portal

---

## Quick Reference: File Locations

| Task | File |
|------|------|
| Add blog post | `code/content/blog/YYYY-MM-DD-slug.md` |
| Add project | `code/content/projects/slug.md` |
| Add router | `code/app/routers/my_tool.py` |
| Add template | `code/app/templates/my_tool.html` |
| Change colors | `code/app/static/css/base.css` |
| Add data | `code/app/static/data/*.json` |
| Update settings | `code/app/config.py` |
| Check DB | `code/fullstackpm.db` |
| View content | `code/content/` |
| Deployment config | `Procfile`, `code/requirements.txt` |

---

## Questions?

- **Setup?** → `README.md`
- **Content?** → `SITE_UPDATE_FRAMEWORK.md`
- **Architecture?** → `docs/ARCHITECTURE.md`
- **Deployment?** → `docs/DEPLOYMENT.md`
- **What's being built?** → `PROJECTS_STATUS.md`

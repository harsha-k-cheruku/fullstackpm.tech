# Quick Reference Guide

## For Future You (or Anyone Taking Over This Project)

---

## Project Overview

**What:** Personal portfolio website for Harsha Cheruku (Full Stack AI PM)

**Tech Stack:**
- Framework: FastAPI (Python)
- Server: Uvicorn (ASGI)
- Templating: Jinja2
- Frontend: Tailwind CSS + HTMX
- Hosting: Render
- Version Control: GitHub

**Live URL:** https://fullstackpm.tech (or your Render URL)

**GitHub:** https://github.com/harsha-k-cheruku/fullstackpm.tech

---

## Quick Start (Local Development)

### First Time Setup

```bash
cd /Users/sidc/Projects/claude_code/fullstackpm.tech

# Install Python packages
pip install -r requirements.txt

# Run the app
cd code
python -m uvicorn app.main:app --reload
```

### Then

- Visit http://localhost:8000
- Changes auto-reload (thanks to --reload)
- Static files serve from /static/
- Templates live in app/templates/

---

## Adding Content

### New Blog Post

1. Create file: `code/content/blog/YYYY-MM-DD-title.md`
2. Copy this template:

```markdown
---
title: "Your Blog Title"
date: 2026-02-20
tags: [tag1, tag2, tag3]
excerpt: "One-sentence summary for listings"
author: "Harsha Cheruku"
---

# Your post content here

Regular markdown. Code blocks work too.

```python
code_block = "supported"
```
```

3. Save, commit, push → Auto-deployed

### New Project

1. Create file: `code/content/projects/project-slug.md`
2. Copy this template:

```markdown
---
title: "Project Title"
description: "One-liner about the project"
tech_stack: [FastAPI, React, PostgreSQL]
status: "in_progress"  # or "planned" or "shipped"
featured: true  # or false
display_order: 1
github_url: "https://github.com/..."
live_url: "https://..."
---

# Problem

What problem does it solve?

# Solution

What did you build?

# Impact

What was the result?
```

---

## Making Changes

### 1. Edit code locally

```bash
cd /Users/sidc/Projects/claude_code/fullstackpm.tech/code
# Edit files
```

### 2. Test locally

```bash
# Terminal 1
python -m uvicorn app.main:app --reload

# Terminal 2 (in browser)
http://localhost:8000
# Check that changes work
```

### 3. Commit to Git

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### 4. Render auto-deploys

- Render sees GitHub push
- Redeploys automatically (2-3 minutes)
- Changes live

---

## Directory Structure

```
fullstackpm.tech/
├── asgi.py                    # Entry point for Render
├── Procfile                   # Deployment instructions
├── requirements.txt           # Python dependencies
├── README.md
│
├── code/
│   ├── __init__.py
│   ├── app/
│   │   ├── main.py           # FastAPI app instance
│   │   ├── config.py         # Settings
│   │   ├── routers/          # URL endpoints
│   │   │   ├── pages.py      # /, /about, /contact, /resume
│   │   │   ├── blog.py       # /blog, /blog/{slug}
│   │   │   ├── projects.py   # /projects, /projects/{slug}
│   │   │   └── seo.py        # /feed.xml, /sitemap.xml, /robots.txt
│   │   ├── services/         # Business logic
│   │   │   ├── content.py    # ContentService (markdown parsing)
│   │   │   └── feed.py       # FeedService (RSS generation)
│   │   ├── templates/        # HTML templates
│   │   │   ├── base.html     # Master template
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── resume.html
│   │   │   ├── 404.html
│   │   │   ├── blog/
│   │   │   │   ├── list.html
│   │   │   │   ├── detail.html
│   │   │   │   ├── tag.html
│   │   │   │   └── partials/post_list.html
│   │   │   ├── projects/
│   │   │   │   ├── gallery.html
│   │   │   │   ├── detail.html
│   │   │   │   └── partials/project_grid.html
│   │   │   └── partials/      # Reusable HTML components
│   │   │       ├── navbar.html
│   │   │       ├── footer.html
│   │   │       └── project_card.html
│   │   └── static/
│   │       ├── css/custom.css # Design tokens, dark mode
│   │       └── js/main.js     # Dark mode toggle
│   │
│   └── content/               # Your actual content
│       ├── blog/
│       │   ├── 2026-02-20-what-is-a-fullstack-pm.md
│       │   └── 2026-02-15-why-im-building-in-public.md
│       └── projects/
│           ├── portfolio-site.md
│           └── pm-interview-coach.md
│
├── strategy/                  # Planning docs
├── learnings/                 # This folder (documentation)
└── .gitignore
```

---

## File Reference

### Key Files

| File | Purpose | Edit When |
|------|---------|-----------|
| `asgi.py` | Entry point | When you move code or change app location |
| `Procfile` | Deployment command | When you change how app starts |
| `requirements.txt` | Python dependencies | When you add/remove packages |
| `code/app/main.py` | FastAPI setup | When you add new routers |
| `code/app/config.py` | Settings | When you add env vars |
| `code/app/templates/base.html` | Master template | When you change header/footer |
| `code/content/blog/*.md` | Blog posts | Every blog post |
| `code/content/projects/*.md` | Projects | Every project |

---

## Common Tasks

### Task: Add navigation link

1. Edit `code/app/templates/partials/navbar.html`
2. Add `<a href="/new-page">New Page</a>`
3. Test locally, commit, push

### Task: Change colors/theme

1. Edit `code/app/static/css/custom.css`
2. Modify CSS variables
3. Test locally, commit, push

### Task: Add a new page (e.g., /speaking)

1. Create `speaking.html` template
2. Add route in `code/app/routers/pages.py`:
```python
@router.get("/speaking", response_class=HTMLResponse)
async def speaking(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "speaking.html",
        _ctx(request, title="Speaking — fullstackpm.tech", current_page="/speaking"),
    )
```
3. Test locally, commit, push

### Task: Update site description

1. Edit `code/app/config.py`
2. Change `site_description`
3. This updates meta tags and RSS

### Task: Fix a bug

1. Make change in code/
2. Test locally
3. Commit with descriptive message
4. Push to GitHub
5. Render auto-deploys

---

## Troubleshooting

### Problem: Localhost:8000 won't load

**Try:**
```bash
# Make sure you're in right directory
cd /Users/sidc/Projects/claude_code/fullstackpm.tech/code

# Try specific port
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001

# Check if port is in use
lsof -i :8000
```

### Problem: Blog post won't show up

**Check:**
1. File is in `code/content/blog/` ✓
2. File name starts with `YYYY-MM-DD-` ✓
3. Has YAML frontmatter at top ✓
4. Has `title:`, `date:`, `excerpt:`, `author:` ✓
5. Restart local server (Ctrl+C, restart)

### Problem: Changes not showing on Render

**Check:**
1. Did you commit? `git status` (should be clean)
2. Did you push? `git log --oneline` (latest commit should be yours)
3. Did Render redeploy? Check Render dashboard → Logs
4. Still not working?
   - Check Render logs for error
   - Try redeploying manually in dashboard

### Problem: 500 error on Render

1. Check Render logs (find the error)
2. Common errors:
   - `TemplateNotFound` → Template file missing
   - `FileNotFoundError` → Content file missing
   - `ImportError` → Code import error
3. Fix locally, test, commit, push

### Problem: "No module named 'app'"

**This means:**
- asgi.py isn't finding code/app/
- Check:
  1. asgi.py exists at root
  2. asgi.py has `sys.path.insert(0, str(Path(__file__).parent / "code"))`
  3. code/ directory exists
  4. code/app/ directory exists

---

## Deployment Checklist

Before deploying (if you changed deployment-related files):

- [ ] `asgi.py` runs locally without errors
- [ ] `Procfile` command works locally
- [ ] `requirements.txt` has all packages you added
- [ ] No secrets in code (use env vars)
- [ ] Tested in browser (all pages load)
- [ ] Committed all changes
- [ ] Pushed to GitHub

---

## Render Dashboard

**Login:** render.com → Your dashboard

**Watch for:**
- Service status (green = good, red = crashed)
- Logs (click to see what app is doing)
- Build/deploy history
- Environment variables
- Custom domain settings

**Common Render Dashboard Actions:**

| Action | Where | When |
|--------|-------|------|
| View logs | Logs tab | Debugging errors |
| Redeploy | Manual Deploy | Force redeploy |
| Environment vars | Settings | Add API keys, secrets |
| Custom domain | Settings | Point fullstackpm.tech to Render |

---

## Performance Tips

1. **Images** → Compress before using
2. **CSS** → Tailwind on CDN (not hosted locally)
3. **JavaScript** → Keep minimal (using HTMX instead)
4. **Content** → Markdown stays fast (no database queries)

---

## Security Reminders

🔒 **Never commit:**
- API keys
- Database passwords
- Auth tokens
- Any secrets

✅ **Instead:**
- Use environment variables
- Set in Render dashboard
- Read from `os.environ` or pydantic Settings

---

## Future: Next Projects

When you build the PM Interview Coach and other projects:

1. Keep same architecture pattern
2. Use same design system (custom.css, base.html)
3. Host on same Render service (under `/tools/coach`, etc.)
4. Add markdown docs to `code/content/projects/`
5. Follow same deployment process

---

## Git Workflow (Standard)

```bash
# See what changed
git status

# Add files to commit
git add file1.py file2.md

# Create commit
git commit -m "Brief description"

# Push to GitHub
git push origin main

# Render sees push, auto-deploys
```

---

## Useful Commands

```bash
# Install packages
pip install -r requirements.txt

# Update all packages
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Run locally
cd code && python -m uvicorn app.main:app --reload

# Check if port is free
lsof -i :8000

# Git log (see history)
git log --oneline

# Git diff (see what changed)
git diff

# Git reset (undo uncommitted changes)
git checkout -- filename
```

---

## URLs Reference

| Route | What It Shows |
|-------|---|
| `/` | Home page |
| `/about` | About page with experience |
| `/contact` | Contact info |
| `/resume` | Resume/CV |
| `/projects` | Project gallery |
| `/projects/{slug}` | Individual project |
| `/blog` | Blog listing (paginated) |
| `/blog/{slug}` | Individual blog post |
| `/blog/tag/{tag}` | Posts by tag |
| `/feed.xml` | RSS feed |
| `/sitemap.xml` | XML sitemap for search engines |
| `/robots.txt` | Instructions for crawlers |
| `/static/css/custom.css` | Design tokens |
| `/static/js/main.js` | Interactive features |

---

## Next Person To Work On This

If someone else maintains this project:

1. Read `learnings/01_OVERVIEW.md` first
2. Understand the folder structure
3. Run locally and verify it works
4. Make small changes first
5. Use this quick reference
6. When adding features, follow existing patterns
7. Keep documentation updated

---

**Remember:** This project is clean, well-organized, and straightforward. It's a great foundation for expansion. Don't over-engineer—keep it simple.

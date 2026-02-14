# Development: Local Setup & Workflow

## Prerequisites

- Python 3.10+ (check: `python --version`)
- Git (check: `git --version`)
- Code editor (VS Code, PyCharm, etc.)
- Terminal/CLI

---

## Local Setup (5 min)

### 1. Clone the Repo
```bash
git clone https://github.com/harsha-k-cheruku/fullstackpm.tech.git
cd fullstackpm.tech
```

### 2. Create Python Virtual Environment
```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the root (or use Render dashboard later):
```bash
OPENAI_API_KEY=sk-your-key-here
```

**Don't have OpenAI key?** Get one at https://platform.openai.com/api-keys

### 5. Run the App
```bash
cd code
python -m uvicorn app.main:app --reload --port 8001
```

Visit: http://localhost:8001

You should see the homepage! 🎉

---

## Project Structure for Development

```
code/app/
├── main.py                    ← Start here (entry point)
├── config.py                  ← Settings (edit to change behavior)
├── database.py                ← SQLAlchemy setup (don't edit)
├── routers/
│   ├── pages.py               ← Home, About, Contact routes
│   ├── blog.py                ← Blog posts
│   ├── projects.py            ← Projects gallery
│   ├── interview_coach.py     ← Interview practice tool
│   └── marketplace.py         ← Analytics dashboard
├── services/
│   ├── content.py             ← Read markdown files
│   ├── interview_evaluator.py ← AI evaluation logic
│   └── analytics.py           ← Data aggregations
├── models/
│   ├── comment.py             ← Database schema
│   └── interview_session.py   ← Database schema
└── templates/                 ← HTML templates
    ├── base.html              ← Base layout
    ├── home.html
    ├── blog/
    │   ├── list.html
    │   └── detail.html
    └── ...
```

---

## Common Development Tasks

### Add a New Blog Post

1. Create file: `/code/content/blog/YYYY-MM-DD-slug.md`

2. Write YAML frontmatter:
```yaml
---
title: "My Post Title"
date: 2026-02-15
tags: [tag1, tag2, tag3]
excerpt: "2-3 sentence summary"
author: "Your Name"
---

## Introduction

Post content here...
```

3. Restart server (Ctrl+C, then run uvicorn again)

4. Visit: http://localhost:8001/blog

### Add a New Project

1. Create file: `/code/content/projects/my-project.md`

2. Write YAML frontmatter:
```yaml
---
title: "Project Name"
description: "One-liner"
tech_stack: [Tech1, Tech2]
status: "live"          # live, in_progress, planned
featured: true
display_order: 1
github_url: "https://..."
live_url: "https://..."
problem: "Problem statement"
approach: "Solution approach"
solution: "What you built"
---

## What
...
```

3. Restart server

4. Visit: http://localhost:8001/projects

### Edit a Template

1. Edit `/code/app/templates/home.html` (or any template)

2. Save

3. Reload browser (Cmd+R / Ctrl+R)

4. Changes appear instantly (FastAPI --reload watches files)

### Edit CSS

1. Edit `/code/app/static/css/custom.css`

2. Save

3. Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)

4. Changes appear

### Edit Python Code

1. Edit any `.py` file in `/code/app/`

2. Save

3. Server auto-restarts (because of `--reload`)

4. Reload browser to see changes

---

## Debugging

### View Server Logs
```bash
# Terminal shows logs as you use the app
[INFO] GET / - "200 OK"
[ERROR] ValueError: Invalid status
```

### Add Print Statements
```python
# In any route
@router.get("/blog")
async def blog(request: Request):
    print("DEBUG: Blog route called")
    content_service = request.app.state.content_service
    posts = content_service.get_posts()
    print(f"DEBUG: Found {len(posts)} posts")  # ← Check terminal
    return ...
```

### Test a Route in Browser
- Visit http://localhost:8001/api/projects/filter?status=live
- See the raw HTML response
- Helps debug HTMX interactions

### Use Browser DevTools
- Right-click → "Inspect"
- Check Console for JavaScript errors
- Check Network tab for API requests

---

## Database

### View Data (SQLite)
```bash
# Install sqlite3 CLI if needed
sqlite3 code/app/data/fullstackpm.db

# Inside sqlite3:
.tables                    # See all tables
SELECT * FROM comments;    # View comments
SELECT * FROM interview_attempt LIMIT 5;
```

### Reset Database
```bash
# Delete the file (next run will recreate it)
rm code/app/data/fullstackpm.db

# Or restart the server
```

---

## Testing Locally

### Test Interview Coach
1. Visit http://localhost:8001/tools/interview-coach
2. Pick a category
3. Answer a question
4. See AI evaluation (uses OpenAI API key)

### Test Blog Comments
1. Visit http://localhost:8001/blog
2. Click on any post
3. Add a comment
4. Check it appears (SQLite stores it)

### Test Project Filters
1. Visit http://localhost:8001/projects
2. Click filter buttons
3. See HTMX update grid in real-time

### Test Dark Mode
1. Click sun/moon icon in navbar
2. Page toggles dark mode
3. Check CSS variables update

---

## Git Workflow

### See What Changed
```bash
git status
```

### Add Changes
```bash
git add code/app/templates/home.html
# Or add everything:
git add .
```

### Commit
```bash
git commit -m "Update: Fix homepage hero text"
```

### Push to GitHub
```bash
git push origin main
```

### Render Auto-Deploys
- ~1-2 minutes after push
- Check https://fullstackpm-tech.onrender.com

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'app'` | Make sure you're running from `/code` directory or edit `asgi.py` |
| `OPENAI_API_KEY not found` | Add to `.env` file or Render environment |
| `Blog posts not showing` | Restart server (changes to `/content` require restart) |
| `CSS not updating` | Hard refresh (Cmd+Shift+R / Ctrl+Shift+R) |
| `Database locked` | Close other sqlite3 sessions or delete `.db` file |
| `Port 8001 already in use` | Change to different port: `--port 8002` |

---

## Next Steps

- **Read:** [ARCHITECTURE.md](./ARCHITECTURE.md) to understand how it all fits together
- **Deploy:** Push to GitHub, watch Render auto-deploy
- **Build:** Add features by following patterns in existing code
- **Iterate:** Make changes locally, test, commit, push

---

## Questions?

- **How do I add a new tool?** Create route in `routers/`, template in `templates/`
- **How do I query the database?** Use SQLAlchemy in `services/` or `routers/`
- **How do I call OpenAI API?** See `services/interview_evaluator.py` for pattern
- **How do I add a new CSS feature?** Edit `code/app/static/css/custom.css`

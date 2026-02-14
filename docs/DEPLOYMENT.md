# Deployment: How Render Hosts fullstackpm.tech

## TL;DR

**What gets deployed:**
- The `/code` folder (FastAPI app)
- Python dependencies from `requirements.txt`

**What doesn't:**
- `/project_ideas/` (GitHub only)
- `/docs/` (GitHub only)
- Blog posts in `/content/blog/` (deployed as static content, read by the app at runtime)

**Deployment is triggered:** Every time you push to `main` branch on GitHub

**Time to live:** 1-2 minutes

---

## How Render Reads Your Repo

```
Your GitHub Repo (fullstackpm.tech)
    ↓
Render checks Procfile
    ↓
Procfile says: "python -m uvicorn asgi:app --host 0.0.0.0 --port $PORT"
    ↓
Render:
  1. Installs dependencies from requirements.txt
  2. Runs asgi.py (entry point)
  3. asgi.py adds /code to Python path
  4. Starts FastAPI app on port 8000+
    ↓
Your site is live at https://fullstackpm-tech.onrender.com
```

---

## Key Files for Deployment

### 1. `requirements.txt` (Root Level)

Located in the project root, tells Render what Python packages to install.

```
fastapi==0.109.0
uvicorn==0.27.0
jinja2==3.1.2
pydantic==2.6.0
python-multipart==0.0.6
markdown==3.5.2
sqlalchemy==2.0.45
openai==1.30.0
```

**Important:** Must be in repo root, not `/code/requirements.txt` (Render looks there first).

### 2. `asgi.py` (Root Level)

Entry point that Render uses. Sets up Python path and starts the app.

```python
from pathlib import Path
import sys
import uvicorn

# Add /code to Python path so "from app..." imports work
sys.path.insert(0, str(Path(__file__).parent / "code"))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
```

### 3. `Procfile`

Tells Render how to start your app.

```
web: python -m uvicorn asgi:app --host 0.0.0.0 --port $PORT
```

**Note:** `$PORT` is environment variable Render sets (usually 10000).

---

## What Happens on Push

### Step 1: GitHub Webhook
```
You: git push origin main
    ↓
GitHub: "Someone pushed to main!"
    ↓
GitHub webhook triggers Render deployment
```

### Step 2: Render Reads Config
```
Render: "What should I deploy?"
    ↓
Reads Procfile
    ↓
Reads requirements.txt
    ↓
Determines service type (Python app)
```

### Step 3: Build Phase (2-5 min)
```
Render:
  1. Clones your repo
  2. Creates fresh Python environment
  3. Runs: pip install -r requirements.txt
  4. Tests that asgi.py can be imported
```

### Step 4: Deploy Phase (1 min)
```
Render:
  1. Stops old server (if running)
  2. Starts new server: python -m uvicorn asgi:app ...
  3. Checks health endpoint (GET /)
  4. Routes traffic to new server
```

### Step 5: Monitoring
```
Live at: https://fullstackpm-tech.onrender.com

If errors occur:
  - Render shows logs in dashboard
  - Can rollback to previous deployment
  - Will restart automatically on crash
```

---

## What Renders Sees vs. Doesn't See

### ✅ DEPLOYED (Render processes)
```
code/                           → Deployed as Python app
content/blog/*.md               → Loaded by ContentService at runtime
content/projects/*.md           → Loaded by ContentService at runtime
requirements.txt                → Dependencies installed
asgi.py                         → Entry point
Procfile                        → Deployment instructions
.github/workflows/              → Can trigger custom deployments
```

### ❌ NOT DEPLOYED (GitHub only)
```
project_ideas/                  → Docs only, no impact
docs/                           → Docs only, no impact
BUILD_*.md                      → Plans only, no impact
.git/                           → Hidden (version history)
README.md                       → Displayed on GitHub, not served
PROJECTS_STATUS.md              → Docs only, no impact
```

### 🎯 KEY INSIGHT
Render only cares about:
1. What's in `/code` (the app itself)
2. What's in `/content` (loaded at runtime by ContentService)
3. `requirements.txt` + `asgi.py` + `Procfile`

Everything else? **Completely ignored by Render.** You can reorganize docs, add project plans, whatever—Render doesn't care.

---

## Folder Reorganization Impact

### Before
```
fullstackpm.tech/
├── code/
├── content/
├── project_ideas/
├── requirements.txt
├── asgi.py
└── Procfile
```

### After (Reorganized)
```
fullstackpm.tech/
├── code/
├── content/
├── project_ideas/
├── docs/
├── BUILD_*.md
├── PROJECTS_STATUS.md
├── requirements.txt         ← Still here
├── asgi.py                  ← Still here
└── Procfile                 ← Still here
```

### Render's Perspective
```
Before deployment: ✅ Works
After reorganization: ✅ Still works (nothing changed for Render)
```

---

## How Content Gets Deployed

### Markdown Content Path
```
1. You write: code/content/blog/2026-02-09-my-post.md
2. You git push
3. Render clones repo (gets the .md file)
4. FastAPI starts
5. ContentService reads /code/content/blog/ directory
6. Loads all .md files into memory
7. When user visits /blog/my-post:
   - Router calls ContentService.get_post_by_slug("my-post")
   - Returns parsed HTML
   - Renders template
   - User sees blog post
```

**Key:** Content files live in Git but are *not precompiled*. They're read and parsed at runtime.

### Why This Works Well
✅ Version history (Git)
✅ Easy to edit (just markdown)
✅ Fast loads (cached in memory)
✅ No build step needed
✅ No database required

---

## Environment Variables

Render sets some automatically:
- `PORT` — Which port to listen on (Render assigns)

You can set in Render dashboard:
- `OPENAI_API_KEY` — For Interview Coach
- `DATABASE_URL` — If you migrate to PostgreSQL (not needed now)

Check them in Render dashboard: Settings → Environment

---

## Monitoring Deployments

### Render Dashboard
- Shows deployment history
- Live logs (tail -f style)
- Health status (running, crashed, etc.)
- Manual deployment trigger (if needed)
- Rollback to previous version (if something breaks)

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'app'` | Python path issue | Check `asgi.py` has correct sys.path insert |
| `No such file: requirements.txt` | Missing root requirements | Add requirements.txt to root |
| `ImportError: cannot import name 'settings'` | Code errors | Fix code, push again |
| `Crashed` | App exited | Check logs in Render dashboard |

---

## Zero-Downtime Deployments

Render handles this automatically:
```
Old server running
    ↓
New server starts
    ↓
Health check passes
    ↓
Traffic switches (instant)
    ↓
Old server stops
```

Result: No downtime, users don't notice.

---

## Cost Structure

### Current Setup ($20-30/month)

| Service | Cost | Notes |
|---------|------|-------|
| Render Free Tier | $0 | Scales up as needed |
| Render Pro | $12/month | Better for production |
| OpenAI (Interview Coach) | $5-10/month | ~1000 evaluations/month |
| **Total** | **$17-22/month** | Very cheap! |

### If You Scale

| Scenario | Cost | When |
|----------|------|------|
| 1M monthly users | $100-200 | Need Render paid tier |
| Extract Interview Coach | $0-500 | If you monetize separately |
| PostgreSQL instead SQLite | +$15/month | If >1M interview sessions |

---

## Deployment Checklist

Before pushing to production:

- [ ] `requirements.txt` is at root, not in `/code`
- [ ] `asgi.py` exists and adds `/code` to sys.path
- [ ] `Procfile` points to `asgi:app`
- [ ] All imports use `from app...` (assuming `asgi.py` fixes path)
- [ ] No hardcoded file paths (use `settings.templates_dir`)
- [ ] `OPENAI_API_KEY` is set in Render environment
- [ ] Local test passes: `python -m uvicorn asgi:app --reload`

---

## Rolling Back

If deployment goes wrong:

1. **In Render dashboard:**
   - Go to Deployments
   - Click "Deploy" on previous working version
   - New version instantly rolls back

2. **Or via GitHub:**
   - Revert your commit
   - `git push origin main`
   - Render auto-redeploys

---

## Questions?

- **How often does Render update?** Every time you push to `main`
- **Can I deploy manually?** Yes, trigger from Render dashboard
- **What about database backups?** SQLite files are versioned in Git
- **Can I add a custom domain?** Yes, in Render settings
- **What if I want a staging environment?** Create a different branch, connect different Render service

See [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details.

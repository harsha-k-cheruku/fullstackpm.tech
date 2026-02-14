# Deployment Guide: Step-by-Step

## What is Deployment?

Deployment = Taking code from your laptop and making it run on a cloud server so anyone can access it.

---

## The Deployment Flow

```
┌─────────────┐
│ Local Code  │
│  (on your   │
│  laptop)    │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  Push to GitHub  │
│  (git push)      │
└──────┬───────────┘
       │
       ↓
┌──────────────────────┐
│  Render sees update  │
│  (GitHub webhook)    │
└──────┬───────────────┘
       │
       ↓
┌──────────────────────────┐
│ Render pulls code        │
│ Installs dependencies    │
│ Runs Procfile command    │
│ Starts your app          │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│ App is live on internet  │
│ Users can visit it       │
└──────────────────────────┘
```

---

## Files Needed for Deployment

### 1. requirements.txt

**What it is:** List of Python packages your app needs.

**Example:**
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
jinja2==3.1.4
python-multipart==0.0.9
python-frontmatter==1.1.0
markdown==3.7
pygments==2.18.0
pydantic-settings==2.11.0
```

**Why it matters:** When Render starts your app, it runs `pip install -r requirements.txt`. Without this, Python packages won't be installed.

**What each package does:**
- **fastapi** → Web framework
- **uvicorn** → Server that runs FastAPI
- **jinja2** → Template engine (renders HTML)
- **python-multipart** → Handles form data
- **python-frontmatter** → Parses YAML in markdown files
- **markdown** → Converts markdown to HTML
- **pygments** → Code syntax highlighting
- **pydantic-settings** → Configuration management

---

### 2. Procfile

**What it is:** Instructions for how to run your app on Render.

**Example:**
```
web: python -m uvicorn asgi:app --host 0.0.0.0 --port $PORT
```

**What each part means:**
- `web` → This is a web process (HTTP server)
- `python -m uvicorn` → Use Python to run uvicorn module
- `asgi:app` → Import the `app` variable from `asgi.py`
- `--host 0.0.0.0` → Listen on all network interfaces (so Render can reach it)
- `--port $PORT` → Use the port that Render provides (usually 3000 or 5000)

**Why it matters:** Render needs to know exactly how to start your app. Without Procfile, Render would guess and probably get it wrong.

---

### 3. asgi.py (Entry Point)

**What it is:** The "front door" of your app. A bridge that connects Render to your actual code.

**Why you need it:** Your code is in `/code/app/main.py`, but Render expects the app at the root. This file handles that mismatch.

**What it does:**
```python
import sys
from pathlib import Path

# Add code directory to Python's search path
sys.path.insert(0, str(Path(__file__).parent / "code"))

# Now Python can find the app module
from app.main import app
```

---

## Step-by-Step: Your First Deployment

### Step 1: Create Procfile (if not exists)

File: `Procfile` (at repository root)
```
web: python -m uvicorn asgi:app --host 0.0.0.0 --port $PORT
```

### Step 2: Create requirements.txt (if not exists)

File: `requirements.txt` (at repository root)
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
jinja2==3.1.4
python-multipart==0.0.9
python-frontmatter==1.1.0
markdown==3.7
pygments==2.18.0
pydantic-settings==2.11.0
```

### Step 3: Create asgi.py (if not exists)

File: `asgi.py` (at repository root)
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "code"))

from app.main import app
```

### Step 4: Commit to Git

```bash
git add Procfile requirements.txt asgi.py
git commit -m "Add deployment files"
git push origin main
```

### Step 5: Create Render Account

1. Go to render.com
2. Sign up (free)
3. Connect GitHub account

### Step 6: Deploy

1. Click "New +" on Render dashboard
2. Click "Web Service"
3. Select your GitHub repository
4. Select repository branch (usually `main`)
5. Set:
   - **Name:** `fullstackpm`
   - **Runtime:** `Python 3`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn asgi:app --host 0.0.0.0 --port 8000`
6. Click "Deploy"
7. Wait 2-3 minutes
8. Your app is live!

### Step 7: Test

Visit your Render URL (e.g., `fullstackpm.onrender.com`)

---

## Common Issues & Fixes

### Issue 1: ModuleNotFoundError: No module named 'app'

**What went wrong:** Python can't find your app module.

**Common causes:**
1. `asgi.py` doesn't exist
2. `asgi.py` doesn't add `/code` to path
3. Path syntax is wrong

**Fix:**
```python
# asgi.py should have:
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "code"))
from app.main import app
```

---

### Issue 2: Build failed: No such file 'requirements.txt'

**What went wrong:** Render can't find `requirements.txt`.

**Common causes:**
1. File is in `/code/` subdirectory instead of root
2. File name is misspelled (should be `requirements.txt`, not `requirements.TXT`)
3. File wasn't pushed to GitHub

**Fix:**
- Make sure `requirements.txt` is at repository root
- Run `git add requirements.txt && git push`
- Redeploy

---

### Issue 3: Build fails during pip install

**What went wrong:** One of your dependencies can't be installed.

**Common causes:**
1. Version number is too old
2. Package doesn't exist
3. Package isn't compatible with Python 3.14

**Fix:**
```bash
# On your laptop, verify packages work locally:
pip install -r requirements.txt

# If that fails, update versions:
pip install --upgrade fastapi uvicorn
pip freeze > requirements.txt
git add requirements.txt && git push
```

---

### Issue 4: App starts but returns 500 error

**What went wrong:** Code runs but has a runtime error.

**How to debug:**
1. Click "Logs" in Render dashboard
2. Look for error traceback
3. Common errors:
   - `TemplateNotFound` → Template file doesn't exist or is in wrong path
   - `FileNotFoundError` → Content file doesn't exist
   - `ImportError` → Code has import errors

**Fix:**
- Fix the error locally
- Test with `uvicorn asgi:app --reload`
- Push to GitHub
- Redeploy

---

## After Deployment: Making Changes

### Workflow for Updates

```
1. Make code changes locally
2. Test locally: uvicorn asgi:app --reload
3. Commit: git commit -m "Description"
4. Push: git push origin main
5. Render auto-deploys (2-3 minutes)
6. Changes are live
```

### Adding New Content

**New blog post:**
1. Create file: `code/content/blog/YYYY-MM-DD-title.md`
2. Add YAML frontmatter + content
3. `git add` and `git push`
4. Render redeploys
5. Blog post appears automatically

**New project:**
1. Create file: `code/content/projects/project-name.md`
2. Add YAML frontmatter + description
3. `git add` and `git push`
4. Render redeploys
5. Project appears automatically

---

## Environment Variables (For Secrets)

If you need to store secrets (API keys, database passwords), use environment variables:

**In code:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    claude_api_key: str = ""  # Reads from CLAUDE_API_KEY env var

    class Config:
        env_file = ".env"
```

**In Render:**
1. Go to service Settings
2. Find "Environment Variables"
3. Add key/value pair: `CLAUDE_API_KEY=sk-...`
4. Redeploy

**Never commit secrets!** Always use environment variables.

---

## Monitoring Your App

**In Render Dashboard:**
- **Logs** → See what your app is doing
- **Metrics** → CPU, memory usage
- **Health** → Is app running or crashed?

**Common issues to watch for:**
- Memory usage growing → Memory leak
- CPU stuck at 100% → Infinite loop or performance issue
- App keeps restarting → Crashes immediately after starting

---

## Scaling (When You Get Lots of Users)

**Current setup:**
- Free Render tier
- 1 web dyno (server)
- 512MB RAM

**If you hit limits:**
1. Upgrade to paid Render plan ($7/month)
2. Increase dyno size (more RAM/CPU)
3. Add database if needed (for user accounts, etc.)

**For 1000s of users**, current setup is fine. Render handles the scaling.

---

## Database (Not Needed Yet)

Your app currently uses:
- **Filesystem** for content (markdown files)
- **In-memory cache** for content service

This is great for:
- Blogs (content is static)
- Portfolios (no user data)
- Documentation sites

But NOT great for:
- User accounts
- Real-time data
- Frequent updates

When/if you need a database:
1. Add database service (Render offers PostgreSQL)
2. Add ORM like SQLAlchemy
3. Update requirements.txt
4. Redeploy

---

## Best Practices

### ✅ Do This

- Keep `Procfile`, `requirements.txt`, `asgi.py` at repository root
- Test locally before pushing
- Use environment variables for secrets
- Monitor Render logs after deployment
- Keep dependencies up to date
- Document how to run locally

### ❌ Don't Do This

- Commit secrets to Git
- Change version pins without testing
- Deploy without testing locally
- Leave debug mode on in production
- Ignore error logs
- Have code in weird nested directories

---

## Your Deployment Checklist

- [ ] `Procfile` exists at root
- [ ] `requirements.txt` exists at root
- [ ] `asgi.py` exists at root
- [ ] All three files are in Git
- [ ] Procfile has correct start command
- [ ] requirements.txt lists all dependencies
- [ ] asgi.py adds `/code` to Python path
- [ ] Code tested locally and works
- [ ] GitHub repo is public (or connected to Render)
- [ ] Render account created
- [ ] Render connected to GitHub
- [ ] Deploy succeeds (no build errors)
- [ ] App loads in browser (returns 200, not 500)
- [ ] Pages render correctly
- [ ] Dark mode works
- [ ] Blog/projects load

---

## Troubleshooting: The Scientific Method

When something breaks:

1. **Observe** → What's the error message?
2. **Reproduce locally** → Can you make it fail on your laptop?
3. **Isolate** → What changed? (Last commit, dependency, code?)
4. **Hypothesis** → What do you think is wrong?
5. **Test** → Fix it and verify it works
6. **Deploy** → Push to GitHub, Render auto-deploys
7. **Verify** → Check that fix worked on production

---

**Next Time You Deploy:** You'll breeze through it. Deployment is mostly just getting the details right—paths, file names, environment variables. The concepts are simple once you've done it once.

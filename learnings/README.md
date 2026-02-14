# Learning Documentation

This folder contains comprehensive guides about your fullstackpm.tech deployment and web development concepts.

## Start Here

### 📖 For a High-Level Understanding
Read in this order:
1. **01_OVERVIEW.md** — What we built and why it was hard (10 min read)
2. **02_ARCHITECTURE.md** — How the application is structured (15 min read)
3. **04_WEB_CONCEPTS.md** — Key web development concepts (15 min read)

### 🚀 For Deployment Knowledge
1. **03_DEPLOYMENT_GUIDE.md** — Step-by-step deployment instructions
2. **05_QUICK_REFERENCE.md** — Checklists and quick answers

### 🔍 For Specific Questions
- "How do I add a blog post?" → 05_QUICK_REFERENCE.md
- "What's wrong with my deployment?" → 03_DEPLOYMENT_GUIDE.md (Troubleshooting section)
- "How does the app work?" → 02_ARCHITECTURE.md
- "What is HTTP/REST?" → 04_WEB_CONCEPTS.md

---

## File Descriptions

| File | Length | What You'll Learn | Best For |
|------|--------|---|---|
| **01_OVERVIEW.md** | 10 min | What went wrong and why we fixed it | Understanding the journey |
| **02_ARCHITECTURE.md** | 20 min | How your app works end-to-end | Understanding structure |
| **03_DEPLOYMENT_GUIDE.md** | 20 min | Step-by-step deployment process | Setting up again |
| **04_WEB_CONCEPTS.md** | 20 min | HTTP, templates, caching, etc. | Understanding web dev |
| **05_QUICK_REFERENCE.md** | 15 min | Quick answers and commands | Daily reference |

**Total reading time:** ~90 minutes (but you don't need to read it all at once)

---

## Problem-Solving Guide

### "I made changes but they're not showing up"

1. Did you commit? → `git status`
2. Did you push? → `git log --oneline`
3. Check Render logs → Dashboard → Logs tab
4. Is there an error? → 03_DEPLOYMENT_GUIDE.md Troubleshooting

### "Something broke on production"

1. Check Render logs → Find error message
2. Try to reproduce locally
3. Fix locally + test
4. Commit + push
5. Render auto-deploys

### "How do I add X?"

- Blog post → 05_QUICK_REFERENCE.md (Adding Content)
- New page → 05_QUICK_REFERENCE.md (Common Tasks)
- New feature → 02_ARCHITECTURE.md (Find right layer)

### "I forgot how deployment works"

Read 03_DEPLOYMENT_GUIDE.md again. It's comprehensive.

---

## Key Concepts Summary

### What Deployment Is
Moving code from your laptop to a cloud server (Render) so the website runs 24/7 and anyone can visit it.

### Why It Was Hard
Your code was in a `/code/` subdirectory, but the server expected it at root. We solved this with `asgi.py` entry point.

### How It Works Now
```
1. You edit code locally
2. Test with: python -m uvicorn app.main:app --reload
3. Commit and push to GitHub
4. Render sees the push
5. Render runs: python -m uvicorn asgi:app
6. Your website is live
```

### The Three Key Files
- **asgi.py** — Tells Python where to find your app
- **Procfile** — Tells Render how to start your app
- **requirements.txt** — Lists Python packages Render needs to install

### Your Architecture
```
asgi.py (entry point)
    ↓
app/main.py (FastAPI setup)
    ↓
routers/ (handle different URLs)
    ↓
services/ (business logic)
    ↓
templates/ (generate HTML)
```

---

## Glossary

| Term | What It Means |
|------|---|
| **Deploy** | Put code on internet |
| **FastAPI** | Python web framework |
| **Uvicorn** | Python web server |
| **Render** | Cloud hosting platform |
| **Git** | Version control |
| **Procfile** | Deployment instructions |
| **ASGI** | Protocol for async web apps |
| **Jinja2** | Template engine |
| **HTTP** | How web works |
| **Router** | Maps URL paths to code |
| **Service** | Business logic layer |
| **Cache** | Stored data for speed |
| **Static files** | CSS, JS, images |
| **Dynamic content** | Generated HTML |

---

## Quick Commands

```bash
# Local development
cd code && python -m uvicorn app.main:app --reload

# Git workflow
git add .
git commit -m "your message"
git push origin main

# Check dependencies
pip list
pip install -r requirements.txt
```

---

## When Things Go Wrong

### 500 Error on Render
→ Check Render logs for error message
→ Reproduce locally
→ Fix locally, test, push

### Module not found
→ Check asgi.py has correct path setup
→ Verify code/ and code/app/ directories exist

### Site won't load at all
→ Check Render logs
→ Check Procfile syntax
→ Check requirements.txt has all packages

### Blog post won't show
→ Verify file location: code/content/blog/
→ Verify YAML frontmatter has all required fields
→ Restart local server

---

## Best Practices Going Forward

### ✅ Do This
- Test changes locally before pushing
- Write descriptive git commit messages
- Keep Procfile, asgi.py, requirements.txt at root
- Store secrets in environment variables (not code)
- Document new features

### ❌ Don't Do This
- Commit secrets to Git
- Change code and push without testing
- Ignore Render error logs
- Manually edit code on the server (always push from Git)
- Leave old test code around

---

## Files You Created/Modified

This deployment required these new files:

```
fullstackpm.tech/
├── asgi.py                    # NEW - Entry point
├── Procfile                   # NEW - Deployment instructions
├── requirements.txt           # NEW - Python packages (moved to root)
├── code/__init__.py           # NEW - Makes code/ a package
├── learnings/                 # NEW - This documentation
│   ├── README.md              # You're reading this
│   ├── 01_OVERVIEW.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_DEPLOYMENT_GUIDE.md
│   ├── 04_WEB_CONCEPTS.md
│   └── 05_QUICK_REFERENCE.md
```

---

## Learning Path (If You Want to Deepen Knowledge)

**Week 1:** Read all files in this folder (90 min)
**Week 2:** Make small changes locally and on Render
**Week 3:** Add new blog posts and projects
**Week 4:** Start PM Interview Coach project (new deployment practice)

---

## Questions to Ask Yourself

After reading these docs, you should be able to answer:

1. ✅ What does "deployment" mean?
2. ✅ Why did we need asgi.py?
3. ✅ What files did we need at the repository root?
4. ✅ How does a request turn into a response?
5. ✅ Why is the app fast?
6. ✅ What happens when you push to GitHub?
7. ✅ How do you add a blog post?
8. ✅ What's in Procfile and why?
9. ✅ How do you troubleshoot a broken deployment?
10. ✅ What's the difference between static and dynamic content?

If you can answer these, you understand the full deployment!

---

## Sharing This Knowledge

If someone asks you "How do you deploy a Python web app?" you can now explain:

**Simple answer (30 seconds):**
> "You put your code on GitHub, connect it to a platform like Render, tell Render how to run your app (Procfile), and Render deploys it automatically whenever you push. My app is FastAPI running on Render."

**Detailed answer (5 minutes):**
> Start with 01_OVERVIEW.md

**Full breakdown (30 minutes):**
> Read all five documents in order

---

## Updates and Additions

As you learn more and work with this project, consider adding to these docs:

- [ ] Common deployment mistakes you made
- [ ] Debugging techniques you discovered
- [ ] Performance optimizations
- [ ] New features you added
- [ ] Lessons learned

Keep this folder living and updated!

---

## Meta: Why These Docs Exist

Traditional deployment tutorials are confusing because they jump between topics and assume too much. These docs are specifically about **your project** and explain:

1. **What happened** (errors you got)
2. **Why it happened** (path issues, module conflicts)
3. **How we fixed it** (asgi.py solution)
4. **How it works now** (architecture overview)
5. **How to do it again** (step-by-step guide)
6. **Context** (web development concepts)

This is **targeted learning** instead of generic tutorials.

---

## Next Steps

1. **This week:** Read all docs (takes 2 hours)
2. **Next week:** Deploy PM Interview Coach (same process, new app)
3. **Future:** Become the person who teaches others how to deploy

---

**You just learned full-stack deployment. That's valuable knowledge. Document what you learn so you never forget.**

Good luck! 🚀

# 📋 Active Task List — Sequential Work Items

**Last Updated:** February 13, 2026
**Workflow:** Planner (Me) → Builder (Other LLM) → Reviewer (Me) → Integration (You)

---

## 🚀 IMMEDIATE TASKS (This Week)

### TASK 1: Complete HTMX Interactions [EST: 45 min]
**Status:** ⏳ Ready to assign
**Owner:** Other LLM (builder)
**Depends on:** Portfolio site foundation (✅ complete)

**What:**
Complete BUILD_06 by adding HTMX endpoints and wiring them to templates

**Detailed Instructions:**

1. **Add 2 new endpoints to `/fullstackpm.tech/code/app/routers/blog.py`:**
```python
@router.get("/api/blog/posts", response_class=HTMLResponse)
async def blog_posts_htmx(request: Request, page: int = Query(1, ge=1)):
    """HTMX endpoint that returns post_list.html partial"""
    posts, has_prev, has_next = app.content.get_blog_posts(page=page)
    return templates.TemplateResponse(
        "blog/partials/post_list.html",
        {"request": request, "posts": posts, "page": page, "has_next": has_next, "has_prev": has_prev}
    )
```

2. **Add 1 new endpoint to `/fullstackpm.tech/code/app/routers/projects.py`:**
```python
@router.get("/api/projects/filter", response_class=HTMLResponse)
async def projects_filter_htmx(request: Request, status: str = Query("all")):
    """HTMX endpoint that returns project_grid.html partial"""
    all_projects = app.content.get_projects()
    if status != "all":
        projects = [p for p in all_projects if p.metadata.get("status") == status]
    else:
        projects = all_projects
    return templates.TemplateResponse(
        "projects/partials/project_grid.html",
        {"request": request, "projects": projects}
    )
```

3. **Update `/fullstackpm.tech/code/app/templates/blog/list.html`:**
   - Add "Load More" button with: `hx-get="/api/blog/posts?page=2" hx-target="#post-list" hx-swap="innerHTML"`
   - Wrap posts in: `<div id="post-list">`

4. **Update `/fullstackpm.tech/code/app/templates/projects/gallery.html`:**
   - Add filter dropdown: `<select hx-get="/api/projects/filter?status={value}" hx-target="#project-grid" hx-swap="innerHTML">`
   - Wrap projects in: `<div id="project-grid">`

**Acceptance Test:**
- ✅ GET /api/blog/posts?page=1 returns HTML (200 OK)
- ✅ GET /api/projects/filter?status=all returns HTML (200 OK)
- ✅ Click "Load More" in blog → next page loads without full refresh
- ✅ Select filter in projects → list updates without full refresh
- ✅ HTMX loading indicator shows briefly

**What to Deliver:**
- Updated `blog.py` (with new endpoint)
- Updated `projects.py` (with new endpoint)
- Updated `list.html` (with HTMX wiring)
- Updated `gallery.html` (with HTMX wiring)

**My Review Process:**
- ✅ Code follows same style as existing routers
- ✅ HTMX attributes correct (hx-get, hx-target, hx-swap)
- ✅ Endpoints tested and working
- ✅ No breaking changes to existing code

**Then You:**
- Copy files to local repo
- Test locally at http://localhost:8001/blog and /projects
- Click "Load More" button
- Test filter dropdown

---

### TASK 2: Add Sample Content [EST: 1.5 hours]
**Status:** ⏳ Ready
**Owner:** You (manually or AI)
**Depends on:** TASK 1 (optional, can do in parallel)

**What:**
Create 3 more projects + 3 more blog posts to give portfolio more substance

**Step-by-step:**

**Step 1: Add 3 Projects**

Create in `/fullstackpm.tech/code/content/projects/`:

**File 1: `fullstack-ai-bootcamp.md`**
```markdown
---
title: FullStack AI Bootcamp
description: AI-powered learning platform for product management
featured: true
status: live
tech:
  - Claude API
  - FastAPI
  - Notion
  - React
display_order: 1
---

# FullStack AI Bootcamp

High-quality AI-powered education platform for PMs learning AI applications...
[Add detailed description]
```

**File 2: `pm-agent-toolkit.md`**
```markdown
---
title: PM Agent Toolkit
description: Open-source framework for PM decision-making
featured: true
status: in-progress
tech:
  - Python
  - Pydantic AI
  - Claude API
  - Open Source
display_order: 2
---

[Add description]
```

**File 3: `marketplace-intelligence.md`**
```markdown
---
title: Marketplace Intelligence Dashboard
description: Real-time market analysis and competitor insights
featured: false
status: planned
tech:
  - Data visualization
  - Analytics
  - D3.js
  - PostgreSQL
display_order: 3
---

[Add description]
```

**Step 2: Add 3 Blog Posts**

Create in `/fullstackpm.tech/code/content/blog/`:

**File 1: `2026-02-14-why-pms-are-drowning.md`**
```markdown
---
title: "Why Product Managers Are Drowning (And How to Fix It)"
description: Analysis of PM operational burden from Lenny's Podcast
date: 2026-02-14
tags:
  - product-management
  - operations
  - podcast-analysis
---

[Article content about operational work burden]
```

**File 2: `2026-02-15-building-in-public.md`**
```markdown
---
title: "Building in Public: Portfolio + Tools + Brand"
description: Why I'm building my portfolio as a series of public projects
date: 2026-02-15
tags:
  - personal-brand
  - product-development
  - open-source
---

[Article about building journey]
```

**File 3: `2026-02-16-fullstack-pm-definition.md`**
```markdown
---
title: "What Makes a FullStack PM?"
description: The skills, mindset, and tools for modern product managers
date: 2026-02-16
tags:
  - product-management
  - career
---

[Article defining fullstack PM competencies]
```

**Acceptance Test:**
- ✅ All 6 files created in correct directories
- ✅ Frontmatter valid (YAML format)
- ✅ Files parse without errors
- ✅ http://localhost:8001/projects shows 4 projects
- ✅ http://localhost:8001/blog shows 5 blog posts
- ✅ Blog posts filterable by tag
- ✅ Pagination works (2+ pages of posts)

**What to Deliver:**
- 3 markdown files in `content/projects/`
- 3 markdown files in `content/blog/`

**My Review:**
- ✅ Files in correct format with frontmatter
- ✅ No frontmatter syntax errors
- ✅ Content shows in portfolio
- ✅ No broken links

**Then You:**
- Copy files to repo
- Refresh localhost
- Verify projects/blog pages show new content

---

### TASK 3: Deploy to Render [EST: 30 min]
**Status:** ⏳ Ready
**Owner:** You
**Depends on:** TASK 1 + TASK 2 (optional)

**Prerequisites:**
- GitHub account (with repo containing /fullstackpm.tech/code/)
- Render account (render.com - free tier OK)

**Steps:**

**Step 1: Push to GitHub**
```bash
cd /Users/sidc/Projects/claude_code/fullstackpm.tech/code/
git init
git add .
git commit -m "Initial portfolio site"
git remote add origin https://github.com/YOUR_USERNAME/fullstackpm-site.git
git push -u origin main
```

**Step 2: Create Procfile**

Create `/fullstackpm.tech/code/Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Step 3: Update requirements.txt**

Add if missing:
```
uvicorn[standard]==0.27.0
```

**Step 4: Deploy on Render**
1. Go to render.com
2. Sign up (free tier)
3. New → Web Service
4. Connect GitHub repo
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
7. Deploy

**Step 5: Set Custom Domain (Optional)**
- Buy domain on Namecheap/Google Domains
- In Render: Settings → Custom Domain → Add `fullstackpm.tech`
- Update DNS to point to Render

**Acceptance Test:**
- ✅ Deploy succeeds (no build errors)
- ✅ http://your-site.onrender.com/ loads (200 OK)
- ✅ All pages accessible
- ✅ Static files load correctly
- ✅ Dark mode toggle works
- ✅ Blog/projects show content
- ✅ RSS feed works

**Then You:**
- Share link: "Portfolio is live!"
- Test all features
- Share on Twitter/LinkedIn

---

## 🔄 FOLLOW-UP TASKS (After Deployment)

### TASK 4: PM Interview Coach - Wave 1 [EST: 8 hours, can parallelize]
**Status:** 📋 Ready to assign
**Owner:** Other LLM (3 tasks in parallel)
**Depends on:** Nothing (independent)

**What:**
Build first 3 components of PM Interview Coach (no dependencies)

**Subtask 4.1: Database Models** [EST: 2 hrs]
- Assign: `/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/BUILD_01_DATABASE_MODELS.md`
- Builder creates: `models.py` + database schema
- I review: Quality score + validation
- Output: Ready for tasks 4.2+

**Subtask 4.2: Base Templates** [EST: 1.5 hrs]
- Assign: `BUILD_02_BASE_TEMPLATES.md`
- Builder creates: Jinja2 templates for layout
- I review: Styling consistency + accessibility
- Output: Template framework ready

**Subtask 4.3: Question Loader Script** [EST: 2 hrs]
- Assign: `BUILD_03_QUESTION_LOADER.md`
- Builder creates: Script to load interview questions
- I review: Data format + validation
- Output: Questions in database, ready for UI

**Parallel Execution:**
- Start all 3 simultaneously
- Should be done in ~2-3 hours (vs 5.5 sequential)
- I review outputs in batches

**Then:**
- TASK 5: Wave 2 (3 more tasks, depends on Wave 1)
- TASK 6: Wave 3 (1 task, depends on Wave 2)

---

### TASK 5: PM Interview Coach - Wave 2 [EST: 8 hours]
**Status:** 📋 Ready after TASK 4
**Owner:** Other LLM (3 tasks in parallel)

**Subtask 5.1: AI Evaluator Service** [EST: 3 hrs]
**Subtask 5.2: Practice UI (Core Loop)** [EST: 3 hrs]
**Subtask 5.3: Landing + History Pages** [EST: 2 hrs]

---

### TASK 6: PM Interview Coach - Wave 3 [EST: 3 hours]
**Status:** 📋 Ready after TASK 5
**Owner:** Other LLM (1 task)

**Task 6.1: Progress Dashboard + HTMX Polish** [EST: 3 hrs]

---

## 📊 TASK TRACKING

### Current Week Status

| Task | Status | Owner | EST | Start | End |
|------|--------|-------|-----|-------|-----|
| 1: HTMX Endpoints | 📋 Ready | Other LLM | 45 min | Today | Today |
| 2: Add Content | ⏳ Ready | You | 1.5 hrs | Today | Today |
| 3: Deploy to Render | ⏳ Ready | You | 30 min | Today | Today |
| **Portfolio = 100%** | 🟢 Done | — | 2.5 hrs | — | — |

### Next Week Status

| Task | Status | Owner | EST | Start | End |
|------|--------|-------|-----|-------|-----|
| 4.1: DB Models | 📋 Ready | Other LLM | 2 hrs | Mon | Mon |
| 4.2: Base Templates | 📋 Ready | Other LLM | 1.5 hrs | Mon | Mon |
| 4.3: Question Loader | 📋 Ready | Other LLM | 2 hrs | Mon | Mon |
| (Review + fixes) | 🔄 In Progress | Me | 1 hr | Mon | Tue |
| 5.1: AI Evaluator | 📋 Ready | Other LLM | 3 hrs | Tue | Tue |
| 5.2: Practice UI | 📋 Ready | Other LLM | 3 hrs | Tue | Tue |
| 5.3: Landing Pages | 📋 Ready | Other LLM | 2 hrs | Tue | Tue |
| (Review + fixes) | 🔄 In Progress | Me | 1 hr | Tue | Wed |
| 6.1: Dashboard | 📋 Ready | Other LLM | 3 hrs | Wed | Wed |
| **Coach = 100%** | 🟢 Done | — | ~16 hrs | Mon | Wed |

---

## ✅ COMPLETION CHECKLIST

### Portfolio Site (Target: This Week)
- [ ] TASK 1: HTMX endpoints complete
- [ ] TASK 2: Content added (6 files)
- [ ] TASK 3: Deployed to Render
- [ ] All pages tested
- [ ] Share link on social media
- [ ] **Status: 100% LIVE**

### PM Interview Coach (Target: Next Week)
- [ ] TASK 4: Wave 1 complete (DB + templates + loader)
- [ ] TASK 5: Wave 2 complete (AI evaluator + UI + landing)
- [ ] TASK 6: Wave 3 complete (dashboard + polish)
- [ ] Beta testing with 10 users
- [ ] **Status: READY FOR BETA**

---

## 📞 HOW TO USE THIS

**To start a task:**
1. Find task in list above
2. Copy the "Detailed Instructions" section
3. Send to other LLM (or do manually if "Owner: You")
4. Wait for output
5. I review and validate
6. You integrate to repo

**To check progress:**
- Update checkboxes in "Completion Checklist"
- Update status badges
- Comment on blockers

**Format for communication:**
```
Task: TASK 1: Complete HTMX Interactions
Owner: Other LLM
Status: Ready to start
Instructions: [Copy from "Detailed Instructions" section]
```

---

**Last Updated:** February 13, 2026
**Next Review:** After TASK 1 complete
**Questions?** See PROJECT_DASHBOARD.md for context

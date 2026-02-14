# Code Puppy Integration Guide

**Your Builder:** Code Puppy (specialized agent for this workflow)
**Your Reviewer:** Claude Code (me, validation + planning)
**Your Integrator:** You (deployment + GitHub + content)

---

## 🤖 How Code Puppy Works With Us

### The Workflow

```
Me (Claude Code)
├─ Create detailed BUILD_XX.md file
├─ Include: scope, architecture, acceptance tests
└─ Hand to Code Puppy

        ↓

Code Puppy
├─ Read BUILD_XX.md
├─ Implement exactly as specified
├─ Generate working code
├─ Return complete implementation
└─ I validate it

        ↓

You
├─ Copy code to /code/app/
├─ Create GitHub repo for project
├─ Test locally at /tools/{slug}
├─ Write blog post about build
└─ Deploy + share
```

### What Code Puppy Should Do

Code Puppy is an expert at:
- ✅ Reading detailed specifications (BUILD files)
- ✅ Generating production-quality code
- ✅ Following architecture patterns
- ✅ Implementing acceptance tests
- ✅ Creating self-contained modules

Code Puppy is NOT responsible for:
- ❌ Deciding architecture (I do that)
- ❌ Reviewing other code (I do that)
- ❌ Deploying to production (you do that)
- ❌ Planning projects (I do that)

---

## 📋 How to Hand Off Tasks to Code Puppy

### Message Template

```
Project: [Project Name]
Task: [Task Number/Name]
Priority: [High/Medium/Low]

Here are the detailed instructions:

[Copy the entire BUILD_XX.md file content here]

Please implement exactly as specified.
Return all files needed.

When you're done, confirm:
✅ All acceptance tests pass
✅ Code follows the patterns shown
✅ No breaking changes to existing code
```

### Example

```
Project: PM Interview Coach
Task: BUILD_02 - Base Templates
Priority: High

Here are the detailed instructions:

[Paste BUILD_02_BASE_TEMPLATES.md content]

Please create:
- templates/base.html
- templates/coach/layout.html
- templates/coach/practice.html
- CSS for coach UI

Confirm acceptance tests pass when done.
```

---

## 🏗️ Project Structure For Live Endpoints

### How Projects Live on the Site

Each project gets its own section:

```
fullstackpm.tech/
├─ code/app/
│  ├─ main.py (router registration)
│  ├─ routers/
│  │  ├─ pages.py (home, about, etc)
│  │  ├─ projects.py (project gallery)
│  │  ├─ blog.py (blog posts)
│  │  └─ tools/
│  │     ├─ coach.py (PM Interview Coach endpoints)
│  │     ├─ toolkit.py (PM Toolkit endpoints)
│  │     ├─ analyzer.py (A/B Test Analyzer endpoints)
│  │     ├─ decision.py (Decision System endpoints)
│  │     ├─ marketplace.py (Marketplace endpoints)
│  │     ├─ prompt_eval.py (Prompt Evaluator endpoints)
│  │     └─ bootcamp.py (Bootcamp endpoints)
│  │
│  ├─ services/
│  │  ├─ content.py (markdown parsing)
│  │  ├─ coach_service.py (coach logic)
│  │  ├─ toolkit_service.py (toolkit logic)
│  │  └─ ...
│  │
│  └─ templates/
│     ├─ projects/
│     │  ├─ detail.html (project info page)
│     │  └─ gallery.html (all projects)
│     └─ tools/
│        ├─ coach/
│        │  ├─ layout.html
│        │  ├─ practice.html
│        │  ├─ history.html
│        │  └─ dashboard.html
│        ├─ toolkit/
│        │  ├─ layout.html
│        │  ├─ main.html
│        │  └─ components/
│        ├─ analyzer/
│        │  └─ ...
│        └─ ...
│
├─ content/
│  ├─ blog/
│  │  ├─ how-i-built-pm-coach.md
│  │  ├─ pm-coach-lessons-learned.md
│  │  ├─ how-i-built-pm-toolkit.md
│  │  └─ ...
│  └─ projects/
│     ├─ pm-interview-coach.md
│     ├─ pm-toolkit.md
│     └─ ...
│
└─ GitHub/
   ├─ fullstackpm.tech (main site + portfolio)
   ├─ pm-interview-coach (standalone project repo)
   ├─ pm-toolkit (standalone project repo)
   ├─ ab-test-analyzer (standalone project repo)
   └─ ...
```

### Router Pattern

**Each project gets its own router file:**

```python
# app/routers/tools/coach.py

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from app.services.coach_service import CoachService

router = APIRouter(prefix="/tools/coach", tags=["coach"])

@router.get("/", response_class=HTMLResponse)
async def coach_home(request: Request):
    """Homepage for PM Interview Coach"""
    return templates.TemplateResponse(
        "tools/coach/layout.html",
        {"request": request}
    )

@router.get("/practice", response_class=HTMLResponse)
async def practice(request: Request):
    """Interactive practice interface"""
    # Implementation
    ...

@router.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    """User's practice history"""
    # Implementation
    ...

@router.post("/api/evaluate")
async def evaluate(answer: str, question_id: int):
    """API: Evaluate user's answer"""
    # Implementation
    ...
```

**Register in main.py:**

```python
# app/main.py

from app.routers.tools import coach, toolkit, analyzer, ...

app.include_router(coach.router)
app.include_router(toolkit.router)
app.include_router(analyzer.router)
# etc.
```

---

## 🌐 URL Structure

### Live Project Endpoints

```
/tools/coach                    Home page for PM Interview Coach
/tools/coach/practice           Interactive practice section
/tools/coach/history            User practice history
/tools/coach/api/...            API endpoints

/tools/toolkit                  PM Toolkit home
/tools/toolkit/...              Toolkit features

/tools/analyzer                 A/B Test Analyzer home
/tools/analyzer/...             Analyzer features

/tools/decision                 Decision System home
/tools/decision/...             Decision features

/tools/marketplace              Marketplace Dashboard home
/tools/marketplace/...          Dashboard features

/tools/prompt-eval              LLM Prompt Evaluator home
/tools/prompt-eval/...          Evaluator features

/tools/bootcamp                 AI Bootcamp info + case study
/tools/bootcamp/...             Bootcamp content
```

### Project Pages (Info)

```
/projects                       Gallery of all projects
/projects/pm-interview-coach   "About PM Interview Coach" page
  ├─ Description + features
  ├─ "Try It Now" → /tools/coach
  ├─ "View Source" → GitHub repo
  └─ Blog posts about it

/projects/pm-toolkit           "About PM Toolkit" page
  └─ ...
```

---

## 📝 Content Integration

### Project Data File

Each project needs metadata:

```yaml
# content/projects/pm-interview-coach.md
---
title: PM Interview Coach
slug: pm-interview-coach
description: AI-powered interview practice for product managers
featured: true
status: live
tech:
  - Python
  - FastAPI
  - Claude API
  - SQLite
display_order: 1
github_repo: https://github.com/YOUR_USERNAME/pm-interview-coach
live_endpoint: /tools/coach
blog_posts:
  - how-i-built-pm-coach
  - pm-coach-lessons-learned
use_cases:
  - PM interview preparation
  - Skill assessment
  - Continuous learning
---

## PM Interview Coach

AI-powered practice platform for product management interviews.

Users can:
- Practice with realistic PM interview questions
- Get AI feedback on their answers
- Track improvement over time
- Review past practice sessions

**[Try it now](/tools/coach)** | **[View source](https://github.com/...)**
```

---

## 🔄 Code Puppy Build Cycle

### Step-by-Step For Each Project

**Step 1: I Create BUILD Files** (Me - Claude Code)
- 8 BUILD files for PM Interview Coach (example)
- Each file has detailed specs + acceptance tests
- Files saved in `strategy/build_tasks/pm_interview_coach/`

**Step 2: You Send Task to Code Puppy** (You)
- Copy TASK 1 instructions
- Send to Code Puppy
- Ask for specific files back

**Step 3: Code Puppy Builds** (Code Puppy)
- Reads BUILD file
- Implements code
- Tests against acceptance criteria
- Returns all files

**Step 4: I Review** (Me - Claude Code)
- Validate against spec
- Score quality (90+ = approved)
- Flag issues if any
- Return to Code Puppy for fixes (if needed)

**Step 5: You Integrate** (You)
- Copy files to repo
- Test locally at http://localhost:8001
- Create blog post about the build
- Push to GitHub
- Deploy

**Step 6: You Content** (You)
- Write blog post: "How I Built [Project]"
- Write blog post: "Lessons Learned"
- Create social posts
- Share project link

---

## 📋 Checklist: Handing Off to Code Puppy

### Before You Send Task

- [ ] BUILD file is complete (1000+ lines)
- [ ] Acceptance tests are clear
- [ ] Scope is well-defined
- [ ] No ambiguity in instructions
- [ ] All dependencies are listed
- [ ] Code examples provided (if needed)

### What Code Puppy Returns

- [ ] All required files created
- [ ] No unused imports
- [ ] Type hints throughout
- [ ] Error handling implemented
- [ ] Acceptance tests pass
- [ ] No breaking changes
- [ ] Follows project patterns

### What You Check After

- [ ] Files in correct location
- [ ] No merge conflicts
- [ ] Tests pass locally
- [ ] Feature works as expected
- [ ] Code quality is good
- [ ] Documentation updated

---

## 🚀 First Project: PM Interview Coach

### Task Breakdown (What Code Puppy Builds)

| Task | Time | What | Status |
|------|------|------|--------|
| BUILD_01 | 2 hrs | Database models + migrations | Ready |
| BUILD_02 | 1.5 hrs | Base templates + layout | Ready |
| BUILD_03 | 2 hrs | Question loader script | Ready |
| BUILD_04 | 3 hrs | AI evaluator service | Ready |
| BUILD_05 | 3 hrs | Practice UI (core loop) | Ready |
| BUILD_06 | 2 hrs | Landing + history pages | Ready |
| BUILD_07 | 2 hrs | Progress dashboard | Ready |
| BUILD_08 | 1 hr | HTMX interactions | Ready |

**Total:** ~16 hours (or 4-6 with parallelization)

### Execution Plan

**Week 1 (Monday):**
- Send BUILD_01, 02, 03 to Code Puppy simultaneously
- I review while they build
- By Wednesday: All 3 tasks complete + integrated

**Week 1 (Wednesday):**
- Send BUILD_04, 05, 06 (depend on previous)
- By Friday: All 3 tasks complete + integrated

**Week 2 (Monday):**
- Send BUILD_07, 08
- By Tuesday: All complete
- Wednesday: You test + write blog posts
- Thursday: Deploy + launch

**Result:** PM Coach live in ~10 days

---

## 📊 Tracking Code Puppy Progress

### Progress File (You Update)

Create `CODE_PUPPY_PROGRESS.md`:

```markdown
# Code Puppy - PM Interview Coach Build Progress

## Wave 1: Foundation
- [ ] BUILD_01 (Database Models) - Assigned: Mon 2/17 - Due: Wed 2/19
  - [ ] Status: Code Puppy building
  - [ ] Review score: Pending
  - [ ] Integrated: No

- [ ] BUILD_02 (Templates) - Assigned: Mon 2/17 - Due: Wed 2/19
  - [ ] Status: Code Puppy building
  - [ ] Review score: Pending
  - [ ] Integrated: No

## Wave 2: Core Features
- [ ] BUILD_03 (Question Loader)
- [ ] BUILD_04 (AI Evaluator)
- [ ] BUILD_05 (Practice UI)

## Wave 3: Polish
- [ ] BUILD_06 (Landing Pages)
- [ ] BUILD_07 (Dashboard)
- [ ] BUILD_08 (HTMX)

## Overall
- Progress: 0/8 tasks
- ETA: Feb 27 (Coach live)
```

---

## 💡 Tips For Working With Code Puppy

### DO

✅ **Be specific** - "Add a button" vs "Add blue button (hex #0000FF) with hover state"
✅ **Show examples** - "See this similar component for pattern"
✅ **Test acceptance** - "Verify all 5 acceptance tests pass"
✅ **Provide context** - "This connects to the database from Task 1"
✅ **Set expectations** - "This should take ~2 hours"

### DON'T

❌ **Be vague** - "Make it look good"
❌ **Change scope mid-task** - Stick to BUILD file
❌ **Assume patterns** - Explicitly state what you want
❌ **Rush** - Take time to write good BUILD files
❌ **Ignore failures** - If test fails, ask for fixes, don't work around

### If Code Puppy Has Issues

1. **Ask for clarification** - "What part is unclear?"
2. **Provide feedback** - "This part doesn't match the spec"
3. **Request revisions** - "Fix issues X, Y, Z and return"
4. **Escalate to me** - "Review this - something's wrong"

---

## 🎯 Success Criteria

### Code Puppy Succeeded If

✅ Code works (no runtime errors)
✅ Acceptance tests pass
✅ Code quality is 90+/100
✅ Follows project patterns
✅ No breaking changes
✅ Ready to deploy immediately

### You Can Deploy If

✅ Tests pass locally
✅ Feature works end-to-end
✅ No security issues
✅ Performance is acceptable
✅ Documentation updated

---

## 📞 Workflow Questions

**Q: Can Code Puppy build multiple tasks in parallel?**
A: Yes! Send 3 non-dependent tasks simultaneously if you want faster execution.

**Q: What if Code Puppy's code has issues?**
A: Ask for fixes (not a big deal), I review again, iterate until good.

**Q: Can Code Puppy write the blog posts?**
A: Technically yes, but better if you write them (authentic voice).

**Q: How long for feedback loop?**
A: Plan on 4-6 hours per task (Code Puppy builds + my review).

**Q: What if something breaks?**
A: Easy to revert. I validate before integration, so major issues caught early.

---

## ✅ Ready to Send First Task?

When you're ready to start PM Interview Coach:

1. Message Code Puppy:
```
Project: PM Interview Coach
Task: BUILD_01_DATABASE_MODELS.md
Location: /fullstackpm.tech/strategy/build_tasks/pm_interview_coach/

[Copy full BUILD file]
```

2. I'll review Code Puppy's code
3. You integrate + test
4. Move to next task

---

**Status:** ✅ Ready to work with Code Puppy
**Next:** Start first task when ready

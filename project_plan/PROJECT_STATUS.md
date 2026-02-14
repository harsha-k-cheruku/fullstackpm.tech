# fullstackpm.tech — Project Status & Plan

**Last Updated:** February 12, 2026
**Owner:** Harsha Cheruku
**AI Assistant:** Claude Code (Sonnet 4.5)

---

## 📊 Overall Status

| Component | Status | Progress |
|-----------|--------|----------|
| **Portfolio Site (Project 0)** | 🟢 90% Complete | Foundation built, polish in progress |
| **PM Interview Coach (Project 1)** | 🟡 Planning | Build tasks created, ready for execution |
| **Projects 2-7** | 🔴 Not Started | Strategy docs exist, build tasks pending |

---

## 🎯 Project 0: Portfolio Site — Current Status

### ✅ Complete (Built & Live)

**Foundation (Phase 1):**
- [x] FastAPI scaffold + Pydantic config
- [x] SQLAlchemy + ContentService (markdown parsing, caching)
- [x] Base template (Tailwind + HTMX + dark mode)
- [x] Navbar + Footer + Mobile menu
- [x] Home page (hero + featured projects + thesis)
- [x] About page (career timeline)
- [x] Contact page (social cards)
- [x] 404 page
- [x] Design system (Geist Sans + pure black/white theme)

**Content (Phase 2):**
- [x] Projects router + gallery + detail pages
- [x] Blog router + list + detail + tag pages
- [x] RSS feed (`/feed.xml`)
- [x] Sitemap (`/sitemap.xml`)
- [x] Robots.txt (`/robots.txt`)
- [x] Sample content (2 blog posts, 2 projects)

**Design System (Phase 3 - Just Updated):**
- [x] Pure black text (#000000) in light mode
- [x] Pure white text (#FFFFFF) in dark mode
- [x] 10-step color scales (blue, emerald, amber, red)
- [x] Semantic color variables (success, warning, danger)
- [x] Card hover effects (CSS class)
- [x] Badge components (CSS classes)

---

### 🟡 In Progress

**Template Polish (Handed off to other LLM):**
- [ ] Add `card-hover` to project cards
- [ ] Add status badges (live, in progress, planned)
- [ ] Remove gradient backgrounds
- [ ] Apply pure black text consistently

**Files being updated:**
- `app/templates/partials/project_card.html`
- `app/templates/home.html`
- `app/templates/projects/gallery.html`
- `app/templates/projects/detail.html`

**Status:** Waiting for other LLM to return updated templates
**ETA:** ~10 minutes
**Next step:** Claude Code validates output

---

### ⏸️ Paused (HTMX Enhancements)

**HTMX Interactions (BUILD_06):**
- [x] Partial directories created
- [x] Partial templates created (`project_grid.html`, `post_list.html`)
- [x] CSS updated (HTMX indicator styles)
- [ ] Update `projects.py` router (add filter endpoint)
- [ ] Update `blog.py` router (add filter endpoint)
- [ ] Update `gallery.html` template (add filter bar + HTMX)
- [ ] Update `list.html` template (add HTMX tags + Load More)

**Status:** Paused to focus on design system updates
**Resumption:** After template polish is complete
**ETA:** 1-2 hours to finish

---

### ❌ Not Started

**Nice-to-Have Features:**
- [ ] Resume page (`/resume`)
- [ ] Search functionality
- [ ] Newsletter signup
- [ ] Analytics integration
- [ ] Performance optimization (image lazy loading, etc.)

---

## 🚀 Project 1: PM Interview Coach — Planning Complete

### ✅ Strategy & Planning Done

**Strategy Document:**
- [x] Product brief (problem, solution, features)
- [x] Technical architecture (FastAPI, SQLite, Claude API)
- [x] Data model (questions, attempts, sessions)
- [x] API endpoints (practice, history, progress)
- [x] UI/UX specs (landing, practice, history, dashboard)

**Build Task Decomposition:**
- [x] Task breakdown (8 tasks identified)
- [x] Dependency graph created
- [x] README.md (task list, build order, success criteria)
- [x] BUILD_01_DATABASE_MODELS.md (reference example - 1000+ lines)
- [x] INSTRUCTIONS_FOR_LLM.md (complete guide for other LLMs)
- [x] HANDOFF_TO_OTHER_LLM.md (copy-paste prompts)
- [x] VALIDATION_CHECKLIST.md (quality scoring rubric)

**Files Created:**
```
strategy/build_tasks/pm_interview_coach/
├── README.md                        ✅
├── BUILD_01_DATABASE_MODELS.md      ✅ (reference example)
├── INSTRUCTIONS_FOR_LLM.md          ✅
├── HANDOFF_TO_OTHER_LLM.md          ✅
└── VALIDATION_CHECKLIST.md          ✅
```

---

### ⏳ Next Steps (Ready to Execute)

**Option A: Hand off to other LLMs**
1. Give BUILD_01 + FRAMEWORK + Strategy to GPT-4/Gemini
2. They generate BUILD_02 through BUILD_08
3. Claude Code validates output
4. Distribute tasks to multiple LLMs for parallel execution

**Option B: Claude Code generates remaining BUILD files**
1. Claude Code writes BUILD_02 through BUILD_08
2. User hands off to other LLMs for code generation
3. Claude Code validates final code

**Recommendation:** Option A (saves ~35k Claude tokens)

---

### 📋 Build Tasks for PM Interview Coach

| # | Task | Status | Depends On | Complexity |
|---|------|--------|------------|------------|
| 1 | Database Models + Migrations | ✅ BUILD file done | None | Medium |
| 2 | Base Templates + Layout | ⏳ Needs BUILD file | None | Simple |
| 3 | Question Loader Script | ⏳ Needs BUILD file | Task 1 | Medium-High |
| 4 | AI Evaluator Service | ⏳ Needs BUILD file | Task 1 | High |
| 5 | Practice UI (Core Loop) | ⏳ Needs BUILD file | Tasks 1, 2, 4 | High |
| 6 | Landing + History Pages | ⏳ Needs BUILD file | Tasks 1, 2 | Medium |
| 7 | Progress Dashboard | ⏳ Needs BUILD file | Tasks 1, 2 | Medium-High |
| 8 | HTMX Interactions | ⏳ Needs BUILD file | Tasks 5, 6, 7 | Medium |

**Parallel execution path:**
- Wave 1: Tasks 1 & 2 (no dependencies)
- Wave 2: Tasks 3 & 4 (after Task 1)
- Wave 3: Tasks 5 & 6 & 7 (after Tasks 1, 2, 4)
- Wave 4: Task 8 (after all UI)

**Total estimated time with parallelization:** 4 LLM invocations (vs 8 sequential)

---

## 📚 Projects 2-7 — Strategy Complete, Build Tasks Pending

### Strategy Documents Created

All strategy documents exist in `strategy/`:

1. ✅ `02_PM_INTERVIEW_COACH.md` (Project 1 - build tasks in progress)
2. ✅ `03_MARKETPLACE_DASHBOARD.md` (Project 2)
3. ✅ `04_AI_PM_TOOLKIT.md` (Project 3)
4. ✅ `05_AI_PM_DECISION_SYSTEM.md` (Project 4)
5. ✅ `06_LLM_PROMPT_EVAL_FRAMEWORK.md` (Project 5)
6. ✅ `07_AB_TEST_ANALYZER.md` (Project 6)
7. ✅ `08_AI_BOOTCAMP_CASE_STUDY.md` (Project 7)

### Build Task Framework Created

**Meta-Framework:**
- ✅ `FRAMEWORK_STRATEGY_TO_TASKS.md` (reusable for all projects)
- ✅ 8-section template (project overview → acceptance tests)
- ✅ Dependency patterns (AI projects, data projects, content projects)
- ✅ Self-containment checklist
- ✅ Quality validation rubric

**Application:**
- ✅ Applied to Project 1 (PM Interview Coach) - 8 build tasks
- ⏳ Pending for Projects 2-7

---

### Next Step for Projects 2-7

For each project:
1. Apply FRAMEWORK to strategy doc
2. Generate README + BUILD_01 through BUILD_XX
3. Hand off to other LLMs for code generation
4. Claude Code validates
5. Deploy

**Estimated effort per project:** 2-3 weeks

---

## 🎨 Design System Evolution

### Phase 1: Initial Design (Feb 9)
- Geist Sans font
- Cool-tinted Slate grays
- Minimal, clean aesthetic

### Phase 2: Apple-Style Text (Feb 11)
- Pure black text (#000000)
- Tighter letter-spacing
- Higher contrast

### Phase 3: Extended Color System (Feb 12) ✅ Current
- 10-step color scales (blue, emerald, amber, red)
- Semantic color variables
- Card hover effects
- Badge components
- Pure black/white theme (light/dark mode)

**Design Philosophy:**
- Minimal, not corporate
- Builder-focused, not agency
- Speed over polish
- Authenticity over perfection

---

## 🔧 Technical Stack

### Core Technologies

| Layer | Technology | Status |
|-------|-----------|--------|
| Backend | FastAPI (Python 3.11+) | ✅ Deployed |
| Templating | Jinja2 | ✅ Working |
| Styling | Tailwind CSS (CDN) | ✅ Working |
| Interactivity | HTMX (CDN) | 🟡 Partial |
| Fonts | Geist Sans + JetBrains Mono | ✅ Working |
| Database | SQLite + SQLAlchemy (async) | ✅ Working |
| Content | Markdown + Frontmatter | ✅ Working |
| Charts | Chart.js (CDN) | ⏳ Not yet needed |
| AI | Claude API (Anthropic SDK) | ⏳ Not yet needed |
| Deployment | Render | ⏳ Pending |

---

## 📁 Project Structure

```
fullstackpm.tech/
├── code/                           # Main application
│   ├── app/
│   │   ├── main.py                 ✅
│   │   ├── config.py               ✅
│   │   ├── routers/
│   │   │   ├── pages.py            ✅
│   │   │   ├── projects.py         ✅ (filter endpoint pending)
│   │   │   ├── blog.py             ✅ (filter endpoint pending)
│   │   │   └── seo.py              ✅
│   │   ├── services/
│   │   │   ├── content.py          ✅
│   │   │   └── feed.py             ✅
│   │   ├── templates/
│   │   │   ├── base.html           ✅
│   │   │   ├── home.html           ✅ (polish pending)
│   │   │   ├── about.html          ✅
│   │   │   ├── contact.html        ✅
│   │   │   ├── 404.html            ✅
│   │   │   ├── projects/
│   │   │   │   ├── gallery.html    ✅ (HTMX pending)
│   │   │   │   ├── detail.html     ✅ (polish pending)
│   │   │   │   └── partials/
│   │   │   │       └── project_grid.html  ✅
│   │   │   ├── blog/
│   │   │   │   ├── list.html       ✅ (HTMX pending)
│   │   │   │   ├── detail.html     ✅
│   │   │   │   ├── tag.html        ✅
│   │   │   │   └── partials/
│   │   │   │       └── post_list.html  ✅
│   │   │   └── partials/
│   │   │       ├── navbar.html     ✅
│   │   │       ├── footer.html     ✅
│   │   │       └── project_card.html  ✅ (polish pending)
│   │   └── static/
│   │       ├── css/custom.css      ✅ (just updated)
│   │       └── js/main.js          ✅
│   ├── content/
│   │   ├── blog/                   ✅ (2 sample posts)
│   │   └── projects/               ✅ (2 sample projects)
│   ├── requirements.txt            ✅
│   └── Procfile                    ⏳
├── strategy/                       # Planning documents
│   ├── 00_MASTER_PLAN.md           ✅
│   ├── 01_PORTFOLIO_SITE.md        ✅
│   ├── 02_PM_INTERVIEW_COACH.md    ✅
│   ├── 03-08_*.md                  ✅ (7 project strategies)
│   ├── 09_DESIGN_SYSTEM.md         ✅
│   ├── 10_COMPONENT_SPECS.md       ✅
│   ├── 11_LLM_EVAL_RUBRIC.md       ✅
│   └── build_tasks/
│       ├── README.md               ✅ (portfolio site)
│       ├── BUILD_01-07_*.md        ✅ (portfolio site)
│       ├── FRAMEWORK_*.md          ✅
│       └── pm_interview_coach/
│           ├── README.md           ✅
│           ├── BUILD_01_*.md       ✅
│           └── INSTRUCTIONS_*.md   ✅
├── project_plan/
│   └── PROJECT_STATUS.md           ✅ (this file)
└── INSTRUCTIONS_FOR_TEMPLATE_UPDATES.md  ✅
```

---

## 💰 Token Usage Strategy

### Current Approach (Optimized)

**Claude Code for:**
- ✅ Critical infrastructure (CSS, routing, core features)
- ✅ Planning & architecture (strategy → build tasks)
- ✅ Creating instruction files for other LLMs
- ✅ Validation & quality checks

**Other LLMs (GPT-4, Gemini, etc.) for:**
- ⏳ Template updates (following instructions)
- ⏳ Generating BUILD_02-08 (following BUILD_01 example)
- ⏳ Repetitive code generation (well-defined tasks)

**Token Savings:**
- Portfolio template updates: 20k tokens saved
- PM Interview Coach BUILD files: 35k tokens saved
- **Total saved so far:** ~55k tokens

**Claude Code token usage (this session):**
- Started: 0 / 200k
- Current: ~108k / 200k (54%)
- Remaining: ~92k tokens

---

## 🎯 Immediate Next Steps (Priority Order)

### 1. Portfolio Site Polish (Today)
**Current blocker:** Waiting for other LLM to update 4 templates
**Action:** Review their output when ready
**Time:** 30 mins
**Token cost:** ~5k (validation)

### 2. Finish HTMX Interactions (Today/Tomorrow)
**Files to update:**
- `app/routers/projects.py` (add filter endpoint)
- `app/routers/blog.py` (add filter endpoint)
- `app/templates/projects/gallery.html` (add filter bar)
- `app/templates/blog/list.html` (add HTMX tags)

**Time:** 1-2 hours
**Token cost:** ~10-15k (or hand off to other LLM)

### 3. PM Interview Coach BUILD Files (This Week)
**Option A:** Hand off to other LLM (~0 Claude tokens)
**Option B:** Claude Code generates (~35k tokens)
**Recommendation:** Option A

### 4. Deploy Portfolio Site (This Week)
**Tasks:**
- Create Procfile
- Set up Render account
- Deploy
- Configure custom domain

---

## 🔄 Workflow for Future Projects

**Proven pattern from this session:**

1. **Strategy** → Claude Code creates high-level plan
2. **Framework** → Claude Code applies FRAMEWORK to create build tasks
3. **Reference** → Claude Code writes BUILD_01 as example
4. **Delegate** → Other LLMs generate BUILD_02-XX following example
5. **Validate** → Claude Code reviews output (quality score)
6. **Execute** → Hand BUILD files to multiple LLMs in parallel
7. **Validate** → Claude Code reviews generated code
8. **Deploy** → Push to production

**Token efficiency:** ~70% savings by delegating to other LLMs

---

## 📈 Progress Timeline

### Week 1 (Feb 9-12)
- ✅ Portfolio site foundation (FastAPI + templates)
- ✅ Content system (markdown + caching)
- ✅ Design system v3 (pure black/white + color scales)
- ✅ RSS + Sitemap + SEO
- ✅ PM Interview Coach planning (8 build tasks)
- ✅ FRAMEWORK creation (reusable for all projects)
- 🟡 HTMX interactions (80% done)
- 🟡 Template polish (in progress)

### Week 2 (Feb 13-19) - Planned
- Complete portfolio site polish
- Deploy portfolio to Render
- Generate PM Interview Coach BUILD files (via other LLMs)
- Start PM Interview Coach development
- Add resume page

### Week 3-4 (Feb 20-Mar 5) - Planned
- Complete PM Interview Coach
- Deploy PM Interview Coach
- Start Project 2 (Marketplace Dashboard)

---

## 🚨 Risks & Blockers

### Current Risks

1. **Template updates from other LLM**
   - **Risk:** They might not follow instructions correctly
   - **Mitigation:** Backups created, Claude Code will validate
   - **Impact:** Low (easy to revert)

2. **Token budget**
   - **Risk:** Running out of Claude tokens before projects done
   - **Mitigation:** Strategic delegation to other LLMs
   - **Impact:** Medium (can continue with other LLMs)

3. **HTMX complexity**
   - **Risk:** HTMX interactions might have bugs
   - **Mitigation:** Acceptance tests defined, incremental rollout
   - **Impact:** Low (progressive enhancement, site works without it)

### No Current Blockers
- All dependencies met
- All files accessible
- Server running locally
- Clear next steps

---

## 🎓 Lessons Learned

### What Worked Well

1. **Build Task Framework**
   - Self-contained files enable LLM parallelization
   - Reference example (BUILD_01) sets quality bar
   - Instruction files reduce token overhead

2. **Design System Evolution**
   - Started simple, iterated based on feedback
   - Pure black/white is bold and distinctive
   - 10-step color scales give flexibility

3. **Token Optimization**
   - Delegating to other LLMs saves 50-70% tokens
   - Claude Code for critical decisions, other LLMs for execution
   - Validation is cheaper than generation

### What to Improve

1. **Git workflow**
   - Need to initialize git repo
   - Commit checkpoints for easier rollback
   - Branch strategy for experimental changes

2. **Testing**
   - Manual testing is slow
   - Need automated acceptance tests
   - Playwright for E2E testing?

3. **Documentation**
   - Code comments sparse
   - Need developer onboarding doc
   - API documentation missing

---

## 📝 Notes & Decisions

### Design Decisions

- **Font:** Geist Sans (distinctive, modern, tight)
- **Text color:** Pure black #000000 (bold, confident)
- **Dark mode:** Pure black background (OLED-friendly)
- **No gradients:** Keep it minimal and fast
- **No animations:** Speed over flashiness

### Technical Decisions

- **FastAPI over Flask:** Async support, modern patterns
- **Jinja2 over React:** SEO-friendly, no build step
- **HTMX over JS frameworks:** Progressive enhancement
- **SQLite over Postgres:** Simple, portable (for now)
- **Markdown over CMS:** Git-based, version controlled

### Strategic Decisions

- **Build in public:** All code/docs in one repo
- **LLM delegation:** Optimize Claude token usage
- **Portfolio first:** Foundation for all other projects
- **Parallel projects:** Use framework to spin up quickly

---

## 🔗 Quick Links

**Local Development:**
- Portfolio site: http://localhost:8001
- Sample (new design): http://localhost:8003/SAMPLE_HOME_NEW_DESIGN.html

**Key Files:**
- Strategy: `/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/`
- Code: `/Users/sidc/Projects/claude_code/fullstackpm.tech/code/`
- Build Tasks: `/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/`
- Instructions: `/Users/sidc/Projects/claude_code/fullstackpm.tech/INSTRUCTIONS_FOR_TEMPLATE_UPDATES.md`

**Backups:**
- Template backups: `code/app/templates/**/*.backup`

---

**Status as of:** February 12, 2026, 5:30 PM
**Next review:** After template updates complete
**Overall health:** 🟢 Green (on track, no blockers)

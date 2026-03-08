# Projects Status & Extraction Timeline

This document tracks all projects across three tiers: Integrated, In Development, and Planned for Extraction.

---

## Tier 1: Integrated (Live on fullstackpm.tech)

Projects tightly coupled to the portfolio site. Deployed with main app.

### 1. PM Interview Coach
**Status:** 🟢 Live
**URL:** /tools/interview-coach
**Tech:** FastAPI + OpenAI ChatGPT + HTMX + SQLite
**Features:**
- 4 practice categories (Product Design, Strategy, Execution, Analytical)
- Real-time AI evaluation using ChatGPT
- Score cards (overall, framework, structure, completeness)
- Practice session tracking

**Metrics:**
- ~500 evaluations/month (estimate)
- OpenAI cost: ~$3-5/month
- No storage cost (SQLite in app)

**When to Extract:** 2026 Q2
- Criteria: 5K+ monthly users, monetization demand
- Action: Move to `fullstackpm-interview-coach` npm package

---

### 2. Marketplace Analytics Dashboard
**Status:** 🟢 Live
**URL:** /tools/marketplace-analytics
**Tech:** FastAPI + Pandas + Chart.js + HTMX
**Features:**
- Overview cards (revenue, listings, rating, satisfaction)
- Revenue trends chart (12-week history)
- Category performance table (sortable, filterable)
- Cohort analysis by signup month
- Real-time filtering via HTMX
- CSV export functionality

**Metrics:**
- 0 users (internal demo, no analytics tracked yet)
- Chart.js: Free (CDN)
- No OpenAI cost

**When to Extract:** 2026 Q3
- Criteria: Integrated with real marketplace data, 10K+ sellers using
- Action: Move to `fullstackpm-marketplace-analytics` as reusable template

---

### 3. SDE Prep Tool (9-Week Intensive)
**Status:** 🟢 Live
**URL:** /tools/sde-prep/intensive-8-week
**Tech:** FastAPI + Jinja2 + localStorage + JSON curriculum data
**Features:**
- 9-week intensive job search prep curriculum (208 tasks)
- Plan page with expandable weeks/days/tasks
- Progress tracker using browser localStorage
- Personal reflection notes page
- Task types: research, writing, practice, networking, application

**Key Files:**
- Curriculum data: `code/app/static/data/curriculum-8-week-intensive.json`
- Plan page: `/tools/sde-prep/intensive-8-week`
- Tracker: `/tools/sde-prep/intensive-tracker`
- Notes: `/tools/sde-prep/intensive-notes`

**Metrics:**
- Storage: localStorage only (no server persistence)
- No API cost

**When to Extract:** Never (personal tool, part of portfolio)

---

### 4. Blog + Comments System
**Status:** 🟢 Live
**URL:** /blog
**Tech:** Markdown + SQLite (comments)
**Features:**
- 13 published posts (AI-Native PM series, D/P Framework, build logs)
- Blog post comments (database-backed)
- Tag filtering
- RSS feed
- SEO (sitemap, robots.txt)
- Future-date scheduling (posts with future dates hidden until publish date)

**Content Series:**
- AI-Native PM Series: 5 posts (What Is an AI-Native PM, The D/P Framework, Life in D/P, When AI Masters D, More P = More Burnout)
- How to Execute P Work: 2 parts (Diagnostic: Mar 6, Tactical: Mar 8)

**Metrics:**
- ~50 monthly blog visitors (estimate)
- Comments: ~5-10 per month
- Storage: <1MB

**When to Extract:** Never (part of core portfolio)

---

### 5. Newsletter Signup
**Status:** 🟢 Live (shipped Mar 1, 2026 | debugged Mar 7-8)
**Locations:** Homepage ("Stay in the Loop" section) + Blog post detail pages
**Tech:** FastAPI + HTMX + Google Sheets backend
**Features:**
- Email + name collection via HTMX form
- Google Sheets storage (persistent across Render redeploys)
- Duplicate detection (friendly "already on the list" message)
- Soft unsubscribe (status column, keeps record)
- CSV export endpoint (/api/newsletter/export)
- Styled success/error responses (HTMX swap + full-page fallback)
- Fixed: Special character URL encoding in unsubscribe links (emails with +, @, etc.)

**Subscribers:** 2+ (as of Mar 8, 2026)
**Status Health:** ✅ Fully operational, tested with special characters

**When to Extract:** Never (core site feature)

---

### 6. Content Strategy Pipeline
**Status:** 🟢 Active
**Location:** `content_strategy/` (linkedin/, substack/, twitter/)
**Purpose:** Cross-posting templates for blog → LinkedIn → Substack → X pipeline
**Content Ready:**
- Articles 1-5 (D/P Framework): LinkedIn posts, Substack variants, Twitter threads
- Articles 6a & 6b (P Work Execution): LinkedIn short form (500-700 words), Substack drafts, Twitter threads
- Roadmap document: `content_strategy/DP_Framework/ROADMAP_AND_OUTLINE.md` (15+ planned articles)

**When to Extract:** Never (part of content workflow)

---

## Tier 2: In Development (Part of fullstackpm.tech)

Projects being actively built. Deployed with main app during development.

### 1. PM Tech Companion
**Status:** 🟡 Phase 1 (Concept Complete)
**Location:** `project_ideas/01_PM_TECH_COMPANION.md`
**Timeline:** Start build 2026-02-20
**Features (Planned):**
- Input: Problem/feature + tech stack + constraints
- Output: Technical breakdown, multiple build paths, effort estimates
- Example: CSV bulk upload architecture walkthrough

**Build Plan:**
- Phase 1 (2 weeks): Core generator engine + LinkedIn posts
- Phase 2 (2 weeks): Multi-platform support (LinkedIn Ads, email, workplace)
- Phase 3 (1 week): Content library + export
- Phase 4 (1 week): Performance dashboard

**When to Extract:** 2026 Q3
- Criteria: 10+ working examples in library
- Action: Launch as SaaS or standalone tool

---

### 2. PM Multiverse
**Status:** 🟡 Phase 1 Complete (Persona Synthesis)
**Location:** `/Users/sidc/Projects/claude_code/pm_multiverse/`
**Dashboard:** `pm_multiverse/dashboard/index.html`
**Timeline:** Started 2026-02-20
**Features (Planned):**
- Interactive experience: 5 PM personas solve the same product problems and explicitly disagree
- Your Take First quiz → Persona Match → The Split → Arena deep dives → Live voting → PM DNA Card
- 10 product problems, ~60-70 content atoms per problem
- LinkedIn-shareable PM DNA cards
- Live vote aggregation (SQLite backend)

**Personas:** Marty Cagan, Teresa Torres, Shreyas Doshi, Lenny Rachitsky, Execution AI Monster (fictional)

**Build Plan:**
- Phase 1 ✅: Persona research + synthesis (all 5 persona files complete)
- Phase 2 (next): Rewrite YouTube Brazil problem JSON with persona-grounded content
- Phase 3: Build interactive HTML/CSS/JS shell + vote API
- Phase 4: Haiku replicates problems 2-10 using content template

**When to Extract:** 2026 Q2
- Criteria: 3+ problems live, vote API working, shareable DNA cards
- Action: Integrate into fullstackpm.tech as `/tools/pm-multiverse` or standalone

---

### 3. LinkedIn Job Search System
**Status:** 🟡 Phase 1 Complete (Pipeline Built)
**Location:** `/Users/sidc/Projects/claude_code/linkedin_job_search/`
**Timeline:** Built 2026-03-05
**Features (Shipped):**
- Daily job finder — searches LinkedIn, Indeed, Glassdoor via JobSpy (no credentials needed)
- JD analyzer — extracts keywords, requirements, ATS-critical terms
- Resume matcher — scores fit against ATS master resume with gap analysis
- Resume tailor — generates specific bullet rewrites to close keyword gaps
- Prompt templates for Claude-powered analysis (zero API cost)
- Config-driven search: Senior PM roles, Seattle + remote, 25mi radius

**Key Files:**
- `scripts/find_jobs.py` → daily job discovery (73+ PM jobs per run)
- `scripts/analyze_jd.py` → JD extraction and prompt generation
- `scripts/match_resume.py` → resume scoring prompt generation
- `scripts/tailor_resume.py` → tailored bullet rewrite prompt generation
- `templates/*.md` → Claude instruction sets for analysis

**Dependencies:** Python 3.10+, python-jobspy, pandas
**When to Extract:** N/A (personal job search tool, separate repo already)

---

### 4. Book Marketing Content Generator
**Status:** 🟡 Phase 0 (Planning)
**Location:** `code/BOOK_MARKETING_GENERATOR.md`
**Timeline:** Start design 2026-03-01
**Features (Planned):**
- Input: Book metadata (title, theme, insights, testimonials)
- Output: 50+ content variations for:
  - LinkedIn (organic + ads, audience-targeted)
  - Email subject lines
  - Workplace ads (Slack, Teams, Discord)
  - Twitter/X threads
  - Testimonial prompts

**When to Extract:** 2026 Q4
- Criteria: Tested with "Memoirs of a Mediocre Manager"
- Action: Open-source or SaaS depending on demand

---

## Tier 3: Planned for Extraction

Projects conceptualized but not yet built. Will live on fullstackpm.tech during development, then move to separate repos.

### 1. Junior PM Agent
**Status:** 📋 Idea Evaluated (in `ideas_evaluated/`)
**Spec:** `ideas_evaluated/2026-03-01-junior-pm-agent.md`
**Concept:** AI agent that handles task-level PM work (PRDs, user stories, bug triage, stakeholder updates, research synthesis) using explicit D/P workflow patterns with human checkpoints.
**Monetization:** Freemium SaaS — Free (5 tasks/mo) → Pro $29/mo → Team $79/seat/mo
**Tech:** FastAPI + Claude API + PostgreSQL + Jira/Slack integrations

**Success Criteria (before moving to active):**
- 10+ PM interviews confirm top 3 tasks worth automating
- Landing page converts at 10%+ from 200+ visitors
- PRD generation prototype rated "usable with minor edits" by 7/10 PMs

**When to Build:** After validation (Q2 2026)

---

### 2. Books Portal
**Status:** 📋 Concept
**Planned Scope:**
- Consolidate all books under `/books/` section
- Move themediocremanager.com content into fullstackpm.tech/books/memoirs
- Book landing pages with cover, reviews, table of contents
- Future: Support multiple books (Memoirs v2, business book, self-help book, etc.)

**When to Build:** 2026-03-15
**When to Extract:** 2026-06-01 (once 2+ books exist)

---

### 3. PM Community Platform (Future)
**Status:** 📋 Concept
**Planned Scope:**
- Forum for PMs to discuss architectural decisions
- Share trade-offs, patterns, lessons learned
- Library of "how to build X" case studies
- Real-time collaboration on PM problems

**When to Build:** 2026 Q2+
**When to Extract:** Standalone service (separate repo + database)

---

### 4. fullstackpm.tech UI/UX Redesign
**Status:** 📋 Concept
**Planned Scope:**
- Adopt the dark gradient + accent color + card-based design language from PM Multiverse "How I Built It" page
- Create unified design system (CSS variables, component patterns) across all pages
- Modernize homepage, project pages, tool pages with consistent visual language
- Improve mobile responsiveness and dark mode consistency

**Inspiration:** `pm_multiverse/how_it_was_built/index.html`
**When to Build:** 2026 Q2
**When to Extract:** N/A (site-wide improvement)

---

### 5. Advanced Interview Coach
**Status:** 📋 Concept
**Planned Features:**
- OAuth + LLM selection (use your ChatGPT/Claude/Gemini key)
- Email notifications on progress
- Cohort analysis (compare performance across users)
- Video recording of practice (store in S3)
- Admin dashboard for content management

**When to Build:** 2026 Q2+
**When to Extract:** 2026 Q3 (separate npm + SaaS)

---

## Repo Strategy

### Current (Single Repo)
```
fullstackpm.tech/
├── code/              ← What Render deploys
├── content/           ← Blog posts, projects
├── content_strategy/  ← Cross-posting drafts (LinkedIn, Substack, X)
├── project_ideas/     ← Concepts being developed
└── docs/              ← Developer documentation

ideas_evaluated/       ← Separate folder (~/Projects/claude_code/ideas_evaluated/)
                         Ideas incubate here before moving to PROJECTS_STATUS.md
```

**Benefits:** Simple, fast iteration, single deployment
**Drawbacks:** Gets cluttered as projects accumulate

---

## Current Snapshot (March 8, 2026)

| Metric | Value |
|--------|-------|
| Blog posts | 13 |
| Project pages | 9 |
| Live tools | 3 (Interview Coach, Marketplace Analytics, SDE Prep) |
| Dev tools | 1 (LinkedIn Job Search System) |
| Newsletter subscribers | 2+ |
| Content strategy drafts | 3 (LinkedIn, Substack, X for D/P Framework) |
| Monthly visitors | ~100 |
| Revenue | $0 |

---

## Week of March 2-8, 2026 — Completed

### Content ✅
- [x] Mar 6: Article 6a published — "The Three Types of P Work Failures and Where to Put Your Human Checkpoints" (diagnostic)
- [x] Mar 8: Article 6b published — "P Work Thresholds, Case Studies, and Your Implementation Checklist" (tactical)
- [ ] Cross-post D/P Framework to LinkedIn (draft ready in `content_strategy/linkedin/`)
- [ ] Cross-post to Substack (draft ready in `content_strategy/substack/`)
- [ ] "How I Built the Newsletter System" build log (deferred to next week)

### Infrastructure ✅
- [x] Newsletter debugging: Fixed special character encoding bug in unsubscribe links (+ @ symbols)
- [x] Newsletter fully tested and operational on Render
- [x] Set up Render env var for Google Sheets credentials
- [ ] Add analytics to site (Plausible or Umami)
- [ ] Connect Google Search Console
- [ ] Add newsletter CTA to About page and Project pages

### Product
- [ ] PM Multiverse Phase 2: Start persona-grounded content rewrite
- [ ] Evaluate PM Agent: Start drafting PM interview questions

---

## Extraction Decision Tree

**Ask these questions to decide when to extract:**

1. **Is it mature?** (v1 complete, tested, stable) → Consider extraction
2. **Is it reusable?** (Others could use it outside portfolio) → Extract
3. **Does it have own dependencies?** (Different from main app) → Extract
4. **Do you want to monetize?** (SaaS, npm package) → Extract
5. **Is it growing faster than portfolio?** (Needs separate velocity) → Extract

**If 3+ "yes" answers → Extract to separate repo**

---

## Current Extraction Timeline

| Project | Current Status | Extraction Date | Target | New Repo |
|---------|---|---|---|---|
| Interview Coach | Live | Q2 2026 | npm + SaaS | fullstackpm-interview-coach |
| SDE Prep Tool | Live | Never | Stay integrated | (none) |
| Marketplace Analytics | Live | Q3 2026 | Reusable template | fullstackpm-marketplace-analytics |
| Newsletter | Live | Never | Stay integrated | (none) |
| PM Multiverse | Phase 1 done | Q2 2026 | Integrate or standalone | fullstackpm-pm-multiverse |
| PM Tech Companion | In dev | Q3 2026 | SaaS or standalone | fullstackpm-pm-tech-companion |
| LinkedIn Job Search | Phase 1 done | N/A | Personal tool | linkedin_job_search |
| Junior PM Agent | Idea evaluated | Q2-Q3 2026 | SaaS | fullstackpm-pm-agent |
| Book Marketing Gen | Planned | Q4 2026 | Open source | fullstackpm-book-marketing-gen |
| UI/UX Redesign | Concept | N/A | Site-wide | (none) |
| Books Portal | Planned | Q2 2026 | Stay integrated | (none) |
| PM Community | Concept | 2027+ | Separate service | fullstackpm-community |

---

## How to Update This Document

1. When you **ship** a project → Move to "Integrated" section
2. When you **start** development → Move to "In Development" with timeline
3. When you **extract** → Update with new repo name
4. When metrics change → Update metrics quarterly

## Week of March 9-15, 2026 — Plan

### Content (Cross-posting focus)
- [ ] Mon 3/9: Cross-post Article 6a to LinkedIn (diagnostic, 500-700 words)
- [ ] Tue 3/10: Cross-post Article 6b to LinkedIn (tactical, 500-700 words)
- [ ] Wed 3/11: Post Substack version of 6a + 6b
- [ ] Thu 3/12: Write Article 7 (Building Teams for P Work) — 10-15K words
- [ ] Fri 3/13: Build log: "How I Built the Newsletter System"
- [ ] Sat 3/14: Catch-up / publishing buffer
- [ ] Sun 3/15: Week 2 retrospective

### Audience Building
- [ ] Add analytics (Plausible or Umami)
- [ ] Google Search Console setup
- [ ] LinkedIn cross-posting (Articles 6a & 6b)
- [ ] Share on X/Twitter (threads from both articles)

### Product
- [ ] PM Multiverse Phase 2: Start persona-grounded content rewrite (YouTube Brazil problem)
- [ ] Junior PM Agent: Finalize validation questions + start PM interviews
- [ ] Interview Coach: Plan Q2 extraction roadmap

### Infrastructure
- [ ] Add newsletter CTA to About page and all Project pages
- [ ] Set up email forwarding from newsletter to personal inbox (if desired)

---

**Last Updated:** 2026-03-08
**Next Review:** 2026-03-15

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

### 3. Blog + Comments System
**Status:** 🟢 Live
**URL:** /blog
**Tech:** Markdown + SQLite (comments)
**Features:**
- 2 published posts
- Blog post comments (database-backed)
- Tag filtering
- RSS feed
- SEO (sitemap, robots.txt)

**Metrics:**
- ~50 monthly blog visitors (estimate)
- Comments: ~5-10 per month
- Storage: <1MB

**When to Extract:** Never (part of core portfolio)
- Stay integrated with main site
- Content = your voice

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

### 2. Book Marketing Content Generator
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

**Build Plan:**
- Phase 1 (2 weeks): Metadata form + LinkedIn post generator
- Phase 2 (2 weeks): Multi-platform variations
- Phase 3 (1 week): Content library + batch export
- Phase 4 (1 week): Performance tracking

**When to Extract:** 2026 Q4
- Criteria: Tested with "Memoirs of a Mediocre Manager"
- Action: Open-source or SaaS depending on demand

---

## Tier 3: Planned for Extraction

Projects conceptualized but not yet built. Will live on fullstackpm.tech during development, then move to separate repos.

### 1. Books Portal
**Status:** 📋 Concept
**Planned Scope:**
- Consolidate all books under `/books/` section
- Move themediocremanager.com content into fullstackpm.tech/books/memoirs
- Book landing pages with cover, reviews, table of contents
- Future: Support multiple books (Memoirs v2, business book, self-help book, etc.)

**When to Build:** 2026-03-15
**When to Extract:** 2026-06-01 (once 2+ books exist)

---

### 2. PM Community Platform (Future)
**Status:** 📋 Concept
**Planned Scope:**
- Forum for PMs to discuss architectural decisions
- Share trade-offs, patterns, lessons learned
- Library of "how to build X" case studies
- Real-time collaboration on PM problems

**When to Build:** 2026 Q2+
**When to Extract:** Standalone service (separate repo + database)

---

### 3. Advanced Interview Coach
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
├── project_ideas/     ← Concepts being developed
└── docs/              ← Developer documentation
```

**Benefits:** Simple, fast iteration, single deployment
**Drawbacks:** Gets cluttered as projects accumulate

### Year 2 (Selective Extraction)
```
fullstackpm.tech/          ← Core portfolio + integrated tools
├── code/
├── content/
├── project_ideas/
└── projects_integrated/
    ├── interview-coach/
    └── marketplace-analytics/

fullstackpm-projects/      ← Mature standalone projects
├── pm-tech-companion/
├── book-marketing-gen/
└── pm-community-platform/
```

**Benefits:** Clean separation, reusable projects, different deployment pipelines
**Drawbacks:** More repos to manage

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
| Marketplace Analytics | Live | Q3 2026 | Reusable template | fullstackpm-marketplace-analytics |
| PM Tech Companion | In dev | Q3 2026 | SaaS or standalone | fullstackpm-pm-tech-companion |
| Book Marketing Gen | Planned | Q4 2026 | Open source | fullstackpm-book-marketing-gen |
| Books Portal | Planned | Q2 2026 | Stay integrated | (none) |
| PM Community | Concept | 2027+ | Separate service | fullstackpm-community |

---

## Monitoring & Metrics

### Interview Coach
- **Track:** Monthly evaluations, user sessions, OpenAI API cost
- **Goal:** 5K+ monthly evaluations before extraction
- **Check:** `SELECT COUNT(*) FROM interview_attempt WHERE created_at > now() - interval '1 month'`

### Marketplace Analytics
- **Track:** Daily active users, feature adoption, data volume
- **Goal:** 1K+ active sellers before extraction
- **Check:** Manual review (no analytics instrumented yet)

### PM Tech Companion
- **Track:** Examples in library, user feedback, usage
- **Goal:** 20+ working examples before SaaS launch
- **Check:** Count markdown files in `project_ideas/examples/`

---

## Next Project Priorities

### This Month (February 2026)
- ✅ Fix project filters (done!)
- 🔄 Start PM Tech Companion Phase 1
- 📋 Plan Books Portal feature

### Next Month (March 2026)
- Complete PM Tech Companion Phase 1-2
- Start Book Marketing Generator design
- Add 3+ new PM Tech Companion examples

### Q2 2026
- Launch Books Portal
- Extract Interview Coach (npm)
- Complete PM Tech Companion SaaS planning
- Add advanced Interview Coach features

---

## How to Update This Document

1. When you **ship** a project → Move to "Integrated" section
2. When you **start** development → Move to "In Development" with timeline
3. When you **extract** → Update with new repo name
4. When metrics change → Update metrics quarterly

**Last Updated:** 2026-02-14
**Next Review:** 2026-04-01

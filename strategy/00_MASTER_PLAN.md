# fullstackpm.tech — Master Plan

## Vision

A personal portfolio and project showcase that proves — through shipped work — that the best Product Managers in 2026 don't just manage products, they build them. This site is both the portfolio AND the first project in it.

**Domain:** fullstackpm.tech
**Owner:** Harsha Cheruku
**Positioning:** Full Stack AI Product Manager — SDE turned PM turned builder

---

## The Narrative

Your career arc is your unfair advantage:

1. **Engineer** (Wipro, ~4 years) — You started writing code. You understand systems.
2. **Product & Program Manager** (VF Corp, ~4 years) — You learned business, supply chain, cross-functional leadership.
3. **Data & Analytics PM** (Verizon, ~4 years) — You discovered the power of data-driven product decisions, experimentation, segmentation.
4. **Marketplace & Advertising PM** (Amazon, ~4 years) — You operated at scale. 3P marketplace, seller experience, international, advertising. $300M+ revenue impact.
5. **PM Consultant** (Delphi, Middle East, ~9 months) — You brought AI/GenAI into consulting. HeyGen, MidJourney, ChatGPT API.
6. **Data Analytics & AI PM** (Walmart, current) — Marketplace growth, predictive analytics, seller strategy, AI automation.
7. **Full Stack PM** (NOW) — You're building again. AI-powered tools, a portfolio of shipped projects, proving the thesis with your own hands.

The story: *"I've been on both sides. I wrote code. I managed products at the biggest companies in the world. Now I do both — and I believe every PM should."*

---

## Core Tech Stack (All Projects)

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | **FastAPI** | Modern Python, async, great for APIs and templates, matches your Python expertise |
| Templates | **Jinja2** | Server-rendered, SEO-friendly, fast |
| Interactivity | **HTMX** | No JS framework needed, progressive enhancement, keeps things simple |
| Styling | **Tailwind CSS** (CDN for MVP, build later) | Utility-first, rapid prototyping, professional look |
| Database | **SQLite** (dev) → **PostgreSQL** (prod) | Start simple, scale when needed |
| AI | **Claude API** (primary), **OpenAI** (fallback) | Best reasoning for PM-quality outputs |
| Data/Analytics | **Pandas + NumPy + SciPy** | Python data stack you already know |
| Visualization | **Chart.js** or **Plotly** | Interactive charts in the browser |
| Deployment | **Render** or **Railway** | Free tier, auto-deploy from GitHub, SSL included |
| Version Control | **GitHub** | Public repos, consistent commit history |

---

## The 8 Projects

### Project 0: Portfolio Site (fullstackpm.tech)
**Signal:** Product thinking, information architecture, technical execution, shipping
**Effort:** 2 weeks
**Status:** Build first — everything else lives here

### Project 1: AI PM Interview Coach
**Signal:** AI integration, prompt engineering, building for your own need
**Effort:** 2 weeks
**Status:** Build second — uses your Munna Kaka question bank

### Project 2: Marketplace Analytics Dashboard
**Signal:** Data analytics, SQL, visualization, marketplace domain expertise
**Effort:** 2-3 weeks
**Status:** Your domain expertise showcase

### Project 3: AI PM Toolkit (Specs + Roadmaps + Stories)
**Signal:** AI agents, PM artifact generation, workflow automation
**Effort:** 2 weeks
**Status:** Shows AI fluency beyond chatbot usage

### Project 4: AI PM Decision System
**Signal:** Product sense, prioritization frameworks, structured reasoning
**Effort:** 2 weeks
**Status:** Senior PM skill demonstration

### Project 5: LLM Prompt Evaluation Framework
**Signal:** AI rigor, evaluation methodology, systematic thinking
**Effort:** 2 weeks
**Status:** Most differentiating for AI PM roles

### Project 6: A/B Test Analyzer & Sample Size Calculator
**Signal:** Statistical thinking, experimentation, analytical depth
**Effort:** 2 weeks
**Status:** Proves "data-driven" isn't just a buzzword

### Project 7: AI Bootcamp Case Study (Write-up of existing work)
**Signal:** End-to-end product leadership, reflection, storytelling
**Effort:** 1 week (write-up only — project already exists)
**Status:** Flagship case study leveraging AI Learning Roadmap + PM Academy

---

## Build Timeline (16 Weeks)

```
Week  1-2  ████████ Project 0: Portfolio Site
Week  3-4  ████████ Project 1: PM Interview Coach
Week  5-7  ████████████ Project 2: Marketplace Dashboard
Week  7-9  ████████ Project 3: AI PM Toolkit
Week  9-11 ████████ Project 4: PM Decision System
Week 11-13 ████████ Project 5: LLM Prompt Eval Framework
Week 13-15 ████████ Project 6: A/B Test Analyzer
Week 15-16 ████ Project 7: AI Bootcamp Case Study
```

**Blog cadence:** One companion post per project, published when project ships.

---

## GitHub Strategy

### Commit Cadence
- Aim for daily commits during active project weeks
- Each project gets its own repo OR lives as a module within the main fullstackpm.tech repo
- Clean READMEs with: problem statement, screenshots/demo, tech stack, how to run

### Repo Structure Options

**Option A: Monorepo** (Recommended for portfolio coherence)
```
fullstackpm.tech/
├── strategy/           # Planning docs (this folder)
├── site/               # The portfolio website (Project 0)
├── projects/
│   ├── interview-coach/
│   ├── marketplace-dashboard/
│   ├── ai-pm-toolkit/
│   ├── pm-decision-system/
│   ├── prompt-eval/
│   ├── ab-test-analyzer/
│   └── bootcamp-case-study/
├── blog/               # Blog post markdown files
└── README.md
```

**Option B: Multi-repo** (Better GitHub activity signal)
- `fullstackpm.tech` — the portfolio site
- `pm-interview-coach` — standalone project
- `marketplace-dashboard` — standalone project
- etc.

**Recommendation:** Start with monorepo for simplicity. Split into separate repos later if you want more GitHub activity tiles.

---

## Content Strategy

### Blog Posts (8 minimum, one per project)

| Post | Project | Angle |
|------|---------|-------|
| "Why I'm Building in Public as a PM" | Site | Meta / launch |
| "I Built an AI Coach to Prep for PM Interviews" | Interview Coach | Building for yourself |
| "5 Marketplace Metrics I Actually Tracked at Amazon" | Dashboard | Domain authority |
| "Can AI Write a Product Spec? I Built a Tool to Find Out" | PM Toolkit | AI product exploration |
| "A Framework for Kill/Build Feature Decisions" | Decision System | Product sense |
| "How I Evaluate LLM Prompts (Not Just Vibes)" | Prompt Eval | AI rigor |
| "Most PMs Get A/B Testing Wrong — Here's the Math" | A/B Analyzer | Analytical depth |
| "What I Learned Building an AI Bootcamp MVP" | Case Study | Reflection + product leadership |

### Voice & Tone
- Conversational but credible
- Experience-based — reference real (non-proprietary) examples from Amazon/Walmart/Verizon
- Honest about tradeoffs
- Action-oriented — every post leaves the reader with something to do
- No fluff, no filler

---

## Interview Prep Integration

The portfolio doesn't replace interview prep — it supercharges it. Here's how each project maps to PM interview categories:

| Interview Category | Projects That Prepare You |
|-------------------|--------------------------|
| **Product Sense / Design** | PM Decision System, PM Toolkit, Portfolio Site |
| **Analytical** | Marketplace Dashboard, A/B Test Analyzer, Prompt Eval |
| **Execution** | All projects (you shipped them), Bootcamp Case Study |
| **Strategy** | PM Decision System, PM Toolkit, Dashboard |
| **Technical** | Every project (you built them with code) |
| **Behavioral / Leadership** | Blog posts, Bootcamp Case Study, building in public narrative |

**Continue using your Munna Kaka materials** for structured interview prep. The portfolio provides the *stories*; the Munna Kaka frameworks provide the *structure* for telling them.

---

## Success Criteria

### After 4 months (all projects shipped):
- [ ] fullstackpm.tech is live with 8 projects showcased
- [ ] 8+ blog posts published
- [ ] GitHub profile shows consistent activity over 16 weeks
- [ ] Each project has a clean README with problem statement, demo, and tech stack
- [ ] You can walk an interviewer through any project in 5 minutes
- [ ] At least 3 projects have live demos (not just code)

### Longer term:
- [ ] LinkedIn articles driving traffic to the site
- [ ] Portfolio referenced in job applications
- [ ] Projects generating inbound conversations ("I saw your marketplace dashboard...")
- [ ] The AI Bootcamp case study positioned as your flagship product leadership story

---

## What This Plan Is NOT

- **Not a monetization plan.** This is a career asset, not a business.
- **Not a content calendar.** Blog when you ship, not on a schedule.
- **Not a comprehensive curriculum.** You're building things, not teaching courses.
- **Not permanent.** The site will evolve. Ship fast, iterate later.

---

## Next Step

Read `01_PORTFOLIO_SITE.md` → Start building the portfolio site.

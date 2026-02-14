# Project 7: AI Bootcamp Case Study

## Product Brief

### Problem
You've already built two significant projects — the AI Learning Roadmap (an automated AI PM bootcamp with full business plan) and the PM Academy (a portfolio website). These represent real product leadership work: vision, strategy, architecture, business model, content strategy. But they're buried in files nobody sees. You need to tell the story.

### Solution
A case study write-up that presents the AI Bootcamp + PM Academy work as a product leadership narrative. This is not code — it's content. It becomes a project entry on your portfolio site, rendered by the existing content engine. Structured as: The Opportunity → Vision → Strategic Decisions → Architecture → Business Model → What I Learned.

### Target Audience
- Interviewers asking "Tell me about a product you built end-to-end"
- Hiring managers evaluating your product leadership depth
- PM peers interested in AI product strategy

### Non-Goals
- No new code to build (write-up only)
- Not a tutorial or how-to guide
- Not promotional (honest, reflective)
- Not a business pitch (it's a retrospective)

---

## Case Study Outline

### Section 1: The Opportunity
**Content guidance:** Set the scene. What market gap did you identify? Why did AI PM education need a new approach?

Key points to cover:
- The gap: PMs need AI/technical skills, but existing resources are either too technical or too surface-level
- The timing: AI tools (Claude Code, Cursor, Copilot) made "vibe coding" possible for non-engineers
- The dual audience: PMs wanting technical skills AND SDEs wanting product skills
- Market size / opportunity framing

**Artifacts to reference:** AI Learning Roadmap master plan (market analysis section), PM Academy product brief

### Section 2: Product Vision
**Content guidance:** What did you set out to build? What was the north star?

Key points to cover:
- The AI Learning Roadmap: an automated AI PM bootcamp that runs at 90% automation
- The PM Academy: a portfolio site proving the "Full Stack PM" concept by being built with vibe coding
- How the two projects complement each other (one is the business, one is the proof)
- The "dogfooding" philosophy: use the tools you teach

**Artifacts to reference:** Master plan vision section, PM Academy product brief

### Section 3: Strategic Decisions (and Why)
**Content guidance:** This is the most important section for interviews. Show your decision-making process.

Decisions to cover:

| Decision | Choice | Alternatives Considered | Why |
|----------|--------|------------------------|-----|
| Tech stack | FastAPI + HTMX | Next.js, Django, Rails | Lightweight, Python-native, no JS build step, demonstrates "vibe coding" |
| Content delivery | Markdown on disk | CMS (Contentful, Strapi), database | Git-native, zero infrastructure, easy AI-assisted authoring |
| Business model | 3-tier pricing ($199/$499/$799) | Freemium, subscription, ad-supported | Maximizes LTV, segments by commitment level |
| Automation level | 90% target | Manual operations, partial automation | Solo founder constraint; automation is the product thesis |
| Dual-path content | Separate PM and SDE tracks | Single generic track | Better targeting, clearer value proposition per audience |
| Database | PostgreSQL (bootcamp) / None (portfolio) | MongoDB, Firebase | PostgreSQL for production data; no DB for static content site |
| Deployment | Railway / Render free tier | AWS, Vercel, self-hosted | Cost-effective, auto-deploy, appropriate for scale |

### Section 4: Architecture & Technical Choices
**Content guidance:** Walk through the system architecture. Use the diagrams from the existing docs.

Key points to cover:
- System architecture: Public site → Automation layer → Data storage → Integration layer
- Automation pipeline: content generation, email sequences, social posting, analytics
- The 4-phase automation maturity model (Core → Content → Advanced → AI-First)
- How AI is used throughout: content generation, student support, analytics summarization
- Cost optimization: $143/month bootstrap to $5,500/month at scale

**Artifacts to reference:** Tech implementation doc, content strategy automation doc

### Section 5: Business Model
**Content guidance:** Show that you think about products as businesses, not just features.

Key points to cover:
- Revenue model: 3-tier pricing with clear value differentiation
- Unit economics: cost per student, LTV projections, margin targets
- Growth projections: Month 3 ($45K) → Month 6 ($225K) → Month 12 ($675K)
- Customer acquisition: content marketing, SEO, LinkedIn, community
- Why these projections are realistic (or where they might be optimistic — be honest)

**Artifacts to reference:** Master plan revenue section, README cost breakdown

### Section 6: Content Strategy
**Content guidance:** Show how you think about content as a product.

Key points to cover:
- 90-day content calendar with AI-assisted generation
- Content pillars: technical skills for PMs, product skills for SDEs, career transitions
- SEO strategy: target keywords, content quality, semantic HTML
- Automation approach: AI generates drafts, human reviews for quality/accuracy
- Email sequences for onboarding and retention

**Artifacts to reference:** Content strategy automation doc

### Section 7: What Worked / What I'd Change
**Content guidance:** This is what separates a good case study from a great one. Be reflective and honest.

What worked:
- Comprehensive planning before building (strategy docs as forcing function)
- Technology choices that minimize operational complexity
- The dual-path value proposition (clearer than a single generic offering)
- Automation-first mindset from day one

What I'd change:
- Revenue projections may be optimistic for a solo founder
- The automation target of 90% is aspirational — human review is more necessary than anticipated for content quality
- Would invest more in community features earlier (Discord, cohort-based learning)
- The tech stack is solid but the content is the actual product — would allocate more time to content creation vs. infrastructure
- Missing: competitive analysis depth, user research validation

### Section 8: Key Metrics & Outcomes
**Content guidance:** If the projects are live, include real metrics. If not, describe the metrics you would track and why.

Metrics framework:
- **Engagement:** page views, time on site, blog read completion rate
- **Growth:** email signups, return visitors, organic search traffic
- **Revenue:** (if applicable) MRR, conversion rate, churn
- **Technical:** uptime, page load speed, deployment frequency
- **Content:** posts published, SEO ranking improvements, social shares

### Section 9: Lessons Learned
**Content guidance:** 3-5 concise, transferable lessons. Not clichés — actual insights from the work.

Possible lessons:
1. "Strategy documents are not overhead — they're the cheapest way to make expensive decisions"
2. "Automation saves time only after the initial investment; budget for setup cost"
3. "The tech stack matters less than the content for a content business"
4. "Building for two audiences (PMs and SDEs) forces clearer value propositions for both"
5. "AI-assisted content generation is a workflow accelerator, not a replacement for expertise"

---

## Content Architecture

This case study is a markdown file that the portfolio site's content engine renders. It lives in `/content/projects/ai-bootcamp-case-study.md`.

### Frontmatter

```yaml
---
title: "AI PM Bootcamp: End-to-End Product Leadership Case Study"
slug: ai-bootcamp-case-study
status: case_study
date: 2026-04-01
tech_stack: [FastAPI, HTMX, PostgreSQL, Claude API, Tailwind CSS]
excerpt: "How I designed and built an automated AI PM bootcamp — from market analysis to technical architecture to business model."
github: null
live_demo: null
thumbnail: ai-bootcamp-case-study.png
---
```

### Companion Blog Post Outline

**Title:** "What I Learned Building an AI Bootcamp MVP"

**Structure:**
1. Hook: "I spent X weeks planning a product I haven't launched yet — and it was the most valuable PM exercise I've done"
2. The 80/20: what I'd keep vs. cut if starting over
3. The biggest surprise: where my assumptions were wrong
4. The meta-lesson: building a product about building products
5. CTA: link to full case study on portfolio site

---

## Presentation Format

### On the Portfolio Site

The case study renders as a project detail page (`/projects/ai-bootcamp-case-study`) with:
- Clean typography (long-form reading experience)
- Inline images/diagrams where helpful
- Decision tables rendered as HTML tables
- Pull quotes highlighting key lessons
- Link to companion blog post
- Links to source repos (AI Learning Roadmap, PM Academy)

### In Interviews

Prepare a 5-minute walkthrough version:
1. "I identified a gap in AI PM education" (30 sec)
2. "I designed a two-product system" (30 sec)
3. "Here are the 3 hardest decisions I made and why" (2 min)
4. "Here's what I'd do differently" (1 min)
5. "Here are the transferable lessons" (1 min)

---

## Development Phases

### Phase 1: Gather and Organize (Days 1-2)
- [ ] Re-read all AI Learning Roadmap docs and PM Academy strategy docs
- [ ] Extract key quotes, decisions, and metrics
- [ ] Outline the case study using the 9 sections above
- [ ] Identify gaps: what's missing that needs to be written from scratch?

### Phase 2: Write First Draft (Days 3-4)
- [ ] Write Sections 1-5 (Opportunity through Business Model)
- [ ] Write Sections 6-9 (Content Strategy through Lessons)
- [ ] Create any supporting diagrams or tables
- [ ] Write the companion blog post

### Phase 3: Review and Publish (Day 5)
- [ ] Self-edit for clarity, honesty, and conciseness
- [ ] Add frontmatter and save as project markdown file
- [ ] Verify rendering on portfolio site
- [ ] Publish blog post
- [ ] Practice the 5-minute interview walkthrough version

---

## Next Step

Start by re-reading all the source documents (AI Learning Roadmap master plan, tech implementation, content strategy, PM Academy product brief and strategy docs). Take notes on the key decisions and their rationale. The case study is only as strong as the decisions you can articulate.

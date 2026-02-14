# BUILD: Book Marketing Content Generator

## Project Overview

An AI-powered content generation system that creates marketing variations for books across LinkedIn, workplace ads, and social platforms. Input book details once, generate dozens of marketing angles, hooks, and CTAs tailored to different platforms and audience segments.

**Audience:** Authors, indie publishers, Full Stack PMs
**Outcome:** 10x faster content creation, consistent messaging, data-driven A/B testing
**Timeline:** ~4 phases (see below)

---

## Problem Statement & Goals

**Problem:** Marketing a book requires creating dozens of variations:
- LinkedIn posts (organic + ads)
- Workplace ad copy (different segments: executives, managers, IC engineers)
- Email subject lines
- Twitter/X threads
- Testimonial prompts
- Call-to-action variations

Manual creation is slow. Templates feel repetitive. Testing takes forever.

**Goals:**
- Generate 50+ marketing variations from book metadata
- Tailor copy to platform (LinkedIn organic vs. ads vs. email)
- Segment by audience (C-suite, managers, individual contributors, students)
- A/B test copy with performance tracking
- Export ready-to-use content for campaigns

---

## Feature Breakdown

### 1) Book Metadata Input
- Title, subtitle, description, target audience, key themes
- Core insights/lessons (3-5 main takeaways)
- Testimonials/reviews (if available)
- CTA preference (Amazon link, landing page, waitlist)

### 2) Content Generation Engine
Using OpenAI, generate variations for:
- **LinkedIn Posts** (organic, 3-5 versions each hook)
  - Hook: Problem recognition
  - Hook: Surprising insight
  - Hook: Personal story
  - Hook: Data-driven takeaway
  - Hook: Call to action variant

- **LinkedIn Ads** (audience-targeted)
  - Executives (decision-maker angle)
  - Managers (team/leadership angle)
  - Individual Contributors (growth/skill angle)
  - Students (career foundation angle)

- **Email Subject Lines** (10+ variations, tested for open rate patterns)
  - Curiosity-driven
  - Benefit-driven
  - Authority-driven
  - FOMO-driven
  - Question-driven

- **Ad Copy Variations** (Workplace ads: Slack, Microsoft Teams, Discord)
  - Long form (100 chars)
  - Medium form (50 chars)
  - Short form (30 chars)

- **Testimonial Prompts** (Suggests what to ask reviewers)
  - "What surprised you most?"
  - "Who should read this?"
  - "What's the key insight you'll implement?"

- **Tweet/X Threads** (5-10 tweet sequences breaking down core ideas)

### 3) Platform-Specific Templates
- LinkedIn native post format
- LinkedIn Ads format (headline + body + CTA)
- Email template ready
- Workplace ad ready
- Social media snippet ready

### 4) Performance Tracking Dashboard
- Track which copy variants get used
- Clickthrough rates (if ads integrated)
- Engagement data (likes, comments, shares)
- A/B testing framework (show 2-3 variants, measure)
- Export performance report

### 5) Content Management
- Save generated content to library
- Tag by platform, audience, hook type
- Batch export (CSV, Markdown, JSON)
- Reuse across books (theme templates)
- Version history

---

## Technical Architecture

**Backend:** FastAPI routes + OpenAI API for generation
**Frontend:** Jinja2 templates + HTMX for real-time generation
**Storage:** SQLite (content library, performance metrics)
**AI:** OpenAI ChatGPT (structured prompts for consistency)

**Core files:**
```
code/app/
├── routers/
│   └── book_marketing.py
├── services/
│   └── content_generator.py
├── models/
│   ├── book.py
│   └── marketing_content.py
├── templates/
│   └── book-marketing/
│       ├── index.html
│       ├── generator.html
│       ├── library.html
│       └── partials/
│           ├── book_form.html
│           ├── content_variants.html
│           └── performance.html
└── static/js/
    └── marketing.js (copy-to-clipboard, export)
```

---

## Step-by-Step Build Plan (4 Phases)

### Phase 1: Core Generation Engine
- Build OpenAI integration with structured prompts
- Create book metadata form
- Test single content type (LinkedIn posts)
- Validate prompt quality + consistency

### Phase 2: Multi-Platform Support
- Add LinkedIn Ads generator
- Add Email subject lines
- Add Workplace ad copy
- Ensure consistency across platforms

### Phase 3: Content Library & Export
- SQLite schema for saving content
- Library page (view, tag, search)
- Batch export (CSV, Markdown)
- Copy-to-clipboard functionality

### Phase 4: Performance & Dashboard
- Track usage of content variants
- A/B testing framework setup
- Performance dashboard (mockups)
- Reuse templates for future books

---

## Acceptance Criteria

### MVP (Must Have)
- Book metadata form works
- LinkedIn posts generation (5+ variations)
- Email subject lines (5+ variations)
- Copy-to-clipboard for each variant
- Responsive mobile friendly
- Dark mode ready

### Nice-to-Haves
- LinkedIn Ads generator (audience-specific)
- Workplace ad copy
- Performance tracking dashboard
- Batch export (CSV)
- Content library with search/tags

---

## Mock Usage Flow

1. **User lands at `/tools/book-marketing`**
2. **Fills out book form:**
   - Title: "Memoirs of a Mediocre Manager"
   - Subtitle: "Surviving tech leadership"
   - Target audience: "Product managers, tech leaders"
   - Key insights: "Leadership isn't about being smart. It's about survival. Reorgs happen. People matter. Ship anyway."
3. **Clicks "Generate Content"**
4. **System generates:**
   - 5 LinkedIn post variations
   - 5 email subject line variations
   - 3 LinkedIn Ads (exec/manager/IC)
   - 5 Workplace ad variations
5. **User copies variants into campaign tools**
6. **Later: tracks performance in dashboard**

---

## Design System Guidelines

Use existing tokens + typography:
- Colors via CSS variables
- Typography: `text-h2`, `text-body`, `text-small`
- Cards: `rounded-xl`, `border-color: var(--color-border)`
- Form inputs: consistent styling

---

## Why Build This Project

1. **Demonstrates Full Stack PM capability** — solves real problem (your own book marketing)
2. **AI workflow example** — uses OpenAI in a structured, repeatable way
3. **Scalable for future books** — template approach works for any book
4. **Community value** — indie authors would pay for this tool
5. **Marketing multiplier** — 50+ variations = 10x more A/B testing opportunities

---

## Deployment Notes

- No schema migrations required for MVP
- OpenAI API key in environment (already set up in Render)
- Add route in `main.py`
- Add to navbar (or Projects page)
- Deploy to Render (auto-deploy on push)

---

## Next Steps

**Ready to build when you are.**

Estimated effort: 5-7 days for full build (Phases 1-4)
Incremental release: Phase 1-2 in 2 days, then iterate

Would you prefer to:
1. Start with Phase 1 only (LinkedIn posts + email)
2. Build full MVP (all 4 phases)
3. Build Phase 1-2 first, then gather feedback before Phase 3-4?

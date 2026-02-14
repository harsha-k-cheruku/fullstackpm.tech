# Project 0: Portfolio Site — fullstackpm.tech

## Product Brief

### Problem
You need a public home base that showcases your projects, communicates your Full Stack PM thesis, and gives interviewers/hiring managers a reason to remember you. LinkedIn alone doesn't demonstrate building capability. A GitHub profile alone doesn't show product thinking. You need both — unified in one place.

### Solution
A personal portfolio site that is itself a demonstration of product + technical skills. Fast, clean, server-rendered, SEO-friendly, and built with the same stack you'll use across all projects.

### Target Audience
1. **Hiring managers & recruiters** looking at your application
2. **Interviewers** who Google you before a panel
3. **PM peers & network** who see your LinkedIn posts
4. **Engineers** who check your GitHub

### Non-Goals
- No user accounts or authentication
- No payment processing
- No newsletter signup (v1 — add later if desired)
- No CMS — content is markdown files in the repo
- No JavaScript framework

---

## Information Architecture

### Sitemap

```
fullstackpm.tech/
├── /                       → Home (landing page)
├── /about                  → About (your story)
├── /projects               → Project gallery
├── /projects/{slug}        → Individual project detail
├── /blog                   → Blog listing
├── /blog/{slug}            → Individual blog post
├── /blog/tag/{tag}         → Posts filtered by tag
├── /resume                 → Interactive resume / experience timeline
├── /contact                → Contact info + links
├── /feed.xml               → RSS feed
├── /sitemap.xml            → SEO sitemap
└── /robots.txt             → Search engine directives
```

### Navigation

**Primary Nav (always visible):**
Home | Projects | Blog | About | Contact

**Footer:**
GitHub | LinkedIn | RSS | "Built with FastAPI + HTMX"

---

## Page Specifications

### Home (`/`)

**Purpose:** Hook visitors in 5 seconds. Answer: "Who is this person and why should I care?"

**Content blocks (top to bottom):**

1. **Hero section**
   - Name: Harsha Cheruku
   - Tagline: "Engineering Mind. Design Obsession."
   - Sub-text: "Product leader with 16 years at Amazon, Walmart, and Verizon — now building AI-powered tools that prove the best PMs don't just manage products, they craft them."
   - CTA buttons: "See My Projects" | "Read My Story"

2. **Featured projects** (3 cards)
   - Show 3 most impressive projects
   - Each card: title, one-line description, tech stack tags, thumbnail/icon
   - Click → `/projects/{slug}`
   - Use HTMX to load project cards dynamically (demonstrates HTMX usage)

3. **Latest blog post**
   - Title, excerpt, date, read time
   - Click → `/blog/{slug}`

4. **The thesis** (brief)
   - 2-3 sentences on what "Full Stack PM" means
   - Link to About page for the full story

### About (`/about`)

**Purpose:** Tell your story. Make it human, not corporate.

**Content structure:**

1. **Opening hook**
   - Something personal/unexpected. Not "I am a product manager with 16 years..."
   - Maybe: "I wrote my first line of code in Bengaluru in 2008. Sixteen years later, I'm writing code again — but now I also know *what* to build and *why*."

2. **The career narrative** (3 chapters)
   - **The Engineer:** Wipro — building systems, understanding technical architecture
   - **The Product Leader:** VF Corp → Verizon → Amazon → Walmart — learning customers, markets, strategy at scale
   - **The Builder (again):** Delphi consulting with GenAI → Walmart AI → now building your own tools
   - Keep each chapter to 2-3 paragraphs. Link to relevant projects where applicable.

3. **What I believe**
   - Your thesis on Full Stack PMs
   - Why AI changes the game for PMs
   - What "vibe coding" means to you

4. **Education & credentials** (brief)
   - Duke MBA, MIT Data Science, Columbia Executive Programs, JNTU CS
   - Certifications: AWS Cloud Practitioner, AI for Product, Tableau, Amazon Marketing Cloud, Amazon DSP

5. **Personal note** (optional)
   - Author of "Memoirs of a Mediocre Manager"
   - Anything else that shows personality

### Projects (`/projects`)

**Purpose:** Gallery of shipped work. The core of the portfolio.

**Layout:** Card grid (responsive — 3 columns desktop, 2 tablet, 1 mobile)

**Each project card shows:**
- Project name
- One-line description
- Tech stack tags (FastAPI, Claude API, Pandas, etc.)
- Status badge: "Live" | "In Progress" | "Case Study"
- Thumbnail or icon

**Click → `/projects/{slug}`**

### Project Detail (`/projects/{slug}`)

**Purpose:** Deep dive into a single project. This is what interviewers will read.

**Content structure (for each project):**

1. **Header:** Project name + one-liner + status badge
2. **The Problem:** What problem does this solve? Who has this problem?
3. **The Approach:** How did you think about solving it? What tradeoffs did you consider?
4. **The Solution:** What did you build? Screenshots/demo GIF. Key features.
5. **Technical Details:** Architecture, tech stack, key implementation decisions
6. **What I Learned:** Honest reflection. What worked, what didn't, what you'd do differently.
7. **Links:** GitHub repo | Live demo | Companion blog post

**Data source:** Each project is a markdown file with YAML frontmatter in `/content/projects/`.

### Blog (`/blog`)

**Purpose:** Long-form thinking that complements the projects.

**Layout:**
- List view with: title, date, excerpt, tags, read time
- Tag filtering (click a tag → `/blog/tag/{tag}`)
- Pagination (10 posts per page)

**Blog posts are markdown files** in `/content/blog/` with frontmatter:
```yaml
---
title: "I Built an AI Coach to Prep for PM Interviews"
date: 2026-03-15
tags: [ai, interview-prep, building-in-public]
excerpt: "Instead of studying flashcards, I built a tool that studies me."
author: Sid Cheruku
---
```

### Resume (`/resume`)

**Purpose:** Interactive version of your experience — more engaging than a PDF.

**Layout:** Visual timeline (vertical)
- Each role: company logo/icon, title, dates, 3-4 bullet points of impact
- Highlight key metrics ($300M+ revenue, 22M customers, 370K businesses)
- Skills section grouped by category:
  - **Product:** Strategy, Roadmap, GTM, Pricing, Marketplace, A/B Testing
  - **Technical:** Python, SQL, R, FastAPI, AWS, Tableau, Looker
  - **AI:** Claude API, OpenAI, Prompt Engineering, GenAI Video/Text, HeyGen, MidJourney
  - **Leadership:** Cross-functional (Eng, Sales, Marketing, Legal, Finance), Coaching
- Download PDF button (link to a static PDF in `/static/`)

### Contact (`/contact`)

**Purpose:** Make it easy to reach you.

**Content:**
- Email (or contact form if you want — v2)
- LinkedIn link
- GitHub link
- Location: Greater Seattle Area
- Optional: Calendly embed for coffee chats

---

## Technical Architecture

### Application Structure

```
fullstackpm.tech/
├── code/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app, lifespan, error handlers
│   │   ├── config.py            # Pydantic settings
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── pages.py         # Home, About, Resume, Contact routes
│   │   │   ├── projects.py      # Project gallery + detail routes
│   │   │   └── blog.py          # Blog list, detail, tag, RSS routes
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── content.py       # Markdown parsing, frontmatter, caching
│   │   │   └── feed.py          # RSS feed generation
│   │   ├── templates/
│   │   │   ├── base.html        # Base layout (nav, footer, head)
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── projects/
│   │   │   │   ├── gallery.html
│   │   │   │   └── detail.html
│   │   │   ├── blog/
│   │   │   │   ├── list.html
│   │   │   │   ├── detail.html
│   │   │   │   └── tag.html
│   │   │   ├── resume.html
│   │   │   └── contact.html
│   │   └── static/
│   │       ├── css/
│   │       │   └── custom.css   # Minimal overrides (Tailwind does most work)
│   │       ├── img/
│   │       │   ├── headshot.jpg
│   │       │   └── projects/    # Project thumbnails
│   │       └── resume.pdf
│   ├── content/
│   │   ├── blog/                # Blog post markdown files
│   │   │   └── 2026-02-15-why-im-building-in-public.md
│   │   └── projects/            # Project detail markdown files
│   │       └── portfolio-site.md
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_pages.py
│   │   ├── test_projects.py
│   │   └── test_blog.py
│   ├── requirements.txt
│   ├── Procfile                 # For Render deployment
│   └── README.md
```

### Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | FastAPI | Matches all project tech stacks, async, great DX |
| Rendering | Server-side (Jinja2) | SEO, fast initial load, no JS dependency |
| Interactivity | HTMX | Progressive enhancement, no build step, tiny footprint |
| Styling | Tailwind CSS (CDN v1, build v2) | Rapid development, professional result |
| Content storage | Markdown on disk | Git-native, no database needed, easy to author |
| Caching | In-memory at startup | Fast reads, no external cache dependency |
| Database | None (v1) | No user accounts, no dynamic data, no unnecessary complexity |
| Deployment | Render free tier | Auto-deploy from GitHub, SSL, custom domain support |

### Content Service (Shared Across Blog + Projects)

A single `ContentService` class that:
- Scans markdown files from a directory on app startup
- Parses YAML frontmatter (title, date, tags, excerpt, status, tech_stack, etc.)
- Converts markdown to HTML (with syntax highlighting via Pygments)
- Calculates reading time
- Generates slugs from filenames
- Caches all parsed content in memory
- Provides filtering (by tag, by status) and pagination

This is an evolution of the `BlogService` already built in the PM Academy codebase.

---

## Design Direction

### Visual Identity

- **Color palette:** Dark navy/charcoal primary (#1a1a2e or similar), white text, accent color (electric blue or teal) for CTAs and highlights
- **Typography:** System font stack (clean, fast loading) — or Inter/JetBrains Mono from Google Fonts
- **Layout:** Clean, lots of whitespace, content-focused. No decorative elements.
- **Inspiration:** Minimal personal sites like leerob.io, brianlovin.com, paco.me — not corporate, not flashy

### Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Navigation collapses to hamburger menu on mobile
- Project cards stack to single column on mobile
- Blog posts full-width on mobile

### Dark Mode
- Support system preference via `prefers-color-scheme`
- Optional toggle in nav
- Tailwind's `dark:` classes make this straightforward

---

## HTMX Usage (Where It Adds Value)

Don't use HTMX everywhere — only where it genuinely improves UX:

1. **Project gallery filtering** — Click a tech stack tag → HTMX swaps the project grid without full page reload
2. **Blog tag filtering** — Same pattern as projects
3. **Blog pagination** — "Load more" button that appends posts via HTMX
4. **Contact form** (v2) — Submit without page reload, show success/error inline

Everything else is standard page navigation. HTMX should feel invisible — users shouldn't know it's there.

---

## SEO Strategy

### On-Page
- Semantic HTML5 (`<article>`, `<nav>`, `<main>`, `<section>`)
- Unique `<title>` and `<meta description>` per page
- Open Graph tags for social sharing (title, description, image)
- Clean URL structure (`/projects/marketplace-dashboard` not `/projects?id=2`)
- `<h1>` on every page, proper heading hierarchy

### Technical
- `sitemap.xml` generated dynamically from all pages + blog posts + projects
- `robots.txt` allowing all crawlers
- Fast load times (no JS framework, minimal CSS, server-rendered)
- Structured data (JSON-LD) for Person and BlogPosting schemas

### Keywords
- "full stack product manager"
- "ai product manager portfolio"
- "product manager who codes"
- "vibe coding pm"
- "[your name]" (personal brand)

---

## Content to Write for Launch

### Minimum viable content:

1. **Home page copy** — hero text, brief thesis statement
2. **About page** — full narrative (the 3 chapters)
3. **1 project entry** — the portfolio site itself (meta but effective)
4. **1 blog post** — "Why I'm Building in Public as a PM"
5. **Resume data** — experience timeline with key metrics

### Nice-to-have for launch:
- Headshot / professional photo
- Company logos for the experience timeline
- A project thumbnail/screenshot

---

## Development Phases

### Phase 1: Foundation (Day 1-2)
- [ ] FastAPI app scaffold with config
- [ ] Base template with Tailwind + nav + footer
- [ ] Home page (static content, no dynamic projects yet)
- [ ] About page
- [ ] Contact page

### Phase 2: Content Engine (Day 3-4)
- [ ] ContentService for markdown parsing (blog + projects)
- [ ] Blog list, detail, and tag pages
- [ ] Project gallery and detail pages
- [ ] RSS feed generation
- [ ] sitemap.xml and robots.txt

### Phase 3: Polish (Day 5-6)
- [ ] Resume / experience timeline page
- [ ] HTMX interactions (project filtering, blog pagination)
- [ ] Dark mode support
- [ ] Meta tags and Open Graph
- [ ] Responsive testing

### Phase 4: Content & Deploy (Day 7)
- [ ] Write initial content (about page, first blog post, first project entry)
- [ ] Deploy to Render with custom domain (fullstackpm.tech)
- [ ] Verify SSL, SEO, mobile rendering
- [ ] Push to GitHub with clean README

---

## Deployment

### Render Setup
1. Connect GitHub repo
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Environment: Python 3.11+
5. Custom domain: fullstackpm.tech
6. Auto-deploy on push to `main`

### Domain Setup
- Point fullstackpm.tech DNS to Render
- Render provides SSL automatically
- www redirect to apex domain (or vice versa)

---

## Next Step

Start building → Phase 1: Foundation.

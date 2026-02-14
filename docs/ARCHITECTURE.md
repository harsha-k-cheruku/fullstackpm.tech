# Architecture: fullstackpm.tech

## Overview

fullstackpm.tech is a Full Stack PM portfolio site that combines:
- **Portfolio** (your projects, writing, resume)
- **Working tools** (Interview Coach, Marketplace Analytics)
- **Public-facing service** (blog, projects, RSS, SEO)

Built with fastAPI backend + Jinja2 templating + Tailwind CSS + HTMX for real-time interactions.

---

## Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | FastAPI (Python) | Lightweight, async, auto-docs, great for rapid iteration |
| **Templates** | Jinja2 | Server-side rendering, SEO-friendly, no JS framework bloat |
| **Styling** | Tailwind CSS + custom CSS variables | Utility-first, dark mode support, consistent design tokens |
| **Interactivity** | HTMX | Real-time updates without JavaScript frameworks |
| **Content** | Markdown + YAML frontmatter | Version-controlled, easy to edit, content-as-code |
| **Data** | SQLite | Lightweight, file-based, perfect for side projects |
| **Deployment** | Render | Auto-deploys on GitHub push, handles scaling, cheap |

---

## Directory Structure

```
fullstackpm.tech/
├── code/                           ← FastAPI application (what Render deploys)
│   ├── app/
│   │   ├── main.py                 ← FastAPI app entrypoint
│   │   ├── config.py               ← Settings (OpenAI keys, database paths, etc.)
│   │   ├── database.py             ← SQLAlchemy setup
│   │   ├── routers/                ← API endpoints
│   │   │   ├── pages.py            ← Home, About, Contact pages
│   │   │   ├── blog.py             ← Blog routes + RSS
│   │   │   ├── projects.py         ← Projects gallery + filters
│   │   │   ├── interview_coach.py  ← Interview Coach tool
│   │   │   ├── marketplace.py      ← Marketplace Analytics tool
│   │   │   └── comments.py         ← Comment API for blog posts
│   │   ├── services/               ← Business logic
│   │   │   ├── content.py          ← ContentService (markdown parsing)
│   │   │   ├── interview_evaluator.py  ← AI evaluation logic
│   │   │   └── analytics.py        ← Marketplace analytics aggregations
│   │   ├── models/                 ← SQLAlchemy ORM models
│   │   │   ├── comment.py
│   │   │   ├── interview_session.py
│   │   │   └── __init__.py
│   │   ├── templates/              ← Jinja2 HTML templates
│   │   │   ├── base.html           ← Base layout + navbar
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── blog/
│   │   │   ├── projects/
│   │   │   ├── interview-coach/
│   │   │   ├── marketplace-analytics/
│   │   │   └── partials/           ← Reusable components
│   │   └── static/
│   │       ├── css/
│   │       │   └── custom.css      ← Design tokens + custom styles
│   │       ├── js/
│   │       │   ├── main.js         ← Dark mode toggle, mobile menu
│   │       │   └── charts.js       ← Chart.js initialization
│   │       └── fonts/
│   ├── requirements.txt            ← Python dependencies
│   └── tests/                      ← (Optional) Unit tests
│
├── content/                        ← Content files (version-controlled in Git)
│   ├── blog/
│   │   ├── 2026-02-09-birth-of-full-stack-pm.md
│   │   ├── 2026-02-15-how-i-built-fullstackpm-tech.md
│   │   └── ...
│   └── projects/
│       ├── portfolio-site.md
│       ├── pm-interview-coach.md
│       ├── marketplace-analytics.md
│       └── ...
│
├── project_ideas/                  ← Incubation folder for new project concepts
│   ├── README.md                   ← How to develop ideas
│   ├── 01_PM_TECH_COMPANION.md     ← Detailed concept docs
│   ├── 02_BOOK_MARKETING_GENERATOR.md
│   └── ...
│
├── docs/                           ← Developer documentation
│   ├── ARCHITECTURE.md             ← This file
│   ├── DEPLOYMENT.md               ← How Render deployment works
│   ├── DEVELOPMENT.md              ← Local setup and development
│   ├── CONTENT_STYLE_GUIDE.md      ← Writing style for blog/projects
│   └── TROUBLESHOOTING.md          ← Common issues and fixes
│
├── PROJECTS_STATUS.md              ← Live tracker of what's being built
├── SITE_UPDATE_FRAMEWORK.md        ← How to update the site (blog, projects, tools)
├── BUILD_*.md files                ← Project plans for Code Puppy
│   ├── BUILD_MARKETPLACE_ANALYTICS.md
│   ├── BUILD_BOOK_MARKETING_GENERATOR.md
│   └── ...
│
├── requirements.txt                ← Root-level Python dependencies (for Render)
├── asgi.py                         ← ASGI entry point for Render
├── Procfile                        ← Render deployment instructions
├── README.md                       ← Project overview
└── .github/                        ← GitHub workflows
    └── workflows/
```

---

## Data Models

### Content Service
Reads markdown files from `/content/` at startup:
```python
class Project:
    title: str
    slug: str
    description: str
    tech_stack: list[str]
    status: str  # "live", "in_progress", "planned"
    featured: bool
    display_order: int
    problem: str  # P/A/S cards
    approach: str
    solution: str
    content: str  # Rendered HTML from markdown

class BlogPost:
    title: str
    slug: str
    date: datetime
    tags: list[str]
    content: str  # Rendered HTML
    author: str
    excerpt: str
    reading_time: int
```

### Database Models (SQLite)
```python
class Comment:  # Blog post comments
    id: UUID
    blog_post_slug: str
    author_name: str
    content: str
    created_at: datetime

class InterviewSession:  # Practice sessions
    id: UUID
    user_id: str (optional, for future auth)
    created_at: datetime
    status: str

class InterviewAttempt:  # Individual question attempts
    id: UUID
    session_id: UUID
    question: str
    user_answer: str
    overall_score: float (1-10)
    framework_score: float
    structure_score: float
    completeness_score: float
    feedback: str
    created_at: datetime
```

---

## Request Flow

### Page Request (Blog Post)
```
User visits /blog/my-post
    ↓
Router (blog.py) receives request
    ↓
ContentService loads my-post.md from /content/blog/
    ↓
Parses YAML frontmatter + markdown content
    ↓
Renders template (blog/detail.html) with content
    ↓
Returns HTML to user
```

### Interactive Feature (Project Filter)
```
User clicks "Live" filter button
    ↓
HTMX sends GET /api/projects/filter?status=live
    ↓
projects.py route loads all projects
    ↓
Filters projects where status == "live"
    ↓
Renders project_grid.html partial
    ↓
HTMX swaps #project-grid with new content
    ↓
JavaScript updates filter button styles
```

### Tool Request (Interview Coach)
```
User submits answer
    ↓
HTMX sends POST /api/interview-coach/submit
    ↓
interview_coach.py receives answer
    ↓
Calls OpenAI API to evaluate (via interview_evaluator.py)
    ↓
Stores result in SQLite (InterviewAttempt)
    ↓
Returns scored feedback HTML
    ↓
HTMX renders feedback section
```

---

## Key Design Decisions

### Content as Code
- Blog posts and projects live in Git
- No CMS required (Git is the CMS)
- Version history built-in
- Easy to collaborate

### Markdown Rendering
- ContentService caches all markdown in RAM at startup
- No database queries needed to render pages
- Fast page load times
- Trade-off: Must restart server to see new content

### SQLite for Tools
- Comments, interview sessions stored separately
- Keep portfolio content simple (markdown only)
- Tools can have state without complicating content pipeline

### HTMX for Interactivity
- Real-time filtering, pagination without page reloads
- No JavaScript framework overhead
- Server-side rendering stays simple
- Progressive enhancement (works without JS)

### Design Tokens (CSS Variables)
- One source of truth for colors, typography
- Dark mode support without duplicate CSS
- Easy to rebrand (change variables in custom.css)
- Tailwind + custom tokens work together

---

## Performance Characteristics

| Feature | Latency | Notes |
|---------|---------|-------|
| Page load (blog) | <100ms | HTML cached, no DB queries |
| Project filter (HTMX) | 50-200ms | In-memory filtering, returns HTML partial |
| Interview submission | 2-5s | Calls OpenAI API (slowest part) |
| Comment post | 500ms | SQLite write + page re-render |
| RSS feed | <100ms | Generated from ContentService cache |

---

## Deployment Pipeline

See [DEPLOYMENT.md](./DEPLOYMENT.md) for details on how changes flow to production.

---

## Future Scaling

### Current Limits
- Works fine for: 1K blog posts, 100K daily users, 10K projects
- OpenAI API costs: ~$10/month (Interview Coach evaluations)
- Render costs: $10-30/month depending on traffic

### When to Extract Projects
See root [PROJECTS_STATUS.md](../PROJECTS_STATUS.md) for extraction timeline.

### When to Migrate Data
- Blog posts: Stay in markdown (version control is valuable)
- Comments: Move to PostgreSQL when >10K comments
- Interview sessions: Stay SQLite until >1M sessions
- Projects: Stay in markdown until you need real-time collaboration

---

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues.

---

## Questions?

- **How do I add a new blog post?** See [SITE_UPDATE_FRAMEWORK.md](../SITE_UPDATE_FRAMEWORK.md)
- **How do I deploy?** See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **How do I set up locally?** See [DEVELOPMENT.md](./DEVELOPMENT.md)

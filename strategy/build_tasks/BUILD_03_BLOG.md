# Project: fullstackpm.tech — Build Task 03: Blog System

## 1. Project Overview

You are building parts of a personal portfolio website for a Full Stack AI Product Manager.

- **Domain:** fullstackpm.tech
- **Purpose:** Portfolio showcasing projects, blog posts, and professional background
- **Owner:** Harsha Cheruku
- **Tagline:** "Engineering Mind. Design Obsession."

## 2. Tech Stack (Mandatory — Do Not Deviate)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | **FastAPI** (Python 3.11+) | All routes return Jinja2 templates |
| Templating | **Jinja2** | Server-side rendering, no client-side frameworks |
| Styling | **Tailwind CSS** (CDN for now) | Use utility classes only |
| Interactivity | **HTMX** (CDN) | For dynamic partial updates |
| Icons | **Heroicons** (inline SVG) | Outline style 24px |
| Fonts | **Geist Sans** + **JetBrains Mono** | Via Google Fonts CDN |
| Content | **Markdown files** with YAML frontmatter | Parsed at startup, cached in memory |
| Deployment | **Render** | Procfile included |

**Do NOT use:** React, Vue, Angular, Svelte, Next.js, npm/node, webpack, any JS framework, Bootstrap, SCSS/LESS.

## 3. Color System

The project uses CSS custom properties defined in `app/static/css/custom.css`. Here is the FULL color system:

```css
/* fullstackpm.tech — Design System Tokens */

:root {
  /* Backgrounds */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8FAFC;
  --color-bg-tertiary: #F1F5F9;

  /* Text */
  --color-text-primary: #0F172A;
  --color-text-secondary: #475569;
  --color-text-tertiary: #94A3B8;

  /* Borders */
  --color-border: #E2E8F0;
  --color-border-hover: #CBD5E1;

  /* Accent (Blue) */
  --color-accent: #2E8ECE;
  --color-accent-hover: #2577AD;
  --color-accent-light: #E8F4FB;
  --color-accent-dark: #1A3A52;

  /* Semantic */
  --color-success: #27AE60;
  --color-success-bg: #D5F5E3;
  --color-warning: #F1C40F;
  --color-warning-bg: #FEF9E7;
  --color-danger: #E74C3C;
  --color-danger-bg: #FADBD8;
  --color-info: #2E8ECE;
}

.dark {
  /* Backgrounds */
  --color-bg-primary: #030712;
  --color-bg-secondary: #0F172A;
  --color-bg-tertiary: #1E293B;

  /* Text */
  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-text-tertiary: #64748B;

  /* Borders */
  --color-border: #1E293B;
  --color-border-hover: #334155;

  /* Accent overrides for dark */
  --color-accent-light: #172554;

  /* Semantic overrides for dark */
  --color-success-bg: #052E16;
  --color-warning-bg: #422006;
  --color-danger-bg: #450A0A;
}
```

## 4. Coding Conventions

### Python
- Type hints on all function signatures
- Pydantic models for data schemas
- Async functions for route handlers
- File naming: lowercase with underscores
- Imports: stdlib first, then third-party, then local (blank line separated between each group)

### Example Import Order
```python
import math
from datetime import datetime
from pathlib import Path

import frontmatter
import markdown

from app.config import settings
```

### Templates
- Extend `base.html` using `{% extends "base.html" %}`
- Use `{% block content %}` for page content
- Reference CSS variables via inline `style=` attributes or Tailwind arbitrary values like `text-[var(--color-accent)]`
- All Heroicons are inline SVG, outline style, 24x24

## 5. The Task

Build the Blog system: router, 3 templates, and a sample blog post.

### What to Build

**1. Router: `app/routers/blog.py`**

Three routes:
- `GET /blog` — paginated blog list (10 posts per page, query param `?page=1`)
- `GET /blog/{slug}` — single blog post detail, 404 if not found
- `GET /blog/tag/{tag}` — blog posts filtered by tag, paginated

Access ContentService via `request.app.state.content_service`.

**2. Templates:**
- `app/templates/blog/list.html` — blog post list with pagination
- `app/templates/blog/detail.html` — rendered blog post with prose typography
- `app/templates/blog/tag.html` — filtered list (reuses same visual style as list.html with tag heading)

**3. Sample content:**
- `content/blog/2026-02-20-what-is-a-fullstack-pm.md`

**4. Router registration in `main.py`**

---

### ContentService API

The `ContentService` already exists at `app/services/content.py`. It is initialized during app startup and stored at `request.app.state.content_service`. You do NOT need to build or modify it. Here is its public API for reference:

```python
class ContentService:
    def get_posts(self, page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]:
        """Paginated blog posts (newest first). Returns (posts, total_count)."""

    def get_post_by_slug(self, slug: str) -> BlogPost | None:
        """Single post by slug."""

    def get_posts_by_tag(self, tag: str, page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]:
        """Posts filtered by tag, paginated."""

    def get_all_tags(self) -> list[str]:
        """All unique tags sorted alphabetically."""

class BlogPost:
    title: str
    slug: str
    date: datetime        # Python datetime
    tags: list[str]
    excerpt: str
    author: str
    reading_time: str     # e.g., "5 min read"
    html_content: str     # Rendered markdown HTML
```

---

### Blog List Layout (list.html)

- Page title with Heroicon (newspaper or document-text)
- Tag filter bar: show all tags as clickable badges, link to `/blog/tag/{tag}`
- Post list (NOT cards — clean list style with bottom border separator):
  - Each post: title (text-h3, links to `/blog/{slug}`, hover changes to accent color), date + reading time (text-small text-tertiary), excerpt (text-body text-secondary, 2-line clamp), tags (small badges linking to `/blog/tag/{tag}`)
  - Separator: `border-b border-[var(--color-border)] pb-6 mb-6`
- Pagination: "Newer" / "Older" links at bottom (only show if applicable)
- Empty state if no posts

### Blog Detail Layout (detail.html)

- Back link: "Back to Blog"
- Post header: title (text-h1), metadata row (date, reading time, author in text-small text-tertiary), tag badges
- Content: `<div class="prose max-w-3xl mx-auto">{{ post.html_content | safe }}</div>` (prose styles are in custom.css)
- Bottom: tag list, "Back to Blog" link

Format dates as "Feb 15, 2026" using Jinja2 filter: `{{ post.date.strftime('%b %d, %Y') }}`

### Blog Tag Layout (tag.html)

- Same as list.html but with heading: "Posts tagged: {tag}"
- Back link to /blog
- Same post list format

---

### Sample Blog Post

`content/blog/2026-02-20-what-is-a-fullstack-pm.md`:

Frontmatter:
```yaml
---
title: "What Is a Full Stack PM?"
date: 2026-02-20
tags: [product-management, ai, career]
excerpt: "The next generation of great product managers won't just manage — they'll build."
author: "Harsha Cheruku"
---
```

Write approximately 300 words of content including an h2 heading, a blockquote, a code block, and a bulleted list.

---

### Existing Codebase Reference (FULL files inline)

These files already exist. Read them carefully to match patterns, styles, and conventions.

#### `app/routers/pages.py` (existing — follow the `_ctx` pattern)

```python
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def _ctx(request: Request, **kwargs) -> dict:
    """Build the standard template context."""
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "home.html",
        _ctx(request, title="Harsha Cheruku — Full Stack AI PM", current_page="/"),
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "about.html",
        _ctx(request, title="About — fullstackpm.tech", current_page="/about"),
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "contact.html",
        _ctx(request, title="Contact — fullstackpm.tech", current_page="/contact"),
    )
```

#### `app/main.py` (existing — you will update this to register the blog router)

```python
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.routers import pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load content, cache, etc.
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

# Include routers
app.include_router(pages.router)

# Templates
templates = Jinja2Templates(directory=str(settings.templates_dir))


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> HTMLResponse:
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "title": "Page Not Found", "config": settings, "current_page": "", "year": datetime.now().year},
        status_code=404,
    )
```

#### `app/templates/base.html` (existing — extend this for all templates)

```html
<!DOCTYPE html>
<html lang="en" class="">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}{{ title | default("fullstackpm.tech") }}{% endblock %}</title>
  <meta name="description" content="{% block description %}{{ meta_description | default("Portfolio of Harsha Cheruku — Full Stack AI Product Manager") }}{% endblock %}">
  <meta name="author" content="Harsha Cheruku">

  <!-- Open Graph -->
  <meta property="og:title" content="{% block og_title %}{{ title | default("fullstackpm.tech") }}{% endblock %}">
  <meta property="og:description" content="{% block og_description %}{{ meta_description | default("Portfolio of Harsha Cheruku — Full Stack AI Product Manager") }}{% endblock %}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{ config.site_url }}{{ request.url.path }}">

  <!-- Fonts: Geist Sans + JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <!-- Tailwind CSS (CDN) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Geist Sans', 'system-ui', '-apple-system', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
        },
      },
    }
  </script>

  <!-- Design System Tokens -->
  <link rel="stylesheet" href="/static/css/custom.css">

  <!-- Dark mode: apply before paint to prevent flash -->
  <script>
    (function() {
      var theme = localStorage.getItem('theme');
      if (!theme) {
        theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      }
    })();
  </script>

  {% block head %}{% endblock %}
</head>
<body class="min-h-screen font-sans antialiased"
      style="background-color: var(--color-bg-primary); color: var(--color-text-primary);">

  <!-- Navigation -->
  {% include "partials/navbar.html" %}

  <!-- Main content -->
  <main class="mx-auto max-w-[1200px] px-4 sm:px-6">
    {% block content %}{% endblock %}
  </main>

  <!-- Footer -->
  {% include "partials/footer.html" %}

  <!-- HTMX (CDN) -->
  <script src="https://unpkg.com/htmx.org@2.0.2" integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwCXuE+cDVtAu2B3crQxD" crossorigin="anonymous"></script>

  <!-- Site JS -->
  <script src="/static/js/main.js"></script>

  {% block scripts %}{% endblock %}
</body>
</html>
```

#### `app/static/css/custom.css` (existing — includes prose styles for rendered markdown)

```css
/* fullstackpm.tech — Design System Tokens */

:root {
  /* Backgrounds */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8FAFC;
  --color-bg-tertiary: #F1F5F9;

  /* Text */
  --color-text-primary: #0F172A;
  --color-text-secondary: #475569;
  --color-text-tertiary: #94A3B8;

  /* Borders */
  --color-border: #E2E8F0;
  --color-border-hover: #CBD5E1;

  /* Accent (Blue) */
  --color-accent: #2E8ECE;
  --color-accent-hover: #2577AD;
  --color-accent-light: #E8F4FB;
  --color-accent-dark: #1A3A52;

  /* Semantic */
  --color-success: #27AE60;
  --color-success-bg: #D5F5E3;
  --color-warning: #F1C40F;
  --color-warning-bg: #FEF9E7;
  --color-danger: #E74C3C;
  --color-danger-bg: #FADBD8;
  --color-info: #2E8ECE;
}

.dark {
  /* Backgrounds */
  --color-bg-primary: #030712;
  --color-bg-secondary: #0F172A;
  --color-bg-tertiary: #1E293B;

  /* Text */
  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-text-tertiary: #64748B;

  /* Borders */
  --color-border: #1E293B;
  --color-border-hover: #334155;

  /* Accent overrides for dark */
  --color-accent-light: #172554;

  /* Semantic overrides for dark */
  --color-success-bg: #052E16;
  --color-warning-bg: #422006;
  --color-danger-bg: #450A0A;
}

/* Typography scale */
.text-display {
  font-size: 3.5rem;
  line-height: 1.05;
  font-weight: 700;
  letter-spacing: -0.04em;
}

.text-h1 {
  font-size: 2.5rem;
  line-height: 1.1;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.text-h2 {
  font-size: 1.75rem;
  line-height: 1.2;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.text-h3 {
  font-size: 1.375rem;
  line-height: 1.25;
  font-weight: 600;
  letter-spacing: -0.015em;
}

.text-h4 {
  font-size: 1.125rem;
  line-height: 1.3;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.text-body-lg {
  font-size: 1.125rem;
  line-height: 1.55;
}

.text-body {
  font-size: 1rem;
  line-height: 1.55;
}

.text-small {
  font-size: 0.875rem;
  line-height: 1.4;
  letter-spacing: 0.01em;
}

.text-xs {
  font-size: 0.75rem;
  line-height: 1.4;
  letter-spacing: 0.02em;
}

/* Prose styling for rendered markdown */
.prose h2 {
  font-size: 1.75rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-top: 3rem;
  margin-bottom: 1rem;
  color: var(--color-text-primary);
}

.prose h3 {
  font-size: 1.375rem;
  font-weight: 600;
  letter-spacing: -0.015em;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
}

.prose p {
  margin-bottom: 1rem;
  line-height: 1.55;
  color: var(--color-text-secondary);
}

.prose a {
  color: var(--color-accent);
}

.prose a:hover {
  text-decoration: underline;
}

.prose ul,
.prose ol {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
  color: var(--color-text-secondary);
}

.prose li {
  margin-bottom: 0.25rem;
}

.prose blockquote {
  border-left: 4px solid var(--color-accent);
  padding-left: 1rem;
  font-style: italic;
  color: var(--color-text-secondary);
  margin-bottom: 1rem;
}

.prose code {
  background-color: var(--color-bg-tertiary);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-family: 'JetBrains Mono', monospace;
}

.prose pre {
  background-color: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  padding: 1rem;
  overflow-x: auto;
  margin-bottom: 1.5rem;
}

.prose pre code {
  background: none;
  padding: 0;
  border-radius: 0;
  font-size: 0.875rem;
}

.prose img {
  border-radius: 0.5rem;
  max-width: 100%;
  margin: 1.5rem 0;
}

.prose table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.prose th,
.prose td {
  border: 1px solid var(--color-border);
  padding: 0.5rem 0.75rem;
  text-align: left;
}

.prose th {
  background-color: var(--color-bg-secondary);
  font-weight: 600;
}

.prose tr:nth-child(even) {
  background-color: var(--color-bg-secondary);
}

/* Line clamp utility */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Transitions */
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-duration: 150ms;
  transition-timing-function: ease-in-out;
}
```

#### `app/config.py` (existing — use `settings` for template context)

```python
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fullstackpm.tech"
    debug: bool = False
    base_dir: Path = Path(__file__).resolve().parent.parent
    content_dir: Path = base_dir / "content"
    templates_dir: Path = base_dir / "app" / "templates"
    static_dir: Path = base_dir / "app" / "static"

    # Site metadata
    site_title: str = "fullstackpm.tech"
    site_description: str = "Portfolio of Harsha Cheruku — Full Stack AI Product Manager"
    site_author: str = "Harsha Cheruku"
    site_url: str = "https://fullstackpm.tech"

    # Social links
    github_url: str = "https://github.com/hcheruku"
    linkedin_url: str = "https://linkedin.com/in/hcheruku"
    rss_url: str = "/feed.xml"

    class Config:
        env_file = ".env"


settings = Settings()
```

---

### Scope Boundaries

- **IN scope:** `app/routers/blog.py`, `app/templates/blog/list.html`, `app/templates/blog/detail.html`, `app/templates/blog/tag.html`, `content/blog/2026-02-20-what-is-a-fullstack-pm.md`, updated `app/main.py`
- **OUT of scope:** RSS feed (Task 5), HTMX pagination (Task 6), projects pages, ContentService itself (already built)

---

## 6. Expected Output

Return these COMPLETE files:

1. `app/routers/blog.py` — Blog router with 3 routes
2. `app/templates/blog/list.html` — Blog list page with tag bar and pagination
3. `app/templates/blog/detail.html` — Single blog post page with prose rendering
4. `app/templates/blog/tag.html` — Tag-filtered blog list page
5. `content/blog/2026-02-20-what-is-a-fullstack-pm.md` — Sample blog post
6. Updated `app/main.py` — With blog router registered

### Output Rules

- Return COMPLETE files, not snippets or diffs
- Include the file path as a comment at the top of each Python file
- Do not add features beyond what was specified
- Do not refactor existing code unless the task asks for it
- Every route handler must have type hints on all parameters and return types
- Follow the exact `_ctx` pattern from `pages.py` for building template context
- All templates must extend `base.html`
- Use CSS variables (not hardcoded colors) for ALL colors in templates
- Use the typography classes from `custom.css` (text-h1, text-h3, text-body, text-small, etc.)
- Heroicons must be inline SVG, outline style, 24x24
- Date format: `{{ post.date.strftime('%b %d, %Y') }}` (renders as "Feb 20, 2026")

## 7. Current Project Structure

```
fullstackpm.tech/
├── strategy/              # Planning docs (DO NOT modify)
├── code/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # UPDATE: add blog router import + registration
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── pages.py      # Routes: /, /about, /contact (DO NOT modify)
│   │   │   └── blog.py       # CREATE: blog routes
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── content.py    # Already exists (DO NOT modify)
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── 404.html
│   │   │   ├── projects/          # Empty (not this task)
│   │   │   ├── blog/
│   │   │   │   ├── list.html      # CREATE
│   │   │   │   ├── detail.html    # CREATE
│   │   │   │   └── tag.html       # CREATE
│   │   │   └── partials/
│   │   │       ├── navbar.html
│   │   │       └── footer.html
│   │   └── static/
│   │       ├── css/custom.css     # DO NOT modify
│   │       ├── js/main.js
│   │       └── img/
│   ├── content/
│   │   ├── blog/
│   │   │   ├── 2026-02-15-why-im-building-in-public.md   # Already exists
│   │   │   └── 2026-02-20-what-is-a-fullstack-pm.md      # CREATE
│   │   └── projects/
│   │       └── portfolio-site.md  # Already exists
│   ├── tests/
│   ├── requirements.txt
│   └── Procfile
```

All file paths in your output are **relative to `code/`**. For example, the blog router goes at `code/app/routers/blog.py` on disk but the import path is `app.routers.blog`.

## 8. Acceptance Test

After implementing, verify all of the following:

### Test 1: Server Starts Without Errors
```bash
cd code && python3 -m uvicorn app.main:app --reload --port 8001
```
The server should start cleanly with no import errors or exceptions.

### Test 2: Blog List Page Renders
Navigate to `http://localhost:8001/blog` in a browser.

Expected:
- Page title with a Heroicon is visible
- Tag filter bar shows clickable tag badges (product-management, ai, career, building-in-public, etc.)
- At least 2 blog posts are listed (the existing sample + the new one)
- Each post shows: title (clickable link), date formatted as "Feb 20, 2026", reading time, excerpt (clamped to 2 lines), tag badges
- Posts are separated by a bottom border (not cards)
- Dark mode toggle works and all text/backgrounds update correctly

### Test 3: Blog Detail Page Renders
Click on a blog post title from the list, or navigate to `http://localhost:8001/blog/what-is-a-fullstack-pm`.

Expected:
- "Back to Blog" link at the top
- Post title in text-h1 styling
- Metadata row: date, reading time, author (text-small, text-tertiary color)
- Tag badges displayed
- Rendered markdown content inside a `.prose` container with proper styling:
  - h2 headings styled
  - Blockquote with left accent border
  - Code block with monospace font and background
  - Bulleted list properly indented
- "Back to Blog" link at the bottom
- Dark mode works correctly

### Test 4: Blog Tag Page Renders
Click a tag badge from the list or detail page, or navigate to `http://localhost:8001/blog/tag/ai`.

Expected:
- Heading shows "Posts tagged: ai"
- "Back to Blog" link visible
- Only posts with the "ai" tag are listed
- Same visual style as the main blog list (borders, not cards)
- Pagination works if there are more than 10 posts with the tag
- Dark mode works correctly

### Test 5: Date Formatting
On all pages where dates appear, verify the format is "Feb 20, 2026" (abbreviated month, zero-padded day, four-digit year).

### Test 6: Excerpt Clamping
On the blog list and tag pages, verify that long excerpts are clamped to 2 lines with overflow hidden (the `line-clamp-2` CSS class).

### Test 7: 404 for Missing Slugs
Navigate to `http://localhost:8001/blog/nonexistent-slug`.

Expected: The site's 404 page is returned (not a server error).

### Test 8: Pagination
If there are enough posts, verify that:
- The "Older" link appears when there are more posts beyond the current page
- The "Newer" link appears on page 2+
- Links include the `?page=` query parameter
- Page 1 does not show a "Newer" link
- The last page does not show an "Older" link

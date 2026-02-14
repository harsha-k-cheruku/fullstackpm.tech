# Project: fullstackpm.tech — Build Task 05: RSS Feed + Sitemap + Robots.txt

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

## 3. Color System (Mandatory — Use These Exact Values)

### CSS Custom Properties

All colors are defined in `app/static/css/custom.css`. Here is the FULL color system — use these exact values via `var()` references, never hardcode hex values in templates:

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

### Python (Backend)
- Use type hints on all function signatures
- Use Pydantic models for request/response schemas
- Use async functions for route handlers
- File naming: lowercase with underscores (e.g., `feed.py`)
- Imports: stdlib first, then third-party, then local (separated by blank lines)
- No unused imports, no commented-out code

### Example Import Order
```python
import math
from datetime import datetime
from pathlib import Path

import frontmatter
import markdown

from app.config import settings
```

## 5. The Task

Build three SEO/infrastructure routes that return XML or plain text responses (no HTML templates needed): an RSS feed, an XML sitemap, and a robots.txt file.

### What to Build

#### 1. RSS Feed Service: `app/services/feed.py`

Create a service that generates RSS 2.0 XML from blog posts using Python's built-in `xml.etree.ElementTree` module. Do NOT add any new dependencies.

**Requirements:**
- Generate valid RSS 2.0 XML
- Channel metadata:
  - `<title>` — use `settings.site_title` (value: `"fullstackpm.tech"`)
  - `<link>` — use `settings.site_url` (value: `"https://fullstackpm.tech"`)
  - `<description>` — use `settings.site_description` (value: `"Portfolio of Harsha Cheruku — Full Stack AI Product Manager"`)
  - `<language>` — `"en-us"`
- Each blog post becomes an `<item>` with:
  - `<title>` — the post title
  - `<link>` — `{site_url}/blog/{slug}`
  - `<description>` — the post excerpt
  - `<pubDate>` — the post date formatted in RFC 822 format (e.g., `"Sat, 15 Feb 2026 00:00:00 +0000"`)
  - `<guid isPermaLink="true">` — same as `<link>`

**Service interface:**
```python
class FeedService:
    def __init__(self, site_url: str, site_title: str, site_description: str) -> None:
        ...

    def generate_rss(self, posts: list) -> str:
        """Generate RSS 2.0 XML string from a list of BlogPost objects."""
        ...
```

**RFC 822 date formatting:**
```python
from email.utils import format_datetime
from datetime import datetime, timezone

# Convert a date to RFC 822:
dt = datetime(2026, 2, 15, tzinfo=timezone.utc)
rfc822_date = format_datetime(dt)
# Result: "Sat, 15 Feb 2026 00:00:00 +0000"
```

Note: BlogPost.date is a `datetime` object. If it is a naive datetime (no timezone info), attach UTC before formatting.

#### 2. Sitemap Route

Generate a valid XML sitemap listing all discoverable pages on the site.

**Static pages to include:**
- `/`
- `/about`
- `/contact`
- `/resume`
- `/projects`
- `/blog`

**Dynamic pages:**
- `/projects/{slug}` for each project from `content_service.get_projects()`
- `/blog/{slug}` for each blog post from `content_service.get_posts()`
- `/blog/tag/{tag}` for each tag from `content_service.get_all_tags()`

**Each `<url>` entry must have:**
- `<loc>` — the full URL (e.g., `https://fullstackpm.tech/about`)
- `<lastmod>` — today's date in `YYYY-MM-DD` format
- `<changefreq>` — frequency string (see table below)
- `<priority>` — priority value (see table below)

**Priority and frequency table:**

| Page | changefreq | priority |
|------|-----------|----------|
| `/` (home) | `daily` | `1.0` |
| `/about` | `monthly` | `0.7` |
| `/contact` | `monthly` | `0.5` |
| `/resume` | `monthly` | `0.7` |
| `/projects` | `weekly` | `0.8` |
| `/blog` | `daily` | `0.9` |
| `/projects/{slug}` | `monthly` | `0.6` |
| `/blog/{slug}` | `monthly` | `0.7` |
| `/blog/tag/{tag}` | `weekly` | `0.5` |

**Sitemap XML format:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://fullstackpm.tech/</loc>
    <lastmod>2026-02-12</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- more <url> entries -->
</urlset>
```

#### 3. Robots.txt Route

Return a simple plain text response with the following content:

```
User-agent: *
Allow: /
Sitemap: https://fullstackpm.tech/sitemap.xml
```

The `Sitemap` URL must use `settings.site_url` (not hardcoded).

#### 4. Router: `app/routers/seo.py`

Create a new router file with all three routes:

| Route | Method | Response Type | Description |
|-------|--------|--------------|-------------|
| `GET /feed.xml` | GET | `application/xml` | RSS 2.0 feed |
| `GET /sitemap.xml` | GET | `application/xml` | XML sitemap |
| `GET /robots.txt` | GET | `text/plain` | Robots.txt |

Each route handler should:
1. Access the ContentService via `request.app.state.content_service`
2. Generate the appropriate content
3. Return a `Response` object with the correct `media_type`

**Route implementation pattern:**
```python
from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.config import settings
from app.services.feed import FeedService

router = APIRouter()


@router.get("/feed.xml")
async def rss_feed(request: Request) -> Response:
    content_service = request.app.state.content_service
    posts, _ = content_service.get_posts(page=1, per_page=100)
    feed_service = FeedService(
        site_url=settings.site_url,
        site_title=settings.site_title,
        site_description=settings.site_description,
    )
    xml_content = feed_service.generate_rss(posts)
    return Response(content=xml_content, media_type="application/xml")
```

#### 5. Register Router in main.py

Add `from app.routers import seo` and `app.include_router(seo.router)` to the existing `main.py`, following the same pattern used for `pages.router`.

### ContentService API (Already Built — Task 1)

The ContentService is initialized in the FastAPI lifespan and stored on `request.app.state.content_service`. Here are the methods you need:

```python
content_service.get_posts(page=1, per_page=100)  # Returns (list[BlogPost], total_count)
content_service.get_projects()                     # Returns list[Project]
content_service.get_all_tags()                     # Returns list[str]
```

**BlogPost model fields:**
```python
title: str          # e.g., "Why I'm Building in Public"
slug: str           # e.g., "why-im-building-in-public"
date: datetime      # e.g., datetime(2026, 2, 15)
excerpt: str        # e.g., "A short summary of the post."
tags: list[str]     # e.g., ["ai", "building-in-public"]
html_content: str   # Rendered HTML from markdown
```

**Project model fields:**
```python
title: str          # e.g., "Portfolio Site"
slug: str           # e.g., "portfolio-site"
description: str    # One-line description
status: str         # "live" | "in_progress" | "case_study" | "planned"
```

### Existing Files (Inline Reference)

#### File: `app/config.py` (DO NOT MODIFY — read values from this)

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

#### File: `app/main.py` (YOU WILL MODIFY — add seo router import and registration)

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

**How to modify main.py:**
1. Add `from app.routers import seo` alongside the existing `from app.routers import pages` import
2. Add `app.include_router(seo.router)` after the existing `app.include_router(pages.router)` line
3. Do NOT change anything else in main.py

**Note:** The lifespan may already have ContentService initialization from Task 1. If so, leave it as-is. If not (if the lifespan is still the empty placeholder shown above), the SEO routes will fail at runtime until Task 1 is also completed. This is expected — Task 5 depends on Task 1.

### Available Libraries (already in requirements.txt)

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
jinja2==3.1.4
python-multipart==0.0.9
python-frontmatter==1.1.0
markdown==3.7
pygments==2.18.0
pydantic-settings==2.11.0
```

Do NOT add any libraries beyond what is listed above. The RSS feed generation uses only Python's built-in `xml.etree.ElementTree` and `email.utils` modules.

### Scope Boundaries

- **IN scope:** `app/services/feed.py` (new), `app/routers/seo.py` (new), updated `app/main.py` (add router import and registration)
- **OUT of scope:** Templates, UI, HTML pages, blog/project detail pages, ContentService changes, custom.css, base.html, any frontend code

No CSS or HTML is needed for this task — all three routes return XML or plain text responses, not rendered templates.

## 6. Expected Output

Return these COMPLETE files:

1. **New `app/services/feed.py`** — The FeedService class that generates RSS 2.0 XML
2. **New `app/routers/seo.py`** — Router with `/feed.xml`, `/sitemap.xml`, and `/robots.txt` routes
3. **Updated `app/main.py`** — The existing file with the seo router added (import + include_router)

### Output Rules

- Return COMPLETE files, not snippets or diffs
- Include the file path as a comment at the top of each Python file
- Do not add features beyond what was specified
- Do not refactor existing code unless the task asks for it
- Every function must have type hints on all parameters and return types
- Use only Python built-in modules for XML generation (`xml.etree.ElementTree`, `email.utils`)
- The RSS feed must be valid RSS 2.0 XML
- The sitemap must be valid XML following the sitemaps.org schema
- Robots.txt must be plain text, not XML

## 7. Current Project Structure

```
fullstackpm.tech/
├── strategy/              # Planning docs (DO NOT modify)
│   ├── 00_MASTER_PLAN.md
│   ├── 01_PORTFOLIO_SITE.md
│   ├── ...
│   ├── 09_DESIGN_SYSTEM.md
│   ├── 10_COMPONENT_SPECS.md
│   ├── 11_LLM_EVAL_RUBRIC.md
│   └── 12_BUILD_INSTRUCTIONS.md
├── code/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # YOU MODIFY THIS (add seo router)
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── pages.py         # Routes: /, /about, /contact
│   │   │   └── seo.py           # YOU CREATE THIS
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── content.py       # ContentService (from Task 1)
│   │   │   └── feed.py          # YOU CREATE THIS
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── 404.html
│   │   │   ├── projects/
│   │   │   │   ├── gallery.html   # (from Task 2)
│   │   │   │   └── detail.html    # (from Task 2)
│   │   │   ├── blog/
│   │   │   │   ├── list.html      # (from Task 3)
│   │   │   │   ├── detail.html    # (from Task 3)
│   │   │   │   └── tag.html       # (from Task 3)
│   │   │   └── partials/
│   │   │       ├── navbar.html
│   │   │       └── footer.html
│   │   └── static/
│   │       ├── css/custom.css
│   │       ├── js/main.js
│   │       └── img/
│   ├── content/
│   │   ├── blog/
│   │   │   └── 2026-02-15-why-im-building-in-public.md  # (from Task 1)
│   │   └── projects/
│   │       └── portfolio-site.md                          # (from Task 1)
│   ├── tests/
│   ├── requirements.txt
│   └── Procfile
```

All file paths in your output are **relative to `code/`**. For example, the feed service file goes at `code/app/services/feed.py` on disk but the import path is `app.services.feed`.

## 8. Acceptance Test

After implementing, verify all of the following:

### Test 1: Server Starts Without Errors
```bash
cd code && python3 -m uvicorn app.main:app --reload --port 8001
```
The server should start cleanly with no import errors or exceptions.

### Test 2: RSS Feed Returns Valid XML
```bash
curl -s http://localhost:8001/feed.xml | head -20
```
Expected output (structure):
```xml
<?xml version='1.0' encoding='utf-8'?>
<rss version="2.0">
  <channel>
    <title>fullstackpm.tech</title>
    <link>https://fullstackpm.tech</link>
    <description>Portfolio of Harsha Cheruku — Full Stack AI Product Manager</description>
    <language>en-us</language>
    <item>
      <title>Why I'm Building in Public</title>
      <link>https://fullstackpm.tech/blog/why-im-building-in-public</link>
      <description>A short summary of the post.</description>
      <pubDate>Sat, 15 Feb 2026 00:00:00 +0000</pubDate>
      <guid isPermaLink="true">https://fullstackpm.tech/blog/why-im-building-in-public</guid>
    </item>
  </channel>
</rss>
```

### Test 3: RSS Feed Has Correct Content-Type
```bash
curl -sI http://localhost:8001/feed.xml | grep content-type
```
Expected: `content-type: application/xml`

### Test 4: Sitemap Returns Valid XML with All URLs
```bash
curl -s http://localhost:8001/sitemap.xml
```
Expected: Valid XML with `<urlset>` containing `<url>` entries for:
- Static pages: `/`, `/about`, `/contact`, `/resume`, `/projects`, `/blog`
- Dynamic pages: `/projects/portfolio-site`, `/blog/why-im-building-in-public`
- Tag pages: `/blog/tag/ai`, `/blog/tag/building-in-public`, etc.

Each `<url>` should contain `<loc>`, `<lastmod>`, `<changefreq>`, and `<priority>`.

### Test 5: Sitemap Has Correct Content-Type
```bash
curl -sI http://localhost:8001/sitemap.xml | grep content-type
```
Expected: `content-type: application/xml`

### Test 6: Robots.txt Returns Correct Text
```bash
curl -s http://localhost:8001/robots.txt
```
Expected:
```
User-agent: *
Allow: /
Sitemap: https://fullstackpm.tech/sitemap.xml
```

### Test 7: Robots.txt Has Correct Content-Type
```bash
curl -sI http://localhost:8001/robots.txt | grep content-type
```
Expected: `content-type: text/plain; charset=utf-8`

### Test 8: All Routes Return 200 Status
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/feed.xml
curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/sitemap.xml
curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/robots.txt
```
Expected: `200` for all three.

### Test 9: Sitemap URLs Use Full Domain
```bash
curl -s http://localhost:8001/sitemap.xml | grep "<loc>"
```
Every `<loc>` value should start with `https://fullstackpm.tech/` — no relative URLs.

### Test 10: RSS Feed Items Are Ordered Newest First
```bash
curl -s http://localhost:8001/feed.xml | grep "<title>"
```
Blog post titles should appear in reverse chronological order (newest post first), matching the order returned by `content_service.get_posts()`.

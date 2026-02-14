# Project: fullstackpm.tech — Build Task 01: Content Service

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

## 5. The Task

Build the `ContentService` class — the shared content engine that parses markdown files with YAML frontmatter for both blog posts and project pages.

### What to Build

A Python class `ContentService` in `app/services/content.py` that:

1. **Scans markdown files** from `content/blog/` and `content/projects/` directories on app startup
2. **Parses YAML frontmatter** using `python-frontmatter` library (already in requirements.txt)
3. **Converts markdown to HTML** using `markdown` library with `fenced_code` and `codehilite` extensions (Pygments for syntax highlighting)
4. **Calculates reading time** based on word count (~200 words/min)
5. **Generates slugs** from filenames: `2026-02-15-why-im-building-in-public.md` → slug: `why-im-building-in-public`
6. **Caches all parsed content** in memory (list of dataclass/Pydantic objects)
7. **Provides methods:**
   - `get_posts(page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]` — paginated blog posts (newest first), returns (posts, total_count)
   - `get_post_by_slug(slug: str) -> BlogPost | None`
   - `get_posts_by_tag(tag: str, page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]`
   - `get_all_tags() -> list[str]` — all unique tags sorted alphabetically
   - `get_projects() -> list[Project]` — all projects sorted by display_order or date
   - `get_project_by_slug(slug: str) -> Project | None`
   - `get_featured_projects(limit: int = 3) -> list[Project]` — projects marked as featured

### Data Models

**BlogPost:**
```python
title: str
slug: str
date: datetime
tags: list[str]
excerpt: str
author: str
reading_time: str       # e.g., "5 min read"
html_content: str       # Rendered markdown HTML
```

**Project:**
```python
title: str
slug: str
description: str        # One-line description
tech_stack: list[str]
status: str             # "live" | "in_progress" | "case_study" | "planned"
featured: bool
display_order: int
html_content: str
```

### Blog Frontmatter Schema

Blog markdown files live in `content/blog/` and use this frontmatter format:

```yaml
---
title: "Post Title"
date: 2026-02-15
tags: [ai, building-in-public, product-management]
excerpt: "A short summary of the post."
author: "Harsha Cheruku"
---
```

### Project Frontmatter Schema

Project markdown files live in `content/projects/` and use this frontmatter format:

```yaml
---
title: "Project Name"
description: "One-line description"
tech_stack: [FastAPI, Claude API, HTMX, Tailwind CSS]
status: "in_progress"
featured: true
display_order: 1
github_url: "https://github.com/harsha-k-cheruku"
live_url: ""
---
```

### Sample Content Files to Create

1. `content/blog/2026-02-15-why-im-building-in-public.md` — A sample blog post (~300 words) about building in public as a PM. Include a code block, a blockquote, and some links to test prose rendering.

2. `content/projects/portfolio-site.md` — A sample project entry for the portfolio site itself. Include the Problem, Approach, Solution, and Technical Details sections.

### Integration with main.py

The ContentService must be initialized in the FastAPI lifespan and made available to routers. Here is the CURRENT `main.py`:

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

app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(pages.router)

templates = Jinja2Templates(directory=str(settings.templates_dir))


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> HTMLResponse:
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "title": "Page Not Found", "config": settings, "current_page": "", "year": datetime.now().year},
        status_code=404,
    )
```

Modify the lifespan to instantiate `ContentService`, load content, and store it on `app.state` so routers can access it via `request.app.state.content_service`.

### Here is the CURRENT `config.py`:

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

    site_title: str = "fullstackpm.tech"
    site_description: str = "Portfolio of Harsha Cheruku — Full Stack AI Product Manager"
    site_author: str = "Harsha Cheruku"
    site_url: str = "https://fullstackpm.tech"

    github_url: str = "https://github.com/hcheruku"
    linkedin_url: str = "https://linkedin.com/in/hcheruku"
    rss_url: str = "/feed.xml"

    class Config:
        env_file = ".env"


settings = Settings()
```

### Available Libraries (already in requirements.txt):

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

Do NOT add any libraries beyond what is listed above. Everything you need is already available.

### Scope Boundaries

- **IN scope:** ContentService class, data models, 2 sample markdown files, main.py lifespan update
- **OUT of scope:** Templates, routes, UI, any frontend code — do not create or modify these

## 6. Expected Output

Return these COMPLETE files:

1. `app/services/content.py` — The ContentService class with all methods
2. `content/blog/2026-02-15-why-im-building-in-public.md` — Sample blog post
3. `content/projects/portfolio-site.md` — Sample project entry
4. Updated `app/main.py` — With lifespan loading ContentService

### Output Rules

- Return COMPLETE files, not snippets or diffs
- Include the file path as a comment at the top of each file (for Python files) or as the first line of a markdown heading (for .md files)
- Do not add features beyond what was specified
- Do not refactor existing code unless the task asks for it
- Every method in ContentService must have type hints on all parameters and return types
- Use Pydantic `BaseModel` (not dataclasses) for BlogPost and Project models

## 7. Current Project Structure

```
fullstackpm.tech/
├── strategy/              # Planning docs (DO NOT modify)
├── code/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── pages.py         # Routes: /, /about, /contact
│   │   ├── services/
│   │   │   └── __init__.py      # Empty — you are building content.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── 404.html
│   │   │   ├── projects/        # Empty
│   │   │   ├── blog/            # Empty
│   │   │   └── partials/
│   │   │       ├── navbar.html
│   │   │       └── footer.html
│   │   └── static/
│   │       ├── css/custom.css
│   │       ├── js/main.js
│   │       └── img/
│   ├── content/
│   │   ├── blog/                # Empty — you create sample post here
│   │   └── projects/            # Empty — you create sample project here
│   ├── tests/
│   ├── requirements.txt
│   └── Procfile
```

All file paths in your output are **relative to `code/`**. For example, when you create the ContentService, the file goes at `code/app/services/content.py` on disk but the import path is `app.services.content`.

## 8. Acceptance Test

After implementing, verify all of the following:

### Test 1: Server Starts Without Errors
```bash
cd code && python3 -m uvicorn app.main:app --reload --port 8001
```
The server should start cleanly with no import errors or exceptions. You should see log output confirming content was loaded.

### Test 2: ContentService Loads Content Correctly
```bash
cd code && python3 -c "
from app.services.content import ContentService
cs = ContentService('content')
cs.load()
posts, total = cs.get_posts()
print(f'{total} posts')
print(f'{len(cs.get_projects())} projects')
"
```
Expected output:
```
1 posts
1 projects
```

### Test 3: Blog Post Retrieval by Slug
```bash
cd code && python3 -c "
from app.services.content import ContentService
cs = ContentService('content')
cs.load()
post = cs.get_post_by_slug('why-im-building-in-public')
print(f'Title: {post.title}')
print(f'Slug: {post.slug}')
print(f'Reading time: {post.reading_time}')
print(f'Tags: {post.tags}')
print(f'Has HTML: {len(post.html_content) > 0}')
"
```
Expected: Title, slug, reading time, tags list, and `Has HTML: True`.

### Test 4: Tags Are Collected and Sorted
```bash
cd code && python3 -c "
from app.services.content import ContentService
cs = ContentService('content')
cs.load()
tags = cs.get_all_tags()
print(f'Tags: {tags}')
print(f'Sorted: {tags == sorted(tags)}')
"
```
Expected: A sorted list of unique tags from the sample blog post, and `Sorted: True`.

### Test 5: Project Retrieval and Featured Filter
```bash
cd code && python3 -c "
from app.services.content import ContentService
cs = ContentService('content')
cs.load()
project = cs.get_project_by_slug('portfolio-site')
print(f'Title: {project.title}')
print(f'Status: {project.status}')
print(f'Featured: {project.featured}')
featured = cs.get_featured_projects()
print(f'Featured count: {len(featured)}')
"
```
Expected: Project details and featured count of 1 (assuming the sample project is marked featured).

### Test 6: Pagination Works
```bash
cd code && python3 -c "
from app.services.content import ContentService
cs = ContentService('content')
cs.load()
posts, total = cs.get_posts(page=1, per_page=5)
print(f'Page 1: {len(posts)} posts, total: {total}')
posts, total = cs.get_posts(page=999, per_page=5)
print(f'Page 999: {len(posts)} posts, total: {total}')
"
```
Expected: Page 1 returns 1 post with total 1. Page 999 returns 0 posts with total 1.

### Test 7: HTML Content Contains Rendered Markdown
```bash
cd code && python3 -c "
from app.services.content import ContentService
cs = ContentService('content')
cs.load()
post = cs.get_post_by_slug('why-im-building-in-public')
assert '<h2>' in post.html_content or '<h2' in post.html_content, 'Missing h2 tags'
assert '<code>' in post.html_content or '<pre>' in post.html_content, 'Missing code block'
assert '<blockquote>' in post.html_content, 'Missing blockquote'
print('All HTML assertions passed')
"
```
Expected: `All HTML assertions passed`

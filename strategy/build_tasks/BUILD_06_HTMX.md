# Project: fullstackpm.tech — Build Task 06: HTMX Interactions

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
| Styling | **Tailwind CSS** (CDN) | Use utility classes only |
| Interactivity | **HTMX** (CDN) | For dynamic partial updates |
| Icons | **Heroicons** (inline SVG) | Outline style 24px |
| Fonts | **Geist Sans** + **JetBrains Mono** | Geist Sans via jsDelivr CDN, JetBrains Mono via Google Fonts |
| Content | **Markdown files** with YAML frontmatter | Parsed at startup, cached in memory |
| Deployment | **Render** | Procfile included |

**Do NOT use:** React, Vue, Angular, Svelte, Next.js, npm/node, webpack, any JS framework, Bootstrap, SCSS/LESS.

## 3. Color System (Mandatory — Use These Exact Values)

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
- File naming: lowercase with underscores (e.g., `projects.py`)
- Imports: stdlib first, then third-party, then local (separated by blank lines)
- No unused imports, no commented-out code

### Example Import Order
```python
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
```

### HTML / Jinja2
- All templates that render full pages extend `base.html`
- **Partial templates** (for HTMX responses) do NOT extend base.html — they return only the HTML fragment to swap
- Use CSS custom properties for all colors: `style="color: var(--color-text-primary);"`
- Do NOT use Tailwind's `dark:` prefix — the design system handles dark mode via CSS variables on the `.dark` class
- Use `text-h1`, `text-h2`, `text-body`, etc. typography classes from custom.css
- Heroicons: inline SVG, outline style, 24px viewBox

### HTMX Conventions
- Use `hx-get` for GET requests (never `hx-post` for read operations)
- Use `hx-target` to specify what element to update
- Use `hx-swap` to control how content is inserted (`innerHTML`, `outerHTML`, `beforeend`, etc.)
- Use `hx-indicator` to show a loading indicator during requests
- Use `hx-trigger` to control when requests fire (default is the natural event)
- Use `hx-push-url` when the HTMX action should update the browser URL bar
- HTMX is already loaded in `base.html` via CDN — do NOT add it again

## 5. The Task

Add HTMX-powered interactions to the **existing** Projects and Blog pages. These pages already work with standard page navigation (built in Tasks 2 and 3). This task adds progressive enhancement — the pages must still work without JavaScript, but HTMX makes filtering and pagination feel instant.

**Philosophy:** HTMX should feel invisible. Users shouldn't know it's there — filtering and pagination should just feel faster than a full page reload.

### Prerequisites

This task depends on **Task 2 (Projects)** and **Task 3 (Blog)** being complete. The following files must already exist:

- `app/routers/projects.py` — with routes `GET /projects` and `GET /projects/{slug}`
- `app/routers/blog.py` — with routes `GET /blog`, `GET /blog/{slug}`, `GET /blog/tag/{tag}`
- `app/templates/projects/gallery.html` — project gallery grid
- `app/templates/blog/list.html` — blog post list with pagination
- `app/templates/blog/tag.html` — blog posts filtered by tag
- `app/templates/partials/project_card.html` — reusable project card component

---

### What to Build

#### A. Project Filtering via HTMX

**Goal:** Let users click tech stack tags to filter the project grid without a full page reload.

**1. New HTMX endpoint in `app/routers/projects.py`:**

Add a new route:

```
GET /projects/filter?tech={tag}
```

- If `tech` is empty or `"all"`, return all projects
- If `tech` is a specific tag (e.g., `"FastAPI"`), return only projects whose `tech_stack` list contains that tag (case-insensitive match)
- This route returns a **partial HTML response** — just the project grid cards, NOT a full page
- Use a new partial template: `projects/partials/project_grid.html`

**Implementation pattern:**
```python
@router.get("/projects/filter", response_class=HTMLResponse)
async def filter_projects(request: Request, tech: str = "all") -> HTMLResponse:
    content_service = request.app.state.content_service
    projects = content_service.get_projects()
    if tech and tech.lower() != "all":
        projects = [
            p for p in projects
            if any(t.lower() == tech.lower() for t in p.tech_stack)
        ]
    return templates.TemplateResponse(
        "projects/partials/project_grid.html",
        {"request": request, "projects": projects, "config": settings},
    )
```

**2. New partial template: `app/templates/projects/partials/project_grid.html`**

This is a fragment — NO `{% extends "base.html" %}`. It renders just the grid of project cards:

```html
{% for project in projects %}
  {% include "partials/project_card.html" %}
{% endfor %}
{% if not projects %}
<div class="col-span-full text-center py-12">
  <p class="text-body" style="color: var(--color-text-tertiary);">No projects match this filter.</p>
  <button hx-get="/projects/filter?tech=all"
          hx-target="#project-grid"
          hx-swap="innerHTML"
          class="mt-4 text-small font-medium transition-colors"
          style="color: var(--color-accent);"
          onmouseover="this.style.color='var(--color-accent-hover)'"
          onmouseout="this.style.color='var(--color-accent)'">
    Show all projects
  </button>
</div>
{% endif %}
```

**3. Update `app/templates/projects/gallery.html`:**

Add a filter bar above the project grid. The filter bar shows "All" plus every unique tech stack tag across all projects.

Changes to make:

a) Pass `all_tech_tags` to the template context from the `GET /projects` route handler. Collect all unique tech stack tags:
```python
all_tech_tags = sorted(set(
    tag for project in projects for tag in project.tech_stack
))
```

b) Add a filter bar section between the page header and the grid:

```html
<!-- Filter Bar -->
<div class="flex flex-wrap gap-2 mb-8">
  <button hx-get="/projects/filter?tech=all"
          hx-target="#project-grid"
          hx-swap="innerHTML"
          hx-indicator="#grid-loading"
          class="text-xs rounded-md px-3 py-1.5 font-medium transition-colors border"
          style="background-color: var(--color-accent); color: white; border-color: var(--color-accent);"
          aria-label="Show all projects">
    All
  </button>
  {% for tag in all_tech_tags %}
  <button hx-get="/projects/filter?tech={{ tag }}"
          hx-target="#project-grid"
          hx-swap="innerHTML"
          hx-indicator="#grid-loading"
          class="text-xs rounded-md px-3 py-1.5 font-medium transition-colors border"
          style="background-color: var(--color-bg-tertiary); color: var(--color-text-secondary); border-color: var(--color-border);"
          onmouseover="this.style.borderColor='var(--color-border-hover)'"
          onmouseout="this.style.borderColor='var(--color-border)'"
          aria-label="Filter by {{ tag }}">
    {{ tag }}
  </button>
  {% endfor %}
</div>
```

c) Wrap the existing project grid in a container with an `id` for HTMX targeting:

```html
<!-- Loading indicator -->
<div id="grid-loading" class="htmx-indicator flex justify-center py-8">
  <svg class="animate-spin h-6 w-6" style="color: var(--color-accent);" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
  </svg>
</div>

<!-- Project grid (HTMX swap target) -->
<div id="project-grid" class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
  {% for project in projects %}
    {% include "partials/project_card.html" %}
  {% endfor %}
</div>
```

d) Add active state management. Add a small inline script in a `{% block scripts %}` to highlight the active filter button:

```html
{% block scripts %}
<script>
  document.addEventListener('htmx:afterRequest', function(event) {
    var filterBar = document.querySelector('.flex.flex-wrap.gap-2.mb-8');
    if (!filterBar) return;
    var buttons = filterBar.querySelectorAll('button');
    buttons.forEach(function(btn) {
      btn.style.backgroundColor = 'var(--color-bg-tertiary)';
      btn.style.color = 'var(--color-text-secondary)';
      btn.style.borderColor = 'var(--color-border)';
    });
    if (event.detail.elt && event.detail.elt.tagName === 'BUTTON') {
      event.detail.elt.style.backgroundColor = 'var(--color-accent)';
      event.detail.elt.style.color = 'white';
      event.detail.elt.style.borderColor = 'var(--color-accent)';
    }
  });
</script>
{% endblock %}
```

---

#### B. Blog Tag Filtering via HTMX

**Goal:** Let users click tag badges on the blog list page to filter posts without a full page reload.

**1. New HTMX endpoint in `app/routers/blog.py`:**

Add a new route:

```
GET /blog/filter?tag={tag}&page={page}
```

- If `tag` is empty or `"all"`, return all posts (paginated)
- If `tag` is a specific tag, return posts with that tag (paginated)
- Returns a **partial HTML response** — just the post list items, NOT a full page
- Use a new partial template: `blog/partials/post_list.html`

**Implementation pattern:**
```python
@router.get("/blog/filter", response_class=HTMLResponse)
async def filter_blog(request: Request, tag: str = "all", page: int = 1) -> HTMLResponse:
    content_service = request.app.state.content_service
    if tag and tag.lower() != "all":
        posts, total = content_service.get_posts_by_tag(tag, page=page, per_page=10)
    else:
        posts, total = content_service.get_posts(page=page, per_page=10)
    has_more = (page * 10) < total
    return templates.TemplateResponse(
        "blog/partials/post_list.html",
        {
            "request": request,
            "posts": posts,
            "current_page": page,
            "has_more": has_more,
            "active_tag": tag if tag.lower() != "all" else None,
            "config": settings,
        },
    )
```

**2. New partial template: `app/templates/blog/partials/post_list.html`**

This fragment renders just the list of blog posts and a "Load More" button if there are more posts. NO `{% extends "base.html" %}`.

```html
{% for post in posts %}
<article class="pb-6 mb-6 border-b" style="border-color: var(--color-border);">
  <a href="/blog/{{ post.slug }}" class="block group">
    <h3 class="text-h3 mb-1 transition-colors" style="color: var(--color-text-primary);"
        onmouseover="this.style.color='var(--color-accent)'"
        onmouseout="this.style.color='var(--color-text-primary)'">
      {{ post.title }}
    </h3>
  </a>
  <div class="flex items-center gap-3 mb-2">
    <span class="text-small" style="color: var(--color-text-tertiary);">{{ post.date.strftime('%b %d, %Y') }}</span>
    {% if post.reading_time %}
    <span class="text-small" style="color: var(--color-text-tertiary);">{{ post.reading_time }}</span>
    {% endif %}
  </div>
  <p class="text-body line-clamp-2 mb-3" style="color: var(--color-text-secondary);">{{ post.excerpt }}</p>
  <div class="flex flex-wrap gap-2">
    {% for tag in post.tags %}
    <span class="text-xs rounded-md px-2 py-1 font-medium"
          style="background-color: var(--color-bg-tertiary); color: var(--color-text-secondary);">
      {{ tag }}
    </span>
    {% endfor %}
  </div>
</article>
{% endfor %}

{% if not posts %}
<div class="text-center py-12">
  <p class="text-body" style="color: var(--color-text-tertiary);">No posts found.</p>
</div>
{% endif %}

{% if has_more %}
<div class="text-center mt-4">
  <button hx-get="/blog/filter?tag={{ active_tag or 'all' }}&page={{ current_page + 1 }}"
          hx-target="#post-list"
          hx-swap="beforeend"
          hx-indicator="#load-more-spinner"
          class="inline-flex items-center gap-2 rounded-lg border px-6 py-3 text-sm font-semibold transition-colors"
          style="color: var(--color-text-primary); border-color: var(--color-border);"
          onmouseover="this.style.borderColor='var(--color-border-hover)'"
          onmouseout="this.style.borderColor='var(--color-border)'">
    Load More
    <span id="load-more-spinner" class="htmx-indicator">
      <svg class="animate-spin h-4 w-4" style="color: var(--color-accent);" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
    </span>
  </button>
</div>
{% endif %}
```

**Important "Load More" behavior:** When the user clicks "Load More", the new posts are appended (`hx-swap="beforeend"`) to the list container. But the button itself is ALSO inside the target, so it will be replaced by the new content. The new partial response includes its OWN "Load More" button with an incremented page number (or no button if there are no more posts). This creates a self-replacing pagination pattern.

To make this work correctly, the "Load More" button should be **outside** the main post list but the entire response should replace the button's parent wrapper. Here's the refined approach:

Wrap the button in a div and use `hx-swap="outerHTML"` on the button's wrapper so the button replaces itself with new posts + a new button:

```html
<!-- At the end of post_list.html, AFTER the posts loop -->
{% if has_more %}
<div id="load-more-wrapper">
  <div class="text-center mt-4">
    <button hx-get="/blog/filter?tag={{ active_tag or 'all' }}&page={{ current_page + 1 }}"
            hx-target="#load-more-wrapper"
            hx-swap="outerHTML"
            hx-indicator="#load-more-spinner"
            class="inline-flex items-center gap-2 rounded-lg border px-6 py-3 text-sm font-semibold transition-colors"
            style="color: var(--color-text-primary); border-color: var(--color-border);"
            onmouseover="this.style.borderColor='var(--color-border-hover)'"
            onmouseout="this.style.borderColor='var(--color-border)'">
      Load More
      <span id="load-more-spinner" class="htmx-indicator">
        <svg class="animate-spin h-4 w-4" style="color: var(--color-accent);" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </span>
    </button>
  </div>
</div>
{% endif %}
```

**3. Update `app/templates/blog/list.html`:**

Changes to make:

a) Add HTMX attributes to the tag filter badges. Change the existing tag badges from standard `<a>` links to HTMX-powered buttons:

```html
<!-- Tag Filter Bar -->
<div class="flex flex-wrap gap-2 mb-8" id="tag-filter-bar">
  <button hx-get="/blog/filter?tag=all"
          hx-target="#post-list"
          hx-swap="innerHTML"
          hx-indicator="#list-loading"
          class="text-xs rounded-md px-3 py-1.5 font-medium transition-colors border"
          style="background-color: var(--color-accent); color: white; border-color: var(--color-accent);"
          aria-label="Show all posts">
    All
  </button>
  {% for tag in all_tags %}
  <button hx-get="/blog/filter?tag={{ tag }}"
          hx-target="#post-list"
          hx-swap="innerHTML"
          hx-indicator="#list-loading"
          class="text-xs rounded-md px-3 py-1.5 font-medium transition-colors border"
          style="background-color: var(--color-bg-tertiary); color: var(--color-text-secondary); border-color: var(--color-border);"
          onmouseover="this.style.borderColor='var(--color-border-hover)'"
          onmouseout="this.style.borderColor='var(--color-border)'"
          aria-label="Filter by {{ tag }}">
    {{ tag }}
  </button>
  {% endfor %}
</div>
```

b) Add a loading indicator between the filter bar and the post list:

```html
<!-- Loading indicator -->
<div id="list-loading" class="htmx-indicator flex justify-center py-8">
  <svg class="animate-spin h-6 w-6" style="color: var(--color-accent);" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
  </svg>
</div>
```

c) Wrap the existing post list in a container with `id="post-list"`:

```html
<div id="post-list">
  {% for post in posts %}
  <article class="pb-6 mb-6 border-b" style="border-color: var(--color-border);">
    <!-- ... existing post markup ... -->
  </article>
  {% endfor %}

  {% if has_more %}
  <div id="load-more-wrapper">
    <div class="text-center mt-4">
      <button hx-get="/blog/filter?tag=all&page=2"
              hx-target="#load-more-wrapper"
              hx-swap="outerHTML"
              hx-indicator="#load-more-spinner-main"
              class="inline-flex items-center gap-2 rounded-lg border px-6 py-3 text-sm font-semibold transition-colors"
              style="color: var(--color-text-primary); border-color: var(--color-border);"
              onmouseover="this.style.borderColor='var(--color-border-hover)'"
              onmouseout="this.style.borderColor='var(--color-border)'">
        Load More
        <span id="load-more-spinner-main" class="htmx-indicator">
          <svg class="animate-spin h-4 w-4" style="color: var(--color-accent);" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </span>
      </button>
    </div>
  </div>
  {% endif %}
</div>
```

d) Replace the old "Newer" / "Older" pagination links with the "Load More" button pattern shown above.

e) Pass `has_more` to the template context from the `GET /blog` route. Update the route handler:
```python
# In the existing GET /blog route handler, add has_more to context:
has_more = (page * 10) < total
# ... pass has_more=has_more to _ctx(...)
```

f) Add active state script in `{% block scripts %}` (same pattern as project filter):

```html
{% block scripts %}
<script>
  document.addEventListener('htmx:afterRequest', function(event) {
    var filterBar = document.getElementById('tag-filter-bar');
    if (!filterBar || !event.detail.elt || !filterBar.contains(event.detail.elt)) return;
    var buttons = filterBar.querySelectorAll('button');
    buttons.forEach(function(btn) {
      btn.style.backgroundColor = 'var(--color-bg-tertiary)';
      btn.style.color = 'var(--color-text-secondary)';
      btn.style.borderColor = 'var(--color-border)';
    });
    event.detail.elt.style.backgroundColor = 'var(--color-accent)';
    event.detail.elt.style.color = 'white';
    event.detail.elt.style.borderColor = 'var(--color-accent)';
  });
</script>
{% endblock %}
```

---

#### C. CSS for HTMX Loading States

Add the following styles to the END of `app/static/css/custom.css`:

```css
/* HTMX loading states */
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: inline-flex;
}

.htmx-request.htmx-indicator {
  display: inline-flex;
}
```

These styles ensure:
- Loading indicators are hidden by default
- They become visible when HTMX adds the `htmx-request` class during an active request
- Both parent-triggered (`.htmx-request .htmx-indicator`) and self-triggered (`.htmx-request.htmx-indicator`) patterns work

---

### ContentService API (Already Built — Task 1)

The ContentService is initialized in the FastAPI lifespan and stored on `request.app.state.content_service`. Here are the methods you need:

```python
class ContentService:
    def get_projects(self) -> list[Project]:
        """All projects sorted by display_order."""

    def get_posts(self, page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]:
        """Paginated blog posts (newest first). Returns (posts, total_count)."""

    def get_posts_by_tag(self, tag: str, page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]:
        """Posts filtered by tag, paginated."""

    def get_all_tags(self) -> list[str]:
        """All unique tags sorted alphabetically."""
```

**Project model fields (relevant for filtering):**
```python
class Project:
    title: str
    slug: str
    description: str
    tech_stack: list[str]    # e.g., ["FastAPI", "Claude API", "HTMX"]
    status: str              # "live" | "in_progress" | "case_study" | "planned"
    featured: bool
    display_order: int
    html_content: str
    github_url: str
    live_url: str
```

**BlogPost model fields:**
```python
class BlogPost:
    title: str
    slug: str
    date: datetime
    tags: list[str]
    excerpt: str
    author: str
    reading_time: str        # e.g., "5 min read"
    html_content: str
```

---

### Existing Files (FULL text of each)

These files already exist. Read them carefully — you are MODIFYING some of them.

#### `app/config.py` (DO NOT MODIFY)

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

#### `app/templates/base.html` (DO NOT MODIFY — reference only)

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

  <!-- Fonts: Geist Sans (via custom.css @font-face) + JetBrains Mono -->
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
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

#### `app/static/css/custom.css` (YOU MODIFY — append HTMX styles at end)

```css
/* fullstackpm.tech — Design System Tokens */

/* Geist Sans — loaded from jsDelivr/Fontsource CDN */
@font-face {
  font-family: 'Geist Sans';
  font-style: normal;
  font-display: swap;
  font-weight: 400;
  src: url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-400-normal.woff2) format('woff2'),
       url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-400-normal.woff) format('woff');
}

@font-face {
  font-family: 'Geist Sans';
  font-style: normal;
  font-display: swap;
  font-weight: 500;
  src: url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-500-normal.woff2) format('woff2'),
       url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-500-normal.woff) format('woff');
}

@font-face {
  font-family: 'Geist Sans';
  font-style: normal;
  font-display: swap;
  font-weight: 600;
  src: url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-600-normal.woff2) format('woff2'),
       url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-600-normal.woff) format('woff');
}

@font-face {
  font-family: 'Geist Sans';
  font-style: normal;
  font-display: swap;
  font-weight: 700;
  src: url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-700-normal.woff2) format('woff2'),
       url(https://cdn.jsdelivr.net/fontsource/fonts/geist-sans@latest/latin-700-normal.woff) format('woff');
}

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
  margin-top: 3rem;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
  color: var(--color-text-primary);
}

.prose h3 {
  font-size: 1.375rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  letter-spacing: -0.015em;
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

/* ===== ADD THE FOLLOWING AT THE END ===== */

/* HTMX loading states */
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: inline-flex;
}

.htmx-request.htmx-indicator {
  display: inline-flex;
}
```

#### `app/static/js/main.js` (DO NOT MODIFY — reference only)

```javascript
// fullstackpm.tech — Dark Mode & Mobile Menu

(function () {
  "use strict";

  // --- Dark Mode ---
  const STORAGE_KEY = "theme";

  function getPreferredTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function applyTheme(theme) {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem(STORAGE_KEY, theme);

    // Update toggle icon
    const sunIcon = document.getElementById("theme-icon-sun");
    const moonIcon = document.getElementById("theme-icon-moon");
    if (sunIcon && moonIcon) {
      sunIcon.classList.toggle("hidden", theme === "light");
      moonIcon.classList.toggle("hidden", theme === "dark");
    }
  }

  // Apply theme immediately to prevent flash
  applyTheme(getPreferredTheme());

  document.addEventListener("DOMContentLoaded", function () {
    // Re-apply to update icons after DOM is ready
    applyTheme(getPreferredTheme());

    // Dark mode toggle button
    const toggleBtn = document.getElementById("theme-toggle");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", function () {
        const current = document.documentElement.classList.contains("dark")
          ? "dark"
          : "light";
        applyTheme(current === "dark" ? "light" : "dark");
      });
    }

    // --- Mobile Menu ---
    const menuBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");

    if (menuBtn && mobileMenu) {
      menuBtn.addEventListener("click", function () {
        const isOpen = !mobileMenu.classList.contains("hidden");
        mobileMenu.classList.toggle("hidden");
        menuBtn.setAttribute("aria-expanded", String(!isOpen));
      });

      // Close menu when clicking a link
      mobileMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
          mobileMenu.classList.add("hidden");
          menuBtn.setAttribute("aria-expanded", "false");
        });
      });
    }
  });
})();
```

### Scope Boundaries

- **IN scope:**
  - Updated `app/routers/projects.py` — add `GET /projects/filter` route + pass `all_tech_tags` to gallery context
  - Updated `app/routers/blog.py` — add `GET /blog/filter` route + pass `has_more` to list context
  - Updated `app/templates/projects/gallery.html` — add filter bar, HTMX attributes, loading indicator
  - Updated `app/templates/blog/list.html` — add HTMX tag filter, "Load More" button, loading indicator
  - New `app/templates/projects/partials/project_grid.html` — partial for filtered project grid
  - New `app/templates/blog/partials/post_list.html` — partial for filtered/paginated blog posts
  - Updated `app/static/css/custom.css` — add HTMX indicator styles at the end

- **OUT of scope:**
  - No changes to `base.html`, `main.js`, `config.py`, `main.py`, or `navbar.html`
  - No changes to ContentService (`app/services/content.py`)
  - No changes to project detail page or blog detail page
  - No new Python dependencies
  - No search functionality (not in this task)
  - No contact form HTMX (future task)

## 6. Expected Output

Return these COMPLETE files:

1. **Updated `app/routers/projects.py`** — existing routes unchanged + new `GET /projects/filter` route + `all_tech_tags` in gallery context
2. **Updated `app/routers/blog.py`** — existing routes unchanged + new `GET /blog/filter` route + `has_more` in list context
3. **Updated `app/templates/projects/gallery.html`** — full template with filter bar + HTMX + loading indicator
4. **Updated `app/templates/blog/list.html`** — full template with HTMX tag filter + "Load More" + loading indicator
5. **New `app/templates/projects/partials/project_grid.html`** — partial for HTMX project grid swap
6. **New `app/templates/blog/partials/post_list.html`** — partial for HTMX blog post list swap
7. **Updated `app/static/css/custom.css`** — existing styles unchanged + HTMX indicator styles appended

### Output Rules

- Return COMPLETE files, not snippets or diffs
- Include the file path as a comment at the top of each Python file
- Do not add features beyond what was specified
- Do not refactor existing code — add the new functionality alongside what exists
- All colors must use CSS variables — no hardcoded hex values in templates
- HTMX is already loaded via CDN in base.html — do NOT add it again
- Partial templates must NOT extend base.html
- All filter buttons must have `aria-label` attributes for accessibility
- Loading spinners use the standard SVG spinner with `animate-spin` class

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
│   │   │   ├── pages.py          # Routes: /, /about, /contact
│   │   │   ├── projects.py       # YOU MODIFY (add /projects/filter route)
│   │   │   ├── blog.py           # YOU MODIFY (add /blog/filter route)
│   │   │   └── seo.py            # (from Task 5)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── content.py        # ContentService (from Task 1)
│   │   │   └── feed.py           # (from Task 5)
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── resume.html       # (from Task 4)
│   │   │   ├── 404.html
│   │   │   ├── projects/
│   │   │   │   ├── gallery.html   # YOU MODIFY (add filter bar + HTMX)
│   │   │   │   ├── detail.html
│   │   │   │   └── partials/
│   │   │   │       └── project_grid.html  # YOU CREATE THIS
│   │   │   ├── blog/
│   │   │   │   ├── list.html      # YOU MODIFY (add HTMX tag filter + Load More)
│   │   │   │   ├── detail.html
│   │   │   │   ├── tag.html
│   │   │   │   └── partials/
│   │   │   │       └── post_list.html     # YOU CREATE THIS
│   │   │   └── partials/
│   │   │       ├── navbar.html
│   │   │       ├── footer.html
│   │   │       └── project_card.html  # (from Task 2, not modified)
│   │   └── static/
│   │       ├── css/custom.css     # YOU MODIFY (append HTMX styles)
│   │       ├── js/main.js
│   │       └── img/
│   ├── content/
│   │   ├── blog/
│   │   │   └── *.md               # Blog posts (from Tasks 1 & 3)
│   │   └── projects/
│   │       └── *.md               # Projects (from Tasks 1 & 2)
│   ├── requirements.txt
│   └── Procfile
```

All file paths in your output are **relative to `code/`**. For example, the project grid partial goes at `code/app/templates/projects/partials/project_grid.html` on disk.

## 8. Acceptance Test

After implementing, verify all of the following:

### Test 1: Server Starts Without Errors
```bash
cd code && python3 -m uvicorn app.main:app --reload --port 8001
```
The server should start cleanly with no import errors or exceptions.

### Test 2: Project Filter Bar Renders
Navigate to `http://localhost:8001/projects`.

Expected:
- A row of filter buttons appears above the project grid
- "All" button is highlighted (accent color background)
- All unique tech stack tags from project content appear as buttons
- Buttons have `aria-label` attributes

### Test 3: Project Filtering Works
Click a tech stack tag button (e.g., "FastAPI") on the Projects page.

Expected:
- The project grid updates WITHOUT a full page reload
- Only projects containing that tech tag are shown
- The clicked button becomes highlighted (accent color)
- The "All" button loses its highlight
- A loading spinner briefly appears during the request

### Test 4: Project Filter "All" Resets
After filtering, click the "All" button.

Expected:
- All projects reappear
- The "All" button is highlighted again
- No page reload occurs

### Test 5: Project Filter Empty State
If filtering by a tag that no projects have (edge case), the grid should show "No projects match this filter." with a "Show all projects" link.

### Test 6: Blog Tag Filter Works
Navigate to `http://localhost:8001/blog` and click a tag badge.

Expected:
- The post list updates WITHOUT a full page reload
- Only posts with that tag are shown
- The clicked tag button becomes highlighted
- A loading spinner briefly appears during the request

### Test 7: Blog "Load More" Works
Navigate to `http://localhost:8001/blog`. If there are more than 10 posts:

Expected:
- A "Load More" button appears below the post list (instead of "Newer"/"Older" links)
- Clicking "Load More" appends new posts below the existing ones (no page reload)
- A small spinner appears on the button while loading
- After all posts are loaded, the "Load More" button disappears
- If there are 10 or fewer posts, no "Load More" button appears

### Test 8: HTMX Filter Endpoint Returns Partial HTML
```bash
curl -s http://localhost:8001/projects/filter?tech=all | head -5
```
Expected: Raw HTML fragment (project cards), NOT a full HTML page (no `<!DOCTYPE>`, no `<html>`, no `<head>`).

```bash
curl -s http://localhost:8001/blog/filter?tag=all | head -5
```
Expected: Raw HTML fragment (post articles), NOT a full HTML page.

### Test 9: Dark Mode Works with HTMX
Toggle dark mode, then use the project filter or blog tag filter.

Expected:
- Filtered content uses dark mode colors correctly
- Loading spinners use accent color in both light and dark mode
- Filter buttons maintain correct styling in dark mode

### Test 10: Graceful Degradation
Disable JavaScript in your browser, then navigate to `/projects` and `/blog`.

Expected:
- Pages render normally with all content visible (server-side rendered)
- Filter buttons are visible but non-functional (acceptable — this is progressive enhancement)
- Blog posts are listed with standard pagination links if HTMX was not used for initial render
- No JavaScript errors in the console

### Test 11: Loading Indicators
Open browser DevTools Network tab and throttle to "Slow 3G". Click a project filter button.

Expected:
- The loading spinner appears between the filter bar and the project grid
- The spinner disappears when the content loads
- Content swaps in smoothly

### Test 12: No Duplicate HTMX Script
View page source on any page with HTMX interactions.

Expected:
- HTMX script tag appears exactly ONCE (in base.html `<script src="https://unpkg.com/htmx.org@2.0.2" ...>`)
- No additional HTMX script tags in the page templates

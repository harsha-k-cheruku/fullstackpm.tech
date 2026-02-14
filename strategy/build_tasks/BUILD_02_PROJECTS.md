# Project: fullstackpm.tech — Build Task 02: Projects Pages

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
| Icons | **Heroicons** (inline SVG) | Outline style 24px for UI |
| Fonts | **Geist Sans** + **JetBrains Mono** | Via Google Fonts CDN |
| Content | **Markdown files** with YAML frontmatter | Parsed at startup, cached in memory |

**Do NOT use:** React, Vue, Angular, Svelte, Next.js, npm/node, webpack, any JS framework, Bootstrap, SCSS/LESS.

## 3. Color System (Mandatory — Use These Exact Values)

```css
:root {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8FAFC;
  --color-bg-tertiary: #F1F5F9;
  --color-text-primary: #0F172A;
  --color-text-secondary: #475569;
  --color-text-tertiary: #94A3B8;
  --color-border: #E2E8F0;
  --color-border-hover: #CBD5E1;
  --color-accent: #2E8ECE;
  --color-accent-hover: #2577AD;
  --color-accent-light: #E8F4FB;
  --color-accent-dark: #1A3A52;
  --color-success: #27AE60;
  --color-success-bg: #D5F5E3;
  --color-warning: #F1C40F;
  --color-warning-bg: #FEF9E7;
  --color-danger: #E74C3C;
  --color-danger-bg: #FADBD8;
  --color-info: #2E8ECE;
}
.dark {
  --color-bg-primary: #030712;
  --color-bg-secondary: #0F172A;
  --color-bg-tertiary: #1E293B;
  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-text-tertiary: #64748B;
  --color-border: #1E293B;
  --color-border-hover: #334155;
  --color-accent-light: #172554;
  --color-success-bg: #052E16;
  --color-warning-bg: #422006;
  --color-danger-bg: #450A0A;
}
```

## 4. Coding Conventions

### Python
- Type hints on all function signatures
- Async functions for route handlers
- File naming: lowercase with underscores
- Imports: stdlib first, then third-party, then local (blank line separated between each group)

### Example Import Order
```python
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config import settings
```

### HTML/Jinja2
- Semantic HTML5: `<nav>`, `<main>`, `<article>`, `<section>`
- All templates extend `base.html`
- Jinja2 blocks: `{% block title %}`, `{% block content %}`
- Indent with 2 spaces

### Tailwind
- Mobile-first: base for mobile, `md:` tablet, `lg:` desktop
- CSS variables for ALL colors — never hardcode hex values
- Use `style="color: var(--color-text-primary);"` instead of Tailwind color classes
- Transitions: `transition-colors duration-150` for hover states
- Border radius: `rounded-xl` for cards
- Focus rings: `focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2`

### Dark Mode
- Via CSS variables (which auto-swap when `.dark` class is on `<html>`)
- Do NOT use Tailwind `dark:` prefix — the CSS variable system handles everything

### Accessibility
- Keyboard-focusable interactive elements
- Images need alt text
- ARIA attributes where semantic HTML is insufficient

## 5. The Task

Build the Projects gallery page (`/projects`) and project detail page (`/projects/{slug}`).

### What to Build

**1. Router: `app/routers/projects.py`**

Two routes:
- `GET /projects` — renders the project gallery grid
- `GET /projects/{slug}` — renders a single project detail page, returns 404 if slug not found

Access the ContentService from `request.app.state.content_service`. Follow the same pattern as `pages.py` (shown below in Existing Files).

**2. Templates:**
- `app/templates/projects/gallery.html` — extends base.html, shows a grid of project cards
- `app/templates/projects/detail.html` — extends base.html, shows a full project writeup

**3. Partial:**
- `app/templates/partials/project_card.html` — reusable card component included in gallery

**4. Sample content:**
- `content/projects/pm-interview-coach.md` — a second sample project

**5. Router registration in `main.py`**

---

### ContentService API (already built — you call these methods)

The ContentService is available at `request.app.state.content_service` and provides:

```python
class ContentService:
    def get_projects(self) -> list[Project]:
        """All projects sorted by display_order."""

    def get_project_by_slug(self, slug: str) -> Project | None:
        """Single project by URL slug. Returns None if not found."""

    def get_featured_projects(self, limit: int = 3) -> list[Project]:
        """Projects marked as featured, limited to N."""

class Project:
    title: str
    slug: str
    description: str        # One-line description
    tech_stack: list[str]
    status: str             # "live" | "in_progress" | "case_study" | "planned"
    featured: bool
    display_order: int
    html_content: str       # Rendered markdown HTML
    github_url: str
    live_url: str
```

---

### Gallery Page Layout

- Page title: "Projects" with a rocket-launch Heroicon next to it
- Subtitle: "Things I've built to demonstrate product + technical skills."
- Responsive grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`
- Each card uses the `project_card.html` partial: `{% include "partials/project_card.html" %}`
- If no projects exist, show an empty state with a message
- Set `current_page` to `"/projects"` so the navbar highlights correctly

### Project Card (partial)

Each card shows:
- Icon badge (40x40 rounded-lg with accent-light bg and accent-colored Heroicon) — use a generic Heroicon (e.g., squares-2x2) since projects don't specify individual icons
- Status badge (top-right, semantic color per status: live=green, in_progress=amber, case_study=blue, planned=gray)
- Title (text-h4, text-primary)
- Description (text-body, text-secondary, line-clamp-2)
- Tech stack tags (flex wrap, small badges)
- Entire card is a clickable `<a>` linking to `/projects/{{ project.slug }}`
- Hover: border color change + subtle shadow via inline `onmouseover`/`onmouseout`
- Focus ring for keyboard navigation

Status badge colors:
- `live` — bg: `var(--color-success-bg)`, text: `var(--color-success)`
- `in_progress` — bg: `var(--color-warning-bg)`, text: `var(--color-warning)`
- `case_study` — bg: `var(--color-accent-light)`, text: `var(--color-accent)`
- `planned` — bg: `var(--color-bg-tertiary)`, text: `var(--color-text-tertiary)`

Status badge label mapping (display clean labels):
- `live` → "Live"
- `in_progress` → "In Progress"
- `case_study` → "Case Study"
- `planned` → "Planned"

### Detail Page Layout

- Back link: "← Back to Projects" linking to `/projects` — styled as a text link with accent color
- Title (text-h1) + status badge (same color logic as card) + description
- Tech stack tags row (same style as card tags)
- Links row: GitHub button + Live Demo button (only render each if the URL is non-empty)
  - GitHub button: outline style with GitHub SVG icon
  - Live Demo button: filled accent style with external-link Heroicon
- Rendered markdown content in a `<div class="prose">` wrapper (prose styles are already in custom.css)
- Max width: `max-w-3xl mx-auto`
- Set `current_page` to `"/projects"` so the navbar highlights correctly

### Sample Project Markdown

Create `content/projects/pm-interview-coach.md`:

```yaml
---
title: "PM Interview Coach"
description: "AI-powered practice tool using real PM frameworks and Claude API"
tech_stack: [FastAPI, Claude API, HTMX, Tailwind CSS, SQLite]
status: "in_progress"
featured: true
display_order: 2
github_url: "https://github.com/hcheruku/pm-interview-coach"
live_url: ""
---
```

Below the frontmatter, write approximately 200 words of realistic project content with these four sections:
- **## The Problem** — PM interview prep is fragmented and relies on memorization rather than real practice
- **## The Approach** — Build an AI-powered coach that simulates real PM interviews using Claude API
- **## The Solution** — A web app where users select a question type (product design, estimation, strategy, behavioral), get a realistic question, submit their answer, and receive structured feedback based on PM frameworks like CIRCLES, RICE, and HEART
- **## Technical Details** — FastAPI backend, HTMX for real-time streaming of AI feedback, SQLite for session history, Tailwind CSS for responsive UI

---

### Existing Files (FULL text of each)

These are the actual files currently in the project. Reference them for patterns, conventions, and structure.

#### `app/routers/pages.py` (pattern to follow for your router)

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

#### `app/main.py` (you will modify this to add router registration)

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

Add `from app.routers import projects` and `app.include_router(projects.router)` to this file.

#### `app/config.py`

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

#### `app/templates/base.html`

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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
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

#### `app/templates/partials/navbar.html`

```html
<!-- partials/navbar.html -->
<nav aria-label="Main navigation"
     class="sticky top-0 z-50 h-16 border-b"
     style="background-color: var(--color-bg-primary); border-color: var(--color-border);">
  <div class="mx-auto flex h-full max-w-[1200px] items-center justify-between px-4 sm:px-6">

    <!-- Site name -->
    <a href="/"
       class="text-lg font-bold transition-colors"
       style="color: var(--color-text-primary);">
      fullstackpm.tech
    </a>

    <!-- Desktop nav links -->
    <div class="hidden items-center gap-1 md:flex">
      {% set nav_links = [
        ("Home", "/"),
        ("Projects", "/projects"),
        ("Blog", "/blog"),
        ("About", "/about"),
        ("Contact", "/contact"),
      ] %}
      {% for label, href in nav_links %}
      <a href="{{ href }}"
         class="relative px-3 py-2 text-sm font-medium transition-colors"
         style="color: {{ 'var(--color-text-primary)' if current_page == href else 'var(--color-text-secondary)' }};"
         {% if current_page == href %}aria-current="page"{% endif %}
         onmouseover="this.style.color='var(--color-text-primary)'"
         onmouseout="this.style.color='{{ 'var(--color-text-primary)' if current_page == href else 'var(--color-text-secondary)' }}'">
        {{ label }}
        {% if current_page == href %}
        <span class="absolute bottom-0 left-3 right-3 h-0.5" style="background-color: var(--color-accent);"></span>
        {% endif %}
      </a>
      {% endfor %}
    </div>

    <!-- Right side: theme toggle + mobile menu button -->
    <div class="flex items-center gap-2">

      <!-- Dark mode toggle -->
      <button id="theme-toggle"
              type="button"
              aria-label="Toggle dark mode"
              class="rounded-lg p-2 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"
              style="color: var(--color-text-secondary); --tw-ring-color: var(--color-accent);"
              onmouseover="this.style.color='var(--color-text-primary)'"
              onmouseout="this.style.color='var(--color-text-secondary)'">
        <!-- Sun icon (shown in dark mode) -->
        <svg id="theme-icon-sun" class="hidden h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
        </svg>
        <!-- Moon icon (shown in light mode) -->
        <svg id="theme-icon-moon" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
        </svg>
      </button>

      <!-- Mobile hamburger -->
      <button id="mobile-menu-btn"
              type="button"
              aria-label="Open menu"
              aria-expanded="false"
              aria-controls="mobile-menu"
              class="rounded-lg p-2 transition-colors md:hidden focus:outline-none focus:ring-2 focus:ring-offset-2"
              style="color: var(--color-text-secondary); --tw-ring-color: var(--color-accent);"
              onmouseover="this.style.color='var(--color-text-primary)'"
              onmouseout="this.style.color='var(--color-text-secondary)'">
        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>
    </div>
  </div>

  <!-- Mobile menu dropdown -->
  <div id="mobile-menu"
       class="hidden border-b md:hidden"
       style="background-color: var(--color-bg-primary); border-color: var(--color-border);">
    <div class="mx-auto max-w-[1200px] px-4 py-3 sm:px-6">
      {% for label, href in nav_links %}
      <a href="{{ href }}"
         class="block rounded-lg px-3 py-2 text-sm font-medium transition-colors"
         style="color: {{ 'var(--color-text-primary)' if current_page == href else 'var(--color-text-secondary)' }};"
         {% if current_page == href %}aria-current="page"{% endif %}>
        {{ label }}
      </a>
      {% endfor %}
    </div>
  </div>
</nav>
```

#### `app/templates/partials/footer.html`

```html
<!-- partials/footer.html -->
<footer class="border-t mt-16 py-12"
        style="background-color: var(--color-bg-secondary); border-color: var(--color-border);">
  <div class="mx-auto max-w-[1200px] px-4 sm:px-6">

    <!-- Three-column grid -->
    <div class="grid grid-cols-1 gap-8 md:grid-cols-3">

      <!-- Col 1: Site info -->
      <div>
        <a href="/" class="text-lg font-bold" style="color: var(--color-text-primary);">
          fullstackpm.tech
        </a>
        <p class="text-small mt-2" style="color: var(--color-text-secondary);">
          Full Stack AI Product Manager. Engineering Mind. Design Obsession.
        </p>
      </div>

      <!-- Col 2: Quick links -->
      <div>
        <h3 class="text-small mb-3 font-semibold" style="color: var(--color-text-primary);">Quick Links</h3>
        <ul class="space-y-2">
          {% set footer_links = [
            ("Home", "/"),
            ("Projects", "/projects"),
            ("Blog", "/blog"),
            ("About", "/about"),
            ("Contact", "/contact"),
          ] %}
          {% for label, href in footer_links %}
          <li>
            <a href="{{ href }}"
               class="text-small transition-colors"
               style="color: var(--color-text-secondary);"
               onmouseover="this.style.color='var(--color-accent)'"
               onmouseout="this.style.color='var(--color-text-secondary)'">
              {{ label }}
            </a>
          </li>
          {% endfor %}
        </ul>
      </div>

      <!-- Col 3: Social links -->
      <div>
        <h3 class="text-small mb-3 font-semibold" style="color: var(--color-text-primary);">Connect</h3>
        <ul class="space-y-2">
          <li>
            <a href="{{ config.github_url }}"
               target="_blank"
               rel="noopener noreferrer"
               class="inline-flex items-center gap-2 text-small transition-colors"
               style="color: var(--color-text-secondary);"
               onmouseover="this.style.color='var(--color-accent)'"
               onmouseout="this.style.color='var(--color-text-secondary)'">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              GitHub
            </a>
          </li>
          <li>
            <a href="{{ config.linkedin_url }}"
               target="_blank"
               rel="noopener noreferrer"
               class="inline-flex items-center gap-2 text-small transition-colors"
               style="color: var(--color-text-secondary);"
               onmouseover="this.style.color='var(--color-accent)'"
               onmouseout="this.style.color='var(--color-text-secondary)'">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
              LinkedIn
            </a>
          </li>
          <li>
            <a href="{{ config.rss_url }}"
               class="inline-flex items-center gap-2 text-small transition-colors"
               style="color: var(--color-text-secondary);"
               onmouseover="this.style.color='var(--color-accent)'"
               onmouseout="this.style.color='var(--color-text-secondary)'">
              <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12.75 19.5v-.75a7.5 7.5 0 0 0-7.5-7.5H4.5m0-6.75h.75c7.87 0 14.25 6.38 14.25 14.25v.75M6 18.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" /></svg>
              RSS Feed
            </a>
          </li>
        </ul>
      </div>
    </div>

    <!-- Bottom attribution -->
    <div class="mt-8 border-t pt-6 text-center" style="border-color: var(--color-border);">
      <p class="text-xs" style="color: var(--color-text-tertiary);">
        Built with FastAPI + HTMX &middot; &copy; {{ year }} Harsha Cheruku
      </p>
    </div>
  </div>
</footer>
```

#### `app/templates/404.html`

```html
{% extends "base.html" %}

{% block content %}

<section class="flex flex-col items-center justify-center py-24 text-center">
  <p class="text-display mb-4" style="color: var(--color-text-tertiary);">404</p>
  <h1 class="text-h2 mb-2" style="color: var(--color-text-primary);">Page not found</h1>
  <p class="text-body mb-8" style="color: var(--color-text-secondary);">
    The page you're looking for doesn't exist or has been moved.
  </p>
  <a href="/"
     class="inline-flex items-center rounded-lg px-5 py-2.5 text-sm font-semibold text-white transition-colors"
     style="background-color: var(--color-accent);"
     onmouseover="this.style.backgroundColor='var(--color-accent-hover)'"
     onmouseout="this.style.backgroundColor='var(--color-accent)'">
    Back to Home
  </a>
</section>

{% endblock %}
```

#### `app/static/css/custom.css`

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
```

#### `app/static/js/main.js`

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

#### `requirements.txt`

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

---

### Scope Boundaries

- **IN scope:** `app/routers/projects.py`, `app/templates/projects/gallery.html`, `app/templates/projects/detail.html`, `app/templates/partials/project_card.html`, `content/projects/pm-interview-coach.md`, updated `app/main.py` (add router registration only)
- **OUT of scope:** Blog pages, resume page, HTMX filtering/sorting (that is a future task), ContentService (already built in Task 01), `custom.css` (do not modify), `base.html` (do not modify), `navbar.html` (do not modify), `footer.html` (do not modify)

## 6. Expected Output

Return these COMPLETE files:

1. `app/routers/projects.py` — Router with `GET /projects` and `GET /projects/{slug}`
2. `app/templates/projects/gallery.html` — Gallery grid page extending base.html
3. `app/templates/projects/detail.html` — Project detail page extending base.html
4. `app/templates/partials/project_card.html` — Reusable card partial
5. `content/projects/pm-interview-coach.md` — Sample project markdown
6. Updated `app/main.py` — Add projects router import and registration

### Output Rules
- Return COMPLETE files, not snippets or diffs
- Include file path as a comment at the top of each file (for Python) or as the filename heading (for templates/markdown)
- Do not add features beyond what is specified in this document
- Do not modify any files not listed in the output list above
- Follow the exact coding conventions in Section 4
- Use CSS variables for all colors — never hardcode hex values in templates

## 7. Current Project Structure

```
fullstackpm.tech/
├── strategy/                         # Planning docs (DO NOT modify)
│   ├── build_tasks/
│   │   ├── BUILD_01_CONTENT_SERVICE.md
│   │   └── BUILD_02_PROJECTS.md      # This file
│   └── ...
├── code/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # MODIFY: add projects router
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── pages.py              # Existing: /, /about, /contact
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── content.py            # Built in Task 01 (ContentService)
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── 404.html
│   │   │   ├── projects/             # CREATE: gallery.html, detail.html
│   │   │   ├── blog/                 # Empty (future task)
│   │   │   └── partials/
│   │   │       ├── navbar.html
│   │   │       └── footer.html
│   │   └── static/
│   │       ├── css/custom.css
│   │       ├── js/main.js
│   │       └── img/
│   ├── content/
│   │   ├── blog/                     # Sample blog post (from Task 01)
│   │   └── projects/                 # CREATE: pm-interview-coach.md
│   ├── tests/
│   │   └── __init__.py
│   ├── requirements.txt
│   └── Procfile
```

All file paths in your output are **relative to `code/`**. For example, when you create the router, the file goes at `code/app/routers/projects.py` on disk but the import path is `app.routers.projects`.

## 8. Acceptance Test

After implementing, verify all of the following:

### Test 1: Server Starts Without Errors
```bash
cd code && python3 -m uvicorn app.main:app --reload --port 8001
```
The server should start cleanly with no import errors or exceptions.

### Test 2: Gallery Page Renders
Open `http://localhost:8001/projects` in a browser.
- Page loads with "Projects" heading and rocket-launch icon
- Subtitle text is visible
- Project cards are displayed in a responsive grid
- Each card shows: icon badge, status badge, title, description, tech stack tags
- Cards link to `/projects/{slug}`

### Test 3: Project Detail Page Renders
Click a project card (e.g., `http://localhost:8001/projects/pm-interview-coach`).
- Back link "Back to Projects" is visible and links to `/projects`
- Title, status badge, and description are shown
- Tech stack tags are displayed
- GitHub link button is rendered (if URL is non-empty)
- Rendered markdown content appears in prose-styled container
- Content has proper heading, paragraph, and list styling

### Test 4: 404 for Nonexistent Project
Navigate to `http://localhost:8001/projects/nonexistent`.
- The 404 page renders (not a server error)

### Test 5: Dark Mode Works
Click the dark mode toggle on both the gallery and detail pages.
- All colors swap correctly via CSS variables
- Status badges, tech tags, and card borders adapt to dark theme
- No hardcoded colors remain visible as light-on-light or dark-on-dark

### Test 6: Status Badge Colors Are Correct
Verify that project cards display the correct status badge colors:
- `live` projects show green badge (success colors)
- `in_progress` projects show amber badge (warning colors)
- `case_study` projects show blue badge (accent colors)
- `planned` projects show gray badge (tertiary colors)

### Test 7: Responsive Layout
Resize the browser window:
- **Mobile (< 768px):** Cards stack in a single column
- **Tablet (768px+):** Cards display in 2 columns
- **Desktop (1024px+):** Cards display in 3 columns
- Tech stack tags wrap properly at all sizes

### Test 8: Keyboard Navigation
Tab through the gallery page:
- Each project card receives visible focus ring
- Enter key on a focused card navigates to the detail page
- Back link on detail page is keyboard-accessible

### Test 9: Navbar Highlighting
On both `/projects` and `/projects/{slug}`:
- The "Projects" link in the navbar should be highlighted (active state)
- Other nav links should be in their default secondary color

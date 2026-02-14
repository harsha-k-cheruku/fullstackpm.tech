# Project: fullstackpm.tech — Build Task 04: Resume Page

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

### Tailwind Usage

Reference CSS variables in Tailwind classes using arbitrary values:
- Background: `bg-[var(--color-bg-primary)]`
- Text: `text-[var(--color-text-secondary)]`
- Border: `border-[var(--color-border)]`
- Accent button: `bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)]`

## 4. Coding Conventions

### Python (Backend)
- Use type hints on all function signatures
- Use Pydantic models for request/response schemas
- Use async functions for route handlers
- File naming: lowercase with underscores (e.g., `blog_service.py`)
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

### HTML/Jinja2 (Templates)
- Use semantic HTML5 elements: `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
- All templates extend `base.html`
- Use Jinja2 blocks: `{% block title %}`, `{% block content %}`
- HTMX attributes on elements, not in JavaScript
- Indent with 2 spaces

### Tailwind (Styling)
- Mobile-first responsive: base styles for mobile, `md:` for tablet, `lg:` for desktop
- Use design system tokens (CSS variables) for all colors — never hardcode hex values
- Transitions: `transition-colors duration-150` for hover states
- Border radius: `rounded-lg` for most elements, `rounded-xl` for cards
- Focus rings: `focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2`

### Dark Mode
- Implemented via `class` strategy on `<html>` element
- All color references use CSS custom properties (which automatically swap in dark mode)
- Do NOT use Tailwind `dark:` prefix — use CSS variables instead
- Test both modes

### Accessibility
- All interactive elements must be keyboard-focusable
- Images must have alt text
- Buttons must have accessible labels
- Use ARIA attributes where semantic HTML is insufficient
- Color must not be the only way information is conveyed

## 5. The Task

Build the **Resume page** — a full page showing Harsha Cheruku's career experience timeline, skills grid, education badges, and a download resume CTA.

### A. Route — Add `GET /resume` to `pages.py`

Add a new route to the existing `app/routers/pages.py` following the `_ctx()` pattern used by the other routes. The route should:

- Serve `resume.html` template
- Pass `title="Resume — fullstackpm.tech"`
- Pass `current_page="/resume"`
- Optionally pass career data as context (or hardcode it in the template — your choice, but be consistent)

### B. Template — `app/templates/resume.html`

Create `app/templates/resume.html` extending `base.html`. The page consists of four sections:

---

#### Section B1: Experience Timeline (Component 06 from specs)

A vertical timeline showing career history, most recent first.

**Visual Requirements:**
- Vertical timeline line: 2px wide, `--color-border`, positioned on the left side
- Timeline dots: 8px circle — `--color-accent` for the current role (is_current=true), `--color-border` for past roles
- Each entry contains:
  - Company name: `text-h3` class, `--color-text-primary`
  - Job title: `text-h4` class, `--color-accent`
  - Date range + location: `text-small` class, `--color-text-tertiary`
  - 3-4 bullet points: `text-body` class, `--color-text-secondary`
  - Tech skill badges: small inline badges using `--color-bg-tertiary` background, `--color-text-secondary` text, `rounded-full`, `text-xs`, `px-3 py-1`
- Entries spaced with `mb-8` or `mb-10`

**Responsive Behavior:**
- Desktop (`sm:` and above): Timeline line visible on left, content offset to the right
- Mobile (below `sm`): Timeline line hidden, entries stacked vertically with a left accent border (`border-l-2` or `border-l-4` using `--color-accent`)

**Career Data — hardcode these 6 entries (most recent first):**

```
1. Walmart Global Tech | Sr. Product Manager, Marketplace | Oct 2024 – Present | Sunnyvale, CA
   - Building AI-powered seller tools for Walmart Marketplace (370K+ businesses)
   - Leading cross-functional team across Engineering, Design, Data Science, and Legal
   - Driving GenAI adoption for seller onboarding and product listing optimization
   Skills: Product Strategy, Marketplace, GenAI, A/B Testing, SQL

2. Amazon | Product Manager, Advertising | Aug 2022 – Apr 2024 | Seattle, WA
   - Launched self-service DSP campaigns reaching 22M+ customers
   - Built ML-powered audience targeting reducing CPA by 18%
   - Owned $300M+ annual advertising revenue pipeline
   Skills: Advertising, ML/AI, Audience Targeting, Revenue Growth

3. Delphi Consulting (Amazon contract) | Sr. PM Consultant, Ads | Jun 2021 – Aug 2022 | Seattle, WA
   - Led Amazon Marketing Cloud analytics platform for enterprise advertisers
   - Designed cross-channel attribution models
   Skills: Analytics, Attribution, Enterprise SaaS

4. Verizon | Product Manager, Digital Commerce | Jun 2018 – Jun 2021 | Basking Ridge, NJ
   - Managed B2B e-commerce platform serving Fortune 500 clients
   - Led platform migration from monolith to microservices
   - Increased conversion rate by 24% through UX optimization
   Skills: E-commerce, B2B, Microservices, UX

5. VF Corporation | Product Analyst | May 2016 – May 2018 | Greensboro, NC
   - Built analytics dashboards for supply chain optimization
   - Led data migration for ERP consolidation across 30+ brands
   Skills: Analytics, Supply Chain, ERP, Tableau

6. Wipro Technologies | Software Development Engineer | Aug 2008 – Jun 2014 | Bengaluru, India
   - Full-stack development on enterprise Java/J2EE applications
   - Technical lead for 5-person engineering team
   Skills: Java, J2EE, Oracle DB, Full-Stack Development
```

---

#### Section B2: Skills Grid

A responsive grid of 4 skill categories, displayed as cards.

**Layout:** `grid grid-cols-1 sm:grid-cols-2 gap-6`

**Each card:**
- Background: `--color-bg-secondary`
- Border: 1px `--color-border`, `rounded-xl`
- Padding: `p-6`
- Category title: `text-h4`, `--color-text-primary`, `mb-4`
- Skills: flex-wrap row of badges (`rounded-full`, `text-xs`, `px-3 py-1`, `--color-bg-tertiary` bg, `--color-text-secondary` text)

**Categories and skills:**

| Category | Skills |
|----------|--------|
| Product | Strategy, Roadmap, GTM, Pricing, Marketplace, A/B Testing |
| Technical | Python, SQL, R, FastAPI, AWS, Tableau, Looker |
| AI | Claude API, OpenAI, Prompt Engineering, GenAI, HeyGen, MidJourney |
| Leadership | Cross-functional, Coaching, Stakeholder Management, P&L |

---

#### Section B3: Education

A row of education/certification badges.

**Layout:** flex-wrap row with `gap-3`

**Each badge:**
- Background: `--color-accent-light`
- Text: `--color-accent`  (in light mode) — since CSS variables handle dark mode, just use `--color-accent` for text
- `rounded-full`, `text-sm`, `px-4 py-2`, `font-medium`

**Entries:**
1. Duke MBA
2. MIT Data Science
3. Columbia Executive Programs
4. JNTU CS
5. AWS Cloud Practitioner

---

#### Section B4: Download Resume CTA

A prominent button linking to the static PDF file.

**Specifications:**
- Link target: `/static/resume.pdf`
- Style: Primary button — `bg-[var(--color-accent)]`, `hover:bg-[var(--color-accent-hover)]`, white text, `rounded-lg`, `px-6 py-3`, `font-semibold`, `text-body`
- Include a download icon (Heroicons `arrow-down-tray` outline, 20px) before the text
- Text: "Download Resume"
- Add `download` attribute to the `<a>` tag
- Center the button or place it at the end of the page
- Add `transition-colors duration-150`
- Focus ring: `focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2`

---

### Reference Files

Below are the FULL contents of every existing file you must reference. Do NOT modify any file except `pages.py` (to add the route). Do NOT create any files other than what is listed in Expected Output.

#### File: `app/routers/pages.py` (CURRENT — you will ADD a route to this file)

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

#### File: `app/templates/base.html` (DO NOT MODIFY — your template extends this)

```html
<!DOCTYPE html>
<html lang="en" class="">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}{{ title | default("fullstackpm.tech") }}{% endblock %}</title>
  <meta name="description" content="{% block description %}{{ meta_description | default("Portfolio of Harsha Cheruku — Full Stack AI Product Manager") }}{% endblock %}">
  <meta name="author" content="Harsha Cheruku">
  <meta property="og:title" content="{% block og_title %}{{ title | default("fullstackpm.tech") }}{% endblock %}">
  <meta property="og:description" content="{% block og_description %}{{ meta_description | default("Portfolio of Harsha Cheruku — Full Stack AI Product Manager") }}{% endblock %}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{ config.site_url }}{{ request.url.path }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: { extend: { fontFamily: { sans: ['Geist Sans', 'system-ui', '-apple-system', 'sans-serif'], mono: ['JetBrains Mono', 'monospace'] } } }
    }
  </script>
  <link rel="stylesheet" href="/static/css/custom.css">
  <script>
    (function() {
      var theme = localStorage.getItem('theme');
      if (!theme) { theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; }
      if (theme === 'dark') { document.documentElement.classList.add('dark'); }
    })();
  </script>
  {% block head %}{% endblock %}
</head>
<body class="min-h-screen font-sans antialiased" style="background-color: var(--color-bg-primary); color: var(--color-text-primary);">
  {% include "partials/navbar.html" %}
  <main class="mx-auto max-w-[1200px] px-4 sm:px-6">
    {% block content %}{% endblock %}
  </main>
  {% include "partials/footer.html" %}
  <script src="https://unpkg.com/htmx.org@2.0.2" integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwCXuE+cDVtAu2B3crQxD" crossorigin="anonymous"></script>
  <script src="/static/js/main.js"></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

#### File: `app/templates/about.html` (REFERENCE ONLY — do NOT modify; use as visual pattern reference for the timeline)

```html
{% extends "base.html" %}
{% block content %}
<section class="py-16 lg:py-20">
  <div class="max-w-3xl">
    <h1 class="text-h1 mb-6" style="color: var(--color-text-primary);">About</h1>
    <p class="text-body-lg mb-12" style="color: var(--color-text-secondary);">...</p>
    <div class="mb-12 flex gap-5">
      <div class="hidden sm:block flex-shrink-0">
        <div class="flex h-11 w-11 items-center justify-center rounded-xl"
             style="background-color: var(--color-bg-tertiary);">
          <!-- Heroicon: code-bracket -->
          <svg class="h-5 w-5" style="color: var(--color-accent);" ...></svg>
        </div>
        <div class="mx-auto mt-2 h-full w-px" style="background-color: var(--color-border);"></div>
      </div>
      <div>
        <p class="text-xs font-semibold uppercase tracking-wider mb-1" style="color: var(--color-accent);">Chapter 1</p>
        <h2 class="text-h2 mb-3" style="color: var(--color-text-primary);">The Engineer</h2>
        <p class="text-body" style="color: var(--color-text-secondary);">...</p>
      </div>
    </div>
    <!-- More chapters follow same pattern -->
  </div>
</section>
{% endblock %}
```

#### File: `app/static/css/custom.css` (DO NOT MODIFY — full contents for reference)

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
  font-weight: 700;
  margin-top: 3rem;
  margin-bottom: 1rem;
  color: var(--color-text-primary);
}

.prose h3 {
  font-size: 1.375rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
}

.prose p {
  margin-bottom: 1rem;
  line-height: 1.7;
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

---

### Scope Boundaries

- **IN scope:** Updated `app/routers/pages.py` with `/resume` route, new `app/templates/resume.html` template
- **OUT of scope:** Navbar changes, other pages, ContentService, any backend services, custom.css modifications, base.html modifications, any JavaScript changes

**Note:** The navbar currently includes links to: Home (/), Projects (/projects), Blog (/blog), About (/about), Contact (/contact). There may or may not already be a "Resume" link in the navbar. Do NOT modify the navbar. Passing `current_page="/resume"` from the route will not break anything — if there is no matching nav link it simply means no link will be highlighted, which is acceptable.

## 6. Expected Output

Return these COMPLETE files:

1. **Updated `app/routers/pages.py`** — The existing file with the new `/resume` route added at the bottom, following the same pattern as the other routes. Do not change any existing routes.

2. **New `app/templates/resume.html`** — The complete resume page template with all four sections (Experience Timeline, Skills Grid, Education, Download CTA).

### Output Rules

- Return COMPLETE files, not snippets or diffs
- Include the file path as a comment at the top of each Python file
- Do not add features beyond what was specified
- Do not refactor existing code unless the task asks for it
- Do not create any additional files (no new CSS, no new JS, no new partials)
- Use only CSS custom properties for colors — never hardcode hex values in templates
- Use inline `style="..."` attributes with `var()` for colors, combined with Tailwind utility classes for layout/spacing
- All Heroicons must be inline SVG (copy the SVG path data directly into the template)

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
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── pages.py         # Routes: /, /about, /contact — YOU ADD /resume HERE
│   │   ├── services/
│   │   │   └── __init__.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── 404.html
│   │   │   ├── resume.html      # YOU CREATE THIS
│   │   │   ├── projects/
│   │   │   ├── blog/
│   │   │   └── partials/
│   │   │       ├── navbar.html
│   │   │       └── footer.html
│   │   └── static/
│   │       ├── css/custom.css
│   │       ├── js/main.js
│   │       └── img/
│   ├── content/
│   │   ├── blog/
│   │   └── projects/
│   ├── tests/
│   ├── requirements.txt
│   └── Procfile
```

All file paths in your output are **relative to `code/`**. For example, the route file is at `code/app/routers/pages.py` on disk but referenced as `app/routers/pages.py` in the project.

## 8. Acceptance Test

After implementing, verify all of the following:

### Test 1: Server Starts Without Errors
```bash
cd code && python3 -m uvicorn app.main:app --reload --port 8001
```
The server should start cleanly with no import errors or exceptions.

### Test 2: Resume Page Loads
Open `http://localhost:8001/resume` in a browser. The page should render without errors and display the full resume content.

### Test 3: Experience Timeline — All 6 Roles Visible
Verify that all 6 career entries are displayed in order (most recent first):
1. Walmart Global Tech — Sr. Product Manager, Marketplace
2. Amazon — Product Manager, Advertising
3. Delphi Consulting (Amazon contract) — Sr. PM Consultant, Ads
4. Verizon — Product Manager, Digital Commerce
5. VF Corporation — Product Analyst
6. Wipro Technologies — Software Development Engineer

Each entry should show: company name, title, date range, location, bullet points, and skill badges.

### Test 4: Current Role is Visually Distinguished
The Walmart Global Tech entry (the only one with "Present" in the date range) should have an accent-colored timeline dot (`--color-accent`), while all past roles have a neutral dot (`--color-border`).

### Test 5: Skills Grid Shows 4 Categories
Verify a 2-column grid (on desktop) with:
- Product: 6 skills
- Technical: 7 skills
- AI: 6 skills
- Leadership: 4 skills

Each skill should appear as a small rounded badge.

### Test 6: Education Badges Present
Verify 5 education/certification badges displayed in a row:
- Duke MBA
- MIT Data Science
- Columbia Executive Programs
- JNTU CS
- AWS Cloud Practitioner

### Test 7: Download Resume Button
A "Download Resume" button/link should be visible, linking to `/static/resume.pdf`. The link should have a `download` attribute.

### Test 8: Dark Mode Toggle
Click the dark mode toggle in the navbar. The entire resume page should switch to dark mode with correct colors:
- Background changes from white to black
- Text colors invert appropriately
- Borders, badges, and accent colors adapt via CSS variables
- No hardcoded colors remain visible (everything should respond to the toggle)

### Test 9: Responsive — Mobile View
Resize the browser to mobile width (< 640px) or use browser DevTools mobile view:
- The timeline vertical line should be hidden
- Experience entries should stack vertically with a left accent border instead
- Skills grid should collapse to a single column
- Education badges should wrap naturally
- No horizontal scroll should appear
- All text should remain readable

### Test 10: Keyboard Navigation and Accessibility
- Tab through the page — the Download Resume button should receive a visible focus ring
- The page heading should use proper `<h1>` tag
- Section headings should follow correct heading hierarchy (h1 > h2 > h3)
- The page should use semantic HTML (`<section>`, `<article>`, `<ul>` for lists)

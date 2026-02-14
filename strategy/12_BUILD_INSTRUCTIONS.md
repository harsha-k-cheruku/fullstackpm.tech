# Standard Build Instruction Protocol

## Purpose

This is a **reusable instruction template** for giving any LLM, developer, or AI coding assistant a task on the fullstackpm.tech project. It ensures:

- Every builder gets the same context and constraints
- Output is in a consistent, predictable format
- Results are comparable across LLMs for benchmarking
- No ambiguity about tech stack, conventions, or file structure

---

## How to Use This

1. Copy the **Instruction Template** below
2. Fill in **Section 5 (The Task)** with what you want built
3. Attach the relevant reference docs (or paste their contents)
4. Send to any LLM or developer

For quick tasks, use the **Short Form**. For full components or pages, use the **Full Form**.

---

## Instruction Template — Full Form

Copy everything between the `---START---` and `---END---` markers.

```
---START INSTRUCTION---

# Project: fullstackpm.tech

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
| Styling | **Tailwind CSS** (CDN for now) | Use utility classes only. No custom CSS unless absolutely necessary |
| Interactivity | **HTMX** (CDN) | For dynamic partial updates. No React/Vue/Angular/Svelte |
| Icons | **Heroicons** (inline SVG) | Outline style 24px for UI, Solid 20px for inline |
| Fonts | **Inter** (headings + body) + **JetBrains Mono** (code) | Via Google Fonts CDN |
| Database | **SQLite** (if needed) | Via SQLAlchemy async or aiosqlite |
| Content | **Markdown files** with YAML frontmatter | Parsed at startup, cached in memory |
| Deployment | **Render** | Procfile included |

**Do NOT use:** React, Vue, Angular, Svelte, Next.js, npm/node, webpack, any JavaScript framework, any CSS preprocessor (SCSS/LESS), Bootstrap, any ORM other than SQLAlchemy.

## 3. Color System (Mandatory — Use These Exact Values)

### CSS Custom Properties

```css
:root {
  /* Backgrounds */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F7F7F7;
  --color-bg-tertiary: #EEEEEE;

  /* Text */
  --color-text-primary: #000000;
  --color-text-secondary: #555555;
  --color-text-tertiary: #999999;

  /* Borders */
  --color-border: #E0E0E0;
  --color-border-hover: #CCCCCC;

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
  --color-bg-primary: #000000;
  --color-bg-secondary: #111111;
  --color-bg-tertiary: #1A1A1A;
  --color-text-primary: #FFFFFF;
  --color-text-secondary: #AAAAAA;
  --color-text-tertiary: #666666;
  --color-border: #222222;
  --color-border-hover: #333333;
  --color-accent-light: #1A3A52;
  --color-success-bg: #0B3D20;
  --color-warning-bg: #4A3F00;
  --color-danger-bg: #4A1A15;
}
```

### Tailwind Usage

Reference CSS variables in Tailwind classes using arbitrary values:
- Background: `bg-[var(--color-bg-primary)]`
- Text: `text-[var(--color-text-secondary)]`
- Border: `border-[var(--color-border)]`
- Accent button: `bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)]`

Or use the Tailwind config aliases if available:
- `bg-surface-primary`, `text-content-secondary`, `bg-accent`, etc.

## 4. Coding Conventions

### Python (Backend)
- Use type hints on all function signatures
- Use Pydantic models for request/response schemas
- Use async functions for route handlers
- File naming: lowercase with underscores (e.g., `blog_service.py`)
- Imports: stdlib first, then third-party, then local (separated by blank lines)
- No unused imports, no commented-out code

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

> **[FILL THIS IN — describe what you want built]**
>
> Examples:
> - "Build the Navigation Bar component (Component 01 from the component specs)"
> - "Build the Home page including hero section, featured projects, and latest blog post"
> - "Build the ContentService that parses markdown files with YAML frontmatter"
> - "Build the complete blog system: routes, service, templates for list/detail/tag pages"

### Reference Documents

> **[ATTACH OR PASTE the relevant spec documents]**
>
> Choose from:
> - Design System: `strategy/09_DESIGN_SYSTEM.md` (always include for UI tasks)
> - Component Specs: `strategy/10_COMPONENT_SPECS.md` (for specific components)
> - Portfolio Site Spec: `strategy/01_PORTFOLIO_SITE.md` (for pages and architecture)
> - Project-specific spec: `strategy/02-08_*.md` (for individual projects)

### Scope Boundaries

> **[FILL THIS IN — what is IN and OUT of scope]**
>
> Example:
> - IN: Navigation bar HTML/Jinja2 template, mobile hamburger menu, dark mode toggle
> - OUT: Blog content, page routes, database setup

## 6. Expected Output Format

### For UI Components (Templates)
Return the following files:

1. **Jinja2 template file(s)** — Complete, ready to save to the templates directory
   - File path: specify where it goes (e.g., `app/templates/partials/navbar.html`)
   - Must extend `base.html` if it's a full page
   - Must be a standalone partial if it's a component

2. **Any required JavaScript** — Minimal vanilla JS only (for dark mode toggle, mobile menu, etc.)
   - File path: `app/static/js/filename.js`
   - No frameworks, no jQuery

3. **Any required CSS** — Only if Tailwind classes are insufficient
   - Add to `app/static/css/custom.css`

### For Backend Code (Python)
Return the following files:

1. **Python source file(s)** — Complete, ready to save
   - File path: specify where it goes (e.g., `app/services/content.py`)
   - Include all imports
   - Include type hints

2. **Route registrations** — Show how to register new routers in `main.py`

3. **Requirements** — List any new pip packages needed (if any)

### For Full Pages (Template + Route)
Return:
1. The Jinja2 template
2. The FastAPI route handler
3. Any service/helper code
4. Any new content files (markdown)

### Output Rules
- Return COMPLETE files, not snippets or diffs
- Include the file path as a comment at the top of each file
- Do not explain the code unless asked — just return the code
- Do not add features beyond what was specified in the task
- Do not refactor existing code unless the task specifically asks for it

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
│   │   │   ├── pages.py
│   │   │   ├── projects.py
│   │   │   └── blog.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── content.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── resume.html
│   │   │   ├── projects/
│   │   │   │   ├── gallery.html
│   │   │   │   └── detail.html
│   │   │   ├── blog/
│   │   │   │   ├── list.html
│   │   │   │   ├── detail.html
│   │   │   │   └── tag.html
│   │   │   └── partials/
│   │   │       ├── navbar.html
│   │   │       ├── footer.html
│   │   │       └── project_card.html
│   │   └── static/
│   │       ├── css/
│   │       │   └── custom.css
│   │       ├── js/
│   │       │   └── main.js
│   │       └── img/
│   ├── content/
│   │   ├── blog/
│   │   └── projects/
│   ├── tests/
│   ├── requirements.txt
│   ├── Procfile
│   └── README.md
├── test_harness/          # LLM comparison tool (separate from main site)
└── README.md
```

> **[UPDATE THIS if the structure has changed since you started building]**

---END INSTRUCTION---
```

---

## Instruction Template — Short Form

For quick tasks where the full context isn't needed (bug fixes, small tweaks, adding a route):

```
---START SHORT INSTRUCTION---

# Project: fullstackpm.tech
# Stack: FastAPI + Jinja2 + Tailwind CSS (CDN) + HTMX
# Colors: CSS variables (see custom.css) — never hardcode hex values
# Dark mode: via CSS variables, NOT Tailwind dark: prefix
# No JS frameworks. No npm. No React/Vue.

## Task
[DESCRIBE WHAT YOU WANT]

## Files to Modify
[LIST THE FILES, or say "you decide"]

## Constraints
[ANYTHING SPECIFIC — e.g., "don't change the nav", "keep it under 50 lines"]

---END SHORT INSTRUCTION---
```

---

## Quick Reference: Which Docs to Attach

| Task Type | Docs to Include |
|-----------|----------------|
| UI Component | Design System + Component Spec for that component |
| Full Page | Design System + Portfolio Site Spec (page section) + relevant Component Specs |
| Backend Service | Portfolio Site Spec (architecture section) |
| Blog System | Portfolio Site Spec + Design System |
| Project Build (e.g., Interview Coach) | That project's spec doc (02-08) + Design System |
| Bug Fix / Tweak | Short Form only (no docs needed) |
| LLM Benchmark | Design System + Component Spec (ONE component only) |

---

## Example: Giving a Task to Another LLM

### You want GPT-4 to build the Navigation Bar:

1. Copy the Full Form template
2. Fill in Section 5:
   ```
   ## 5. The Task
   Build the Navigation Bar component.

   ### Reference Documents
   [Paste contents of 10_COMPONENT_SPECS.md — Component 01 section only]

   ### Scope Boundaries
   - IN: navbar.html partial, mobile menu toggle JS, dark mode toggle JS
   - OUT: base.html, page routes, all other components
   ```
3. Paste the entire filled template to GPT-4
4. Save GPT-4's output to `test_harness/outputs/navbar/gpt4.html`
5. Give me the same task: "Build Component 01: Navigation Bar"
6. Save my output to `test_harness/outputs/navbar/claude.html`
7. Open the test harness and compare

### You want me to build the Home page:

Just say: **"Build the Home page"**

I already have access to all the docs. I'll confirm scope, then build it. No template needed when working with me directly.

---

## Version Control

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-02-11 | Initial protocol created |

Update this document if the tech stack, color system, or project structure changes.

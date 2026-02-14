# Project: fullstackpm.tech — Build Task 07: Project Card Component

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
| Icons | **Heroicons** (inline SVG) | Outline style, 24px viewBox |
| Fonts | **Geist Sans** + **JetBrains Mono** | Via Google Fonts CDN |
| Content | **Markdown files** with YAML frontmatter | Parsed at startup, cached in memory |
| Deployment | **Render** | Procfile included |

**Do NOT use:** React, Vue, Angular, Svelte, Next.js, npm/node, webpack, any JS framework, Bootstrap, SCSS/LESS.

## 3. Color System

The project uses CSS custom properties defined in `app/static/css/custom.css`. Here is the FULL color system — you MUST use these variables for every color in the component. Never hardcode hex values.

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

### Jinja2 Templates
- All page templates extend `base.html` using `{% extends "base.html" %}`
- Partial templates (components) are included via `{% include "partials/component_name.html" %}`
- Partials do NOT extend base.html — they are fragments meant to be included by parent templates
- Use semantic HTML5 elements (`<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`)

### Tailwind CSS
- Mobile-first responsive design using `md:` and `lg:` breakpoint prefixes
- Use `rounded-xl` for card-level elements
- Use `rounded-lg` for smaller elements inside cards (badges, icon containers)
- Use `rounded-md` for tech stack tags
- Use `rounded-full` for status badges (pill shape)

### Colors — CSS Variables Only
- **NEVER** hardcode hex color values in templates
- Apply colors via inline `style` attributes referencing CSS variables: `style="color: var(--color-text-primary);"`
- For Tailwind classes that accept arbitrary values, use bracket notation: `bg-[var(--color-bg-secondary)]`
- Both approaches are used in the codebase; follow existing patterns

### Transitions
- Use `transition-all duration-150` for hover effects on cards
- Use `transition-colors duration-150` for text/border color changes
- Hover states are applied via `onmouseover` / `onmouseout` inline handlers (this is the established pattern)

### Accessibility
- All interactive elements must be keyboard-focusable
- Focus ring pattern: `focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2`
- Use `aria-label` for elements where visual meaning is not conveyed by text alone
- Use `aria-current="page"` for active navigation links

### Icons
- Heroicons outline style, 24px viewBox (`viewBox="0 0 24 24"`)
- Rendered as inline SVG (not icon fonts, not external files)
- Icon sizing via Tailwind: `h-5 w-5` inside icon badges, `h-4 w-4` for inline icons
- Icon color via `style="color: var(--color-accent);"` and `stroke="currentColor"`

## 5. The Task

Build the **Project Card** component as a Jinja2 partial template.

This is **Component 03** from the component specs.

### File to Create

```
app/templates/partials/project_card.html
```

### Component Spec: Project Card

**Description:** A card displaying a project summary in the project gallery grid. Clickable — the entire card navigates to the project detail page.

### Props/Inputs (Jinja2 Variables)

The partial receives a `project` variable with the following fields:

```
project.title: string          — Project name
project.description: string    — One-line description (max 120 chars)
project.tech_stack: string[]   — Array of technology names
project.status: string         — "live" | "in_progress" | "case_study" | "planned"
project.slug: string           — URL slug for detail page
project.thumbnail: string?     — Optional image path (may be null/undefined)
```

### Visual Requirements

**Card container:**
- Background: `var(--color-bg-secondary)`
- Border: 1px solid `var(--color-border)`
- Border radius: `rounded-xl`
- Padding: `p-6` (when no thumbnail) or `p-0` with content in a `p-6` div below (when thumbnail exists)

**Hover state:**
- Border color transitions to `var(--color-border-hover)`
- Add subtle shadow: `0 1px 3px 0 rgb(0 0 0 / 0.1)`
- Transition duration: 150ms
- Cursor: pointer

**Icon badge (top-left of content area):**
- Size: 40x40px (`h-10 w-10`)
- Background: `var(--color-accent-light)`
- Border radius: `rounded-lg`
- Contains a Heroicon (outline, 24px) in `var(--color-accent)` color at `h-5 w-5`
- Use the `command-line` Heroicon as a generic project icon (a terminal/code icon fits the portfolio theme)

**Title:**
- Typography class: `text-h4`
- Color: `var(--color-text-primary)`
- Bottom margin: `mb-2`

**Description:**
- Typography class: `text-body`
- Color: `var(--color-text-secondary)`
- Bottom margin: `mb-4`

**Tech stack tags:**
- Layout: flex row with wrapping — `flex flex-wrap gap-2`
- Each tag: `text-xs rounded-md px-2 py-1 font-medium`
- Tag background: `var(--color-bg-tertiary)`
- Tag text color: `var(--color-text-secondary)`

**Status badge (top-right of content area):**
- Shape: pill — `text-xs rounded-full px-2.5 py-1 font-medium`
- Position: in a flex row with the icon badge, pushed to the right via `justify-between`
- Must include `aria-label` with human-readable status
- Semantic colors per status value:

| Status value | Background variable | Text variable | Display label | aria-label |
|---|---|---|---|---|
| `live` | `var(--color-success-bg)` | `var(--color-success)` | Live | `Status: Live` |
| `in_progress` | `var(--color-warning-bg)` | `var(--color-warning)` | In Progress | `Status: In Progress` |
| `case_study` | `var(--color-accent-light)` | `var(--color-accent)` | Case Study | `Status: Case Study` |
| `planned` | `var(--color-bg-tertiary)` | `var(--color-text-tertiary)` | Planned | `Status: Planned` |

**Thumbnail (optional):**
- If `project.thumbnail` is defined/truthy: display an `<img>` at the top of the card
- Image classes: `rounded-t-xl w-full aspect-video object-cover`
- Image `alt` attribute: `project.title`
- When thumbnail is present, card padding is `p-0` and all text content is wrapped in a `<div class="p-6">`
- When no thumbnail: card padding is `p-6` directly on the link/card element (no wrapper div needed, but using one is acceptable for consistency)

**Entire card is a link:**
- Wrap everything in `<a href="/projects/{{ project.slug }}">`
- The `<a>` tag gets the card styling classes: `block rounded-xl border transition-all duration-150`
- Focus ring on the `<a>`: `focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2`

### Behavior

- Click anywhere on the card navigates to `/projects/{{ project.slug }}`
- Hover: border color and shadow transition (150ms) applied via `onmouseover` / `onmouseout` inline handlers
- No other interactivity — no expand, no modal, no HTMX calls

### Responsive

- The card is always full-width of its grid cell
- The parent page handles the grid layout (e.g., `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`), NOT this component
- Tech stack tags wrap naturally at narrow widths via `flex-wrap`

### Accessibility

- The entire card is wrapped in an `<a>` element, making it keyboard-focusable by default
- Focus ring: `focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2`
- Status badge has `aria-label` (e.g., `aria-label="Status: Live"`)
- Tech stack badges are decorative — no special aria role needed
- Image (if present) has `alt="{{ project.title }}"` attribute

### Reference HTML Structure

This is the target structure. Your implementation should match this closely:

```html
<a href="/projects/{{ project.slug }}"
   class="block rounded-xl border transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2"
   style="background-color: var(--color-bg-secondary); border-color: var(--color-border); cursor: pointer;"
   onmouseover="this.style.borderColor='var(--color-border-hover)'; this.style.boxShadow='0 1px 3px 0 rgb(0 0 0 / 0.1)'"
   onmouseout="this.style.borderColor='var(--color-border)'; this.style.boxShadow='none'">

  <!-- Optional thumbnail -->
  {% if project.thumbnail %}
  <img src="{{ project.thumbnail }}"
       alt="{{ project.title }}"
       class="rounded-t-xl w-full aspect-video object-cover">
  {% endif %}

  <div class="p-6">
    <!-- Icon badge + Status badge row -->
    <div class="mb-4 flex items-start justify-between">
      <!-- Icon badge -->
      <div class="flex h-10 w-10 items-center justify-center rounded-lg"
           style="background-color: var(--color-accent-light);">
        <!-- Heroicon: command-line (outline, 24px) -->
        <svg class="h-5 w-5" style="color: var(--color-accent);" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="m6.75 7.5 3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0 0 21 18V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v12a2.25 2.25 0 0 0 2.25 2.25Z" />
        </svg>
      </div>

      <!-- Status badge -->
      {% if project.status == "live" %}
      <span class="text-xs rounded-full px-2.5 py-1 font-medium"
            style="background-color: var(--color-success-bg); color: var(--color-success);"
            aria-label="Status: Live">
        Live
      </span>
      {% elif project.status == "in_progress" %}
      <span class="text-xs rounded-full px-2.5 py-1 font-medium"
            style="background-color: var(--color-warning-bg); color: var(--color-warning);"
            aria-label="Status: In Progress">
        In Progress
      </span>
      {% elif project.status == "case_study" %}
      <span class="text-xs rounded-full px-2.5 py-1 font-medium"
            style="background-color: var(--color-accent-light); color: var(--color-accent);"
            aria-label="Status: Case Study">
        Case Study
      </span>
      {% elif project.status == "planned" %}
      <span class="text-xs rounded-full px-2.5 py-1 font-medium"
            style="background-color: var(--color-bg-tertiary); color: var(--color-text-tertiary);"
            aria-label="Status: Planned">
        Planned
      </span>
      {% endif %}
    </div>

    <!-- Title -->
    <h3 class="text-h4 mb-2" style="color: var(--color-text-primary);">{{ project.title }}</h3>

    <!-- Description -->
    <p class="text-body mb-4" style="color: var(--color-text-secondary);">{{ project.description }}</p>

    <!-- Tech stack tags -->
    <div class="flex flex-wrap gap-2">
      {% for tech in project.tech_stack %}
      <span class="text-xs rounded-md px-2 py-1 font-medium"
            style="background-color: var(--color-bg-tertiary); color: var(--color-text-secondary);">
        {{ tech }}
      </span>
      {% endfor %}
    </div>
  </div>
</a>
```

### Existing Pattern to Match

The home page (`home.html`) already has project cards with a similar visual structure. Here is the existing pattern for reference — your partial should match this style exactly:

```html
<!-- From home.html — Featured Projects section -->
<div class="group rounded-xl border p-6 transition-all duration-150"
     style="background-color: var(--color-bg-secondary); border-color: var(--color-border);"
     onmouseover="this.style.borderColor='var(--color-border-hover)'; this.style.boxShadow='0 1px 3px 0 rgb(0 0 0 / 0.1)'"
     onmouseout="this.style.borderColor='var(--color-border)'; this.style.boxShadow='none'">

  <!-- Icon + Status row -->
  <div class="mb-4 flex items-start justify-between">
    <div class="flex h-10 w-10 items-center justify-center rounded-lg"
         style="background-color: var(--color-accent-light);">
      <svg class="h-5 w-5" style="color: var(--color-accent);" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <!-- ... Heroicon path ... -->
      </svg>
    </div>
    <span class="text-xs rounded-full px-2.5 py-1 font-medium"
          style="background-color: var(--color-warning-bg); color: var(--color-warning);">
      In Progress
    </span>
  </div>

  <!-- Title + Description -->
  <h3 class="text-h4 mb-2" style="color: var(--color-text-primary);">{{ project.title }}</h3>
  <p class="text-body mb-4" style="color: var(--color-text-secondary);">{{ project.desc }}</p>

  <!-- Tags -->
  <div class="flex flex-wrap gap-2">
    {% for tag in project.tags %}
    <span class="text-xs rounded-md px-2 py-1 font-medium"
          style="background-color: var(--color-bg-tertiary); color: var(--color-text-secondary);">
      {{ tag }}
    </span>
    {% endfor %}
  </div>
</div>
```

The key differences in your new partial versus the home page pattern:
1. The card is wrapped in an `<a>` tag (making it a link) instead of a plain `<div>`
2. The card supports an optional thumbnail image
3. The status badge uses proper semantic colors for all 4 status values (not just two)
4. The status badge includes `aria-label` attributes
5. The `<a>` tag has a focus ring for keyboard accessibility

### Full custom.css File (Typography Classes Reference)

Your component uses the `text-h4`, `text-body`, `text-xs`, and `text-small` typography classes. Here is the FULL `custom.css` file so you understand every available class:

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
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin-top: 3rem;
  margin-bottom: 1rem;
  color: var(--color-text-primary);
}

.prose h3 {
  font-size: 1.375rem;
  font-weight: 600;
  line-height: 1.25;
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

### Scope Boundaries

- **IN scope:** `app/templates/partials/project_card.html` partial template only
- **OUT of scope:** Gallery page, routes, grid layout, ContentService, base.html, custom.css, any Python files

## 6. Expected Output

Return exactly **one** complete file:

1. **`app/templates/partials/project_card.html`** — Complete Jinja2 partial template

### Output Rules

- Return the COMPLETE file, not a snippet or diff
- The file must be a valid Jinja2 partial (no `{% extends %}`, no `{% block %}` definitions)
- Do not add features beyond what was specified
- Do not create or modify any other files
- Every color must use CSS custom properties — zero hardcoded hex values
- The component must work in both light mode and dark mode without any modifications (the CSS variables handle the theming)

## 7. Current Project Structure

```
fullstackpm.tech/
├── strategy/                          # Planning docs (DO NOT modify)
│   ├── README.md
│   └── build_tasks/
│       ├── README.md
│       ├── BUILD_01_CONTENT_SERVICE.md
│       └── BUILD_07_PROJECT_CARD.md   # This file
├── code/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app with lifespan
│   │   ├── config.py                  # Pydantic settings
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── pages.py              # Routes: /, /about, /contact
│   │   ├── services/
│   │   │   └── __init__.py
│   │   ├── templates/
│   │   │   ├── base.html             # Base layout (extends nothing)
│   │   │   ├── home.html             # Home page (extends base.html)
│   │   │   ├── about.html            # About page (extends base.html)
│   │   │   ├── contact.html          # Contact page (extends base.html)
│   │   │   ├── 404.html              # Error page
│   │   │   ├── projects/             # Empty — future project pages
│   │   │   ├── blog/                 # Empty — future blog pages
│   │   │   └── partials/
│   │   │       ├── navbar.html       # Navigation bar partial
│   │   │       ├── footer.html       # Footer partial
│   │   │       └── project_card.html # <-- YOU ARE BUILDING THIS
│   │   └── static/
│   │       ├── css/
│   │       │   └── custom.css        # Design system tokens + typography
│   │       ├── js/
│   │       │   └── main.js           # Theme toggle + mobile menu
│   │       └── img/                  # Static images
│   ├── content/
│   │   ├── blog/                     # Markdown blog posts
│   │   └── projects/                 # Markdown project pages
│   ├── tests/
│   │   └── __init__.py
│   ├── requirements.txt
│   └── Procfile
```

All file paths are **relative to `code/`**. The partial you are building goes at `code/app/templates/partials/project_card.html`.

## 8. Acceptance Test

After creating the partial, verify correctness by performing the following checks:

### Test 1: Include the Partial in a Test Page

Create a temporary test by adding this to any existing template (e.g., temporarily in `home.html`) or inspecting the partial directly:

```html
{% set test_projects = [
  {"title": "PM Interview Coach", "description": "AI-powered practice tool using real PM frameworks and Claude API.", "tech_stack": ["FastAPI", "Claude API", "HTMX"], "status": "live", "slug": "pm-interview-coach", "thumbnail": null},
  {"title": "Marketplace Dashboard", "description": "Interactive analytics with synthetic 3P marketplace data.", "tech_stack": ["FastAPI", "Pandas", "Plotly"], "status": "in_progress", "slug": "marketplace-dashboard", "thumbnail": null},
  {"title": "AI PM Toolkit", "description": "Generate PRDs, roadmaps, and user stories with structured AI.", "tech_stack": ["FastAPI", "Claude API", "Jinja2"], "status": "case_study", "slug": "ai-pm-toolkit", "thumbnail": "/static/img/sample-thumb.jpg"},
  {"title": "Design System", "description": "Component library and token system for fullstackpm.tech.", "tech_stack": ["Tailwind CSS", "Jinja2"], "status": "planned", "slug": "design-system", "thumbnail": null},
] %}

<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
  {% for project in test_projects %}
    {% include "partials/project_card.html" %}
  {% endfor %}
</div>
```

### Test 2: Verify All 4 Status Values Render Correctly

Visually inspect each card and confirm:
- **live** card: Green background badge, green text reading "Live"
- **in_progress** card: Yellow/amber background badge, yellow text reading "In Progress"
- **case_study** card: Blue-tinted background badge, blue text reading "Case Study"
- **planned** card: Gray background badge, gray text reading "Planned"

### Test 3: Verify Dark Mode

Toggle dark mode (click the moon/sun icon in the navbar) and confirm:
- Card backgrounds change from light gray to dark gray
- Text colors invert appropriately
- Border colors update
- Status badge backgrounds use dark-mode overrides
- Tech stack tag backgrounds update

### Test 4: Verify Hover States

Mouse over each card and confirm:
- Border color transitions smoothly (150ms)
- Subtle box shadow appears
- Cursor is pointer
- On mouseout, border and shadow revert

### Test 5: Verify Keyboard Accessibility

Tab through the cards using the keyboard and confirm:
- Each card receives focus (visible focus ring with accent color)
- Focus ring has proper offset (`ring-offset-2`)
- Pressing Enter navigates to the project URL

### Test 6: Verify Thumbnail Behavior

- Cards without `thumbnail` (or `thumbnail: null`) should render without an image area — just the padded content
- The card with a thumbnail should show an image at the top with `rounded-t-xl` corners and 16:9 aspect ratio
- Content below the thumbnail should be in a `p-6` container

### Test 7: Verify No Hardcoded Hex Colors

Search the partial file for any `#` character (outside of comments). There should be zero matches — all colors must come from CSS variables.

### Acceptance Criteria Checklist

- [ ] Card renders with all data fields populated (title, description, tech stack, status, link)
- [ ] Status badge shows correct color per status value (test all 4: live, in_progress, case_study, planned)
- [ ] Tech stack tags wrap gracefully at narrow widths
- [ ] Hover transition is smooth (150ms duration)
- [ ] Click navigates to `/projects/{slug}`
- [ ] Card looks correct with thumbnail present
- [ ] Card looks correct without thumbnail
- [ ] Works in light mode
- [ ] Works in dark mode
- [ ] Focus ring visible on keyboard Tab navigation
- [ ] Status badge has `aria-label` attribute
- [ ] No hardcoded hex colors — all colors from CSS variables
- [ ] Uses `text-h4` typography class for title
- [ ] Uses `text-body` typography class for description
- [ ] Uses `text-xs` typography class for tags and status badge
- [ ] Icon badge is 40x40px with `rounded-lg` and accent-light background
- [ ] Heroicon is inline SVG, outline style, 24px viewBox

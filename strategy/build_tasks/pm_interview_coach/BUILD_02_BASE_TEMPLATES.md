# BUILD_02_BASE_TEMPLATES.md

## Section 1: Project Overview

**Project Name:** PM Interview Coach

**Purpose:** An AI-powered interview practice tool that presents questions from a curated question bank, evaluates answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

**Owner:** Harsha Cheruku (fullstackpm.tech)

**How This Task Fits:** This task establishes the shared UI foundation for the PM Interview Coach app. It creates the base layout, navigation, footer, and app-specific CSS overrides that all subsequent pages will extend. It is independent of the database and AI layers, enabling parallel development of UI and backend logic.

**What This Task Builds:**
- Base template (`app/templates/base.html`) that extends the portfolio base layout
- App-specific navigation partial with Home | History | Progress links
- App-specific footer partial
- Shared CSS overrides (`app/static/css/app.css`) for PM Interview Coach UI

This task has **zero dependencies** and can be built immediately.

---

## Section 2: Tech Stack (Mandatory Constraints)

| Layer | Technology | Version/Notes |
|-------|-----------|---------------|
| **Runtime** | Python | 3.11+ |
| **Backend Framework** | FastAPI | Async route handlers |
| **Templating** | Jinja2 | Server-side rendering |
| **Styling** | Tailwind CSS (CDN) | Utility classes only |
| **Interactivity** | HTMX (CDN) | Partial updates |
| **Icons** | Heroicons (inline SVG) | Outline style, 24px viewBox |
| **Fonts** | Geist Sans + JetBrains Mono | Geist via jsDelivr, JetBrains via Google Fonts |
| **Deployment** | Render | Procfile included |

**Do NOT use:** React, Vue, Angular, Svelte, Next.js, npm/node, webpack, Bootstrap, SCSS/LESS.

---

## Section 3: Design System

This section defines the complete design system used across the PM Interview Coach project. All UI components in subsequent tasks must use these tokens.

### Color Tokens

```css
:root {
  /* Backgrounds (cool-tinted, Slate palette) */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8FAFC;
  --color-bg-tertiary: #F1F5F9;

  /* Text (black, high contrast) */
  --color-text-primary: #000000;
  --color-text-secondary: #1D1D1F;
  --color-text-tertiary: #48484A;

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
  /* Backgrounds (deep navy) */
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

### Typography Scale

```css
.text-display { font-size: 3.5rem; line-height: 1.05; font-weight: 700; letter-spacing: -0.04em; }
.text-h1 { font-size: 2.5rem; line-height: 1.1; font-weight: 700; letter-spacing: -0.03em; }
.text-h2 { font-size: 1.75rem; line-height: 1.2; font-weight: 600; letter-spacing: -0.02em; }
.text-h3 { font-size: 1.375rem; line-height: 1.25; font-weight: 600; letter-spacing: -0.015em; }
.text-h4 { font-size: 1.125rem; line-height: 1.3; font-weight: 600; letter-spacing: -0.01em; }
.text-body-lg { font-size: 1.125rem; line-height: 1.5; letter-spacing: -0.011em; }
.text-body { font-size: 1rem; line-height: 1.5; letter-spacing: -0.011em; }
.text-small { font-size: 0.875rem; line-height: 1.4; letter-spacing: -0.006em; }
.text-xs { font-size: 0.75rem; line-height: 1.4; letter-spacing: -0.003em; }
```

### Font Loading

```html
<!-- Geist Sans (primary font) via jsDelivr/Fontsource CDN -->
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5/index.css">

<!-- JetBrains Mono (monospace) via Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## Section 4: Coding Conventions

### Python
- Type hints on all function signatures
- Async route handlers only
- Import order: stdlib → third-party → local

### HTML/Jinja2
- All templates extend `base.html`
- Use semantic HTML5 elements (`<nav>`, `<main>`, `<footer>`)
- Indent with 2 spaces
- Use CSS variables for all colors (no hex values)

### Tailwind
- Mobile-first: base, `md:` tablet, `lg:` desktop
- Use utility classes only
- Focus rings: `focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2`

### HTMX
- Use `hx-get`, `hx-post`, `hx-target`, `hx-swap`, `hx-indicator`
- Loading states must have `.htmx-indicator`

### Accessibility
- All interactive elements must be keyboard focusable
- Use `aria-label` where text is missing

---

## Section 5: The Task

### Overview

Build the UI foundation for PM Interview Coach:
1. Base template that extends the portfolio site base layout
2. App-specific navigation bar (Home, History, Progress)
3. App-specific footer
4. App CSS overrides for layout and utilities

### Scope Boundaries

**IN SCOPE:**
- `app/templates/base.html` (PM Interview Coach base layout)
- `app/templates/partials/nav.html`
- `app/templates/partials/footer.html`
- `app/static/css/app.css`

**OUT OF SCOPE:**
- Any database models or services
- Any routes or API logic
- Any page templates (index, history, practice, progress)
- Any HTMX interactions

### Template Specifications

**Base Template (`app/templates/base.html`):**
- Extends the portfolio base layout from fullstackpm.tech
- Adds app-specific `<main>` wrapper with max width 1200px
- Includes PM Interview Coach nav + footer partials
- Loads `app/static/css/app.css` after portfolio `custom.css`

**Nav (`app/templates/partials/nav.html`):**
- Links: Home (`/`), History (`/history`), Progress (`/progress`)
- Use `aria-current="page"` for active page
- Sticky top nav, border bottom, dark mode aware

**Footer (`app/templates/partials/footer.html`):**
- Simple two-column layout: app name + short description, right side links (GitHub/LinkedIn from settings)
- Border top, small text

**App CSS (`app/static/css/app.css`):**
- Light overrides for card spacing and layout utilities
- Add `.container` class: `max-width: 1200px; margin: 0 auto; padding: 0 1rem;`
- Add `.page-section` spacing utilities
- No new colors (only existing CSS variables)

### Inline Reference Files (Existing)

#### Portfolio Base Template (fullstackpm.tech) — `code/app/templates/base.html`

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

---

## Section 6: Expected Output

After completing this task, you should produce the following files:

1. **`app/templates/base.html`** — PM Interview Coach base layout (extends portfolio base)
2. **`app/templates/partials/nav.html`** — App navigation partial
3. **`app/templates/partials/footer.html`** — App footer partial
4. **`app/static/css/app.css`** — App-specific overrides

### Output Rules

- Return COMPLETE files, not snippets
- Include file path as a comment at the top of each file
- Do not add features beyond this spec
- All colors via CSS variables (no hex values)
- Use Geist Sans + JetBrains Mono fonts

---

## Section 7: Project Structure

```
pm-interview-coach/
├── app/
│   ├── templates/
│   │   ├── base.html                 [THIS TASK]
│   │   └── partials/
│   │       ├── nav.html              [THIS TASK]
│   │       └── footer.html           [THIS TASK]
│   └── static/
│       └── css/
│           └── app.css               [THIS TASK]
│
├── app/routers/                       [LATER]
├── app/services/                      [LATER]
└── app/templates/                     [LATER: pages]
```

---

## Section 8: Acceptance Test

### Test 1: Base Template Extends Portfolio Base
- Open `app/templates/base.html`
- Verify `{% extends "base.html" %}` points to portfolio base OR uses `{% extends "portfolio/base.html" %}` as defined in task

### Test 2: Nav Links Present
- Open `app/templates/partials/nav.html`
- Confirm links: Home (`/`), History (`/history`), Progress (`/progress`)
- Active link uses `aria-current="page"`

### Test 3: Footer Renders
- Open `app/templates/partials/footer.html`
- Confirm app name + short description + GitHub/LinkedIn links

### Test 4: CSS Overrides Load
- Verify `app/static/css/app.css` exists
- Confirm `.container` and `.page-section` utility classes are defined

### Test 5: Dark Mode Compatible
- Inspect templates to ensure colors use CSS variables (no hex colors)
- Verify dark mode uses `.dark` class on `<html>` (inherited from portfolio)

---

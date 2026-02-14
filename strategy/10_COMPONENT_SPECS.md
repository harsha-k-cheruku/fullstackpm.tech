# Component Specifications

## Purpose

These specs serve two roles:
1. **Build guide** — Precise instructions for building each component
2. **LLM benchmark input** — The exact same spec given to every LLM being tested, ensuring a level playing field

Each component spec is **model-agnostic**: no LLM-specific instructions, no hints about implementation approach. Just requirements, constraints, and acceptance criteria.

---

## Spec Format

Every component follows this structure:

```
## Component: [Name]
### Description — What it is and where it's used
### Props/Inputs — Data it receives
### Visual Requirements — Exact appearance (referencing Design System tokens)
### Behavior — Interactions, states, transitions
### Responsive — How it adapts across breakpoints
### Accessibility — ARIA, keyboard, screen reader requirements
### Acceptance Criteria — Testable pass/fail conditions
### Reference HTML — Skeleton structure (no styling) to show expected DOM
```

---

## Component 01: Navigation Bar

### Description
Fixed-height top navigation bar present on every page. Contains site name/logo, primary nav links, dark mode toggle, and mobile hamburger menu.

### Props/Inputs
```
current_page: string   — Active route path (e.g., "/projects", "/blog")
dark_mode: boolean     — Current dark mode state
```

### Visual Requirements
- Height: 4rem (h-16)
- Background: `--color-bg-primary` with bottom border `--color-border`
- Content max-width: 1200px, centered
- Left: Site name "fullstackpm.tech" in `text-lg font-bold`
- Center/Right: Nav links — Home, Projects, Blog, About, Contact
- Far right: Dark mode toggle icon (sun/moon)
- Active nav link: `--color-text-primary` with 2px bottom border in `--color-accent`
- Inactive nav link: `--color-text-secondary`, hover → `--color-text-primary`
- Sticky: `position: sticky; top: 0; z-index: 50`

### Behavior
- Dark mode toggle: clicks swap `dark` class on `<html>`, icon transitions sun↔moon, persists to localStorage
- Nav links: standard `<a>` navigation (no HTMX)
- Mobile (below md): nav links hidden, hamburger icon appears, click reveals dropdown/slide-out menu

### Responsive
- `>= md`: Full horizontal nav with all links visible
- `< md`: Logo + hamburger only. Links in dropdown menu.

### Accessibility
- `<nav>` element with `aria-label="Main navigation"`
- Active link has `aria-current="page"`
- Hamburger button has `aria-expanded`, `aria-controls`
- Dark mode toggle has `aria-label="Toggle dark mode"`
- All links keyboard-focusable with visible focus ring

### Acceptance Criteria
- [ ] Nav renders at 64px height on all pages
- [ ] Active page link is visually distinct (accent underline)
- [ ] Dark mode toggle works and persists across page reloads
- [ ] Mobile menu opens/closes without JS framework (vanilla JS or Alpine.js)
- [ ] Passes axe accessibility audit with zero violations
- [ ] Sticky positioning works during scroll
- [ ] All text meets WCAG AA contrast ratios in both modes

### Reference HTML
```html
<nav aria-label="Main navigation">
  <div> <!-- max-width container -->
    <a href="/">fullstackpm.tech</a>
    <div> <!-- desktop nav links -->
      <a href="/" aria-current="page">Home</a>
      <a href="/projects">Projects</a>
      <a href="/blog">Blog</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </div>
    <button aria-label="Toggle dark mode"><!-- sun/moon icon --></button>
    <button aria-expanded="false" aria-controls="mobile-menu"><!-- hamburger icon --></button>
  </div>
  <div id="mobile-menu" hidden><!-- mobile nav links --></div>
</nav>
```

---

## Component 02: Hero Section (Home Page)

### Description
Full-width hero section at the top of the home page. Introduces the site owner with a headline, sub-text, and two CTA buttons.

### Props/Inputs
```
name: string           — "Harsha Cheruku"
headline: string       — "Engineering Mind. Design Obsession."
subtext: string        — "Product leader with 16 years at Amazon, Walmart, and Verizon — now building AI-powered tools that prove the best PMs don't just manage products, they craft them."
cta_primary: {text, href}   — "See My Projects" → /projects
cta_secondary: {text, href} — "Read My Story" → /about
```

### Visual Requirements
- Padding: `py-20 lg:py-24` (generous vertical space)
- Name: `text-display` (48px), `--color-text-primary`
- Headline: `text-h2` (28px), `--color-accent`
- Subtext: `text-body-lg` (18px), `--color-text-secondary`, max-width 600px
- CTA Primary: Primary button (lg size)
- CTA Secondary: Secondary button (lg size)
- CTAs in a flex row with `gap-4`, stack vertically on mobile
- Content left-aligned (not centered)
- No background image, no gradient — clean and typographic

### Behavior
- Static content, no animation on load
- Buttons are standard links

### Responsive
- `>= lg`: Full sizing as specified
- `< lg`: Name drops to `text-4xl`, headline to `text-xl`
- `< sm`: CTAs stack vertically, full width

### Accessibility
- Heading hierarchy: `<h1>` for name, visually styled headline is a `<p>` (not a second h1)
- CTAs are `<a>` elements styled as buttons

### Acceptance Criteria
- [ ] Hero renders with correct typography scale
- [ ] Both CTAs navigate to correct pages
- [ ] Content is left-aligned, not centered
- [ ] Responsive: text scales down, buttons stack on mobile
- [ ] No layout shift on load
- [ ] Meets contrast requirements in both light and dark mode

---

## Component 03: Project Card

### Description
A card displaying a project summary in the project gallery grid. Clickable — navigates to project detail page.

### Props/Inputs
```
title: string          — Project name
description: string    — One-line description (max 120 chars)
tech_stack: string[]   — Array of technology names
status: string         — "live" | "in_progress" | "case_study" | "planned"
slug: string           — URL slug for detail page
thumbnail: string?     — Optional image path
```

### Visual Requirements
- Standard card pattern: `bg-secondary border border-border rounded-xl p-6`
- Hover: `border-border-hover shadow-sm`
- Title: `text-h4 text-primary mb-2`
- Description: `text-body text-secondary mb-4`
- Tech stack: flex row of default badges, `gap-2`, wrapping allowed
- Status badge: top-right corner, semantic color based on status:
  - live → success (green)
  - in_progress → warning (amber)
  - case_study → info (blue)
  - planned → default (gray)
- Entire card is clickable (wrap in `<a>` or use click handler)
- Cursor: pointer on hover
- If thumbnail: display at top of card, `rounded-t-xl`, aspect-ratio 16:9
- If no thumbnail: no image area (don't show placeholder)

### Behavior
- Click navigates to `/projects/{slug}`
- Hover state: border and shadow transition
- No other interactivity

### Responsive
- Cards in grid: 1 col mobile, 2 col tablet, 3 col desktop
- Card itself is always full-width of its grid cell

### Accessibility
- Card is an `<a>` or `<article>` with `<a>` inside
- Status badge has `aria-label` (e.g., "Status: Live")
- Tech stack badges are decorative (no aria role needed)
- Focus ring visible on keyboard navigation

### Acceptance Criteria
- [ ] Card renders with all data fields populated
- [ ] Status badge shows correct color per status value
- [ ] Tech stack tags wrap gracefully at narrow widths
- [ ] Hover transition is smooth (150ms)
- [ ] Click navigates to correct URL
- [ ] Card looks correct with and without thumbnail
- [ ] Works in both light and dark mode

---

## Component 04: Blog Post Card

### Description
A list item in the blog feed showing post title, date, excerpt, tags, and reading time.

### Props/Inputs
```
title: string
date: string           — ISO date (display formatted)
excerpt: string        — First 160 chars of post
tags: string[]
reading_time: string   — e.g., "5 min read"
slug: string
```

### Visual Requirements
- Layout: horizontal on desktop (title/excerpt left, metadata right), stacked on mobile
- Title: `text-h3 text-primary`, hover → `text-accent`
- Date + reading time: `text-small text-tertiary`
- Excerpt: `text-body text-secondary`, 2-line clamp
- Tags: small badges, `gap-2`
- Bottom border separator between posts: `border-b border-border pb-6 mb-6`
- No card background — clean list style

### Behavior
- Title click → `/blog/{slug}`
- Tag click → `/blog/tag/{tag}`

### Acceptance Criteria
- [ ] Post displays all fields correctly
- [ ] Date is human-formatted (e.g., "Feb 15, 2026")
- [ ] Excerpt clamps at 2 lines with ellipsis
- [ ] Tags are clickable and navigate to tag filter page
- [ ] Clean separation between posts via border
- [ ] Responsive: stacks cleanly on mobile

---

## Component 05: Blog Post Content (Rendered Markdown)

### Description
The rendered HTML output of a blog post's markdown content. Needs proper typography for long-form reading.

### Props/Inputs
```
html_content: string   — Pre-rendered HTML from markdown
title: string
date: string
tags: string[]
reading_time: string
author: string
```

### Visual Requirements
- Content wrapper: `max-w-3xl mx-auto` (reading width)
- Post header: title (`text-h1`), metadata row (date, reading time, author in `text-small text-tertiary`), tags
- Prose typography (apply to content area):
  - Paragraphs: `text-body leading-relaxed mb-4`
  - H2: `text-h2 mt-12 mb-4`
  - H3: `text-h3 mt-8 mb-3`
  - Links: `text-accent hover:underline`
  - Lists: proper indentation, `mb-4`
  - Blockquotes: left border `border-l-4 border-accent pl-4 italic text-secondary`
  - Code inline: `bg-tertiary px-1.5 py-0.5 rounded text-sm font-mono`
  - Code blocks: design system code block pattern
  - Images: `rounded-lg max-w-full my-6`
  - Tables: bordered, striped rows
- Bottom: tag list, "Back to Blog" link

### Acceptance Criteria
- [ ] All markdown elements render with correct typography
- [ ] Code blocks have syntax highlighting
- [ ] Images are responsive (max-width 100%)
- [ ] Reading experience is comfortable (line length, spacing)
- [ ] Works in both light and dark mode

---

## Component 06: Experience Timeline (Resume Page)

### Description
Vertical timeline showing career history with company, title, dates, and key accomplishments.

### Props/Inputs
```
experiences: [{
  company: string,
  title: string,
  date_range: string,        — e.g., "Oct 2024 - Present"
  location: string,
  bullets: string[],         — 3-4 key accomplishments
  tech_skills: string[],
  is_current: boolean
}]
```

### Visual Requirements
- Vertical timeline line: 2px, `--color-border`, centered on left edge
- Each entry: dot on timeline (8px circle, `--color-accent` for current, `--color-border` for past)
- Company: `text-h3 text-primary`
- Title: `text-h4 text-accent`
- Date + location: `text-small text-tertiary`
- Bullets: `text-body text-secondary`, standard list
- Tech skills: small badges row
- Entries spaced with `mb-8`

### Responsive
- Desktop: timeline on left, content to right
- Mobile: timeline hidden, entries stacked with left border accent

### Acceptance Criteria
- [ ] Timeline renders all entries in chronological order (most recent first)
- [ ] Current role is visually distinguished (accent dot)
- [ ] Tech skills render as badges
- [ ] Responsive: graceful degradation on mobile
- [ ] Both modes (light/dark) render correctly

---

## Component 07: Filter Bar (HTMX-Powered)

### Description
A reusable filter bar used on Projects, Blog, and Dashboard pages. Triggers HTMX requests to update content below.

### Props/Inputs
```
filters: [{
  name: string,          — Query parameter name
  type: "select" | "tags" | "search",
  options: string[]?,    — For select type
  placeholder: string?
}]
htmx_target: string      — CSS selector of content to update
htmx_url: string         — Endpoint to fetch filtered content
```

### Visual Requirements
- Horizontal row of filter controls, wrapping on mobile
- Select: standard form select with design system styling
- Tags: clickable badges, active state uses accent color
- Search: text input with search icon, `--color-bg-primary`
- All controls in a flex row with `gap-3`

### Behavior
- Select change: triggers `hx-get` with filter params to `htmx_url`, swaps `htmx_target`
- Tag click: toggles active state, triggers same HTMX request
- Search: `hx-trigger="keyup changed delay:300ms"` for debounced search

### Acceptance Criteria
- [ ] Filter changes trigger HTMX request without page reload
- [ ] Target content updates smoothly
- [ ] Active filters are visually indicated
- [ ] Search debounces correctly (300ms)
- [ ] Works with any combination of filter types
- [ ] Graceful on mobile (wraps or scrolls horizontally)

---

## Component 08: Stats Card Grid

### Description
Row of 3-5 metric cards used on dashboards and progress pages. Each shows a number, label, and optional trend indicator.

### Props/Inputs
```
stats: [{
  label: string,        — "Total GMV", "Active Sellers"
  value: string,        — "42", "$1.2M", "87%"
  trend: string?,       — "+12%" or "-3%"
  trend_direction: "up" | "down" | "neutral"?
}]
```

### Visual Requirements
- Grid: `grid-cols-2 lg:grid-cols-4 gap-4`
- Each card: `bg-secondary border border-border rounded-xl p-4`
- Value: `text-h2 text-primary font-bold`
- Label: `text-small text-secondary`
- Trend: `text-xs` — green+arrow-up for positive, red+arrow-down for negative, gray for neutral

### Acceptance Criteria
- [ ] Grid is responsive (2 cols mobile, 4 cols desktop)
- [ ] Trend indicators use correct semantic colors
- [ ] Values render at correct typography scale
- [ ] Cards are equal height in each row

---

## Component 09: Loading & Empty States

### Description
Standardized loading indicators and empty state messages used across all pages.

### Loading State
- Skeleton pulse: card-shaped `animate-pulse bg-tertiary rounded-xl` blocks matching the expected content layout
- Inline loading: small spinner (`animate-spin` 20px circle with accent border) next to the triggering element
- HTMX indicator: element with `htmx-indicator` class, hidden by default, shown during request

### Empty State
- Centered container: icon (Heroicons outline), heading, description, optional CTA
- Example: "No projects yet" + "Check back soon or explore the blog"
- Use `text-secondary` for all empty state text

### Acceptance Criteria
- [ ] Loading skeletons match the shape of actual content
- [ ] Spinner appears during HTMX requests and disappears on completion
- [ ] Empty states display when content arrays are empty
- [ ] Empty states include actionable CTAs where appropriate

---

## Component 10: Footer

### Description
Site-wide footer with links, attribution, and social links.

### Props/Inputs
```
github_url: string
linkedin_url: string
rss_url: string
```

### Visual Requirements
- Background: `--color-bg-secondary` with top border
- Padding: `py-12`
- Three columns on desktop, stacked on mobile:
  - Col 1: Site name + one-line description
  - Col 2: Quick links (Home, Projects, Blog, About, Contact)
  - Col 3: Social links (GitHub, LinkedIn, RSS) with icons
- Bottom row: "Built with FastAPI + HTMX" in `text-xs text-tertiary`

### Acceptance Criteria
- [ ] Three-column layout on desktop, stacked on mobile
- [ ] All links functional
- [ ] Social links open in new tab (`target="_blank" rel="noopener"`)
- [ ] Attribution text present
- [ ] Consistent with design system colors/spacing

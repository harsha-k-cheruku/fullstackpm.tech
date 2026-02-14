# fullstackpm.tech — Design System

## Design Philosophy

**Professional but human.** This is a personal portfolio, not a SaaS landing page. It should feel like meeting a thoughtful, experienced PM who also happens to build things — not a corporate brochure. Clean, confident, minimal. Let the work speak.

**Principles:**
1. **Content-first** — Typography, whitespace, and readability over decoration
2. **Restrained color** — Neutral base with one bold accent. Color used for meaning, not flair.
3. **Consistent rhythm** — Predictable spacing and sizing so every page feels cohesive
4. **Dark mode native** — Designed for dark mode first (developer/PM audience preference), with full light mode support
5. **No gratuitous animation** — Transitions serve function (loading states, tab switches), not spectacle

---

## Color Palette

### Design Tokens

All colors defined as CSS custom properties AND Tailwind config values. Every component references tokens, never raw hex values.

### Core Colors (Approved)

| Color | Hex | Role |
|-------|-----|------|
| Black | `#000000` | Text (light mode), backgrounds (dark mode) |
| White | `#FFFFFF` | Page background (light mode), text (dark mode) |
| Off-White | `#F7F7F7` | Cards, secondary backgrounds (light mode) |
| Blue | `#2E8ECE` | Accent — CTAs, links, active states |
| Green | `#27AE60` | Success — "Ship It", Live, Healthy |
| Red | `#E74C3C` | Danger — "Kill It", Errors, Critical |
| Yellow | `#F1C40F` | Warning — "Keep Testing", In Progress |

### Primary Palette (Derived from Core Colors)

| Token | Light Mode | Dark Mode | Usage |
|-------|-----------|-----------|-------|
| `--color-bg-primary` | `#FFFFFF` | `#000000` | Page background |
| `--color-bg-secondary` | `#F7F7F7` | `#111111` | Card backgrounds, sections |
| `--color-bg-tertiary` | `#EEEEEE` | `#1A1A1A` | Hover states, code blocks, tags |
| `--color-text-primary` | `#000000` | `#FFFFFF` | Headings, body text |
| `--color-text-secondary` | `#555555` | `#AAAAAA` | Subtext, captions, metadata |
| `--color-text-tertiary` | `#999999` | `#666666` | Placeholders, disabled text |
| `--color-border` | `#E0E0E0` | `#222222` | Card borders, dividers |
| `--color-border-hover` | `#CCCCCC` | `#333333` | Border on hover |

*Black/white foundation with warm neutrals. High contrast, clean, bold.*

### Accent Color

| Token | Value | Usage |
|-------|-------|-------|
| `--color-accent` | `#2E8ECE` | Primary CTAs, active nav, links |
| `--color-accent-hover` | `#2577AD` | Hover on accent elements |
| `--color-accent-light` | `#E8F4FB` | Accent backgrounds (light mode) |
| `--color-accent-dark` | `#1A3A52` | Accent backgrounds (dark mode) |
| `--color-accent-text` | `#FFFFFF` | Text on accent backgrounds |

### Semantic Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-success` | `#27AE60` | Positive indicators, "Ship It", healthy |
| `--color-success-bg` | `#D5F5E3` / `#0B3D20` | Success background (light/dark) |
| `--color-warning` | `#F1C40F` | Caution, "Keep Testing", at risk |
| `--color-warning-bg` | `#FEF9E7` / `#4A3F00` | Warning background (light/dark) |
| `--color-danger` | `#E74C3C` | Errors, "Kill It", critical |
| `--color-danger-bg` | `#FADBD8` / `#4A1A15` | Danger background (light/dark) |
| `--color-info` | `#2E8ECE` | Informational badges, tooltips |

### Tailwind Config Mapping

```js
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        surface: {
          primary: 'var(--color-bg-primary)',
          secondary: 'var(--color-bg-secondary)',
          tertiary: 'var(--color-bg-tertiary)',
        },
        content: {
          primary: 'var(--color-text-primary)',
          secondary: 'var(--color-text-secondary)',
          tertiary: 'var(--color-text-tertiary)',
        },
        accent: {
          DEFAULT: 'var(--color-accent)',
          hover: 'var(--color-accent-hover)',
          light: 'var(--color-accent-light)',
          dark: 'var(--color-accent-dark)',
        },
        semantic: {
          success: 'var(--color-success)',
          warning: 'var(--color-warning)',
          danger: 'var(--color-danger)',
          info: 'var(--color-info)',
        },
      },
    },
  },
}
```

---

## Typography

### Font Stack

| Usage | Font | Fallback | Why |
|-------|------|----------|-----|
| **Headings** | Inter | `system-ui, -apple-system, sans-serif` | Clean, modern, excellent readability at all sizes |
| **Body** | Inter | `system-ui, -apple-system, sans-serif` | Same family for cohesion |
| **Code** | JetBrains Mono | `ui-monospace, Menlo, monospace` | Clear distinction between regular and code text |

Load via Google Fonts (2 families, minimal weight selection to keep bundle small):
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Type Scale

Based on a **1.250 (Major Third)** ratio. All sizes in rem.

| Token | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| `text-display` | 3rem (48px) | 700 | 1.1 | -0.02em | Hero headline only |
| `text-h1` | 2.25rem (36px) | 700 | 1.2 | -0.02em | Page titles |
| `text-h2` | 1.75rem (28px) | 600 | 1.3 | -0.01em | Section headings |
| `text-h3` | 1.375rem (22px) | 600 | 1.4 | 0 | Subsection headings |
| `text-h4` | 1.125rem (18px) | 600 | 1.4 | 0 | Card titles, labels |
| `text-body` | 1rem (16px) | 400 | 1.6 | 0 | Body text, paragraphs |
| `text-body-lg` | 1.125rem (18px) | 400 | 1.7 | 0 | Lead paragraphs, featured text |
| `text-small` | 0.875rem (14px) | 400 | 1.5 | 0.01em | Captions, metadata, dates |
| `text-xs` | 0.75rem (12px) | 500 | 1.4 | 0.02em | Badges, labels, tags |
| `text-code` | 0.875rem (14px) | 400 | 1.6 | 0 | Inline code, code blocks |

### Tailwind Classes

```
Display:  text-5xl font-bold tracking-tight leading-tight
H1:       text-4xl font-bold tracking-tight leading-tight
H2:       text-2xl font-semibold leading-snug
H3:       text-xl font-semibold leading-normal
H4:       text-lg font-semibold leading-normal
Body:     text-base font-normal leading-relaxed
Body Lg:  text-lg font-normal leading-relaxed
Small:    text-sm font-normal leading-normal
XS:       text-xs font-medium tracking-wide
Code:     text-sm font-mono leading-relaxed
```

---

## Spacing Scale

Use Tailwind's default spacing scale. **Do not invent custom values.** Consistency matters more than precision.

### Standard Spacing Reference

| Token | Value | Common Usage |
|-------|-------|-------------|
| `space-1` | 0.25rem (4px) | Tight inner padding, icon gaps |
| `space-2` | 0.5rem (8px) | Badge padding, tight gaps |
| `space-3` | 0.75rem (12px) | Button padding (y), input padding |
| `space-4` | 1rem (16px) | Card padding (inner), list item gaps |
| `space-6` | 1.5rem (24px) | Card padding (outer), section gaps |
| `space-8` | 2rem (32px) | Section spacing within a page |
| `space-12` | 3rem (48px) | Major section separators |
| `space-16` | 4rem (64px) | Page section padding (top/bottom) |
| `space-20` | 5rem (80px) | Hero section padding |
| `space-24` | 6rem (96px) | Max page section spacing |

### Layout Constants

| Element | Value | Tailwind |
|---------|-------|----------|
| Page max-width | 1200px | `max-w-7xl` |
| Content max-width (reading) | 768px | `max-w-3xl` |
| Card grid gap | 1.5rem | `gap-6` |
| Nav height | 4rem | `h-16` |
| Footer padding | 3rem top/bottom | `py-12` |
| Page padding (horizontal) | 1rem mobile, 2rem desktop | `px-4 lg:px-8` |

---

## Border Radius

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| `radius-sm` | 0.25rem | `rounded` | Badges, tags, inline elements |
| `radius-md` | 0.5rem | `rounded-lg` | Buttons, inputs, small cards |
| `radius-lg` | 0.75rem | `rounded-xl` | Cards, modals, panels |
| `radius-full` | 9999px | `rounded-full` | Avatars, pills, toggles |

**Default for most elements: `rounded-lg`**

---

## Shadows

Minimal shadow usage. Shadows create depth hierarchy — use sparingly.

| Token | Tailwind | Usage |
|-------|----------|-------|
| `shadow-sm` | `shadow-sm` | Subtle card elevation on hover |
| `shadow-md` | `shadow-md` | Dropdown menus, popovers |
| `shadow-lg` | `shadow-lg` | Modals, slide-over panels |
| `shadow-none` | `shadow-none` | Default state for most cards (use border instead) |

**Dark mode:** Shadows are invisible on dark backgrounds. Use `ring-1 ring-white/10` for card edges instead.

---

## Component Patterns

### Buttons

| Variant | Light Mode | Dark Mode | Usage |
|---------|-----------|-----------|-------|
| **Primary** | `bg-accent text-white hover:bg-accent-hover` | Same | Main CTAs: "See Projects", "Submit", "Evaluate" |
| **Secondary** | `border border-border text-primary hover:bg-tertiary` | `border border-border text-primary hover:bg-tertiary` | Secondary actions: "Read More", "Export" |
| **Ghost** | `text-secondary hover:text-primary hover:bg-tertiary` | Same | Tertiary actions: nav links, filter toggles |
| **Danger** | `bg-danger text-white hover:bg-red-600` | Same | Destructive: "Delete" |

**Sizes:**
| Size | Padding | Text | Tailwind |
|------|---------|------|----------|
| `sm` | `px-3 py-1.5` | `text-sm` | Inline actions, tags |
| `md` | `px-4 py-2` | `text-sm` | Default |
| `lg` | `px-6 py-3` | `text-base` | Hero CTAs, primary page actions |

**All buttons:** `rounded-lg font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2`

### Cards

```
Default:    bg-secondary border border-border rounded-xl p-6
Hover:      hover:border-border-hover hover:shadow-sm transition-all duration-150
Active/Selected: border-accent ring-1 ring-accent
```

**Card anatomy:**
- Outer: `rounded-xl border p-6`
- Title: `text-h4 text-primary mb-2`
- Description: `text-body text-secondary`
- Footer/metadata: `text-small text-tertiary mt-4`
- Tags: flex row of badges with `gap-2`

### Badges / Tags

```
Default:    bg-tertiary text-secondary text-xs font-medium px-2.5 py-0.5 rounded
Accent:     bg-accent-light text-accent text-xs font-medium px-2.5 py-0.5 rounded (dark: bg-accent-dark)
Success:    bg-success-bg text-success ... (same pattern)
Warning:    bg-warning-bg text-warning ...
Danger:     bg-danger-bg text-danger ...
```

**Tech stack tags:** Use default style
**Status badges:** Use semantic colors (Live=success, In Progress=warning, Planned=default)
**Verdict badges:** Use semantic colors (Build=success, Keep Testing=warning, Kill=danger)

### Forms / Inputs

```
Input:      w-full bg-primary border border-border rounded-lg px-4 py-2.5 text-body text-primary
            placeholder:text-tertiary
            focus:border-accent focus:ring-1 focus:ring-accent focus:outline-none
            transition-colors duration-150

Textarea:   Same as input + min-h-[120px] resize-y

Label:      text-sm font-medium text-primary mb-1.5 block

Help text:  text-xs text-tertiary mt-1

Error:      border-danger focus:border-danger focus:ring-danger
            + text-xs text-danger mt-1 (error message)
```

### Navigation

```
Nav bar:    bg-primary border-b border-border h-16 px-4 lg:px-8
            flex items-center justify-between max-w-7xl mx-auto

Nav link:   text-sm font-medium text-secondary hover:text-primary transition-colors
Active:     text-primary (optionally with accent underline: border-b-2 border-accent)

Logo/Name:  text-lg font-bold text-primary

Mobile:     Hamburger icon at md breakpoint, slide-out or dropdown menu
```

### Footer

```
Footer:     bg-secondary border-t border-border py-12 mt-16

Content:    max-w-7xl mx-auto px-4 lg:px-8
            Grid: 2-3 columns on desktop, stack on mobile

Links:      text-sm text-secondary hover:text-primary
Built with: text-xs text-tertiary
```

---

## Layout & Grid

### Breakpoints (Tailwind defaults)

| Name | Min Width | Usage |
|------|-----------|-------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet, nav collapse point |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Wide desktop |

### Page Layout Pattern

```html
<body class="bg-primary text-primary min-h-screen">
  <nav><!-- Fixed height nav --></nav>
  <main class="max-w-7xl mx-auto px-4 lg:px-8 py-8 lg:py-16">
    <!-- Page content -->
  </main>
  <footer><!-- Footer --></footer>
</body>
```

### Grid Patterns

| Pattern | Classes | Usage |
|---------|---------|-------|
| **Project cards** | `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6` | Project gallery |
| **Blog list** | `max-w-3xl mx-auto` (single column) | Blog posts |
| **Dashboard** | `grid grid-cols-1 lg:grid-cols-4 gap-6` (KPI cards) | Dashboard metrics |
| **Two-column detail** | `grid grid-cols-1 lg:grid-cols-5 gap-8` (3+2 split) | Project detail |
| **Content + sidebar** | `grid grid-cols-1 lg:grid-cols-4 gap-8` (3+1 split) | Blog detail |

---

## Dark Mode

### Implementation

```html
<!-- In <html> tag -->
<html class="dark"> <!-- or toggled via JS -->
```

Dark mode is the default. Light mode is the toggle option. Use `prefers-color-scheme` for initial state, then allow manual toggle stored in `localStorage`.

### Toggle Component

Small sun/moon icon in the nav bar. Click toggles `dark` class on `<html>` and persists to `localStorage`.

### Dark Mode CSS Variables

```css
:root {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F7F7F7;
  --color-bg-tertiary: #EEEEEE;
  --color-text-primary: #000000;
  --color-text-secondary: #555555;
  --color-text-tertiary: #999999;
  --color-border: #E0E0E0;
  --color-border-hover: #CCCCCC;

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

---

## Iconography

Use **Heroicons** (by Tailwind Labs) — SVG icons, consistent with Tailwind ecosystem.
- Style: Outline (24px) for nav and UI elements
- Style: Solid (20px) for inline / small elements
- Load via copy-paste SVG (no icon font dependency)

---

## Motion & Transitions

| Interaction | Transition | Tailwind |
|-------------|-----------|----------|
| Button hover | Background color | `transition-colors duration-150` |
| Card hover | Border + shadow | `transition-all duration-150` |
| Nav link hover | Text color | `transition-colors duration-150` |
| HTMX swap | Fade in | `htmx-swapping: opacity-0; transition: opacity 200ms;` |
| Dark mode toggle | All colors | `transition-colors duration-300` on `<html>` |
| Loading spinner | Rotate | `animate-spin` |
| Skeleton pulse | Opacity | `animate-pulse` |

**No bounce, no slide, no parallax.** Transitions are functional, not decorative.

---

## Code Blocks

```
Container:  bg-tertiary rounded-xl p-4 overflow-x-auto border border-border
Code text:  font-mono text-sm text-primary leading-relaxed
Syntax:     Pygments (monokai for dark, github-light for light) or Tailwind Typography prose
Language badge: absolute top-right, text-xs text-tertiary bg-secondary px-2 py-1 rounded
```

---

## Accessibility

- All interactive elements have visible focus rings (`focus:ring-2 focus:ring-accent`)
- Color contrast ratios meet WCAG AA (4.5:1 for normal text, 3:1 for large text)
- Semantic HTML: `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
- All images have alt text
- Skip-to-content link (visually hidden, appears on focus)
- No information conveyed by color alone (always pair with text/icon)

---

## File: `custom.css`

Minimal custom CSS — Tailwind handles 95%. Custom CSS only for:
1. CSS custom properties (color tokens)
2. HTMX transition styles
3. Prose/typography overrides for blog content
4. Scrollbar styling (dark mode)
5. Print styles

---

## Quick Reference: Copy-Paste Patterns

### Standard Page Shell
```html
<main class="max-w-7xl mx-auto px-4 lg:px-8 py-8 lg:py-16">
  <h1 class="text-4xl font-bold tracking-tight mb-4">Page Title</h1>
  <p class="text-lg text-secondary leading-relaxed mb-8">Page description</p>
  <!-- Content -->
</main>
```

### Standard Card
```html
<div class="bg-secondary border border-border rounded-xl p-6 hover:border-border-hover hover:shadow-sm transition-all duration-150">
  <h3 class="text-lg font-semibold mb-2">Card Title</h3>
  <p class="text-secondary mb-4">Card description text.</p>
  <div class="flex gap-2">
    <span class="bg-tertiary text-secondary text-xs font-medium px-2.5 py-0.5 rounded">Tag</span>
  </div>
</div>
```

### Standard Button
```html
<button class="bg-accent text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-accent-hover transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2">
  Button Text
</button>
```

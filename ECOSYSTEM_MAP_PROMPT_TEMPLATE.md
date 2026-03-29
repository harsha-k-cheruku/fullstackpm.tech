# Ecosystem Map Prompt Template (PM Visual Guide Standard)

Use this prompt whenever creating or updating an ecosystem map page so quality matches the strongest reference pages.

---

## Prompt (copy/paste)

You are updating a **PM Visual Guide ecosystem page** in a FastAPI + Jinja template codebase.

### Goal
Create a comprehensive, PM-focused ecosystem map page with:
1. Strong visual diagrams
2. PM decision lens (tradeoffs, metrics, unit economics)
3. A reference/components section for interview prep
4. Fully responsive, no overflow/broken layouts

### Required structure
Build page with this exact structure:

1. Breadcrumb + page header
2. Sticky subnav with anchors for all sections
3. 5-7 diagram sections (domain-specific)
4. **Components / Explainers section** with PM lens (required)
5. Footer attribution
6. Scroll-based active subnav JS

### Mandatory sections
- Diagram sections (`id` anchors)
- `#components` section with:
  - 3-6 component cards
  - per card: what it does, PM metrics, failure mode/pitfall
  - final “Interview shortcut” callout

### PM lens requirements (non-negotiable)
Every page must include:
- Tradeoffs (e.g., growth vs risk, yield vs quality, speed vs compliance)
- Metrics that PMs would own
- Unit economics or operational impact framing
- Interview-ready summary callouts

### Design and code constraints
- Use dedicated CSS vars with light/dark support
- Keep files small and modular (partials over giant templates)
- No horizontal overflow
- Bar/width visuals must never exceed 100%
- Mobile breakpoints for dense grids and flow rows
- Keep copy specific, not generic fluff

### Navigation and behavior requirements
- Subnav links must match section IDs exactly
- Scroll spy array must include every section, including `components`
- Each section should have clear `h2` + concise intro paragraph

### Acceptance checklist
- [ ] Page loads via route
- [ ] Sticky subnav works and updates active state while scrolling
- [ ] No clipped/overflowing diagrams on desktop/mobile
- [ ] `#components` section exists and is substantive
- [ ] At least one PM interview callout with metrics + tradeoffs
- [ ] Dark mode remains legible

### Output expectations
Return concrete file changes for:
- Main template (`.../resources/<ecosystem>.html`)
- Subnav partial
- Diagram partials (as needed)
- Components/explainers partial (required)
- Ecosystem CSS updates

Do not hand-wave. Implement directly.

---

## Recommended implementation pattern

- `templates/resources/<ecosystem>.html`
  - include subnav
  - include all diagram partials
  - include `<ecosystem>_explainers.html`
- `templates/resources/partials/<ecosystem>_subnav.html`
  - includes `#components`
- `templates/resources/partials/<ecosystem>_explainers.html`
  - component cards + PM interview shortcut callout
- `static/css/<ecosystem>.css`
  - responsive guards + overflow safety

---

## Why this standard exists

Most ecosystem pages fail because they stop at “what exists.”
Great PM prep content explains:
- what matters,
- what breaks,
- what to measure,
- and how to reason about tradeoffs under constraints.

That’s the bar.

# Instructions: Update Templates with New Design System Features

## Context

The CSS design system has been upgraded with:
1. **10-step color scales** for blue, success (emerald), warning (amber), and danger (red)
2. **Semantic color variables** for better UX
3. **Card hover effects** for subtle polish
4. **Badge components** for status indicators

All existing color variables still work (backwards compatible). New features are opt-in.

## What You Need to Do

Update all HTML templates to use the new design features. This is purely additive — no breaking changes.

---

## Change 1: Add Hover Effects to Cards

### Before:
```html
<a href="/projects/{{ project.slug }}"
   class="block rounded-xl border transition-all duration-150">
```

### After:
```html
<a href="/projects/{{ project.slug }}"
   class="block rounded-xl border card-hover">
```

**Why:** Adds subtle lift + shadow on hover. More polished UX.

**Where to apply:**
- `app/templates/partials/project_card.html` (project cards)
- `app/templates/home.html` (featured project cards)
- Any card-like components

---

## Change 2: Add Status Badges

### Before (no visual status indicator):
```html
<h3>{{ project.title }}</h3>
```

### After:
```html
<div class="mb-2">
  {% if project.status == "live" %}
  <span class="badge badge-success">Live</span>
  {% elif project.status == "in_progress" %}
  <span class="badge badge-warning">In Progress</span>
  {% elif project.status == "planned" %}
  <span class="badge badge-info">Planned</span>
  {% endif %}
</div>
<h3>{{ project.title }}</h3>
```

**Why:** Visual status indicators are easier to scan than text.

**Where to apply:**
- `app/templates/partials/project_card.html`
- `app/templates/projects/gallery.html`
- `app/templates/projects/detail.html`

---

## Change 3: Remove Blue Gradient Backgrounds

### Before:
```html
<section style="background: linear-gradient(135deg, #E6F4FB 0%, white 100%);">
```

### After:
```html
<section style="background-color: var(--color-bg-primary);">
```

**Why:** Gradients feel too corporate for a builder's portfolio. Keep it minimal.

**Where to apply:**
- Any section with gradient backgrounds
- Hero sections should have plain white background

---

## Change 4: Use Semantic Colors for Alerts/Messages

### Before:
```html
<div style="background-color: #D5F5E3; color: #27AE60;">
  Success message
</div>
```

### After:
```html
<div style="background-color: var(--color-success-bg); color: var(--color-success-900);">
  Success message
</div>
```

**Why:** Semantic colors auto-adjust for light/dark mode. More maintainable.

**Available semantic colors:**
- Success: `--color-success-bg`, `--color-success-500`, `--color-success-900`
- Warning: `--color-warning-bg`, `--color-warning-500`, `--color-warning-900`
- Danger: `--color-danger-bg`, `--color-danger-500`, `--color-danger-900`

**Where to apply:**
- Flash messages
- Form validation errors
- Success confirmations
- Alert boxes

---

## Files to Update

### High Priority (User-Facing)
1. `app/templates/partials/project_card.html` — Add badges + hover effect
2. `app/templates/home.html` — Add badges to featured projects
3. `app/templates/projects/gallery.html` — Add hover to grid items
4. `app/templates/projects/detail.html` — Add status badge

### Medium Priority (Nice-to-Have)
5. `app/templates/blog/list.html` — Add hover to post items
6. `app/templates/contact.html` — Use semantic colors for form validation
7. Any alert/notification components

### Low Priority (Future)
8. Admin pages (if any)
9. Email templates (use simple colors, not CSS variables)

---

## Testing Checklist

After making changes, verify:

- [ ] Cards have subtle lift on hover (desktop)
- [ ] Status badges appear on project cards
- [ ] Badge colors are correct (green=live, yellow=in progress, blue=planned)
- [ ] No gradient backgrounds (plain white or bg-secondary)
- [ ] Dark mode still works (toggle and check)
- [ ] Mobile responsive (badges don't break layout)
- [ ] Hover effects don't trigger on mobile (touch devices)

---

## Example: Full Project Card Update

**Before:**
```html
<!-- app/templates/partials/project_card.html -->
<a href="/projects/{{ project.slug }}"
   class="block rounded-xl border transition-all duration-150"
   style="background-color: var(--color-bg-secondary); border-color: var(--color-border);">
  <div class="p-6">
    <h3 class="text-h4 mb-2" style="color: var(--color-text-primary);">
      {{ project.title }}
    </h3>
    <p class="text-body mb-4" style="color: var(--color-text-secondary);">
      {{ project.description }}
    </p>
  </div>
</a>
```

**After:**
```html
<!-- app/templates/partials/project_card.html -->
<a href="/projects/{{ project.slug }}"
   class="block rounded-xl border card-hover"
   style="background-color: var(--color-bg-secondary); border-color: var(--color-border);">
  <div class="p-6">
    <!-- Status badge -->
    <div class="mb-3">
      {% if project.status == "live" %}
      <span class="badge badge-success">Live</span>
      {% elif project.status == "in_progress" %}
      <span class="badge badge-warning">In Progress</span>
      {% elif project.status == "case_study" %}
      <span class="badge badge-info">Case Study</span>
      {% elif project.status == "planned" %}
      <span class="badge badge-info">Planned</span>
      {% endif %}
    </div>

    <h3 class="text-h4 mb-2" style="color: var(--color-text-primary);">
      {{ project.title }}
    </h3>
    <p class="text-body mb-4" style="color: var(--color-text-secondary);">
      {{ project.description }}
    </p>
  </div>
</a>
```

**Changes made:**
1. Added `card-hover` class (replaces manual transition)
2. Added status badge with conditional rendering
3. Added `mb-3` spacing below badge

---

## CSS Variables Reference

### New Color Scales (Available Now)

**Blue (Primary):**
```css
--color-blue-50   #E6F4FB  /* Lightest - backgrounds */
--color-blue-100  #CCE9F7
--color-blue-200  #99D3EF
--color-blue-300  #66BDE7
--color-blue-400  #33A7DF
--color-blue-500  #2E8ECE  /* Main accent (same as before) */
--color-blue-600  #2577AD  /* Hover state */
--color-blue-700  #1D608C
--color-blue-800  #14496B
--color-blue-900  #0C324A  /* Darkest - text on light bg */
```

**Success (Emerald):**
```css
--color-success-50   #ECFDF5
--color-success-100  #D1FAE5
--color-success-500  #10B981  /* Main success color */
--color-success-600  #059669
--color-success-700  #047857
--color-success-900  #064E3B
```

**Warning (Amber):**
```css
--color-warning-50   #FFFBEB
--color-warning-100  #FEF3C7
--color-warning-500  #F59E0B  /* Main warning color */
--color-warning-600  #D97706
--color-warning-900  #78350F
```

**Danger (Red):**
```css
--color-danger-50   #FEF2F2
--color-danger-100  #FEE2E2
--color-danger-500  #EF4444  /* Main danger color */
--color-danger-600  #DC2626
--color-danger-900  #7F1D1D
```

### Backwards Compatible Aliases

These still work (no breaking changes):
```css
--color-accent        (same as --color-blue-500)
--color-accent-hover  (same as --color-blue-600)
--color-accent-light  (same as --color-blue-50)
--color-accent-dark   (same as --color-blue-900)
--color-success       (same as --color-success-500)
--color-success-bg    (same as --color-success-50)
--color-warning       (same as --color-warning-500)
--color-warning-bg    (same as --color-warning-50)
--color-danger        (same as --color-danger-500)
--color-danger-bg     (same as --color-danger-50)
```

---

## New CSS Classes Available

**Card Hover Effect:**
```css
.card-hover         /* Add to any card for lift + shadow on hover */
```

**Badges:**
```css
.badge              /* Base badge styles */
.badge-success      /* Green (for "live", "active", "success") */
.badge-warning      /* Amber (for "in progress", "pending", "warning") */
.badge-danger       /* Red (for "error", "failed", "blocked") */
.badge-info         /* Blue (for "planned", "info", "draft") */
```

---

## Pro Tips

1. **Don't over-use badges** — only for status indicators, not every tag
2. **Hover effects only on cards** — don't add to buttons (they have their own hover)
3. **Use semantic color names** — `--color-success-500` is clearer than `#10B981`
4. **Test dark mode** — semantic colors auto-adjust
5. **Keep gradients out** — plain backgrounds only

---

## Questions?

If you're unsure about a template:
1. Check if it's user-facing (high priority)
2. Check if it has cards (add hover)
3. Check if it has status (add badge)
4. When in doubt, keep it minimal

**Goal:** Subtle polish, not a redesign.

---

## Prompt for Other LLMs

Copy-paste this to GPT-4, Gemini, Claude (web), etc.:

```
Read this file: /Users/sidc/Projects/claude_code/fullstackpm.tech/INSTRUCTIONS_FOR_TEMPLATE_UPDATES.md

Then update these templates following the instructions:

1. app/templates/partials/project_card.html
2. app/templates/home.html
3. app/templates/projects/gallery.html
4. app/templates/projects/detail.html

Apply these changes:
- Add `card-hover` class to cards
- Add status badges (live, in progress, planned)
- Remove any gradient backgrounds (use plain white)
- Use semantic color variables where applicable

Return the complete updated files.
```

---

**CSS already updated:** ✅ Done by Claude Code
**Templates need updating:** ❌ Hand off to other LLM
**Token cost for other LLM:** ~8-10k (vs 20-30k if Claude Code did it)

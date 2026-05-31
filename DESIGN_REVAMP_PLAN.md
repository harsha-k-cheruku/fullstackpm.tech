# fullstackpm.tech — Design & Reorganization Revamp Plan

**Created:** 2026-05-24
**Status:** Ready to execute. Tasks are ordered by priority and independence.
**Revert safety:** All changes are git-tracked. Revert any task with `git revert <commit>` or full rollback with `git checkout 81173e6 -- .`

## How to use this plan

Each task is self-contained. Hand any task to Code Puppy with:
> "Read DESIGN_REVAMP_PLAN.md and execute Task X."

Code Puppy should read this file, execute only the specified task, commit, push, and mark the task done here.

---

## Design direction (context for Code Puppy)

**Shift:** Developer portfolio → Editorial publication
**Comp feel:** Lenny's Newsletter, The Pragmatic Engineer, Stratechery
**Brand:** "The Full Stack PM" — PM, AI builder, author

**Design principles:**
- Indigo accent over generic SaaS blue
- More whitespace — sections should breathe
- Consistent card treatment across all pages
- Typography-forward — headings command the page
- Newsletter-first hierarchy — the CTA is visible above the fold

---

## Phase 1 — Quick Fixes (no design risk, do these first)

### Task 1.1 — Fix duplicate navigation
**File:** `code/app/templates/base.html`
**What:** The navigation menu appears twice in the markup. Find and remove the duplicate.
**Verify:** View source on any page — `<nav>` should appear exactly once.
**Status:**  done

---

### Task 1.2 — Rename "Resources" to "Podcasts" in navigation
**Files:**
- `code/app/templates/partials/navbar.html` (or wherever nav links live in base.html)
- `code/app/templates/partials/footer.html`
**What:** Change the nav label "Resources" → "Podcasts". The URL `/resources` can stay the same for now.
**Verify:** Nav shows "Podcasts" on live site.
**Status:**  done

---

### Task 1.3 — Add "Newsletter" to navigation
**File:** `code/app/templates/partials/navbar.html` (or base.html)
**What:** Add a "Newsletter" link in the nav pointing to `https://fullstackpm.beehiiv.com/subscribe`. Opens in same tab.
**Position:** After "Blog", before "@fullstackpm"
**Verify:** Nav shows: Home · Projects · Blog · Newsletter · Podcasts · @fullstackpm
**Status:**  done

---

### Task 1.4 — Remove "Planned" projects from Projects page
**File:** `code/app/templates/projects/` or the projects content directory
**What:** The Projects page currently shows 5 "Planned" items (AI PM Toolkit, AI PM Decision System, LLM Prompt Evaluation Framework, A/B Test Analyzer, AI PM Bootcamp). Remove them from the displayed list. Don't delete the underlying content — just hide them from the page render (filter by status: only show `live` and `in_progress`).
**Verify:** Projects page shows only Live (7) and In Progress (3) items. No "Planned" section.
**Status:**  done

---

### Task 1.5 — Replace Beehiiv iframe with native styled form
**File:** `code/app/templates/partials/newsletter_signup.html`
**What:** The current embed is an `<iframe>` that can't inherit the site's CSS variables — it looks visually out of sync (wrong colors, wrong font). Replace it with a native HTML form that captures the email and redirects to Beehiiv's subscribe page with it pre-filled. No API key or publication UUID needed.

**How it works:** The form uses JavaScript to build the redirect URL `https://fullstackpm.beehiiv.com/subscribe?email=EMAIL` and opens it in a new tab. Beehiiv pre-fills the email so the user just clicks confirm — one extra step but fully styled to match the site.

**Replace the entire contents of `newsletter_signup.html` with:**
```html
<!-- partials/newsletter_signup.html -->
<form onsubmit="event.preventDefault(); window.open('https://fullstackpm.beehiiv.com/subscribe?email=' + encodeURIComponent(this.email.value), '_blank');"
      style="display:flex;flex-direction:column;gap:10px;max-width:400px;margin:0 auto;">
  <div style="display:flex;gap:8px;flex-wrap:wrap;">
    <input type="email"
           name="email"
           placeholder="your@email.com"
           required
           style="flex:1;min-width:0;padding:0.6rem 0.9rem;border-radius:8px;border:1px solid var(--color-border);background-color:var(--color-bg-primary);color:var(--color-text-primary);font-size:0.9rem;outline:none;">
    <button type="submit"
            style="padding:0.6rem 1.2rem;border-radius:8px;background-color:var(--color-accent);color:#fff;font-weight:600;font-size:0.9rem;border:none;cursor:pointer;white-space:nowrap;">
      Subscribe
    </button>
  </div>
  <p style="font-size:0.75rem;color:var(--color-text-tertiary);margin:0;">No spam. Unsubscribe any time.</p>
</form>
```

**Verify:** Newsletter signup form matches the site's colors (indigo button, correct background, correct text). Entering an email and clicking Subscribe opens a new tab to the Beehiiv subscribe page with the email pre-filled. No iframe border visible.
**Status:**  done

---

## Phase 2 — Color & Design System

### Task 2.1 — Swap accent color from SaaS blue to editorial indigo
**File:** `code/app/static/css/custom.css`
**What:** Replace the blue accent scale with an indigo scale.

Replace these values:
```css
/* OLD */
--color-blue-500: #2E8ECE;  /* Primary accent */
--color-blue-600: #2577AD;
--color-blue-400: #33A7DF;
--color-blue-300: #66BDE7;
--color-blue-200: #99D3EF;
--color-blue-100: #CCE9F7;
--color-blue-50:  #E6F4FB;
--color-blue-700: #1D608C;
--color-blue-800: #14496B;
--color-blue-900: #0C324A;
```

With:
```css
/* NEW — editorial indigo */
--color-blue-500: #6366F1;  /* Primary accent */
--color-blue-600: #4F46E5;
--color-blue-400: #818CF8;
--color-blue-300: #A5B4FC;
--color-blue-200: #C7D2FE;
--color-blue-100: #E0E7FF;
--color-blue-50:  #EEF2FF;
--color-blue-700: #4338CA;
--color-blue-800: #3730A3;
--color-blue-900: #312E81;
```

Dark mode override (in `.dark` block):
```css
--color-blue-50:  #1E1B4B;
--color-blue-100: #312E81;
```

**Verify:** Buttons, links, and accent elements across the site show indigo instead of blue. Check homepage, blog, projects.
**Status:**  done

---

### Task 2.2 — Soften light mode text from pure black to near-black
**File:** `code/app/static/css/custom.css`
**What:** In the `:root` block, change:
```css
/* OLD */
--color-text-primary: #000000;
--color-text-secondary: #1D1D1F;
--color-text-tertiary: #48484A;
```
To:
```css
/* NEW */
--color-text-primary: #0F172A;
--color-text-secondary: #374151;
--color-text-tertiary: #6B7280;
```
**Verify:** Light mode body text is softer — not pure black. Dark mode unchanged.
**Status:**  done

---

### Task 2.3 — Increase section spacing across the site
**File:** `code/app/static/css/custom.css`
**What:** Add a global section spacing rule at the bottom of custom.css:
```css
/* Section breathing room */
section + section {
  margin-top: 1rem;
}
```

Also find any `padding: 3rem 0` on section elements in templates and increase to `padding: 5rem 0`. Focus on `index.html` and `home.html` — these are the densest pages.

**Specific files to update:**
- `code/app/templates/index.html` — change all `padding: 3rem 0` on `<section>` elements to `padding: 5rem 0`

**Verify:** Homepage sections have more breathing room. The page feels less dense.
**Status:**  done

---

## Phase 3 — Homepage Reorganization

### Task 3.1 — Move newsletter section above the book section
**File:** `code/app/templates/index.html`
**What:** Currently the section order is:
1. Hero
2. PM Reading Stack
3. Live Tools
4. Latest Writing
5. Newsletter ← (just added)
6. Book (Memoirs)
7. Footer

Reorder to:
1. Hero
2. Newsletter ← move up
3. Live Tools
4. Book (Memoirs)
5. Latest Writing
6. PM Reading Stack ← move down
7. Footer

**Verify:** On homepage, newsletter section appears near the top, before the tools.
**Status:**  done

---

### Task 3.2 — Revamp the Hero section
**File:** `code/app/templates/index.html` (or `home.html` — check which is active)
**What:** The current hero is minimal. Upgrade it:

```html
<section style="padding: 6rem 0 4rem; border-bottom: 1px solid var(--color-border);">
  <div class="max-w-3xl mx-auto px-6">
    <p style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--color-accent);margin-bottom:1rem;">
      The Full Stack PM
    </p>
    <h1 style="font-size:2.5rem;font-weight:800;line-height:1.15;letter-spacing:-0.02em;color:var(--color-text-primary);margin-bottom:1.25rem;">
      The PM who ships.
    </h1>
    <p style="font-size:1.15rem;line-height:1.7;color:var(--color-text-secondary);max-width:560px;margin-bottom:2rem;">
      Product thinking, AI-native workflows, and the economics of what endures.
      Written by a PM who builds things and ships books.
    </p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;">
      <a href="https://fullstackpm.beehiiv.com/subscribe"
         style="display:inline-block;padding:0.65rem 1.4rem;border-radius:8px;background-color:var(--color-accent);color:#fff;font-weight:600;font-size:0.9rem;text-decoration:none;">
        Get the newsletter
      </a>
      <a href="/blog"
         style="display:inline-block;padding:0.65rem 1.4rem;border-radius:8px;border:1px solid var(--color-border);color:var(--color-text-primary);font-weight:600;font-size:0.9rem;text-decoration:none;">
        Read the blog →
      </a>
    </div>
  </div>
</section>
```

Replace the existing hero section with this. Keep the overall page structure intact.
**Verify:** Hero has "The Full Stack PM" label, strong H1, subtitle, two CTAs (newsletter + blog).
**Status:**  done

---

### Task 3.3 — Standardize card styling across homepage
**File:** `code/app/templates/index.html`
**What:** All cards on the homepage should use the same base style:
```
border: 1px solid var(--color-border)
border-radius: 12px
padding: 20px 24px
background-color: var(--color-bg-secondary)
```
Find any cards with inconsistent styling (missing border, different radius, inline background colors) and normalize them.

**Verify:** Visual scan of homepage — all cards look like they belong to the same system.
**Status:**  done

---

## Phase 4 — Resources/Podcasts Page

### Task 4.1 — Update Resources page heading and description
**File:** `code/app/templates/resources/index.html` (or wherever the resources page is)
**What:**
- Change page `<title>` from "Resources" to "Podcasts & Resources — The Full Stack PM"
- Change the H1 heading from "Resources" to "Podcasts & Resources"
- Add a subtitle: "Three automated shows. Daily intelligence, PM learning, and weekend market history."
**Verify:** Resources page shows updated heading and subtitle.
**Status:**  done

---

## Phase 5 — Footer Cleanup

### Task 5.1 — Update footer bio and links
**File:** `code/app/templates/partials/footer.html`
**What:**
- Update the bio text to match the new bio: "PM, AI builder, and author. Writing on product thinking, AI-native workflows, and what endures."
- Add newsletter link to footer quick links: "Newsletter" → `https://fullstackpm.beehiiv.com/subscribe`
- Change "Resources" → "Podcasts" in footer links
**Verify:** Footer shows updated bio and correct links.
**Status:**  done

---

## Phase 6 — Newspaper Layout

**Goal:** Shift the visual language from "SaaS product page" to "editorial publication." Pure white, typography-forward, ink-on-paper feel. Comp: Stratechery, Lenny's Newsletter.

### Task 6.1 — Go full white: remove all colored section backgrounds
**Files:** `code/app/templates/index.html`, `code/app/static/css/custom.css`
**What:**
- In `custom.css`, change `--color-bg-secondary` and `--color-bg-tertiary` to match `--color-bg-primary` (`#FFFFFF`) in `:root`. This removes the alternating slate section fills site-wide.
- In `index.html`, remove any inline `background-color: var(--color-bg-secondary)` on `<section>` elements — replace with nothing (transparent).
- Dark mode: leave `--color-bg-secondary` and `--color-bg-tertiary` unchanged in the `.dark` block — dark mode needs the layering.
**Verify:** Homepage in light mode is all white — no gray/slate band sections. Dark mode still has depth.
**Status:**  done

---

### Task 6.2 — Use thin horizontal rules as section dividers instead of background fills
**File:** `code/app/templates/index.html`
**What:** Each `<section>` currently uses `border-bottom: 1px solid var(--color-border)` — keep these. But remove any `padding`-heavy section wrappers that exist purely to create visual separation via background color. The border rule alone should divide sections.
**Verify:** Sections are clearly separated by a thin line, not by color blocks.
**Status:**  done

---

### Task 6.3 — Remove PM Reading Stack section from homepage
**File:** `code/app/templates/index.html`
**What:** Find and remove the entire PM Reading Stack `<section>` block. It promotes external content and dilutes the editorial identity. Do not delete any backend data — just remove the section from the homepage template.
**Verify:** Homepage no longer shows PM Reading Stack. Page feels less cluttered.
**Status:**  done

---

### Task 6.4 — Strengthen typography hierarchy
**File:** `code/app/static/css/custom.css`
**What:** Make headings heavier and more commanding — newspaper masthead energy.
- Change `.text-h1` `font-weight` from `700` to `800`
- Change `.text-h2` `font-weight` from `700` to `800`
- Change `.text-display` `font-weight` from `700` to `800`
- Add `letter-spacing: -0.03em` to `.text-display` (tighter = more editorial)
**Verify:** Section headings on homepage feel bolder and more authoritative.
**Status:**  done

---

### Task 6.5 — Tighten card borders, remove card background fills
**File:** `code/app/templates/index.html`
**What:** Cards currently use `background-color: var(--color-bg-secondary)` which adds a gray tint. In a newspaper layout, cards should be white with a clean border.
- Find all cards on the homepage with `background-color: var(--color-bg-secondary)` and change to `background-color: var(--color-bg-primary)` (white).
- Keep the `border: 1px solid var(--color-border)` and `border-radius: 12px` — just remove the fill.
**Verify:** Cards are white-on-white with a clean border outline. No gray fills.
**Status:**  done

---

## Execution order (recommended)

Run phases in this order. Each phase is independent but builds on the previous:

```
Phase 1 (Tasks 1.1 → 1.5)  — Quick fixes, no visual risk         ✅ done
Phase 2 (Tasks 2.1 → 2.3)  — Design system, biggest visual impact ✅ done
Phase 3 (Tasks 3.1 → 3.3)  — Homepage reorganization              ✅ done
Phase 4 (Task 4.1)          — Resources page                       ✅ done
Phase 5 (Task 5.1)          — Footer                               ✅ done
Phase 6 (Tasks 6.1 → 6.5)  — Newspaper layout                      done
```

**Total estimated Claude work:** ~2-3 hours across sessions
**Total estimated your review time:** ~30 minutes (spot-check each phase live on Render)

---

## Reverting if needed

To revert a single task:
```bash
git log --oneline   # find the commit hash
git revert <hash>   # creates a new undo commit
git push origin main
```

To revert everything back to pre-revamp state:
```bash
git checkout 81173e6 -- code/app/templates/ code/app/static/css/
git commit -m "Revert: roll back to pre-revamp state"
git push origin main
```

---

*Plan created 2026-05-24. Update task statuses as each is completed.*

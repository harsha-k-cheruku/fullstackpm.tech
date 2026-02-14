# Site Update Framework

This document defines how to handle different types of updates to fullstackpm.tech based on the type of request.

---

## Quick Reference Matrix

| Type | Location | Format | Process | Review |
|------|----------|--------|---------|--------|
| **Blog Post** | `/code/content/blog/` | Markdown + YAML | Write, commit, auto-deploy | Check formatting |
| **Project** | `/code/content/projects/` | Markdown + frontmatter | Write, add P/A/S cards, commit | Test detail page |
| **Tool/App** | `/code/app/routers/` | FastAPI + templates | Create router, templates, tests | Live at /tools/* |
| **Design/CSS** | `/code/app/static/css/` | CSS variables | Edit custom.css, test dark mode | Verify contrast |
| **Homepage** | `/code/app/templates/home.html` | Jinja2 + inline styles | Edit sections, test responsive | Check all screen sizes |
| **Page Content** | `/code/app/templates/` | Jinja2 | Edit template directly | Preview layout |

---

## 1. Blog Posts

### Request Type
"Write a blog post about...", "Add an article on...", "I have content about..."

### Process

**Step 1: Prepare Content**
- Receive article text (or read link if shareable)
- Clean up formatting
- Identify key themes for tags

**Step 2: Create Markdown File**
Location: `/code/content/blog/YYYY-MM-DD-title-slug.md`

**Step 3: Format with YAML Frontmatter**
```yaml
---
title: "Full Title Here"
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
excerpt: "2-3 sentence summary"
author: "Harsha Cheruku"
---
```

**Step 4: Write Content**
- **Avoid excessive blank lines** — max 1 blank line between paragraphs
- Use **## Headings** for major sections (not ###)
- Keep paragraphs **3-4 sentences max**
- Use **bold** for key concepts, not italics
- Use **bullet points** for lists (not numbered unless sequential)
- No more than 2-3 ## sections per 1000 words

**Step 5: Commit & Deploy**
```bash
git add code/content/blog/
git commit -m "Add blog post: Title"
git push origin main
```

**Blog posts appear at:** `/blog` (list) and `/blog/slug` (detail)

### Formatting Guidelines

✅ **Good:**
```markdown
## Section Title

First paragraph introduces the idea in 2-3 sentences.

Second paragraph develops it with examples.

- Bullet point one
- Bullet point two
```

❌ **Bad:**
```markdown
## Section Title

First paragraph.

Second paragraph.

### Subsection

Third paragraph.

#### Sub-subsection

Fourth paragraph.
```

---

## 2. Projects

### Request Type
"Create a project page for...", "Add a new tool...", "Showcase this product..."

### Process

**Step 1: Create Markdown File**
Location: `/code/content/projects/project-slug.md`

**Step 2: Add Required Frontmatter**
```yaml
---
title: "Project Name"
description: "One-line description"
tech_stack: [Tech1, Tech2, Tech3]
status: "shipped|shipping|in_progress|planned"
featured: true|false
display_order: 1
github_url: "https://github.com/..."
live_url: "https://..." OR "/tools/path"
problem: "Brief problem statement (1-2 sentences)"
approach: "How you're solving it (1-2 sentences)"
solution: "What you built (1-2 sentences)"
---
```

**Step 3: Write Content**
Start directly with:
```markdown
## What

Overview of what the project does and key features.

## Why

Problem statement and motivation.

## How

Technical approach, architecture, how it works.

## Technical Stack

- **Framework:** Details
- **Database:** Details
- **Deployment:** Details
```

**Step 4: Review**
- Problem/Approach/Solution cards display correctly
- What/Why/How sections are clear
- Links work (GitHub, Live URL)
- Tech stack is accurate

**Step 5: Commit**
```bash
git add code/content/projects/
git commit -m "Add/update project: Name"
git push origin main
```

**Projects appear at:** `/projects` (gallery) and `/projects/slug` (detail with P/A/S cards)

### Project Frontmatter Rules

- **status:** Use exact values: `shipped`, `shipping`, `in_progress`, `planned`
- **display_order:** Lower number = higher on page
- **featured:** `true` for homepage, `false` for gallery-only
- **problem/approach/solution:** Max 1 sentence each. These become the 3 cards at the top.

---

## 3. Tools & Apps

### Request Type
"Build a tool at...", "Create an interactive feature...", "Add a new endpoint..."

### Process

**Step 1: Design Structure**
- Define route: `/tools/feature-name`
- Identify database needs (new table? existing?)
- Plan templates

**Step 2: Create Backend**
Location: `/code/app/routers/feature.py`

```python
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

@router.get("/tools/feature-name")
async def feature_home(request: Request):
    return templates.TemplateResponse("feature/index.html", {...})
```

**Step 3: Create Templates**
Location: `/code/app/templates/feature/`

Structure:
```
feature/
├── index.html      (landing/main page)
├── practice.html   (if interactive)
└── partials/
    ├── feedback.html
    ├── cards.html
    └── etc.html
```

**Step 4: Add Models if Needed**
Location: `/code/app/models/feature.py`

For database tables:
```python
from sqlalchemy import Column, String, DateTime

class FeatureData(Base):
    __tablename__ = "feature_data"
    id = Column(Integer, primary_key=True)
    # ... fields
```

Update `/code/app/models/__init__.py` to export.

**Step 5: Include Router in main.py**
```python
from app.routers import feature

app.include_router(feature.router)
```

**Step 6: Update Dependencies**
If new packages needed, add to:
- `/code/requirements.txt`
- `/requirements.txt` (root)

**Step 7: Test**
- Run locally: `python -m uvicorn asgi:app --reload`
- Test all features
- Check mobile responsive
- Test dark mode

**Step 8: Add to Homepage**
Update `/code/app/templates/home.html` to link to the tool.

**Step 9: Commit**
```bash
git add code/app/
git add requirements.txt
git commit -m "Add tool: Feature name"
git push origin main
```

---

## 4. Design & Styling

### Request Type
"Fix readability...", "Improve colors...", "Dark mode issue..."

### Process

**Step 1: Identify Issue**
- Where does it occur? (blog, projects, homepage, etc.)
- Light mode or dark mode (or both)?
- What element? (text, background, borders, etc.)

**Step 2: Fix in CSS**
Location: `/code/app/static/css/custom.css`

Use **CSS variables** for colors:
```css
/* Light mode (default) */
--color-text-primary: #000000
--color-bg-secondary: #F8FAFC
--color-accent: #2E8ECE

/* Dark mode (in .dark selector) */
.dark {
  --color-text-primary: #FFFFFF
  --color-bg-secondary: #1E293B
}
```

**Step 3: Test Both Modes**
- Toggle dark mode
- Check all pages
- Verify sufficient contrast (AA standard: 4.5:1)

**Step 4: Responsive Check**
- Mobile (320px)
- Tablet (768px)
- Desktop (1024px+)

**Step 5: Commit**
```bash
git add code/app/static/css/
git commit -m "Fix: Improve readability of X element"
git push origin main
```

---

## 5. Homepage & Template Updates

### Request Type
"Update the homepage...", "Change the about page...", "Fix the navigation..."

### Process

**Step 1: Identify Section**
Location: `/code/app/templates/home.html` or `/code/app/templates/pages/about.html`

**Step 2: Edit Template**
- Keep inline styles using `style="..."` for dynamic colors
- Use Tailwind classes for spacing/layout
- Reference CSS variables: `var(--color-accent)`, `var(--color-text-primary)`

**Step 3: Test Responsive**
- Hamburger menu on mobile
- Card grid stacks on mobile
- Text readable on all sizes

**Step 4: Test Dark Mode**
- Toggle dark mode
- Check text contrast
- Verify all colors update

**Step 5: Commit**
```bash
git add code/app/templates/
git commit -m "Update: Homepage section changes"
git push origin main
```

---

## Commit Message Format

Always follow this pattern:
```
[Type]: What changed (concise)

Detailed explanation if needed.

Include: what file, why changed, impact.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

### Types
- **Add:** New feature/page/tool
- **Fix:** Bug fix or readability issue
- **Update:** Change to existing content
- **Improve:** Enhancement or optimization
- **Refactor:** Code restructuring

---

## Testing Checklist

### Before Every Commit

- [ ] Read the content (blog posts, project descriptions)
- [ ] Check formatting (no excessive blank lines)
- [ ] Verify dark mode (colors have sufficient contrast)
- [ ] Test responsive (mobile, tablet, desktop)
- [ ] Check links (GitHub, live URLs, internal links)
- [ ] No console errors (check browser dev tools)
- [ ] Commit message is clear and descriptive

### For Blogs
- [ ] Title is compelling
- [ ] Tags are relevant (3-5 tags)
- [ ] Excerpt summarizes main idea
- [ ] No more than ## headings
- [ ] Paragraphs are concise

### For Projects
- [ ] Problem/Approach/Solution are 1-2 sentences each
- [ ] What/Why/How sections are well-written
- [ ] Tech stack is accurate
- [ ] Links work (GitHub, live URL)
- [ ] Cards render correctly on detail page

### For Tools
- [ ] Route is at `/tools/name`
- [ ] All forms/buttons work
- [ ] Data saves/persists correctly
- [ ] Mobile responsive
- [ ] Dark mode compatible

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Blog formatting looks scattered | Too many blank lines | Remove extra blank lines, max 1 between paragraphs |
| Text unreadable in dark mode | Blue on blue background | Use white text on accent bg, or change bg color |
| Project cards don't show | Missing P/A/S frontmatter | Add problem, approach, solution fields |
| Tool doesn't appear | Router not included in main.py | Add `app.include_router(feature.router)` |
| Styles don't update | CSS cache | Hard refresh (Cmd+Shift+R / Ctrl+Shift+R) |
| Mobile looks broken | No Tailwind responsive classes | Add `md:`, `lg:` prefixes to classes |
| Homepage broken | Typo in template | Check Jinja2 syntax: `{{ }}` not `{ }` |

---

## Deployment Notes

**Auto-Deploy:**
- Push to GitHub main branch → Render auto-deploys within 1-2 minutes
- No manual actions needed
- New routes, templates, styles all pick up automatically

**Environment Variables:**
- For secrets: set in Render dashboard (OPENAI_API_KEY, etc.)
- For config: use app/config.py (Settings class)

**Database:**
- SQLite files auto-created on first access
- New models require import in `/code/app/models/__init__.py`

---

## Quick Start for Different Requests

### "Write a blog post about X"
1. Get content
2. Create `/code/content/blog/YYYY-MM-DD-slug.md`
3. Add frontmatter (title, date, tags, excerpt, author)
4. Write content (## sections, tight paragraphs)
5. Commit and push

### "Add a project page for X"
1. Create `/code/content/projects/slug.md`
2. Add frontmatter with P/A/S cards
3. Write What/Why/How sections
4. Commit and push

### "Build a tool at /tools/X"
1. Create router in `/code/app/routers/`
2. Create templates in `/code/app/templates/X/`
3. Create models if needed
4. Include router in main.py
5. Add to home.html
6. Test locally
7. Commit and push

### "Fix the styling/design"
1. Edit `/code/app/static/css/custom.css`
2. Test light + dark mode
3. Test responsive
4. Commit and push

---

**Use this framework to guide all updates to fullstackpm.tech.**

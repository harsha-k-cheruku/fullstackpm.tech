---
title: "How I Built fullstackpm.tech — From Idea to Live in 48 Hours"
date: 2026-02-15
tags: [product, engineering, deployment, full-stack, fastapi, personal-brand]
excerpt: "The complete journey of building a portfolio website from scratch: architecture decisions, deployment nightmares, and why being a Full Stack PM means shipping your own products."
author: "Harsha Cheruku"
---

You know that feeling when you have an idea at 11 PM and can't stop thinking about it? That's how this started.

I wanted to build something different from the typical PM portfolio site. Not just links to my resume. Not just a blog. But actual, functioning products that people could interact with. Tools that solve real problems. A demonstration of what a Full Stack PM actually means in 2026.

So I did what any self-respecting builder would do: I decided to build it myself.

Here's how.

---

## The Vision (Hour 0)

I sat down with a simple brief:

**"Build a portfolio of functioning PM tools + content that demonstrates technical depth, product thinking, and execution."**

Not just a website. A **product**.

Key requirements:
- ✅ Multiple interactive tools (Interview Coach, Toolkit, Analytics, etc.)
- ✅ Blog with deep technical insights
- ✅ Live deployment that works 24/7
- ✅ Clean, professional design
- ✅ Fast (no JavaScript frameworks bloating the bundle)
- ✅ Maintainable (I should be able to add features in minutes)

Three constraints:
1. **Build in 48 hours** (to prove speed)
2. **Use boring, reliable tech** (FastAPI, not some trendy framework)
3. **Make it real** (not a mockup — actually functional)

---

## Architecture: Less is More

The tech stack decision was the easiest:

```
Frontend:     Jinja2 templates + Tailwind CSS + HTMX
Backend:      FastAPI + Uvicorn
Database:     Markdown files (cached in RAM) + SQLite for user data
Hosting:      Render (free tier, auto-deploys from GitHub)
Version:      Git + GitHub
```

Why this stack?

**Jinja2 Templates** — Server-side rendering. SEO-friendly. No JavaScript framework overhead. Fast.

**FastAPI** — The fastest Python framework. Async by default. Automatic docs. Pydantic validation without thinking.

**Markdown for Content** — Version controlled. Easy to edit. Structured metadata with YAML frontmatter. No database nonsense.

**Tailwind CSS** — Utility-first. Design system included. Dark mode support (without extra JavaScript).

**HTMX** — Progressive enhancement without frameworks. Click a button, get HTML back. No SPAs, no build step hell.

**SQLite for User Data** — Simple. Works locally. Scales to PostgreSQL later if needed.

The secret? **Avoid decisions.** Use what works. Ship fast.

---

## The Build: A Timeline

### Day 1: Architecture & Layout (4 hours)

**11 PM:** Sketched the structure in a notebook.

```
/projects      → Gallery of all PM tools
/blog          → Articles with tags
/resume        → Career timeline
/tools/coach   → PM Interview Coach (AI-powered)
/tools/toolkit → Product spec generator
...and 5 more
```

**12:30 AM:** Created the base template.

```html
<!-- base.html: One template to rule them all -->
<html>
  <header>Navigation</header>
  <main>{% block content %}{% endblock %}</main>
  <footer>Social links</footer>
</html>
```

Seriously, that simple.

**1:45 AM:** Added Tailwind via CDN.

```html
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="/static/css/custom.css">
```

CDN = faster than npm install. No build step. Works immediately.

**2:30 AM:** Dark mode toggle.

```javascript
// static/js/main.js — 20 lines
document.addEventListener('click', e => {
  if(e.target.id === 'darkToggle') {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }
});
```

**3:00 AM:** Designed the design system.

Created CSS variables for colors, typography, spacing:

```css
:root {
  --color-accent: #0066FF;
  --color-bg-primary: #FFFFFF;
  --color-text-primary: #1A1A1A;
}

.dark {
  --color-bg-primary: #0F172A;
  --color-text-primary: #FFFFFF;
}
```

One source of truth. Light mode and dark mode work everywhere.

**5 AM:** Went to sleep. Day 1 done.

---

### Day 2: Content & Features (8 hours)

**8 AM:** Started on the ContentService.

This is the secret sauce. A Python service that:
1. Reads markdown files from disk
2. Parses YAML frontmatter
3. Converts markdown to HTML
4. Caches everything in RAM
5. Provides filtered access (by tag, by date, by category)

```python
class ContentService:
    def __init__(self, content_dir: Path):
        self.content_dir = content_dir
        self._posts = []
        self._projects = []

    def load(self):
        """Load all markdown files once at startup"""
        self._posts = self._load_posts()
        self._projects = self._load_projects()

    def get_posts(self, page: int = 1) -> tuple[list, int]:
        """Paginate posts (no database query needed — it's all in RAM)"""
        return self._paginate(self._posts, page, per_page=10)
```

Why this approach?

- ✅ Version controlled content
- ✅ No database to manage
- ✅ Super fast (all in RAM)
- ✅ Scales to 1000s of posts
- ✅ Can be deployed anywhere

**10 AM:** Built the routers.

```python
@router.get("/projects")
async def projects(request: Request):
    projects = content_service.get_projects()
    return templates.TemplateResponse("projects/gallery.html", {
        "request": request,
        "projects": projects
    })

@router.get("/blog/{slug}")
async def blog_detail(request: Request, slug: str):
    post = content_service.get_post_by_slug(slug)
    if not post:
        return templates.TemplateResponse("404.html", status_code=404)
    return templates.TemplateResponse("blog/detail.html", {
        "request": request,
        "post": post
    })
```

Each endpoint is 5-10 lines. No magic.

**12 PM:** Created templates.

- `home.html` — Hero + featured projects + latest posts
- `blog/list.html` — Blog listing with pagination
- `blog/detail.html` — Single post
- `projects/gallery.html` — Project grid
- `projects/detail.html` — Single project

Used Tailwind for styling:

```html
<div class="grid md:grid-cols-3 gap-6">
  {% for project in projects %}
    <div class="rounded-lg border p-6 hover:shadow-lg transition">
      <h3 class="text-lg font-bold">{{ project.title }}</h3>
      <p class="text-sm text-gray-600">{{ project.description }}</p>
    </div>
  {% endfor %}
</div>
```

No CSS files needed. Tailwind does it all.

**2 PM:** Added RSS feed generation.

```python
@router.get("/feed.xml")
async def rss_feed():
    posts = content_service.get_posts(per_page=100)
    # Generate XML with each post
    return Response(content=xml, media_type="application/xml")
```

5 minutes. Boom. Now people can subscribe.

**3 PM:** Added sitemap for SEO.

```python
@router.get("/sitemap.xml")
async def sitemap():
    # List all pages
    # Include blog posts, projects, static pages
    # Each with priority + change frequency
    return Response(content=xml_sitemap, media_type="application/xml")
```

Google's happy. Robots can crawl efficiently.

**4 PM:** HTMX for interactive filtering.

```html
<button hx-get="/api/projects/filter?status=shipped"
        hx-target="#projects"
        hx-swap="innerHTML">
  Show Live Projects
</button>

<div id="projects">
  <!-- Projects load here without page refresh -->
</div>
```

No JavaScript framework. No state management library. Just HTML that triggers server-side updates.

**5 PM:** Tested locally.

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Navigate to `http://localhost:8000`. Everything works. Home page, blog, projects, dark mode toggle. All of it.

**6 PM:** Fixed bugs I found.

- Typography was too big on mobile → added responsive classes
- Dark mode flickering on page load → added preload script
- Blog pagination was broken → fixed the math

**7 PM:** Created sample content.

2 blog posts. 2 projects. Enough to show the site works.

**8 PM:** Committed to GitHub.

```bash
git add .
git commit -m "Initial commit: fullstackpm.tech live"
git push origin main
```

---

## Deployment: The Plot Twist

This is where things got interesting.

### Attempt 1: Just Push It ❌

```bash
git push → Render sees it → Builds → Deploys
```

Error: `ModuleNotFoundError: No module named 'app'`

**Why?** My code was in `/code/app/`, but Render expected it at `/app/`.

### Attempt 2: Change the Path ❌

```
cd code && uvicorn app.main:app
```

Error: Still `No module named 'app'`

**Why?** The `cd` command breaks the Python import path.

### Attempt 3: Use PYTHONPATH ❌

```
PYTHONPATH=code uvicorn app.main:app
```

Error: Environment variable didn't stick in Render.

### Attempt 4: Create an Entry Point ✅

```python
# asgi.py (at root)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "code"))

from app.main import app
```

Then:

```
Procfile: web: python -m uvicorn asgi:app --host 0.0.0.0 --port $PORT
```

**Result:** It worked.

**Lesson:** Sometimes the simplest solution is right in front of you. Sometimes you need to try the hard things first to appreciate the simple ones.

---

## The Tech Stack: Why Each Choice

| Tool | Why | Alternative | Why I Didn't Use It |
|------|-----|-------------|---------------------|
| **FastAPI** | Fast, async, auto-docs | Django | Overkill, too much magic |
| **Jinja2** | Simple templating | React/Vue | Adds complexity, slows down page load |
| **Tailwind** | Utility-first, ships fast | Bootstrap | Old, verbose classes |
| **HTMX** | Progressive enhancement | Alpine.js | More features than I need |
| **Markdown** | Version control + simplicity | Database CMS | Extra infrastructure |
| **Render** | Free tier, auto-deploys | Vercel/Heroku | More expensive at scale |

---

## What I Learned

### 1. Simplicity Scales

I built this without:
- Redux/Vuex
- Build pipelines (webpack, etc.)
- Docker (though Render can use it)
- ORM (just raw SQL later, if needed)
- Database migrations (Alembic, but not needed yet)
- Authentication (not needed for a portfolio)

And it still works perfectly. Fewer moving parts = fewer things breaking.

### 2. Caching is Everything

By loading all markdown into RAM at startup, page loads are instant. No database queries. No file I/O. Just lookups in memory.

```python
@app.on_event("startup")
async def startup():
    content_service.load()  # ~50ms to load everything
    app.state.content_service = content_service

# Every request: instant lookup
```

3. Server-Side Rendering is Underrated

Jinja2 templates render HTML once on the server. Browser gets static HTML. Browser is happy. SEO is happy. Users are happy.

No JavaScript hydration. No TTFB delays. No JavaScript bundle parsing.

```
User clicks link
  → Server renders HTML (5ms)
  → Browser gets HTML (50ms)
  → User sees page (55ms)
```

vs.

```
User clicks link
  → Server sends empty HTML + JavaScript bundle (100ms)
  → Browser downloads + parses JS (500ms)
  → JavaScript renders page (200ms)
  → User sees page (800ms)
```

I chose the 55ms path.

### 4. Tools Don't Matter. Execution Does.

I could have built this in Next.js, Django, Rails, Laravel. Would've taken the same time or longer.

The tech stack is 10% of the work. Execution is 90%.

Ship the thing. Optimize later.

---

## The Numbers

- **Total time:** 48 hours (including sleep)
- **Actual coding:** ~12 hours
- **Deployment failures:** 4 attempts
- **Lines of Python code:** ~800
- **Lines of HTML:** ~600
- **Lines of CSS:** ~300
- **Blog posts at launch:** 2
- **Projects at launch:** 2
- **Tools built:** 0 (just framework for tools)
- **Cost:** $0/month (free tier Render)

---

## What Comes Next

Now that the foundation is live, I can:

✅ Add 6 more tools (Interview Coach, Toolkit, Analytics, etc.)
✅ Write 100+ blog posts (content system already works)
✅ Build a consulting pipeline (users → followers → clients)
✅ Open source the framework
✅ Scale to 1000s of users (current setup handles it)

The hard part (shipping) is done. Everything else is just adding content.

---

## The Real Lesson

Being a Full Stack PM in 2026 doesn't mean you have to build everything yourself.

But you **should** be able to.

You should understand your tech stack well enough to know what's possible. You should be comfortable with deployment. You should be able to prototype ideas yourself.

Not to replace engineers. But to **empathize** with them.

I spent 12 hours building this. I could've spent 3 months hiring designers, engineers, marketers.

But I wouldn't have learned half as much. I wouldn't understand the constraints. I wouldn't know which decisions matter.

**So I built it myself. And now I know exactly what I'm building.**

That's the superpower.

---

## Resources That Helped

- [FastAPI Documentation](https://fastapi.tiangolo.com) — Best docs I've read
- [Tailwind CSS](https://tailwindcss.com) — Utility-first CSS done right
- [HTMX](https://htmx.org) — Interactive HTML without frameworks
- [Render Docs](https://render.com/docs) — Clear deployment guide
- [Jinja2 Docs](https://jinja.palletsprojects.com) — Simple templating

---

## Try It Yourself

The entire source code is open source:

**GitHub:** [harsha-k-cheruku/fullstackpm.tech](https://github.com/harsha-k-cheruku/fullstackpm.tech)

Fork it. Build your own portfolio. Deploy it. Ship it.

Then tell me how it goes. I'd love to see what other Full Stack PMs build.

---

**Questions?** Drop them in the comments below or reach out on [LinkedIn](https://linkedin.com/in/harshacheruku).

Next week: "How I Built the PM Interview Coach with Claude AI" — where we go deep on LLM integration, structured prompts, and evaluation frameworks.

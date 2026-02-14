# Architecture: How Your App Works

## The Big Picture

Your website is a **server-side rendered web application**. Here's what that means:

```
User's Browser                    Your Server (Render)
    │                                  │
    ├─→ "Give me the home page"  ───→  ├─ Receive request
    │                                  ├─ Load data (blog posts, projects)
    │                                  ├─ Render HTML from templates
    │← Send HTML (complete page)  ←─── ├─ Send back full HTML
    │                                  │
    ├─ Display page in browser         │
```

**This is different from modern JavaScript apps** where the browser does all the work. You're using the older, simpler model.

---

## Your Application Structure

### Layer 1: Entry Point (asgi.py)

```
asgi.py
├─ Tells Python where to find modules
└─ Imports and exposes the FastAPI app
```

**Why it exists:** Render needs a clear entry point. `asgi.py` is the "front door" of your app.

---

### Layer 2: Application Core (code/app/main.py)

```
main.py
├─ Creates FastAPI app instance
├─ Mounts static files (CSS, JavaScript)
├─ Registers routers (different URL endpoints)
├─ Sets up templating engine (Jinja2)
└─ Defines error handlers (404, etc.)
```

**What this does:** Sets up the basic FastAPI app and wires everything together.

---

### Layer 3: Routers (code/app/routers/)

Routers handle specific URL paths:

```
pages.py
├─ GET /              → Home page
├─ GET /about         → About page
├─ GET /contact       → Contact page
└─ GET /resume        → Resume page

blog.py
├─ GET /blog          → List all blog posts
├─ GET /blog/{slug}   → Individual blog post
├─ GET /blog/tag/{tag} → Posts tagged with X
└─ GET /api/blog/posts → HTMX partial (load more)

projects.py
├─ GET /projects      → Project gallery
├─ GET /projects/{slug} → Project detail
└─ GET /api/projects/filter → HTMX filtering

seo.py
├─ GET /feed.xml      → RSS feed
├─ GET /sitemap.xml   → XML sitemap for Google
└─ GET /robots.txt    → Instructions for web crawlers
```

**How requests flow:**
```
Browser: GET /blog/my-first-post
    ↓
FastAPI routes to blog.py
    ↓
blog.py calls content_service.get_post_by_slug("my-first-post")
    ↓
ContentService finds the markdown file
    ↓
Content service renders markdown → HTML
    ↓
blog.py loads "blog/detail.html" template
    ↓
Template fills in the post data
    ↓
HTML is sent back to browser
```

---

### Layer 4: Services (code/app/services/)

Services do the heavy lifting:

```
ContentService (content.py)
├─ Loads markdown files from disk
├─ Parses YAML frontmatter (metadata)
├─ Converts markdown to HTML
├─ Caches everything in memory
├─ Provides methods:
│   ├─ get_posts() → paginated list
│   ├─ get_post_by_slug(slug) → single post
│   ├─ get_posts_by_tag(tag) → filtered posts
│   ├─ get_projects() → all projects
│   ├─ get_project_by_slug(slug) → single project
│   └─ get_all_tags() → unique tags
│
FeedService (feed.py)
├─ Generates RSS XML
├─ Takes blog posts as input
└─ Formats each post as RSS item
```

**Why separate services?** Keeps business logic separate from HTTP layer. Makes testing easier and code more reusable.

---

### Layer 5: Templates (code/app/templates/)

Templates are HTML with placeholders:

```
base.html                          ← Master template
├─ Header and navigation
├─ {% block content %} ... {% endblock %}
└─ Footer

home.html (extends base.html)
├─ Hero section
├─ Impact & expertise grid
├─ Featured projects
├─ Latest writing
└─ CTA section

blog/
├─ list.html                       ← Blog post listing
├─ detail.html                     ← Single blog post
├─ tag.html                        ← Posts by tag
└─ partials/
    └─ post_list.html              ← HTMX snippet (load more posts)

projects/
├─ gallery.html                    ← Project grid
├─ detail.html                     ← Single project
└─ partials/
    └─ project_grid.html           ← HTMX snippet (filter projects)
```

**How templating works:**
```
Template (blog/detail.html):
    <h1>{{ post.title }}</h1>
    <p>By {{ post.author }} on {{ post.date }}</p>
    {{ post.html_content | safe }}

Router passes data:
    post = {
        title: "What Is a Full Stack PM?",
        author: "Harsha Cheruku",
        date: "2026-02-20",
        html_content: "<p>A Full Stack PM...</p>"
    }

Result (rendered HTML):
    <h1>What Is a Full Stack PM?</h1>
    <p>By Harsha Cheruku on 2026-02-20</p>
    <p>A Full Stack PM...</p>
```

---

### Layer 6: Content (code/content/)

Your actual content lives here:

```
content/
├─ blog/
│   ├─ 2026-02-20-what-is-a-fullstack-pm.md
│   └─ 2026-02-15-why-im-building-in-public.md
│
└─ projects/
    ├─ portfolio-site.md
    └─ pm-interview-coach.md
```

**Format (markdown with YAML frontmatter):**
```yaml
---
title: "What Is a Full Stack PM?"
date: 2026-02-20
tags: [product-management, ai, career]
excerpt: "The next generation of great product managers..."
author: "Harsha Cheruku"
---

# Content starts here

A Full Stack PM blends product strategy...
```

**Why markdown?**
- Easy to write and read
- Version-controlled in Git
- No database needed
- Can be edited in any text editor

---

### Layer 7: Static Files (code/app/static/)

```
static/
├─ css/
│   └─ custom.css                  ← Design tokens, dark mode, typography
└─ js/
    └─ main.js                     ← Dark mode toggle, interactivity
```

**How they're served:**
```
Browser: GET /static/css/custom.css
    ↓
FastAPI sees /static/ prefix
    ↓
Serves file directly from code/app/static/
    ↓
Browser receives CSS file
```

---

## Request Flow: End-to-End

**Example: User visits https://fullstackpm.tech/blog/why-im-building-in-public**

```
1. Browser sends HTTP GET request to /blog/why-im-building-in-public

2. Request reaches Render servers (uvicorn server)

3. FastAPI router sees /blog/{slug} pattern matches

4. blog.py router handler is called with slug="why-im-building-in-public"

5. Handler calls:
   content_service.get_post_by_slug("why-im-building-in-public")

6. ContentService:
   - Looks in code/content/blog/ directory
   - Finds 2026-02-15-why-im-building-in-public.md
   - Loads the file
   - Parses YAML frontmatter → metadata
   - Converts markdown content → HTML
   - Returns BlogPost object

7. Router checks if post exists (404 if not)

8. Router loads template: blog/detail.html

9. Router passes context to template:
   {
     "request": request_object,
     "post": post_object,
     "config": settings,
     "title": "Why I'm Building in Public - Blog"
   }

10. Jinja2 template engine renders HTML:
    - Fills in {{ post.title }}, {{ post.author }}, etc.
    - Includes base.html for header/footer
    - Combines everything into one HTML document

11. FastAPI returns HTML to browser

12. Browser receives HTML and displays the page

13. Browser also loads CSS from /static/css/custom.css
    (Separate request, same process)

14. Page appears on user's screen
```

---

## Configuration (code/app/config.py)

```python
class Settings(BaseSettings):
    app_name: str = "fullstackpm.tech"
    base_dir: Path = Path(__file__).resolve().parent.parent
    content_dir: Path = base_dir / "content"
    templates_dir: Path = base_dir / "app" / "templates"
    static_dir: Path = base_dir / "app" / "static"

    site_title: str = "fullstackpm.tech"
    site_description: str = "Portfolio of Harsha Cheruku..."
    github_url: str = "https://github.com/harsha-k-cheruku"
```

**Why?**
- Centralizes all configuration in one place
- Easy to change without editing code
- Can read from environment variables (for secrets)
- Path configuration makes code portable

---

## Technology Stack Explained

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Runtime** | Python 3.14 | Programming language |
| **Web Framework** | FastAPI | Handles HTTP requests/responses |
| **Server** | Uvicorn | ASGI server (runs FastAPI) |
| **Templates** | Jinja2 | Renders HTML with dynamic data |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **Hosting** | Render | Cloud platform |
| **Version Control** | Git + GitHub | Track code changes |
| **Content Format** | Markdown | Easy-to-write content format |

---

## Key Design Decisions

### Why FastAPI?
- Fast (hence the name)
- Automatic API documentation
- Built-in validation
- Easy to deploy
- Great for both APIs and traditional websites

### Why Server-Side Rendering?
- Simpler to build and maintain
- Better for SEO (Google can read content)
- Less JavaScript to manage
- Faster initial page load

### Why Markdown + YAML?
- No database needed (simpler deployment)
- Version-controlled content
- Easy for anyone to edit
- Works great for blogs/portfolios

### Why Render?
- Free tier for small projects
- Auto-deploys from GitHub
- Simple for beginners
- Good enough for thousands of users

---

## Performance: How It Stays Fast

**Caching:**
- ContentService loads all markdown files into memory on startup
- No disk reads per request (everything is in RAM)

**Content Delivery:**
- Static files served directly by web server
- Tailwind CSS loaded from CDN (not your server)

**Rendering:**
- Markdown → HTML conversion happens once (at startup, not per request)
- Templates are compiled by Jinja2 (fast rendering)

---

## Next: Adding Features

When you want to add something new:

1. **New page?** → Create router + template
2. **New blog post?** → Drop markdown file in content/blog/
3. **New project?** → Drop markdown file in content/projects/
4. **New styling?** → Add CSS to custom.css
5. **New feature?** → Create service + router

Everything auto-reloads on Render when you push to GitHub.

---

**Key Takeaway:** Your app follows a classic **3-tier architecture**: Presentation (templates), Business Logic (services), and Data (content files). This is the same pattern used by most web applications, from tiny projects to massive platforms.

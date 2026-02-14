# fullstackpm.tech

Personal portfolio and project showcase for a Full Stack PM.

**Live site:** https://fullstackpm.tech

---

## What This Is

A portfolio that demonstrates Full Stack PM capabilities through **shipped work** rather than just ideas.

Features:
- 📝 Blog posts on product strategy and AI workflows
- 🛠️ Live tools (Interview Coach, Analytics Dashboard)
- 📊 Case studies showing real PM execution
- 🎓 Resources for aspiring Full Stack PMs

Built with **FastAPI + Jinja2 + Tailwind + HTMX** and deployed to Render.

---

## Quick Start

### Visit the Site
https://fullstackpm.tech

### Develop Locally
```bash
# Setup
git clone https://github.com/harsha-k-cheruku/fullstackpm.tech.git
cd fullstackpm.tech
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
cd code
python -m uvicorn app.main:app --reload

# Visit http://localhost:8001
```

**Full setup guide:** See [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)

---

## Folder Structure

```
fullstackpm.tech/                    ← You are here
├── code/                            ← FastAPI application (deployed to Render)
│   ├── app/main.py                 ← App entry point
│   ├── routers/                    ← API endpoints (blog, projects, tools)
│   ├── services/                   ← Business logic
│   ├── models/                     ← Database models
│   ├── templates/                  ← Jinja2 HTML templates
│   └── static/                     ← CSS, JavaScript
│
├── content/                         ← Markdown content (blog posts, projects)
│   ├── blog/                       ← Blog posts
│   └── projects/                   ← Project write-ups
│
├── docs/                           ← Developer documentation
│   ├── ARCHITECTURE.md             ← System design & tech stack
│   ├── DEPLOYMENT.md               ← How Render deployment works
│   └── DEVELOPMENT.md              ← Local setup guide
│
├── project_ideas/                  ← Incubation folder for new concepts
│   ├── 01_PM_TECH_COMPANION.md     ← AI-powered technical planning tool
│   ├── 02_BOOK_MARKETING_GENERATOR.md
│   └── README.md                   ← How to develop project ideas
│
├── PROJECTS_STATUS.md              ← Track what's being built
├── SITE_UPDATE_FRAMEWORK.md        ← How to add content (blog, projects, tools)
├── BUILD_*.md files                ← Project plans for builders
├── requirements.txt                ← Python dependencies
├── asgi.py                         ← Render entry point
├── Procfile                        ← Render deployment config
└── README.md                       ← This file
```

**Key principle:** Organize for humans, not machines. Render only cares about `/code`, `requirements.txt`, and `Procfile`.

---

## Live Projects

| Project | Status | URL | Tech |
|---------|--------|-----|------|
| **PM Interview Coach** | 🟢 Live | /tools/interview-coach | FastAPI + OpenAI + HTMX |
| **Marketplace Analytics** | 🟢 Live | /tools/marketplace-analytics | FastAPI + Pandas + Chart.js |
| **Blog** | 🟢 Live | /blog | Markdown + SQLite comments |
| **Projects Portfolio** | 🟢 Live | /projects | Markdown content |
| **PM Tech Companion** | 🟡 In Dev | `/tools/pm-tech-companion` | FastAPI + OpenAI |
| **Book Marketing Generator** | 📋 Planned | TBD | FastAPI + OpenAI |

See [PROJECTS_STATUS.md](./PROJECTS_STATUS.md) for detailed status, metrics, and extraction timeline.

---

## How to Contribute

### Add a Blog Post
1. Create `code/content/blog/YYYY-MM-DD-slug.md`
2. Write YAML frontmatter + markdown content
3. `git push origin main`
4. Render auto-deploys in 1-2 minutes

See [SITE_UPDATE_FRAMEWORK.md](./SITE_UPDATE_FRAMEWORK.md) for detailed instructions.

### Add a Project Page
1. Create `code/content/projects/slug.md`
2. Include Problem/Approach/Solution cards
3. Write What/Why/How sections
4. `git push origin main`

See [SITE_UPDATE_FRAMEWORK.md](./SITE_UPDATE_FRAMEWORK.md) for detailed instructions.

### Build a New Tool
1. Create router in `code/app/routers/`
2. Create templates in `code/app/templates/`
3. Add to `code/app/main.py`
4. Test locally
5. `git push origin main`

See [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md) for step-by-step guide.

---

## Documentation

- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** — System design, tech stack, data models, request flow
- **[DEPLOYMENT.md](./docs/DEPLOYMENT.md)** — How Render hosting works, why reorganization doesn't break anything
- **[DEVELOPMENT.md](./docs/DEVELOPMENT.md)** — Local setup, common tasks, debugging
- **[SITE_UPDATE_FRAMEWORK.md](./SITE_UPDATE_FRAMEWORK.md)** — How to update the site based on request type
- **[PROJECTS_STATUS.md](./PROJECTS_STATUS.md)** — What's being built, extraction timeline
- **[project_ideas/README.md](./project_ideas/README.md)** — How to develop new project concepts

---

## Technology Stack

### Backend
- **FastAPI** — Lightweight Python web framework, async support, auto-docs
- **Jinja2** — Server-side templating, SEO-friendly
- **SQLAlchemy** — ORM for database models
- **OpenAI API** — AI evaluation and content generation

### Frontend
- **Tailwind CSS** — Utility-first styling, dark mode support
- **HTMX** — Real-time updates without JavaScript frameworks
- **Chart.js** — Data visualization (charts and graphs)

### Infrastructure
- **Render** — PaaS hosting, auto-deploys from GitHub
- **SQLite** — Lightweight database for comments, sessions
- **GitHub** — Version control, content management

---

## Deployment

Automatic deployments via Render:

```
You push to main branch
    ↓
GitHub webhook triggers Render
    ↓
Render runs: pip install -r requirements.txt
    ↓
Render starts: python -m uvicorn asgi:app
    ↓
Your site updates (1-2 minutes)
```

See [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed explanation.

---

## Project Ideas & Long-Term Vision

See [project_ideas/README.md](./project_ideas/README.md) for concepts in development.

Current ideas:
- 🛠️ **PM Tech Companion** — AI tool that translates PM intent into technical architecture
- 📚 **Book Marketing Generator** — AI content generation for book marketing across platforms
- 👥 **PM Community Platform** — Forum for sharing architectural decisions and patterns
- 📖 **Books Portal** — Consolidate all writing under one section

---

## Metrics & Monitoring

### Current Usage (February 2026)
- ~100 monthly visitors
- ~20 blog post views/day
- ~5 Interview Coach evaluations/day
- ~$20/month total hosting cost

### OpenAI API Cost
- Interview Coach: ~$3-5/month (1000 evaluations)
- Future tools: ~$5-10/month

---

## License

This code is provided as-is. Feel free to fork, study, and learn from the patterns and architecture.

---

## Questions?

- **How do I set up locally?** → [DEVELOPMENT.md](./docs/DEVELOPMENT.md)
- **How does deployment work?** → [DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- **How do I add content?** → [SITE_UPDATE_FRAMEWORK.md](./SITE_UPDATE_FRAMEWORK.md)
- **What's the system design?** → [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **What's being built next?** → [PROJECTS_STATUS.md](./PROJECTS_STATUS.md)

---

## About

Built by [Harsha Cheruku](https://www.linkedin.com/in/harshacheruku/) — Full Stack PM, builder, writer.

- 🔗 LinkedIn: https://linkedin.com/in/harshacheruku
- 📚 Book: [Memoirs of a Mediocre Manager](https://www.amazon.com/Memoirs-Mediocre-Manager-Surviving-Cross-Functional/dp/B0G2X59WRL/)
- 🐦 Twitter: [@harshacheruku](https://twitter.com/harshacheruku)

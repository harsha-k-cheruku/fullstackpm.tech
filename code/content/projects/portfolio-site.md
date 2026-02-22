---
title: "fullstackpm.tech"
description: "Portfolio site showcasing AI PM projects, writing, and career highlights."
tech_stack: [FastAPI, Jinja2, Tailwind CSS, HTMX, Markdown]
status: "live"
featured: true
display_order: 4
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "https://www.fullstackpm.tech"
problem: "Most PM portfolios show opinions, not outcomes. Decks and case studies don't prove you can actually build and ship products."
approach: "Build a working product portfolio where projects live as markdown, deploy with one push, and demonstrate Full Stack PM capabilities through shipped artifacts."
solution: "A fast, simple architecture using FastAPI + Jinja2 that shows PM work (blog), PM thinking (projects with What/Why/How), and PM execution (working tools like Interview Coach)."
---
## What

A full-stack portfolio that demonstrates product thinking through shipped artifacts.

**What you'll find here:**
- **Projects** — Interactive tools and products I've built (like this Interview Coach)
- **Writing** — Deep dives on product strategy, Full Stack PM philosophy, deployment
- **Resume** — Career progression from SDE → PM → Builder (16+ years)
- **Book** — "Memoirs of a Mediocre Manager" — satire on tech leadership
- **Comments** — Real conversations on blog posts with other builders

This isn't a static resume site. It's a working demonstration of product execution.

## Why

Most PM portfolios are portfolios of opinions: decks, case studies, strategic frameworks.

But opinions are cheap. Shipped products aren't.

I built this because:
- **Show, don't tell.** Anyone can write about product thinking. Fewer actually ship things.
- **Demonstrate Full Stack capability.** A PM who understands tech, can prototype, and deploys their own work is rare.
- **Practice what you preach.** If I write about fast iteration, the site should prove I can ship quickly.
- **Build in public.** Every project here is real, with real constraints, real tradeoffs, and real learnings.

This site is the answer to: *"What can a Full Stack PM actually build?"*

## How

**The architecture is deliberately simple:**

1. **Content as code** — Blog posts and projects live in markdown files, version-controlled on GitHub
2. **Fast rendering** — All content loads into memory at startup, so pages are instant
3. **Design system first** — One set of CSS variables, one set of typography rules, works in light and dark mode
4. **Progressive enhancement** — HTMX for interactivity without JavaScript frameworks
5. **Database for user content** — Comments and interview coach sessions stored in SQLite

**The build process:**
- Write markdown files locally
- Push to GitHub
- Render auto-deploys (no manual steps)
- Site updates within 1 minute

**Key features:**
- **Blog with tags** — Filter articles by topic (product, engineering, strategy)
- **RSS feed** — Subscribe to updates
- **Sitemap + SEO** — Discoverable by search engines
- **Dark mode** — CSS variables, no JavaScript
- **Comments** — Real discussions on blog posts
- **Interview Coach** — Integrated PM interview practice tool
- **Mobile responsive** — Works on all devices

## Technical Stack

- **Backend:** FastAPI (Python) — lightweight, async, auto-documentation
- **Templates:** Jinja2 — server-side rendering, SEO-friendly
- **Styling:** Tailwind CSS + custom design tokens — fast, maintainable, accessible
- **Content:** Markdown + YAML — version controlled, easy to edit
- **Database:** SQLite — comments and interview sessions
- **Interactivity:** HTMX — real-time updates without frontend bloat
- **Deployment:** Render — single Procfile, auto-deploys on push

**Why this stack?**
- Fast to prototype and ship
- No build pipelines or JavaScript bundling
- Content lives in Git (your version control system)
- Scales from 1 user to 1M users with minimal changes

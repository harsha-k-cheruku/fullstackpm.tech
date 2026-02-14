---
title: "fullstackpm.tech"
description: "Portfolio site showcasing AI PM projects, writing, and career highlights."
tech_stack: [FastAPI, Jinja2, Tailwind CSS, HTMX, Markdown]
status: "in_progress"
featured: true
display_order: 1
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: ""
---
## Problem
Product work often disappears into decks and internal documents. I wanted a portfolio that demonstrates product thinking through shipped artifacts: written analysis, interactive project case studies, and working prototypes. The goal was to create a site that feels like a product — not just a profile.

## Approach
I designed a FastAPI-first architecture so content could live in markdown while the UX still feels handcrafted. The layout emphasizes narrative and clarity: a homepage that positions the product thesis, project cards that show outcomes, and a resume timeline that communicates progression. Everything stays lightweight and fast to iterate.

## Solution
The site delivers a cohesive personal brand for a Full Stack AI PM. Projects are rendered from markdown with YAML frontmatter, enabling rapid iteration without a CMS. The UI uses a consistent tokenized design system, ensuring light/dark mode compatibility and strong accessibility defaults. The architecture supports future growth: RSS, blog filtering, and HTMX-powered updates.

## Technical Details
- **Backend:** FastAPI with Jinja2 templates
- **Content:** Markdown + YAML frontmatter parsed at startup
- **Styling:** Tailwind CSS CDN with design tokens
- **Interactivity:** HTMX for partial updates
- **Deployment:** Render with a lightweight Procfile setup

Next up: refine project detail templates, add blog pagination, and ship the first interactive project demo.

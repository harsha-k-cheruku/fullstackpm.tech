# Build Tasks — fullstackpm.tech

## Purpose

Each file in this folder is a **self-contained build instruction** that can be given to any LLM, AI coding tool, or developer. The LLM does not need prior context about the project — everything needed is included inline.

## How to Use

1. Pick a task file from the list below
2. Copy the entire contents
3. Paste into any LLM (Claude, GPT-4, Gemini, Copilot, etc.)
4. Save the output files to the paths specified in the instruction
5. Start the server: `cd code && python3 -m uvicorn app.main:app --reload --port 8001`
6. Verify using the acceptance test at the bottom of each task

## Task List

| # | File | What It Builds | Depends On | Complexity |
|---|------|---------------|------------|------------|
| 1 | `BUILD_01_CONTENT_SERVICE.md` | ContentService (markdown parsing, caching, filtering) + sample content files | None | Medium-High |
| 2 | `BUILD_02_PROJECTS.md` | Projects router + gallery + detail templates + project_card partial | Task 1 | Medium |
| 3 | `BUILD_03_BLOG.md` | Blog router + list/detail/tag templates + sample blog post | Task 1 | Medium |
| 4 | `BUILD_04_RESUME.md` | Resume route + experience timeline + skills grid | None | Medium |
| 5 | `BUILD_05_RSS_SEO.md` | RSS feed + sitemap.xml + robots.txt | Task 1 | Simple |
| 6 | `BUILD_06_HTMX.md` | Project filtering + blog pagination via HTMX | Tasks 2 & 3 | Medium-High |
| 7 | `BUILD_07_PROJECT_CARD.md` | Standalone project_card.html partial (for LLM benchmarking) | None | Simple |

## Dependency Graph

```
Independent (start anytime):
  Task 1: ContentService
  Task 4: Resume
  Task 7: Project Card (benchmark component)

After Task 1:
  Task 2: Projects
  Task 3: Blog
  Task 5: RSS + SEO

After Tasks 2 & 3:
  Task 6: HTMX Interactions
```

**Recommended order:** 1 & 4 in parallel → 2 & 3 in parallel → 5 → 6

Task 7 is a standalone benchmarking task — give it to multiple LLMs and compare outputs.

## What's Already Built

These files exist and are referenced in the build instructions:

| File | Purpose |
|------|---------|
| `code/app/main.py` | FastAPI app with lifespan, static files, 404 handler |
| `code/app/config.py` | Pydantic settings |
| `code/app/routers/pages.py` | Routes for /, /about, /contact |
| `code/app/templates/base.html` | Base layout with Tailwind CDN, HTMX, fonts, dark mode |
| `code/app/templates/partials/navbar.html` | Sticky nav with dark mode toggle |
| `code/app/templates/partials/footer.html` | 3-column footer |
| `code/app/templates/home.html` | Hero + featured projects + thesis |
| `code/app/templates/about.html` | Career narrative with timeline icons |
| `code/app/templates/contact.html` | Social/location cards |
| `code/app/static/css/custom.css` | Design tokens + typography + prose styles |
| `code/app/static/js/main.js` | Dark mode toggle + mobile menu |

## For LLM Benchmarking

To compare LLMs on the same task:

1. Use **Task 7 (Project Card)** — it's small, visual, and has clear acceptance criteria
2. Give the identical instruction to each LLM
3. Save outputs to `test_harness/outputs/project_card/{llm_name}.html`
4. Compare side-by-side using the test harness (see `strategy/11_LLM_EVAL_RUBRIC.md`)

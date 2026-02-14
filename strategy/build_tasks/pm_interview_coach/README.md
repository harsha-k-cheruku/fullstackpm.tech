# Build Tasks — PM Interview Coach

## Purpose

Each file in this folder is a **self-contained build instruction** that can be given to any LLM to generate working code. No prior context needed — everything is included inline.

## How to Use

1. Pick a task file from the list below
2. Copy the entire contents
3. Paste into any LLM (Claude, GPT-4, Gemini, Cursor, Copilot, etc.)
4. Save the output files to the paths specified
5. Run the acceptance test at the bottom of each task

## Task List

| # | File | What It Builds | Depends On | Complexity |
|---|------|---------------|------------|------------|
| 1 | `BUILD_01_DATABASE_MODELS.md` | SQLAlchemy models (Question, Attempt, Session) + Alembic migrations + seed data | None | Medium |
| 2 | `BUILD_02_BASE_TEMPLATES.md` | Base layout + nav + footer + shared partials (reuses portfolio base, creates app-specific layouts) | None | Simple |
| 3 | `BUILD_03_QUESTION_LOADER.md` | Script to parse Munna Kaka docs + PM Questions XLSX into database | Task 1 | Medium-High |
| 4 | `BUILD_04_AI_EVALUATOR.md` | Claude API integration + category-specific prompts + JSON scoring | Task 1 | High |
| 5 | `BUILD_05_PRACTICE_UI.md` | Practice page (question display, timer, answer form, feedback section) + routes | Tasks 1, 2, 4 | High |
| 6 | `BUILD_06_LANDING_HISTORY.md` | Landing page (category cards) + History page (filterable table) + routes | Tasks 1, 2 | Medium |
| 7 | `BUILD_07_PROGRESS_DASHBOARD.md` | Progress dashboard (stats cards + Chart.js visualizations) + stats service | Tasks 1, 2 | Medium-High |
| 8 | `BUILD_08_HTMX_INTERACTIONS.md` | HTMX partials for Next Question, Try Again, Filter History, Load More | Tasks 5, 6, 7 | Medium |

## Dependency Graph

```
Independent (start anytime):
  Task 1: Database Models + Migrations + Seed Data
  Task 2: Base Templates + Layout

After Task 1:
  Task 3: Question Loader Script
  Task 4: AI Evaluator Service

After Tasks 1 & 2:
  Task 6: Landing + History Pages

After Tasks 1, 2, 4:
  Task 5: Practice UI (core loop)

After Tasks 1, 2:
  Task 7: Progress Dashboard

After Tasks 5, 6, 7:
  Task 8: HTMX Interactions (progressive enhancement)
```

**Recommended order:**
- **Parallel start:** 1 & 2
- **Next parallel:** 3 & 4 (after Task 1)
- **Next parallel:** 5 & 6 (after Tasks 1, 2, 4)
- **Then:** 7 (after Tasks 1, 2)
- **Finally:** 8 (after all UI pages exist)

## Critical Path

The shortest path to a working prototype:
1. Task 1 (Database) → Task 3 (Seed Questions) → Task 4 (AI Evaluator) → Task 5 (Practice UI)

This gives you the core practice loop. Tasks 6, 7, 8 add history, progress, and polish.

## What's Already Built (From Portfolio Site)

These exist and are referenced in the build tasks:

| File | Purpose |
|------|---------|
| `fullstackpm.tech/code/app/templates/base.html` | Base HTML layout (fonts, Tailwind, HTMX, dark mode) |
| `fullstackpm.tech/code/app/static/css/custom.css` | Design tokens (colors, typography) |
| `fullstackpm.tech/code/app/config.py` | Pydantic settings pattern |

PM Interview Coach will be a **standalone FastAPI app** that reuses the design system but has its own:
- Database (separate SQLite file)
- Models, routers, services
- Templates (extends portfolio's base.html for consistent look)
- Static files (Chart.js, app-specific JS)

## For LLM Benchmarking

To compare LLMs on the same task, use:
- **Task 4 (AI Evaluator)** — tests prompt engineering, JSON parsing, error handling
- **Task 5 (Practice UI)** — tests full-stack integration, HTMX, UI polish

These are the most challenging tasks and will show clear quality differences.

## Directory Structure After All Tasks

```
pm-interview-coach/
├── app/
│   ├── __init__.py
│   ├── main.py                         # FastAPI app (Task 1)
│   ├── config.py                       # Settings (Task 1)
│   ├── database.py                     # SQLAlchemy setup (Task 1)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── question.py                 # Question model (Task 1)
│   │   ├── attempt.py                  # Attempt model (Task 1)
│   │   └── session.py                  # Session model (Task 1)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── pages.py                    # Landing, History (Task 6)
│   │   ├── practice.py                 # Practice routes (Task 5)
│   │   ├── stats.py                    # Progress routes (Task 7)
│   │   └── api.py                      # JSON API endpoints (Task 8)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── evaluator.py                # Claude API integration (Task 4)
│   │   ├── question_selector.py        # Random weighted selection (Task 5)
│   │   └── stats_engine.py             # Aggregate stats (Task 7)
│   ├── templates/
│   │   ├── index.html                  # Landing page (Task 6)
│   │   ├── practice.html               # Practice page (Task 5)
│   │   ├── history.html                # History page (Task 6)
│   │   ├── progress.html               # Progress dashboard (Task 7)
│   │   └── partials/
│   │       ├── question_card.html      # HTMX partial (Task 8)
│   │       ├── feedback.html           # HTMX partial (Task 5)
│   │       ├── history_table.html      # HTMX partial (Task 8)
│   │       └── stats_cards.html        # HTMX partial (Task 7)
│   └── static/
│       ├── css/
│       │   └── app.css                 # App-specific overrides (Task 2)
│       └── js/
│           └── main.js                 # Timer, Chart.js setup (Tasks 5, 7)
├── data/
│   ├── munna_kaka/                     # Question bank docs (provided by user)
│   └── pm_questions.xlsx               # Question bank XLSX (provided by user)
├── scripts/
│   └── load_questions.py               # Question loader script (Task 3)
├── alembic/                            # Database migrations (Task 1)
├── tests/
│   ├── test_evaluator.py               # Unit tests (Task 4)
│   ├── test_question_loader.py         # Unit tests (Task 3)
│   └── test_stats.py                   # Unit tests (Task 7)
├── requirements.txt                    # Python deps (Task 1)
├── .env.example                        # Environment vars template (Task 1)
├── Procfile                            # Render deployment (Task 1)
└── README.md                           # Project docs (Task 1)
```

## Success Criteria

After all tasks are complete, you should be able to:

1. **Seed questions:** `python scripts/load_questions.py` → populates database
2. **Start server:** `python -m uvicorn app.main:app --reload --port 8002`
3. **Browse categories:** Navigate to `http://localhost:8002/` → see 7 category cards
4. **Practice:** Click a category → get random question → type answer → submit → see AI evaluation with scores
5. **View history:** Navigate to `/history` → filter by category → see all attempts
6. **View progress:** Navigate to `/progress` → see score trends, category breakdown, practice heatmap
7. **HTMX works:** All interactions feel instant (no page reloads)

## Notes

- This is a **standalone app** — separate repo from fullstackpm.tech
- Database file: `pm_interview_coach.db` (SQLite for dev, PostgreSQL for prod)
- Claude API key required (from Anthropic Console)
- Question bank data NOT included in build tasks — user must provide `data/munna_kaka/` folder and `pm_questions.xlsx`
- All build tasks assume the question data structure is consistent (each task that needs sample data will describe the expected format)

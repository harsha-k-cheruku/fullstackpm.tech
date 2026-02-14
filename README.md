# fullstackpm.tech

Personal portfolio and project showcase for a Full Stack AI Product Manager.

**Live site:** [fullstackpm.tech](https://fullstackpm.tech)

## What This Is

A portfolio that proves — through shipped work — that the best Product Managers in 2026 don't just manage products, they build them.

## Tech Stack

- **Backend:** FastAPI + Jinja2 templates
- **Frontend:** Tailwind CSS + HTMX
- **Content:** Markdown with YAML frontmatter
- **Deployment:** Render

## Projects

| # | Project | Description | Status |
|---|---------|-------------|--------|
| 0 | Portfolio Site | This site — personal portfolio and blog | In Progress |
| 1 | PM Interview Coach | AI-powered interview practice with feedback | Planned |
| 2 | Marketplace Dashboard | Analytics dashboard with synthetic marketplace data | Planned |
| 3 | AI PM Toolkit | Generate PRDs, roadmaps, and user stories with AI | Planned |
| 4 | PM Decision System | AI-assisted build/kill feature decisions | Planned |
| 5 | Prompt Eval Framework | Systematic LLM prompt quality evaluation | Planned |
| 6 | A/B Test Analyzer | Statistical test analysis and sample size calculator | Planned |
| 7 | AI Bootcamp Case Study | Product leadership case study of existing work | Planned |

## Local Development

```bash
cd code
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000`

## Repository Structure

```
fullstackpm.tech/
├── strategy/       # Planning and spec documents for each project
├── code/           # Portfolio site source code
├── content/        # Blog posts and project write-ups (markdown)
└── README.md
```

## Strategy Documents

See `strategy/` for detailed planning docs:

- `00_MASTER_PLAN.md` — Overall vision, timeline, and project overview
- `01_PORTFOLIO_SITE.md` — Portfolio site product brief and technical spec
- `02_PM_INTERVIEW_COACH.md` — AI interview coach spec
- `03_MARKETPLACE_DASHBOARD.md` — Analytics dashboard spec
- `04_AI_PM_TOOLKIT.md` — PM artifact generator spec
- `05_AI_PM_DECISION_SYSTEM.md` — Feature decision system spec
- `06_LLM_PROMPT_EVAL_FRAMEWORK.md` — Prompt evaluation framework spec
- `07_AB_TEST_ANALYZER.md` — A/B test analyzer spec
- `08_AI_BOOTCAMP_CASE_STUDY.md` — Case study outline

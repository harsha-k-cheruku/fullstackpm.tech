# Project 3: AI PM Toolkit (Specs + Roadmaps + Stories)

## Product Brief

### Problem
PMs spend significant time writing the same types of documents: PRDs, user stories, roadmaps. The structure is formulaic but the thinking required is substantial. AI can accelerate the first draft dramatically — but only if the prompts are well-designed and the output is structured correctly. Most PMs use ChatGPT with ad-hoc prompts and get mediocre results.

### Solution
A multi-mode AI toolkit that generates structured PM artifacts from a product brief. Three modes: PRD Generator, Roadmap Builder, and Story Writer. Each mode uses carefully engineered prompts that produce consistently high-quality, structured output. Export to Markdown or PDF.

### Target Audience
- Interviewers evaluating your AI fluency and PM process understanding
- PMs who want better AI-assisted document generation
- You, demonstrating prompt engineering depth

### Non-Goals
- Not a full project management tool (no task tracking, no Jira integration)
- Not a collaborative editor
- Not a template library (AI generates fresh content each time)
- No user accounts (v1)

---

## Features

### MVP

| Feature | Description |
|---------|-------------|
| **Product Brief Input** | Structured form: product name, target user, problem statement, market context, constraints, goals |
| **PRD Generator** | Generates: problem statement, target user + JTBD, success metrics with targets, MVP scope (in/out), technical considerations, risks, open questions |
| **Roadmap Builder** | Generates: phased roadmap (Now/Next/Later or quarterly), milestones, dependencies, success criteria per phase |
| **Story Writer** | Generates: user stories with acceptance criteria, edge cases, technical notes. Grouped by epic. |
| **Output Editor** | Rendered markdown output with inline editing capability |
| **Export** | Download as Markdown (.md) or PDF |
| **History** | Save and browse past generations |

### v2
- Input an existing PRD and get AI critique/suggestions
- Generate from competitor analysis ("Build a better version of X")
- Team review workflow (share link, collect comments)
- Custom output templates

---

## Technical Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | HTMX + Tailwind CSS |
| AI | Claude API (structured output) |
| Database | SQLite |
| Export | python-markdown + WeasyPrint (PDF) |

### Prompt Engineering Strategy

Each mode has a dedicated system prompt with:
1. **Persona:** Senior PM at a top tech company
2. **Output schema:** Exact JSON structure expected
3. **Quality guardrails:** "Include specific, measurable metrics, not vague goals" / "Each user story must have at least 3 acceptance criteria"
4. **Context injection:** The product brief fields are injected into a structured user message

**PRD prompt focuses on:** completeness, measurability, scope clarity
**Roadmap prompt focuses on:** phasing logic, dependencies, realistic milestones
**Story prompt focuses on:** user-centric language, testable acceptance criteria, edge cases

### Data Model

```sql
generations (
  id TEXT PK,
  mode TEXT NOT NULL,          -- "prd", "roadmap", "stories"
  product_name TEXT,
  input_brief TEXT NOT NULL,   -- JSON of all input fields
  output_markdown TEXT,        -- Generated markdown content
  output_json TEXT,            -- Structured JSON output from AI
  model_used TEXT,
  tokens_used INTEGER,
  generation_time_ms INTEGER,
  created_at DATETIME,
  updated_at DATETIME
)
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Landing — mode selector (PRD / Roadmap / Stories) |
| GET | `/generate/{mode}` | Input form for selected mode |
| POST | `/api/generate` | Submit brief → AI generation → return result |
| GET | `/result/{id}` | View generated output |
| GET | `/result/{id}/edit` | Edit generated output |
| PUT | `/api/result/{id}` | Save edits |
| GET | `/api/result/{id}/export/md` | Download as Markdown |
| GET | `/api/result/{id}/export/pdf` | Download as PDF |
| GET | `/history` | Browse past generations |

### Application Structure

```
ai-pm-toolkit/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── routers/ (pages.py, generate.py, export.py)
│   ├── services/
│   │   ├── generator.py        # Orchestrates AI generation
│   │   ├── prompts/
│   │   │   ├── prd.py          # PRD system + user prompt templates
│   │   │   ├── roadmap.py      # Roadmap prompt templates
│   │   │   └── stories.py      # Story writer prompt templates
│   │   ├── claude_client.py    # API wrapper
│   │   └── exporter.py         # Markdown + PDF export
│   ├── templates/
│   └── static/
├── tests/
├── requirements.txt
└── README.md
```

---

## UI/UX

### Landing (`/`)
- Three large cards: PRD Generator, Roadmap Builder, Story Writer
- Each card: icon, name, description of what it generates, "Start" CTA
- Recent generations list below

### Input Form (`/generate/{mode}`)
- Shared fields: Product Name, Target User, Problem Statement
- Mode-specific fields:
  - PRD: Market Context, Constraints, Goals, Technical Context
  - Roadmap: Time Horizon, Team Size, Current State, Strategic Priorities
  - Stories: Epics/Features List, User Personas, Technical Constraints
- Submit → loading state with "Generating your {artifact}..." → HTMX swaps in result

### Result View (`/result/{id}`)
- Rendered markdown output (clean typography)
- Toolbar: Edit, Export MD, Export PDF, Regenerate, Copy to Clipboard
- Metadata sidebar: mode, generation time, token count, date

---

## Development Phases

### Phase 1: Foundation (Days 1-3)
- [ ] Project scaffold
- [ ] Input forms for all 3 modes
- [ ] Claude API client with structured output parsing
- [ ] PRD generation prompt + endpoint (start with one mode, validate quality)

### Phase 2: All Modes + Output (Days 4-7)
- [ ] Roadmap generation prompt + endpoint
- [ ] Story writer prompt + endpoint
- [ ] Result rendering page (markdown → HTML)
- [ ] Inline editing capability
- [ ] Save to database

### Phase 3: Export & Polish (Days 8-10)
- [ ] Markdown export
- [ ] PDF export (WeasyPrint)
- [ ] History page
- [ ] Regenerate with same inputs
- [ ] Responsive design, tests, deploy

---

## Next Step

Write the PRD generation prompt first and test it independently (even via CLI) to validate output quality before building the web UI. The prompt quality is the core value — everything else is scaffolding.

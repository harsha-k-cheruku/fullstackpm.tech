# Project 1: AI PM Interview Coach

## Product Brief

### Problem
PM interview prep is inefficient. You have a comprehensive question bank (Munna Kaka docs covering 7 categories + PM Questions.xlsx) but no way to practice with structured feedback. Reading answers isn't the same as formulating them under pressure. You need a practice partner that evaluates your answers against PM frameworks and tracks your improvement.

### Solution
An AI-powered interview practice tool that presents questions from your existing question bank, evaluates your answers using Claude API against category-specific PM frameworks, provides structured scoring and feedback, and tracks progress over time.

### Target Audience
- Primary: You (interview prep)
- Secondary: Other PM candidates (portfolio demonstration)

### Non-Goals
- Not a question authoring tool (questions come from existing docs)
- Not a mock interview simulator with back-and-forth dialogue (v1)
- No video/audio recording
- No user accounts (single-user, session-based)

---

## Features

### MVP (v1)

| Feature | Description |
|---------|-------------|
| **Question Browser** | Browse questions by category: Product Design, Strategy, Execution, Analytical, Project Management, App Critique, Cross-Functional |
| **Random Question** | "Surprise Me" button, weighted toward weaker categories if history exists |
| **Timed Practice** | Optional countdown timer (5, 10, or 15 minutes) |
| **Answer Submission** | Large textarea for typed answers |
| **AI Evaluation** | Claude API evaluates against category-specific frameworks with structured JSON output |
| **Scoring** | Overall score (1-10) + 3 sub-scores: Framework Adherence, Structure, Completeness |
| **Feedback** | Strengths list, improvements list, suggested framework, example point missed |
| **Radar Chart** | Visual radar chart of sub-scores per answer |
| **Practice History** | Filterable table of all past attempts with scores |
| **Progress Dashboard** | Score trends over time, category breakdown, weakest areas, practice streak |

### v2 (Post-Launch)
- Voice input via Web Speech API
- Follow-up probe questions from AI ("Tell me more about how you'd measure success...")
- Framework reference library page
- Spaced repetition scheduling
- PDF export of progress report

---

## Technical Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | HTMX + Tailwind CSS |
| AI | Claude API (Anthropic) |
| Database | SQLite (SQLAlchemy async) |
| Charts | Chart.js |

### Data Model

```sql
questions (
  id INTEGER PK,
  category TEXT NOT NULL,        -- "product_design", "strategy", etc.
  subcategory TEXT,
  difficulty TEXT DEFAULT 'medium',
  question_text TEXT NOT NULL,
  source TEXT NOT NULL,           -- "munna_kaka_design", "pm_questions_xlsx"
  frameworks TEXT,                -- JSON: ["CIRCLES", "STAR"]
  created_at DATETIME
)

attempts (
  id INTEGER PK,
  question_id INTEGER FK,
  session_id TEXT NOT NULL,
  answer_text TEXT NOT NULL,
  time_spent_sec INTEGER,
  overall_score REAL,             -- 1.0-10.0
  framework_score REAL,
  structure_score REAL,
  completeness_score REAL,
  strengths TEXT,                 -- JSON array
  improvements TEXT,              -- JSON array
  suggested_framework TEXT,
  example_point TEXT,
  raw_eval_json TEXT,
  created_at DATETIME
)

practice_sessions (
  id TEXT PK,                     -- UUID
  category_filter TEXT,
  mode TEXT DEFAULT 'standard',
  timer_minutes INTEGER,
  started_at DATETIME,
  ended_at DATETIME,
  questions_count INTEGER,
  avg_score REAL
)
```

### API Endpoints

**Pages (HTML):**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Landing — category cards with counts and scores |
| GET | `/practice/{category}` | Practice page for a category |
| GET | `/practice/random` | Random question (weighted) |
| GET | `/history` | Practice history with filters |
| GET | `/progress` | Progress dashboard with charts |

**API (HTMX partials + JSON):**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/questions` | List/filter questions |
| GET | `/api/questions/random` | Get random question |
| POST | `/api/practice/submit` | Submit answer for AI evaluation |
| GET | `/api/stats/overview` | Aggregate progress stats |
| GET | `/api/stats/by-category` | Score breakdown by category |
| GET | `/api/stats/trend` | Score trend over time |

**HTMX Partials:**
| Method | Path | Trigger |
|--------|------|---------|
| GET | `/partials/question-card/{id}` | "Next Question" click |
| POST | `/partials/feedback` | Answer form submission |
| GET | `/partials/history-table` | Filter change |

### AI Evaluation Strategy

**Framework-to-Category Mapping:**

| Category | Frameworks | Evaluation Focus |
|----------|-----------|-----------------|
| Product Design | CIRCLES, Design Thinking | User empathy, structured decomposition, creative solutions |
| Strategy | Porter's, SWOT, Ansoff | Market analysis, competitive positioning, strategic clarity |
| Execution | RICE, MoSCoW | Prioritization rigor, trade-off reasoning |
| Analytical | Hypothesis-driven, Fermi | Structured breakdown, assumptions, math |
| Project Management | Agile, RACI | Timeline realism, risk ID, dependencies |
| App Critique | HEART, UX Heuristics | Systematic evaluation, actionable recommendations |
| Cross-Functional | STAR, Stakeholder Mapping | Concrete examples, conflict resolution |

**Prompt structure:** System prompt sets evaluator persona + category context. User message contains question + answer. Response is structured JSON with scores and feedback.

### Application Structure

```
pm-interview-coach/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/ (question.py, attempt.py, session.py)
│   ├── routers/ (pages.py, questions.py, practice.py, stats.py)
│   ├── services/ (evaluator.py, question_loader.py, stats_engine.py)
│   ├── templates/ (base, index, practice, history, progress + partials/)
│   └── static/
├── data/ (munna_kaka/ docs + pm_questions.xlsx)
├── scripts/ (load_questions.py)
├── tests/
├── requirements.txt
└── README.md
```

---

## UI/UX

### Landing Page (`/`)
- Hero: "PM Interview Coach" + one-liner
- 7 category cards in a grid, each showing: icon, name, question count, avg score (progress ring)
- "Surprise Me" FAB button (weighted random)
- Nav: Home | History | Progress

### Practice Page (`/practice/{category}`)
- Single-column, centered (max 768px)
- Question card (text + category badge + difficulty pill + hint toggle)
- Optional timer bar (green → yellow → red)
- Answer textarea (min 6 rows, auto-expand, 50-char minimum to submit)
- Submit button → loading spinner → HTMX swaps in feedback section:
  - Large overall score (color-coded)
  - Radar chart (3 sub-scores)
  - Strengths (green bullets) + Improvements (orange bullets)
  - Suggested framework callout + example point box
  - "Try Again" and "Next Question" buttons

### History (`/history`)
- Filterable table: category, difficulty, date range, score range
- Columns: Date, Category, Question (truncated), Score, Time Spent
- Click → slide-over detail panel with full Q&A and evaluation

### Progress Dashboard (`/progress`)
- Summary cards: Total Practiced, Avg Score, Practice Streak, Weakest Category
- Score trend line chart (per category, toggleable)
- Category performance horizontal bar chart (sorted worst→best)
- Practice heatmap (GitHub-style contribution grid)

---

## Development Phases

### Phase 1: Foundation (Days 1-3)
- [ ] Project scaffold (FastAPI, SQLite, SQLAlchemy)
- [ ] Build question ingestion script (parse Munna Kaka docs + XLSX → DB)
- [ ] Base template (Tailwind + HTMX)
- [ ] Landing page with category cards
- [ ] Seed DB and verify category counts

### Phase 2: Core Practice Loop (Days 4-6)
- [ ] Question browsing + random selection API
- [ ] Practice page with question display, timer, answer textarea
- [ ] Claude API integration (evaluator service with category-aware prompts)
- [ ] Submit endpoint → AI evaluation → structured JSON parsing
- [ ] Feedback partial (scores, radar chart, strengths/improvements)
- [ ] HTMX wiring: submit → feedback swap, Next Question, Try Again

### Phase 3: History & Progress (Days 7-9)
- [ ] Practice history page with filterable table
- [ ] Stats aggregation queries (by category, over time, weakest)
- [ ] Progress dashboard with Chart.js visualizations
- [ ] Session tracking (browser cookie)
- [ ] Weighted random question selection

### Phase 4: Polish & Deploy (Days 10-12)
- [ ] Responsive design pass
- [ ] Loading states, error handling, empty states
- [ ] Tests (evaluator, question loader, API)
- [ ] Deploy + add to portfolio site

---

## Next Step

Build `scripts/load_questions.py` first — parse each Munna Kaka document to extract individual questions, categorize them, assign difficulty, and map frameworks. This is the critical path; everything else depends on having questions in the database.

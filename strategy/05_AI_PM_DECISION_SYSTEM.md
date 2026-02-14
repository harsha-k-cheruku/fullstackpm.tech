# Project 4: AI PM Decision System

## Product Brief

### Problem
Feature prioritization is one of the highest-stakes decisions a PM makes, yet most PMs rely on gut instinct plus ad-hoc spreadsheets. There's no consistent, multi-framework evaluation process. At Amazon, a misjudged priority on a high-traffic surface could cost millions in opportunity cost. At Walmart, shipping the wrong capability to stores meant wasted deployment across 4,700+ locations.

### Solution
An AI-powered decision support system that evaluates feature proposals against 5 established PM frameworks simultaneously: RICE, Effort/Impact Matrix, Strategic Alignment, Opportunity Cost, and Market Timing. Produces a structured **Build / Don't Build / Needs More Data** recommendation with transparent scoring, reasoning, and comparison capabilities.

### Target Audience
- Interviewers evaluating your product sense and prioritization rigor
- PMs making feature decisions who want a structured second opinion
- PM leaders who want to bring consistency to prioritization discussions

### Non-Goals
- Not an autonomous decision-maker (the PM decides, the system advises)
- Not a replacement for customer research or usability testing
- Not a roadmap sequencing tool
- No Jira/Linear integration (v1)

---

## Features

### MVP

| Feature | Description |
|---------|-------------|
| **Feature Input Form** | Structured input: description, target user segment, market context, strategic goals, effort estimate, resource constraints, competitive landscape |
| **5-Framework Evaluation** | AI evaluates against RICE, Effort/Impact, Strategic Alignment, Opportunity Cost, Market Timing — all in parallel |
| **Verdict** | Build / Don't Build / Needs More Data with confidence level (High/Medium/Low) |
| **Scoring Breakdown** | Visual scores per framework with explanations |
| **Reasoning** | Full narrative: key factors, risks, what would change the verdict |
| **Evaluation History** | Save and browse past evaluations |
| **Side-by-Side Comparison** | Compare 2-3 feature evaluations in a table |
| **Export** | Markdown, JSON, PDF |

### v2
- Custom framework weights (startup vs. enterprise context)
- Historical calibration (track outcomes of built features)
- Batch evaluation (paste a feature list, get ranked stack)
- Sensitivity analysis (how does verdict change if assumptions shift)

---

## Evaluation Frameworks

### 1. RICE Scoring
- **Reach:** Users impacted per quarter
- **Impact:** 0.25x (Minimal) to 3x (Massive)
- **Confidence:** 0-100% based on input data quality
- **Effort:** Person-weeks
- **Score:** (Reach x Impact x Confidence) / Effort

### 2. Effort/Impact Matrix
Positions feature on a 2x2: Quick Wins | Big Bets | Fill-Ins | Money Pits

### 3. Strategic Alignment
-10 (Contradictory) to +10 (Direct Alignment) against stated goals

### 4. Opportunity Cost
Evaluates: alternative features those resources could deliver, cost of delay for other roadmap items, time-sensitivity

### 5. Market Timing
Scores based on: competitor moves, first-mover opportunity, market maturity, regulatory forces

### Synthesis
AI weighs all 5, identifies convergence/divergence, produces verdict + confidence + key factors + risks + "what would change this."

---

## Technical Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | HTMX + Tailwind CSS |
| AI | Claude API |
| Database | SQLite |
| Export | Markdown + WeasyPrint (PDF) |

### Prompt Architecture: Fan-Out / Fan-In

1. **Fan-Out:** Feature input sent to 5 parallel Claude API calls (one per framework) via `asyncio.gather()`. Each has a specialized system prompt.
2. **Fan-In:** All 5 results aggregated into a single synthesis prompt that produces the final verdict.

Benefits: parallelism, specialization, transparency, debuggability.

### Data Model

```sql
evaluations (
  id TEXT PK,
  title TEXT NOT NULL,
  feature_description TEXT NOT NULL,
  target_user_segment TEXT,
  market_context TEXT,
  strategic_goals TEXT,            -- JSON array
  resource_constraints TEXT,       -- JSON: {team_size, timeline_weeks, budget}
  competitive_landscape TEXT,
  verdict TEXT,                    -- "BUILD", "DONT_BUILD", "NEEDS_MORE_DATA"
  verdict_confidence TEXT,         -- "HIGH", "MEDIUM", "LOW"
  overall_score REAL,              -- 0-100
  key_factors TEXT,                -- JSON array
  risks TEXT,                      -- JSON array
  what_would_change TEXT,          -- JSON array
  full_reasoning TEXT,
  raw_ai_response TEXT,
  tokens_used INTEGER,
  created_at DATETIME
)

framework_scores (
  id TEXT PK,
  evaluation_id TEXT FK,
  framework TEXT,                  -- "RICE", "EFFORT_IMPACT", etc.
  score REAL,                      -- 0-100 normalized
  raw_score TEXT,                  -- JSON (framework-specific sub-scores)
  explanation TEXT,
  created_at DATETIME
)

comparison_sets (
  id TEXT PK,
  name TEXT,
  evaluation_ids TEXT,             -- JSON array
  created_at DATETIME
)
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Landing with recent evaluations |
| GET | `/evaluate` | New evaluation form |
| POST | `/api/evaluate` | Submit → 5 parallel AI evals → synthesis → result |
| GET | `/evaluations/{id}` | Detail view |
| GET | `/compare` | Comparison selection |
| GET | `/compare?ids=a,b,c` | Side-by-side view |
| GET | `/history` | All evaluations with filters |
| GET | `/api/evaluations/{id}/export/{format}` | Export (md/json/pdf) |

---

## UI/UX

### Evaluation Form (`/evaluate`)
- Multi-section form: Feature Details, Market Context, Strategic Context, Constraints
- Strategic goals as dynamic add/remove list (HTMX)
- Submit → loading state ("Evaluating across 5 frameworks...") → result slides in

### Detail View (`/evaluations/{id}`)
- **Left column (60%):** Verdict badge + confidence, key factors, risks, what would change, full reasoning (expandable)
- **Right column (40%):** 5 framework score cards, each with progress bar + explanation (expandable for sub-scores)
- Actions: Re-evaluate, Export, Delete

### Comparison (`/compare`)
- Select 2-3 evaluations via checkboxes → "Compare Selected"
- Table: rows = Verdict, Confidence, Overall Score, each framework score, key factors, top risk
- Highest/lowest scores highlighted per row

### History (`/history`)
- Filterable by verdict, date, score range, tags
- Live search with HTMX debounce

---

## Development Phases

### Phase 1: Foundation (Days 1-3)
- [ ] Project scaffold + database schema
- [ ] Input form page
- [ ] Claude API client with retry logic
- [ ] RICE evaluation prompt + parser (start with one framework)

### Phase 2: All Frameworks + Synthesis (Days 4-8)
- [ ] Remaining 4 framework prompts + parsers
- [ ] Parallel execution via asyncio.gather()
- [ ] Synthesis prompt + verdict generation
- [ ] Structured output validation with retry
- [ ] Store results in database

### Phase 3: Results UI (Days 9-13)
- [ ] Detail page with verdict + framework cards
- [ ] Expandable framework details via HTMX
- [ ] Landing page with recent evaluations
- [ ] Loading/progress state during evaluation

### Phase 4: Compare, History, Export (Days 14-18)
- [ ] Comparison selection + table
- [ ] History page with filters
- [ ] Export (Markdown, JSON, PDF)
- [ ] Responsive design, tests, deploy

---

## Next Step

Build the RICE evaluation prompt first and test the full loop: form input → single API call → parsed result → rendered on page. Once RICE works end-to-end, expand to all 5 frameworks and synthesis.

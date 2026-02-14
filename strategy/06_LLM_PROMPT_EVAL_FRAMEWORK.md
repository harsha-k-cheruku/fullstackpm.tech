# Project 5: LLM Prompt Evaluation Framework

## Product Brief

### Problem
Most teams building with LLMs evaluate prompts by vibes: "does this output look good?" This leads to prompt regressions, inconsistent quality, and no ability to compare prompt versions systematically. For an AI PM, the ability to rigorously evaluate and iterate on prompts is a core skill — and one that almost nobody demonstrates publicly.

### Solution
A structured system for managing, evaluating, and comparing LLM prompt quality. Define test cases, create evaluation rubrics, run prompts against test suites, score outputs across multiple dimensions, and compare prompt versions side-by-side. Think of it as unit testing for prompts.

### Target Audience
- Interviewers evaluating your AI product rigor (this is the most differentiating project)
- AI/ML teams building LLM-powered features
- PMs who need to QA prompt-based features

### Non-Goals
- Not a prompt library/marketplace
- Not a fine-tuning tool
- Not a general LLM playground
- No multi-user collaboration (v1)

---

## Features

### MVP

| Feature | Description |
|---------|-------------|
| **Prompt Manager** | Create, version, and organize prompts with system/user message templates and variable slots |
| **Test Case Manager** | Define test cases: input variables, expected output characteristics, edge cases |
| **Evaluation Rubrics** | Define scoring criteria: accuracy, relevance, format compliance, completeness, safety, tone |
| **Run Evaluations** | Execute a prompt against a test suite → AI judge scores each output against rubric |
| **Scoring Dashboard** | Aggregate scores across test cases with pass/fail thresholds |
| **Version Comparison** | Side-by-side: Prompt v1 vs v2 outputs and scores for the same test cases |
| **Regression Detection** | Flag when a new prompt version scores lower on any dimension |
| **Cost Tracking** | Token usage and estimated cost per evaluation run |

### v2
- A/B-style evaluation (which output does a human judge prefer?)
- Multi-model comparison (same prompt on Claude vs GPT vs Gemini)
- Automated prompt optimization suggestions
- CI/CD integration (run eval suite on prompt changes)
- Shared rubric templates

---

## Evaluation Methodology

### Scoring Dimensions (Default Rubric)

| Dimension | Description | Scale |
|-----------|-------------|-------|
| **Accuracy** | Is the output factually correct and relevant to the input? | 1-5 |
| **Completeness** | Does the output cover all expected aspects? | 1-5 |
| **Format Compliance** | Does the output follow the specified structure/format? | 1-5 |
| **Relevance** | Is every part of the output relevant (no filler/hallucination)? | 1-5 |
| **Tone** | Does the output match the desired voice/tone? | 1-5 |
| **Safety** | Is the output free of harmful, biased, or inappropriate content? | Pass/Fail |

### Evaluation Approach: LLM-as-Judge

An evaluator prompt instructs Claude to act as a quality assessor:
- Input: the original prompt, the test case inputs, the generated output, and the rubric
- Output: structured JSON with per-dimension scores and reasoning
- The evaluator prompt is itself versioned and testable (meta-evaluation)

### Aggregate Metrics

| Metric | Calculation |
|--------|------------|
| **Overall Score** | Weighted average across dimensions |
| **Pass Rate** | % of test cases scoring above threshold on all dimensions |
| **Dimension Breakdown** | Average score per dimension across all test cases |
| **Regression Count** | # of test cases where new version scores lower than previous |
| **Cost per Run** | Total tokens x price per token |

---

## Technical Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | HTMX + Tailwind CSS |
| AI (generation) | Claude API + OpenAI API (for multi-model comparison in v2) |
| AI (evaluation) | Claude API (LLM-as-judge) |
| Database | SQLite |
| Charts | Chart.js |

### Data Model

```sql
prompts (
  id TEXT PK,
  name TEXT NOT NULL,
  description TEXT,
  system_message TEXT,
  user_message_template TEXT,     -- Contains {{variable}} slots
  variables TEXT,                  -- JSON array of variable names
  version INTEGER DEFAULT 1,
  parent_id TEXT FK,               -- Previous version of this prompt
  created_at DATETIME
)

test_cases (
  id TEXT PK,
  prompt_id TEXT FK,
  name TEXT NOT NULL,
  description TEXT,
  input_variables TEXT NOT NULL,   -- JSON: {"variable_name": "value"}
  expected_characteristics TEXT,   -- JSON: what good output looks like
  tags TEXT,                       -- JSON array: ["edge_case", "happy_path"]
  created_at DATETIME
)

rubrics (
  id TEXT PK,
  name TEXT NOT NULL,
  dimensions TEXT NOT NULL,        -- JSON array of {name, description, scale, weight}
  pass_threshold REAL DEFAULT 3.5,
  created_at DATETIME
)

evaluation_runs (
  id TEXT PK,
  prompt_id TEXT FK,
  rubric_id TEXT FK,
  status TEXT,                     -- "running", "completed", "failed"
  model_used TEXT,
  total_test_cases INTEGER,
  passed INTEGER,
  failed INTEGER,
  overall_score REAL,
  total_tokens INTEGER,
  estimated_cost REAL,
  started_at DATETIME,
  completed_at DATETIME
)

evaluation_results (
  id TEXT PK,
  run_id TEXT FK,
  test_case_id TEXT FK,
  generated_output TEXT,
  dimension_scores TEXT,           -- JSON: {dimension: {score, reasoning}}
  overall_score REAL,
  passed BOOLEAN,
  generation_tokens INTEGER,
  evaluation_tokens INTEGER,
  created_at DATETIME
)
```

### API Endpoints

**Pages:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Dashboard: prompts overview, recent runs |
| GET | `/prompts` | Prompt manager |
| GET | `/prompts/{id}` | Prompt detail with versions and test cases |
| GET | `/prompts/{id}/test-cases` | Test case manager |
| GET | `/rubrics` | Rubric manager |
| GET | `/runs/{id}` | Evaluation run results |
| GET | `/compare` | Version comparison selector |

**API:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/prompts` | Create prompt |
| PUT | `/api/prompts/{id}` | Update (creates new version) |
| POST | `/api/test-cases` | Create test case |
| POST | `/api/rubrics` | Create rubric |
| POST | `/api/evaluate` | Run evaluation: prompt + test suite + rubric |
| GET | `/api/runs/{id}/results` | Get evaluation results |
| GET | `/api/compare/{v1_run_id}/{v2_run_id}` | Compare two runs |

---

## UI/UX

### Dashboard (`/`)
- Prompt cards showing: name, latest version, last run score, test case count
- Recent evaluation runs with pass/fail badges
- Quick action: "New Prompt" and "Run Evaluation"

### Prompt Detail (`/prompts/{id}`)
- Version history sidebar (v1, v2, v3... click to view)
- System message and user template displayed with syntax highlighting
- Variable slots highlighted
- Test cases table below
- "Run Evaluation" button → select rubric → execute

### Evaluation Run Results (`/runs/{id}`)
- Summary: Overall score, pass rate, cost, duration
- Dimension breakdown bar chart
- Per-test-case table: test name, score, pass/fail, expand for full output + reasoning
- Regression warnings highlighted in red

### Version Comparison (`/compare`)
- Select two evaluation runs (same prompt, different versions)
- Side-by-side: for each test case, show v1 output vs v2 output with scores
- Delta column: score change per dimension
- Summary: "v2 improved accuracy by +0.3 but regressed on format compliance by -0.2"

---

## Development Phases

### Phase 1: Foundation (Days 1-3)
- [ ] Project scaffold + database schema
- [ ] Prompt CRUD (create, view, version)
- [ ] Test case CRUD
- [ ] Rubric CRUD with default rubric

### Phase 2: Evaluation Engine (Days 4-7)
- [ ] Prompt execution (fill template variables → call Claude → capture output)
- [ ] LLM-as-judge evaluator (score output against rubric)
- [ ] Evaluation run orchestration (iterate test cases, aggregate scores)
- [ ] Store results in database
- [ ] Results page with per-test-case breakdown

### Phase 3: Comparison & Analysis (Days 8-10)
- [ ] Version comparison engine
- [ ] Side-by-side UI
- [ ] Regression detection logic
- [ ] Cost tracking and display
- [ ] Dashboard with prompt overview and recent runs

### Phase 4: Polish & Deploy (Days 11-14)
- [ ] Chart.js visualizations (dimension breakdown, score trends)
- [ ] Responsive design
- [ ] Seed with 2-3 example prompts + test suites for demo
- [ ] Tests and deploy
- [ ] Add to portfolio site

---

## Next Step

Build the evaluation engine first: take one hardcoded prompt + 3 test cases + one rubric, run the full evaluation pipeline (generate → judge → score → aggregate), and print results. Validate that the LLM-as-judge scoring is consistent and useful before building the web UI.

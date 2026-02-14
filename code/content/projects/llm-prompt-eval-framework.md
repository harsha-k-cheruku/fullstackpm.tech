---
title: "LLM Prompt Evaluation Framework"
description: "Structured system for managing, evaluating, and comparing LLM prompt quality with rigorous testing."
tech_stack: [FastAPI, Claude API, HTMX, SQLite, Chart.js]
status: "planned"
featured: false
display_order: 6
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/llm-prompt-eval-framework"
problem: "Teams building with LLMs evaluate prompts by vibes: 'does this output look good?' This leads to prompt regressions, inconsistent quality, and no ability to compare prompt versions systematically. Most teams lack a rigorous framework for evaluating LLM quality."
approach: "Build a structured system that treats prompts like code. Define test cases, create evaluation rubrics, run prompts against test suites, score outputs across multiple dimensions, and compare versions side-by-side. Think of it as unit testing for prompts."
solution: "An interactive tool where you create prompts, define test cases and scoring rubrics, run evaluations with an LLM-as-judge, and compare prompt versions. Provides pass/fail metrics, regression detection, and cost tracking per evaluation run."
---

## What

A rigorous testing framework for LLM prompts. Instead of evaluating outputs subjectively, define what good looks like (rubric), test it systematically (test suite), and compare versions objectively (side-by-side analysis).

**Input:** A prompt (with template variables), test cases, and evaluation rubric

**Output:** Structured evaluation results including:
- **Test Score:** Pass/fail per test case (composite score across dimensions)
- **Dimension Breakdown** — Accuracy, Completeness, Format Compliance, Relevance, Tone, Safety (each 1-5 scale)
- **Regression Detection** — Flag when new version scores lower on any dimension
- **Cost Tracking** — Token usage and estimated cost per evaluation run
- **Version Comparison** — Side-by-side view of v1 vs v2 outputs and scores for same test cases
- **Scoring Methodology** — LLM-as-judge approach with versioned evaluator prompts

## Why

**The Problem:**
Most teams using Claude/ChatGPT/Gemini have no systematic way to validate prompt quality. They rely on ad-hoc testing, anecdotal feedback ("this output looks good"), and manual spot-checking. When they iterate on prompts, they don't know if they're improving or introducing regressions.

**Why This Tool Matters:**
- **Rigor:** Move from gut-feel evaluation to structured scoring across multiple dimensions
- **Regression Detection:** Know immediately when a prompt change makes things worse
- **Cost Visibility:** Understand token usage per evaluation run and optimize accordingly
- **Iteration Confidence:** Change prompts knowing you can measure impact
- **Interview Differentiator:** Shows you understand both LLM evaluation methodology AND testing best practices

**Who Needs This:**
- AI/ML teams validating prompt-based features
- PMs building LLM-powered products (Interview Coach, Marketplace Analytics, etc.)
- You, demonstrating rigorous evaluation thinking (most differentiating project for interviewers)

## How

**Architecture:**

```
Create Prompt (system message + user template with {{variables}})
    ↓
Define Test Cases (input values, expected characteristics, edge cases)
    ↓
Define Rubric (scoring dimensions, scale, weights)
    ↓
Run Evaluation:
    For each test case:
      - Fill prompt template with test inputs
      - Call Claude API
      - LLM-as-Judge scores output against rubric
      - Store results
    ↓
Aggregate Results (overall score, pass rate, dimension breakdown)
    ↓
Compare Versions (v1 vs v2 side-by-side)
    ↓
Detect Regressions (flag score drops)
```

**Key Features:**

1. **Prompt Manager**
   - Create, version, and organize prompts
   - System message + user template with {{variable}} slots
   - Version history (v1, v2, v3...)

2. **Test Case Builder**
   - Define inputs (JSON object: {"variable_name": "value"})
   - Describe expected characteristics ("should be under 100 words", "must include a recommendation", etc.)
   - Tag for categorization (happy_path, edge_case, etc.)

3. **Evaluation Rubrics**
   - Default rubric: Accuracy (1-5), Completeness (1-5), Format Compliance (1-5), Relevance (1-5), Tone (1-5), Safety (Pass/Fail)
   - Configurable rubrics with custom dimensions
   - Weighted scoring

4. **Evaluation Engine**
   - LLM-as-judge approach: Claude evaluates outputs against rubric
   - Structured JSON scoring (dimension scores + reasoning)
   - Per-test-case storage with full output + feedback

5. **Version Comparison**
   - Select two evaluation runs (same prompt, different versions)
   - Side-by-side: v1 output vs v2 output with scores
   - Delta column showing score changes per dimension
   - Summary: "v2 improved accuracy by +0.3 but regressed on format compliance by -0.2"

6. **Regression Detection**
   - Automatic flagging when new version scores lower
   - Breakdown by dimension (which dimensions regressed?)
   - Historical trend view

7. **Cost Tracking**
   - Token count per evaluation run
   - Estimated cost (based on Claude pricing)
   - Cost per test case

**Build Path:**

- **Phase 1 (Days 1-3):** Foundation
  - Scaffold + database schema
  - Prompt CRUD (create, view, version)
  - Test case CRUD
  - Rubric CRUD with default rubric

- **Phase 2 (Days 4-7):** Evaluation Engine
  - Prompt execution (fill template → call Claude)
  - LLM-as-judge evaluator (score against rubric)
  - Evaluation run orchestration
  - Store results, display per-test-case breakdown

- **Phase 3 (Days 8-10):** Comparison & Analysis
  - Version comparison engine
  - Side-by-side UI
  - Regression detection logic
  - Cost tracking display

- **Phase 4 (Days 11-14):** Polish & Deploy
  - Chart.js visualizations (dimension scores, score trends)
  - Dashboard with prompt overview and recent runs
  - Responsive design
  - Seed with 2-3 example prompts + test suites for demo
  - Deploy to portfolio

## Technical Stack

- **Backend:** FastAPI (async, structured request/response)
- **AI (Generation):** Claude API (gpt-4 for prompt execution)
- **AI (Evaluation):** Claude API (LLM-as-judge for scoring)
- **Frontend:** HTMX + Tailwind CSS
- **Storage:** SQLite
- **Charts:** Chart.js (dimension breakdown, score trends, version comparison)
- **Syntax Highlighting:** Prism.js for prompt/output display

---

## Why Build This Project

1. **Demonstrates Evaluation Rigor** — You don't just use LLMs; you test and measure them systematically.

2. **Shows Deep AI/LLM Understanding** — The LLM-as-judge pattern, evaluation methodology, and prompt versioning show technical depth beyond "ChatGPT is cool."

3. **Directly Applicable** — You can use this tool to evaluate prompts in your Interview Coach and other LLM-powered features. Real utility = good portfolio signal.

4. **Interview Differentiator** — This is the most differentiating project because few people build systematic evaluation frameworks. Shows you think about quality rigorously.

5. **Transferable Skills** — The testing and versioning patterns map to code testing workflows, showing PM + engineering thinking.

---

## Next Steps

See `strategy/06_LLM_PROMPT_EVAL_FRAMEWORK.md` for detailed specification including data model, API endpoints, UI/UX design, and phase breakdown.

**Expected Timeline:** 2 weeks for MVP
**Complexity:** Medium-High (evaluation engine + LLM-as-judge logic)
**Impact:** High (immediately useful + interview differentiator)

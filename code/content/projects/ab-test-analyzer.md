---
title: "A/B Test Analyzer & Sample Size Calculator"
description: "Statistical analysis tool for A/B testing with Frequentist and Bayesian approaches, power analysis, and sample size calculator."
tech_stack: [FastAPI, SciPy, NumPy, HTMX, SQLite, Chart.js]
status: "planned"
featured: false
display_order: 7
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/ab-test-analyzer"
problem: "Every PM talks about A/B testing. Few understand the statistics behind it. Most rely on whatever their experimentation platform says, accepting results without understanding p-values, confidence intervals, or power analysis. This represents a gap in analytical rigor."
approach: "Build a web-based tool with two modes: Pre-Test (sample size calculator + power analysis) and Post-Test (statistical significance analysis). Support both Frequentist and Bayesian approaches with visualizations and plain-English recommendations."
solution: "An interactive statistical calculator that helps you plan experiments (how many users needed?) and analyze results (is this significant?). Includes power curves, distribution visualizations, lift confidence intervals, and a recommendation engine (Ship It / Keep Testing / Kill It)."
---

## What

A statistical analysis tool for A/B testing. Instead of guessing whether results are significant, use rigorous statistical methods to decide.

**Pre-Test Mode:**
- Input: baseline conversion rate, minimum detectable effect (MDE), significance level, power, daily traffic
- Output: required sample size per variant, estimated test duration, power curve visualization

**Post-Test Mode:**
- Input: control results (visitors + conversions), variant results (visitors + conversions)
- Output: p-value, observed lift, confidence interval, effect size, achieved power, recommendation (Ship It / Keep Testing / Kill It)

**Two Methodologies:**
- **Frequentist:** Z-tests, p-values, confidence intervals (traditional hypothesis testing)
- **Bayesian:** Beta posteriors, P(variant > control), expected loss, credible intervals

## Why

**The Problem:**
Most PMs don't understand the math behind A/B testing. They don't know:
- How many users they need to detect a given effect size
- Whether their results are actually significant or just noise
- The difference between frequentist p-values and Bayesian probabilities
- Why early stopping leads to inflated false positive rates

This leads to:
- Underpowered tests (not enough users)
- Misinterpreted results ("60% conversion is better than 55%, ship it!")
- Overconfidence in marginal effects
- Wasted test time on trivial improvements

**Why This Tool Matters:**
- **Analytical Rigor:** Show you understand statistics, not just "bigger number wins"
- **Decision Confidence:** Move from gut-feel to evidence-based recommendations
- **Cost Awareness:** Understand sample size → duration → cost trade-offs
- **Teaching Tool:** Helps teams learn statistical thinking
- **Interview Differentiator:** Direct connection to your Verizon experimentation background

**Who Needs This:**
- Product teams running A/B tests (Marketplace Analytics could use this)
- PMs evaluating feature performance
- You, demonstrating analytical depth matched to your Verizon experience

## How

**Architecture:**

```
Pre-Test Path:
  Input (baseline rate, MDE, alpha, power, traffic)
    ↓
  Sample Size Calculator (formula: (Z_alpha/2 + Z_beta)^2 * ...)
    ↓
  Power Curve Generation (power vs sample size across MDE values)
    ↓
  Duration Estimate (sample size / daily traffic)
    ↓
  Visualization (bar chart, sensitivity table)

Post-Test Path:
  Input (control visitors/conversions, variant visitors/conversions)
    ↓
  Statistical Test (two-proportion z-test)
    ↓
  Compute Metrics (p-value, lift, CI, effect size, achieved power)
    ↓
  Decision Logic (recommendation engine)
    ↓
  Visualizations (distribution chart, lift chart with CI)
    ↓
  Optional: Bayesian Analysis (Beta posteriors, credible intervals)
```

**Key Features:**

1. **Sample Size Calculator**
   - Baseline conversion rate (with slider 0-100%)
   - Minimum detectable effect (with slider)
   - Significance level (dropdown: 0.01, 0.05, 0.10)
   - Statistical power (dropdown: 0.80, 0.90, 0.95)
   - Daily traffic input
   - Returns: required sample size, estimated test duration (days), sample per variant

2. **Frequentist Post-Test Analyzer**
   - Two-proportion z-test
   - Outputs:
     - p-value (two-tailed)
     - z-statistic
     - Observed lift (%)
     - 95% confidence interval (Wilson score interval)
     - Effect size (Cohen's h)
     - Achieved statistical power

3. **Bayesian Post-Test Analyzer**
   - Beta posterior for each variant (control and variant)
   - Outputs:
     - P(variant > control) — probability that variant is better
     - Expected loss — risk of choosing wrong variant
     - Credible interval (95%)
     - Expected lift distribution

4. **Recommendation Engine**
   - **Ship It:** p < 0.05 AND positive lift (or P(variant > control) > 0.95 in Bayesian)
   - **Keep Testing:** inconclusive (p > 0.05 but not definitive negative, or P(variant > control) 0.25-0.75)
   - **Kill It:** p < 0.05 AND negative lift (or P(control > variant) > 0.95 in Bayesian)
   - Includes reasoning paragraph explaining the recommendation

5. **Visualizations**
   - Distribution chart: control vs variant bell curves overlaid with overlap shaded
   - Lift chart: point estimate with confidence interval whiskers
   - Power curve: power (y-axis) vs sample size (x-axis) for current MDE
   - Sensitivity table: required sample size for different MDE values

6. **Test History**
   - Save analyses to SQLite
   - Browse past tests
   - Compare results across time (did we run enough tests? did we ship winners?)

7. **Mode Toggle**
   - Switch between Frequentist and Bayesian at top of page
   - Both calculators respect the toggle

**Build Path:**

- **Phase 1 (Days 1-3):** Statistical Engine
  - Implement frequentist sample size calculator (SciPy)
  - Implement frequentist post-test analyzer
  - Implement Bayesian posterior calculation
  - Implement recommendation logic
  - Write validation tests (compare against known textbook results)

- **Phase 2 (Days 4-7):** Web UI
  - FastAPI scaffold + templates
  - Pre-test calculator page with HTMX
  - Post-test analyzer page with HTMX
  - Chart.js visualizations
  - Mode toggle

- **Phase 3 (Days 8-10):** History & Polish
  - SQLite storage
  - History page
  - Result detail page
  - Responsive design
  - Deploy

## Technical Stack

- **Backend:** FastAPI (async for smooth calculations)
- **Math:** SciPy (z-tests, power analysis), NumPy (array operations)
- **Frontend:** HTMX + Tailwind CSS
- **Storage:** SQLite
- **Charts:** Chart.js (distributions, power curves, confidence intervals)
- **Testing:** pytest + scipy.stats for validation against known results

---

## Why Build This Project

1. **Demonstrates Statistical Literacy** — Most PMs don't understand the math. You do.

2. **Direct Verizon Connection** — You ran massive experimentation programs at Verizon. This tool validates that expertise with runnable code.

3. **Immediately Useful** — You can use this to analyze Marketplace Analytics experiments or other A/B tests.

4. **Interview Differentiator** — Combines product thinking (recommendations, UX) with analytical depth (frequentist/Bayesian).

5. **Teaching Value** — Other PMs will use this to learn statistics. Shows you care about knowledge transfer.

---

## Next Steps

See `strategy/07_AB_TEST_ANALYZER.md` for detailed specification including statistical methodology, data models, API endpoints, and comprehensive development phases.

**Expected Timeline:** 2 weeks for MVP
**Complexity:** Medium (statistical engine + web UI)
**Impact:** High (immediately useful + interview signal)

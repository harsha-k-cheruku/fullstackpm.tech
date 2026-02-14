# Project 6: A/B Test Analyzer & Sample Size Calculator

## Product Brief

### Problem
Every PM talks about A/B testing. Few understand the statistics behind it. Most rely on whatever their experimentation platform tells them, accepting results without understanding p-values, confidence intervals, or power analysis. This project proves you understand the math — and built a tool for it.

### Solution
A web-based A/B test analysis tool with two modes: **Pre-Test** (sample size calculator + power analysis) and **Post-Test** (statistical significance analysis + recommendation). Supports both Frequentist and Bayesian approaches. Includes visualizations of distributions, lift, and confidence intervals, plus a historical test log.

### Target Audience
- Interviewers evaluating your analytical rigor
- PMs running A/B tests who want a second opinion or a teaching tool
- You, demonstrating deep analytical skills (directly maps to Verizon experimentation background)

### Non-Goals
- Not a replacement for Optimizely/LaunchDarkly/Statsig
- No integration with experimentation platforms
- No multi-variate testing (v1 — two variants only)
- No sequential testing / early stopping rules (v1)

---

## Statistical Methodology

### Frequentist Mode

**Pre-Test (Sample Size):**
- Inputs: baseline conversion rate (p1), minimum detectable effect (MDE), significance level (alpha, default 0.05), statistical power (1-beta, default 0.80)
- Formula: `n = (Z_alpha/2 + Z_beta)^2 * (p1(1-p1) + p2(1-p2)) / (p1-p2)^2`
- Outputs: required sample size per variant, estimated test duration (given daily traffic input)

**Post-Test (Significance):**
- Inputs: control visitors, control conversions, variant visitors, variant conversions
- Tests: two-proportion z-test
- Outputs: p-value, z-statistic, observed lift (%), absolute difference, 95% confidence interval for the difference, effect size (Cohen's h), statistical power achieved
- Recommendation: "Ship It" (p < alpha, positive lift) / "Keep Testing" (inconclusive) / "Kill It" (p < alpha, negative lift OR no practical significance)

### Bayesian Mode

**Pre-Test:**
- Prior: Beta(1,1) uniform or user-specified Beta(alpha, beta)
- Simulation: Monte Carlo with configurable samples (default 100,000)
- Outputs: probability that variant beats control, expected loss, credible interval

**Post-Test:**
- Posterior: Beta(alpha + conversions, beta + non-conversions) for each variant
- Outputs: P(variant > control), expected lift distribution, 95% credible interval, expected loss (risk of choosing wrong variant), recommended decision threshold

### Key Formulas Implemented

| Concept | Implementation |
|---------|---------------|
| Z-test | `scipy.stats.norm` |
| P-value | Two-tailed from z-statistic |
| Confidence Interval | Wilson score interval for proportions |
| Effect Size | Cohen's h: `2 * arcsin(sqrt(p))` |
| Power Analysis | `scipy.stats.norm.ppf` |
| Bayesian Posterior | `scipy.stats.beta` |
| Monte Carlo | `numpy.random.beta` sampling |

---

## Features

### MVP

| Feature | Description |
|---------|-------------|
| **Pre-Test Calculator** | Input baseline rate + MDE → sample size, duration estimate, power curve |
| **Post-Test Analyzer** | Input results → significance, lift, CI, recommendation |
| **Frequentist Mode** | Z-test based analysis with p-values and confidence intervals |
| **Bayesian Mode** | Beta-posterior analysis with probability of winning and expected loss |
| **Distribution Visualization** | Chart showing control vs variant distributions with overlap |
| **Lift Visualization** | Chart showing observed lift with confidence/credible interval |
| **Power Curve** | Chart showing power vs sample size for different MDE values |
| **Plain-English Recommendation** | "Ship It" / "Keep Testing" / "Kill It" with reasoning |
| **Test History** | Save and browse past analyses |

### v2
- Multiple metrics per test (primary + guardrail metrics)
- Revenue/continuous metric support (not just conversion rates)
- Sequential analysis with early stopping boundaries
- Segment breakdown (analyze by user segment)
- Shareable result links

---

## Technical Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | HTMX + Tailwind CSS |
| Math | SciPy + NumPy |
| Charts | Chart.js (distributions, power curves, CI plots) |
| Database | SQLite |

### Data Model

```sql
tests (
  id TEXT PK,
  name TEXT NOT NULL,
  description TEXT,
  mode TEXT NOT NULL,              -- "pre_test" or "post_test"
  method TEXT NOT NULL,            -- "frequentist" or "bayesian"

  -- Pre-test inputs
  baseline_rate REAL,
  mde REAL,
  alpha REAL DEFAULT 0.05,
  power REAL DEFAULT 0.80,
  daily_traffic INTEGER,

  -- Post-test inputs
  control_visitors INTEGER,
  control_conversions INTEGER,
  variant_visitors INTEGER,
  variant_conversions INTEGER,

  -- Results
  required_sample_size INTEGER,
  estimated_duration_days INTEGER,
  p_value REAL,
  z_statistic REAL,
  observed_lift REAL,
  ci_lower REAL,
  ci_upper REAL,
  effect_size REAL,
  achieved_power REAL,
  prob_variant_wins REAL,          -- Bayesian
  expected_loss REAL,              -- Bayesian
  recommendation TEXT,             -- "ship", "keep_testing", "kill"
  recommendation_reasoning TEXT,
  full_results TEXT,               -- JSON of all computed values

  created_at DATETIME
)
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Landing — choose Pre-Test or Post-Test |
| GET | `/pre-test` | Sample size calculator form |
| GET | `/post-test` | Results analyzer form |
| POST | `/api/pre-test/calculate` | Compute sample size → return results partial |
| POST | `/api/post-test/analyze` | Compute significance → return results partial |
| GET | `/api/pre-test/power-curve` | Power curve chart data (JSON) |
| GET | `/api/post-test/distribution` | Distribution chart data (JSON) |
| GET | `/result/{id}` | Saved result detail |
| GET | `/history` | Past analyses |

### Application Structure

```
ab-test-analyzer/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── routers/ (pages.py, calculator.py)
│   ├── services/
│   │   ├── frequentist.py     # Z-test, power analysis, sample size
│   │   ├── bayesian.py        # Beta posteriors, Monte Carlo
│   │   ├── recommender.py     # Decision logic → Ship/Keep/Kill
│   │   └── charts.py          # Chart.js data formatters
│   ├── templates/
│   └── static/
├── tests/
│   ├── test_frequentist.py    # Validate against known statistical results
│   ├── test_bayesian.py
│   └── test_recommender.py
├── requirements.txt
└── README.md
```

---

## UI/UX

### Landing (`/`)
- Two large cards: "Pre-Test: Plan Your Experiment" and "Post-Test: Analyze Your Results"
- Mode toggle: Frequentist | Bayesian (affects both calculators)
- Recent analyses list

### Pre-Test Calculator (`/pre-test`)
- **Input section:**
  - Baseline conversion rate (% input with slider)
  - Minimum detectable effect (% input with slider)
  - Significance level (dropdown: 0.01, 0.05, 0.10)
  - Statistical power (dropdown: 0.80, 0.90, 0.95)
  - Daily traffic per variant (number input)
- **Results section (HTMX swap on calculate):**
  - Big number: Required sample size per variant
  - Estimated test duration in days
  - Power curve chart (power vs sample size, with current MDE highlighted)
  - Sensitivity table: required sample for different MDE values
- Calculate button triggers `hx-post` → results appear below without page reload

### Post-Test Analyzer (`/post-test`)
- **Input section:**
  - Control: visitors + conversions (or paste conversion rate)
  - Variant: visitors + conversions
  - Optional: test name and description
- **Results section (HTMX swap on analyze):**
  - **Verdict banner:** Large colored banner — green "Ship It", yellow "Keep Testing", red "Kill It" + reasoning paragraph
  - **Key metrics grid:** p-value, lift %, confidence interval, effect size, achieved power
  - **Distribution chart:** Two bell curves (control vs variant) with overlap shaded
  - **Lift chart:** Point estimate with CI whiskers
  - **Bayesian mode adds:** P(variant wins), expected loss, posterior distribution chart
  - Save button

### History (`/history`)
- Table: Name, Date, Mode, Method, Recommendation badge, Lift
- Click → full result detail

---

## Development Phases

### Phase 1: Statistical Engine (Days 1-3)
- [ ] Implement frequentist sample size calculator (SciPy)
- [ ] Implement frequentist post-test analyzer (z-test, CI, power)
- [ ] Implement Bayesian posterior calculation and Monte Carlo
- [ ] Implement recommendation logic
- [ ] Write statistical validation tests (compare against known textbook results)

### Phase 2: Web UI (Days 4-7)
- [ ] Project scaffold (FastAPI, templates, Tailwind, HTMX)
- [ ] Pre-test calculator page with HTMX form → results
- [ ] Post-test analyzer page with HTMX form → results
- [ ] Chart.js visualizations (distributions, power curves, CI plots)
- [ ] Mode toggle (Frequentist/Bayesian)

### Phase 3: History & Polish (Days 8-10)
- [ ] Save results to SQLite
- [ ] History page
- [ ] Result detail page
- [ ] Responsive design
- [ ] Deploy + add to portfolio

---

## Next Step

Implement `services/frequentist.py` and `services/bayesian.py` first as pure Python modules with no web dependencies. Write tests that validate calculations against known statistical results (e.g., a test with 1000 control visitors, 100 conversions, 1000 variant visitors, 120 conversions should produce a known p-value). The math must be correct before building the UI.

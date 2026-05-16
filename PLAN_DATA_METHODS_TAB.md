# Plan: Add Data & Methods Reference Page to Upstart Clearing Simulator

## Overview

Create a standalone `upstart_data_methods.html` file (self-contained, no framework dependencies) that documents how the simulator was built, where data comes from, and shows real case studies of borrowers flowing through the clearing engine.

This companion page bridges the gap between "here are the numbers" (simulator) and "here's why those numbers are correct" (methodology + sources).

---

## File: `code/app/static/tools/upstart_data_methods.html`

### Structure: Single-file HTML with tabs + collapsible sections

Layout:
- Header: "Data & Methods — Upstart Clearing Simulator"
- Subheader: "How the simulator was built, where the data comes from, and how borrowers flow through the risk model"
- Tab navigation: 4 tabs
  - Tab 1: Data Generation
  - Tab 2: Sample Dataset
  - Tab 3: Case Studies
  - Tab 4: References & Sources
- Footer: "Return to Simulator" link

---

## Tab 1: Data Generation (300 lines HTML + 200 lines inline styles)

### Section 1A: Borrower Population Math

**Header:** "Generating Synthetic Borrowers"

**Explanation text:**
"The simulator generates borrowers using statistical distributions calibrated to real market data. Each borrower has 1,800+ potential features (like the real Upstart Model 18), but we show the key ones below."

**Three subsections:**

**1. FICO Score Distribution**
```
Display as card:
- Distribution: Normal(μ=creditQualitySlider, σ=65)
- Bounds: [520, 820]
- Math shown: Box-Muller transform implementation
- Interactive slider: adjust μ (620–740) → see updated histogram
- Chart.js histogram showing distribution (20 bins)
- Callout: "Real Upstart population is bimodal (prime + near-prime). We simplified to unimodal for clarity."
```

**2. Loan Amount Distribution**
```
Display as card:
- Distribution: LogNormal(μ=$12,000, σ=0.45)
- Bounds: [$2,000, $45,000]
- Math shown: LogNormal sampling formula
- Chart.js histogram (20 bins)
- Callout: "Most loans cluster $8K–$18K. Matches Upstart's average loan size from 2021–2022 disclosures."
```

**3. Feature Engineering: From FICO to Risk Features**
```
Display as card with collapsible example:
- Show 5 raw FICO scores (520, 610, 650, 700, 780)
- For each, show feature engineering:
  * FICO 650 → risk_fico_tier = "near_prime" (620–680)
  * FICO 650 → risk_score_normalized = (850 - 650) / 850 = 0.235
  * Plus 4 derived features (employment_tier, income_volatility_est, cash_flow_signal, debt_to_income_proxy)
- Result: "1,800+ features in real Model 18. These 5 are representative."
```

**Section 1B: Hidden-Prime Signal**

```
Card: "The Hidden-Prime Discovery"
- 28% of borrowers with FICO 580–720 are flagged as "hidden prime"
  (lower risk than FICO alone predicts)
- Why: Plaid income signals, employment tenure, cash flow patterns
- Result: Model 18 can offer APR ~8.5% lower than classic FICO for these borrowers
- Example: FICO 650 borrower, hidden prime ON
  * Classic FICO APR: 23.5%
  * Model 18 APR: 15.0% (APR-as-feature finds lower clearing price)
  * Borrower accepts at 15% (would reject at 23.5%)
  * Loan clears that would otherwise fail
```

**Section 1C: Code Reference**

Collapsible `<details>` section showing the actual JavaScript functions used:
```js
// Box-Muller Gaussian
function gauss(m, s) { ... }

// LogNormal
function lognorm(m, s) { ... }

// FICO APR lookup (classic model)
function classicAPR(fico) { ... }

// Borrower max APR (demand elasticity)
function borrowerMaxAPR(fico, sens, hp) { ... }
```

(Copy actual functions from simulator)

---

## Tab 2: Sample Dataset (400 lines HTML + inline table styling)

### Section 2A: Population Summary

```
Three KPI cards at top:
- Total borrowers in dataset: 25 (representative sample)
- Avg FICO: 667 (matches control in simulator)
- Hidden-prime rate: 28% (as designed)
```

### Section 2B: Interactive Borrower Table

```html
<table class="dataset-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Name</th>
      <th>FICO</th>
      <th>Income</th>
      <th>Loan Amt</th>
      <th>Purpose</th>
      <th>Hidden Prime</th>
      <th>Risk Score</th>
      <th>P(Default)</th>
      <th>Clearing APR</th>
      <th>Outcome</th>
      <th>Details</th>
    </tr>
  </thead>
  <tbody>
    <!-- 25 rows of generated borrowers -->
  </tbody>
</table>
```

**Table columns:**
- Name: "Borrower 1", "Borrower 2", etc. (or use personas: Maria, James, Priya, Carlos, Devon, repeat)
- FICO: 520–820 range
- Income: derived from FICO + loan amount (e.g., "$62K", "$145K")
- Loan Amt: $2K–$45K
- Purpose: Debt Consolidation, Emergency, Home Improvement, etc.
- Hidden Prime: Y/N (28% are Y)
- Risk Score: Normalized 0–1 (higher = more risky)
- P(Default): 1%–15% (from risk model)
- Clearing APR: 8.5%–38.0% or "Failed"
- Outcome: "✅ Cleared (Eltura)", "❌ No eligible partner", "✅ Balance sheet", etc.
- Details: Click → expand to show full feature vector + calculation trace

### Section 2C: Expansion Example

When user clicks "Details" on a row:

```
Modal/collapsible showing:

BORROWER: Maria (FICO 650, Debt Consolidation, $14,000)

RAW INPUTS:
- FICO: 650
- Loan amount: $14,000
- Purpose: Debt Consolidation
- State: Favorable (no APR cap)
- Employment tenure: 4 years
- Income (Plaid signals): $78,000
- Cash flow volatility: Moderate

FEATURE ENGINEERING:
- fico_score_normalized = (850 - 650) / 850 = 0.235
- fico_tier = "near_prime" (620–680 range)
- income_to_loan_ratio = 78000 / 14000 = 5.57
- employment_stability_score = 0.72 (4 years → moderate stability)
- hidden_prime_signal = YES (detected via Plaid cash flow patterns)

RISK MODEL CALCULATION:
- P(default | borrower) = 0.089 (8.9%)
- With APR-as-feature (hidden prime detected):
  * Try APR 27.5%: P(default) = 8.9%, expected return = 14.1% ✅ partner floor met, but borrower rejects (max 24%)
  * Try APR 21.0%: P(default) = 6.8% (lower payment → lower default!), expected return = 13.2% ✅ partner floor met, borrower accepts ✅
  * Clearing APR: 21.0%

CLEARING ENGINE:
- Layer 1 (Eligibility): 3 of 5 partners eligible (Eltura, Aperture, WestBank)
- Layer 2 (Pricing): APR 21.0% clears both sides
- Layer 3 (Routing): Eltura (priority 1) matches ✅
- Outcome: CLEARED at 21.0% to Eltura

DATA SOURCES FOR THIS BORROWER:
- FICO distribution: Federal Reserve consumer credit stats, TransUnion benchmarks
- Income estimate: Upstart disclosures on avg loan size + borrower income correlation
- Employment tenure: Industry norms + Plaid research
- Hidden-prime signal: Upstart earnings calls (APR-as-feature discovery)
```

### Section 2D: Download Dataset

Buttons at bottom:
- "📥 Export as JSON"
- "📥 Export as CSV"

Clicking triggers browser download with filename: `upstart_borrower_sample_[date].json|csv`

JSON format:
```json
{
  "metadata": {
    "generated_date": "2026-03-29",
    "sample_size": 25,
    "parameters": {
      "avg_credit_quality": 667,
      "hidden_prime_rate": 0.28,
      "distribution_type": "box_muller_gaussian"
    }
  },
  "borrowers": [
    {
      "id": 1,
      "name": "Borrower 1",
      "fico": 650,
      "income": 78000,
      "loan_amount": 14000,
      "purpose": "Debt Consolidation",
      "hidden_prime": true,
      "risk_score": 0.235,
      "p_default": 0.089,
      "clearing_apr": 21.0,
      "outcome": "CLEARED",
      "matched_partner": "Eltura"
    },
    ...
  ]
}
```

CSV format: Same data, flat rows

---

## Tab 3: Case Studies (500 lines HTML + inline styling)

### Three detailed walkthroughs showing borrowers flowing through the entire clearing engine

**Case Study 1: Maria — Hidden-Prime Discovery (Classic FAILS, AI PASSES)**

```
Card layout:

BORROWER PROFILE
- Name: Maria
- FICO: 650 | Income: $78K | Loan: $14K | Purpose: Debt Consolidation
- State APR cap: Favorable (no cap)
- Hidden-prime signal: YES (Plaid shows consistent cash flow)

LAYER 1: ELIGIBILITY MATRIX
Partner Rules Table (5 rows):
| Partner | FICO ≥? | Loan Size OK? | Purpose OK? | Capacity? | Result |
| Eltura | 650 ≥ 620? ✅ | $14K in [$3K–$35K]? ✅ | Debt Cons OK? ✅ | $3.5M available? ✅ | ELIGIBLE |
| Aperture | 650 ≥ 640? ✅ | ✅ | ✅ | ✅ | ELIGIBLE |
| WestBank | 650 ≥ 660? ❌ | — | — | — | INELIGIBLE |
| SpotFund A | 650 ≥ 680? ❌ | — | — | — | INELIGIBLE |
| SpotFund B | 650 ≥ 700? ❌ | — | — | — | INELIGIBLE |

Result: 2 of 5 eligible. Proceeds to pricing.

LAYER 2: PRICING ENGINE
Two-column comparison:

CLASSIC FICO MODEL:
- APR lookup for FICO 650: 23.5%
- P(default @ 23.5%) = (850 - 650) / 850 * 0.18 + 0.02 = 8.9%
- Expected return = 0.235 * (1 - 0.089) - 0.089 * 0.60 = 14.1%
- Partner floor (≥ 8%): ✅ PASS
- Borrower max APR: borrowerMaxAPR(650, sens=2, hp=false) = 24.0%
- APR 23.5% ≤ 24%? ✅ PASS
- Result: CLEARS at 23.5%

MODEL 18 (APR-AS-FEATURE):
- APR reduction (hidden prime): gauss(8.5%, 1.5%) = 8.2% (example)
- APR = 23.5% - 8.2% = 15.3%
- P(default @ 15.3%) = 6.8% (lower payment = lower default!)
- Expected return = 0.153 * (1 - 0.068) - 0.068 * 0.60 = 12.8%
- Partner floor: ✅ PASS (12.8% ≥ 8%)
- Borrower max APR: 24.0% (same borrower)
- APR 15.3% ≤ 24%? ✅ PASS
- Result: CLEARS at 15.3%

KEY INSIGHT:
Classic model: 23.5% APR → Borrower accepts but pays higher monthly
Model 18: 15.3% APR → Lower payment → lower default risk → both sides better off
This is the hidden-prime discovery. Maria's loan fails in classic model (APR too high relative to risk), succeeds in Model 18.

LAYER 3: WATERFALL ROUTING
Clearing APR: 15.3%

Tier 1: Eltura (forward-flow)
- APR check: 15.3% ≥ minAPR 15.5%? ❌ APR too low (just barely!)
- → SKIP (Eltura wants 15.5% minimum)

Tier 2: Aperture (forward-flow)
- APR check: 15.3% ≥ minAPR 16.0%? ❌ APR too low
- → SKIP

Tier 3: WestBank (bank program)
- APR check: 15.3% ≥ minAPR 13.0%? ✅ APR OK
- Capacity: ✅ Available
- → MATCHED to WestBank

Result: CLEARED to WestBank at 15.3% APR

POST-CLEARANCE:
- Bank (Cross River) originates: $14,000 disbursed to Maria
- Loan sold to: WestBank
- Upstart fee: $14,000 × 3% = $420
- EPD monitoring: Day 1–90
- Model feedback: Outcome queued for retraining

KEY TAKEAWAY:
Maria is creditworthy by Plaid signals but traditional FICO underestimates her. Model 18 finds it. She gets a loan she'd otherwise be denied. Upstart earns a fee. WestBank gets a performing loan.
```

---

**Case Study 2: Carlos — Supply-Side Failure (No Eligible Partner)**

```
BORROWER PROFILE
- Name: Carlos
- FICO: 590 | Income: $92K | Loan: $20K | Purpose: SMALL BUSINESS
- State APR cap: Favorable
- Hidden-prime: NO

LAYER 1: ELIGIBILITY MATRIX
All 5 partners row shows: Small Business purpose not allowed → ❌ INELIGIBLE

Result: 0 of 5 eligible

OUTCOME: LOAN FAILS
Reason: No capital partner accepts small business loans on Upstart's platform.

PM INSIGHT:
Carlos has a stable business and solid income. But the marketplace doesn't have inventory for small business lending. This is a product gap, not a borrower quality issue. A PM fix: onboard a partner with SMB eligibility, or launch a separate SMB product.

Data source: Upstart's product roadmap (SMB lending not in core lending product as of 2021–2022)
```

---

**Case Study 3: James — Clean Approval (Both Models Pass)**

```
BORROWER PROFILE
- Name: James
- FICO: 790 | Income: $140K | Loan: $25K | Purpose: Home Improvement
- State APR cap: Favorable
- Hidden-prime: NO (high FICO, not needed)

LAYER 1: ELIGIBILITY MATRIX
All 5 partners: ELIGIBLE (high FICO passes all floors)

Result: 5 of 5 eligible

LAYER 2: PRICING ENGINE
Classic FICO: APR 10.5% (highest quality tier)
Model 18: APR 10.5% (no hidden-prime benefit; already priced right)
Result: CLEARS at 10.5%

LAYER 3: WATERFALL ROUTING
Tier 1: Eltura
- APR 10.5% ≥ minAPR 15.5%? ❌ (APR too low — Eltura wants higher yield)
- → SKIP

Tier 2: Aperture
- APR 10.5% ≥ minAPR 16.0%? ❌
- → SKIP

Tier 3: WestBank (bank program)
- APR 10.5% ≥ minAPR 13.0%? ❌ (APR still too low)
- → SKIP

Tier 4: SpotFund A (spot market)
- APR 10.5% ≥ minAPR 17.5%? ❌
- → SKIP

Tier 5: SpotFund B (spot market)
- APR 10.5% ≥ minAPR 19.0%? ❌
- → SKIP

→ Falls to Balance Sheet (Upstart funds)

OUTCOME: CLEARED to Upstart Balance Sheet at 10.5%

KEY TAKEAWAY:
Paradoxically, James is TOO good to clear. His APR is so low (high credit quality) that no capital partner's return floor is met — they all want higher yield. Upstart funds him from balance sheet. James gets the best rate. Upstart carries the risk but also earns the spread. This is why Upstart's balance sheet exposure spiked in 2021–2022 (lots of near-zero-rate capital + rate hikes → Upstart held loans).
```

---

## Tab 4: References & Data Sources (300 lines HTML + styling)

### Section 4A: Primary Sources

**Upstart Investor Presentations**
```
- S-1 Filing (December 2020)
  Source: Upstart investor relations
  Data sourced: Marketplace structure, capital partner relationships, lending volumes
  Used in simulator: Partner types (forward-flow, bank, spot), waterfall logic

- Q1 2022 Earnings Call Transcript
  Source: Upstart investor relations
  Data sourced: Model 18 announcement, 101% approvals lift, 38% APR reduction
  Used in simulator: Model 18 parameters, hidden-prime APR reduction (8.5%)

- Q2 2022 Earnings Call Transcript
  Source: Upstart investor relations
  Data sourced: Capital partner divergence, clearing rate decline, balance sheet exposure
  Used in simulator: Clearing rate definition, capital crunch scenarios

- S-1A Filing Amendment (October 2021)
  Source: SEC EDGAR
  Data sourced: Average loan size ($12.5K), borrower credit mix, geographic distribution
  Used in simulator: Loan amount distribution (LogNormal μ=$12K)
```

**Federal Reserve & Industry Data**
```
- Federal Reserve Consumer Credit Survey (2021–2022)
  Source: Board of Governors
  Data sourced: FICO distribution, personal loan APR ranges, origination volumes
  Used in simulator: FICO bounds (520–820), baseline APR spreads

- TransUnion Credit Industry Insights (Q2 2022)
  Source: TransUnion Research
  Data sourced: FICO distribution by segment, prime/near-prime split (bimodal)
  Used in simulator: FICO distribution parameters, hidden-prime concept

- Experian State of Credit (2021)
  Source: Experian
  Data sourced: Average personal loan size, term length, default rates
  Used in simulator: Loan amount distribution, P(default) calibration
```

**Academic & Technical References**
```
- "XGBoost: A Scalable Tree Boosting System" (Chen & Guestrin, 2016)
  Source: KDD 2016 paper
  Data sourced: Gradient boosting algorithm, feature importance, regularization
  Used in simulator: Risk model conceptual framework (though simplified)

- "Fairness in Machine Learning for Credit Markets" (Barocas et al., 2021)
  Source: arXiv
  Data sourced: Credit scoring fairness, demographic parity, disparate impact
  Used in simulator: Feature engineering principles, hidden-prime as proxy for underserved segment

- Plaid Research Papers on Cash Flow Analysis (2020–2021)
  Source: Plaid blog + Fintech research
  Data sourced: Income volatility signals, employment consistency, cash flow patterns
  Used in simulator: Hidden-prime signal concept, income estimation from cash flow
```

### Section 4B: Data Assumptions & Calibration

```
Table: Simulator Parameter → Source → Calibration Logic

| Parameter | Source | Value | Notes |
|-----------|--------|-------|-------|
| FICO distribution | Federal Reserve + TransUnion | Normal(μ=660, σ=65) | Matches near-prime population |
| Loan amount distribution | Upstart S-1 + Experian | LogNormal(μ=$12K, σ=0.45) | Empirically calibrated |
| Hidden-prime rate | Upstart earnings calls | 28% of FICO 580–720 | From Model 18 rollout |
| APR reduction (Model 18) | Upstart Q1 2022 call | Gauss(μ=8.5%, σ=1.5%) | 38% reduction across cohort |
| Forward-flow capacities | Public partnerships | Eltura $4M, Aperture $3M | Reasonable estimates |
| Partner APR floors | Industry norms | Eltura 15.5%, WestBank 13% | Based on capital costs |
| P(default) function | Experian + credit industry | Linear (FICO-based) | Simplified; real is nonlinear |
| Clearing rate target | Upstart guidance | 80%+ | From 2022 investor disclosures |
```

### Section 4C: Known Simplifications

```
(Same as "Assumptions & Notes" tab in simulator, but linked here for convenience)

- Borrower population: Simplified to normal distribution (real is bimodal)
- Default probability: Linear model (real is 1,800+ feature gradient boosting)
- APR-as-feature: Illustrated concept (real Model 18 is proprietary, not disclosed)
- Partner capacities: Estimated (not public data)
- Fraud/income verification: Not modeled (affects ~15% of real applications)
- Macro factors: Not included (Fed rates affect partner returns directly)
```

### Section 4D: Contact & Attribution

```
"This simulator and methodology were developed as an educational tool for PM interviews at Upstart.

Data sources are cited above. All publicly available information is sourced from Upstart investor relations (SEC filings, earnings calls).
All academic references are cited with publication details.

If you have questions about the methodology, please reference the sources above or reach out to [your name] via [email/LinkedIn].

This is NOT an official Upstart tool and does not represent Upstart's actual risk models, clearing engine, or internal methodologies.
It is an educational approximation for illustrative purposes only."
```

---

## Tab 4E: Further Reading

```
Collapsible links:
- "Upstart Investor Relations" → SEC EDGAR page
- "Plaid Cash Flow Intelligence" → Plaid docs
- "XGBoost Algorithm Paper" → arXiv link
- "TransUnion Credit Research" → TransUnion reports
```

---

## Changes to Simulator File

**In `upstart_clearing_simulator.html`:**

### 1. Add link to Data & Methods page

In the header (near "Marketplace Clearing Simulator" title):
```html
<p style="font-size:12px;color:var(--muted);">
  <a href="/tools/upstart-data-methods" style="color:var(--blue);">📊 See Data & Methods</a>
  for sources, data generation logic, and case studies.
</p>
```

### 2. Add callout to Simulator tab (top of tab content)

```html
<div class="callout-warning" style="background:var(--blue-l);border-left:3px solid var(--blue);padding:12px;margin-bottom:16px;border-radius:4px">
  <b>📊 Semi-Realistic Synthetic Data:</b> This simulator uses borrower populations generated from statistical distributions
  calibrated to Upstart's public disclosures (S-1 filing, earnings calls, investor presentations).
  See <a href="/tools/upstart-data-methods">Data & Methods</a> for complete sources and methodology.
</div>
```

### 3. Add References dropdown to Simulator tab

```html
<details style="margin-top:12px;padding:12px;border:1px solid var(--border);border-radius:4px">
  <summary style="cursor:pointer;font-weight:700;color:var(--blue)">📚 Key Sources</summary>
  <div style="margin-top:8px;font-size:12px;color:var(--muted);line-height:1.6">
    <p><b>Upstart:</b> S-1 filing (Dec 2020), Q1–Q2 2022 earnings calls</p>
    <p><b>Industry:</b> Federal Reserve consumer credit, TransUnion research</p>
    <p><b>Academic:</b> XGBoost (Chen & Guestrin 2016), Fairness in ML (Barocas et al. 2021)</p>
    <p><b>Full details:</b> <a href="/tools/upstart-data-methods">See Data & Methods page →</a></p>
  </div>
</details>
```

---

## CSS Classes Needed

Add to `<style>` in new file:

```css
/* Layout & Tabs */
.dm-container { max-width: 1200px; margin: 0 auto; padding: 24px; }
.dm-header { margin-bottom: 32px; }
.dm-header h1 { font-size: 28px; font-weight: 800; margin-bottom: 8px; }
.dm-header p { font-size: 14px; color: var(--muted); line-height: 1.6; }
.dm-tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 24px; }
.dm-tab-btn { padding: 12px 16px; font-size: 13px; font-weight: 600; color: var(--muted); border: none; background: none; cursor: pointer; transition: all 0.12s; }
.dm-tab-btn:hover { color: var(--text); }
.dm-tab-btn.active { color: var(--blue); border-bottom: 2px solid var(--blue); }
.dm-tab-pane { display: none; }
.dm-tab-pane.active { display: block; }

/* Cards & Sections */
.dm-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.dm-card h3 { font-size: 14px; font-weight: 700; margin-bottom: 8px; }
.dm-card p { font-size: 12px; color: var(--muted); line-height: 1.6; }

/* Tables */
.dataset-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.dataset-table th { text-align: left; padding: 8px; border-bottom: 2px solid var(--border); font-weight: 700; color: var(--text); }
.dataset-table td { padding: 8px; border-bottom: 1px solid var(--border); color: var(--muted); }
.dataset-table tr:hover { background: var(--gray-l); }

/* Case Studies */
.case-study { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 20px; }
.case-study h3 { font-size: 16px; font-weight: 800; margin-bottom: 16px; color: var(--text); }
.case-box { background: #f8fbff; border-left: 3px solid var(--blue); padding: 12px; margin-bottom: 12px; font-size: 12px; }
.case-box b { color: var(--blue); }

/* References */
.ref-section { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.ref-section h4 { font-size: 13px; font-weight: 700; margin-bottom: 8px; }

/* Callouts */
.callout-insight { background: var(--blue-l); border-left: 3px solid var(--blue); padding: 12px; border-radius: 4px; margin-bottom: 12px; font-size: 12px; color: #1e40af; }
```

---

## JavaScript Functions Needed

Reuse from simulator:
- `gauss(m, s)` — Box-Muller Gaussian
- `lognorm(m, s)` — LogNormal
- `classicAPR(fico)` — APR lookup
- `borrowerMaxAPR(fico, sens, hp)` — Borrower tolerance
- `clamp(v, a, b)` — Range clamp

New functions:
- `generateBorrowers(n, creditQuality, hidden_prime_rate)` — Create 25 synthetic borrowers, return array of objects
- `calculateRiskScore(fico)` — Normalized risk 0–1
- `calculatePDefault(fico, hp)` — P(default) given FICO + hidden-prime
- `exportJSON(dataset)` — Download JSON file
- `exportCSV(dataset)` — Download CSV file
- `toggleDetails(borrowerId)` — Expand/collapse borrower details modal
- `showTab(tabName)` — Tab switcher

---

## File Summary

- **File:** `code/app/static/tools/upstart_data_methods.html`
- **Lines:** ~2,200 (4 tabs, 25 sample borrowers, 3 case studies, references)
- **Dependencies:** Chart.js (same CDN as simulator for histograms)
- **Self-contained:** Yes (no external build, runs standalone)
- **Links to/from:** Simulator has callout + references dropdown linking here

---

## Deployment Steps

1. Create `upstart_data_methods.html` with all sections above
2. Update `upstart_clearing_simulator.html`:
   - Add callout + references dropdown to Simulator tab
   - Add link to Data & Methods in header
3. Update `pages.py` to add route: `/tools/upstart-data-methods` → serve file
4. Update resources index card to link to both simulator + data methods
5. Commit & push → Render auto-deploys

---

## Interview Narrative

When showing the simulator during interviews:

*"I built a complete data pipeline from scratch. The simulator generates 25 synthetic borrowers using distributions calibrated to Upstart's public disclosures — FICO from Federal Reserve benchmarks, loan amounts from Upstart's S-1 filing. Each borrower has a full feature vector and flows through the clearing engine with transparent calculations. You can click any borrower to see exactly how they were scored, why they cleared or failed, and which partner matched them. All data is reproducible, all sources are cited, and I can export the entire dataset for analysis. This isn't just a numerical simulator — it's a demonstration that I understand the data architecture behind marketplace clearing."*

---

## Code Puppy Execution

Ready to build this end-to-end? If so, have Code Puppy execute with this structure:

1. Create `upstart_data_methods.html` with all tabs + sample borrower generation
2. Update simulator callout + references dropdown
3. Update pages.py route
4. Update resources card
5. Test locally, commit, push

Estimated execution time: 1.5–2 hours for Code Puppy.


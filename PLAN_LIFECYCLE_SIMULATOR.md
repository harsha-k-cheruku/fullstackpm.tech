# Plan: Upstart Lifecycle Simulator — Full Build

## Context

**What:** Rebuild the Upstart Clearing Simulator from scratch as a full loan lifecycle simulator. Not a patch of the existing tool — a ground-up rebuild that reuses proven logic but builds on the fullstackpm.tech design system.

**Why:** The current simulator is a 1,824-line monolithic HTML file with inline styles, disconnected tabs, and no lifecycle beyond the clearing moment. The new simulator needs to show borrowers entering the pipeline, clearing through the engine, performing over 36 months, and the impact on capital partner portfolios — all animated and interactive.

**Who uses it:** The site owner demos this to a hiring manager (Director of Product at Upstart) in a 45-minute interview presentation. It also serves as a standalone portfolio piece for any visitor.

**Constraints:**
- 2-week build window
- Entirely client-side JS (no backend computation)
- 100 borrowers max, 5 capital partners (2 forward-flow, 1 bank, 1 spot, 1 balance sheet)
- Must extend `base.html` (Jinja2 + Tailwind + dark mode + nav/footer)
- Must reuse `borrower_generation.js` as-is

**Replaces:** `code/app/static/tools/upstart_clearing_simulator.html` (the old simulator stays until new one is verified, then gets removed)

---

## Files to Create

| File | Type | Purpose |
|------|------|---------|
| `code/app/templates/lifecycle_simulator.html` | Jinja2 template | Main page — extends base.html, 5 tabs, all UI |
| `code/app/static/js/clearing_engine.js` | JS module | Eligibility, pricing, waterfall routing — extracted from old simulator |
| `code/app/static/js/lifecycle_engine.js` | JS module | Month-by-month payment/default/payoff simulation |
| `code/app/static/js/animation_controller.js` | JS module | Play/pause/resume, Chart.js live updates, intervention hooks |
| `code/app/static/css/simulator.css` | CSS | Simulator-specific styles (supplements Tailwind) |

## Files to Modify

| File | Change |
|------|--------|
| `code/app/routers/pages.py` | Add route for `/tools/lifecycle-simulator` |
| `code/content/projects/upstart-clearing-simulator.md` | Update tech_stack, description, live_url |

## Files to Reuse (no changes)

| File | What to reuse |
|------|---------------|
| `code/app/static/tools/borrower_generation.js` | All of it — generate 100 synthetic borrowers |
| Old `upstart_clearing_simulator.html` | Extract `clearLoans()` logic, partner configs, persona data, walkthrough step logic |

## Files to Eventually Remove

| File | When |
|------|------|
| `code/app/static/tools/upstart_clearing_simulator.html` | After new simulator is verified and deployed |

---

## Data Structures

### Capital Partners (5 total)

```javascript
const PARTNERS = [
  // Forward-flow (committed volume, priority routing)
  {
    id: 'eltura',
    name: 'Eltura Capital',
    type: 'forward_flow',
    priority: 1,
    ficoFloor: 640,
    ficoMax: 850,
    minLoan: 5000,
    maxLoan: 50000,
    minAPR: 15.5,
    purposes: ['debt_consolidation', 'credit_card', 'home_improvement', 'major_purchase'],
    capacity: 25,          // max loans in this simulation (out of 100)
    returnFloor: 8.0,      // minimum acceptable annualized return %
    epdTrigger: 5.0,       // EPD % that triggers repurchase review
    color: '#3b82f6'       // chart color
  },
  {
    id: 'aperture',
    name: 'Aperture Finance',
    type: 'forward_flow',
    priority: 2,
    ficoFloor: 620,
    ficoMax: 750,
    minLoan: 3000,
    maxLoan: 35000,
    minAPR: 17.0,
    purposes: ['debt_consolidation', 'credit_card', 'medical', 'major_purchase'],
    capacity: 20,
    returnFloor: 10.0,
    epdTrigger: 5.0,
    color: '#8b5cf6'
  },
  // Bank (origination partner, regulatory role)
  {
    id: 'westbank',
    name: 'WestBank',
    type: 'bank',
    priority: 3,
    ficoFloor: 600,
    ficoMax: 850,
    minLoan: 1000,
    maxLoan: 50000,
    minAPR: 13.0,
    purposes: ['debt_consolidation', 'credit_card', 'home_improvement', 'medical', 'major_purchase', 'small_business'],
    capacity: 30,
    returnFloor: 6.0,
    epdTrigger: 6.0,
    color: '#10b981'
  },
  // Spot (opportunistic, higher return floor)
  {
    id: 'spotfund',
    name: 'SpotFund B',
    type: 'spot',
    priority: 4,
    ficoFloor: 660,
    ficoMax: 780,
    minLoan: 10000,
    maxLoan: 40000,
    minAPR: 19.0,
    purposes: ['debt_consolidation', 'credit_card'],
    capacity: 10,
    returnFloor: 12.0,
    epdTrigger: 4.0,
    color: '#f59e0b'
  },
  // Balance Sheet (Upstart itself — backstop, last resort)
  {
    id: 'upstart_bs',
    name: 'Upstart (Balance Sheet)',
    type: 'balance_sheet',
    priority: 99,
    ficoFloor: 580,
    ficoMax: 850,
    minLoan: 1000,
    maxLoan: 50000,
    minAPR: 0,
    purposes: ['debt_consolidation', 'credit_card', 'home_improvement', 'medical', 'major_purchase', 'small_business'],
    capacity: 100,          // unlimited backstop
    returnFloor: 0,
    epdTrigger: 999,
    color: '#ef4444'
  }
];
```

### Borrower State (lifecycle)

```javascript
// After clearing, each funded borrower gets this state object
{
  id: 0,                       // index
  fico: 653,
  amount: 14000,
  purpose: 'debt_consolidation',
  hiddenPrime: true,
  offeredAPR: 16.2,
  matchedPartner: 'eltura',
  term: 36,                    // months
  monthlyPayment: 495.12,      // calculated from amount + APR + term

  // Lifecycle state (updated each month)
  status: 'current',           // 'current' | '30dpd' | '60dpd' | '90dpd' | 'default' | 'paid_off' | 'early_payoff'
  remainingBalance: 12340.00,
  monthsActive: 6,
  paymentHistory: ['ok','ok','ok','ok','ok','late'], // one entry per month
  totalPaid: 2970.72,
  totalInterestPaid: 810.72
}
```

### Partner Portfolio State (updated each month)

```javascript
{
  partnerId: 'eltura',
  loansHeld: 18,
  totalFunded: 252000,
  currentPerforming: 16,
  delinquent30: 1,
  delinquent60: 0,
  delinquent90: 0,
  defaulted: 1,
  paidOff: 0,
  earlyPayoff: 0,

  // Computed metrics
  portfolioYield: 11.2,        // annualized actual return %
  epdRate: 2.1,                // early payment default rate %
  cumulativeLossRate: 0.8,     // total losses / total funded %
  utilization: 72.0,           // loans held / capacity %
  concentrationRisk: {         // FICO band distribution
    '580-619': 0,
    '620-659': 8,
    '660-699': 6,
    '700-739': 3,
    '740+': 1
  }
}
```

### Simulation Snapshot (one per month, stored in array)

```javascript
// simulation.snapshots[month] =
{
  month: 6,
  portfolioHealth: {
    current: 72,
    dpd30: 8,
    dpd60: 3,
    dpd90: 1,
    defaulted: 4,
    paidOff: 8,
    earlyPayoff: 4
  },
  partnerStates: { /* partnerId → PartnerPortfolioState */ },
  upstartMetrics: {
    cumulativeFees: 18400,
    balanceSheetExposure: 6.2,   // %
    clearingRate: 86.0,          // % from original clearing
    modelAccuracy: 0.94,         // predicted vs actual default correlation
    revenuePerLoan: 420,
    monthlyOrigination: 0        // only non-zero in month 0
  },
  borrowerMetrics: {
    approvalRate: 92.0,
    clearingRate: 86.0,
    avgAPR: 18.4,
    hiddenPrimeUnlockRate: 28.0,
    acceptanceRate: 86.0,        // % who accepted offer
    delinquencyRate: 12.0        // % currently 30+ DPD
  }
}
```

---

## Module APIs

### clearing_engine.js

```javascript
window.clearingEngine = {

  /**
   * Run full clearing simulation on a borrower pool
   * @param {Array} borrowers - from borrower_generation.js
   * @param {Array} partners - partner config array
   * @param {string} modelType - 'classic' | 'model18'
   * @returns {Object} { cleared: [...], failed: [...], stats: {...}, allocations: {...} }
   */
  runClearing(borrowers, partners, modelType),

  /**
   * Check one borrower against one partner's eligibility rules
   * @param {Object} borrower
   * @param {Object} partner
   * @param {number} remainingCapacity - current remaining slots
   * @returns {Object} { eligible: bool, reasons: [...] }
   */
  checkEligibility(borrower, partner, remainingCapacity),

  /**
   * Price a loan for a borrower
   * @param {Object} borrower
   * @param {string} modelType - 'classic' | 'model18'
   * @returns {Object} { apr: number, pDefault: number, expectedReturn: number, hiddenPrimeReduction: number }
   */
  priceLoan(borrower, modelType),

  /**
   * Route a priced borrower through the waterfall
   * @param {Object} borrower - with pricing attached
   * @param {Array} eligiblePartners - partners that passed eligibility
   * @param {Object} allocations - current capacity usage { partnerId: count }
   * @returns {Object} { matched: bool, partner: string|null, reason: string }
   */
  waterfallRoute(borrower, eligiblePartners, allocations),

  /**
   * Walk through clearing for a single borrower (detailed step-by-step)
   * @param {Object} borrower
   * @param {Array} partners
   * @param {string} modelType
   * @param {Object} allocations - optional, for capacity tracking
   * @returns {Object} { steps: [...], outcome: string, detail: {...} }
   */
  walkthrough(borrower, partners, modelType, allocations)
};
```

### lifecycle_engine.js

```javascript
window.lifecycleEngine = {

  /**
   * Initialize portfolio from clearing results
   * @param {Array} clearedLoans - loans that were funded
   * @param {Array} partners - partner config array
   * @returns {Object} portfolio state object
   */
  initPortfolio(clearedLoans, partners),

  /**
   * Advance portfolio by one month
   * @param {Object} portfolio - current portfolio state
   * @param {number} month - which month we're stepping into
   * @param {Object} config - { baseDefaultRate, earlyPayoffRate, recoveryRate }
   * @returns {Object} updated portfolio + snapshot for this month
   */
  stepMonth(portfolio, month, config),

  /**
   * Get transition probabilities for a borrower
   * Risk-grade based: higher risk = higher P(delinquency)
   * @param {Object} borrower - with current status and risk grade
   * @param {Object} config - user-configurable rates
   * @returns {Object} { pOnTime, pLate, pDefault, pEarlyPayoff }
   */
  getTransitionProbs(borrower, config),

  /**
   * Compute partner portfolio metrics from current loan states
   * @param {Array} loans - all loans assigned to this partner
   * @param {Object} partner - partner config
   * @returns {Object} PartnerPortfolioState
   */
  computePartnerMetrics(loans, partner),

  /**
   * Compute Upstart platform metrics
   * @param {Object} portfolio - full portfolio state
   * @returns {Object} upstartMetrics
   */
  computeUpstartMetrics(portfolio),

  /**
   * Compute borrower health metrics
   * @param {Object} portfolio - full portfolio state
   * @returns {Object} borrowerMetrics
   */
  computeBorrowerMetrics(portfolio),

  /**
   * Apply a partner intervention (mid-simulation eligibility change)
   * @param {Object} portfolio
   * @param {string} partnerId
   * @param {Object} changes - { ficoFloor?, capacity?, enabled? }
   * @returns {Object} updated portfolio with intervention logged
   */
  applyIntervention(portfolio, partnerId, changes)
};
```

### animation_controller.js

```javascript
window.animationController = {

  /**
   * Initialize the animation system
   * @param {Object} portfolio - from lifecycleEngine.initPortfolio()
   * @param {Object} config - { speed: 500, maxMonths: 36, onTick, onComplete, onPause }
   */
  init(portfolio, config),

  /**
   * Start or resume animation
   * Calls lifecycleEngine.stepMonth() on each tick
   * Updates all registered charts and KPI elements
   */
  play(),

  /**
   * Pause animation at current month
   * Enables partner intervention panel
   */
  pause(),

  /**
   * Resume after pause (possibly with interventions applied)
   */
  resume(),

  /**
   * Jump to a specific month (for analytics tab month selector)
   * @param {number} month
   */
  seekTo(month),

  /**
   * Register a Chart.js chart for live updates
   * @param {string} chartId
   * @param {Chart} chartInstance
   * @param {Function} updateFn - called with (snapshot, month) on each tick
   */
  registerChart(chartId, chartInstance, updateFn),

  /**
   * Register a KPI element for live updates
   * @param {string} elementId
   * @param {Function} valueFn - called with (snapshot) → returns display value
   */
  registerKPI(elementId, valueFn),

  /**
   * Get current state
   * @returns {Object} { month, playing, snapshots, portfolio }
   */
  getState()
};
```

---

## Transition Probability Model (lifecycle_engine.js)

This is the core logic for month-by-month simulation. Keep it simple and configurable.

### Risk Grades

Map FICO to risk grade (reuse from borrower_generation.js):
```
A: FICO ≥ 740  |  B: 700–739  |  C: 660–699  |  D: 620–659  |  E: < 620
```

### Monthly Transition Matrix (defaults — user can adjust via sliders)

For a borrower in **current** status:

| Risk Grade | P(stay current) | P(→ 30DPD) | P(early payoff) |
|------------|-----------------|-------------|-----------------|
| A | 0.985 | 0.005 | 0.010 |
| B | 0.975 | 0.010 | 0.015 |
| C | 0.955 | 0.025 | 0.020 |
| D | 0.930 | 0.045 | 0.025 |
| E | 0.900 | 0.070 | 0.030 |

For a borrower in **30DPD** status:

| Risk Grade | P(recover → current) | P(→ 60DPD) |
|------------|---------------------|-------------|
| A | 0.70 | 0.30 |
| B | 0.60 | 0.40 |
| C | 0.50 | 0.50 |
| D | 0.40 | 0.60 |
| E | 0.30 | 0.70 |

For **60DPD**: P(recover) = 0.20, P(→ 90DPD) = 0.80 (all grades)
For **90DPD**: P(recover) = 0.05, P(→ default) = 0.95 (all grades)

**Hidden-prime adjustment:** If `borrower.hiddenPrime === true`, use one grade better transition probabilities (e.g., D-grade hidden-prime uses C-grade probabilities). This is the whole point — Model 18 identifies borrowers whose actual risk is better than FICO suggests.

### Configurable Sliders (exposed in UI)

| Slider | Range | Default | What it does |
|--------|-------|---------|--------------|
| Base Default Rate | 0.5x – 2.0x | 1.0x | Multiplier on all P(→ delinquent) transitions |
| Early Payoff Rate | 0.5x – 2.0x | 1.0x | Multiplier on P(early payoff) |
| Recovery Rate | 0.5x – 2.0x | 1.0x | Multiplier on P(recover from DPD) |

### Amortization

Standard fixed-rate amortization:
```javascript
function monthlyPayment(principal, annualRate, termMonths) {
  const r = annualRate / 100 / 12;
  return principal * r / (1 - Math.pow(1 + r, -termMonths));
}
```

Each performing month: interest = remainingBalance × (APR/12), principal = payment - interest, remainingBalance -= principal.

### Partner Yield Calculation

```javascript
function annualizedYield(partner) {
  const totalInterestReceived = partner.loans
    .filter(l => l.status !== 'default')
    .reduce((sum, l) => sum + l.totalInterestPaid, 0);
  const totalLosses = partner.loans
    .filter(l => l.status === 'default')
    .reduce((sum, l) => sum + l.remainingBalance, 0);
  const netReturn = totalInterestReceived - totalLosses;
  const avgMonthsDeployed = /* weighted average months active */;
  return (netReturn / partner.totalFunded) * (12 / avgMonthsDeployed) * 100;
}
```

---

## Scenario Presets

Three pre-configured scenarios that tell different stories:

### Healthy Market (default)
```javascript
{
  name: 'Healthy Market',
  description: 'Normal conditions — balanced supply/demand, stable default rates',
  modelType: 'model18',
  borrowerCount: 100,
  ficoMean: 680,
  defaultMultiplier: 1.0,
  earlyPayoffMultiplier: 1.0,
  recoveryMultiplier: 1.0,
  partnerOverrides: {}  // all partners at default config
}
```

### Capital Crunch (2022)
```javascript
{
  name: 'Capital Crunch (2022)',
  description: 'Forward-flow partners pull back, capacity drops, BS exposure spikes',
  modelType: 'model18',
  borrowerCount: 100,
  ficoMean: 660,
  defaultMultiplier: 1.5,
  earlyPayoffMultiplier: 0.5,
  recoveryMultiplier: 0.7,
  partnerOverrides: {
    eltura: { capacity: 10, ficoFloor: 680 },     // tightened
    aperture: { capacity: 5, ficoFloor: 700 },     // nearly pulled out
    spotfund: { enabled: false }                    // gone
  }
}
```

### Rate Spike
```javascript
{
  name: 'Rate Spike',
  description: 'Rising rates push APRs up, borrower acceptance drops, prime borrowers refi away',
  modelType: 'model18',
  borrowerCount: 100,
  ficoMean: 690,
  defaultMultiplier: 1.2,
  earlyPayoffMultiplier: 1.8,      // prime borrowers leaving fast
  recoveryMultiplier: 0.9,
  partnerOverrides: {
    eltura: { minAPR: 18.0 },       // raised return floor
    aperture: { minAPR: 20.0 },
    spotfund: { minAPR: 22.0 }
  }
}
```

---

## UI Specification

### Template Structure

```html
<!-- code/app/templates/lifecycle_simulator.html -->
{% extends "base.html" %}
{% block title %}Upstart Lifecycle Simulator{% endblock %}

{% block head %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="/tools/borrower_generation.js"></script>
<script src="/static/js/clearing_engine.js"></script>
<script src="/static/js/lifecycle_engine.js"></script>
<script src="/static/js/animation_controller.js"></script>
<link rel="stylesheet" href="/static/css/simulator.css">
{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 py-6">

  <!-- Header + Scenario Selector -->
  <div class="flex items-center justify-between mb-4">
    <div>
      <h1 class="text-xl font-bold">Upstart Lifecycle Simulator</h1>
      <p class="text-sm text-gray-500">Full loan lifecycle: pipeline → clearing → portfolio performance → partner impact</p>
    </div>
    <div class="flex gap-2">
      <!-- Scenario preset buttons -->
    </div>
  </div>

  <!-- Tab Navigation (5 tabs) -->
  <div class="border-b border-gray-200 dark:border-gray-700 mb-4">
    <nav class="flex gap-0">
      <button data-tab="pipeline">Pipeline & Clearing</button>
      <button data-tab="timeline">Portfolio Timeline</button>
      <button data-tab="analytics">Marketplace Analytics</button>
      <button data-tab="deepdive">Loan Deep Dive</button>
      <button data-tab="reapp">Re-Application Funnel</button>
    </nav>
  </div>

  <!-- Tab Panes -->
  <div id="tab-pipeline">...</div>
  <div id="tab-timeline">...</div>
  <div id="tab-analytics">...</div>
  <div id="tab-deepdive">...</div>
  <div id="tab-reapp">...</div>

</div>
{% endblock %}
```

### Tab 1: Pipeline & Clearing

**Layout:** Left sidebar (controls) + Right main (results)

**Left sidebar (260px):**
- Borrower count display: "100 borrowers"
- FICO mean slider (620–740, default 680)
- Model toggle: Classic FICO / Model 18
- Partner checklist: 5 partners with on/off toggles + color dots
- "▶ Generate & Clear" button (primary action)

**Right main:**
- **Before run:** Empty state with explainer text
- **After run:**
  - KPI row (4 cards): Clearing Rate, BS Exposure, Avg APR, Hidden-Prime Unlocked
  - Insight callouts (conditional — green/yellow/red based on thresholds)
  - Charts row: Waterfall doughnut (cleared/apr_high/no_partner) + Partner utilization bar
  - **Borrower Results Table:**
    - Columns: #, FICO, Amount, Purpose, HP, APR, Outcome, Partner, [Walk →]
    - Filter buttons: All / Cleared / APR Rejected / No Partner
    - Max 100 rows (all borrowers)
    - Color-coded rows: green (cleared), red (APR rejected), gray (no partner)
    - HP column: ★ for hidden-prime
    - Click "Walk →" button → switches to Loan Deep Dive tab with that borrower loaded
  - Row count: "Showing 86 of 100 loans (Cleared)"

### Tab 2: Portfolio Timeline

**Layout:** Top controls + Left partner panel + Center charts + Right metrics

**Only available after clearing runs.** Show locked state with message: "Run clearing simulation first →"

**Top controls bar:**
- Month counter: "Month 12 / 36" (large, prominent)
- Play ▶ / Pause ⏸ / Reset ↺ buttons
- Speed selector: 0.5x / 1x / 2x (controls interval speed)
- Config sliders: Base Default Rate, Early Payoff Rate, Recovery Rate

**Left partner panel (240px):**
- One card per partner (5 total):
  - Partner name + color dot + type badge
  - Editable fields (only when paused): FICO floor, capacity, on/off toggle
  - "Modified" badge if changed from defaults
  - When playing: fields are read-only, metrics update live

**Center charts (flex grow):**
- **Portfolio Health** (stacked area chart, primary):
  - X-axis: Month 0–36
  - Y-axis: # of loans
  - Series: Current (green), 30DPD (yellow), 60DPD (orange), 90DPD (red), Default (dark red), Paid Off (blue), Early Payoff (light blue)
  - Updates each tick — new data point added, chart scrolls
- **Cumulative Loss Rate** (line chart, secondary):
  - X-axis: Month 0–36
  - Y-axis: Loss rate %
  - One line per partner + one for overall portfolio
  - Threshold line at each partner's EPD trigger

**Right metrics panel (280px):**
- **Upstart Platform card:**
  - Cumulative fees: $XX,XXX
  - BS exposure: X.X%
  - Revenue/loan: $XXX
- **Per-partner cards (scrollable):**
  - Portfolio Yield: XX.X% (north star — large font)
  - EPD Rate: X.X% (red if approaching trigger)
  - Loss Rate: X.X%
  - Utilization: XX%
  - Traffic light indicator (green/yellow/red)

**Intervention flow:**
1. User clicks ⏸ Pause
2. Partner panel fields become editable
3. User changes Aperture FICO floor from 620 → 660
4. "Intervention at Month 12" badge appears
5. User clicks ▶ Resume
6. Simulation continues with new eligibility rules
7. Vertical dashed line appears on charts at Month 12 with label "Intervention"

### Tab 3: Marketplace Analytics

**Only available after lifecycle simulation has run (at least 1 month).**

**Top:** Month selector — dropdown or slider to pick any month from 0 to current. Defaults to latest month.

**Three panels in a grid (1 row × 3 columns on desktop, stacked on mobile):**

**Panel 1: Borrower Health**
- Approval Rate: XX% (bar)
- Clearing Rate: XX% (bar)
- Avg APR Offered: XX.X%
- Hidden-Prime Unlock Rate: XX%
- Acceptance Rate: XX%
- Current Delinquency Rate: XX% (with trend arrow ↑↓)
- Risk Grade Distribution: horizontal stacked bar (A/B/C/D/E)

**Panel 2: Upstart Platform Health**
- Cumulative Platform Fees: $XX,XXX (with monthly trend sparkline)
- Balance Sheet Exposure: XX.X% (gauge or bar with green/yellow/red zones)
- Revenue Per Loan: $XXX
- Model Accuracy: XX% (predicted vs actual default)
- Clearing Efficiency: XX% (matched on first waterfall tier)
- Monthly Origination Volume: XX (only non-zero at month 0)

**Panel 3: Capital Partner Health**
- **Per-partner sub-cards** (one per active partner):
  - Portfolio Yield: XX.X% (north star, large)
  - EPD Rate: XX.X%
  - Cumulative Loss Rate: XX.X%
  - Utilization: XX%
  - FICO Concentration: mini horizontal bar
  - Traffic light: 🟢 / 🟡 / 🔴
  - If red: callout box — "EPD at X.X% — approaching Y% repurchase trigger"
- **Aggregate metrics:**
  - Partner Diversity Index (how evenly distributed is volume)
  - At-Risk Partners count

**Traffic light thresholds:**

| Metric | 🟢 Green | 🟡 Yellow | 🔴 Red |
|--------|---------|----------|--------|
| Clearing Rate | ≥ 85% | 70–85% | < 70% |
| BS Exposure | < 8% | 8–15% | > 15% |
| Partner EPD | < 3% | 3–4.5% | > 4.5% |
| Partner Loss Rate | < 5% | 5–8% | > 8% |
| Model Accuracy | > 90% | 80–90% | < 80% |

### Tab 4: Loan Deep Dive

**Layout:** Borrower selector at top + 4-step walkthrough below

**Borrower selector:**
- Dropdown of all 100 borrowers (sorted by: interesting ones first — hidden-prime, failed, edge cases)
- Persona shortcuts: Maria (hidden-prime win), Carlos (supply failure), James (BS paradox)
- Or: "Click Walk → on any row in Pipeline tab"

**4-step walkthrough (vertical flow, expanding cards):**

**Step 1: Eligibility Matrix**
- Table: one row per partner
- Columns: Partner | FICO Check | Loan Size | Purpose | Capacity | Result
- Each cell: ✅ or ❌ with the actual values
- Summary: "3 of 5 partners eligible"

**Step 2: Pricing Engine**
- Side-by-side comparison: Classic FICO vs Model 18
- Each side shows: APR, P(default), Expected Return, Partner Floor Check, Borrower Max APR
- Highlight which model wins
- If hidden-prime: callout showing the APR reduction and why

**Step 3: Waterfall Routing**
- Vertical waterfall: Tier 1 → Tier 2 → ... → Balance Sheet
- Each tier: partner name, APR check (offered vs. floor), capacity check, result (MATCH / SKIP)
- Green highlight on the matching tier
- If failed: red highlight showing where and why

**Step 4: Funding & Lifecycle (if lifecycle has run)**
- Funded amount, APR, term, monthly payment
- Payment history strip: one colored cell per month (green=ok, yellow=late, red=default, blue=paid off)
- Current status, remaining balance, total paid, total interest
- If defaulted: which month, remaining balance at default (= partner loss)

### Tab 5: Re-Application Funnel (stub)

**Static content — no simulation:**

- Header: "Re-Application Pipeline — Product Roadmap"
- Summary card: "Of X borrowers who completed loans, Y% would re-apply within 18 months (estimated)"
- **Rules Framework** (display only):
  1. Payment history quality (on-time rate > 95% → 2x more likely)
  2. Income growth signal (employment tenure + income trajectory)
  3. Time since completion (12–18 month sweet spot)
  4. Improved risk profile (FICO lift from successful payment history)
  5. Loan purpose affinity (debt consolidation borrowers → home improvement next)
- **PM Framing callout:**
  > "This is a product roadmap item, not a current feature. The PM question is: what data do we already have from the loan lifecycle that predicts re-application? Payment history, FICO trajectory, and income signals are all available without additional data collection. The acquisition cost of a returning borrower is ~60% lower than a new borrower, and their risk profile is measurably better because we have observed performance data."
- Visual: simple funnel graphic (100 funded → 85 completed → 13 re-apply → 11 funded again)

---

## Router Addition

```python
# In code/app/routers/pages.py — add this route

@router.get("/tools/lifecycle-simulator", response_class=HTMLResponse)
async def lifecycle_simulator(request: Request):
    return templates.TemplateResponse(
        "lifecycle_simulator.html",
        {"request": request, "title": "Upstart Lifecycle Simulator"}
    )
```

---

## Build Stages & Acceptance Criteria

### Stage 1: Foundation + Tab 1 (Days 1–3)

**Build:**
1. Create `lifecycle_simulator.html` extending `base.html` — header, 5 tab buttons, tab switching JS
2. Create `simulator.css` — simulator-specific styles that complement Tailwind
3. Create `clearing_engine.js` — extract and modularize from old simulator:
   - `runClearing()`, `checkEligibility()`, `priceLoan()`, `waterfallRoute()`
   - Partner config as exported constant
   - Model 18 hidden-prime APR reduction logic
4. Add route in `pages.py`
5. Build Tab 1 UI: sidebar controls + generate button + results rendering
6. Build borrower results table with filters

**Acceptance criteria:**
- [ ] Page loads at `/tools/lifecycle-simulator` with nav, footer, dark mode
- [ ] Selecting a scenario preset updates sidebar controls
- [ ] Clicking "Generate & Clear" produces 100 borrowers and runs them through clearing
- [ ] KPI cards show: clearing rate, BS exposure, avg APR, hidden-prime unlocked
- [ ] Borrower table shows all 100 loans with correct outcomes
- [ ] Filter buttons work (All / Cleared / APR Rejected / No Partner)
- [ ] Clicking "Walk →" switches to Loan Deep Dive tab (even if that tab is empty placeholder)
- [ ] All 5 partner types represented in results
- [ ] Classic vs Model 18 toggle changes clearing outcomes visibly

### Stage 2: Lifecycle Engine (Days 4–6)

**Build:**
1. Create `lifecycle_engine.js` with all functions from API spec above
2. Implement transition probability matrix
3. Implement amortization calculator
4. Implement partner metric aggregation
5. Implement Upstart + borrower metric computation
6. Implement intervention application
7. Test by calling `stepMonth()` 36 times in console and inspecting output

**Acceptance criteria:**
- [ ] `initPortfolio()` takes clearing output and creates stateful borrower array
- [ ] `stepMonth()` advances all borrowers by 1 month with probabilistic outcomes
- [ ] After 36 months: some borrowers current, some defaulted, some paid off, some early payoff
- [ ] Hidden-prime borrowers default at lower rates than same-FICO non-hidden-prime
- [ ] Partner metrics compute correctly (yield, EPD, loss rate, utilization)
- [ ] Upstart metrics compute correctly (fees, BS exposure)
- [ ] Config multipliers actually affect outcomes (2x default rate → more defaults)
- [ ] `applyIntervention()` changes partner eligibility for future months
- [ ] All functions are deterministic when given same random seed

### Stage 3: Animated Timeline — Tab 2 (Days 7–9)

**Build:**
1. Create `animation_controller.js`
2. Build Tab 2 UI: controls bar, partner panel, chart area, metrics panel
3. Create Chart.js instances: stacked area (portfolio health) + line (loss rate)
4. Wire animation loop: play → tick → stepMonth → update charts + KPIs
5. Implement pause/resume with partner intervention editing
6. Add intervention markers (vertical dashed lines on charts)
7. Speed selector (0.5x = 1000ms, 1x = 500ms, 2x = 250ms per month)

**Acceptance criteria:**
- [ ] Tab 2 is locked until clearing runs
- [ ] Clicking Play starts animation — month counter ticks, charts update live
- [ ] Stacked area chart grows with each month
- [ ] Partner metric cards update each month
- [ ] Clicking Pause stops animation, enables partner editing
- [ ] Changing a partner's FICO floor while paused → Resume → visible impact on subsequent months
- [ ] Intervention appears as vertical dashed line on charts
- [ ] Speed selector works (0.5x/1x/2x)
- [ ] Reset returns to Month 0
- [ ] Capital Crunch scenario produces visibly worse outcomes (higher defaults, more BS exposure)

### Stage 4: Marketplace Analytics — Tab 3 (Day 10)

**Build:**
1. Build Tab 3 UI: month selector + 3-panel grid
2. Wire month selector to `animationController.seekTo()`
3. Render borrower health panel from snapshot data
4. Render Upstart platform panel from snapshot data
5. Render per-partner health cards from snapshot data
6. Traffic light logic (green/yellow/red thresholds)
7. At-risk partner callouts

**Acceptance criteria:**
- [ ] Tab 3 is locked until lifecycle has run at least 1 month
- [ ] Month selector shows data for any completed month
- [ ] All three panels render with correct metrics
- [ ] Traffic lights reflect thresholds correctly
- [ ] At-risk partner callout appears when EPD > 4.5%
- [ ] Changing month selector updates all three panels
- [ ] Data matches what Tab 2 showed for that same month

### Stage 5: Loan Deep Dive — Tab 4 (Days 11–12)

**Build:**
1. Build Tab 4 UI: borrower selector + 4-step walkthrough
2. Wire persona shortcuts (Maria, Carlos, James)
3. Wire "Walk →" click from Tab 1 results table
4. Implement Step 1: eligibility matrix table
5. Implement Step 2: pricing comparison (classic vs Model 18 side-by-side)
6. Implement Step 3: waterfall routing visualization
7. Implement Step 4: funding + payment history strip (if lifecycle ran)

**Acceptance criteria:**
- [ ] Selecting any borrower from dropdown shows their full walkthrough
- [ ] Persona shortcuts load predefined borrowers
- [ ] Click from Tab 1 table loads correct borrower
- [ ] Step 1 shows pass/fail for each partner with actual values
- [ ] Step 2 shows classic vs Model 18 side-by-side with correct math
- [ ] Step 3 shows waterfall with clear MATCH/SKIP per tier
- [ ] Step 4 shows payment history strip if lifecycle has run
- [ ] Hidden-prime borrowers show the APR reduction callout

### Stage 6: Re-App Stub + Project Page + Polish + Demo (Days 13–14)

**Build:**
1. Build Tab 5: static re-application funnel content
2. **Update project page** — replace `code/content/projects/upstart-clearing-simulator.md` with new content (see Project Page Content below)
3. Add scenario preset functionality (Healthy / Capital Crunch / Rate Spike)
4. Loading states for all tabs (skeleton loaders or spinners)
5. Empty states with clear messaging
6. Error handling (edge cases in clearing or lifecycle)
7. Mobile responsiveness pass
8. Test all three scenarios end-to-end
9. Write demo script (exact narrative per click)
10. Verify project card renders correctly on `/resources/product-breakdowns` page

**Acceptance criteria:**
- [ ] Tab 5 shows re-application funnel with rules framework
- [ ] Project page card on `/resources/product-breakdowns` shows correct title, description, tech stack, and live link
- [ ] Project detail page renders full What/Why/How content
- [ ] `live_url` points to `/tools/lifecycle-simulator` (not old URL)
- [ ] Tech stack shows actual technologies used
- [ ] All three scenario presets work and tell distinct stories
- [ ] No empty/broken states — every tab has appropriate messaging
- [ ] Works on mobile (stacked layout, scrollable)
- [ ] All 5 tabs work together as connected experience
- [ ] Full demo can be completed in 5–7 minutes
- [ ] No console errors in any flow

---

## Personas (reuse from old simulator)

### Maria — Hidden-Prime Discovery
- FICO 650, Income $78K, Loan $14K, Debt Consolidation
- Hidden-prime: YES
- Classic: APR ~23.5% (borderline fail)
- Model 18: APR ~15.3% (clear win)
- Routes to WestBank (Eltura/Aperture floors too high)
- Lifecycle: strong performer, pays on time, early payoff at Month 28

### Carlos — Supply-Side Failure
- FICO 590, Income $42K, Loan $8K, Small Business
- Hidden-prime: NO
- Fails eligibility at all partners (Small Business not supported at FICO 590)
- Demo point: "This is a product gap, not a borrower quality issue"

### James — Balance Sheet Paradox
- FICO 790, Income $120K, Loan $30K, Home Improvement
- Hidden-prime: NO (doesn't need it)
- Both models: APR ~10.5%
- All partner APR floors fail (too low for their return requirements)
- Falls to balance sheet
- Demo point: "So creditworthy his APR is below all partner floors"

---

## What NOT to Build

- No backend computation (everything in browser JS)
- No database / persistence (simulation state lives in memory, gone on refresh)
- No user accounts or saved simulations
- No real Upstart data (all synthetic, with disclaimer)
- No Data & Methods page updates (follow-on)
- No actual re-application simulation (stub only)
- No automated testing (manual verification per acceptance criteria)
- Do NOT modify `borrower_generation.js`

---

## Demo Script (write during Stage 6)

Target: 5–7 minutes, covering:
1. (30s) Intro — "I built a lifecycle simulator for Upstart's capital marketplace"
2. (60s) Tab 1 — Generate 100 loans, run clearing, show results, point out hidden-prime
3. (90s) Tab 2 — Play animation, narrate portfolio evolution, pause at Month 12, intervene, resume
4. (60s) Tab 3 — Show marketplace analytics, point out at-risk partner, explain PM action
5. (30s) Tab 4 — Click through Maria's deep dive
6. (30s) Tab 5 — Show re-application framework, explain PM roadmap thinking
7. (30s) Close — "This is how I think about marketplace operations"

---

## Project Page Content

**File:** `code/content/projects/upstart-clearing-simulator.md`

Replace the entire file with the following (matches existing project card format):

```markdown
---
title: "Upstart Lifecycle Simulator"
description: "Full loan lifecycle simulator for Upstart's capital marketplace — pipeline generation, three-layer clearing engine, animated 36-month portfolio performance, capital partner health monitoring, and mid-simulation intervention testing."
tech_stack: [Vanilla JS, Chart.js, Tailwind CSS, Jinja2, FastAPI]
status: "live"
featured: true
display_order: 2
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/lifecycle-simulator"
problem: "Marketplace clearing decisions have a 90-day feedback delay — a PM changes partner eligibility today but doesn't see the EPD impact for months. The 2022 capital crunch showed what happens when this delay prevents preventive action: Upstart held $1B+ on its balance sheet."
approach: "Build an interactive lifecycle simulator that compresses 36 months of portfolio evolution into 3 minutes. Generate synthetic borrowers, clear them through a three-layer engine, then watch month-by-month performance with live capital partner metrics — including the ability to intervene mid-simulation and see downstream effects."
solution: "A browser-based sandbox with 5 connected views: Pipeline & Clearing (generate + match 100 loans), Portfolio Timeline (animated month-by-month with intervention), Marketplace Analytics (three-stakeholder health dashboard), Loan Deep Dive (step-by-step borrower walkthrough), and Re-Application Funnel (product roadmap framing). All client-side JS — no backend computation."
---

## What

A full lifecycle simulator for Upstart's capital marketplace. Not just the clearing moment — the entire journey from borrower pipeline through 36 months of portfolio performance.

**Features:**
- **Pipeline & Clearing** — Generate 100 synthetic borrowers, run them through eligibility → pricing (Classic vs Model 18) → waterfall routing across 5 capital partners
- **Animated Portfolio Timeline** — Watch loans perform month-by-month: payments, delinquencies, defaults, early payoffs. Partner metrics update live.
- **Mid-Simulation Intervention** — Pause at any month, tighten a partner's eligibility or capacity, resume and see the downstream impact immediately
- **Three-Stakeholder Analytics** — Borrower Health, Upstart Platform Health, and Capital Partner Health dashboards with traffic-light indicators
- **Loan Deep Dive** — Click any borrower to walk through their clearing decision step-by-step, plus payment history if lifecycle has run
- **Scenario Presets** — Healthy Market, Capital Crunch (2022), Rate Spike — each tells a different marketplace story
- **Hidden-Prime Discovery** — See Model 18 unlock borrowers that FICO undervalues, with side-by-side pricing comparison

## Why

Upstart's capital marketplace is one of the most sophisticated clearing engines in fintech — but the feedback loops are invisible. A PM adjusting partner eligibility today doesn't see the EPD impact for 90 days. This simulator makes the causal chain visible:

- **Compress time** — 36 months of portfolio evolution in 3 minutes
- **Make tradeoffs tangible** — See clearing rate vs. partner EPD vs. balance sheet exposure in real-time
- **Test interventions safely** — What if you tighten Aperture's FICO floor at Month 8 vs. Month 14? Run both scenarios.
- **Three-stakeholder thinking** — Borrower experience, platform economics, and partner returns all in one view
- **Model 18 intuition** — See exactly how APR-as-feature discovers hidden-prime borrowers and creates marketplace value

Built for PM candidates, marketplace operators, and anyone curious about how lending marketplaces actually work.

## How

**Architecture:**
- **Computation:** Entirely client-side JavaScript — no backend API calls, no database, no network latency
- **Rendering:** Chart.js for animated charts, Tailwind CSS + Jinja2 templates (extends site base.html)
- **Modules:** 4 JS files — `borrower_generation.js` (synthetic data), `clearing_engine.js` (eligibility + pricing + routing), `lifecycle_engine.js` (month-by-month simulation), `animation_controller.js` (play/pause/resume + Chart.js updates)
- **Scale:** 100 borrowers × 5 partners × 36 months = 3,600 state transitions per simulation. Runs in <200ms total.

**The flow:**
1. Select a scenario (Healthy Market, Capital Crunch, Rate Spike) or configure custom parameters
2. Generate 100 borrowers and run them through the three-layer clearing engine
3. Review clearing results — KPIs, borrower table, filter by outcome
4. Play the portfolio timeline — watch metrics evolve month by month, animated
5. Pause → adjust partner eligibility → resume → see the intervention's impact
6. Switch to Analytics dashboard — identify at-risk partners, check platform health
7. Deep dive into any individual borrower's clearing decision and payment history

**Data sources:**
- Transition probabilities based on industry personal lending data (configurable)
- Partner structures inspired by Upstart's public filings (names obfuscated)
- Credit score distributions reflect market reality for near-prime personal lending
- All data synthetic — clear disclaimer displayed

**Limitations:**
- Simplified lifecycle model (Markov chain, not vintage-calibrated)
- 100-borrower scale (sufficient for demo, not for statistical analysis)
- No persistence — simulation state resets on page refresh
- Re-application stage is a product roadmap stub, not simulated
```

**Verification:** After writing this file, check that:
1. The project card renders correctly on `/resources/product-breakdowns`
2. Title, description, and tech stack display properly
3. `live_url` links to `/tools/lifecycle-simulator`
4. The What/Why/How sections render on the project detail page

---

## Reference: Old Simulator Code Locations

For extracting logic into new modules:

| Logic | Old file location | Lines (approx) |
|-------|-------------------|-----------------|
| `clearLoans()` | upstart_clearing_simulator.html | ~1400–1500 |
| `makeBorrowers()` | upstart_clearing_simulator.html | ~1300–1400 |
| `evalEligibility()` | upstart_clearing_simulator.html | ~1550–1600 |
| Partner config array | upstart_clearing_simulator.html | ~1200–1300 |
| Walkthrough logic | upstart_clearing_simulator.html | ~1600–1825 |
| Persona definitions | upstart_clearing_simulator.html | ~1060–1100 |
| KPI rendering | upstart_clearing_simulator.html | ~1450–1500 |
| Chart.js setup | upstart_clearing_simulator.html | ~1500–1550 |

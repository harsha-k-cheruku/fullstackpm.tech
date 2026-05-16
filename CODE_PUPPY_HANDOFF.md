# Code Puppy Handoff: Upstart Lifecycle Simulator Build

**Timeline:** 2 weeks (Days 1–14)
**Status:** Ready for execution
**Reference:** `PLAN_LIFECYCLE_SIMULATOR.md` (detailed specs, data structures, APIs, acceptance criteria)

---

## TL;DR — What You're Building

A browser-based lifecycle simulator for Upstart's capital marketplace. It generates 100 synthetic loans, clears them through a three-layer engine, then simulates 36 months of portfolio performance with animated charts and live metrics. Users can pause, adjust capital partner eligibility, and see downstream effects. All client-side JS — no backend computation.

**5 connected tabs:**
1. Pipeline & Clearing — generate + match loans
2. Portfolio Timeline — animated month-by-month performance
3. Marketplace Analytics — three-stakeholder health dashboard
4. Loan Deep Dive — step-by-step borrower walkthrough
5. Re-Application Funnel — product roadmap stub

**Demo use case:** Full walkthrough in 5–7 minutes, showing marketplace operations thinking.

---

## Before You Start

### 1. Read These Files (in order)

1. `PLAN_LIFECYCLE_SIMULATOR.md` (this repo) — full spec, data structures, module APIs, acceptance criteria
2. `upstart_simulator.md` (interview prep folder) — brainstorm/discovery notes
3. `15_Simulator_PRFAQ.md` (interview prep folder) — context on what this tool solves
4. `16_Simulator_PRD.md` (interview prep folder) — detailed product requirements
5. `17_Simulator_BRD.md` (interview prep folder) — business context and success metrics

### 2. Understand the Stack

- **Frontend:** Vanilla JS (no frameworks), Chart.js 4.4.0, Tailwind CSS, Jinja2 templates
- **Backend:** FastAPI (already exists, just add one route)
- **No new dependencies.** Everything you need is in the project or via CDN.

### 3. Know the Three-Layer Clearing Engine

The logic you'll extract from the old simulator and refactor:
- **Layer 1 (Eligibility):** Does borrower meet partner FICO/loan size/purpose requirements? Capacity available?
- **Layer 2 (Pricing):** What APR clears both borrower acceptance and partner return floor? Classic FICO vs Model 18 (hidden-prime).
- **Layer 3 (Waterfall):** Route borrower through partner priority tiers. First match wins. Falls to balance sheet if no match.

---

## Stage 1: Foundation + Tab 1 (Days 1–3)

### What You're Building
- Jinja2 template extending `base.html`
- Clearing engine module (extracted from old simulator)
- Tab 1 UI with sidebar controls and results table
- Route in FastAPI

### Step-by-Step

**Step 1a: Create the template** (1 hour)

File: `code/app/templates/lifecycle_simulator.html`

```html
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

  <!-- Header -->
  <div class="flex items-center justify-between mb-4">
    <div>
      <h1 class="text-2xl font-bold dark:text-white">Upstart Lifecycle Simulator</h1>
      <p class="text-sm text-gray-600 dark:text-gray-400">Full loan lifecycle: pipeline → clearing → 36-month portfolio performance</p>
    </div>
    <div class="flex gap-2" id="scenario-buttons"></div>
  </div>

  <!-- Tabs -->
  <div class="border-b border-gray-200 dark:border-gray-700 mb-4">
    <nav class="flex gap-0" role="tablist">
      <button role="tab" data-tab="pipeline" class="px-4 py-2 font-semibold border-b-2 border-transparent dark:text-gray-400 tab-btn active">Pipeline & Clearing</button>
      <button role="tab" data-tab="timeline" class="px-4 py-2 font-semibold border-b-2 border-transparent dark:text-gray-400 tab-btn">Portfolio Timeline</button>
      <button role="tab" data-tab="analytics" class="px-4 py-2 font-semibold border-b-2 border-transparent dark:text-gray-400 tab-btn">Marketplace Analytics</button>
      <button role="tab" data-tab="deepdive" class="px-4 py-2 font-semibold border-b-2 border-transparent dark:text-gray-400 tab-btn">Loan Deep Dive</button>
      <button role="tab" data-tab="reapp" class="px-4 py-2 font-semibold border-b-2 border-transparent dark:text-gray-400 tab-btn">Re-Application</button>
    </nav>
  </div>

  <!-- Tab 1: Pipeline & Clearing -->
  <div role="tabpanel" id="tab-pipeline" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
    <!-- Left sidebar: controls -->
    <div class="md:col-span-1 bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
      <h3 class="text-sm font-bold uppercase text-gray-600 dark:text-gray-400 mb-4">Borrower Generation</h3>
      <div class="space-y-4">
        <div>
          <label class="text-xs font-semibold text-gray-600 dark:text-gray-400">FICO Mean: <span class="font-bold text-blue-600 dark:text-blue-400" id="fico-value">680</span></label>
          <input type="range" id="fico-slider" min="620" max="740" value="680" class="w-full">
        </div>
        <div>
          <label class="text-xs font-semibold text-gray-600 dark:text-gray-400">Model</label>
          <div class="flex gap-2 mt-1">
            <button class="flex-1 px-2 py-1 text-xs font-semibold rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 model-btn active" data-model="model18">Model 18</button>
            <button class="flex-1 px-2 py-1 text-xs font-semibold rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 model-btn" data-model="classic">Classic</button>
          </div>
        </div>
        <button id="gen-clear-btn" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded">▶ Generate & Clear</button>
      </div>
    </div>

    <!-- Right side: results -->
    <div class="md:col-span-3">
      <div id="pipeline-empty" class="text-center py-12 text-gray-500 dark:text-gray-400">
        <p class="text-sm">Click "Generate & Clear" to start</p>
      </div>
      <div id="pipeline-results" style="display:none" class="space-y-4">
        <!-- KPI cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3" id="kpi-cards"></div>
        <!-- Filters -->
        <div class="flex gap-2 flex-wrap" id="filter-buttons"></div>
        <!-- Borrower table -->
        <div class="bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 overflow-x-auto">
          <table class="w-full text-xs">
            <thead class="bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
              <tr>
                <th class="px-3 py-2 text-left">#</th>
                <th class="px-3 py-2 text-left">FICO</th>
                <th class="px-3 py-2 text-left">Amount</th>
                <th class="px-3 py-2 text-left">Purpose</th>
                <th class="px-3 py-2 text-left">HP</th>
                <th class="px-3 py-2 text-left">APR</th>
                <th class="px-3 py-2 text-left">Outcome</th>
                <th class="px-3 py-2 text-left">Partner</th>
                <th class="px-3 py-2 text-left"></th>
              </tr>
            </thead>
            <tbody id="borrower-table-body"></tbody>
          </table>
        </div>
        <div class="text-xs text-gray-500 dark:text-gray-400" id="table-count"></div>
      </div>
    </div>
  </div>

  <!-- Tab 2: Portfolio Timeline -->
  <div role="tabpanel" id="tab-timeline" style="display:none" class="space-y-4">
    <div class="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700 text-yellow-800 dark:text-yellow-200 p-3 rounded text-sm" id="timeline-locked">
      Run clearing simulation first → Timeline will unlock
    </div>
    <div id="timeline-content" style="display:none" class="space-y-4">
      <!-- Controls bar -->
      <div class="bg-white dark:bg-gray-800 p-4 rounded border border-gray-200 dark:border-gray-700 space-y-4">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div class="text-2xl font-bold dark:text-white">Month <span id="month-counter">0</span> / 36</div>
          <div class="flex gap-2">
            <button id="play-btn" class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded">▶ Play</button>
            <button id="pause-btn" class="px-4 py-2 bg-gray-400 text-white font-semibold rounded" disabled>⏸ Pause</button>
            <button id="reset-btn" class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded">↺ Reset</button>
          </div>
          <div class="flex gap-2 items-center">
            <label class="text-xs font-semibold text-gray-600 dark:text-gray-400">Speed:</label>
            <select id="speed-select" class="px-2 py-1 text-sm rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white">
              <option value="0.5">0.5x</option>
              <option value="1" selected>1x</option>
              <option value="2">2x</option>
            </select>
          </div>
        </div>

        <!-- Config sliders -->
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="text-xs font-semibold text-gray-600 dark:text-gray-400">Default Rate: <span id="default-value">1.0x</span></label>
            <input type="range" id="default-slider" min="0.5" max="2" step="0.1" value="1" class="w-full">
          </div>
          <div>
            <label class="text-xs font-semibold text-gray-600 dark:text-gray-400">Early Payoff: <span id="payoff-value">1.0x</span></label>
            <input type="range" id="payoff-slider" min="0.5" max="2" step="0.1" value="1" class="w-full">
          </div>
          <div>
            <label class="text-xs font-semibold text-gray-600 dark:text-gray-400">Recovery: <span id="recovery-value">1.0x</span></label>
            <input type="range" id="recovery-slider" min="0.5" max="2" step="0.1" value="1" class="w-full">
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="lg:col-span-2 bg-white dark:bg-gray-800 p-4 rounded border border-gray-200 dark:border-gray-700">
          <h3 class="text-sm font-bold mb-2 dark:text-white">Portfolio Health</h3>
          <canvas id="health-chart" height="80"></canvas>
        </div>
        <div class="bg-white dark:bg-gray-800 p-4 rounded border border-gray-200 dark:border-gray-700">
          <h3 class="text-sm font-bold mb-2 dark:text-white">Loss Rate</h3>
          <canvas id="loss-chart" height="80"></canvas>
        </div>
      </div>

      <!-- Metrics panels -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="metrics-panels"></div>
    </div>
  </div>

  <!-- Tab 3: Marketplace Analytics -->
  <div role="tabpanel" id="tab-analytics" style="display:none">
    <div class="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700 text-yellow-800 dark:text-yellow-200 p-3 rounded text-sm" id="analytics-locked">
      Run portfolio simulation first → Analytics will unlock
    </div>
    <div id="analytics-content" style="display:none" class="space-y-4">
      <div class="flex items-center gap-4 mb-4">
        <label class="text-sm font-semibold text-gray-600 dark:text-gray-400">View month:</label>
        <select id="month-selector" class="px-3 py-1 rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white">
          <option value="0">Month 0</option>
        </select>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="analytics-panels"></div>
    </div>
  </div>

  <!-- Tab 4: Loan Deep Dive -->
  <div role="tabpanel" id="tab-deepdive" style="display:none" class="space-y-4">
    <div id="deepdive-empty" class="text-center py-12 text-gray-500 dark:text-gray-400">
      <p class="text-sm">Click "Walk" on any borrower in Pipeline tab</p>
    </div>
    <div id="deepdive-content" style="display:none" class="space-y-4">
      <div class="bg-white dark:bg-gray-800 p-4 rounded border border-gray-200 dark:border-gray-700">
        <label class="text-sm font-semibold text-gray-600 dark:text-gray-400">Select borrower:</label>
        <div class="flex gap-2 mt-2 flex-wrap">
          <select id="borrower-selector" class="flex-1 px-3 py-2 rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white text-sm"></select>
          <button class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded text-sm" onclick="SIM.showPersona('maria')">Maria</button>
          <button class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded text-sm" onclick="SIM.showPersona('carlos')">Carlos</button>
          <button class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded text-sm" onclick="SIM.showPersona('james')">James</button>
        </div>
      </div>
      <div id="walkthrough-steps" class="space-y-4"></div>
    </div>
  </div>

  <!-- Tab 5: Re-Application -->
  <div role="tabpanel" id="tab-reapp" style="display:none" class="max-w-2xl">
    <div class="bg-white dark:bg-gray-800 p-6 rounded border border-gray-200 dark:border-gray-700 space-y-4">
      <h2 class="text-lg font-bold dark:text-white">Re-Application Pipeline — Product Roadmap</h2>
      <div class="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 p-4 rounded text-sm text-blue-900 dark:text-blue-200">
        <p class="font-semibold mb-2">Estimated Re-Application Rate</p>
        <p id="reapp-stat">Of X borrowers who completed loans, Y% would re-apply within 18 months</p>
      </div>
      <div>
        <h3 class="font-bold mb-3 dark:text-white">Rules Framework</h3>
        <ol class="space-y-2 text-sm dark:text-gray-300">
          <li><strong>1. Payment History Quality:</strong> On-time rate >95% → 2x more likely to re-apply</li>
          <li><strong>2. Income Growth Signal:</strong> Employment tenure + income trajectory predict ability to take larger loan</li>
          <li><strong>3. Time Since Completion:</strong> 12–18 month window is the sweet spot for re-application</li>
          <li><strong>4. Improved Risk Profile:</strong> FICO lift from successful payment history improves approval odds</li>
          <li><strong>5. Loan Purpose Affinity:</strong> Debt consolidation borrowers → home improvement next; major purchase → auto next</li>
        </ol>
      </div>
      <div class="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 p-4 rounded text-sm text-blue-900 dark:text-blue-200">
        <p><strong>PM Framing:</strong> This is a product roadmap item, not a current feature. The question is: what data exists from the loan lifecycle that predicts re-application? All five signals above are available without additional data collection. Re-acquisition cost is ~60% lower than new borrower acquisition, and risk profile is measurably better because we have observed performance data.</p>
      </div>
    </div>
  </div>

</div>

<script>
// Tab switching
document.querySelectorAll('[role="tab"]').forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    document.querySelectorAll('[role="tabpanel"]').forEach(p => p.style.display = 'none');
    document.getElementById(`tab-${tab}`).style.display = 'block';
    document.querySelectorAll('[role="tab"]').forEach(b => b.classList.remove('active', 'border-blue-600', 'text-blue-600', 'dark:text-blue-400', 'dark:border-blue-400'));
    btn.classList.add('active', 'border-blue-600', 'text-blue-600', 'dark:text-blue-400', 'dark:border-blue-400');
  });
});

// Stub: actual functionality comes from clearing_engine.js, lifecycle_engine.js, animation_controller.js
console.log('Lifecycle Simulator loaded. Ready for clearing_engine, lifecycle_engine, animation_controller modules.');
</script>
{% endblock %}
```

**Step 1b: Create clearing_engine.js** (2 hours)

File: `code/app/static/js/clearing_engine.js`

Extract from the old simulator (`code/app/static/tools/upstart_clearing_simulator.html`), refactor into modular functions. See `PLAN_LIFECYCLE_SIMULATOR.md` for full API spec.

Key functions to export:
- `runClearing(borrowers, partners, modelType)` — main entry point
- `checkEligibility(borrower, partner, remainingCapacity)`
- `priceLoan(borrower, modelType)`
- `waterfallRoute(borrower, eligiblePartners, allocations)`

Model 18 hidden-prime logic: If `hiddenPrime === true`, reduce APR by ~8.2% and adjust P(default) downward.

**Step 1c: Add FastAPI route** (30 min)

File: `code/app/routers/pages.py`

```python
@router.get("/tools/lifecycle-simulator", response_class=HTMLResponse)
async def lifecycle_simulator(request: Request):
    return templates.TemplateResponse(
        "lifecycle_simulator.html",
        {"request": request, "title": "Upstart Lifecycle Simulator"}
    )
```

**Step 1d: Create simulator.css** (30 min)

File: `code/app/static/css/simulator.css`

Minimal — mostly Tailwind + a few overrides:
```css
.tab-btn {
  @apply transition-all;
}
.tab-btn.active {
  @apply border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400;
}
```

**Step 1e: Wire up Tab 1** (1.5 hours)

In your JavaScript (inside the template or a separate file), implement:
- FICO slider updates display value
- Model toggle switches between Classic/Model 18
- "Generate & Clear" button calls:
  1. `borrowerGeneration.generateBorrowerFull(100, ficoMean, 0.28)` → get borrowers
  2. `clearingEngine.runClearing(borrowers, PARTNERS, modelType)` → get results
  3. `renderTab1Results(results)` → display KPIs, table, filters

**Acceptance Criteria for Stage 1:**
- [ ] Page loads at `/tools/lifecycle-simulator`
- [ ] Sidebar controls (FICO slider, Model toggle) work
- [ ] Clicking "Generate & Clear" produces 100 borrowers
- [ ] Results show KPI cards (clearing rate %, BS exposure %, avg APR, hidden-prime unlocked %)
- [ ] Borrower table shows all loans with FICO, Amount, Purpose, APR, Outcome, Partner
- [ ] Outcome color coding: green (cleared), red (APR rejected), gray (no partner)
- [ ] HP column shows ★ for hidden-prime borrowers
- [ ] Filter buttons work (All / Cleared / APR Rejected / No Partner)
- [ ] Click "Walk" on any row switches to Loan Deep Dive tab (placeholder OK for now)
- [ ] No console errors

---

## Stage 2: Lifecycle Engine (Days 4–6)

### What You're Building
- `lifecycle_engine.js` module with all functions from spec
- Transition probability matrix for borrower payment behavior
- Partner metric computation
- Intervention logic

### Reference
See `PLAN_LIFECYCLE_SIMULATOR.md` — "Transition Probability Model" section for the full matrix and logic.

### Key Functions (API spec in plan)

```javascript
window.lifecycleEngine = {
  initPortfolio(clearedLoans, partners),
  stepMonth(portfolio, month, config),
  getTransitionProbs(borrower, config),
  computePartnerMetrics(loans, partner),
  computeUpstartMetrics(portfolio),
  computeBorrowerMetrics(portfolio),
  applyIntervention(portfolio, partnerId, changes)
};
```

### Hidden-Prime Adjustment

If `borrower.hiddenPrime === true`, use one risk grade better transition probabilities. E.g., D-grade hidden-prime uses C-grade probabilities.

### Partner Yield Formula

```
yield = (totalInterest - totalLosses) / totalFunded * (12 / avgMonthsDeployed) * 100
```

### Test Harness

```javascript
let portfolio = lifecycleEngine.initPortfolio(clearedLoans, PARTNERS);
for (let m = 0; m < 36; m++) {
  let result = lifecycleEngine.stepMonth(portfolio, m, { defaultMultiplier: 1.0, earlyPayoffMultiplier: 1.0, recoveryMultiplier: 1.0 });
  console.log(`Month ${m}:`, result.snapshot);
}
```

**Acceptance Criteria for Stage 2:**
- [ ] `initPortfolio()` converts clearing output to stateful borrowers
- [ ] `stepMonth()` deterministically advances all borrowers by 1 month
- [ ] After 36 steps: mix of statuses (current, defaulted, paid off, early payoff)
- [ ] Hidden-prime borrowers have lower default rates than same-FICO non-hidden-prime
- [ ] Partner metrics compute correctly
- [ ] Config multipliers actually affect outcomes
- [ ] `applyIntervention()` changes partner eligibility for future months
- [ ] No console errors

---

## Stage 3: Animated Timeline (Days 7–9)

### What You're Building
- `animation_controller.js` — play/pause/resume loop, Chart.js updates
- Tab 2 UI wired to animation
- Partner intervention panel (editable while paused)

### Key Functions

```javascript
window.animationController = {
  init(portfolio, config),
  play(),
  pause(),
  resume(),
  seekTo(month),
  registerChart(chartId, chartInstance, updateFn),
  registerKPI(elementId, valueFn),
  getState()
};
```

### Animation Loop Pseudocode

```javascript
let animationInterval;
function play() {
  animationInterval = setInterval(() => {
    let result = lifecycleEngine.stepMonth(SIM.portfolio, SIM.currentMonth, SIM.config);
    SIM.snapshots.push(result.snapshot);
    SIM.currentMonth++;
    updateAllCharts(result.snapshot);
    updateAllKPIs(result.snapshot);
    document.getElementById('month-counter').textContent = SIM.currentMonth;
    if (SIM.currentMonth >= 36) pause();
  }, SIM.animationSpeed); // 500ms default
}

function pause() {
  clearInterval(animationInterval);
  SIM.playing = false;
  enablePartnerEditing();
}
```

### Chart.js Setup

**Health Chart (stacked area):**
- X: months 0–36
- Y: # of loans
- Series: Current (green), 30DPD (yellow), 60DPD (orange), 90DPD (red), Default (dark red), Paid Off (blue), Early Payoff (light blue)

**Loss Chart (line):**
- X: months 0–36
- Y: cumulative loss % per partner + overall

### Partner Intervention

When paused, partner cards show editable inputs:
- FICO floor (number input)
- Capacity (number input)
- On/off toggle

When resumed, `lifecycleEngine.applyIntervention()` updates partner config, and remaining months use new settings.

**Acceptance Criteria for Stage 3:**
- [ ] Tab 2 locked until clearing runs
- [ ] Play button starts animation
- [ ] Month counter increments each tick
- [ ] Charts update live
- [ ] Pause stops animation and enables editing
- [ ] Partner fields editable when paused
- [ ] Resume applies intervention to remaining months
- [ ] Intervention markers (vertical dashed lines) appear on charts
- [ ] Speed selector works (0.5x/1x/2x)
- [ ] Reset returns to Month 0
- [ ] All 3 scenarios produce visibly different outcomes

---

## Stage 4: Marketplace Analytics (Day 10)

### What You're Building
- Tab 3 UI with month selector
- Three-panel layout: Borrower Health, Upstart Platform, Capital Partner Health
- Traffic light indicators

### Borrower Health Panel

Render from snapshot:
- Approval rate: (approved / total) × 100
- Clearing rate: (cleared / total) × 100
- Avg APR: average offered APR
- Hidden-prime unlock: (hidden-prime cleared / total cleared) × 100
- Delinquency rate: (30+ DPD / active) × 100
- Risk grade distribution: pie or stacked bar

### Upstart Platform Panel

- Cumulative fees: (all cleared loans) × 0.03 (3% platform fee)
- BS exposure: (BS loans / total cleared) × 100
- Revenue per loan: cumulative fees / total cleared
- Model accuracy: correlation(predicted default, actual default)
- Clearing efficiency: (tier-1 matches / total cleared) × 100

### Capital Partner Panel

Per-partner cards with:
- Portfolio Yield (north star — large font, colored)
- EPD Rate (with threshold alert if >3%)
- Cumulative Loss Rate
- Utilization
- Traffic light (green/yellow/red based on thresholds)

**Acceptance Criteria for Stage 4:**
- [ ] Tab 3 locked until lifecycle runs
- [ ] Month selector populates with all completed months
- [ ] All three panels render with correct data
- [ ] Traffic lights reflect thresholds
- [ ] At-risk partners highlighted red
- [ ] Month selector updates all panels

---

## Stage 5: Loan Deep Dive (Days 11–12)

### What You're Building
- Tab 4 UI with borrower selector and 4-step walkthrough
- Persona shortcuts (Maria, Carlos, James)
- Click-through from Tab 1 results table

### Step 1: Eligibility Matrix

Table showing pass/fail for each partner:
- Partner | FICO Check | Loan Size | Purpose | Capacity | Result

### Step 2: Pricing Comparison

Side-by-side Classic vs Model 18:
- APR | P(default) | Expected Return | Partner Floor | Borrower Max APR | Result

Highlight the winner. If hidden-prime, show APR reduction callout.

### Step 3: Waterfall Routing

Vertical flow chart showing each tier:
- Tier 1: Eltura → APR check → Capacity check → MATCH/SKIP
- Tier 2: Aperture → ...
- ...
- Balance Sheet (green highlight on winner)

### Step 4: Funding + Payment History

If lifecycle ran, show payment history strip:
- One colored cell per month: green (ok), yellow (late), red (default), blue (paid off)

**Acceptance Criteria for Stage 5:**
- [ ] Borrower selector dropdown works
- [ ] Persona buttons load prebuilt borrowers (Maria FICO 650 hidden-prime, Carlos FICO 590 supply fail, James FICO 790 BS paradox)
- [ ] All 4 steps render correctly
- [ ] Click "Walk" from Tab 1 loads correct borrower
- [ ] Payment history strip shows if lifecycle has run

---

## Stage 6: Re-App Stub + Polish + Demo (Days 13–14)

### What You're Building
- Tab 5: static re-application content
- Project page update
- Scenario presets (Healthy, Capital Crunch, Rate Spike)
- Loading/empty states
- Demo script documentation

### Project Page Update

File: `code/content/projects/upstart-clearing-simulator.md`

Replace entire file with content from `PLAN_LIFECYCLE_SIMULATOR.md` — "Project Page Content" section. (Full markdown template provided there.)

### Scenario Presets

Three buttons in header:
1. **Healthy Market** — default config
2. **Capital Crunch (2022)** — tighter partner criteria, higher defaults
3. **Rate Spike** — higher APR floors, more early payoffs

Each preset updates FICO mean, default multiplier, partner configs.

### Final Checks

1. No console errors in any flow
2. All tabs work in sequence
3. Dark mode renders correctly
4. Mobile responsive (stacked layout)
5. Full demo runs in 5–7 minutes

### Demo Script (for Harsha to use)

Write markdown file: `DEMO_SCRIPT.md` (in fullstackpm.tech root)

```
## Upstart Lifecycle Simulator — Demo Script (5–7 minutes)

### (30s) Intro
"I built a lifecycle simulator for Upstart's capital marketplace. It shows how clearing decisions cascade into partner portfolio outcomes over time."

### (60s) Tab 1 — Pipeline & Clearing
- Select "Healthy Market" scenario
- Click "Generate & Clear" — point out the KPI cards (86% clearing rate, 6% BS exposure)
- Show borrower table — "This is Maria, hidden-prime, FICO 650. Model 18 found her at 16% APR. Classic FICO would've failed her."

### (90s) Tab 2 — Portfolio Timeline
- Click "Play" — watch month counter and charts evolve
- At Month 12, click "Pause" — edit Aperture's FICO floor (raise from 620 to 660)
- Click "Resume" — point out the intervention marker and changes in Aperture's metrics
- Narrate: "By tightening early, we prevent her EPD from climbing to the repurchase trigger"

### (60s) Tab 3 — Marketplace Analytics
- Switch to Tab 3 — show the three-panel dashboard
- Point to at-risk partner callout (if red): "This is the PM signal — act before it hits the trigger"

### (30s) Tab 4 — Deep Dive
- Click into Maria's full story — show the 4-step walkthrough
- "Here's the clearing decision: Layer 1 eligibility, Layer 2 pricing, Layer 3 waterfall routing"

### (30s) Tab 5 — Re-App Roadmap
- "This is a future product roadmap item. The data signals already exist."

### (30s) Close
"This is how I think about marketplace PM — making the invisible visible, trading off between stakeholders, and acting on leading indicators."
```

**Acceptance Criteria for Stage 6:**
- [ ] Tab 5 renders with rules framework
- [ ] Project page metadata updated
- [ ] All 3 scenarios work end-to-end
- [ ] No broken/empty states
- [ ] Mobile responsive
- [ ] All 5 tabs connected
- [ ] Demo runs in 5–7 minutes
- [ ] No console errors

---

## Deployment & Testing

### Local Testing

```bash
cd code
python -m uvicorn app.main:app --reload
# Visit http://localhost:8000/tools/lifecycle-simulator
```

### Pre-Demo Checklist

- [ ] Test full demo end-to-end in Chrome (target browser for interview)
- [ ] Test all 3 scenarios
- [ ] Test on same network/machine used for interview
- [ ] Verify no console errors
- [ ] Verify dark mode (if relevant to presentation environment)
- [ ] Have a backup screen recording of the demo (in case of live failures)

### Deployment

```bash
git add code/
git commit -m "Add Upstart Lifecycle Simulator — full rebuild with 5-tab interactive demo"
git push origin main
# Render auto-deploys
```

---

## Quick Links (Reference)

- **Detailed Spec:** `fullstackpm.tech/PLAN_LIFECYCLE_SIMULATOR.md`
- **Product Context:** `interview-prep/15_Simulator_PRFAQ.md`, `16_Simulator_PRD.md`, `17_Simulator_BRD.md`
- **Old Simulator:** `code/app/static/tools/upstart_clearing_simulator.html` (extraction source)
- **Borrower Generator:** `code/app/static/tools/borrower_generation.js` (reuse, don't modify)

---

## Questions?

Ask Harsha. This document and the spec files should cover everything, but:
- Data structure ambiguity → check `PLAN_LIFECYCLE_SIMULATOR.md`
- Product intent → check PRFAQ / PRD
- Business context → check BRD
- Demo narrative → check demo script section above

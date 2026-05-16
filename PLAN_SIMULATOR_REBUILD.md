# Plan: Rebuild Upstart Clearing Simulator

## Context

The user said "it is really not working" after reviewing the live tool at `/tools/upstart-clearing-simulator`. After reading all ~1,824 lines of HTML/JS plus borrower_generation.js and the project content page, here's the full diagnosis:

**The JS logic itself is correct.** The real problems are structural UX gaps that make the tool feel disconnected and fail to tell a compelling interview story.

---

## Diagnosis: What's Actually Broken

### Critical Gap: Simulator and Walkthrough are completely disconnected
- You run 500 loans through the simulator → see aggregate charts
- You go to Loan Walkthrough → start fresh with a new blank borrower OR pick a persona
- There is **no way to drill into a specific borrower from the simulation results**
- This breaks the core demo narrative: "here's a pool of 500 loans, click Maria to watch her clear"

### Simulator shows no individual loan data
- Results panel: 4 KPI cards + 3 charts (waterfall doughnut, utilization bar, scatter)
- **No table of individual loans** — you can't see which loans cleared, which failed, or why
- The scatter chart shows FICO vs APR dots but you can't click them

### `capPass = true` hardcoded in Walkthrough (line 1714)
- Every loan in the walkthrough shows "Capacity: ✅ available" — always
- Partners never run out of capacity in the walkthrough, even though this is one of the key dynamics in the simulator
- Makes the walkthrough feel fake and simplistic

### 7 tabs is too many, layout confusing
- Tab buttons show: Simulator → Loan Walkthrough → Borrower Journey → Capital Partner → Bank Partner → Clearing Engine → Assumptions
- But `tab-walkthrough` HTML div is at line 1061 (after Bank Partner and Clearing Engine in the HTML)
- Borrower Journey, Capital Partner Journey, and Bank Partner Journey are 3 separate tabs with similar patterns — overwhelming

### Project page metadata is wrong (`upstart-clearing-simulator.md`)
- Claims tech stack: `[FastAPI, Python, Pandas, Interactive Tables, HTMX, Tailwind CSS]`
- Actual tech: vanilla JS + Chart.js + CSS variables + borrower_generation.js + FastAPI for routing
- No HTMX, no Tailwind, no Pandas used anywhere in the tool

### PLAN_IMPROVE_DATA_METHODS.md never executed
- Data & Methods page has no "Generate Dataset" button
- Case Studies tab has thin 4-line text boxes, not detailed breakdowns

---

## Proposed Rebuild

### What NOT to rebuild
The following is working well and should stay unchanged:
- `borrower_generation.js` — clean, correct
- `clearLoans()` and `makeBorrowers()` — correct waterfall logic
- KPI rendering and Chart.js charts — good
- The 4-step walkthrough structure (eligibility → pricing → routing → funded) — correct and educational
- Personas (Maria, Carlos, James, Priya, Devon) — compelling stories
- Clearing Engine tab and Assumptions tab — high quality, keep as-is

### Phase 1: Add Borrower Results Table to Simulator Tab

**File:** `code/app/static/tools/upstart_clearing_simulator.html`

After the scatter chart, add a `div#borrower-results` section with a sortable/filterable table:

```html
<!-- Below scatter chart in res-panel -->
<div class="sc-card" id="borrower-results-card" style="display:none">
  <div class="ch-ttl">Individual Loan Results</div>
  <div class="ch-sub">Click any row to walk through that loan step-by-step →</div>
  <div style="display:flex;gap:8px;margin-bottom:10px">
    <button class="filter-btn active" onclick="filterResults('all',this)">All</button>
    <button class="filter-btn" onclick="filterResults('cleared',this)">Cleared</button>
    <button class="filter-btn" onclick="filterResults('apr_high',this)">APR Rejected</button>
    <button class="filter-btn" onclick="filterResults('no_partner',this)">No Partner</button>
  </div>
  <div id="borrower-table-wrap" style="overflow-x:auto;max-height:340px;overflow-y:auto">
    <table id="borrower-table" class="results-table">
      <thead>
        <tr>
          <th>#</th><th>FICO</th><th>Amount</th><th>Purpose</th>
          <th>HP</th><th>APR</th><th>Outcome</th><th>Partner</th><th></th>
        </tr>
      </thead>
      <tbody id="borrower-table-body"></tbody>
    </table>
  </div>
  <div style="font-size:11px;color:var(--muted);margin-top:8px" id="borrower-table-count"></div>
</div>
```

Add rendering function `renderBorrowerTable(r)`:
- Shows top 100 loans by default (most interesting: cleared near-prime + failed ones)
- Each row has "🔬 Walk" button that calls `initWalkthroughFromSim(loan)`
- Row color: green for cleared, red for apr_high, gray for no_partner
- HP column shows "★" for hidden-prime borrowers
- Clicking row opens Loan Walkthrough tab with that borrower pre-loaded
- Filter buttons to show only cleared/failed/no-partner

Call `renderBorrowerTable(res)` at end of `runSim()`.

### Phase 2: Connect Walkthrough to Simulator

**New function:** `initWalkthroughFromSim(loan)`

```javascript
function initWalkthroughFromSim(loan) {
  // Pre-populate walkthrough from a loan that already ran through clearLoans()
  wt.fico = loan.fico;
  wt.amount = loan.amount;
  wt.purpose = loan.purpose;
  wt.stateCap = 'Favorable';
  wt.hiddenPrime = loan.hiddenPrime || loan.hp || false;
  wt.personaId = null;
  wt.fromSim = true;  // flag to show "from simulation run" context
  wt.simOutcome = loan.outcome;     // 'CLEARED', 'APR_TOO_HIGH', 'NO_ELIGIBLE_PARTNER'
  wt.simPartner = loan.matchedPartner;
  wt.simOfferedAPR = loan.offered;
  wt.step = 1;
  wt.eligiblePartners = [];
  wt.clearingAPR = null;
  wt.matchedPartner = null;
  wt.pricing = null;
  document.getElementById('wt-log').innerHTML = '';
  showTab('walkthrough', document.querySelector('[data-tab="walkthrough"]'));
  renderWalkthrough();
}
```

When `wt.fromSim` is true, add a callout at top of Step 1:
```
📊 From your simulation run: This borrower [CLEARED at X% APR via Eltura] / [FAILED: APR too high]
Walk through the steps to see why.
```

**Fix `capPass` in `evalEligibility`** (line 1576):
Replace `const capPass = true;` with logic that tracks a "snapshot" of remaining capacity based on the current simulation's `alloc` data. Pass `remainingCaps` as an optional parameter to `evalEligibility`, defaulting to `{each partner: their full cap}` if not provided.

For walkthrough from sim: use the actual remaining caps at the time that specific borrower was processed. For custom/persona walkthroughs: show full capacity (or show "Simplified: capacity assumed available" note).

### Phase 3: Consolidate Tabs (7 → 5)

**Merge** Borrower Journey + Capital Partner Journey + Bank Partner Journey into single "Market Participants" tab with internal subtabs or anchor scrolling.

New tab order:
1. ⚙ Simulator
2. 🔬 Loan Walkthrough
3. 👥 Market Participants (merged — Borrower, Capital Partner, Bank Partner)
4. ⚡ Clearing Engine
5. 📋 Assumptions & Notes

Remove 2 tabs (Capital Partner, Bank Partner become sections inside Market Participants).

The Market Participants tab has 3 internal buttons:
- Borrower Journey
- Capital Partner Journey
- Bank Partner Journey

Each shows on click (same pattern as outer tabs). This reduces top-level cognitive load while preserving all content.

### Phase 4: Execute PLAN_IMPROVE_DATA_METHODS.md

**File:** `code/app/static/tools/upstart_data_methods.html`

1. **Add "Generate Dataset" button** to Data Generation tab:
   - After the FICO slider section, add: `<button onclick="generateDataset()">▶ Generate Dataset</button>`
   - `generateDataset()` calls `borrowerGeneration.generateBorrowerFull(N, currentFICO, 0.28)` and re-renders the Sample Dataset table
   - KPI cards (avg FICO, % hidden prime, avg APR) update when new dataset generates

2. **Expand Case Studies** (Maria, Carlos, James sections in Case Studies tab):
   - Each gets the same 4-layer breakdown format: Eligibility → Pricing → Routing → Funded
   - Use color-coded cards matching the walkthrough's visual language
   - Show side-by-side Classic vs AI for Maria and Devon

### Phase 5: Fix Project Page Metadata

**File:** `code/content/projects/upstart-clearing-simulator.md`

Change tech_stack line 4:
```
tech_stack: [Vanilla JS, Chart.js, CSS Variables, FastAPI, borrower_generation.js]
```

Update "How" section backend description to accurately reflect that the logic is all client-side JS, FastAPI only serves the static file.

---

## Files to Modify

| File | Changes |
|------|---------|
| `code/app/static/tools/upstart_clearing_simulator.html` | Borrower table, walkthrough connection, tab consolidation, capPass fix |
| `code/app/static/tools/upstart_data_methods.html` | Generate Dataset button, expanded case studies |
| `code/content/projects/upstart-clearing-simulator.md` | Tech stack + How section accuracy fix |

**No new files needed.** `borrower_generation.js` and `pages.py` are correct as-is.

---

## Key Demo Narrative After Rebuild

*"Let me run 500 borrowers through the clearing engine. See — 84% clearing rate, 6% balance sheet exposure, healthy. Now watch this: I'll find a near-prime borrower who's hidden-prime [clicks row in table] — FICO 653, hidden prime flag, failed classic but Model 18 cleared her at 22% APR. Click Walk Through → [walkthrough opens] — here's Layer 1, she passes 3 of 5 partners. Layer 2, classic says FAIL, Model 18 unlocks her. Layer 3, Eltura catches her because their forward-flow agreement targets exactly this segment. This is the Upstart flywheel — the mechanism is transparent, reproducible, and the math is correct."*

---

## Verification

1. Run simulator → see borrower table appear below charts
2. Click "Cleared" filter → shows only funded loans
3. Click "🔬 Walk" on a hidden-prime borrower → switches to Loan Walkthrough tab with pre-loaded borrower
4. Walk through steps 1-4; Step 1 shows the correct callout "from simulation run: CLEARED at X% via Eltura"
5. Load "Capital Crunch" scenario → same flow, some loans now show NO_ELIGIBLE_PARTNER
6. On Data & Methods: move FICO slider → click Generate Dataset → table updates with new 25 borrowers
7. Check project page at /resources/product-breakdowns → tech stack shows correct tools
8. Tab count: 5 (not 7); Clearing Engine and Assumptions still present

# Plan: Unify Borrower Generation Across Simulator & Data & Methods

## Overview

Currently, the simulator (`makeBorrowers()`) and Data & Methods (`generateBorrowers()`) generate borrowers separately, even though they use identical distributions. This creates a credibility gap during interviews: *"Are these the same borrowers or different populations?"*

**Goal:** Create a single, shared `borrowerGeneration.js` module that both pages include, ensuring all borrowers are generated identically with full feature transparency.

---

## Architecture Change

### Current State (Two Independent Systems)

```
Simulator (makeBorrowers)
  → generates minimal: {fico, amount, hp, maxAPR}
  → no purpose, income, risk score, etc.

Data & Methods (generateBorrowers)
  → generates rich: {fico, amount, purpose, income, risk, p_default, clearing_apr, outcome}
  → uses same math but separate code
```

### New State (Unified Pipeline)

```
Shared Borrower Generation Module (borrowerGeneration.js)
  ↓
  generateBorrowerFull(n, creditQuality, hiddenPrimeRate)
    → returns rich borrower objects with ALL fields

Simulator imports this
  → calls generateBorrowerFull()
  → displays only needed fields (FICO, amount, cleared/failed, partner, APR)
  → has access to hidden fields for debugging/export

Data & Methods imports this
  → calls generateBorrowerFull()
  → displays all fields in table + exports JSON/CSV

Both can export/import same format
```

---

## Implementation Plan

### Step 1: Create Shared Module

**New file:** `code/app/static/tools/borrower_generation.js`

Contains:
```js
// ========== MATH FUNCTIONS (reuse from simulator) ==========
function gauss(m, s) { /* Box-Muller */ }
function lognorm(m, s) { /* LogNormal */ }
function clamp(v, a, b) { /* Range clamp */ }

// ========== RISK & PRICING FUNCTIONS ==========
function classicAPR(fico) { /* FICO → APR lookup */ }
function borrowerMaxAPR(fico, sensitivity, hp) { /* Demand elasticity */ }
function calculateRiskScore(fico, hp) { /* Normalized 0-1 */ }
function calculatePDefault(fico, hp) { /* P(default) */ }

// ========== PURPOSE SELECTION ==========
function choosePurpose(seed) {
  // Deterministic based on borrower index
  // Ensures same borrower gets same purpose across runs
  const purposes = ['Debt Consolidation', 'Emergency/Medical', 'Home Improvement', 'Auto Refinance'];
  return purposes[seed % purposes.length];
}

// ========== INCOME ESTIMATION ==========
function estimateIncome(fico, loanAmount, hiddenPrime) {
  // Derived from FICO + loan amount + hidden-prime signal
  // Higher FICO + larger loan → higher income estimate
  const baseIncome = (fico - 500) * 850 + gauss(22000, 12000);
  const loanAdjustment = loanAmount * 2.2;
  return clamp(baseIncome + loanAdjustment, 30000, 180000);
}

// ========== MAIN BORROWER GENERATION ==========
function generateBorrowerFull(n = 25, creditQuality = 667, hiddenPrimeRate = 0.28) {
  const borrowers = [];

  for (let i = 1; i <= n; i++) {
    // Raw generation (identical to simulator)
    const fico = Math.round(clamp(gauss(creditQuality, 65), 520, 820));
    const amount = Math.round(clamp(lognorm(12000, 0.45), 2000, 45000) / 100) * 100);

    // Derived fields (enrichment)
    const purpose = choosePurpose(i);
    const hp = fico >= 580 && fico <= 720 && Math.random() < hiddenPrimeRate;
    const income = estimateIncome(fico, amount, hp);
    const riskScore = calculateRiskScore(fico, hp);
    const pDefault = calculatePDefault(fico, hp);

    // APR calculation (both models)
    const classicApr = classicAPR(fico);
    const aiApr = hp ? clamp(classicApr - clamp(gauss(8.5, 1.5), 5, 12), 9, 40) : classicApr;
    const maxApr = borrowerMaxAPR(fico, 2, hp);
    const clearingApr = aiApr <= maxApr ? Number(aiApr.toFixed(1)) : null;

    // Full borrower object
    const borrower = {
      id: i,
      fico,
      amount,
      purpose,
      income,
      hiddenPrime: hp,
      riskScore: Number(riskScore.toFixed(3)),
      pDefault: Number(pDefault.toFixed(3)),
      clearingApr,
      classicApr: Number(classicApr.toFixed(1)),
      aiApr: Number(aiApr.toFixed(1)),
      maxApr: Number(maxApr.toFixed(1)),
      outcome: null,  // populated by simulator after clearing
      matchedPartner: null  // populated by simulator after routing
    };

    borrowers.push(borrower);
  }

  return borrowers;
}

// ========== EXPORT/IMPORT ==========
function exportDataset(borrowers, format = 'json') {
  if (format === 'json') {
    return JSON.stringify({
      metadata: {
        generated_date: new Date().toISOString(),
        sample_size: borrowers.length,
        parameters: {
          avg_fico: Math.round(borrowers.reduce((s, b) => s + b.fico, 0) / borrowers.length),
          hidden_prime_rate: borrowers.filter(b => b.hiddenPrime).length / borrowers.length,
          distribution_type: 'Box-Muller Gaussian (FICO), LogNormal (loan amount)'
        }
      },
      borrowers
    }, null, 2);
  } else if (format === 'csv') {
    const headers = ['ID', 'FICO', 'Income', 'Loan Amount', 'Purpose', 'Hidden Prime', 'Risk Score', 'P(Default)', 'Classic APR', 'AI APR', 'Max APR', 'Clearing APR', 'Outcome', 'Partner'];
    const rows = borrowers.map(b => [
      b.id,
      b.fico,
      `$${b.income}`,
      `$${b.amount}`,
      b.purpose,
      b.hiddenPrime ? 'Yes' : 'No',
      b.riskScore.toFixed(3),
      `${(b.pDefault * 100).toFixed(2)}%`,
      `${b.classicApr}%`,
      `${b.aiApr}%`,
      `${b.maxApr}%`,
      b.clearingApr ? `${b.clearingApr}%` : 'Failed',
      b.outcome || 'Pending',
      b.matchedPartner || 'N/A'
    ]);
    return [headers, ...rows].map(r => r.join(',')).join('\n');
  }
}

function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

// Export functions for use in both pages
window.borrowerGeneration = {
  generateBorrowerFull,
  exportDataset,
  downloadFile
};
```

---

### Step 2: Update Simulator

**File:** `code/app/static/tools/upstart_clearing_simulator.html`

**Changes:**

1. **Add script tag in `<head>`:**
```html
<script src="borrower_generation.js"></script>
```

2. **Replace `makeBorrowers()` with unified call:**

Old:
```js
function makeBorrowers(n, cq, sens) {
  return Array.from({length:n}, (_,i) => {
    const f = Math.round(clamp(gauss(cq,65),520,820));
    const hp = f<720 && Math.random()<0.28;
    const amt = Math.round(clamp(lognorm(12000,0.45),2000,45000)/100)*100;
    return {id:i, fico:f, amount:amt, hp, maxAPR:borrowerMaxAPR(f,sens,hp)};
  });
}
```

New:
```js
function makeBorrowers(n, cq, sens) {
  // Use shared generation from borrower_generation.js
  const borrowers = borrowerGeneration.generateBorrowerFull(n, cq, 0.28);
  // Add simulator-specific field (sensitivity affects demand elasticity)
  return borrowers.map(b => ({
    ...b,
    maxAPR: borrowerMaxAPR(b.fico, sens, b.hiddenPrime)
  }));
}
```

3. **Update `clearLoans()` to populate outcome + matchedPartner:**

After a loan is routed, set:
```js
borrower.outcome = status; // 'CLEARED', 'NO_ELIGIBLE_PARTNER', 'APR_TOO_HIGH'
borrower.matchedPartner = partnerName; // 'Eltura', 'Balance Sheet', etc.
```

4. **Add export button to Simulator tab:**

After scenario results KPIs, add:
```html
<button onclick="exportSimulatorRun()">📥 Export Dataset (JSON/CSV)</button>
```

JS function:
```js
function exportSimulatorRun() {
  const format = confirm('Export as JSON (OK) or CSV (Cancel)?') ? 'json' : 'csv';
  const content = borrowerGeneration.exportDataset(sim.borrowers, format);
  const ext = format === 'json' ? 'json' : 'csv';
  borrowerGeneration.downloadFile(
    content,
    `upstart_clearing_run_${new Date().toISOString().split('T')[0]}.${ext}`,
    `text/${ext}`
  );
}
```

---

### Step 3: Update Data & Methods

**File:** `code/app/static/tools/upstart_data_methods.html`

**Changes:**

1. **Add script tag in `<head>`:**
```html
<script src="borrower_generation.js"></script>
```

2. **Replace `generateBorrowers()` with unified call:**

Old: Custom implementation
New:
```js
const DATASET = borrowerGeneration.generateBorrowerFull(25, 667, 0.28);
```

3. **Keep the table rendering the same** (it already displays all the fields)

4. **Export buttons still work:** They call `borrowerGeneration.exportDataset(DATASET, format)`

---

### Step 4: Add Cross-Reference Callouts

**In Simulator tab (top callout):**

Update existing callout:
```html
<div class="callout-warning">
  <b>📊 Unified Borrower Generation:</b> Both the simulator and Data & Methods page
  use identical borrower generation (Box-Muller FICO: N(μ=660, σ=65), LogNormal loans: LN(μ=$12K, σ=0.45), 28% hidden-prime rate).
  You can export a simulator run and compare it side-by-side with the
  <a href="/tools/upstart-data-methods">methodology page →</a>
</div>
```

**In Data & Methods header:**

Add after title:
```html
<p style="color:var(--muted);font-size:13px;">
  These 25 borrowers use the exact same generation algorithm as the
  <a href="/tools/upstart-clearing-simulator">simulator</a>.
  Download this dataset and load it into the simulator to see real-time clearing.
</p>
```

---

### Step 5: Add "Load Dataset" Feature (Optional Enhancement)

If you want the simulator to let users load a JSON dataset (e.g., the sample from Data & Methods):

```html
<!-- In Simulator tab controls -->
<div class="ctrl-sec">
  <div class="sec-ttl">Dataset</div>
  <input type="file" id="dataset-upload" accept=".json" onchange="loadDataset(event)">
  <button onclick="loadSampleDataset()">📊 Load Sample (25 borrowers)</button>
</div>
```

JS:
```js
function loadSampleDataset() {
  const borrowers = borrowerGeneration.generateBorrowerFull(25, 667, 0.28);
  sim.borrowers = borrowers;
  document.getElementById('sl-vol').value = 25;
  document.getElementById('lbl-vol').textContent = '25 loans';
  runSim();
}

function loadDataset(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = (e) => {
    const json = JSON.parse(e.target.result);
    sim.borrowers = json.borrowers || [];
    document.getElementById('sl-vol').value = sim.borrowers.length;
    document.getElementById('lbl-vol').textContent = sim.borrowers.length + ' loans';
    runSim();
  };
  reader.readAsText(file);
}
```

This lets users: *"Export the sample dataset from Data & Methods, then load it into the simulator to see it clear in real-time."* Very powerful for interviews.

---

## File Structure After Changes

```
code/app/static/tools/
├── borrower_generation.js (NEW - shared module, ~150 lines)
├── upstart_clearing_simulator.html (UPDATED - include script, use shared functions, add export)
└── upstart_data_methods.html (UPDATED - include script, use shared generation, add callout)
```

---

## Interview Narrative

*"Both the simulator and the methodology page use identical borrower generation. You can see the 25 examples on the Data & Methods page, export them as JSON, then load them into the simulator to watch them clear in real-time. The math is consistent across both tools — same Box-Muller distribution for FICO, same LogNormal for loan amounts, same hidden-prime detection, same risk model. This ensures transparency: you can verify the simulator is doing what the methodology claims it does."*

---

## Testing Checklist

- [ ] Simulator generates borrowers using shared module
- [ ] Data & Methods uses shared module for 25 borrowers
- [ ] Export JSON from simulator → file is valid, contains all borrower fields
- [ ] Export CSV from simulator → file opens in Excel, all columns present
- [ ] Load sample dataset button populates simulator with 25 borrowers
- [ ] Callouts in both pages link correctly
- [ ] Borrower fields match between simulator export and Data & Methods table
- [ ] Hidden-prime rate ~28% in both (verify across multiple runs)

---

## Token Estimate

- New `borrower_generation.js`: ~200 lines
- Simulator updates: ~50 lines (use shared module, add export button/function)
- Data & Methods updates: ~20 lines (use shared module, add callouts)
- Total: ~270 lines of changes

**File sizes after:**
- `borrower_generation.js`: ~5 KB
- `upstart_clearing_simulator.html`: ~111 KB (slight increase)
- `upstart_data_methods.html`: ~25 KB (slight decrease, uses shared module)

All well within bounds. No external dependencies.

---

## Code Puppy Execution

Ready to build this? Steps:

1. Create `borrower_generation.js` with all math functions + `generateBorrowerFull()`
2. Update simulator to include script, use shared functions, add export button
3. Update Data & Methods to include script, use shared functions, add callouts
4. Test local: run simulator, export dataset, compare with Data & Methods table
5. Commit & push → Render deploys


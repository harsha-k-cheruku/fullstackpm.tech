# Plan: Improve Data & Methods Page UX

## Overview

Two UX gaps in `upstart_data_methods.html`:

1. **Data Generation tab:** FICO slider only visualizes—doesn't regenerate dataset. Users expect: adjust slider → click "Generate" → get new 25 borrowers with that FICO mean.

2. **Case Studies tab:** 3 ultra-condensed text boxes (4 lines each). Need detailed layer-by-layer breakdowns matching simulator's Clearing Engine tab quality.

---

## Change 1: Add "Generate Dataset" Button to Data Generation Tab

### Location
After the "Hidden-Prime Discovery" KPI cards (after line 128 in current file).

### New Section HTML

```html
<div class="dm-card">
  <h3>Generate Custom Dataset</h3>
  <p>Use the FICO slider above to adjust the average credit quality, then regenerate the sample dataset:</p>
  <div style="display: flex; gap: 10px; margin-top: 12px;">
    <input type="range" id="customFicoInput" min="620" max="740" value="667" step="1"
           style="flex: 1;" onchange="updateCustomFicoLabel(+this.value)">
    <span id="customFicoLabel" style="font-weight: 700; color: var(--blue); min-width: 60px;">FICO 667</span>
  </div>
  <button id="generateBtn" onclick="regenerateDataset()"
          style="margin-top: 12px; background: var(--blue); color: #fff; border: none; padding: 10px 16px; border-radius: 6px; font-weight: 700; cursor: pointer; width: 100%;">
    🔄 Generate New Dataset (25 borrowers)
  </button>
  <p style="font-size: 12px; color: var(--muted); margin-top: 8px;">
    <b>Hidden-prime rate:</b> Fixed at 28% (realistic rate for near-prime segments)
  </p>
</div>
```

### JavaScript Functions

Add these after the existing `generateBorrowers()` function:

```js
function updateCustomFicoLabel(ficoValue) {
  document.getElementById('customFicoLabel').textContent = 'FICO ' + ficoValue;
}

function regenerateDataset() {
  const ficoMean = parseInt(document.getElementById('customFicoInput').value);
  console.log(`[Data & Methods] Regenerating dataset with FICO mean = ${ficoMean}`);

  // Generate new borrowers with custom FICO mean
  DATASET = generateBorrowers(25, ficoMean, 0.28);

  // Update Sample Dataset tab
  renderDatasetTable(DATASET);

  // Update Sample Dataset KPIs
  const avgFico = Math.round(DATASET.reduce((s, b) => s + b.fico, 0) / DATASET.length);
  const hpRate = (DATASET.filter(b => b.hidden_prime).length / DATASET.length * 100).toFixed(0);
  document.getElementById('kpiFico').textContent = avgFico;
  document.getElementById('kpiHp').textContent = hpRate + '%';

  // Switch to Sample Dataset tab to show results
  document.querySelector('[onclick="showTab(\'dataset\', this)"]').click();

  // Scroll to top of page
  window.scrollTo(0, 0);
}
```

### UX Flow

1. User adjusts FICO slider in Data Generation tab → slider label updates live
2. User clicks "🔄 Generate New Dataset" button
3. Page generates 25 new borrowers with that FICO mean
4. Auto-switches to Sample Dataset tab
5. New borrowers display in table + KPI cards update (avg FICO, hidden-prime %)
6. User can export the custom dataset as JSON/CSV

---

## Change 2: Expand Case Studies Tab

### Current State (Too Condensed)

```
Case Study 1: Maria — Hidden-Prime Discovery
  Borrower Profile: FICO 650, Income $78K, Loan $14K, Debt Consolidation, hidden-prime ON.
  Layer 1 (Eligibility): Eligible partners: Eltura, Aperture. WestBank+ spots fail FICO floors.
  Layer 2 (Pricing): Classic ≈ 23.5%; Model 18 lowers APR materially...
  Layer 3 (Routing): Waterfall checks partner APR floors...
```

### New Structure (Detailed & Scannable)

For **each case study**, use this template:

```html
<div class="case-study">
  <h3>Case Study N: [Name] — [Outcome Title]</h3>

  <!-- Borrower Profile Card -->
  <div class="case-box">
    <h4>📋 Borrower Profile</h4>
    <table style="width: 100%; font-size: 12px; margin-top: 8px;">
      <tr><td><b>Name:</b></td><td>[Name]</td></tr>
      <tr><td><b>FICO:</b></td><td>[FICO]</td></tr>
      <tr><td><b>Income:</b></td><td>[Income]</td></tr>
      <tr><td><b>Loan Amount:</b></td><td>[Amount]</td></tr>
      <tr><td><b>Purpose:</b></td><td>[Purpose]</td></tr>
      <tr><td><b>Hidden-Prime Signal:</b></td><td>[Y/N]</td></tr>
      <tr><td><b>State APR Cap:</b></td><td>[Favorable/Moderate/Restrictive]</td></tr>
    </table>
  </div>

  <!-- Layer 1: Eligibility Matrix -->
  <div class="case-box">
    <h4>Layer 1: Eligibility Matrix</h4>
    <p style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">Binary rules: FICO floor, loan size, purpose, capacity.</p>
    <table style="width: 100%; font-size: 11px; border-collapse: collapse;">
      <tr style="border-bottom: 1px solid var(--border);">
        <th style="text-align: left; padding: 4px;">Partner</th>
        <th style="text-align: left; padding: 4px;">FICO Floor</th>
        <th style="text-align: left; padding: 4px;">Loan Size</th>
        <th style="text-align: left; padding: 4px;">Purpose</th>
        <th style="text-align: left; padding: 4px;">Result</th>
      </tr>
      <!-- 5 partner rows here -->
      <tr style="border-bottom: 1px solid var(--border);">
        <td style="padding: 4px;">Eltura</td>
        <td style="padding: 4px;">650 ≥ 620? ✅</td>
        <td style="padding: 4px;">$14K OK? ✅</td>
        <td style="padding: 4px;">DC OK? ✅</td>
        <td style="padding: 4px; color: #065f46; font-weight: 700;">ELIGIBLE</td>
      </tr>
      <!-- ... repeat for other partners ... -->
    </table>
    <p style="font-size: 12px; margin-top: 8px; color: var(--muted);"><b>Outcome:</b> [X of 5 eligible / 0 eligible → fails]</p>
  </div>

  <!-- Layer 2: Pricing Engine (if applicable) -->
  <div class="case-box">
    <h4>Layer 2: Pricing Engine — APR as a Feature</h4>
    <p style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">Find lowest APR where both sides agree: partner return floor met AND borrower accepts.</p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
      <div style="background: #f1f5f9; padding: 10px; border-radius: 6px;">
        <h5 style="font-size: 12px; margin-bottom: 6px;">📊 Classic FICO</h5>
        <div style="font-size: 11px; line-height: 1.6;">
          <div><b>APR:</b> 23.5%</div>
          <div><b>P(default):</b> 8.9%</div>
          <div><b>Expected return:</b> 14.1%</div>
          <div><b>Partner floor (≥8%):</b> ✅ PASS</div>
          <div><b>Borrower max APR:</b> 24.0%</div>
          <div style="margin-top: 6px; padding: 6px; background: #fee2e2; border-radius: 4px; color: #991b1b; font-weight: 700;">
            ❌ FAILS: Borrower rejects (23.5% ≤ 24% but at upper limit)
          </div>
        </div>
      </div>
      <div style="background: #f0fdf4; padding: 10px; border-radius: 6px; border: 2px solid var(--blue);">
        <h5 style="font-size: 12px; margin-bottom: 6px;">🤖 Model 18 (APR-as-Feature)</h5>
        <div style="font-size: 11px; line-height: 1.6;">
          <div><b>APR Reduction:</b> 8.2% (hidden-prime)</div>
          <div><b>APR:</b> 23.5% − 8.2% = <b style="color: var(--green);">15.3%</b></div>
          <div><b>P(default):</b> 6.8% ↓ (lower payment)</div>
          <div><b>Expected return:</b> 12.8%</div>
          <div><b>Partner floor:</b> ✅ PASS</div>
          <div><b>Borrower max APR:</b> 24.0%</div>
          <div style="margin-top: 6px; padding: 6px; background: #d1fae5; border-radius: 4px; color: #065f46; font-weight: 700;">
            ✅ CLEARS at 15.3% APR
          </div>
        </div>
      </div>
    </div>
    <p style="font-size: 12px; margin-top: 8px; background: var(--blue-l); padding: 8px; border-radius: 4px; border-left: 3px solid var(--blue); color: #1e40af;">
      <b>🎯 Key Insight:</b> [Insight specific to this case]
    </p>
  </div>

  <!-- Layer 3: Waterfall Routing (if applicable) -->
  <div class="case-box">
    <h4>Layer 3: Waterfall Routing</h4>
    <p style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">Clearing APR: <b style="color: var(--blue);">15.3%</b></p>
    <div style="font-size: 11px; line-height: 1.8;">
      <div style="display: flex; gap: 8px; margin-bottom: 6px;">
        <div style="flex: 0 0 40px;"><b>Tier 1:</b></div>
        <div style="flex: 1;">
          <b>Eltura</b> (forward-flow, priority 1)
          <div style="color: var(--muted); font-size: 10px; margin-top: 2px;">
            APR check: 15.3% ≥ minAPR 15.5%? ❌ APR too low (just barely!)
          </div>
          <div style="color: var(--muted); font-size: 10px;">→ SKIP to next tier</div>
        </div>
      </div>
      <div style="display: flex; gap: 8px; margin-bottom: 6px;">
        <div style="flex: 0 0 40px;"><b>Tier 2:</b></div>
        <div style="flex: 1;">
          <b>Aperture</b> (forward-flow, priority 2)
          <div style="color: var(--muted); font-size: 10px; margin-top: 2px;">
            APR check: 15.3% ≥ minAPR 16.0%? ❌ APR too low
          </div>
          <div style="color: var(--muted); font-size: 10px;">→ SKIP to next tier</div>
        </div>
      </div>
      <div style="display: flex; gap: 8px; background: #d1fae5; padding: 8px; border-radius: 4px; border-left: 3px solid var(--green);">
        <div style="flex: 0 0 40px;"><b>Tier 3:</b></div>
        <div style="flex: 1;">
          <b>WestBank</b> (bank program, priority 3)
          <div style="color: var(--muted); font-size: 10px; margin-top: 2px;">
            APR check: 15.3% ≥ minAPR 13.0%? ✅ Meets return floor
          </div>
          <div style="color: var(--muted); font-size: 10px;">Capacity: ✅ Available</div>
          <div style="color: var(--green); font-weight: 700; font-size: 11px; margin-top: 4px;">→ MATCHED to WestBank</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Post-Clearance & PM Insight -->
  <div class="case-box">
    <h4>✅ Outcome & PM Insight</h4>
    <div style="font-size: 12px; line-height: 1.6;">
      <p><b>Final Status:</b> ✅ CLEARED to WestBank at 15.3% APR</p>
      <p style="margin-top: 8px; color: var(--muted);"><b>Data Flywheel:</b> Loan funded → Bank disburses $14K → Loan sold to WestBank → Upstart earns $420 platform fee (3%) → EPD monitoring starts → Outcome feeds back into Model 18 retraining in 30–90 days.</p>
      <p style="margin-top: 8px; background: var(--blue-l); padding: 8px; border-radius: 4px; border-left: 3px solid var(--blue); color: #1e40af;">
        <b>🔍 Why This Matters:</b> [PM-level takeaway specific to this case]
      </p>
    </div>
  </div>
</div>
```

### Three Case Study Variants

#### Case Study 1: Maria (Hidden-Prime Win)
- **Outcome Title:** "Hidden-Prime Discovery"
- **Intro:** FICO 650, hidden-prime ON
- **Layer 1:** Both Eltura and Aperture eligible
- **Layer 2:** Classic fails (APR 23.5%, borrower rejects); AI passes (APR 15.3%, both sides accept)
- **Layer 3:** Matches to WestBank (Eltura/Aperture APR floors too high)
- **Insight:** "Maria is creditworthy by Plaid signals but FICO underestimates her. Model 18 unlocks a loan she'd otherwise be denied."

#### Case Study 2: Carlos (Supply Failure)
- **Outcome Title:** "Supply-Side Failure"
- **Intro:** FICO 590, Small Business purpose
- **Layer 1:** All 5 partners fail (Small Business not supported) → **LOAN FAILS HERE**
- **Layer 2:** Skipped (no eligible partners)
- **Layer 3:** Skipped
- **Insight:** "Carlos is creditworthy by income, but the marketplace has no inventory for SMB lending. This is a product gap, not a borrower quality issue. PM fix: onboard a partner with SMB eligibility."

#### Case Study 3: James (Balance Sheet Paradox)
- **Outcome Title:** "Too Good to Clear (Balance Sheet Paradox)"
- **Intro:** FICO 790, clean approval
- **Layer 1:** All 5 partners eligible (highest FICO tier)
- **Layer 2:** Both models produce low APR (10.5%) because risk is already low
- **Layer 3:** ALL partner APR floors fail (Eltura min 15.5%, SpotFund B min 19.0%, etc.) → Falls to Balance Sheet
- **Insight:** "James is so creditworthy that his APR is below all partner return floors. Upstart funds him from balance sheet. This is why Upstart's balance sheet exposure spiked in 2021–2022: near-zero-rate capital + rising rates = mandatory balance sheet holdings."

---

## CSS Classes Needed

Add these to `<style>` if not present:

```css
.case-study h4 { font-size: 13px; font-weight: 700; margin-bottom: 8px; }
.case-box table { width: 100%; font-size: 11px; border-collapse: collapse; }
.case-box table tr { border-bottom: 1px solid var(--border); }
.case-box table th, .case-box table td { padding: 6px 4px; text-align: left; }
```

---

## Summary of Changes

| Component | Change | Impact |
|-----------|--------|--------|
| **Data Generation Tab** | Add "Generate Dataset" button + FICO slider input | Users can create custom datasets with different credit quality means |
| **Case Studies Tab** | Expand from 4-line text to detailed 4-layer breakdowns | Crystal-clear how borrowers flow through clearing engine |
| **Sample Dataset Tab** | KPI cards update when dataset regenerates | Dynamic feedback when user generates new data |

---

## User Experience Flow

### New Workflow: Custom Data Generation

1. Open Data & Methods → Data Generation tab
2. Adjust FICO slider to 700 (want higher credit quality borrowers)
3. Click "🔄 Generate New Dataset"
4. Page auto-switches to Sample Dataset tab
5. See 25 borrowers with average FICO ≈ 700 (vs default 667)
6. See clearing rate, outcomes change
7. Export as JSON/CSV with custom parameters

### New Workflow: Case Studies Deep Dive

1. Open Case Studies tab
2. Read Maria case: see her profile, then watch her go through each layer
3. See classic model fail (23.5% APR, borrower rejects) vs AI pass (15.3%, both accept)
4. See her match to WestBank (Eltura/Aperture floors too high)
5. Understand WHY each decision was made with concrete numbers
6. Close details, open Carlos: immediately see "0/5 eligible → supply failure"
7. Understand product gap vs borrower gap distinction

---

## Code Puppy Execution

Ready to build this? Steps:

1. Find the location after "Hidden-Prime Discovery" section in Data Generation tab
2. Add "Generate Dataset" button + regenerateDataset() function
3. Locate Case Studies tab (id="tab-cases")
4. Replace ultra-condensed case study HTML with detailed layer-by-layer templates
5. Add CSS for tables + styling if needed
6. Test: adjust FICO slider, click "Generate", verify dataset updates + auto-switches to Sample tab
7. Test: click Case Studies tab, verify each case shows full layer breakdown
8. Commit & push

Estimated execution: 1 hour for Code Puppy.


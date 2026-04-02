(function () {
  'use strict';

  const SIM = {
    modelType: 'model18',
    filter: 'all',
    borrowerCount: 100,
    borrowers: [],
    results: null,
    portfolio: null,
    lifecycleConfig: { baseDefaultRate: 1, earlyPayoffRate: 1, recoveryRate: 1 },
    selectedBorrower: null,
  };

  const PARTNERS = [
    { id: 'eltura', name: 'Eltura', type: 'ff', cap: 4000000, minFICO: 620, minAPR: 15.5, pri: 1, on: true },
    { id: 'aperture', name: 'Aperture', type: 'ff', cap: 3000000, minFICO: 640, minAPR: 16.0, pri: 2, on: true },
    { id: 'westbank', name: 'WestBank', type: 'bank', cap: 2000000, minFICO: 660, minAPR: 13.0, pri: 3, on: true },
    { id: 'spotfund_a', name: 'SpotFund A', type: 'spot', cap: null, minFICO: 680, minAPR: 17.5, pri: 4, on: true },
    { id: 'spotfund_b', name: 'SpotFund B', type: 'spot', cap: null, minFICO: 700, minAPR: 19.0, pri: 5, on: true },
  ];

  const SCENARIOS = {
    healthy: {
      label: 'Healthy Market',
      description: 'Baseline conditions, Model 18 pricing enabled, all capital partners active.',
      ficoMean: 680,
      modelType: 'model18',
      lifecycle: { baseDefaultRate: 1, earlyPayoffRate: 1, recoveryRate: 1 }
    },
    crunch: {
      label: 'Capital Crunch',
      description: 'Limited capital availability, Classic pricing only, partners with strict capacity constraints.',
      ficoMean: 645,
      modelType: 'classic',
      lifecycle: { baseDefaultRate: 1.5, earlyPayoffRate: 0.5, recoveryRate: 0.7 }
    },
    spike: {
      label: 'Rate Spike',
      description: 'Rising rates environment, Model 18 enabled with higher APR floors, partner minimums increased.',
      ficoMean: 700,
      modelType: 'model18',
      lifecycle: { baseDefaultRate: 1.2, earlyPayoffRate: 1.8, recoveryRate: 0.9 }
    },
  };

  const $ = (id) => document.getElementById(id);
  const money = (n) => '$' + Number(n || 0).toLocaleString();
  const pct = (n) => (n || 0).toFixed(1) + '%';

  function calculateModel18Score(borrower) {
    const baseScore = borrower.fico || 650;
    const isHP = borrower.hiddenPrime || borrower.hidden_prime || borrower.hp || false;
    const boost = isHP ? 50 : 0;
    return Math.min(baseScore + boost, 850);
  }

  function switchTab(tab) {
    document.querySelectorAll('[role="tabpanel"]').forEach((p) => (p.style.display = 'none'));
    const panel = $(`tab-${tab}`);
    if (panel) panel.style.display = 'block';
    document.querySelectorAll('[role="tab"]').forEach((b) => b.classList.remove('active'));
    const active = document.querySelector(`[role="tab"][data-tab="${tab}"]`);
    if (active) active.classList.add('active');
  }

  function renderKPIs(summary) {
    $('kpi-cards').innerHTML = [
      ['Clearing Rate', pct(summary.clearingRatePct)],
      ['BS Exposure', pct(summary.bsExposurePct)],
      ['Avg APR', pct(summary.avgApr)],
      ['HP Unlocked', pct(summary.hiddenPrimeUnlockedPct)],
    ]
      .map(([k, v]) => `<div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">${k}</div><div class="text-xl font-bold mt-1">${v}</div></div>`)
      .join('');
  }

  function outcomeClass(outcome) {
    if (outcome === 'CLEARED' || outcome === 'BALANCE_SHEET') return 'outcome-cleared';
    if (outcome === 'APR_REJECTED') return 'outcome-apr';
    return 'outcome-np';
  }

  function filteredLoans() {
    if (!SIM.results) return [];
    const loans = SIM.results.loans;
    if (SIM.filter === 'cleared') return loans.filter((l) => l.m18Outcome === 'CLEARED' || l.m18Outcome === 'BALANCE_SHEET');
    if (SIM.filter === 'apr_rejected') return loans.filter((l) => l.m18Outcome === 'APR_REJECTED');
    if (SIM.filter === 'no_partner') return loans.filter((l) => l.m18Outcome === 'NO_PARTNER');
    return loans;
  }

  function renderFilters() {
    $('filter-buttons').innerHTML = [
      ['all', 'All'],
      ['cleared', 'Cleared'],
      ['apr_rejected', 'APR Rejected'],
      ['no_partner', 'No Partner'],
    ]
      .map(
        ([k, l]) =>
          `<button class="px-3 py-1 rounded border text-xs ${SIM.filter === k ? 'bg-blue-600 text-white border-blue-600' : 'border-gray-300 dark:border-gray-600'}" data-filter="${k}">${l}</button>`,
      )
      .join('');

    $('filter-buttons').querySelectorAll('[data-filter]').forEach((btn) => {
      btn.addEventListener('click', () => {
        SIM.filter = btn.dataset.filter;
        renderFilters();
        renderTable();
      });
    });
  }

  function renderTable() {
    const rows = filteredLoans();
    $('borrower-table-body').innerHTML = rows
      .map(
        (loan, idx) => `<tr class="border-b border-gray-100 dark:border-gray-700 text-xs">
      <td class="px-2 py-1">${idx + 1}</td>
      <td class="px-2 py-1">${loan.fico}</td>
      <td class="px-2 py-1 font-semibold text-blue-600">${loan.model18Score || loan.fico}</td>
      <td class="px-2 py-1">${money(loan.amount)}</td>
      <td class="px-2 py-1">${loan.purpose}</td>
      <td class="px-2 py-1">${loan.hiddenPrime ? '★' : ''}</td>
      <td class="px-2 py-1">${loan.m18Apr ? pct(loan.m18Apr) : '—'}</td>
      <td class="px-2 py-1 ${outcomeClass(loan.m18Outcome)}">${loan.m18Outcome || '—'}</td>
      <td class="px-2 py-1">${loan.m18Partner || '—'}</td>
      <td class="px-2 py-1">${loan.classicApr ? pct(loan.classicApr) : '—'}</td>
      <td class="px-2 py-1 ${outcomeClass(loan.classicOutcome)}">${loan.classicOutcome || '—'}</td>
      <td class="px-2 py-1">${loan.classicPartner || '—'}</td>
      <td class="px-2 py-1"><button class="px-1 py-0 text-[10px] rounded border border-purple-500 text-purple-600" data-walk="${loan.id}">Walk</button></td></tr>`,
      )
      .join('');

    $('borrower-table-body').querySelectorAll('[data-walk]').forEach((btn) => btn.addEventListener('click', () => walkLoan(Number(btn.dataset.walk))));
    $('table-count').textContent = `Showing ${rows.length} of ${SIM.results.loans.length} loans`;
  }

  function metricLight(value, greenMax, yellowMax, lowerIsBetter = true) {
    if (lowerIsBetter) {
      if (value > yellowMax) return '🔴';
      if (value > greenMax) return '🟡';
      return '🟢';
    }
    if (value < greenMax) return '🔴';
    if (value < yellowMax) return '🟡';
    return '🟢';
  }

  // ── Marketplace Performance: fixed 100-loan baseline ──

  function seededRand(seed) {
    let t = seed;
    return function () {
      t += 0x6d2b79f5;
      let x = Math.imul(t ^ (t >>> 15), 1 | t);
      x ^= x + Math.imul(x ^ (x >>> 7), 61 | x);
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  }

  function generateBaseline() {
    // Generate 100 loans, 20 per partner, pre-cleared with deterministic attributes
    const rand = seededRand(42);
    const baselineLoans = [];
    let id = 9000;
    PARTNERS.forEach((partner) => {
      for (let i = 0; i < 20; i++) {
        const fico = partner.minFICO + Math.floor(rand() * 80);
        const hp = rand() < 0.28;
        const amount = 5000 + Math.floor(rand() * 30000);
        const purposes = ['Debt Consolidation', 'Home Improvement', 'Medical', 'Auto', 'Education'];
        const purpose = purposes[Math.floor(rand() * purposes.length)];
        const apr = partner.minAPR + rand() * 6;
        baselineLoans.push({
          id: id++,
          fico,
          hiddenPrime: hp,
          hidden_prime: hp,
          hp,
          amount,
          purpose,
          outcome: 'CLEARED',
          offeredApr: apr,
          matchedPartner: partner.name,
          matchedPartnerId: partner.id,
          partnerType: partner.type === 'bank' ? 'bank' : (partner.type === 'spot' ? 'spot' : 'ff'),
        });
      }
    });
    return baselineLoans;
  }

  function runBaselineScenarios() {
    const baselineLoans = generateBaseline();
    SIM.baseline = {};

    Object.entries(SCENARIOS).forEach(([key, scenario]) => {
      const portfolio = lifecycleEngine.initPortfolio(baselineLoans, PARTNERS);
      for (let m = 0; m <= 36; m++) {
        lifecycleEngine.stepMonth(portfolio, m, scenario.lifecycle);
      }
      SIM.baseline[key] = portfolio;
    });
  }

  function getBaselineSnapshot(scenarioKey, month) {
    const portfolio = SIM.baseline?.[scenarioKey];
    if (!portfolio?.snapshots?.length) return null;
    return portfolio.snapshots.find((s) => s.month === month) || portfolio.snapshots[portfolio.snapshots.length - 1];
  }

  function renderMarketplacePerformance() {
    const month = Number($('mp-month-slider').value) || 1;
    const filterPartner = $('mp-partner-filter').value;

    $('mp-month-label').textContent = `Month ${month}`;

    const scenarioMeta = {
      healthy: { label: 'Healthy Market', color: '#2563eb', bg: '#e0f2fe', border: '#93c5fd' },
      crunch: { label: 'Capital Crunch', color: '#d97706', bg: '#fef3c7', border: '#fcd34d' },
      spike: { label: 'Rate Spike', color: '#db2777', bg: '#fce7f3', border: '#f9a8d4' },
    };

    // Render scenario KPI cards (3 columns)
    let cardsHTML = '';
    Object.entries(scenarioMeta).forEach(([key, meta]) => {
      const snap = getBaselineSnapshot(key, month);
      if (!snap) return;

      let pms = snap.partnerMetrics || [];
      if (filterPartner !== 'all') {
        pms = pms.filter((p) => p.partnerId === filterPartner);
      }

      const b = snap.borrowerMetrics;
      const u = snap.upstartMetrics;
      const epdAvg = pms.length ? pms.reduce((a, p) => a + (p.epdRate || 0), 0) / pms.length : 0;
      const lossAvg = pms.length ? pms.reduce((a, p) => a + (p.lossRate || 0), 0) / pms.length : 0;
      const yieldAvg = pms.length ? pms.reduce((a, p) => a + (p.annualizedYield || 0), 0) / pms.length : 0;
      const totalFunded = pms.reduce((a, p) => a + (p.totalFunded || 0), 0);
      const activeCount = pms.reduce((a, p) => a + (p.activeCount || 0), 0);
      const defaultedCount = pms.reduce((a, p) => a + (p.defaultedCount || 0), 0);

      cardsHTML += `<div class="bg-white dark:bg-gray-800 p-4 rounded border-2" style="border-color:${meta.border}">
        <div class="flex items-center gap-2 mb-3">
          <div class="w-3 h-3 rounded-full" style="background:${meta.color}"></div>
          <h4 class="text-sm font-bold" style="color:${meta.color}">${meta.label}</h4>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs">
          <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Avg Yield</div><div class="text-lg font-bold mt-1">${pct(yieldAvg)}</div></div>
          <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Avg Loss</div><div class="text-lg font-bold mt-1">${metricLight(lossAvg, 5, 8, true)} ${pct(lossAvg)}</div></div>
          <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Avg EPD</div><div class="text-lg font-bold mt-1">${metricLight(epdAvg, 3, 4.5, true)} ${pct(epdAvg)}</div></div>
          <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Default Rate</div><div class="text-lg font-bold mt-1">${metricLight(b.defaultRatePct, 4, 7, true)} ${pct(b.defaultRatePct)}</div></div>
          <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Active</div><div class="text-lg font-bold mt-1">${activeCount}</div></div>
          <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Defaulted</div><div class="text-lg font-bold mt-1">${defaultedCount}</div></div>
        </div>
        <div class="mt-2 text-xs text-gray-500">Total Funded: ${money(totalFunded)} · Delinquency: ${pct(b.delinquentRatePct)} · Completion: ${pct(b.completionRatePct)}</div>
      </div>`;
    });
    $('mp-scenario-cards').innerHTML = cardsHTML;

    // Render partner breakdown table
    const partnerList = filterPartner === 'all' ? PARTNERS : PARTNERS.filter((p) => p.id === filterPartner);
    let tableRows = '';
    partnerList.forEach((partner) => {
      let cells = `<td class="px-2 py-1 font-semibold">${partner.name}</td>`;
      ['healthy', 'crunch', 'spike'].forEach((key) => {
        const snap = getBaselineSnapshot(key, month);
        const pm = snap?.partnerMetrics?.find((p) => p.partnerId === partner.id);
        if (pm) {
          cells += `<td class="px-2 py-1">${pct(pm.annualizedYield)}</td>`;
          cells += `<td class="px-2 py-1">${metricLight(pm.lossRate, 5, 8, true)} ${pct(pm.lossRate)}</td>`;
          cells += `<td class="px-2 py-1">${metricLight(pm.epdRate, 3, 4.5, true)} ${pct(pm.epdRate)}</td>`;
        } else {
          cells += '<td class="px-2 py-1 text-gray-400">—</td>'.repeat(3);
        }
      });
      tableRows += `<tr class="border-b border-gray-100 dark:border-gray-700">${cells}</tr>`;
    });

    // Add totals row
    let totCells = '<td class="px-2 py-1 font-bold">Total</td>';
    ['healthy', 'crunch', 'spike'].forEach((key) => {
      const snap = getBaselineSnapshot(key, month);
      const pms = snap?.partnerMetrics || [];
      const yieldAvg = pms.length ? pms.reduce((a, p) => a + (p.annualizedYield || 0), 0) / pms.length : 0;
      const lossAvg = pms.length ? pms.reduce((a, p) => a + (p.lossRate || 0), 0) / pms.length : 0;
      const epdAvg = pms.length ? pms.reduce((a, p) => a + (p.epdRate || 0), 0) / pms.length : 0;
      totCells += `<td class="px-2 py-1 font-bold">${pct(yieldAvg)}</td>`;
      totCells += `<td class="px-2 py-1 font-bold">${pct(lossAvg)}</td>`;
      totCells += `<td class="px-2 py-1 font-bold">${pct(epdAvg)}</td>`;
    });
    tableRows += `<tr class="border-t-2 border-gray-300 dark:border-gray-500 bg-gray-50 dark:bg-gray-700">${totCells}</tr>`;

    $('mp-partner-table-body').innerHTML = tableRows;

    // At-risk callouts (across all scenarios)
    let atRiskHTML = '';
    ['healthy', 'crunch', 'spike'].forEach((key) => {
      const snap = getBaselineSnapshot(key, month);
      const pms = snap?.partnerMetrics || [];
      const atRisk = pms.filter((p) => (p.epdRate || 0) > 4.5 || (p.lossRate || 0) > 8);
      if (atRisk.length) {
        atRiskHTML += atRisk.map((p) => `<div class="text-sm">🔴 <b>${scenarioMeta[key].label}</b> — ${p.partnerName}: EPD ${pct(p.epdRate)}, Loss ${pct(p.lossRate)}</div>`).join('');
      }
    });
    $('mp-atrisk').innerHTML = atRiskHTML
      ? `<h4 class="text-xs font-semibold uppercase text-gray-500 mb-2">At-Risk Partner Callouts</h4>${atRiskHTML}`
      : '<div class="text-sm">🟢 No at-risk partners at this month across any scenario.</div>';
  }

  function renderDeepDive(loanId) {
    const loan = (SIM.results?.loans || []).find((l) => l.id === loanId);
    if (!loan) return;
    SIM.selectedBorrower = loan;
    $('deepdive-empty').style.display = 'none';
    $('deepdive-content').style.display = 'block';

    const isNoPartner = loan.m18Outcome === 'NO_PARTNER' && loan.classicOutcome === 'NO_PARTNER';

    // Build eligibility matrix with failure reasons
    const partnerRows = PARTNERS.map((p) => {
      const RANGES = { ff: [3000, 40000], bank: [5000, 35000], spot: [2000, 50000] };
      const [minAmt, maxAmt] = RANGES[p.type] || [2000, 50000];
      const f = loan.fico >= p.minFICO ? '✅' : '❌';
      const a = (loan.amount >= minAmt && loan.amount <= maxAmt) ? '✅' : '❌';
      const purp = loan.purpose === 'Small Business' ? '❌' : '✅';
      const cap = p.cap == null ? '✅' : (loan.amount <= p.cap ? '✅' : '❌');
      const eligible = f === '✅' && a === '✅' && purp === '✅' && cap === '✅';
      const reasons = [];
      if (f === '❌') reasons.push(`FICO ${loan.fico} < ${p.minFICO}`);
      if (a === '❌') reasons.push(`Amount outside ${money(minAmt)}–${money(maxAmt)}`);
      if (purp === '❌') reasons.push('Small Business excluded');
      if (cap === '❌') reasons.push('Exceeds partner cap');
      const resultCell = eligible
        ? '<span class="text-green-600 font-semibold">Eligible</span>'
        : `<span class="text-red-600 font-semibold">Ineligible</span>`;
      const reasonNote = !eligible && reasons.length ? `<div class="text-[10px] text-red-500 mt-0.5">${reasons.join(', ')}</div>` : '';
      return `<tr><td class="px-2 py-1">${p.name}</td><td class="px-2 py-1">${f}</td><td class="px-2 py-1">${a}</td><td class="px-2 py-1">${purp}</td><td class="px-2 py-1">${cap}</td><td class="px-2 py-1">${resultCell}${reasonNote}</td></tr>`;
    }).join('');

    const noPartnerCallout = isNoPartner
      ? `<div class="mt-3 p-3 rounded bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 text-sm text-red-800 dark:text-red-200"><b>No Partner Match:</b> This borrower was ineligible for all partners or eligible partners had exhausted their capacity by the time this loan was processed in the waterfall. Capacity is consumed sequentially — earlier loans in the pipeline fill partner caps first.</div>`
      : '';

    $('deepdive-step1').innerHTML = `<h4 class="font-semibold mb-2">Step 1: Eligibility Matrix</h4><table class="w-full text-xs"><thead><tr><th class="px-2 py-1 text-left">Partner</th><th class="px-2 py-1 text-left">FICO</th><th class="px-2 py-1 text-left">Min Amount</th><th class="px-2 py-1 text-left">Purpose</th><th class="px-2 py-1 text-left">Cap</th><th class="px-2 py-1 text-left">Result</th></tr></thead><tbody>${partnerRows}</tbody></table>${noPartnerCallout}`;

    const classic = clearingEngine.priceLoan(loan, 'classic');
    const model18 = clearingEngine.priceLoan(loan, 'model18');
    const winner = model18.offeredApr < classic.offeredApr ? 'Model 18' : 'Classic';
    const hpCallout = loan.hiddenPrime ? `<div class="text-xs text-blue-600 mt-1">Hidden-prime detected: APR reduced by ${(classic.offeredApr - model18.offeredApr).toFixed(1)} pts under Model 18.</div>` : '';
    $('deepdive-step2').innerHTML = `<h4 class="font-semibold mb-2">Step 2: Pricing Engine</h4><div class="grid md:grid-cols-2 gap-3 text-sm"><div class="kpi-card"><div class="font-semibold">Classic</div><div>APR: <b>${pct(classic.offeredApr)}</b></div><div>P(default): <b>${pct(classic.pDefault * 100)}</b></div><div>Borrower max APR: <b>${pct(classic.maxApr)}</b></div></div><div class="kpi-card"><div class="font-semibold">Model 18</div><div>APR: <b>${pct(model18.offeredApr)}</b></div><div>P(default): <b>${pct(model18.pDefault * 100)}</b></div><div>Borrower max APR: <b>${pct(model18.maxApr)}</b></div></div></div><div class="text-xs mt-2">Winner: <b>${winner}</b>${hpCallout}</div>`;

    const sortedPartners = [...PARTNERS].sort((a, b) => a.pri - b.pri);
    const waterfallRows = sortedPartners
      .map((p) => {
        const m18Match = loan.m18Partner === p.name;
        const classicMatch = loan.classicPartner === p.name;
        return `<tr>
          <td class="px-2 py-1">${p.name}</td>
          <td class="px-2 py-1 ${m18Match ? 'text-green-600 font-bold' : 'text-gray-400'}">${m18Match ? 'MATCH' : 'SKIP'}</td>
          <td class="px-2 py-1 ${classicMatch ? 'text-green-600 font-bold' : 'text-gray-400'}">${classicMatch ? 'MATCH' : 'SKIP'}</td>
        </tr>`;
      }).join('');
    $('deepdive-step3').innerHTML = `<h4 class="font-semibold mb-2">Step 3: Waterfall Routing</h4>
      <table class="w-full text-xs"><thead><tr>
        <th class="px-2 py-1 text-left">Partner</th>
        <th class="px-2 py-1 text-left" style="background:#e0f2fe;color:#0c4a6e">Model 18</th>
        <th class="px-2 py-1 text-left" style="background:#f3e8ff;color:#581c87">Classic</th>
      </tr></thead><tbody>${waterfallRows}</tbody></table>
      <div class="text-xs mt-2 text-gray-500">M18: ${loan.m18Outcome || '—'} · Classic: ${loan.classicOutcome || '—'}</div>${isNoPartner ? '<div class="mt-2 p-2 rounded bg-red-50 dark:bg-red-900 text-xs text-red-700 dark:text-red-200">All partners skipped — either ineligible or capacity exhausted during waterfall processing.</div>' : ''}`;

    const lifeLoan = SIM.portfolio?.loans?.find((l) => l.id === loan.id);
    if (!lifeLoan) {
      $('deepdive-step4').innerHTML = `<h4 class="font-semibold mb-2">Step 4: Funding & Lifecycle</h4><div class="text-sm text-gray-500">${isNoPartner ? 'Loan was not funded — no partner match, so no lifecycle to simulate.' : 'No lifecycle data available for this loan.'}</div>`;
    } else {
      const strip = (lifeLoan.paymentHistory || []).slice(0, 36).map((s) => {
        const c = s === 'current' ? 'bg-green-500' : s.includes('dpd') ? 'bg-yellow-400' : s === 'default' ? 'bg-red-500' : 'bg-blue-500';
        return `<span class="inline-block w-3 h-3 rounded-sm ${c} mr-1" title="${s}"></span>`;
      }).join('');
      $('deepdive-step4').innerHTML = `<h4 class="font-semibold mb-2">Step 4: Funding & Lifecycle</h4><div class="text-sm">Funded: <b>${money(lifeLoan.amount)}</b> · APR: <b>${pct(lifeLoan.offeredApr)}</b> · Remaining: <b>${money(lifeLoan.remainingBalance)}</b></div><div class="text-sm mt-1">Status: <b>${lifeLoan.status}</b> · Total Paid: <b>${money(lifeLoan.totalPaid)}</b> · Interest: <b>${money(lifeLoan.totalInterestPaid)}</b></div><div class="mt-2">${strip || '<span class="text-xs text-gray-500">No months yet</span>'}</div>`;
    }

    switchTab('deepdive');
  }

  function bindDeepDiveSelect() {
    const sel = $('deepdive-borrower');
    if (!sel || !SIM.results) return;
    sel.innerHTML = SIM.results.loans.map((l) => `<option value="${l.id}">#${l.id} · FICO ${l.fico} · ${l.purpose} · M18: ${l.m18Outcome || '—'} · Classic: ${l.classicOutcome || '—'}</option>`).join('');
    sel.addEventListener('change', () => renderDeepDive(Number(sel.value)));
  }

  function walkLoan(id) {
    renderDeepDive(id);
    const sel = $('deepdive-borrower');
    if (sel) sel.value = String(id);
  }

  function updateReapp() {
    if (!SIM.portfolio) return;
    const loans = SIM.portfolio.loans || [];
    const funded = loans.length;
    const completed = loans.filter((l) => l.status === 'paid_off' || l.status === 'early_payoff').length;
    const reapply = Math.round(completed * 0.15);
    $('reapp-funded').textContent = String(funded);
    $('reapp-completed').textContent = String(completed);
    $('reapp-reapply').textContent = String(reapply);
  }

  function setScenarioActive(key) {
    document.querySelectorAll('.scenario-btn').forEach((b) => {
      const active = b.dataset.scn === key;
      b.style.backgroundColor = active ? '#1d4ed8' : '';
      b.style.color = active ? 'white' : '';
      b.style.borderColor = active ? '#1d4ed8' : '';
    });
  }

  function applyScenario(key) {
    const s = SCENARIOS[key];
    if (!s) return;
    $('fico-slider').value = s.ficoMean;
    $('fico-value').textContent = String(s.ficoMean);
    SIM.modelType = s.modelType;
    SIM.lifecycleConfig = { ...s.lifecycle };
    setScenarioActive(key);
    // Update scenario description
    const descEl = $('scenario-description');
    if (descEl) {
      descEl.innerHTML = `<b id="scenario-title">${s.label}</b>: ${s.description}`;
    }
  }

  function bindScenarios() {
    $('scenario-buttons').innerHTML = Object.entries(SCENARIOS)
      .map(([k, v]) => `<button class="px-3 py-1 rounded border text-xs scenario-btn" data-scn="${k}">${v.label}</button>`)
      .join('');
    $('scenario-buttons').querySelectorAll('[data-scn]').forEach((btn) => btn.addEventListener('click', () => applyScenario(btn.dataset.scn)));
    applyScenario('healthy');
  }

  function generatePipeline() {
    SIM.borrowers = borrowerGeneration.generateBorrowerFull(SIM.borrowerCount, Number($('fico-slider').value), 0.28);
    SIM.results = null;
    SIM.filter = 'all';

    $('pipeline-empty').style.display = 'none';
    $('pipeline-results').style.display = 'block';
    $('kpi-cards').innerHTML = `<div class="col-span-4 text-xs text-gray-500 dark:text-gray-400 py-1">${SIM.borrowers.length} borrowers in pipeline — click ⚡ Run Clearing to process</div>`;
    $('filter-buttons').innerHTML = '';

    $('borrower-table-body').innerHTML = SIM.borrowers
      .map((loan, idx) => `<tr class="border-b border-gray-100 dark:border-gray-700 text-xs">
        <td class="px-2 py-1">${idx + 1}</td>
        <td class="px-2 py-1">${loan.fico}</td>
        <td class="px-2 py-1 text-gray-400">—</td>
        <td class="px-2 py-1">${money(loan.amount)}</td>
        <td class="px-2 py-1">${loan.purpose}</td>
        <td class="px-2 py-1">${loan.hiddenPrime ? '★' : ''}</td>
        <td class="px-2 py-1 text-gray-400">—</td>
        <td class="px-2 py-1 text-gray-400 italic">Pending</td>
        <td class="px-2 py-1 text-gray-400">—</td>
        <td class="px-2 py-1 text-gray-400">—</td>
        <td class="px-2 py-1 text-gray-400 italic">Pending</td>
        <td class="px-2 py-1 text-gray-400">—</td>
        <td class="px-2 py-1"></td></tr>`)
      .join('');
    $('table-count').textContent = `${SIM.borrowers.length} borrowers generated — awaiting clearing`;

    const clearBtn = $('clear-btn');
    clearBtn.disabled = false;
    clearBtn.style.opacity = '1';
    clearBtn.style.cursor = 'pointer';
  }

  function runClearing() {
    if (!SIM.borrowers.length) return;

    // Run both models and merge results
    const m18Results = clearingEngine.runClearing(SIM.borrowers, PARTNERS, 'model18');
    const classicResults = clearingEngine.runClearing(SIM.borrowers, PARTNERS, 'classic');

    // Merge loan data side-by-side
    const mergedLoans = SIM.borrowers.map((b, idx) => {
      const m18Loan = m18Results.loans.find(l => l.id === b.id);
      const classicLoan = classicResults.loans.find(l => l.id === b.id);
      return {
        ...b,
        id: b.id,
        fico: b.fico,
        model18Score: calculateModel18Score(b),
        amount: b.amount,
        purpose: b.purpose,
        hiddenPrime: b.hiddenPrime || b.hidden_prime || b.hp || false,
        m18Apr: m18Loan?.offeredApr,
        m18Outcome: m18Loan?.outcome,
        m18Partner: m18Loan?.matchedPartner,
        classicApr: classicLoan?.offeredApr,
        classicOutcome: classicLoan?.outcome,
        classicPartner: classicLoan?.matchedPartner,
      };
    });

    // Use Model 18 results for lifecycle (primary model)
    SIM.results = m18Results;
    SIM.results.loans = mergedLoans;

    SIM.portfolio = lifecycleEngine.initPortfolio(m18Results.loans, PARTNERS);
    // Run all 36 months of lifecycle simulation upfront
    for (let m = 0; m <= 36; m++) {
      lifecycleEngine.stepMonth(SIM.portfolio, m, SIM.lifecycleConfig);
    }

    renderKPIs(SIM.results.summary);
    SIM.filter = 'all';
    renderFilters();
    renderTable();
    bindDeepDiveSelect();
    updateReapp();
  }

  function bindEvents() {
    document.querySelectorAll('[role="tab"]').forEach((b) => b.addEventListener('click', () => switchTab(b.dataset.tab)));
    $('fico-slider').addEventListener('input', (e) => ($('fico-value').textContent = e.target.value));
    $('count-slider').addEventListener('input', (e) => {
      SIM.borrowerCount = Number(e.target.value);
      $('count-value').textContent = String(SIM.borrowerCount);
    });

    $('gen-btn').addEventListener('click', generatePipeline);
    $('clear-btn').addEventListener('click', runClearing);

    $('mp-month-slider').addEventListener('input', () => renderMarketplacePerformance());
    $('mp-partner-filter').addEventListener('change', () => renderMarketplacePerformance());
  }

  window.SIM = window.SIM || {};

  document.addEventListener('DOMContentLoaded', () => {
    bindScenarios();
    bindEvents();
    runBaselineScenarios();
    renderMarketplacePerformance();
  });
})();

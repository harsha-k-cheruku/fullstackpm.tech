(function () {
  'use strict';

  const SIM = {
    modelType: 'model18',
    filter: 'all',
    borrowers: [],
    results: null,
    portfolio: null,
    lifecycleConfig: { baseDefaultRate: 1, earlyPayoffRate: 1, recoveryRate: 1 },
    timeline: { healthChart: null, lossChart: null, interventionMonths: [] },
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
    healthy: { label: 'Healthy Market', ficoMean: 680, modelType: 'model18', lifecycle: { baseDefaultRate: 1, earlyPayoffRate: 1, recoveryRate: 1 } },
    crunch: { label: 'Capital Crunch', ficoMean: 645, modelType: 'classic', lifecycle: { baseDefaultRate: 1.5, earlyPayoffRate: 0.5, recoveryRate: 0.7 } },
    spike: { label: 'Rate Spike', ficoMean: 700, modelType: 'model18', lifecycle: { baseDefaultRate: 1.2, earlyPayoffRate: 1.8, recoveryRate: 0.9 } },
  };

  const PERSONA_RULES = {
    maria: (l) => l.hiddenPrime && l.fico >= 640 && l.fico <= 670,
    carlos: (l) => l.outcome === 'NO_PARTNER' || l.fico < 620,
    james: (l) => l.partnerType === 'bs' || l.fico >= 760,
  };

  const $ = (id) => document.getElementById(id);
  const money = (n) => '$' + Number(n || 0).toLocaleString();
  const pct = (n) => (n || 0).toFixed(1) + '%';

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
    if (SIM.filter === 'cleared') return loans.filter((l) => l.outcome === 'CLEARED' || l.outcome === 'BALANCE_SHEET');
    if (SIM.filter === 'apr_rejected') return loans.filter((l) => l.outcome === 'APR_REJECTED');
    if (SIM.filter === 'no_partner') return loans.filter((l) => l.outcome === 'NO_PARTNER');
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
        (loan, idx) => `<tr class="border-b border-gray-100 dark:border-gray-700">
      <td class="px-3 py-2">${idx + 1}</td><td class="px-3 py-2">${loan.fico}</td><td class="px-3 py-2">${money(loan.amount)}</td><td class="px-3 py-2">${loan.purpose}</td>
      <td class="px-3 py-2">${loan.hiddenPrime || loan.hidden_prime || loan.hp ? '★' : ''}</td><td class="px-3 py-2">${loan.offeredApr ? pct(loan.offeredApr) : '—'}</td>
      <td class="px-3 py-2 ${outcomeClass(loan.outcome)}">${loan.outcome}</td><td class="px-3 py-2">${loan.matchedPartner || '—'}</td>
      <td class="px-3 py-2"><button class="px-2 py-1 rounded border border-purple-500 text-purple-600" data-walk="${loan.id}">Walk</button></td></tr>`,
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

  function findSnapshot(month) {
    if (!SIM.portfolio?.snapshots?.length) return null;
    return SIM.portfolio.snapshots.find((s) => s.month === month) || SIM.portfolio.snapshots[SIM.portfolio.snapshots.length - 1];
  }

  function renderPartnerCards(snapshot) {
    $('timeline-partner-cards').innerHTML = (snapshot.partnerMetrics || [])
      .map(
        (p) => `<div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">${p.partnerName}</div>
      <div class="mt-1 text-xs">Yield: <b>${pct(p.annualizedYield)}</b></div><div class="text-xs">EPD: <b>${pct(p.epdRate)}</b></div><div class="text-xs">Loss: <b>${pct(p.lossRate)}</b></div></div>`,
      )
      .join('');
  }

  function renderTimelineSummary() {
    if (!SIM.portfolio?.snapshots?.length) return;
    const latest = SIM.portfolio.snapshots[SIM.portfolio.snapshots.length - 1];
    const s = latest.statusCounts || {};
    const hp = SIM.portfolio.loans.filter((l) => l.hiddenPrime);
    const non = SIM.portfolio.loans.filter((l) => !l.hiddenPrime);
    const hpRate = hp.length ? (hp.filter((l) => l.status === 'default').length / hp.length) * 100 : 0;
    const nonRate = non.length ? (non.filter((l) => l.status === 'default').length / non.length) * 100 : 0;

    $('timeline-ready-summary').innerHTML = `<div class="font-semibold mb-1">Lifecycle engine ready ✅ (Month ${latest.month})</div>
      <div>Active: ${(s.current || 0) + (s['30dpd'] || 0) + (s['60dpd'] || 0) + (s['90dpd'] || 0)} · Defaults: ${s.default || 0} · Paid off: ${(s.paid_off || 0) + (s.early_payoff || 0)}</div>
      <div class="text-xs text-gray-500 mt-1">Borrower delinquency: ${pct(latest.borrowerMetrics.delinquentRatePct)} · Upstart BS exposure: ${pct(latest.upstartMetrics.bsExposurePct)} · Model accuracy: ${pct(latest.upstartMetrics.modelAccuracy)}</div>`;
    $('timeline-month').textContent = `${latest.month} / 36`;
    $('timeline-metrics').innerHTML = `<div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">HP Default Rate</div><div class="text-xl font-bold mt-1">${pct(hpRate)}</div></div>
      <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Non-HP Default Rate</div><div class="text-xl font-bold mt-1">${pct(nonRate)}</div></div>
      <div class="kpi-card"><div class="text-[10px] uppercase text-gray-500">Gap (Non-HP - HP)</div><div class="text-xl font-bold mt-1">${pct(nonRate - hpRate)}</div></div>`;
    renderPartnerCards(latest);
  }

  function renderAnalytics(month) {
    const snap = findSnapshot(month);
    if (!snap) return;
    const locked = $('analytics-locked');
    const ready = $('analytics-ready');
    if (snap.month >= 1) {
      locked.style.display = 'none';
      ready.style.display = 'block';
    } else {
      locked.style.display = 'block';
      ready.style.display = 'none';
    }

    $('analytics-month-label').textContent = `Month ${snap.month}`;
    const slider = $('analytics-month-slider');
    slider.max = String(SIM.portfolio.snapshots[SIM.portfolio.snapshots.length - 1].month);
    slider.value = String(snap.month);

    const b = snap.borrowerMetrics;
    const u = snap.upstartMetrics;
    const pms = snap.partnerMetrics || [];
    const epdAvg = pms.length ? pms.reduce((a, p) => a + (p.epdRate || 0), 0) / pms.length : 0;
    const lossAvg = pms.length ? pms.reduce((a, p) => a + (p.lossRate || 0), 0) / pms.length : 0;

    $('analytics-borrower-panel').innerHTML = `<h4 class="text-xs font-semibold uppercase text-gray-500 mb-2">Borrower Health</h4>
      <div class="text-sm">${metricLight(b.delinquentRatePct, 5, 8, true)} Delinquency: <b>${pct(b.delinquentRatePct)}</b></div>
      <div class="text-sm">${metricLight(b.defaultRatePct, 4, 7, true)} Default Rate: <b>${pct(b.defaultRatePct)}</b></div>
      <div class="text-sm">${metricLight(b.completionRatePct, 70, 55, false)} Completion: <b>${pct(b.completionRatePct)}</b></div>`;

    $('analytics-upstart-panel').innerHTML = `<h4 class="text-xs font-semibold uppercase text-gray-500 mb-2">Upstart Platform</h4>
      <div class="text-sm">${metricLight(u.bsExposurePct, 8, 15, true)} BS Exposure: <b>${pct(u.bsExposurePct)}</b></div>
      <div class="text-sm">${metricLight(u.modelAccuracy, 90, 80, false)} Model Accuracy: <b>${pct(u.modelAccuracy)}</b></div>
      <div class="text-sm">Fees: <b>${money(u.cumulativeFees)}</b></div>`;

    $('analytics-partner-panel').innerHTML = `<h4 class="text-xs font-semibold uppercase text-gray-500 mb-2">Capital Partners</h4>
      <div class="text-sm">${metricLight(epdAvg, 3, 4.5, true)} Avg EPD: <b>${pct(epdAvg)}</b></div>
      <div class="text-sm">${metricLight(lossAvg, 5, 8, true)} Avg Loss: <b>${pct(lossAvg)}</b></div>`;

    const atRisk = pms.filter((p) => (p.epdRate || 0) > 4.5 || (p.lossRate || 0) > 8);
    $('analytics-atrisk').innerHTML = atRisk.length
      ? `<h4 class="text-xs font-semibold uppercase text-gray-500 mb-2">At-Risk Partner Callouts</h4>${atRisk.map((p) => `<div class="text-sm">🔴 <b>${p.partnerName}</b> — EPD ${pct(p.epdRate)}, Loss ${pct(p.lossRate)}</div>`).join('')}`
      : '<div class="text-sm">🟢 No at-risk partners at this month.</div>';
  }

  function logTimeline(msg) {
    $('timeline-log').innerHTML = `<div class="text-gray-500">[${new Date().toLocaleTimeString()}] ${msg}</div>` + $('timeline-log').innerHTML;
  }

  const interventionMarkerPlugin = {
    id: 'interventionMarkers',
    afterDraw(chart) {
      const months = SIM.timeline.interventionMonths || [];
      const x = chart.scales.x;
      const y = chart.scales.y;
      if (!months.length || !x || !y) return;
      const ctx = chart.ctx;
      ctx.save();
      ctx.setLineDash([5, 5]);
      ctx.strokeStyle = '#9333ea';
      months.forEach((m) => {
        const px = x.getPixelForValue(`M${m}`);
        if (!Number.isFinite(px)) return;
        ctx.beginPath();
        ctx.moveTo(px, y.top);
        ctx.lineTo(px, y.bottom);
        ctx.stroke();
      });
      ctx.restore();
    },
  };

  function buildTimelineCharts() {
    if (SIM.timeline.healthChart) SIM.timeline.healthChart.destroy();
    if (SIM.timeline.lossChart) SIM.timeline.lossChart.destroy();

    SIM.timeline.healthChart = new Chart($('timeline-health-chart'), {
      type: 'line',
      data: { labels: [], datasets: [
        { label: 'Current', data: [], borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.25)', fill: true, stack: 'status' },
        { label: 'Delinquent', data: [], borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.25)', fill: true, stack: 'status' },
        { label: 'Default', data: [], borderColor: '#dc2626', backgroundColor: 'rgba(220,38,38,0.25)', fill: true, stack: 'status' },
        { label: 'Paid', data: [], borderColor: '#2563eb', backgroundColor: 'rgba(37,99,235,0.25)', fill: true, stack: 'status' },
      ] },
      options: { responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } }, plugins: { legend: { position: 'bottom' } } },
      plugins: [interventionMarkerPlugin],
    });

    SIM.timeline.lossChart = new Chart($('timeline-loss-chart'), {
      type: 'line',
      data: { labels: [], datasets: [
        { label: 'Loss Rate %', data: [], borderColor: '#ef4444', tension: 0.2 },
        { label: 'Delinquency %', data: [], borderColor: '#f59e0b', tension: 0.2 },
      ] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { beginAtZero: true } } },
      plugins: [interventionMarkerPlugin],
    });

    animationController.registerChart('health', SIM.timeline.healthChart, (_, __, snaps) => {
      SIM.timeline.healthChart.data.labels = snaps.map((s) => `M${s.month}`);
      SIM.timeline.healthChart.data.datasets[0].data = snaps.map((s) => s.statusCounts.current || 0);
      SIM.timeline.healthChart.data.datasets[1].data = snaps.map((s) => (s.statusCounts['30dpd'] || 0) + (s.statusCounts['60dpd'] || 0) + (s.statusCounts['90dpd'] || 0));
      SIM.timeline.healthChart.data.datasets[2].data = snaps.map((s) => s.statusCounts.default || 0);
      SIM.timeline.healthChart.data.datasets[3].data = snaps.map((s) => (s.statusCounts.paid_off || 0) + (s.statusCounts.early_payoff || 0));
    });

    animationController.registerChart('loss', SIM.timeline.lossChart, (_, __, snaps) => {
      SIM.timeline.lossChart.data.labels = snaps.map((s) => `M${s.month}`);
      SIM.timeline.lossChart.data.datasets[0].data = snaps.map((s) => {
        const p = s.partnerMetrics || [];
        return p.length ? Number((p.reduce((a, m) => a + (m.lossRate || 0), 0) / p.length).toFixed(2)) : 0;
      });
      SIM.timeline.lossChart.data.datasets[1].data = snaps.map((s) => Number((s.borrowerMetrics?.delinquentRatePct || 0).toFixed(2)));
    });
  }

  function setupAnimationController() {
    animationController.init(SIM.portfolio, {
      speedMs: Number($('timeline-speed').value || 500),
      maxMonths: 36,
      lifecycleConfig: SIM.lifecycleConfig,
      onTick: (_, m) => {
        renderTimelineSummary();
        renderAnalytics(m);
        if ($('analytics-ready').style.display !== 'none') $('analytics-month-slider').value = String(m);
      },
      onPause: (_, m) => logTimeline(`Paused at Month ${m}`),
      onComplete: (_, m) => {
        renderTimelineSummary();
        renderAnalytics(m);
        logTimeline('Simulation reached Month 36');
      },
    });
    buildTimelineCharts();
    animationController.seekTo(0);
    renderTimelineSummary();
    renderAnalytics(0);
  }

  function runLifecycleMonths(m = 36) {
    animationController.seekTo(m);
    renderTimelineSummary();
    renderAnalytics(m);
    logTimeline(`Ran deterministic simulation through Month ${m}`);
  }

  function resetLifecycle() {
    SIM.portfolio = lifecycleEngine.initPortfolio(SIM.results.loans, PARTNERS);
    lifecycleEngine.stepMonth(SIM.portfolio, 0, SIM.lifecycleConfig);
    SIM.timeline.interventionMonths = [];
    setupAnimationController();
    logTimeline('Lifecycle reset to Month 0');
  }

  function applyTimelineIntervention() {
    if (animationController.getState().playing) return logTimeline('Pause before intervening (Zen puppy rule).');
    const partnerId = $('intervention-partner').value;
    const fico = Number($('intervention-fico').value || 700);
    lifecycleEngine.applyIntervention(SIM.portfolio, partnerId, { ficoFloor: fico });
    SIM.timeline.interventionMonths.push(SIM.portfolio.month);
    renderTimelineSummary();
    renderAnalytics(SIM.portfolio.month);
    logTimeline(`Applied intervention at Month ${SIM.portfolio.month}: ${partnerId} ficoFloor → ${fico}`);
  }

  function personaPick(name) {
    const list = SIM.results?.loans || [];
    return list.find(PERSONA_RULES[name]) || list[0] || null;
  }

  function renderDeepDive(loanId) {
    const loan = (SIM.results?.loans || []).find((l) => l.id === loanId);
    if (!loan) return;
    SIM.selectedBorrower = loan;
    $('deepdive-empty').style.display = 'none';
    $('deepdive-content').style.display = 'block';

    const detail = clearingEngine.walkthrough ? clearingEngine.walkthrough(loan, PARTNERS, SIM.modelType, {}) : null;
    const partnerRows = PARTNERS.map((p) => {
      const f = loan.fico >= p.minFICO ? '✅' : '❌';
      const a = loan.amount >= 2000 ? '✅' : '❌';
      const purp = loan.purpose === 'Small Business' ? '❌' : '✅';
      const cap = p.cap == null ? '✅' : (loan.amount <= p.cap ? '✅' : '❌');
      const result = f === '✅' && a === '✅' && purp === '✅' && cap === '✅' ? 'Eligible' : 'Ineligible';
      return `<tr><td class="px-2 py-1">${p.name}</td><td class="px-2 py-1">${f}</td><td class="px-2 py-1">${a}</td><td class="px-2 py-1">${purp}</td><td class="px-2 py-1">${cap}</td><td class="px-2 py-1">${result}</td></tr>`;
    }).join('');

    $('deepdive-step1').innerHTML = `<h4 class="font-semibold mb-2">Step 1: Eligibility Matrix</h4><table class="w-full text-xs"><thead><tr><th class="px-2 py-1 text-left">Partner</th><th>FICO</th><th>Loan</th><th>Purpose</th><th>Cap</th><th>Result</th></tr></thead><tbody>${partnerRows}</tbody></table>`;

    const classic = clearingEngine.priceLoan(loan, 'classic');
    const model18 = clearingEngine.priceLoan(loan, 'model18');
    const winner = model18.offeredApr < classic.offeredApr ? 'Model 18' : 'Classic';
    const hpCallout = loan.hiddenPrime ? `<div class="text-xs text-blue-600 mt-1">Hidden-prime detected: APR reduced by ${(classic.offeredApr - model18.offeredApr).toFixed(1)} pts under Model 18.</div>` : '';
    $('deepdive-step2').innerHTML = `<h4 class="font-semibold mb-2">Step 2: Pricing Engine</h4><div class="grid md:grid-cols-2 gap-3 text-sm"><div class="kpi-card"><div class="font-semibold">Classic</div><div>APR: <b>${pct(classic.offeredApr)}</b></div><div>P(default): <b>${pct(classic.pDefault * 100)}</b></div><div>Borrower max APR: <b>${pct(classic.maxApr)}</b></div></div><div class="kpi-card"><div class="font-semibold">Model 18</div><div>APR: <b>${pct(model18.offeredApr)}</b></div><div>P(default): <b>${pct(model18.pDefault * 100)}</b></div><div>Borrower max APR: <b>${pct(model18.maxApr)}</b></div></div></div><div class="text-xs mt-2">Winner: <b>${winner}</b>${hpCallout}</div>`;

    const waterfall = PARTNERS.sort((a, b) => a.pri - b.pri)
      .map((p) => `<div class="text-xs py-1">${p.name} → ${loan.matchedPartnerId === p.id ? '<b class="text-green-600">MATCH</b>' : 'SKIP'}</div>`)
      .join('');
    const bsLine = loan.partnerType === 'bs' ? '<div class="text-xs py-1"><b class="text-amber-600">Balance Sheet fallback</b></div>' : '';
    $('deepdive-step3').innerHTML = `<h4 class="font-semibold mb-2">Step 3: Waterfall Routing</h4>${waterfall}${bsLine}`;

    const lifeLoan = SIM.portfolio?.loans?.find((l) => l.id === loan.id);
    if (!lifeLoan) {
      $('deepdive-step4').innerHTML = '<h4 class="font-semibold mb-2">Step 4: Funding & Lifecycle</h4><div class="text-sm text-gray-500">Run timeline first to view payment history strip.</div>';
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
    sel.innerHTML = SIM.results.loans.map((l) => `<option value="${l.id}">#${l.id} · FICO ${l.fico} · ${l.purpose} · ${l.outcome}</option>`).join('');
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

  function setModelActive(modelType) {
    document.querySelectorAll('.model-btn').forEach((b) => {
      const active = b.dataset.model === modelType;
      b.style.backgroundColor = active ? '#2563eb' : '';
      b.style.color = active ? 'white' : '';
      b.style.borderColor = active ? '#2563eb' : '';
    });
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
    setModelActive(SIM.modelType);
    setScenarioActive(key);
  }

  function bindScenarios() {
    $('scenario-buttons').innerHTML = Object.entries(SCENARIOS)
      .map(([k, v]) => `<button class="px-3 py-1 rounded border text-xs scenario-btn" data-scn="${k}">${v.label}</button>`)
      .join('');
    $('scenario-buttons').querySelectorAll('[data-scn]').forEach((btn) => btn.addEventListener('click', () => applyScenario(btn.dataset.scn)));
    applyScenario('healthy');
  }

  function generatePipeline() {
    SIM.borrowers = borrowerGeneration.generateBorrowerFull(100, Number($('fico-slider').value), 0.28);
    SIM.results = null;
    SIM.filter = 'all';

    $('pipeline-empty').style.display = 'none';
    $('pipeline-results').style.display = 'block';
    $('kpi-cards').innerHTML = `<div class="col-span-4 text-xs text-gray-500 dark:text-gray-400 py-1">${SIM.borrowers.length} borrowers in pipeline — click ⚡ Run Clearing to process</div>`;
    $('filter-buttons').innerHTML = '';

    $('borrower-table-body').innerHTML = SIM.borrowers
      .map((loan, idx) => `<tr class="border-b border-gray-100 dark:border-gray-700">
        <td class="px-3 py-2">${idx + 1}</td><td class="px-3 py-2">${loan.fico}</td><td class="px-3 py-2">${money(loan.amount)}</td><td class="px-3 py-2">${loan.purpose}</td>
        <td class="px-3 py-2">${loan.hiddenPrime ? '★' : ''}</td><td class="px-3 py-2 text-gray-400">—</td>
        <td class="px-3 py-2 text-gray-400 italic">Pending</td><td class="px-3 py-2 text-gray-400">—</td><td class="px-3 py-2"></td></tr>`)
      .join('');
    $('table-count').textContent = `${SIM.borrowers.length} borrowers generated — awaiting clearing`;

    const clearBtn = $('clear-btn');
    clearBtn.disabled = false;
    clearBtn.style.opacity = '1';
    clearBtn.style.cursor = 'pointer';
  }

  function runClearing() {
    if (!SIM.borrowers.length) return;
    SIM.results = clearingEngine.runClearing(SIM.borrowers, PARTNERS, SIM.modelType);
    SIM.portfolio = lifecycleEngine.initPortfolio(SIM.results.loans, PARTNERS);
    lifecycleEngine.stepMonth(SIM.portfolio, 0, SIM.lifecycleConfig);

    $('timeline-locked').style.display = 'none';
    $('timeline-ready').style.display = 'block';

    setupAnimationController();
    renderKPIs(SIM.results.summary);
    SIM.filter = 'all';
    renderFilters();
    renderTable();
    bindDeepDiveSelect();
    updateReapp();
    logTimeline('Clearing complete — lifecycle portfolio initialized');
  }

  function bindEvents() {
    document.querySelectorAll('[role="tab"]').forEach((b) => b.addEventListener('click', () => switchTab(b.dataset.tab)));
    $('fico-slider').addEventListener('input', (e) => ($('fico-value').textContent = e.target.value));
    document.querySelectorAll('.model-btn').forEach((btn) => btn.addEventListener('click', () => {
      SIM.modelType = btn.dataset.model;
      setModelActive(SIM.modelType);
    }));

    $('gen-btn').addEventListener('click', generatePipeline);
    $('clear-btn').addEventListener('click', runClearing);
    $('timeline-play').addEventListener('click', () => { animationController.play(); logTimeline('Play timeline'); });
    $('timeline-pause').addEventListener('click', () => animationController.pause());
    $('timeline-resume').addEventListener('click', () => { animationController.resume(); logTimeline('Resume timeline'); });
    $('timeline-run-36').addEventListener('click', () => runLifecycleMonths(36));
    $('timeline-reset').addEventListener('click', resetLifecycle);
    $('timeline-apply-intervention').addEventListener('click', applyTimelineIntervention);
    $('timeline-speed').addEventListener('change', (e) => { animationController.setSpeed(Number(e.target.value)); logTimeline(`Speed set to ${e.target.selectedOptions[0].text}`); });
    $('analytics-month-slider').addEventListener('input', (e) => {
      const month = Number(e.target.value || 0);
      animationController.pause();
      animationController.seekTo(month);
      renderTimelineSummary();
      renderAnalytics(month);
      updateReapp();
    });

  }

  window.SIM = window.SIM || {};
  window.SIM.showPersona = (name) => {
    const p = personaPick(name);
    if (p) walkLoan(p.id);
  };

  document.addEventListener('DOMContentLoaded', () => {
    bindScenarios();
    bindEvents();
  });
})();

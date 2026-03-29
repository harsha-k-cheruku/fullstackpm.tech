(function () {
  'use strict';

  function gauss(mean, sigma) {
    let u = 0;
    let v = 0;
    while (!u) u = Math.random();
    while (!v) v = Math.random();
    return mean + sigma * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function lognorm(mean, sigma) {
    return Math.exp(Math.log(mean) + sigma * gauss(0, 1));
  }

  function classicAPR(fico) {
    if (fico >= 780) return 10.5;
    if (fico >= 740) return 13;
    if (fico >= 700) return 16.5;
    if (fico >= 660) return 21.5;
    if (fico >= 620) return 27.5;
    if (fico >= 580) return 33;
    return 38;
  }

  function borrowerMaxAPR(fico, sensitivity, hiddenPrime) {
    let base;
    if (fico >= 780) base = 14;
    else if (fico >= 740) base = 18;
    else if (fico >= 700) base = 23;
    else if (fico >= 660) base = 29;
    else if (fico >= 620) base = 33;
    else if (fico >= 580) base = 37;
    else base = 42;

    if (hiddenPrime) base -= 5;

    return clamp(base + (sensitivity - 2) * -3 + gauss(0, 2), 9, 50);
  }

  function calculateRiskScore(fico, hiddenPrime) {
    const raw = (850 - fico) / 850;
    return clamp(hiddenPrime ? raw - 0.02 : raw, 0, 1);
  }

  function calculatePDefault(fico, hiddenPrime) {
    let p = calculateRiskScore(fico, hiddenPrime) * 0.18 + 0.02;
    if (hiddenPrime) p -= 0.02;
    return clamp(p, 0.01, 0.15);
  }

  function choosePurpose(seed) {
    const purposes = [
      'Debt Consolidation',
      'Emergency/Medical',
      'Home Improvement',
      'Auto Refinance',
    ];
    return purposes[seed % purposes.length];
  }

  function estimateIncome(fico, loanAmount, hiddenPrime) {
    const baseIncome = (fico - 500) * 850 + gauss(22000, 12000);
    const loanAdjustment = loanAmount * 2.2;
    const hpAdjustment = hiddenPrime ? 4000 : 0;
    return Math.round(clamp(baseIncome + loanAdjustment + hpAdjustment, 30000, 180000) / 1000) * 1000;
  }

  function generateBorrowerFull(n = 25, creditQuality = 667, hiddenPrimeRate = 0.28) {
    const borrowers = [];

    for (let i = 1; i <= n; i += 1) {
      const fico = Math.round(clamp(gauss(creditQuality, 65), 520, 820));
      const amount = Math.round(clamp(lognorm(12000, 0.45), 2000, 45000) / 100) * 100;
      const hiddenPrime = fico >= 580 && fico <= 720 && Math.random() < hiddenPrimeRate;
      const purpose = choosePurpose(i);
      const income = estimateIncome(fico, amount, hiddenPrime);
      const riskScore = calculateRiskScore(fico, hiddenPrime);
      const pDefault = calculatePDefault(fico, hiddenPrime);
      const classicApr = classicAPR(fico);
      const aiApr = hiddenPrime
        ? clamp(classicApr - clamp(gauss(8.5, 1.5), 5, 12), 9, 40)
        : classicApr;
      const maxApr = borrowerMaxAPR(fico, 2, hiddenPrime);
      const clearingApr = aiApr <= maxApr ? Number(aiApr.toFixed(1)) : null;

      borrowers.push({
        id: i,
        name: `Borrower ${i}`,
        fico,
        amount,
        purpose,
        income,
        hiddenPrime,
        riskScore: Number(riskScore.toFixed(3)),
        pDefault: Number(pDefault.toFixed(3)),
        clearingApr,
        classicApr: Number(classicApr.toFixed(1)),
        aiApr: Number(aiApr.toFixed(1)),
        maxApr: Number(maxApr.toFixed(1)),
        outcome: null,
        matchedPartner: null,

        // Compatibility aliases for existing pages (avoid brittle mass refactors)
        hp: hiddenPrime,
        loan_amount: amount,
        hidden_prime: hiddenPrime,
        risk_score: Number(riskScore.toFixed(3)),
        p_default: Number(pDefault.toFixed(3)),
        clearing_apr: clearingApr,
        matched_partner: null,
      });
    }

    return borrowers;
  }

  function exportDataset(borrowers, format = 'json') {
    if (!Array.isArray(borrowers)) return '';

    if (format === 'csv') {
      const headers = [
        'id', 'name', 'fico', 'income', 'amount', 'purpose', 'hiddenPrime',
        'riskScore', 'pDefault', 'classicApr', 'aiApr', 'maxApr', 'clearingApr', 'outcome', 'matchedPartner',
      ];

      const rows = borrowers.map((b) => headers.map((h) => JSON.stringify(b[h] ?? '')).join(','));
      return [headers.join(','), ...rows].join('\n');
    }

    const avgFico = borrowers.length
      ? Math.round(borrowers.reduce((sum, b) => sum + (b.fico || 0), 0) / borrowers.length)
      : 0;

    const hiddenPrimeRate = borrowers.length
      ? borrowers.filter((b) => b.hiddenPrime).length / borrowers.length
      : 0;

    return JSON.stringify(
      {
        metadata: {
          generated_date: new Date().toISOString(),
          sample_size: borrowers.length,
          parameters: {
            avg_fico: avgFico,
            hidden_prime_rate: hiddenPrimeRate,
            distribution_type: 'Box-Muller Gaussian (FICO), LogNormal (loan amount)',
          },
        },
        borrowers,
      },
      null,
      2,
    );
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

  window.borrowerGeneration = {
    gauss,
    clamp,
    lognorm,
    classicAPR,
    borrowerMaxAPR,
    calculateRiskScore,
    calculatePDefault,
    choosePurpose,
    estimateIncome,
    generateBorrowerFull,
    exportDataset,
    downloadFile,
  };
})();

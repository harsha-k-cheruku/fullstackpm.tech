(function () {
  'use strict';

  const RISK_ORDER = ['A', 'B', 'C', 'D', 'E'];

  const CURRENT_TRANSITIONS = {
    A: { stayCurrent: 0.985, to30dpd: 0.005, earlyPayoff: 0.01 },
    B: { stayCurrent: 0.975, to30dpd: 0.01, earlyPayoff: 0.015 },
    C: { stayCurrent: 0.955, to30dpd: 0.025, earlyPayoff: 0.02 },
    D: { stayCurrent: 0.93, to30dpd: 0.045, earlyPayoff: 0.025 },
    E: { stayCurrent: 0.9, to30dpd: 0.07, earlyPayoff: 0.03 },
  };

  const DPD30_TRANSITIONS = {
    A: { recover: 0.7, worsen: 0.3 },
    B: { recover: 0.6, worsen: 0.4 },
    C: { recover: 0.5, worsen: 0.5 },
    D: { recover: 0.4, worsen: 0.6 },
    E: { recover: 0.3, worsen: 0.7 },
  };

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function riskGradeFromFico(fico) {
    if (fico >= 740) return 'A';
    if (fico >= 700) return 'B';
    if (fico >= 660) return 'C';
    if (fico >= 620) return 'D';
    return 'E';
  }

  function improveGrade(grade) {
    const idx = RISK_ORDER.indexOf(grade);
    if (idx <= 0) return grade;
    return RISK_ORDER[idx - 1];
  }

  function mulberry32(seed) {
    let t = seed;
    return function rand() {
      t += 0x6d2b79f5;
      let x = Math.imul(t ^ (t >>> 15), 1 | t);
      x ^= x + Math.imul(x ^ (x >>> 7), 61 | x);
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  }

  function monthlyPayment(principal, annualRate, termMonths) {
    const r = annualRate / 100 / 12;
    if (r <= 0) return principal / termMonths;
    return principal * r / (1 - Math.pow(1 + r, -termMonths));
  }

  function getTransitionProbs(borrower, config) {
    const defaults = {
      baseDefaultRate: 1,
      earlyPayoffRate: 1,
      recoveryRate: 1,
    };
    const cfg = { ...defaults, ...(config || {}) };

    let grade = borrower.riskGrade;
    if (borrower.hiddenPrime) grade = improveGrade(grade);

    if (borrower.status === 'current') {
      const base = CURRENT_TRANSITIONS[grade];
      const to30 = clamp(base.to30dpd * cfg.baseDefaultRate, 0, 0.95);
      const early = clamp(base.earlyPayoff * cfg.earlyPayoffRate, 0, 0.95);
      const stay = clamp(1 - to30 - early, 0, 1);
      return {
        pOnTime: stay,
        pLate30: to30,
        pEarlyPayoff: early,
        pLate60: 0,
        pLate90: 0,
        pDefault: 0,
      };
    }

    if (borrower.status === '30dpd') {
      const base = DPD30_TRANSITIONS[grade];
      const recover = clamp(base.recover * cfg.recoveryRate, 0, 1);
      return {
        pRecover: recover,
        pWorsen: clamp(1 - recover, 0, 1),
      };
    }

    if (borrower.status === '60dpd') {
      const recover = clamp(0.2 * cfg.recoveryRate, 0, 1);
      return { pRecover: recover, pWorsen: clamp(1 - recover, 0, 1) };
    }

    if (borrower.status === '90dpd') {
      const recover = clamp(0.05 * cfg.recoveryRate, 0, 1);
      return { pRecover: recover, pWorsen: clamp(1 - recover, 0, 1) };
    }

    return {};
  }

  function computePartnerMetrics(loans, partner) {
    const fundedLoans = loans.filter((l) => l.matchedPartnerId === partner.id || (partner.id === 'balance_sheet' && l.partnerType === 'bs'));

    const totalFunded = fundedLoans.reduce((sum, l) => sum + l.amount, 0);
    const active = fundedLoans.filter((l) => ['current', '30dpd', '60dpd', '90dpd'].includes(l.status)).length;
    const defaulted = fundedLoans.filter((l) => l.status === 'default').length;
    const epd = fundedLoans.filter((l) => l.status === 'default' && l.defaultMonth != null && l.defaultMonth <= 3).length;

    const totalInterest = fundedLoans.reduce((sum, l) => sum + l.totalInterestPaid, 0);
    const losses = fundedLoans.filter((l) => l.status === 'default').reduce((sum, l) => sum + (l.remainingBalanceAtDefault || l.remainingBalance || 0), 0);

    const avgMonths = fundedLoans.length
      ? fundedLoans.reduce((sum, l) => sum + l.monthsActive, 0) / fundedLoans.length
      : 1;

    const netReturn = totalInterest - losses;
    const annualizedYield = totalFunded > 0
      ? (netReturn / totalFunded) * (12 / Math.max(1, avgMonths)) * 100
      : 0;

    const lossRate = totalFunded > 0 ? (losses / totalFunded) * 100 : 0;
    const epdRate = fundedLoans.length ? (epd / fundedLoans.length) * 100 : 0;

    return {
      partnerId: partner.id,
      partnerName: partner.name,
      fundedCount: fundedLoans.length,
      totalFunded,
      activeCount: active,
      defaultedCount: defaulted,
      annualizedYield,
      lossRate,
      epdRate,
      utilizationPct: partner.cap ? clamp((totalFunded / partner.cap) * 100, 0, 100) : null,
    };
  }

  function computeUpstartMetrics(portfolio) {
    const loans = portfolio.loans;
    const funded = loans.filter((l) => l.initiallyFunded);
    const bsFunded = funded.filter((l) => l.partnerType === 'bs');

    const cumulativeFees = funded.reduce((sum, l) => sum + (l.amount * 0.03), 0);
    const bsExposurePct = funded.length ? (bsFunded.length / funded.length) * 100 : 0;
    const revenuePerLoan = funded.length ? cumulativeFees / funded.length : 0;

    const defaults = loans.filter((l) => l.status === 'default');
    const avgPred = defaults.length
      ? defaults.reduce((s, l) => s + (l.pDefault || 0), 0) / defaults.length
      : 0;
    const modelAccuracy = clamp((1 - Math.abs(avgPred - 0.08)) * 100, 50, 99);

    return {
      cumulativeFees,
      bsExposurePct,
      revenuePerLoan,
      modelAccuracy,
      clearingEfficiencyPct: portfolio.initialClearingRate || 0,
    };
  }

  function computeBorrowerMetrics(portfolio) {
    const loans = portfolio.loans;
    const active = loans.filter((l) => ['current', '30dpd', '60dpd', '90dpd'].includes(l.status));
    const delinquent = loans.filter((l) => ['30dpd', '60dpd', '90dpd'].includes(l.status));
    const defaults = loans.filter((l) => l.status === 'default');
    const paid = loans.filter((l) => l.status === 'paid_off' || l.status === 'early_payoff');

    return {
      totalLoans: loans.length,
      activeLoans: active.length,
      delinquentRatePct: active.length ? (delinquent.length / active.length) * 100 : 0,
      defaultRatePct: loans.length ? (defaults.length / loans.length) * 100 : 0,
      completionRatePct: loans.length ? (paid.length / loans.length) * 100 : 0,
    };
  }

  function initPortfolio(clearedLoans, partners) {
    const seed = 202605;
    const rand = mulberry32(seed);

    const loans = (clearedLoans || [])
      .filter((l) => l.outcome === 'CLEARED' || l.outcome === 'BALANCE_SHEET')
      .map((loan) => {
        const amount = loan.amount ?? loan.loan_amount;
        const apr = loan.offeredApr ?? loan.aiApr ?? loan.clearingApr ?? 18;
        const termMonths = 36;
        const pmt = monthlyPayment(amount, apr, termMonths);

        return {
          ...loan,
          amount,
          offeredApr: apr,
          riskGrade: riskGradeFromFico(loan.fico),
          hiddenPrime: loan.hiddenPrime ?? loan.hidden_prime ?? loan.hp ?? false,
          status: 'current',
          month: 0,
          monthsActive: 0,
          termMonths,
          monthlyPayment: pmt,
          remainingBalance: amount,
          totalPaid: 0,
          totalInterestPaid: 0,
          totalPrincipalPaid: 0,
          defaultMonth: null,
          remainingBalanceAtDefault: 0,
          paymentHistory: [],
          initiallyFunded: true,
          rngSeed: Math.floor(rand() * 1_000_000),
        };
      });

    return {
      seed,
      month: 0,
      loans,
      partners: JSON.parse(JSON.stringify(partners || [])),
      interventions: [],
      snapshots: [],
      initialClearingRate: loans.length,
    };
  }

  function nextRandom(loan, month) {
    const rand = mulberry32(loan.rngSeed + month * 7919);
    return rand();
  }

  function stepMonth(portfolio, month, config) {
    portfolio.month = month;

    portfolio.loans = portfolio.loans.map((loan) => {
      if (['default', 'paid_off', 'early_payoff'].includes(loan.status)) {
        return loan;
      }

      const updated = { ...loan, month, monthsActive: loan.monthsActive + 1, paymentHistory: [...(loan.paymentHistory || [])] };
      const probs = getTransitionProbs(updated, config);
      const roll = nextRandom(updated, month);

      if (updated.status === 'current') {
        const r1 = probs.pOnTime;
        const r2 = r1 + probs.pLate30;

        if (roll <= r1) {
          const interest = updated.remainingBalance * (updated.offeredApr / 100 / 12);
          const principal = Math.max(0, Math.min(updated.monthlyPayment - interest, updated.remainingBalance));
          updated.remainingBalance = Math.max(0, updated.remainingBalance - principal);
          updated.totalPaid += updated.monthlyPayment;
          updated.totalInterestPaid += interest;
          updated.totalPrincipalPaid += principal;
          if (updated.remainingBalance <= 5 || updated.monthsActive >= updated.termMonths) {
            updated.status = 'paid_off';
            updated.remainingBalance = 0;
            updated.paymentHistory.push('paid_off');
          } else {
            updated.paymentHistory.push('current');
          }
          return updated;
        }

        if (roll <= r2) {
          updated.status = '30dpd';
          updated.paymentHistory.push('30dpd');
          return updated;
        }

        updated.status = 'early_payoff';
        updated.totalPrincipalPaid += updated.remainingBalance;
        updated.totalPaid += updated.remainingBalance;
        updated.remainingBalance = 0;
        updated.paymentHistory.push('early_payoff');
        return updated;
      }

      if (updated.status === '30dpd' || updated.status === '60dpd' || updated.status === '90dpd') {
        if (roll <= probs.pRecover) {
          updated.status = updated.status === '90dpd' ? '60dpd' : 'current';
          updated.paymentHistory.push(updated.status);
          return updated;
        }

        if (updated.status === '30dpd') updated.status = '60dpd';
        else if (updated.status === '60dpd') updated.status = '90dpd';
        else {
          updated.status = 'default';
          updated.defaultMonth = month;
          updated.remainingBalanceAtDefault = updated.remainingBalance;
        }
        updated.paymentHistory.push(updated.status);
      }

      return updated;
    });

    const partnerMetrics = portfolio.partners.map((p) => computePartnerMetrics(portfolio.loans, p));
    const upstartMetrics = computeUpstartMetrics(portfolio);
    const borrowerMetrics = computeBorrowerMetrics(portfolio);

    const statusCounts = portfolio.loans.reduce((acc, loan) => {
      acc[loan.status] = (acc[loan.status] || 0) + 1;
      return acc;
    }, {});

    const snapshot = {
      month,
      statusCounts,
      partnerMetrics,
      upstartMetrics,
      borrowerMetrics,
      interventions: [...portfolio.interventions],
    };

    portfolio.snapshots.push(snapshot);

    return { portfolio, snapshot };
  }

  function applyIntervention(portfolio, partnerId, changes) {
    portfolio.partners = portfolio.partners.map((p) => {
      if (p.id !== partnerId) return p;
      return {
        ...p,
        minFICO: changes.ficoFloor ?? p.minFICO,
        cap: changes.capacity ?? p.cap,
        on: changes.enabled ?? p.on,
      };
    });

    portfolio.interventions.push({
      month: portfolio.month,
      partnerId,
      changes,
      timestamp: new Date().toISOString(),
    });

    return portfolio;
  }

  window.lifecycleEngine = {
    initPortfolio,
    stepMonth,
    getTransitionProbs,
    computePartnerMetrics,
    computeUpstartMetrics,
    computeBorrowerMetrics,
    applyIntervention,
    monthlyPayment,
  };
})();

(function () {
  'use strict';

  const PARTNER_LOAN_RANGES = {
    ff: [3000, 40000],
    bank: [5000, 35000],
    spot: [2000, 50000],
  };

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function checkEligibility(borrower, partner, remainingCapacity) {
    const [minAmt, maxAmt] = PARTNER_LOAN_RANGES[partner.type] || [2000, 50000];
    const purposeOk = borrower.purpose !== 'Small Business';
    const ficoOk = borrower.fico >= partner.minFICO;
    const amountOk = borrower.amount >= minAmt && borrower.amount <= maxAmt;
    const capacityOk = partner.cap == null ? true : remainingCapacity >= borrower.amount;

    return {
      eligible: purposeOk && ficoOk && amountOk && capacityOk,
      checks: { purposeOk, ficoOk, amountOk, capacityOk },
    };
  }

  function priceLoan(borrower, modelType) {
    const classicApr = borrowerGeneration.classicAPR(borrower.fico);
    const isHiddenPrime = borrower.hiddenPrime || borrower.hidden_prime || borrower.hp;

    let offeredApr = classicApr;
    if (modelType === 'model18') {
      if (isHiddenPrime) {
        offeredApr = clamp(classicApr - clamp(borrowerGeneration.gauss(8.2, 1.2), 5, 12), 9, 40);
      } else {
        offeredApr = clamp(classicApr - clamp(borrowerGeneration.gauss(1.0, 0.8), 0, 3), 9, 40);
      }
    }

    const maxApr = borrowerGeneration.borrowerMaxAPR(borrower.fico, 2, !!isHiddenPrime);
    const basePDefault = borrowerGeneration.calculatePDefault(borrower.fico, !!isHiddenPrime);
    const pDefault = clamp(basePDefault - ((classicApr - offeredApr) * 0.0015), 0.01, 0.2);

    return {
      classicApr: Number(classicApr.toFixed(1)),
      offeredApr: Number(offeredApr.toFixed(1)),
      maxApr: Number(maxApr.toFixed(1)),
      pDefault: Number(pDefault.toFixed(3)),
      borrowerAccepts: offeredApr <= maxApr,
    };
  }

  function waterfallRoute(borrower, priced, eligiblePartners, allocations, activePartners) {
    if (!priced.borrowerAccepts) {
      return { outcome: 'APR_REJECTED', matchedPartner: null, partnerType: null };
    }

    for (const partner of eligiblePartners.sort((a, b) => a.pri - b.pri)) {
      if (!activePartners.includes(partner.id)) continue;
      if (priced.offeredApr < partner.minAPR) continue;
      if (partner.cap != null && allocations[partner.id] < borrower.amount) continue;

      if (partner.cap != null) {
        allocations[partner.id] -= borrower.amount;
      }

      return {
        outcome: 'CLEARED',
        matchedPartner: partner.name,
        matchedPartnerId: partner.id,
        partnerType: partner.type,
      };
    }

    return {
      outcome: 'BALANCE_SHEET',
      matchedPartner: 'Upstart Balance Sheet',
      matchedPartnerId: 'balance_sheet',
      partnerType: 'bs',
    };
  }

  function runClearing(borrowers, partners, modelType) {
    const allocations = {};
    const activePartners = partners.filter((p) => p.on !== false).map((p) => p.id);

    partners.forEach((p) => {
      allocations[p.id] = p.cap == null ? Infinity : p.cap;
    });

    const results = borrowers.map((borrower) => {
      const normalized = {
        ...borrower,
        amount: borrower.amount ?? borrower.loan_amount,
        hiddenPrime: borrower.hiddenPrime ?? borrower.hidden_prime ?? borrower.hp ?? false,
      };

      const eligiblePartners = partners.filter((partner) =>
        checkEligibility(normalized, partner, allocations[partner.id]).eligible,
      );

      if (eligiblePartners.length === 0) {
        return {
          ...normalized,
          offeredApr: null,
          outcome: 'NO_PARTNER',
          matchedPartner: null,
          matchedPartnerId: null,
          partnerType: null,
        };
      }

      const priced = priceLoan(normalized, modelType);
      const route = waterfallRoute(normalized, priced, eligiblePartners, allocations, activePartners);

      return {
        ...normalized,
        offeredApr: priced.offeredApr,
        classicApr: priced.classicApr,
        maxApr: priced.maxApr,
        pDefault: priced.pDefault,
        outcome: route.outcome,
        matchedPartner: route.matchedPartner,
        matchedPartnerId: route.matchedPartnerId,
        partnerType: route.partnerType,
      };
    });

    const total = results.length;
    const cleared = results.filter((r) => r.outcome === 'CLEARED' || r.outcome === 'BALANCE_SHEET');
    const bsCount = results.filter((r) => r.outcome === 'BALANCE_SHEET').length;
    const aprRejected = results.filter((r) => r.outcome === 'APR_REJECTED').length;
    const noPartner = results.filter((r) => r.outcome === 'NO_PARTNER').length;
    const hiddenPrimeUnlocked = results.filter((r) => (r.hiddenPrime || r.hidden_prime || r.hp) && (r.outcome === 'CLEARED' || r.outcome === 'BALANCE_SHEET')).length;

    const avgApr = cleared.length
      ? cleared.reduce((sum, r) => sum + (r.offeredApr || 0), 0) / cleared.length
      : 0;

    return {
      loans: results,
      summary: {
        total,
        cleared: cleared.length,
        clearingRatePct: total ? (cleared.length / total) * 100 : 0,
        bsExposurePct: cleared.length ? (bsCount / cleared.length) * 100 : 0,
        avgApr,
        aprRejected,
        noPartner,
        hiddenPrimeUnlockedPct: cleared.length ? (hiddenPrimeUnlocked / cleared.length) * 100 : 0,
      },
    };
  }

  window.clearingEngine = {
    runClearing,
    checkEligibility,
    priceLoan,
    waterfallRoute,
  };
})();

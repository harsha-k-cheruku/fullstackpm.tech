# Product Deep Dive Plan: A/B Testing & Experimentation

**For:** Code Puppy | **Status:** Ready to implement | **Complexity:** High | **Build time:** 2.5 hours

---

## Quick Reference

**Q1 Analogy:** "The scientific method, applied to product decisions."

**Q2 Mechanism:**
```
Hypothesis Formation → Experiment Design → Traffic Allocation → Data Collection → Statistical Analysis → Decision & Learning
```

**Q3 Cross-Model Variation:**

| Dimension | Tech (Google) | E-commerce (Amazon) | Social (TikTok) | SaaS (Stripe) | Media (Netflix) |
|-----------|---------------|-------------------|---|---|---|
| **Experiment velocity** | Millions/year (10k+/day) | Thousands/year | Thousands/year (rapid iteration) | Hundreds/year (careful) | Hundreds/year |
| **Typical test size** | 1-2% traffic (huge scale) | 5-10% traffic | 10-20% traffic | 50%+ traffic (smaller user base) | 10-50% traffic |
| **Time-to-decision** | Days (fast infrastructure) | Weeks (statistical rigor) | Days (rapid feedback) | Weeks (customer impact matters) | Weeks (subscription metric lags) |
| **False positive rate tolerance** | <1% (at scale, even 1% = millions wasted) | 2-5% acceptable | 2-5% acceptable | <1% (customer trust) | <1% (subscriber satisfaction) |
| **Metric movement threshold** | >0.1% lift is significant (scale matters) | >1% lift triggers decision | >2% lift good, >0.5% sometimes ships | >5% lift required (sample size) | >3% lift required (variance) |
| **Infrastructure complexity** | Ultra-sophisticated (proprietary) | Very sophisticated (homegrown) | Sophisticated | Moderate (bought solution like Statsig) | Moderate |

**Q4 Metrics:**
- Experiment velocity (# of experiments launched/month)
- Confidence in experiment results (false positive rate)
- Time-to-statistical-significance (days to reach conclusion)
- Learning velocity (how fast are we learning?)
- Experiment ROI (time spent experimenting vs value gained)

**Q5 Hard Problems:**
1. **Multiple comparisons problem** — Run 100 tests, by chance 5 will show statistical significance. How to avoid false positives?
2. **Sample size / power tradeoff** — Large test size = accurate but slow. Small = fast but unreliable.
3. **Metric interactions** — Moving one metric might hurt another (clickthrough vs retention). How to account?
4. **Novelty bias** — New feature = temporary lift (users curious). Does lift persist?
5. **Variance & noise** — Hard to detect small improvements in noisy metrics. How to design experiments to reduce noise?
6. **Decisions with incomplete data** — Can't wait for significance. When to ship a borderline result?

---

## Content Summary

### Section 1: What & Why
- Opening: "The scientific method, applied to product decisions."
- Purpose: Replace "gut feel" with data. Test hypotheses. Reduce risk of bad decisions.
- Tension: Speed (ship fast) vs rigor (statistically significant). False negatives (kill good ideas) vs false positives (ship bad ideas).
- Visual: Intuition-driven decisions (often wrong) vs hypothesis-driven experimentation (data grounded)

### Section 2: How It Works (7-node flow)
1. Hypothesis formation (if we change X, metric Y will improve because of reason Z)
2. Experiment design (sample size, duration, success criteria)
3. Implementation (code the treatment variant, set up traffic allocation)
4. Data collection (run the test, collect metrics)
5. Statistical analysis (is the difference statistically significant?)
6. Decision (ship, iterate, or kill)
7. Learning & scaling (document learnings, iterate on winner)

### Section 3: Across Business Models
- 5-column table above
- Callout: "Google runs millions of experiments (scale + infrastructure). TikTok runs thousands (rapid iteration on recommendations). Netflix runs hundreds (subscription metric is expensive to move)."

### Section 4: Metrics (8 cards)
1. **Experiment velocity** — # of launched experiments/month. Benchmark: 1-10 depending on company size
2. **Time-to-significance** — Days to reach statistical significance. Benchmark: 7-30 days (depends on metric variance)
3. **False positive rate** — % of statistically significant results that didn't replicate. Benchmark: <5% (should be <2.5% ideally)
4. **Statistical power** — Ability to detect true effect. Benchmark: 80%+ power (detect if true improvement >desired minimum)
5. **Experiment impact** — % improvement in North Star from experiments. Benchmark: 5-20%/year (varies by maturity)
6. **Confidence interval width** — Precision of estimate. Narrow = precise. Benchmark: <1% width for core metrics
7. **Mínimum detectable effect (MDE)** — Smallest improvement you can detect. Benchmark: 1-5% depending on metric
8. **Decision quality** — Reverse rate (% of shipped experiments that were later reversed). Benchmark: <10% (higher = poor decision-making)

### Section 5: Architecture (4 layers)
1. **Experiment Allocation** — Traffic splitting (A/B, A/B/C/D, multivariate), bucketing algorithm (deterministic, stable)
2. **Variant Serving** — Feature flags (gradual rollout), configuration management, remote config
3. **Data Collection & Analysis** — Event tracking, metric computation, statistical tests (t-test, Bayesian)
4. **Dashboard & Reporting** — Experiment results, confidence intervals, learning logs

### Section 6: Challenges (6 cards)
1. **Multiple comparisons problem** — Run 100 tests, 5 false positives by chance. Solution: Bonferroni correction, pre-register metrics, lower alpha (0.01 instead of 0.05)
2. **Sample size calculation** — Too small = no significance, too large = slow. Solution: Power analysis, effect size estimation from prior experiments
3. **Novelty bias** — Users try new feature (temporary boost). Solution: Run longer, analyze early vs late periods separately, holdout controls
4. **Metric interactions** — Improve clickthrough but hurt retention. Solution: Monitor multiple metrics, use composite metrics (like revenue)
5. **Variance & noise** — Hard to detect small improvements. Solution: Reduce noise (CUPED variance reduction), stratify analysis, increase sample size
6. **Incomplete data decisions** — Borderline p-value (0.06). Ship or not? Solution: Define decision rules in advance (sequential analysis, Bayesian thresholds)

### Section 7: Patterns (4 companies)
1. **Google** — Massive scale (millions experiments/year). Sophisticated infrastructure. Focus on novelty + interaction effects. High velocity = can ship with <1% lift.
2. **Amazon** — Careful experimentation (statistical rigor). Pre-registered metrics. Long runways (weeks). Account for seasonality, user segments. Extensive post-launch monitoring.
3. **Netflix** — Long experiment duration (subscriber metrics are slow). Multiple holdout controls. Focus on retention + satisfaction. Deep metric interactions (content quality + UX).
4. **Stripe** — Careful (customer trust). Longer runways. Higher MDE (require >5% improvement). Extensive manual review before shipping changes.

---

## Build Instructions

**Files:** 11 total

**CSS Variables (Fuchsia/Pink for testing):**
```css
--dd-ex-primary: #d946ef;     /* Fuchsia */
--dd-ex-secondary: #c026d3;
--dd-ex-accent: #f0abfc;
--dd-ex-bg: #fdf2f8;
--dd-ex-border: #f0abfc;
--dd-ex-text: #831843;
```

**Key sections:**
- S1: Hypothesis-driven development
- S2: 7-node experimentation pipeline
- S3: Google, Amazon, Netflix, Stripe comparison
- S4: Experiment velocity, time-to-significance, false positive rate, power
- S5: Traffic allocation, variant serving, data collection, reporting
- S6: Multiple comparisons, sample size, novelty bias, metric interactions, variance, incomplete data
- S7: Google, Amazon, Netflix, Stripe patterns

**Route:** `/resources/product-breakdowns/experimentation`
**Gallery slug:** `experimentation.html`


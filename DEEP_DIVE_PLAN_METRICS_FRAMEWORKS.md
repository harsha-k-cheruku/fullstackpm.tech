# Product Deep Dive Plan: Product Metrics Frameworks

**For:** Code Puppy | **Status:** Ready to implement | **Complexity:** Medium | **Build time:** 2 hours

---

## Quick Reference

**Q1 Analogy:** "The dashboard that tells you if you're winning or losing."

**Q2 Mechanism:**
```
Define Business Goal → Identify Metrics (North Star) → Break Into Sub-metrics → Set Targets → Monitor & Alert → Iterate
```

**Q3 Cross-Model Variation:**

| Dimension | SaaS (Stripe) | Marketplace (Airbnb) | Social (TikTok) | Media (Netflix) | Fintech (Wise) |
|-----------|---------------|---------------------|---|---|---|
| **North Star** | Payment volume ($) | GMV (gross booking value) | Watch time (hours) | Hours watched / completion rate | Transfer volume ($) |
| **Sub-metric 1** | API transactions | Bookings (supply × demand) | Users (DAU) | Subscriber growth | Transfer growth |
| **Sub-metric 2** | Chargeback rate | Conversion (browse → book) | Engagement (time per session) | Retention (D30) | Transfer success rate |
| **Sub-metric 3** | Developer NPS | Host satisfaction | Creator growth | Churn rate | Fraud rate |
| **Audit frequency** | Weekly | Weekly | Daily | Daily | Daily |
| **Revision frequency** | Quarterly | Quarterly | Monthly (trends) | Quarterly | Monthly (fraud changes) |

**Q4 Metrics (meta!):**
- Metric health (are we measuring accurately?)
- Metric coverage (% of company objectives covered by metrics?)
- Metric alignment (do all teams have same metrics?)
- Decision impact (% of decisions actually use metrics?)

**Q5 Hard Problems:**
1. **Metric misalignment** — Different teams measure differently. Sales counts deals different than finance. Who's right?
2. **Gaming metrics** — Incentivize metric = team optimizes for metric, not business. (VanityMetrics problem)
3. **Lagging indicators** — Important metrics lag reality. Quarterly revenue metric = slow decision loop.
4. **Correlation vs causation** — Metric goes up ≠ your action caused it. Could be seasonal, external factors.
5. **Too many metrics** — Track 50 metrics = track none. Attention is scarce. What's actually important?
6. **Unmeasurable qualitative goals** — "Great customer experience" = can't measure directly. How to operationalize?

---

## Content Summary

### Section 1: What & Why
- Opening: "The dashboard that tells you if you're winning or losing."
- Purpose: Give teams shared language (one metric, one truth) + alignment + accountability
- Tension: Simplicity (few metrics, focus) vs completeness (cover all business levers)
- Visual: OMTM (One Metric That Matters) pyramid vs bloated metrics dashboards

### Section 2: How It Works (7-node flow)
1. Define business goal (what are we optimizing for? Revenue? Growth? Retention?)
2. Identify North Star metric (the ONE metric that indicates success)
3. Break into sub-metrics (what drives North Star?)
4. Set targets (what's good performance?)
5. Monitor & report (track weekly, alert on anomalies)
6. Investigate changes (why did metric move?)
7. Adjust strategy (iterate based on learnings)

### Section 3: Across Business Models
- 5-column table above
- Callout: "Stripe's North Star is payment volume (revenue driver). TikTok's is watch time (engagement driver). They're different because business models are different."

### Section 4: Metrics (8 cards)
1. **North Star metric clarity** — % of company who can articulate North Star. Benchmark: 80%+ (if <50%, metric is unclear)
2. **Metric alignment** — % of teams using same metric definition. Benchmark: 100% for core metrics (misalignment = disaster)
3. **Sub-metric coverage** — % of metric drivers covered by dashboards. Benchmark: 80%+ (should track what moves North Star)
4. **Metric timeliness** — Hours from event to dashboard update. Benchmark: real-time to hourly for core metrics
5. **Gaming incidents** — # of times metric was optimized against business goal. Benchmark: <1 incident/quarter (if higher, metrics are poorly designed)
6. **Metric trust score** — % of company who trusts metrics. Benchmark: 70%+ (trust = they use metrics for decisions)
7. **Decision velocity** — # of decisions made per week based on metrics. Benchmark: 5-20 (varies by company size)
8. **Metric ROI** — Time saved / time spent on metric tracking. Benchmark: 10:1 (for every hour tracking, save 10 hours in bad decisions)

### Section 5: Architecture (4 layers)
1. **Metric Definition** — How each metric is calculated, formula, data source, owner
2. **Data Pipeline** — Collect raw events, aggregate, compute metrics nightly/hourly
3. **Visualization** — Dashboards (Looker, Tableau), alerts, reporting
4. **Governance** — Single source of truth, metric definitions documented, change control

### Section 6: Challenges (6 cards)
1. **Metric misalignment** — Different teams measure differently (Sales: closed deals, Finance: revenue recognized). Solution: Single source of truth, definition docs, reconciliation
2. **Gaming metrics** — Sales optimizes for deals-won, but many are unprofitable. Solution: Multi-metric system (add profitability score), audit for gaming
3. **Lagging indicators** — Revenue metric is quarterly. Can't iterate fast. Solution: Leading indicators (pipeline, opportunity count) + lag metrics
4. **Vanity metrics** — Increased signups but no revenue. Solution: Focus on actionable metrics (conversion rate) not just magnitude metrics (signups)
5. **Too many dashboards** — 50 metrics = no clarity. Solution: Hierarchy (North Star → sub-metrics), ruthless simplification
6. **Unmeasurable goals** — "Improve customer experience" isn't measurable. Solution: Operationalize (CSAT score, NPS, support ticket count)

### Section 7: Patterns (4 companies)
1. **Airbnb** — North Star: nights booked. Sub-metrics: supply (# listings), demand (# bookings), conversion (browse → book), retention (repeat guests). Weekly reviews.
2. **Stripe** — North Star: payment volume ($). Sub-metrics: API transactions, developer NPS, chargeback rate, transaction success rate.
3. **Netflix** — North Star: hours watched (completion rate). Sub-metrics: subscriber growth, retention (D30), engagement (hours/user/month), churn.
4. **Twitter** — North Star was (historically) MAU. Now Daily Active Users. Sub-metrics: time spent, engagement (retweets), creator growth. Daily tracking.

---

## Build Instructions

**Files:** 11 total

**CSS Variables (Emerald/Green for measurement):**
```css
--dd-mf-primary: #059669;     /* Emerald */
--dd-mf-secondary: #047857;
--dd-mf-accent: #10b981;
--dd-mf-bg: #ecfdf5;
--dd-mf-border: #6ee7b7;
--dd-mf-text: #064e3b;
```

**Key sections:**
- S1: One metric that matters (OMTM)
- S2: 7-node metrics framework pipeline
- S3: Airbnb, Stripe, Netflix, Twitter comparison
- S4: Metric clarity, alignment, coverage, timeliness
- S5: Metric definition, data pipeline, visualization, governance
- S6: Misalignment, gaming, lagging indicators, vanity metrics, too many, unmeasurable
- S7: Airbnb, Stripe, Netflix, Twitter patterns

**Route:** `/resources/product-breakdowns/product-metrics-frameworks`
**Gallery slug:** `product_metrics_frameworks.html`


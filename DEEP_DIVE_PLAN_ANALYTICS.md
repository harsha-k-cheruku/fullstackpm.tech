# Product Deep Dive Plan: Analytics & Data Platform

**For:** Code Puppy | **Status:** Ready to implement | **Complexity:** High | **Build time:** 2.5 hours

---

## Quick Reference

**Q1 Analogy:** "The nervous system that tells the brain what the body is doing."

**Q2 Mechanism:**
```
Event Collection → Ingestion Pipeline → Storage & Warehouse → Metrics Computation → Visualization & API → Decision Making
```

**Q3 Cross-Model Variation:**

| Dimension | Marketplace (Uber) | SaaS (Stripe) | Media (TikTok) | Fintech (Wise) | E-commerce (Amazon) |
|-----------|-------------------|---------------|---|---|---|
| **Metrics #1** | Trips/bookings | API calls/volume | Watch time | Transaction count | Orders / revenue |
| **Metrics #2** | Pickup time | Uptime/latency | User engagement | Transfer success rate | Conversion rate |
| **Metrics #3** | Driver earnings | Churn rate | Creator growth | Fraud rate | Return rate |
| **Event volume/day** | Millions | Billions | Billions | Millions | Billions |
| **Latency requirement** | Real-time (10s, dashboard) | Real-time (API clients polling) | Real-time (ranking) | Real-time (fraud detection) | Batch (nightly reporting) |
| **Retention policy** | Keep 2+ years (operational) | Keep 7+ years (regulatory) | Keep 90 days (trends matter, not history) | Keep 7+ years (regulatory + compliance) | Keep 3+ years (warehouse) |
| **Key challenge** | Real-time fraud + operational (two pipelines) | Compliance + cost (7 years = big data) | Freshness (model retraining hourly) | Audit trail (immutable ledger) | Cost (petabyte scale) |

**Q4 Metrics:**
- Event ingestion latency (lag from event to warehouse)
- Query latency (seconds to answer a metric question)
- Data freshness (how old is the data in dashboard?)
- Data accuracy (do metrics match reality?)
- Dashboard adoption (% of team using analytics)
- Cost per GB stored

**Q5 Hard Problems:**
1. **Real-time vs batch tradeoff** — Real-time = fresh data but expensive. Batch = cheap but stale (hours old).
2. **Data quality** — Missing events, incorrect timestamps, duplicate events. How to clean?
3. **Cardinality explosion** — 1000 metrics × 100 dimensions = millions of combinations. Query becomes slow.
4. **Privacy + analytics** — Track user behavior = privacy concerns. How to anonymize?
5. **Cost at scale** — 1B events/day = petabytes/month. Storage + compute = millions/month.
6. **Governance** — Who owns the truth? If two teams measure same metric differently, who's right?

---

## Content Summary

### Section 1: What & Why
- Opening: "The nervous system that tells the brain what the body is doing."
- Two purposes: Operational (Is system working right now?) vs Strategic (How do we grow?)
- Tension: Fresh data (expensive) vs cheap data (stale)
- Visual: Real-time ops dashboard vs nightly strategy dashboard

### Section 2: How It Works (7-node flow)
1. Event generation (user action, system event)
2. Collection (send event to analytics service)
3. Ingestion (ingest into pipeline, validate)
4. Storage (warehouse, append-only, indexed)
5. Computation (nightly/hourly aggregation)
6. Metrics serving (API to fetch metrics)
7. Visualization (dashboards, alerts, reports)

### Section 3: Across Business Models
- 5-column table above
- Callout: "Uber needs real-time fraud detection (operational). Amazon can batch nightly (strategic planning). TikTok needs hourly model retraining (algorithmic)."

### Section 4: Metrics (8 cards)
1. **Event ingestion latency** — Minutes from event to warehouse. Benchmark: <1 min (batch), <1 sec (real-time)
2. **Query latency** — Time to answer metric question. Benchmark: <1 sec for real-time dashboard
3. **Data freshness** — Age of data in dashboard. Benchmark: real-time (streaming) or hourly (batch)
4. **Data completeness** — % of expected events received. Benchmark: 99.5%+ (missing is red flag)
5. **Dashboard adoption** — % of team using analytics. Benchmark: 60-80% (high adoption = good decision making)
6. **Metric accuracy** — % match to ground truth (manual count). Benchmark: 99%+ for core metrics
7. **Cost per GB** — Storage + compute cost per gigabyte. Benchmark: $0.10-1.00/GB/month depending on tool
8. **Query efficiency** — Queries completed per unit cost. Benchmark: track internally for optimization

### Section 5: Architecture (4 layers)
1. **Event Collection** — SDK/API (capture events from app), validation schema, deduplication, rate limiting
2. **Ingestion Pipeline** — Event queue (Kafka, Pub/Sub), stream processor (Flink, Beam), early aggregation
3. **Storage** — Data warehouse (Snowflake, BigQuery), real-time data stores (Redis, ClickHouse), backups
4. **Metrics & API** — Metrics layer (pre-computed aggregations), BI dashboards (Tableau, Looker), alerting

### Section 6: Challenges (6 cards)
1. **Real-time cost explosion** — Real-time events = 10x cost vs batch. Solution: Hybrid (critical metrics real-time, rest batch), event sampling
2. **Data quality issues** — Missing events, duplicate timestamps. Solution: Schema validation, reconciliation jobs, anomaly detection
3. **Cardinality explosion** — Too many dimension combinations. Solution: Limit dimensions, pre-compute common combos, approximate queries
4. **Privacy concerns** — Tracking behavior = user privacy risk. Solution: Anonymization, differential privacy, aggregate-only queries
5. **Cost at scale** — Petabytes = millions/month in storage. Solution: Tiered storage (hot/cold), compression, archival
6. **Metric ownership conflicts** — Different teams measure differently. Solution: Single source of truth, metric definition docs, data governance

### Section 7: Patterns (4 companies)
1. **Uber** — Dual pipeline: real-time Kafka for operational (fraud, surge pricing) + Hadoop for strategic (long-term trends)
2. **Stripe** — Immutable ledger: event sourcing, audit trail, compliance-focused. 7+ year retention for regulatory.
3. **TikTok** — Near real-time: stream processing for hourly aggregations. Model retraining pipeline tied to metrics.
4. **Amazon** — Scale-first: massive warehouse, 3+ year retention, strong governance (metric definitions).

---

## Build Instructions

**Files:** 11 total

**CSS Variables (Slate/Blue for data):**
```css
--dd-an-primary: #475569;     /* Slate */
--dd-an-secondary: #334155;
--dd-an-accent: #64748b;
--dd-an-bg: #f1f5f9;
--dd-an-border: #cbd5e1;
--dd-an-text: #1e293b;
```

**Key sections:**
- S1: Operational vs strategic analytics
- S2: 7-node analytics pipeline
- S3: Uber, Stripe, TikTok, Amazon comparison
- S4: Latency, freshness, completeness, accuracy metrics
- S5: Collection, ingestion, storage, metrics serving
- S6: Real-time cost, data quality, cardinality, privacy, scale, governance
- S7: Uber, Stripe, TikTok, Amazon patterns

**Route:** `/resources/product-breakdowns/analytics-data-platform`
**Gallery slug:** `analytics_and_data_platform.html`


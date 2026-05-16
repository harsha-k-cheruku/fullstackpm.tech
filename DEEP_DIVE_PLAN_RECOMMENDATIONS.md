# Product Deep Dive Plan: Recommendations & Personalization

**For:** Code Puppy | **Status:** Ready to implement | **Complexity:** High | **Build time:** 2.5 hours

---

## Quick Reference (5 Questions)

**Q1 Analogy:** "The friend who knows your taste better than you do."

**Q2 Core Mechanism:**
```
User Behavior Observation → Feature Extraction → Model Training → Scoring & Ranking → Serving → Feedback Loop
```

**Q3 Cross-Model Variation:**

| Dimension | Social (TikTok) | E-commerce (Amazon) | SaaS (Notion) | Fintech (Square) | Streaming (Spotify) |
|-----------|-----------------|-------------------|---------------|-----------------|-------------------|
| **What's recommended** | Videos (algorithm selects) | Products (related items) | Templates (usage-based) | Features (based on biz type) | Songs/playlists (mood-based) |
| **Recommendation driver** | Watch time + engagement | Purchase history + browsing | Template usage patterns | Merchant profile + sales data | Listening history + taste |
| **Scale of algorithm** | Millions/sec (For You Page) | Thousands/sec (homepage) | Hundreds/min (template gallery) | Tens/min (feature rollout) | Millions/sec (daily mixes) |
| **Cold start problem** | EXTREME (new creators) | HIGH (new products) | MEDIUM (new templates) | LOW (can profile merchant quickly) | MEDIUM (new users) |
| **Ranking signal #1** | Watch time (engagement) | Purchase likelihood | Template download count | Revenue potential | Audio features (genre, tempo) |
| **Ranking signal #2** | Report rates (quality) | Product rating | Creator reputation | Merchant segment | User history similarity |
| **Ranking signal #3** | Follower count (virality) | Price/discount | Recency | Historical performance | Explicit user ratings |
| **Personalization depth** | EXTREME (per user) | HIGH (per user + demographics) | MEDIUM (per user type) | LOW (per merchant segment) | HIGH (per user mood/context) |
| **Latency requirement** | <100ms (real-time) | <500ms (batch OK) | <1s (backend) | <1s (async) | <500ms (on-demand) |
| **Model retraining frequency** | Daily (trends shift fast) | Weekly | Monthly | Quarterly | Daily |
| **False positive cost** | MEDIUM (irrelevant video, skip it) | MEDIUM (wrong product, no buy) | LOW (template not useful, ignore) | LOW (feature not adopted) | LOW (wrong song, skip it) |

**Q4 Key Metrics:**
- Recommendation CTR (% of recommendations clicked)
- Serendipity (% of successful recommendations user wouldn't have found themselves)
- Coverage (% of catalog recommended vs not recommended)
- Diversity (not just the same few items)
- Cold start conversion (new users → recommendations performing well)

**Q5 Hard Problems:**
1. **Cold start** — New users/items have no history. How bootstrap recommendations?
2. **Filter bubbles** — Recommending what user already likes = stale. Where's discovery?
3. **Sparsity** — Most user-item pairs never interact. How to score?
4. **Latency** — Recommendations must be fast. ML models are slow.
5. **Feedback loops** — Recommending item → users see it more → model thinks it's popular → recommends more → creates artificial trends
6. **Fairness** — Model may favor certain creators/products. How to ensure equitable exposure?

---

## Content Summary

### Section 1: What & Why
- Opening: "The friend who knows your taste better than you do."
- Dual purpose: Surface relevant items + discover new items user didn't know existed
- Tension: Relevance vs serendipity (recommending what they like vs surprising them)
- Visual: Two modes — "For You Based on History" vs "Explore New Content"

### Section 2: How It Works (Animated 7-node flow)
1. Observe behavior (views, clicks, purchases, ratings)
2. Feature extraction (user profile, item features, interaction patterns)
3. Model training (collaborative filtering, content-based, hybrid)
4. Scoring (rank all items by predicted user preference)
5. Ranking & filtering (apply business rules, diversity constraints)
6. Serving (return top N recommendations, format for display)
7. Feedback → Loop (track which recommendations convert, retrain)

### Section 3: Across Business Models
- 5-column comparison table (see above)
- Callout: "The tradeoff: TikTok optimizes for watch time (engagement), Netflix optimizes for series completion (retention), Amazon optimizes for purchase likelihood (revenue). Different signals for different business models."

### Section 4: Metrics (8 cards)
1. **Recommendation CTR** — % of recommendations clicked / impressions. Benchmark: 5-20% depending on model quality
2. **Conversion from Recommendations** — % of recommended items purchased/viewed/completed. Benchmark: 2-8%
3. **Coverage** — % of catalog that appears in recommendations. Benchmark: 50-80% (avoid long-tail bias)
4. **Diversity** — % of recommendations from different categories/creators. Benchmark: 40-60% diverse
5. **Serendipity Score** — % of successful recommendations user wouldn't have found themselves. Benchmark: 30-50%
6. **Cold Start Performance** — Conversion rate for new users getting recommendations. Benchmark: 50-70% of warm users
7. **Filter Bubble Score** — How similar are recommendations to user's past behavior. Target: moderate (not too similar)
8. **Model Latency (P95)** — Response time in ms. Benchmark: <200ms for real-time models

### Section 5: Architecture (4 layers)
1. **Behavior Collection** — Event streaming (views, clicks, purchases), user features (demographics, preferences)
2. **Feature Engineering** — User profiles (embedding vectors), item features (content-based attributes), interaction patterns
3. **Model Training** — Collaborative filtering (user-user, item-item), content-based filtering, hybrid (both signals), LLM-based
4. **Serving & Ranking** — Feature store (Redis), model serving (TensorFlow Serving), ranking pipeline (apply business rules, diversity)

### Section 6: Challenges (6 cards)
1. **Cold Start Problem** — New users/items. Solution: Use implicit signals (device, IP geo), content features, popularity baseline
2. **Filter Bubbles** — Over-personalizing = user trapped in echo chamber. Solution: Inject diversity, novelty term, serendipity goals
3. **Latency Requirements** — ML models slow, need sub-100ms response. Solution: Approximate algorithms (ANN), caching, batch pre-computation
4. **Data Sparsity** — Most user-item pairs never interact. Solution: Use side information (metadata, user demographics), collaborative signal propagation
5. **Feedback Loops** — Recommendations amplify existing biases/trends. Solution: Causal models, counterfactual reasoning, exploration strategies
6. **Creator/Merchant Fairness** — Small creators get buried by algorithm. Solution: Fairness constraints, diversity quotas, discovery programs

### Section 7: Patterns (4 companies)
1. **TikTok** — For You Page: extreme personalization, watch-time driven, millions of experiments. Each user sees different feed.
2. **Netflix** — Hybrid model: collaborative filtering + content features + editorial curation. Heavy A/B testing. Weekly model retraining.
3. **Amazon** — Purchase likelihood modeling: "Customers who bought X also bought Y." Real-time ranking with business rules (margin, discount inventory).
4. **Spotify** — Dual approach: Discover Weekly (content-based, mood + audio features) + Release Radar (collaborative, new releases). Daily updates.

---

## Build Instructions

**Files:** 11 total (1 CSS + 1 main + 7 partials + route + gallery update)

**CSS Variables (Purple/Violet for intelligence):**
```css
--dd-rc-primary: #7e22ce;     /* Purple */
--dd-rc-secondary: #6d28d9;
--dd-rc-accent: #c084fc;
--dd-rc-bg: #faf5ff;
--dd-rc-border: #d8b4fe;
--dd-rc-text: #5b21b6;
```

**Key sections:**
- S1: Personalization vs discovery tension
- S2: Animated flow through recommendation pipeline
- S3: Comparison across TikTok, Amazon, Spotify, Netflix, Square
- S4: 8 metrics including serendipity + coverage
- S5: 4-layer architecture (collection → features → training → serving)
- S6: Cold start, filter bubbles, latency, sparsity, feedback loops, fairness
- S7: TikTok, Netflix, Amazon, Spotify case studies

**Route:** `/resources/product-breakdowns/recommendations-personalization`
**Gallery card slug:** `recommendations_and_personalization.html`


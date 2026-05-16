# Product Deep Dive Plan: Ratings & Reviews

**For:** Code Puppy
**Status:** Ready to implement
**Complexity:** Medium (fewer sub-components than T&S, but nuanced)
**Build time:** 2 hours (reuses base CSS)

---

## Part 1: The 5 Questions Framework

### Q1: What is this component's job? (One sentence + analogy)

**Word-of-mouth at scale, with receipts.**

Ratings & Reviews give users a way to signal quality, help others make better decisions, and give platforms a ranking signal. It's like Yelp for anything — the user-generated reputation layer that drives trust and discovery.

### Q2: What is the core mechanism?

```
Action Completed → Prompt for Review → Collect Rating + Text → Validate Authenticity → Aggregate Score → Display & Use for Ranking
```

After a transaction (stay, purchase, ride, date, etc.), prompt the user. Collect star rating + optional text. Filter fake/spam reviews. Aggregate into average score + distribution. Use that score in search ranking, recommendations, and trust signals.

### Q3: What changes across business models?

| Dimension | Marketplace (Airbnb) | E-commerce (Amazon) | Social (TikTok) | SaaS (Notion) | Content (Netflix) |
|-----------|---------------------|--------------------|--------------------|------------|-------------------|
| **What's being rated?** | Host/property or guest behavior | Product quality | Creator/content quality | Product/template quality | Content (show/movie) quality |
| **Scale of reviews** | 10-100 per listing (reviews are rare) | 1000s per product (reviews are common) | Millions of "likes" (reviews are implicit) | 10-100 per product (sparse) | 100K+ ratings per show (dense) |
| **Incentive to review** | "Help others" + reciprocal (write review, get better reviews) | "Help community" + seller incentives (leave review, get discount) | Algorithmic amplification (engagement) | Rarely incentivized | Rarely incentivized |
| **Review authenticity problem** | Moderate (fake hosts/guests gaming ratings) | High (sellers buying fake 5-star reviews) | Very low (implicit likes are hard to fake) | Low (business reviewers are honest) | Low (aggregation hides manipulation) |
| **Ranking impact** | MASSIVE (search sorts by rating) | HUGE (Buy Box requires 4+ stars) | Moderate (engagement drives ranking, not star rating) | Low (relevance over rating) | Low (other signals matter more) |
| **Primary use case** | Decide if I trust this host/listing | Decide if I buy this product | Decide if content is worth my time | Decide if template saves me time | Decide if show is worth watching |
| **Review depth** | Long form (500+ words) | Mixed (1-star rants, 5-star "great!") | Implicit (likes/shares) | Short form (2-5 stars, occasional comment) | Stars only (no text) |
| **Manipulation risk** | HIGH (money at stake) | VERY HIGH (Amazon wars over reviews) | LOW (algorithm can't be gamed easily) | LOW (B2B skepticism) | LOW (averaging reduces outliers) |

**The pattern:** More money at stake (marketplace, e-commerce) = more fake reviews. More algorithmic ranking (social) = less reliance on explicit reviews.

### Q4: What do PMs measure?

**Health metrics** (Is the system working?):
- Review authenticity score (% of reviews flagged as suspicious)
- Review velocity (reviews per transaction, drop-off over time)
- Review distribution (is it polarized 5-star + 1-star, or realistic bell curve?)
- Time-to-review (days from transaction to review posted)

**Quality metrics** (Is it working well?):
- Review helpfulness (votes on review: was this helpful?)
- Seller/creator response rate (% of negative reviews with seller response)
- Review text quality (average word count, informativeness score)
- Correlation of rating to conversion (does 4.5★ item sell better than 4.0★?)

**Business metrics** (Is it driving value?):
- Conversion lift from reviews (% increase in sales for item with 100+ reviews vs new item)
- Trust impact (survey: "I trust ratings on this platform")
- Manipulation incidents (# of caught fake review rings per month)
- Review-driven repeat purchases (% of repeat buyers who cite reviews)

### Q5: What are the hard problems?

1. **Fake Review Wars** — Sellers/hosts/creators have strong incentive to fake reviews. You're in an arms race against coordinated fraud.
2. **Selection Bias** — Only highly satisfied or very angry people leave reviews. Honest 3-star experience is underrepresented.
3. **Cold Start** — New products have zero reviews. Users trust nothing. How do you bootstrap?
4. **Review Text Quality** — Lots of "Great!" (useless) and "Terrible!!!!!!1" (emotional venting, hard to learn from).
5. **Negative Review Suppression** — Sellers ask unhappy customers not to leave reviews. How do you incentivize honest feedback?
6. **Category Specificity** — A 5-star hotel is different from a 5-star restaurant. Rating scale is context-dependent but users don't know that.

---

## Part 2: Section-by-Section Content

### Section 1: What & Why

**Opening:** "Word-of-mouth at scale, with receipts."

Reviews serve two masters:
1. **Help users decide** — "Should I book this host? Buy this product? Watch this show?"
2. **Help platforms rank** — "What should we surface in search? What should we recommend?"

The tension: an honest, representative rating is different from a rating that's correlated with quality. Amazon's 5-star reviews skew toward extremes (super happy or super mad). The middle 3-star reviews are suppressed because satisfied customers don't bother.

**Why it matters:**
- Fake reviews erode trust faster than any T&S failure. One obvious fake review = users doubt ALL reviews.
- Reviews are a ranker signal. Amazon's "A9" algorithm uses review trends as a proxy for product quality.
- Reviews are a retention tool. Users who read reviews before booking are less likely to charge back or complain.

**Visual:** Two-column "Authentic Review Patterns" (bell curve, normal distribution) vs "Manipulated Review Patterns" (all 5-stars then sudden 1-stars, or suspicious timing pattern).

**Callout:** "The insight most teams miss: fake reviews hurt future customers more than they help current sellers. Short-term seller incentive conflicts with long-term platform trust."

---

### Section 2: How It Works (Animated Flow)

```
Transaction Completion → Post-Action Prompt → User Writes Review → Content Moderation → Aggregation & Storage → Ranking Integration → Feedback Loop
```

**7-node animation:**
1. **Transaction Completed** — User completes action (booking, purchase, ride, etc.)
2. **Prompt Delivery** — Platform emails/notifies user to leave review (timing matters — too soon = no feedback, too late = forgotten)
3. **Review Submission** — User rates (stars) + writes optional text
4. **Content Moderation** — Filter spam, verify authenticity (is review text auto-generated? Is reviewer real?)
5. **Aggregation** — Average rating, vote count, distribution stats (how many 5-stars vs 1-stars?)
6. **Ranking Integration** — Use rating in search algorithms, recommendation engines, trust signals
7. **Feedback Loop** — Track impact (do higher-rated items convert better?) → learn optimal timing/prompting

**Feedback loop:** Conversion data (which items sold more after review) flows back to help calibrate review weighting in ranking models.

---

### Section 3: Across Business Models

**5-column comparison table** (see Part 1 table above, expanded):

| Dimension | Airbnb | Amazon | TikTok | Notion | Netflix |
|-----------|--------|--------|--------|--------|---------|
| **What gets rated** | Host, property, guest (3-sided) | Product (1-way) | Creator/content (implicit) | Template quality | Show/movie (1-way) |
| **# of reviews/item** | 50-200 | 1000-100K | Millions of implicit likes | 5-50 | 100K-500K |
| **Star scale** | 5-star (host + guest) | 5-star | Implicit engagement | 5-star | 5-star (aggregated) |
| **Review depth** | Long form (travelers write essays) | Mixed (1-star rants, 5-star praise) | Micro-signals (like, retweet, comments) | Short (mostly stars, some comments) | Stars only |
| **Authenticity challenge** | HIGH (hosts fake-book themselves) | EXTREME (sellers hire fake reviewers) | LOW (engagement hard to fake at scale) | LOW (B2B disincentive) | MEDIUM (review bombing happens) |
| **Response mechanism** | Host responds to guest, guest responds to host | Seller can respond to reviews | Creators can comment/duet | Not really a feature | Studios can run campaigns |
| **Ranking impact** | MASSIVE (sort by rating) | HUGE (rating + review count) | LOW (implicit, driven by watch time) | MEDIUM (relevance first) | NONE (other signals dominate) |
| **Manipulation patterns** | "Book us, we'll book you back" (ring trading) | Fake 5-star reviews, 1-star competitor attacks | Collusion (reply with encouragement) | Minimal | Organized review bombing |
| **Mitigation strategy** | Verify guest actually stayed (transaction proof) | Verified Purchase badge, ML detection | Implicit signals are native-hard-to-game | Minimal needed | Temporal filtering (ignore surge of same score) |

---

### Section 4: Key Metrics (8 cards)

1. **Review Authenticity Score**
   - Formula: % of reviews flagged as suspicious by ML + human review
   - Benchmark: 2-5% for healthy marketplace (5-10% = indicates fraud), >10% = under attack
   - Why: Inverse health metric. If rising, you're being gamed.

2. **Review Velocity (Reviews per Transaction)**
   - Formula: # of reviews / # of completed transactions in period
   - Benchmark: 5-15% (5-15% of users write reviews). Higher = stronger incentive/culture.
   - Why: If dropping, review prompt timing or incentive is off. If 0%, users don't care.

3. **Review Distribution Shape**
   - Formula: % of 5-star + % of 1-star / % of 3-star (ratio of extremes to middle)
   - Benchmark: ~1.5-2.0 ratio. If >3.0, you're seeing polarization (fake 5s + angry 1s, not representative).
   - Why: Bell curve = healthy. Bimodal = manipulated or genuinely polarizing.

4. **Negative Review Response Rate**
   - Formula: (Sellers/creators who responded to 1-2 star reviews / total negative reviews) × 100
   - Benchmark: 30-50% for marketplaces (good = shows sellers care about feedback)
   - Why: Engagement metric. Shows whether platform encourages constructive dialogue.

5. **Review Helpfulness Score**
   - Formula: (Helpful votes / total votes on a review) — aggregated
   - Benchmark: 40-60% of reviews get marked "helpful" by others
   - Why: Quality metric. If low, reviews aren't useful. If high, good signal for ranking.

6. **Cold Start Conversion Penalty**
   - Formula: Conversion rate for 0-review items / conversion rate for 100+ review items
   - Benchmark: 50-70% (new items convert 50-70% as well as reviewed items)
   - Why: Business metric. Large penalty means reviews are essential (address with recommendations, trust signals).

7. **Review-to-Repeat-Purchase Correlation**
   - Formula: % of repeat customers who cited reviews in post-purchase survey
   - Benchmark: 30-50% of repeat buys driven by positive reviews
   - Why: Behavioral metric. Shows reviews are driving real decisions.

8. **Time-to-First-Review**
   - Formula: Average days from transaction to review posted
   - Benchmark: 3-7 days (too long = reviews come late, forgotten experience; too soon = uninformed reviews)
   - Why: Operational metric. If high, adjust prompt timing. If low, might be too early.

**Callout:** "The metric most platforms ignore: Review Authenticity Score. If it's >10%, you have a fake review problem that WILL erode trust. Fix it now."

---

### Section 5: Architecture Deep Dive

**4-layer static diagram:**

**Layer 1: Review Collection & Ingestion**
- Post-transaction trigger (when booking confirmed, purchase delivered, etc.)
- Prompt scheduler (decides WHEN to ask for review — timing is critical)
- Review submission form (stars + text box, optional photos)
- Data pipeline (ingest review to database)
- Sub-components: Timing A/B tests, form variants, spam pre-filter

**Layer 2: Content Moderation & Authenticity**
- Spam detection (auto-generated text, boilerplate patterns)
- Sentiment analysis (is this genuine feedback or venting?)
- Reviewer authenticity (is this a real user or bot? cross-check with transaction history)
- ML model scores each review for authenticity (0-100 confidence)
- Sub-components: Blacklisted keywords, account age checks, velocity flags

**Layer 3: Aggregation & Storage**
- Review database (store raw review + moderation flags)
- Aggregation compute (nightly: recalculate avg rating, distribution, trends)
- Caching layer (Redis: serve cached avg rating)
- Time-series analytics (track rating trends over time for items)
- Sub-components: Bucketing (5-star, 4-star, etc.), temporal aggregation

**Layer 4: Ranking Integration & Feedback**
- Ranking API (expose rating + review count + distribution to ranking service)
- Review display (web UI to show top reviews, sorted by helpfulness)
- Seller response system (sellers can respond to negative reviews)
- Feedback loop (track: do higher-rated items convert better? Retrain models)
- Sub-components: Review sorting algorithms, response workflows

**Callout:** "The hidden cost: content moderation. Reviews at scale require armies of contractors to spot-check ML decisions. Budget 20% of review engineering for this."

---

### Section 6: Common Challenges (6 cards)

1. **Fake Review Rings**
   - **Problem:** Coordinated groups of people (or bots) create fake accounts and leave glowing reviews for a target seller, then negative reviews for competitors.
   - **Solution pattern:** Graph-based detection (find clusters of accounts reviewing same sellers, check for coordinated patterns). Cross-platform reputation (share fraud signals across sister properties).
   - **Example:** Amazon caught a fake review ring orchestrating 30K+ fake reviews. Now uses account linking (IP, payment method, email) to detect rings automatically.

2. **Selection Bias (The Middle Stars Problem)**
   - **Problem:** Only outliers leave reviews. Highly satisfied (5-star) and very angry (1-star) people write reviews. The honest 3-star experiences are silent.
   - **Solution pattern:** Implicit signals (likes, repeat purchases, return rates) to estimate quality beyond explicit reviews. Survey representative samples.
   - **Example:** Netflix doesn't rely on ratings (too biased toward extremes). Uses watch-time, completion rate, skip rate as true quality signals.

3. **Cold Start (New Item Problem)**
   - **Problem:** New products have zero reviews. Users trust nothing. They don't convert. How do you bootstrap?
   - **Solution pattern:** Use reviewer reputation (5-star review from verified buyer with 100+ past reviews = more trusted than anonymous new account). Transfer trust (if same seller's other items have 4.5★ rating, new item starts with trust bonus).
   - **Example:** Amazon gives "Verified Purchase" badge to reviews from people who actually bought the item. Prioritizes those reviews higher.

4. **Negative Review Suppression**
   - **Problem:** Sellers discourage unhappy customers from leaving negative reviews (offer refund if they don't review). Users who had bad experience are silent.
   - **Solution pattern:** Incentivize honest reviews (survey: "How satisfied are you?" → escalate 2-3 star to post-purchase review request). Make it easy to report suppression.
   - **Example:** Airbnb explicitly prohibits guests/hosts from asking each other not to review. Actively investigates reports of suppression.

5. **Review Text Quality Decay**
   - **Problem:** Most reviews are low-effort: "Great!!!" or "Terrible product waste of money." Neither helps future users make decisions.
   - **Solution pattern:** Prompt for specificity (ask "What was your favorite part?" instead of just "Rate this"). Highlight helpful reviews (crowd vote on usefulness). Penalize generic reviews in ranking.
   - **Example:** Amazon shows "Most Helpful" reviews first (sorted by votes from readers), not chronological or highest-rated. Incentivizes detailed, useful reviews.

6. **Rating Context Ambiguity**
   - **Problem:** What's a 5-star hotel? What's a 5-star service? Scale means different things in different contexts. User doesn't know if 4.2★ is good or mediocre.
   - **Solution pattern:** Show context (avg rating for this category, comparison to similar items). Use category-specific rating scales. Show review distribution (% 5-star, % 4-star, etc.).
   - **Example:** Airbnb shows "Overall rating: 4.8" + distribution bars (see that it's 95% 5-star) + compares to neighborhood average. Context matters.

**Callout:** "The challenge that haunts every review system: fake reviews. The incentives are so strong (money!) that this is an ongoing arms race. Allocate 30% of your review team to fraud detection, permanently."

---

### Section 7: Real-World Patterns (4 company cards)

1. **Amazon**
   - **Approach:** Verified Purchase badge (only reviews from buyers who bought it count). ML detection of fake reviews + linguistic analysis of text. Seller response system.
   - **What's different:** Treats reviews as critical ranking signal (affects product ranking in search). Invests massive resources in authenticity. Has public "anti-review-fraud" team.
   - **Key lesson:** Reviews are a feature that can make or break your marketplace. Fake reviews are an existential threat. Treat accordingly.

2. **Airbnb**
   - **Approach:** Dual reviews (host reviews guest, guest reviews host + property). Photo verification (guests can upload photos). No review until both parties have checked in/out.
   - **What's different:** Requires transaction proof. Can detect fake bookings (same account hosting multiple listings, booking pattern anomalies). Transparent about review delays (explains review process to users).
   - **Key lesson:** Transaction proof is your best authenticity signal. Structure incentives so both parties benefit from honest reviews.

3. **TikTok**
   - **Approach:** No explicit reviews. Implicit signals instead (likes, shares, comments, watch time, skip rate). Algorithm learns from these signals.
   - **What's different:** Avoids manipulation entirely by not having explicit star ratings. Engagement is the rating. Can't fake millions of likes at scale.
   - **Key lesson:** Sometimes the best review system is no explicit review system. Let implicit behavior speak.

4. **Notion**
   - **Approach:** Minimal reviews (stars on Templates gallery, but sparse). Relies on community (templates with community votes, features on homepage). User reputation (badge for "power user").
   - **What's different:** B2B context (template buyers are sophisticated). Community-driven (power users get badges, visibility). Doesn't need aggressive review systems.
   - **Key lesson:** Review importance scales with buyer sophistication. B2B = less review reliance. B2C = review-critical.

**Callout:** "What they all share: reviews are not a 'feature to add.' They're a core ranking and trust signal. If you build a platform, design reviews into it from day 1. Adding reviews later = always compromised."

---

## Part 3: Build Instructions

### Files to Create (13 files)

| File | Purpose |
|------|---------|
| `code/app/static/css/dd-ratings-reviews.css` | Topic CSS with `--dd-rr-*` variables (amber/orange palette) |
| `code/app/templates/resources/product_breakdowns/ratings_and_reviews.html` | Main template |
| `code/app/templates/resources/partials/dd_rr_subnav.html` | 7-section subnav |
| `code/app/templates/resources/partials/dd_rr_what_and_why.html` | Section 1 |
| `code/app/templates/resources/partials/dd_rr_how_it_works.html` | Section 2 (animated 7-node flow) |
| `code/app/templates/resources/partials/dd_rr_across_models.html` | Section 3 (5-column grid) |
| `code/app/templates/resources/partials/dd_rr_metrics.html` | Section 4 (8 metric cards) |
| `code/app/templates/resources/partials/dd_rr_architecture.html` | Section 5 (4-layer diagram) |
| `code/app/templates/resources/partials/dd_rr_challenges.html` | Section 6 (6 challenge cards) |
| `code/app/templates/resources/partials/dd_rr_patterns.html` | Section 7 (4 company cards) |

### Files to Modify

| File | Change |
|------|--------|
| `code/app/routers/resources.py` | Add route: `/resources/product-breakdowns/ratings-and-reviews` |
| `code/app/templates/resources/product_breakdowns.html` | Add Ratings & Reviews card to gallery grid |

### CSS Variables

```css
:root {
  --dd-rr-primary: #d97706;    /* Amber (trust/stars) */
  --dd-rr-secondary: #b45309;  /* Darker amber */
  --dd-rr-accent: #f59e0b;     /* Lighter amber */
  --dd-rr-bg: #fffbeb;
  --dd-rr-border: #fcd34d;
  --dd-rr-text: #b45309;
}

.dark {
  --dd-rr-primary: #f59e0b;
  --dd-rr-secondary: #d97706;
  --dd-rr-accent: #fbbf24;
  --dd-rr-bg: #451a03;
  --dd-rr-border: #b45309;
  --dd-rr-text: #fcd34d;
}

.dd-ratings-reviews {
  --dd-primary: var(--dd-rr-primary);
  /* ... map all --dd-rr-* to --dd-* */
}
```

### Verification Checklist

- [ ] `/resources/product-breakdowns/ratings-and-reviews` loads
- [ ] All 7 sections render
- [ ] Animated flow plays smoothly
- [ ] Dark mode colors adapt
- [ ] Mobile responsive
- [ ] Gallery shows S&D, T&S, and R&R cards
- [ ] No console errors
- [ ] Commit message mentions Ratings & Reviews


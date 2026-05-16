# Product Deep Dive Plan: Trust & Safety

**For:** Code Puppy
**Status:** Ready to implement
**Complexity:** High (6 sub-components)
**Build time:** 2-3 hours (reuses base CSS)

---

## Part 1: The 5 Questions Framework

### Q1: What is this component's job? (One sentence + analogy)

**The bouncer, the referee, and the insurance adjuster.**

Trust & Safety keeps bad actors off the platform, enforces the rules, and protects users when things go wrong. It's three jobs in one:
- **Bouncer** = Detection & prevention (stop the bad guy at the door)
- **Referee** = Enforcement & moderation (manage disputes, apply penalties)
- **Insurance Adjuster** = Resolution & recovery (help when something goes wrong)

### Q2: What is the core mechanism?

```
Signal Detection → Risk Scoring → Decision Tree → Action → Appeal → Learning Loop
```

Every platform observes signals (user behavior, content, metadata, timing patterns), scores risk, decides what to do (warn, restrict, remove, escalate), takes action, allows appeals, and learns from outcomes.

### Q3: What changes across business models?

| Dimension | Marketplace | E-commerce | Social | SaaS | Fintech |
|-----------|-------------|-----------|--------|------|---------|
| **Primary threat** | Fraud (fake listings, scams) | Counterfeit products, returns fraud | Abuse (harassment, spam), illegal content | Credential theft, account takeover | Money laundering, identity theft |
| **Key signals** | Transaction history, dispute rate, seller rating changes, listing patterns | Payment method, refund rate, velocity, geolocation mismatch | User behavior, content reports, follow patterns, engagement | Login patterns, API usage, permission grants, data exports | Transaction patterns, KYC data, beneficiary changes |
| **Decision speed** | Hours (can investigate) | Minutes (fraud at scale) | Seconds (content removal) | Hours (balance UX with risk) | Real-time (prevent transaction) |
| **Enforcement tool** | Account suspension, listing removal, payment hold | Refund + blacklist | Content removal, account ban, shadowban | Force password reset, session kill, 2FA mandate | Transaction block, account freeze, report to authorities |
| **False positive cost** | High (legitimate sellers leave) | Medium (lost repeat customers) | High (suppress innocent users) | Low (annoying but safe) | Extreme (blocks legitimate transactions, regulatory fines) |
| **Regulatory requirement** | Light (varies by country) | Medium (consumer protection laws) | Medium (moderation liability varies) | Light (SOC 2) | Extreme (AML/KYC/CFT mandatory) |

**The pattern:** Fintech = strict & real-time (regulatory + money). Social = loose & automated (speed). Marketplaces = balanced (trust is the entire business model).

### Q4: What do PMs measure?

**Health metrics** (Is the system working?):
- False positive rate (% of legitimate users incorrectly flagged)
- False negative rate (% of actual bad actors not caught)
- Investigation backlog (days of pending reviews)
- Mean time to suspension (speed from report to action)

**Quality metrics** (Is it working well?):
- Repeat offender rate (% of suspended users who re-offend with new account)
- Appeal overturn rate (% of appeals where we were wrong)
- User trust score (survey: "I trust this platform is safe")
- Friction index (# of extra steps users must take for safety features)

**Business metrics** (Is it driving value?):
- Net platform growth (retention vs. suspensions)
- Trust-driven conversions (% of buyers who cite safety as reason to use us)
- Regulatory incidents (# of compliance violations, fines avoided)
- Cost per abuse prevention (total T&S spend / # of prevented incidents)

### Q5: What are the hard problems?

1. **False Positive Hell** — Catching 99% of bad actors means 1% get through. But 0.1% false positives = lots of innocent users harmed. The curve is brutal.
2. **Cold Start + New Account Fraud** — New accounts have no history, so you can't score risk. Scammers exploit this. How do you bootstrap trust?
3. **Gaming the System** — Bad actors learn your rules and stay just below the threshold. Rules become an adversarial game.
4. **Speed vs Accuracy** — Content removal needs to be fast (social), but account bans need to be careful (marketplace). Hard to have both.
5. **Appeal Paralysis** — Users want fairness/appeals, but appeals cost money & time. Too generous = guilty people get unbanned. Too strict = users leave.
6. **Regulatory Patchwork** — Rules differ by country, jurisdiction, platform type. One global policy doesn't work.

---

## Part 2: Section-by-Section Content

### Section 1: What & Why

**Opening:** "The bouncer, the referee, and the insurance adjuster."

Three distinct jobs:
1. **Prevention** — Stop bad actors before they harm the platform (bouncer at the door)
2. **Enforcement** — Catch rule-breakers, apply penalties, manage disputes (referee during the game)
3. **Recovery** — Help users when they're scammed, hacked, or wrongfully accused (adjuster after the incident)

Most platforms conflate these. The best separate them and balance resource allocation.

**Why it matters:**
- Trust is your moat. One successful scam = lost user forever.
- Regulatory pressure keeps rising. You WILL be sued. Plan for it.
- Cold start fraud is devastating. Scammers exploit new platforms before reputation systems kick in.
- False positives erode trust as much as false negatives.

**Visual:** Two-mode panel showing "Legitimate User Journey" vs "Scammer Journey" — showing where T&S intervenes at each step.

**Callout:** "The metric you're probably not measuring: false positive rate. Every wrongfully suspended user costs more than catching 10 actual bad actors."

---

### Section 2: How It Works (Animated Flow)

```
Signal Observation → Risk Scoring → Decision Tree → Action → User Appeal → Learning Feedback Loop
```

**7-node animation:**
1. **Signal Observation** — Log all user actions (transactions, content, login patterns, reports, metadata)
2. **Risk Scoring** — ML model assigns risk score (0-100) to user, account, transaction, content
3. **Decision Tree** — Rule engine applies thresholds (>80 = instant ban, 50-80 = human review, <50 = allow)
4. **Action** — Bouncer (block), Referee (warn/suspend/remove), Adjuster (escalate to specialist)
5. **User Appeal** — Wrongfully accused user submits appeal with evidence
6. **Investigation & Reversal** — Team reviews, makes decision, may reverse action
7. **Model Update** — Outcome feeds back to training pipeline (we were right/wrong)

**Feedback loop:** Appeals → Investigation outcomes → Model retraining

---

### Section 3: Across Business Models

**5-column comparison table:**

| Dimension | Marketplace (Airbnb) | E-commerce (Amazon) | Social (Twitter) | SaaS (Okta) | Fintech (Stripe) |
|-----------|---------------------|--------------------|-----------------|-----------|--------------------|
| **Primary threat** | Fake listings, scammer hosts/guests, chargebacks | Counterfeit goods, return fraud, payment fraud | Spam, harassment, child safety, election misinformation | Account takeover, insider threats, data breach | Money laundering, fraud, sanctions violations |
| **Key signal #1** | Host history, booking cancellation pattern | Seller track record, refund history | Account age, follower authenticity, content patterns | Login velocity, geographic mismatch, data access patterns | Transaction amount, beneficiary jurisdiction, velocity |
| **Key signal #2** | Guest reviews & disputes | Payment method changes, geo velocity | Report volume, engagement vs follower ratio | Unusual API calls, permission grants | KYC/AML data, sanctioned entity lists |
| **Key signal #3** | Booking timing (last-minute = higher risk) | Return rate, time-to-return | Tweet similarity (bots), follow/unfollow patterns | Session duration anomalies | Source of funds verification |
| **Speed of decision** | Hours to days (investigate) | Minutes (scale) | Seconds to minutes (content) | Hours (balance UX & risk) | Real-time (prevent payment) |
| **Cost of false positive** | High (trust in hosts/guests eroded) | Medium (loses repeat customer) | High (suppresses legitimate users) | Medium-High (bad UX, support burden) | Extreme (blocks legitimate customer, reputational) |
| **Enforcement tool** | Suspend account, refund + blacklist, deactivate listing | Remove product, refund buyer, seller ban | Delete tweets, shadowban, account suspension, permanent ban | Force password reset, 2FA, session terminate | Block transaction, freeze account, flag to compliance, escalate to regulators |
| **Regulatory weight** | Low-medium (varies by country) | Medium (consumer protection laws) | Medium (moderation liability) | Light (SOC 2, data protection laws) | EXTREME (AML/KYC/CTF, GDPR, sanctions) |
| **Repeat offender rate** | 15-25% (create new listing/account) | 5-10% (payment methods easier to track) | 20-40% (easy to create new account) | <5% (email domain tied to identity) | <2% (KYC makes re-offending hard) |

---

### Section 4: Key Metrics (8 cards)

1. **False Positive Rate**
   - Formula: (Wrongfully suspended users / Total suspended users) × 100
   - Benchmark: 5-15% for marketplaces, 2-5% for fintech
   - Why: Every false positive = lost user, bad PR, potential legal liability

2. **False Negative Rate**
   - Formula: (Actual bad actors who weren't caught / Total actual bad actors) × 100
   - Benchmark: Hard to measure accurately, but industry consensus is 10-20% for marketplaces
   - Why: Misses = scams happen on your platform, erodes trust

3. **Mean Time to Suspension (MTTS)**
   - Formula: Average days from report to action
   - Benchmark: <24 hours for serious threats, <7 days for investigation-required
   - Why: Slow response = user harm continues, more victims. Fast = better trust.

4. **Appeal Overturn Rate**
   - Formula: (Appeals where action reversed / Total appeals) × 100
   - Benchmark: 15-30% (means you're catching real cases but not perfect)
   - Why: >30% = too aggressive in original decision. <10% = not reviewing rigorously.

5. **User Trust Score**
   - Formula: Survey question: "On a scale of 1-10, how safe do you feel using this platform?"
   - Benchmark: 7.5+ (anything <7 = trust erosion, churn risk)
   - Why: Leading indicator. Trust score drops before users actually leave.

6. **Repeat Offender Rate**
   - Formula: (Users suspended who re-offend with new account / Total suspended) × 100
   - Benchmark: 5-20% for marketplaces (depends on how tied accounts are to identity)
   - Why: Indicates: (a) did we really stop them? (b) can new accounts be created too easily?

7. **Investigation Backlog**
   - Formula: # of pending T&S cases awaiting human review
   - Benchmark: <48 hours of backlog (if >10 cases per analyst, you're understaffed)
   - Why: Backlog = delayed justice = user frustration. Metric of operational health.

8. **Cost Per Prevention**
   - Formula: (Total T&S spend per month / # of prevented incidents) = $ per bad actor stopped
   - Benchmark: $100-1000 per prevention depending on industry
   - Why: Business metric. Are you spending efficiently? Where's ROI?

**Callout:** "The metric nobody talks about: appeal overturn rate. It's your honesty meter. If it's <10%, you're not reviewing appeals seriously. If it's >40%, you were wrong too often."

---

### Section 5: Architecture Deep Dive

**4-layer static diagram:**

**Layer 1: Signal Ingestion & Storage**
- User behavior logs (login, transaction, content, reports)
- Real-time streaming (Kafka, Pub/Sub)
- Data warehouse (snowflake, BigQuery)
- Sub-components: Event schema, deduplication, retention policies (keep 2+ years for legal)

**Layer 2: Feature Engineering & Risk Scoring**
- Feature extractors (velocity features: # accounts from same IP, transaction freq, etc.)
- Real-time feature store (Redis/Tecton)
- Risk scoring model (XGBoost, neural net trained on historical labels)
- Sub-components: Model serving API, A/B test framework, model version control

**Layer 3: Decision Engine & Workflow**
- Rule engine (if score > 80 AND account_age < 7 days, then AUTO_SUSPEND)
- Decision queue (route to auto-action, human review, escalation tier)
- Case management system (Salesforce, custom tool)
- Sub-components: Rule versioning, audit logs, approval workflows

**Layer 4: Enforcement & Appeals**
- Action executor (API calls to suspend, remove, restrict features)
- Appeal interface (users submit evidence, AI routes to right specialist)
- Investigation tools (analyst dashboard, investigation logs)
- Sub-components: Communication templates, reversal automation, compliance audit trail

**Feedback:** Every appeal outcome + every suspended user re-offence feeds back to Layer 2 for model retraining (monthly batch).

**Callout:** "The hidden cost: the case management system. T&S teams drown in tools and process overhead. A bad CMS can double your operational cost."

---

### Section 6: Common Challenges (6 cards)

1. **Cold Start Fraud**
   - **Problem:** New accounts have zero history. Scammers register and immediately commit fraud.
   - **Solution pattern:** Pre-trust signals (email domain reputation, IP geolocation, phone verification, payment method age). Weight these heavily for first 7 days.
   - **Example:** Stripe uses velocity-based rules (block if $10k in 1st transaction from new acct) + phone verification for high-risk regions.

2. **False Positive Spiral**
   - **Problem:** Over-aggressive rules catch many bad actors BUT also suspend legitimate users. Those suspended users create negative reviews, complain on Twitter, request chargebacks.
   - **Solution pattern:** Separate action types. Don't suspend immediately — warn first for borderline cases. Use friction (require 2FA) instead of blocking.
   - **Example:** Airbnb's "Reservation Hold" system doesn't deny the booking, just holds payment until check-in. Reduces false positive impact.

3. **Game-Theoretic Drift**
   - **Problem:** Bad actors learn your rules and adapt. They stay just below the suspension threshold. Rules become outdated faster than you can update them.
   - **Solution pattern:** Model-based scoring (ML) instead of fixed rules. ML adapts faster. Combine with adversarial testing (hire people to try to break your system).
   - **Example:** Payment processors use ensemble models (30+ sub-models) so bad actors can't game a single rule.

4. **Appeal Backlog & Unfairness**
   - **Problem:** Appeal queue grows faster than analysts can review. Users wait weeks for decision. Those wrongfully suspended leave.
   - **Solution pattern:** Tiered appeals (auto-reverse if strong evidence, escalate if unclear). For high-conviction cases, reverse immediately + investigate.
   - **Example:** Twitter's appeals are mostly automated (check if user has new evidence + check model confidence). Only <10% need human review.

5. **Regulatory Compliance Whack-a-Mole**
   - **Problem:** Regulations differ by country. GDPR says "delete user data," but you need it for investigations. AML says "report suspicious activity," but GDPR says "don't share data."
   - **Solution pattern:** Data residency + jurisdiction-specific policies. For high-risk regions, more aggressive verification. For GDPR, separate "investigation hold" data from "operational" data.
   - **Example:** Stripe has different T&S rules for EU (stricter privacy, lighter enforcement) vs US (lighter privacy, more investigation power).

6. **Trust Erosion from Abuse**
   - **Problem:** Even with T&S, some scams happen. Users feel unsafe. Word spreads.
   - **Solution pattern:** Transparency (explain why action was taken). Insurance/recovery programs (refund scammed buyers). Public reports (show % of bad actors caught).
   - **Example:** Airbnb's $1M Host Protection Insurance + published "How we keep you safe" reports (quarterly stats on suspensions, recoveries).

**Callout:** "The challenge that kills most T&S programs: false positives eroding user trust faster than bad actors being caught. The math is brutal: catch 100 bad guys, wrongly suspend 5 legit users, lose all 105."

---

### Section 7: Real-World Patterns (4 company cards)

1. **Stripe**
   - **Approach:** Real-time ML scoring + rule engine + escalation workflow. Proprietary risk model trained on billions of transactions.
   - **What's different:** Fintech-grade (AML/KYC built in from day 1). No gray areas. Real-time blocking. Accepts high false positive rate because cost of false negatives is regulatory jail time.
   - **Key lesson:** In fintech, Trust & Safety is existential. Treat it like core product, not compliance checkbox.

2. **Airbnb**
   - **Approach:** Host/guest reputation systems + ML risk scoring + human investigation team. "Host Protection Insurance" for refunds when scams happen.
   - **What's different:** Two-sided (need to trust both sides). Transparent (users see why action taken). Insurance-backed (recover if scammed).
   - **Key lesson:** In marketplaces, trust IS the business model. Invest heavily in transparency and recovery, not just prevention.

3. **Twitter / X**
   - **Approach:** Content moderation at scale (millions of posts/day). Combination of user reports, automation (ML), human review queues. Heavy reliance on crowdsourcing (Birdwatch).
   - **What's different:** Speed over perfection (remove harmful content in minutes, investigate later). Embrace appeals (reverse 20%+ of actions).
   - **Key lesson:** In social, you can't be perfect. Accept that you'll make mistakes. Speed and transparency matter more than accuracy.

4. **Okta**
   - **Approach:** Account takeover prevention (unusual login patterns, geo velocity, unauthorized API calls). Mandatory 2FA for enterprises. Session-based restrictions.
   - **What's different:** B2B SaaS (identity is everything). Proactive (block suspicious logins immediately). Reversible (user can authenticate differently and regain access).
   - **Key lesson:** In SaaS, prevent account takeover above all else. Everything else is secondary. Make blocking easy to reverse.

**Callout:** "What they all have in common: T&S is not a cost center, it's a competitive advantage. The best platforms invest 10-15% of their engineering headcount in Trust & Safety."

---

## Part 3: Build Instructions

### Files to Create (13 files)

| File | Purpose |
|------|---------|
| `code/app/static/css/dd-trust-safety.css` | Topic CSS with `--dd-ts-*` variables (red/rose palette) |
| `code/app/templates/resources/product_breakdowns/trust_and_safety.html` | Main template |
| `code/app/templates/resources/partials/dd_ts_subnav.html` | 7-section subnav |
| `code/app/templates/resources/partials/dd_ts_what_and_why.html` | Section 1 |
| `code/app/templates/resources/partials/dd_ts_how_it_works.html` | Section 2 (animated 7-node flow) |
| `code/app/templates/resources/partials/dd_ts_across_models.html` | Section 3 (5-column grid) |
| `code/app/templates/resources/partials/dd_ts_metrics.html` | Section 4 (8 metric cards) |
| `code/app/templates/resources/partials/dd_ts_architecture.html` | Section 5 (4-layer diagram) |
| `code/app/templates/resources/partials/dd_ts_challenges.html` | Section 6 (6 challenge cards) |
| `code/app/templates/resources/partials/dd_ts_patterns.html` | Section 7 (4 company cards) |

### Files to Modify

| File | Change |
|------|--------|
| `code/app/routers/resources.py` | Add route: `/resources/product-breakdowns/trust-and-safety` |
| `code/app/templates/resources/product_breakdowns.html` | Add Trust & Safety card to gallery grid |

### CSS Variables

```css
:root {
  --dd-ts-primary: #dc2626;    /* Red (security/danger) */
  --dd-ts-secondary: #991b1b;  /* Dark red */
  --dd-ts-accent: #f87171;     /* Light red */
  --dd-ts-bg: #fef2f2;
  --dd-ts-border: #fca5a5;
  --dd-ts-text: #7f1d1d;
}

.dark {
  --dd-ts-primary: #ef4444;
  --dd-ts-secondary: #dc2626;
  --dd-ts-accent: #f87171;
  --dd-ts-bg: #450a0a;
  --dd-ts-border: #7f1d1d;
  --dd-ts-text: #fca5a5;
}

.dd-trust-safety {
  --dd-primary: var(--dd-ts-primary);
  /* ... map all --dd-ts-* to --dd-* */
}
```

### Route Registration

Add to `code/app/routers/resources.py`:

```python
@router.get("/resources/product-breakdowns/trust-and-safety", response_class=HTMLResponse)
async def trust_and_safety(request: Request) -> HTMLResponse:
    """Serve the Trust & Safety deep dive."""
    return templates.TemplateResponse(
        "resources/product_breakdowns/trust_and_safety.html",
        _ctx(
            request,
            title="Trust & Safety — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )
```

### Animated Flow (Section 2)

**7 nodes in staggered layout for visibility:**
1. Signal Observation (x=60, y=60)
2. Risk Scoring (x=280, y=60)
3. Decision Tree (x=500, y=60)
4. Action (x=680, y=160)
5. User Appeal (x=500, y=280)
6. Investigation (x=280, y=280)
7. Model Update (x=900, y=160)

**Paths:** Longer curved segments connecting nodes with dramatic curves for animation visibility. Use same 12s duration + 2s staggering as S&D.

---

## Verification Checklist

- [ ] `/resources/product-breakdowns/trust-and-safety` loads
- [ ] All 7 sections render
- [ ] Animated flow plays smoothly (dots visible traveling through nodes)
- [ ] Dark mode: all colors adapt
- [ ] Mobile responsive
- [ ] Gallery shows both S&D and Trust & Safety cards
- [ ] No console errors
- [ ] Subnav scroll-tracking works
- [ ] Commit message mentions Trust & Safety deep dive


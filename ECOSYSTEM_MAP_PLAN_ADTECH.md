# Ecosystem Map Plan: Adtech / Programmatic Ecosystem

**For:** Code Puppy | **Priority:** Tier 1 (build next) | **Build time:** 4-5 hours
**PM hiring relevance:** Google, Amazon Ads, Meta, The Trade Desk, LiveRamp, DoubleVerify, IAS

---

## Why This Is a Map

The programmatic chain has 8+ participants with real-time bidding happening in ~100ms. A diagram shows what prose buries. PMs at ad-tech companies need to understand the full stack — from advertiser intent to rendered ad — and most never see the full picture.

---

## Diagrams to Build (6 diagrams)

### Diagram 1: Programmatic Stack — Layer Map
**Section ID:** `#stack`
**Type:** Layered architecture (like Financial Ecosystem Layer Map)

```
┌─────────────────────────────────────────────────┐
│  ADVERTISER SIDE                                 │
│  Brand → Agency → Trading Desk                  │
├─────────────────────────────────────────────────┤
│  DEMAND SIDE                                     │
│  DSP (Google DV360, The Trade Desk, Amazon DSP) │
├─────────────────────────────────────────────────┤
│  EXCHANGE LAYER                                  │
│  Ad Exchange (Google AdX, OpenX, Index Exchange)│
│  + Data Layer (DMP, CDP, Clean Rooms)           │
├─────────────────────────────────────────────────┤
│  SUPPLY SIDE                                     │
│  SSP (Google Ad Manager, Magnite, PubMatic)     │
├─────────────────────────────────────────────────┤
│  PUBLISHER SIDE                                  │
│  Publisher → Website/App → Ad Slot → User       │
├─────────────────────────────────────────────────┤
│  VERIFICATION & MEASUREMENT                      │
│  IAS, DoubleVerify, MOAT, Nielsen, Comscore     │
└─────────────────────────────────────────────────┘
```

**Content per layer:**
- **Advertiser Side:** Brand sets budget + goals (awareness, conversions). Agency manages campaigns. Trading desk executes.
- **Demand Side (DSP):** Software that buys ad inventory programmatically. Bids on impressions in real-time. Key players: DV360 (Google), TTD, Amazon DSP.
- **Exchange Layer:** Marketplace where DSPs bid against each other for impressions. Ad Exchange runs the auction. Data Layer provides audience targeting signals.
- **Supply Side (SSP):** Software that helps publishers sell inventory. Connects to exchanges, runs yield optimization. Key: Google Ad Manager, Magnite, PubMatic.
- **Publisher Side:** Website/app with ad slots. Publisher earns revenue per impression. User sees the ad.
- **Verification:** Third parties verify ads are viewable, brand-safe, and fraud-free. Nielsen/Comscore measure reach.

---

### Diagram 2: Real-Time Bidding (RTB) Sequence
**Section ID:** `#rtb`
**Type:** Sequence diagram (like Financial Ecosystem Loan Flow — tabbed)

**Timeline: One Ad Impression (~50-150ms total)**

| Step | Actor | Action | Time |
|------|-------|--------|------|
| 1 | User | Loads web page | 0ms |
| 2 | Publisher | Ad tag fires, sends bid request to SSP | 5ms |
| 3 | SSP | Forwards bid request to connected exchanges | 10ms |
| 4 | Exchange | Sends bid request to connected DSPs (with user signal data) | 15ms |
| 5 | DSP | Evaluates user profile, runs bidding algorithm, sets bid price | 20-50ms |
| 6 | DSP | Returns bid response to exchange | 50ms |
| 7 | Exchange | Runs auction (2nd price or 1st price), selects winner | 55ms |
| 8 | SSP | Receives winning bid, passes creative URL to publisher | 60ms |
| 9 | Publisher | Renders winning creative in ad slot | 70ms |
| 10 | User | Sees the ad (latency budget: 100-150ms total) | 100ms |
| 11 | Verification | IAS/DV verify viewability + brand safety (async, post-render) | 200ms+ |
| 12 | Advertiser | Conversion tracked (click, purchase — hours/days later) | Hours |

**Show as horizontal sequence diagram with 6 participant columns:** User, Publisher, SSP, Exchange, DSP, Advertiser

---

### Diagram 3: Cookie Death & Identity Alternatives
**Section ID:** `#identity`
**Type:** Comparison grid (like TSM Business Models cards)

**4 cards showing the evolution:**

1. **Third-Party Cookie (Legacy)**
   - How: Browser drops cookie, DSP reads it across sites, builds profile
   - Pros: Universal, easy, cheap
   - Cons: Privacy nightmare, blocked by Safari/Firefox, Chrome deprecating
   - Status: DYING (Chrome delay after delay, but inevitable)

2. **First-Party Data**
   - How: Publisher collects data directly (login, email, subscription). Shared with DSP via clean room.
   - Pros: User consented, high quality, durable
   - Cons: Only works for publishers with login walls. Small publishers locked out.
   - Winners: NYT, WSJ, Amazon (massive first-party data)

3. **Identity Solutions (UID2, LiveRamp)**
   - How: Hashed email becomes universal ID. DSPs use it instead of cookie. Opt-in.
   - Pros: Cross-site without cookies, privacy-compliant
   - Cons: Adoption fragmented, multiple competing standards
   - Key players: TTD (UID2), LiveRamp (RampID), Google (PAIR)

4. **Contextual Targeting (Post-Cookie)**
   - How: Target based on page content (article about cars → car ad), not user profile.
   - Pros: No personal data needed, privacy-safe, scales
   - Cons: Less precise, worse performance for niche targeting
   - Revival: Companies like GumGum, Peer39 building sophisticated contextual models

**Below cards:** Timeline showing cookie deprecation milestones (2020 → Safari blocks, 2024 → Chrome delay, 2025 → Chrome delay again, 2026 → ???)

---

### Diagram 4: Revenue Flow — Who Takes What
**Section ID:** `#revenue`
**Type:** Sankey-style flow diagram (like Financial Ecosystem Money Flow)

**For a $10 CPM (cost per 1000 impressions):**

```
Advertiser pays $10.00 (100%)
  │
  ├── Agency fee: $1.50 (15%)
  │
  ├── DSP fee: $1.00 (10%)
  │     (The Trade Desk, DV360)
  │
  ├── Exchange/SSP fee: $1.50 (15%)
  │     (AdX, Magnite)
  │
  ├── Verification fee: $0.30 (3%)
  │     (IAS, DoubleVerify)
  │
  ├── Data/targeting fee: $0.70 (7%)
  │     (DMPs, CDPs, data brokers)
  │
  └── Publisher receives: $5.00 (50%)
        (The actual content creator)
```

**Key insight callout:** "The ad tech tax: publishers receive ~50% of what advertisers pay. The other 50% goes to intermediaries. This is why publishers are building direct sales teams and why Google's antitrust trial matters."

**Second view (toggle):** Compare this split for:
- Programmatic open auction: 50% to publisher
- Private marketplace (PMP): 65% to publisher
- Direct deal: 85% to publisher
- Walled garden (Meta/Google): 70-80% to platform (they ARE the publisher)

---

### Diagram 5: Advertiser vs Publisher View
**Section ID:** `#perspectives`
**Type:** Two-panel comparison (like Deep Dive "What & Why" mode panels)

**Left panel: Advertiser View**
- Goal: Reach the right user at the right time for the lowest cost
- Sees: Campaign dashboard, impressions, clicks, conversions, ROAS
- Cares about: Targeting accuracy, viewability, brand safety, fraud protection
- Pain: "Am I reaching real humans?" "Is my ad actually seen?" "Where did my budget go?"
- Metric: ROAS (Return on Ad Spend) = Revenue / Ad Spend

**Right panel: Publisher View**
- Goal: Maximize revenue from every page view without degrading user experience
- Sees: Fill rate, CPM, eCPM, revenue per session, ad load
- Cares about: Yield optimization, ad quality, page speed, user experience
- Pain: "Why is my CPM dropping?" "Are these ads annoying my users?" "How much of my revenue goes to intermediaries?"
- Metric: eCPM (effective Cost Per Mille) = Total Revenue / Impressions × 1000

**Between panels:** Show how the same transaction ($10 CPM impression) looks from each side

---

### Diagram 6: Measurement & Attribution
**Section ID:** `#measurement`
**Type:** Flow diagram with comparison

**Attribution Models (4 cards):**

1. **Last-Click Attribution**
   - How: Credit goes to last ad clicked before conversion
   - Pro: Simple, deterministic
   - Con: Ignores awareness ads that started the journey
   - Used by: Small advertisers, Google Ads default

2. **Multi-Touch Attribution (MTA)**
   - How: Credit distributed across all touchpoints (linear, time-decay, position-based)
   - Pro: More accurate, captures full journey
   - Con: Complex, data-hungry, privacy challenges
   - Used by: Sophisticated brands, agencies

3. **Media Mix Modeling (MMM)**
   - How: Statistical model correlating ad spend to outcomes at aggregate level
   - Pro: Privacy-safe (no user-level data), includes offline channels
   - Con: Slow (monthly cadence), can't optimize in real-time
   - Used by: Large brands (P&G, Unilever), gaining popularity post-cookie

4. **Incrementality Testing**
   - How: A/B test: show ad to test group, don't show to control. Measure difference.
   - Pro: Causal (proves ad caused conversion, not just correlated)
   - Con: Expensive (need holdout group = lost revenue), slow
   - Used by: Sophisticated advertisers (Meta, Google offer built-in tools)

---

## Color Palette

```css
:root {
  /* Advertiser (Orange) */
  --at-advertiser-bg: #fff7ed;
  --at-advertiser-border: #fdba74;
  --at-advertiser-text: #9a3412;

  /* DSP / Demand (Blue) */
  --at-demand-bg: #eff6ff;
  --at-demand-border: #93c5fd;
  --at-demand-text: #1e40af;

  /* Exchange (Indigo) */
  --at-exchange-bg: #eef2ff;
  --at-exchange-border: #a5b4fc;
  --at-exchange-text: #3730a3;

  /* SSP / Supply (Green) */
  --at-supply-bg: #f0fdf4;
  --at-supply-border: #86efac;
  --at-supply-text: #15803d;

  /* Publisher (Teal) */
  --at-publisher-bg: #f0fdfa;
  --at-publisher-border: #5eead4;
  --at-publisher-text: #0f766e;

  /* Verification (Purple) */
  --at-verify-bg: #faf5ff;
  --at-verify-border: #d8b4fe;
  --at-verify-text: #7e22ce;

  /* Data (Amber) */
  --at-data-bg: #fffbeb;
  --at-data-border: #fcd34d;
  --at-data-text: #b45309;

  /* Neutral / Cards */
  --at-card-bg: #ffffff;
  --at-card-border: #e2e8f0;
  --at-heading: #0f172a;
  --at-body: #475569;
  --at-muted: #64748b;
}
```

Dark mode: follow the TSM/FE pattern (invert to dark backgrounds, lighter text).

---

## Files to Create

| File | Purpose |
|------|---------|
| `code/app/static/css/adtech-ecosystem.css` | Full CSS with `--at-*` variables + dark mode + component styles |
| `code/app/templates/resources/adtech_ecosystem.html` | Main template (breadcrumb + header + subnav + 6 diagram includes + footer + scroll JS) |
| `code/app/templates/resources/partials/at_subnav.html` | Sticky subnav (6 section links) |
| `code/app/templates/resources/partials/at_diagram_stack.html` | Diagram 1: Programmatic stack layer map |
| `code/app/templates/resources/partials/at_diagram_rtb.html` | Diagram 2: RTB sequence (tabbed, like FE loan flow) |
| `code/app/templates/resources/partials/at_diagram_identity.html` | Diagram 3: Cookie death & identity alternatives |
| `code/app/templates/resources/partials/at_diagram_revenue.html` | Diagram 4: Revenue flow (who takes what) |
| `code/app/templates/resources/partials/at_diagram_perspectives.html` | Diagram 5: Advertiser vs publisher view |
| `code/app/templates/resources/partials/at_diagram_measurement.html` | Diagram 6: Measurement & attribution models |

## Files to Modify

| File | Change |
|------|--------|
| `code/app/routers/resources.py` | Add route: `/resources/ecosystem-maps/adtech-ecosystem` |
| `code/app/templates/resources/ecosystem_maps.html` | Add Adtech card to gallery grid |

## Route

```python
@router.get("/resources/ecosystem-maps/adtech-ecosystem", response_class=HTMLResponse)
async def adtech_ecosystem(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "resources/adtech_ecosystem.html",
        _ctx(request, title="Adtech / Programmatic Ecosystem — PM Visual Guide | fullstackpm.tech",
             current_page="/resources/ecosystem-maps"),
    )
```

## Verification

- [ ] `/resources/ecosystem-maps/adtech-ecosystem` loads
- [ ] All 6 diagrams render
- [ ] RTB sequence diagram is tabbed (like FE loan flow)
- [ ] Revenue flow shows the 50/50 split clearly
- [ ] Cookie death cards show timeline
- [ ] Dark mode adapts
- [ ] Mobile responsive
- [ ] Gallery shows 3 cards (Financial, Marketplace, Adtech)
- [ ] Scroll tracking subnav works


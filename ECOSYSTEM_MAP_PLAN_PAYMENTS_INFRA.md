# Ecosystem Map Plan: Payments Infrastructure Ecosystem

**For:** Code Puppy | **Priority:** Tier 2 | **Build time:** 4-5 hours
**PM hiring relevance:** Stripe, Adyen, Braintree, Square, Checkout.com, Worldpay
**Note:** Extends the Financial Ecosystem map. Link the two.

---

## Why This Is a Map

The Financial Ecosystem map covers payment rails at a high level. This goes deeper: card network economics, the acquiring/issuing split, payment gateway vs processor vs acquirer, and how Stripe abstracts all of it. PMs at payment companies must understand every participant in the chain.

---

## Diagrams to Build (5 diagrams)

### Diagram 1: Full Card Transaction Stack
**Section ID:** `#stack`
**Type:** Layered architecture with participant roles

```
┌─────────────────────────────────────────────────────┐
│  CARDHOLDER (Consumer)                               │
│  Has card issued by bank, swipes/taps/enters online  │
├─────────────────────────────────────────────────────┤
│  MERCHANT                                            │
│  Accepts card via POS terminal or online checkout    │
├─────────────────────────────────────────────────────┤
│  PAYMENT GATEWAY                                     │
│  Encrypts + routes transaction (Stripe.js, Braintree)│
├─────────────────────────────────────────────────────┤
│  PAYMENT PROCESSOR / ACQUIRER                        │
│  Connects merchant to card network (Stripe, Adyen)  │
├─────────────────────────────────────────────────────┤
│  CARD NETWORK                                        │
│  Routes between acquirer and issuer (Visa, MC, Amex)│
├─────────────────────────────────────────────────────┤
│  ISSUING BANK                                        │
│  Issued the card, holds the funds (Chase, BofA, etc)│
├─────────────────────────────────────────────────────┤
│  SETTLEMENT NETWORK                                  │
│  Moves actual money (ACH, Fedwire, SWIFT)           │
└─────────────────────────────────────────────────────┘
```

**For each participant, show:**
- Role (what they do)
- Revenue (how they make money)
- Examples (real companies)
- PM relevance (what a PM at that layer worries about)

**Key callout:** "Many companies straddle multiple layers. Stripe is both gateway AND processor AND acquirer. Square is merchant + processor + issuer (Cash Card). The trend is vertical integration."

---

### Diagram 2: Interchange Economics — Who Gets What from a $100 Swipe
**Section ID:** `#interchange`
**Type:** Fee breakdown (Sankey-style, like adtech revenue flow)

**For a $100 card transaction:**

```
Merchant pays $2.90 total (2.9%)
  │
  ├── Interchange fee: $1.80 (1.8%)
  │     → Goes to ISSUING BANK (Chase, BofA)
  │     → Largest chunk. Set by card network. Non-negotiable.
  │     → Funds rewards programs (points, cashback)
  │
  ├── Network assessment fee: $0.15 (0.15%)
  │     → Goes to CARD NETWORK (Visa, Mastercard)
  │     → For maintaining the network infrastructure
  │
  ├── Acquirer/processor markup: $0.95 (0.95%)
  │     → Goes to PROCESSOR (Stripe, Adyen, Square)
  │     → Covers fraud prevention, support, technology
  │     → This is the negotiable part
  │
  └── Merchant receives: $97.10
```

**Show 4 variants (tabbed or comparison row):**
- **Debit card (regulated):** Interchange capped at 0.05% + $0.21 (Durbin Amendment)
- **Credit card (rewards):** Interchange 1.5-2.5% (funds cashback/points)
- **Amex:** Network fee higher (~2.5-3.5%) because Amex is both network AND issuer
- **International:** Higher interchange + cross-border fee (~1% extra)

**Key callout:** "Interchange fees are the reason merchants hate credit cards and love debit cards. It's also why Visa/MC are two of the most profitable companies on earth — they set the fees but don't bear the fraud risk."

---

### Diagram 3: Payment Methods Compared
**Section ID:** `#methods`
**Type:** Comparison grid (table or cards)

| Method | Speed | Cost to merchant | Reversibility | Fraud risk | Global reach |
|--------|-------|-----------------|---------------|------------|-------------|
| **Credit card** | Instant auth, 1-2 day settle | 2.5-3.5% | HIGH (chargebacks) | HIGH (CNP fraud) | Global (Visa/MC) |
| **Debit card** | Instant auth, 1-2 day settle | 0.5-1.5% | MEDIUM (disputes) | MEDIUM | Global (Visa/MC) |
| **ACH / bank transfer** | 1-3 business days | $0.20-1.50 flat | LOW (hard to reverse) | LOW | US only |
| **Wire transfer** | Same day (Fedwire) | $15-30 flat | NONE (irrevocable) | LOW | Via SWIFT (global) |
| **Real-Time Payments (RTP/FedNow)** | Seconds | $0.01-0.05 | NONE (irrevocable) | LOW | US (growing) |
| **Digital wallets (Apple Pay, Google Pay)** | Instant (tokenized card) | Same as underlying card | Same as card | LOWER (tokenized) | Growing global |
| **Buy Now Pay Later** | Instant (for consumer) | 3-6% (merchant pays) | MEDIUM | MEDIUM | US/EU/AU |
| **Crypto / stablecoins** | Minutes to hours | 0.1-1% | NONE (irrevocable) | LOW (pseudonymous) | Global (no borders) |

**Key callout:** "The tradeoff is always: speed vs cost vs reversibility. Cards are fast but expensive and reversible (chargebacks). Wire transfers are cheap and irrevocable but slow. RTP/FedNow is the future: fast, cheap, irrevocable."

---

### Diagram 4: Stripe's Abstraction Layer
**Section ID:** `#stripe`
**Type:** Architecture diagram showing what Stripe hides vs exposes

**Left: What the developer sees (Stripe API)**
```
stripe.charges.create({
  amount: 10000,  // $100
  currency: 'usd',
  source: 'tok_visa',
})
```
→ One API call. Done.

**Right: What Stripe does behind the scenes**
```
1. Receives tokenized card data (PCI handled by Stripe.js)
2. Routes to correct processor (bank-specific routing)
3. Sends auth request to card network (Visa)
4. Network routes to issuing bank
5. Bank checks funds, returns auth code
6. Stripe runs Radar fraud check (ML model)
7. If 3D Secure required, redirects user
8. Captures funds
9. Batches settlement (next business day)
10. Deposits to merchant's bank (Stripe Connect payout)
11. Handles disputes if chargeback occurs
12. Reports to merchant dashboard
```

**Callout:** "Stripe's genius is abstraction. One API call hides 12 steps, 6 participants, 3 networks, and 2 days of settlement. That's why developers love it — and why Stripe captures 0.95% of every transaction for the privilege."

---

### Diagram 5: Cross-Border Payments
**Section ID:** `#crossborder`
**Type:** Flow diagram with comparison

**Traditional: Correspondent Banking (SWIFT)**
```
Sender (US) → Sender's bank → Correspondent bank (US)
  → SWIFT message → Correspondent bank (EU) → Recipient's bank → Recipient (EU)
```
- Time: 2-5 business days
- Cost: $25-50 + FX spread (1-3%)
- Transparency: Low (fees unclear until arrival)
- Coverage: Global (10,000+ banks on SWIFT)

**Modern: Wise/Nium/Airwallex**
```
Sender (US) → Wise collects USD domestically
  → Wise's local account in EU pays out EUR from local balance
  → Recipient (EU) receives EUR via local rails
```
- Time: Hours to 1 day
- Cost: 0.5-1.5% (transparent upfront)
- Transparency: High (mid-market FX rate shown)
- How: Pre-funded local accounts in each country. Money doesn't actually cross borders — Wise rebalances internally.

**Future: Stablecoins / CBDCs**
```
Sender → Convert to USDC on-chain → Transfer via blockchain → Convert to local currency → Recipient
```
- Time: Minutes
- Cost: <0.5%
- Status: Early but growing (Circle, Stellar network)

**Key callout:** "Money is slow because it crosses borders through correspondent banks (SWIFT). Wise's innovation: money doesn't cross borders at all. They maintain local pools in each country and rebalance. That's why they're 5-10x cheaper."

---

## Color Palette

```css
:root {
  /* Merchant (Green) */
  --pi-merchant-bg: #f0fdf4;
  --pi-merchant-border: #86efac;
  --pi-merchant-text: #15803d;

  /* Processor/Acquirer (Blue) */
  --pi-processor-bg: #eff6ff;
  --pi-processor-border: #93c5fd;
  --pi-processor-text: #1e40af;

  /* Network (Indigo) */
  --pi-network-bg: #eef2ff;
  --pi-network-border: #a5b4fc;
  --pi-network-text: #3730a3;

  /* Issuer (Purple) */
  --pi-issuer-bg: #faf5ff;
  --pi-issuer-border: #d8b4fe;
  --pi-issuer-text: #7e22ce;

  /* Settlement (Teal) */
  --pi-settle-bg: #f0fdfa;
  --pi-settle-border: #5eead4;
  --pi-settle-text: #0f766e;

  /* Fees/Money (Amber) */
  --pi-fees-bg: #fffbeb;
  --pi-fees-border: #fcd34d;
  --pi-fees-text: #b45309;

  /* Neutral */
  --pi-card-bg: #ffffff;
  --pi-card-border: #e2e8f0;
  --pi-heading: #0f172a;
  --pi-body: #475569;
}
```

---

## Files to Create (8 files)

| File | Purpose |
|------|---------|
| `code/app/static/css/payments-infrastructure.css` | CSS with `--pi-*` variables |
| `code/app/templates/resources/payments_infrastructure.html` | Main template |
| `code/app/templates/resources/partials/pi_subnav.html` | 5-section subnav |
| `code/app/templates/resources/partials/pi_diagram_stack.html` | Diagram 1: Full card transaction stack |
| `code/app/templates/resources/partials/pi_diagram_interchange.html` | Diagram 2: Interchange economics (tabbed) |
| `code/app/templates/resources/partials/pi_diagram_methods.html` | Diagram 3: Payment methods compared |
| `code/app/templates/resources/partials/pi_diagram_stripe.html` | Diagram 4: Stripe abstraction layer |
| `code/app/templates/resources/partials/pi_diagram_crossborder.html` | Diagram 5: Cross-border payments |

## Files to Modify

| File | Change |
|------|--------|
| `code/app/routers/resources.py` | Add route: `/resources/ecosystem-maps/payments-infrastructure` |
| `code/app/templates/resources/ecosystem_maps.html` | Add card to gallery |

## Verification

- [ ] All 5 diagrams render
- [ ] Interchange breakdown shows fee split clearly
- [ ] Payment methods comparison is scannable
- [ ] Stripe abstraction shows "1 API call vs 12 steps"
- [ ] Cross-border shows SWIFT vs Wise vs Stablecoin
- [ ] Dark mode + mobile responsive
- [ ] Link to Financial Ecosystem map from page


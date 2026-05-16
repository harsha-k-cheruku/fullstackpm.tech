# Ecosystem Map Plans: Tier 3 (5 Maps)

**For:** Code Puppy | **Priority:** Tier 3 (build when Tier 1-2 complete) | **Build time:** 3-4 hours each

These plans are lighter than Tier 1-2 but contain enough detail for Code Puppy to build without additional research.

---

## Map 7: Mortgage / Real Estate Ecosystem

**PM Relevance:** Better, Blend, Opendoor, Zillow, Redfin
**Prefix:** `mr` | **Color:** Emerald/Green (money + land)
**Route:** `/resources/ecosystem-maps/mortgage-real-estate`

### Diagrams (5)

**1. Origination Flow** (`#origination`)
- Sequence: Buyer applies → Loan officer → Underwriter → Appraisal → Title search → Closing → Recording
- Show 8 participants: Buyer, Agent, Lender, Underwriter, Appraiser, Title company, Escrow, County recorder
- Timeline: 30-60 days typical (highlight where delays happen)
- Key callout: "The average mortgage takes 47 days to close. 23 of those days are waiting for third parties (appraisal, title, underwriting)."

**2. GSE Securitization** (`#securitization`)
- Flow: Lender originates → sells to Fannie/Freddie → GSE bundles into MBS → investors buy → servicer collects payments
- Participants: Originator, GSE (Fannie Mae, Freddie Mac, Ginnie Mae), MBS investors, Loan servicer
- Key: Originator makes money on origination fees + servicing rights. GSE guarantees default risk. Investors get yield.
- Callout: "Fannie/Freddie guarantee ~70% of all US mortgages. If they went bankrupt (2008), the entire housing market collapses."

**3. Servicer vs Lender vs Investor** (`#participants`)
- 3-column comparison:
  - **Lender:** Makes the loan (Wells Fargo, Rocket Mortgage). Makes money on origination.
  - **Servicer:** Collects payments, handles escrow, processes defaults (could be same or different entity). Makes money on servicing fee (0.25-0.50%).
  - **Investor:** Owns the loan (pension fund, insurance company via MBS). Makes money on interest payments.
- Key: These three roles are often split across different companies. Borrower interacts with servicer, but investor owns the loan.

**4. Title & Escrow Participants** (`#titleescrow`)
- Flow: Buyer/seller → agents → title search → title insurance → escrow account → closing
- Explain: Title insurance ($1000-3000, one-time, protects against liens/claims), Escrow (holds funds until closing conditions met)
- Key: Title insurance is a $20B industry with ~95% profit margins because claims are <5% of premiums. Massive disruption opportunity.

**5. iBuying Model Comparison** (`#ibuying`)
- Cards: Opendoor (buy sight-unseen, resell), Zillow Offers (RIP, failed 2021), Offerpad (similar to Opendoor)
- Compare: Traditional sale (60 days, 6% commission) vs iBuyer (14 days, 5-7% service fee)
- Why iBuying is hard: home values are hard to predict, holding costs, renovation costs, market risk
- Callout: "Zillow lost $881M on iBuying in 2021 because their pricing algorithm overvalued homes. Home price prediction is harder than it looks."

### Color Palette
```css
--mr-buyer-bg: #eff6ff; --mr-buyer-text: #1e40af;       /* Blue */
--mr-lender-bg: #f0fdf4; --mr-lender-text: #15803d;     /* Green */
--mr-gse-bg: #eef2ff; --mr-gse-text: #3730a3;           /* Indigo */
--mr-title-bg: #fffbeb; --mr-title-text: #b45309;       /* Amber */
--mr-investor-bg: #faf5ff; --mr-investor-text: #7e22ce; /* Purple */
```

---

## Map 8: Crypto Exchange Ecosystem

**PM Relevance:** Coinbase, Kraken, Gemini, Chainalysis
**Prefix:** `cx` | **Color:** Orange/Amber (crypto gold)
**Route:** `/resources/ecosystem-maps/crypto-exchange`

### Diagrams (5)

**1. CEX vs DEX Architecture** (`#cex-dex`)
- Two-panel comparison:
  - **CEX (Centralized Exchange):** Coinbase, Binance, Kraken. Custodial (holds your keys). Order book matching. KYC required. Fast. Regulated.
  - **DEX (Decentralized Exchange):** Uniswap, dYdX, Curve. Non-custodial (your keys, your coins). AMM (automated market maker). No KYC. Slower. Unregulated.
- Trade-off spectrum: Speed + convenience (CEX) ↔ Privacy + self-sovereignty (DEX)

**2. Order Book Mechanics** (`#orderbook`)
- Visual: Bid/ask spread, limit orders, market orders, depth chart
- Show: How a $10K BTC market buy executes against limit orders
- Compare: Traditional order book (CEX) vs AMM/liquidity pools (DEX, Uniswap x*y=k formula)

**3. Custody Layers** (`#custody`)
- Layers: Self-custody (hardware wallet) → Exchange custody (Coinbase) → Institutional custody (Anchorage, BitGo, Coinbase Prime)
- Key: "Not your keys, not your coins" — FTX collapse demonstrated this ($8B customer funds lost)
- Regulation: SEC pushing for qualified custodians, SOC 2 for crypto custody

**4. On/Off Ramp Flows** (`#ramps`)
- On-ramp: Fiat → crypto (bank transfer → exchange → buy BTC/ETH)
- Off-ramp: Crypto → fiat (sell crypto → exchange → bank withdrawal)
- Friction points: KYC, bank integration (many banks block crypto), transaction limits, processing time
- Alternatives: P2P (LocalBitcoins), ATMs, card-based purchases (Moonpay, Transak)

**5. Stablecoin Rails** (`#stablecoins`)
- Types: Fiat-backed (USDC, USDT), Algo-stable (DAI), commodity-backed (PAXG)
- Flow: How stablecoins work as payment rails (mint → transfer → redeem)
- Key: USDC + USDT process >$10T/year in transfers. That's more than Visa.
- Risk: Tether reserves controversy, Circle's transparency, regulatory pressure

### Color Palette
```css
--cx-btc-bg: #fff7ed; --cx-btc-text: #9a3412;          /* Orange (Bitcoin) */
--cx-eth-bg: #eef2ff; --cx-eth-text: #3730a3;           /* Indigo (Ethereum) */
--cx-stable-bg: #f0fdf4; --cx-stable-text: #15803d;     /* Green (stablecoins) */
--cx-exchange-bg: #faf5ff; --cx-exchange-text: #7e22ce;  /* Purple (exchanges) */
--cx-custody-bg: #f1f5f9; --cx-custody-text: #334155;   /* Slate (custody) */
```

---

## Map 9: InsurTech Ecosystem

**PM Relevance:** Lemonade, Root, Hippo, Coalition, Pie Insurance
**Prefix:** `it` | **Color:** Blue/Cyan (trust/protection)
**Route:** `/resources/ecosystem-maps/insurtech`

### Diagrams (5)

**1. Risk Pooling & Reinsurance Tower** (`#riskpool`)
- Layer diagram: Policyholder premiums → Primary insurer (risk pool) → Reinsurer (excess risk) → Retrocession (reinsurance of reinsurance)
- Key: Insurance is pooling risk. Reinsurance is insurance for insurers. It's turtles all the way down.
- Numbers: Global reinsurance market ~$350B. Top 5 reinsurers (Munich Re, Swiss Re, Hannover Re, Berkshire, SCOR) control ~35%.

**2. Claims Processing Flow** (`#claims`)
- Sequence: Loss event → Claim filed → Adjuster assigned → Investigation → Estimate → Approval/Denial → Payment
- Compare: Traditional (30-60 days, human adjuster) vs AI-powered (Lemonade: 3 seconds for simple claims)
- Key: Claims processing is the moment of truth. Fast, fair claims = customer retention. Slow, adversarial = churn + lawsuits.

**3. MGA vs Carrier vs Broker** (`#participants`)
- 3-column comparison:
  - **Carrier:** Owns the risk pool, writes the policy (State Farm, Allstate, Progressive)
  - **MGA (Managing General Agent):** Underwrites on behalf of carrier, but doesn't hold risk (Coalition, At-Bay)
  - **Broker:** Sells policies from multiple carriers to customers (Marsh, Aon, independent agents)
- Key: MGAs are the InsurTech sweet spot — technology-driven underwriting without needing a balance sheet.

**4. Embedded Insurance Distribution** (`#embedded`)
- Flow: User buys product (car, home, trip) → Insurance offered at point of sale → One-click purchase
- Examples: Tesla insurance (built into car purchase), Airbnb host protection, Amazon device protection
- Key: Embedded insurance has 3-5x higher conversion than standalone because it's offered at the moment of need.

**5. InsurTech Business Models** (`#bizmodels`)
- Cards: Full-stack carrier (Lemonade), MGA (Coalition), Distribution/broker (Policygenius), Claims tech (Tractable), Data/underwriting (Cape Analytics)
- Compare: Full-stack = own risk + technology. MGA = technology only, rent balance sheet. Distribution = customer acquisition.

### Color Palette
```css
--it-carrier-bg: #eff6ff; --it-carrier-text: #1e40af;    /* Blue */
--it-mga-bg: #f0fdfa; --it-mga-text: #0f766e;            /* Teal */
--it-broker-bg: #fff7ed; --it-broker-text: #9a3412;       /* Orange */
--it-claims-bg: #faf5ff; --it-claims-text: #7e22ce;       /* Purple */
--it-risk-bg: #fef2f2; --it-risk-text: #991b1b;           /* Red */
```

---

## Map 10: Brokerage & Wealth Management Ecosystem

**PM Relevance:** Robinhood, Betterment, Wealthfront, Fidelity, Schwab
**Prefix:** `bw` | **Color:** Indigo/Purple (finance/prestige)
**Route:** `/resources/ecosystem-maps/brokerage-wealth`

### Diagrams (5)

**1. Trade Clearing (DTCC / T+1)** (`#clearing`)
- Sequence: Investor places order → Broker sends to exchange/ATS → Matching engine → NSCC (National Securities Clearing Corp) → DTC (Depository Trust Company) → Settlement (T+1)
- Key: As of May 2024, US moved from T+2 to T+1 settlement. Reduces counterparty risk. Europe still T+2.
- Participants: Investor, Broker, Exchange (NYSE, Nasdaq), NSCC, DTC, Custodian bank

**2. Custody Chain** (`#custody`)
- Layers: Investor → Broker (holds in street name) → Custodian (BNY Mellon, State Street) → DTC (ultimate depository)
- Key: You don't actually "own" shares. Your broker holds them in "street name." DTC holds the master record. This is why direct registration (DRS) became a meme stock movement.

**3. RIA vs Broker-Dealer** (`#riavsbd`)
- Two-panel comparison:
  - **Broker-Dealer:** Sells products, earns commissions. Suitability standard (product must be "suitable"). Regulated by FINRA/SEC.
  - **RIA (Registered Investment Advisor):** Advises clients, earns fees (AUM-based). Fiduciary standard (must act in client's best interest). Regulated by SEC.
- Key: The shift from BD to RIA is the defining trend. ~$30T now managed by RIAs. Fiduciary duty matters.

**4. PFOF Controversy** (`#pfof`)
- Flow: Retail investor → Robinhood → routes order to market maker (Citadel Securities, Virtu) → market maker fills order
- What PFOF is: Market maker pays Robinhood $0.002-0.004/share for the order flow. Robinhood makes money. User gets "free" trades.
- Controversy: Is the market maker giving best execution? SEC proposed ban (2023), delayed. EU banned it (2026).
- Both sides: "Free trades democratize investing" vs "Hidden cost through worse execution"

**5. Robo-Advisor Model** (`#roboadvisor`)
- Flow: User answers risk questionnaire → Algorithm selects portfolio (ETFs) → Auto-rebalancing → Tax-loss harvesting
- Players: Betterment, Wealthfront, Schwab Intelligent Portfolios, Vanguard Digital Advisor
- Compare: Robo (0.25% fee, $0 minimum) vs Human advisor (1% fee, $250K minimum) vs DIY (0% fee, your time)
- Key: Robo-advisors manage ~$1T AUM. Growing but haven't killed human advisors (yet).

### Color Palette
```css
--bw-investor-bg: #eff6ff; --bw-investor-text: #1e40af;  /* Blue */
--bw-broker-bg: #eef2ff; --bw-broker-text: #3730a3;      /* Indigo */
--bw-exchange-bg: #f0fdf4; --bw-exchange-text: #15803d;   /* Green */
--bw-clearing-bg: #faf5ff; --bw-clearing-text: #7e22ce;   /* Purple */
--bw-custody-bg: #fffbeb; --bw-custody-text: #b45309;     /* Amber */
```

---

## Map 11: E-commerce Fulfillment Ecosystem

**PM Relevance:** Amazon, Shopify, TikTok Shop, Walmart Marketplace
**Prefix:** `ef` | **Color:** Teal/Green (logistics)
**Route:** `/resources/ecosystem-maps/ecommerce-fulfillment`

### Diagrams (5)

**1. 1P vs 3P vs FBA Comparison** (`#models`)
- 3 architecture cards:
  - **1P (First Party):** Amazon buys from brand → stores in warehouse → ships to customer. Amazon owns inventory.
  - **3P (Third Party):** Seller lists on marketplace → ships from own warehouse. Seller owns inventory.
  - **FBA (Fulfilled by Amazon):** Seller sends inventory to Amazon warehouse → Amazon picks, packs, ships. Seller owns inventory, Amazon does logistics.
- Key: 60% of Amazon sales are 3P. FBA is ~70% of 3P volume. FBA is Amazon's logistics-as-a-service.

**2. Last-Mile Logistics Stack** (`#lastmile`)
- Layers: Warehouse → Sortation center → Delivery station → Last mile (driver) → Customer doorstep
- Players: Amazon Logistics, UPS, FedEx, USPS, DHL, gig drivers (Flex, DoorDash)
- Cost breakdown: Last mile = 53% of total shipping cost. Sorting/transit = 37%. Warehouse = 10%.
- Key: Last mile is the most expensive and hardest to optimize. Amazon built its own delivery network to control it.

**3. Returns Economics** (`#returns`)
- Flow: Customer returns → RMA → Ship back → Warehouse receives → Inspect → Restock or liquidate
- Stats: E-commerce return rate ~20-30% (vs 8-10% in-store). Returns cost $800B/year globally.
- Economics: Average return costs merchant $10-15 in shipping + handling + restocking. Many items cheaper to destroy than restock.
- Key: Returns are the hidden margin killer. Free returns = customer expectation but unsustainable economics.

**4. Seller Fee Breakdown** (`#fees`)
- For a $100 product sold on Amazon FBA:
  - Referral fee: $15 (15%)
  - FBA fee: $5-8 (pick, pack, ship)
  - Storage fee: $0.50-2.00/month
  - Advertising: $5-15 (PPC required to be visible)
  - Total Amazon take: $25-40 (25-40%)
  - Seller keeps: $60-75 (before COGS)
- Compare with Shopify: $39/month + 2.9% payment processing. Total platform cost: ~5-8%.
- Key: Amazon takes 25-40% but provides traffic + fulfillment. Shopify takes 5-8% but you bring your own traffic.

**5. Amazon Flywheel** (`#flywheel`)
- The virtuous cycle: Lower prices → More customers → More sellers → More selection → Better experience → Lower costs (at scale) → Lower prices
- Show the loop with each node as a step
- Counter-forces: What breaks the flywheel (quality degradation, fake reviews, seller exits, regulatory pressure)
- Key: The flywheel is real but has limits. Amazon's marketplace quality is declining as Chinese sellers flood with low-quality goods.

### Color Palette
```css
--ef-seller-bg: #f0fdf4; --ef-seller-text: #15803d;      /* Green */
--ef-amazon-bg: #fff7ed; --ef-amazon-text: #9a3412;       /* Orange */
--ef-logistics-bg: #eff6ff; --ef-logistics-text: #1e40af; /* Blue */
--ef-customer-bg: #faf5ff; --ef-customer-text: #7e22ce;   /* Purple */
--ef-returns-bg: #fef2f2; --ef-returns-text: #991b1b;     /* Red */
```

---

## Build Instructions (All Tier 3 Maps)

**Per map, create:**
- 1 CSS file (`code/app/static/css/{slug}.css`)
- 1 main template (`code/app/templates/resources/{slug}.html`)
- 1 subnav partial (`code/app/templates/resources/partials/{prefix}_subnav.html`)
- 4-5 diagram partials (`code/app/templates/resources/partials/{prefix}_diagram_*.html`)
- Route in `resources.py`
- Card in `ecosystem_maps.html` gallery

**Follow the exact pattern of:**
- `financial_ecosystem.html` (main template structure)
- `financial-ecosystem.css` (CSS variable convention)
- `fe_subnav.html` (subnav pattern)
- `fe_diagram_*.html` (diagram partial pattern)

**Each map should have:**
- Breadcrumb: Resources > Ecosystem Maps > {Map Name}
- Page header with title + description
- Sticky subnav with diagram section links
- Diagram partials with dividers
- Scroll-tracking JS
- Footer attribution
- Full dark mode support
- Mobile responsive


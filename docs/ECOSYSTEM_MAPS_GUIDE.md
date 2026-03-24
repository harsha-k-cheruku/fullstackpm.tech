# Ecosystem Research & Build Instructions
**For:** Claude Code thread building Ecosystem Maps for fullstackpm.tech
**Reference file:** `/Users/sidc/Projects/claude_code/product_breakdowns/drafts/financial-ecosystem-visual-v2.html`

---

## What You Are Building

Each ecosystem map is a self-contained, interactive HTML file that gives a product manager a complete mental model of an industry — who the participants are, how money flows, what the technology layers are, how transactions clear, and what the PM's job looks like inside it.

The financial ecosystem map (`financial-ecosystem-visual-v2.html`) is the gold standard reference. Every new ecosystem map must follow the same visual design system, diagram structure, and depth of analysis. Read it fully before building anything new.

---

## Step 0: Read the Reference File First

Before researching any new ecosystem, read the full reference:
```
/Users/sidc/Projects/claude_code/product_breakdowns/drafts/financial-ecosystem-visual-v2.html
```

Understand:
- The CSS design system (variables, class names, color palette)
- The seven diagram types and what each one teaches
- The nav structure and tab-switching JS pattern
- How layer annotations and color chips work
- The tone: educational, precise, PM-oriented — not marketing copy

You will reuse the CSS classes and design patterns from this file in every new ecosystem map. Copy the `<style>` block as your starting point and add ecosystem-specific styles on top.

---

## The Standard Diagram Set

Every ecosystem map must include all seven of these diagrams, adapted to the specific industry. The questions each diagram answers are fixed — only the content changes.

### Diagram 1: The Layer Map (Nested Boxes)
**Question it answers:** Who sits where? What depends on what?

Structure every industry as nested layers — innermost = most foundational, outermost = closest to end user. The nesting communicates: outer layers cannot exist without inner layers.

Standard layer pattern (adapt names and colors per industry):
- **Innermost core:** The foundational regulated entity (banks in finance, telcos in comms, grid operators in energy)
- **Layer 1 — The Rails:** The pipes that carry the core resource (ACH/Fedwire in finance, spectrum/fiber in telco, electrical grid in energy)
- **Layer 2 — Infrastructure APIs:** Middleware that makes the rails accessible to builders without a license (Plaid/Marqeta in finance, Twilio/AWS in tech, data APIs in healthcare)
- **Layer 3 — Products:** The consumer-facing or business-facing products built on the infrastructure (lending/payments/BNPL in finance, apps/SaaS in tech)
- **Outermost — End Users:** Whoever consumes the final product
- **External panel — Capital/Resource Sources:** Whoever funds or supplies the core resource (not a technology layer — a financial/supply relationship)

Color coding to maintain across all maps (inherit from reference):
- End Users: blue (`#eff6ff` / `#3b82f6`)
- Layer 3 Products: green/yellow/purple (per product type)
- Layer 2 Infrastructure: pink/red (`#fff1f2` / `#fda4af`)
- Layer 1 Rails: grey (`#f8fafc` / `#94a3b8`)
- Core: deep blue center
- Capital/Resource sources: orange (`#fff7ed` / `#fdba74`)

### Diagram 2: The Four Business Models
**Question it answers:** What are the distinct ways companies make money in this industry?

Every mature industry has 3-5 distinct business model archetypes. Identify them. For each model:
- Who the participants are
- The step-by-step flow of value/money
- How the company earns revenue (what triggers the fee, what the fee is)
- The key PM challenge specific to that model

Use the 4-column grid layout from the reference. Each model gets its own card with flow steps, earn badge, and PM challenge callout.

### Diagram 3: How a Transaction Clears (Tabbed, One Per Business Model)
**Question it answers:** From "I want this" to "transaction complete" — every participant, every handoff, every decision point.

Use the tab-switcher pattern from the reference. One tab per business model from Diagram 2. Each tab shows:
- Participant row across the top (icons + labels)
- Step-by-step sequence with labeled rows
- Color-coded cells: `active` (blue) = this party is doing something, `sending` (green) = this party is initiating a transfer/action, `decision` (purple) = a model or algorithm is running
- A `seq-model-note` callout explaining the model's core logic
- A `seq-earn-bar` at the bottom summarizing who earns what

### Diagram 4: The Core Distinction (What Makes This Industry Unique)
**Question it answers:** What is the fundamental problem this industry solves, and how do the sub-categories differ in their approach?

In finance: Lending vs. Payments vs. BNPL (time vs. space vs. both).
Adapt this to each industry's core tension. Examples:
- Ad Tech: Guaranteed vs. Programmatic vs. Direct (certainty vs. price optimization vs. relationship)
- Healthcare: Fee-for-service vs. Capitation vs. Value-based (activity vs. population vs. outcomes)
- Travel: Inventory ownership vs. OTA vs. Meta (principal vs. agent vs. aggregator)

Include the concept callout boxes (3-column grid explaining the distinction in plain English) and the layer activation chips at the bottom of each card showing which layers are involved.

### Diagram 5: The Data Flywheel
**Question it answers:** Why does the market leader keep winning? What is the self-reinforcing loop?

Every digital industry has a flywheel. Find it. Map it as a linear chain that loops back to the start. Include:
- The 5-7 steps of the flywheel
- Which steps are "highlight" (the reinforcing accelerators)
- A dark-panel insight box explaining: what the moat is, how the flywheel can run in reverse (failure mode), and the time lag between action and feedback
- A scoping note if the flywheel only applies to specific business models (not all companies in the industry benefit equally)

### Diagram 6: How Value/Money Actually Moves (Two-Panel)
**Question it answers:** What infrastructure does the transaction use? How do capital/resource flows differ from product flows?

Two panels:
- **Left panel:** How a product company reaches the underlying infrastructure (the "fintech stack" equivalent — product → API → rail → end user)
- **Right panel:** How capital or core resources flow at the institutional level (bypassing the middleware layer because they're regulated/licensed directly)

Include rail badges (colored pills) showing the specific protocol/mechanism used at each connection.

### Diagram 7: User Journeys (Multiple Scenarios)
**Question it answers:** What actually happens, step by step, from the user's perspective and behind the scenes?

Include 4-5 distinct scenarios that cover different user types and transaction paths. Each journey card shows:
- Who the persona is and the scenario
- Timeline (how long each phase takes)
- Step-by-step with color coding: green steps = value/money moves, purple steps = a model or algorithm runs
- Rail badges where applicable
- A footer summarizing what infrastructure was used and who earned what

---

## Research Framework — How to Investigate a New Ecosystem

### Phase 1: Map the participants (1-2 hours)

Ask: Who is involved in every transaction in this industry, from end to end?

Go beyond obvious participants. In finance, "borrower and lender" misses: credit bureaus, bank data APIs, card networks, capital partners, servicers, regulators. Every industry has hidden middle layers.

For each participant, answer:
- What do they want from the transaction?
- What are they afraid of?
- How do they earn money?
- What regulatory status do they have (licensed? exempt? gray area?)
- What would happen to the system if they disappeared?

Sources: 10-K filings of public companies in the space, S-1s, industry association white papers, company engineering blogs, academic papers on market structure.

### Phase 2: Trace the money (1-2 hours)

Follow a single dollar from payer to payee. At every step ask:
- Who touches this dollar?
- What do they deduct before passing it on?
- What rail/protocol carries it?
- How long does it take?
- What could cause it to fail at this step?

Money flows are almost always more complex than they appear. "The advertiser pays the publisher" skips: the DSP, SSP, ad exchange, data broker, viewability vendor, and ad server that each take a cut.

Draw the money flow before designing any diagram. Get it accurate first.

### Phase 3: Find the technology layers (1 hour)

Ask: What infrastructure does a new entrant need to access to build in this space?

Identify:
- The regulated "pipe" (the thing only licensed entities can own/operate)
- The middleware that unlocks access without a license (the "Plaid equivalent")
- The product layer built on top

In every industry there is a moment where you either have a license/access or you don't. Find that line. Everything below it is "Layer 1 and below." Everything above it is "Layer 2 and 3."

### Phase 4: Identify the business model archetypes (1 hour)

Ask: What are the fundamentally different ways companies make money in this space?

Look for differences in:
- Who the customer is (B2C vs. B2B vs. B2B2C)
- What triggers revenue (per transaction, subscription, take rate, spread, float)
- Where risk lives (on the company's balance sheet, on a partner, distributed)
- What the company owns vs. intermediates

A business model is "fundamentally different" if it requires different key metrics, different cross-functional partners, and different PM skills. If two models require the same PM skills, they're probably variants of the same model.

### Phase 5: Find the flywheel (30 minutes)

Ask: What does more usage produce that makes the product better for the next user?

The flywheel is almost always data-driven in digital industries. More transactions → more data → better model/algorithm → better product → more transactions.

But ask: which companies in this industry actually benefit from this flywheel? Some business models in the space don't accumulate data that improves their product. Scope the flywheel correctly.

### Phase 6: Map the failure modes (30 minutes)

Ask: What can break?

Every industry has 3-4 structural failure modes. These usually follow the same pattern as the financial ecosystem:
- Supply shock (the resource/capital/inventory dries up)
- Quality shock (the underlying model/product fails)
- Demand shock (users stop showing up)
- Regulatory shock (the rules change)

Understanding failure modes is what separates a PM who has memorized the industry from one who actually understands it. Include them in the diagram notes and flywheel "runs in reverse" section.

---

## Candidate Ecosystems — Prioritized

These are ordered by: (a) PM interview frequency, (b) how teachable the structure is, (c) how differentiating the content would be vs. what already exists online.

### Priority 1 — Build These First

**1. Programmatic Advertising / Ad Tech**
The structure: Advertiser → DSP → Ad Exchange → SSP → Publisher. Real-time bidding happens in 100ms. Every layer takes a cut. The data layer (DMPs, CDPs, identity graphs) is as complex as the money layer.
Core tension: Guaranteed vs. Programmatic vs. Direct deals (certainty vs. price optimization vs. relationships).
Key PM domain: Yield optimization, auction mechanics, viewability, brand safety, identity resolution post-cookie.
Why it's hard: Nobody outside ad tech understands the full stack. This is a major gap content can fill.

**2. Travel Commerce / OTA**
The structure: Traveler → OTA/Meta → GDS → Airline/Hotel inventory. The inventory is perishable (an empty seat tonight is worthless tomorrow). Price is dynamic. The B2B2C layering is complex.
Core tension: Inventory ownership (Airbnb, iBuyer) vs. OTA (Expedia, Booking) vs. Metasearch (Google Flights, Kayak).
Key PM domain: Yield management, price elasticity, search ranking, loyalty programs, fintech products layered on top (price freeze, travel insurance, BNPL for flights).
Why it's hard: The GDS layer (Amadeus, Sabre, Travelport) is invisible to most PMs but controls access to inventory.

**3. Healthcare / Health Insurance**
The structure: Patient → Provider → Clearinghouse → Payer (insurance). Claims processing is a distinct infrastructure. Prior authorization is a product problem. The payer is often the adversary.
Core tension: Fee-for-service vs. Capitation vs. Value-based care (activity vs. population health vs. outcomes).
Key PM domain: Prior auth, clinical decision support, network adequacy, claims adjudication, patient engagement, care navigation.
Why it's hard: Regulation (HIPAA, ACA, state mandates) shapes every product decision. PMs who understand this are rare.

**4. Two-Sided Marketplace (Physical Goods)**
The structure: Buyer → Platform → Seller → Fulfillment → Buyer. But there are four types of marketplace and they need different PM skills: pure (Etsy), managed (Amazon 3P), vertical (Faire), and services (Thumbtack).
Core tension: Supply liquidity vs. demand quality vs. trust infrastructure.
Key PM domain: Search ranking, fraud prevention, dispute resolution, seller economics, logistics integration, cross-border.
Why it's hard: Most PM content treats all marketplaces the same. The distinctions between physical goods, services, and experiences marketplaces are significant and underexplained.

### Priority 2 — Build After Priority 1

**5. Payments Infrastructure (Developer-First)**
The structure: Merchant → Processor (Stripe) → Card Network → Issuing Bank → Cardholder. The acquiring side and issuing side have completely different economics. Fraud is the central PM problem.
Core tension: Developer-first (Stripe) vs. Enterprise (Adyen) vs. SMB (Square) vs. Consumer (PayPal).
Key PM domain: Authorization rates, fraud models, chargeback management, international expansion, embedded finance.
Note: Partially covered in the financial ecosystem v2. This would be a dedicated deep dive on the payments side only.

**6. SaaS / B2B Analytics Platform**
The structure: Data source → ETL/pipeline → Data warehouse → BI/analytics layer → End user (analyst). The "rails" are the data infrastructure. The "product" is the query layer and visualization.
Core tension: Self-serve analytics vs. embedded analytics vs. AI-native querying.
Key PM domain: Data modeling UX, query performance, permission/governance, adoption metrics, time-to-insight.
Why it's interesting: The PM must understand both the data engineering stack and the analyst's job-to-be-done. Very few people span both.

**7. Ride-Sharing / Gig Economy**
The structure: Rider → Platform → Driver → Fulfillment. Supply (drivers) is elastic and price-sensitive. Demand is location- and time-dependent. Surge pricing is the clearing mechanism.
Core tension: Pure marketplace (Uber) vs. Fleet ownership (autonomous) vs. Enterprise (corporate ride accounts).
Key PM domain: Dynamic pricing, supply forecasting, driver incentives, matching algorithms, safety systems.
Why it's interesting: Surge pricing is the most visible marketplace clearing mechanism in consumer tech. Most people experience it but don't understand it.

**8. Consumer Subscription / Creator Economy**
The structure: Creator → Platform → Subscriber → Monetization. The "content" is the inventory. Discovery is the clearing mechanism (how content finds audience).
Core tension: Subscription (Substack, Patreon) vs. Ad-supported (YouTube) vs. Tipping (Twitch) vs. Commerce (Shopify creators).
Key PM domain: Churn, LTV, discovery algorithms, creator monetization tools, payment processing for recurring revenue.

---

## Build Instructions — Step by Step

### Step 1: Research (complete Phase 1-6 above)

Before writing a single line of HTML, have answers to:
- Complete participant list with incentives and fears
- Full money flow traced dollar-by-dollar
- Technology layer map (what's the rails, what's middleware, what's product)
- 3-5 distinct business model archetypes
- The flywheel and who benefits from it
- 3-4 failure modes

Document your research in a markdown file first:
```
/Users/sidc/Projects/claude_code/product_breakdowns/drafts/[ecosystem]-research.md
```

### Step 2: Copy the reference HTML as your starting point

```bash
cp /Users/sidc/Projects/claude_code/product_breakdowns/drafts/financial-ecosystem-visual-v2.html \
   /Users/sidc/Projects/claude_code/product_breakdowns/drafts/[ecosystem]-ecosystem-visual.html
```

Replace the content section by section. Keep all CSS. Keep the JS tab-switcher. Keep the nav structure. Only change content and add any ecosystem-specific styles at the bottom of the `<style>` block.

### Step 3: Build in diagram order

Build one diagram at a time. Validate visually before moving to the next. Do not batch-build all seven at once — errors compound.

Order: Diagram 1 (Layer Map) → Diagram 2 (Business Models) → Diagram 3 (Transaction Sequence, tabs) → Diagram 4 (Core Distinction) → Diagram 5 (Flywheel) → Diagram 6 (Value/Money Flow) → Diagram 7 (User Journeys)

### Step 4: Quality checks before publishing

For each diagram, ask:
- Is every participant labeled and color-coded?
- Does the money/value flow make sense if traced step by step?
- Are the layer annotations accurate (is this really Layer 2, or is it Layer 3)?
- Is the content generic (applicable to the whole industry) or accidentally specific to one company?
- Would a PM who has never worked in this industry understand it after reading?
- Is the tone educational and precise, not promotional?

For the file overall:
- Does the nav work and link to all seven diagrams?
- Do all tab-switchers function correctly?
- Does the file render correctly at 1200px wide and at 768px wide (tablet)?
- Is the file self-contained (no external dependencies beyond the browser)?

### Step 5: Add to the site

1. Copy the finished file to the site static directory:
```bash
cp /Users/sidc/Projects/claude_code/product_breakdowns/drafts/[ecosystem]-ecosystem-visual.html \
   /Users/sidc/Projects/claude_code/fullstackpm.tech/code/app/static/resources/[ecosystem]-ecosystem.html
```

2. Add a route to the resources router (`code/app/routers/resources.py`):
```python
@router.get("/resources/ecosystem-maps/[ecosystem]")
async def [ecosystem]_ecosystem():
    path = settings.static_dir / "resources" / "[ecosystem]-ecosystem.html"
    return FileResponse(str(path))
```

3. Add a card to the Ecosystem Maps index page (`code/app/templates/resources/ecosystem_maps.html`) following the existing card pattern.

4. Commit and push:
```bash
git add .
git commit -m "Add [Ecosystem] ecosystem map to Ecosystem Maps section"
git push origin main
```

---

## Quality Bar — What "Good" Looks Like

A good ecosystem map passes this test: a smart PM who has never worked in the industry reads it and can, the next day, have a credible domain conversation in an interview. They can name the participants, explain how money flows, describe the business model types, and articulate what the PM's core challenge is in each model.

A bad ecosystem map:
- Lists participants without explaining incentives or fears
- Shows money flow without explaining what can break it
- Describes business models without specifying how revenue is triggered
- Presents the flywheel without scoping which companies benefit
- Uses company-specific examples as if they're universal (e.g., "Uber's surge algorithm" instead of "ride-share dynamic pricing")
- Is accurate but shallow — gives facts without building mental models

The financial ecosystem v2 is the calibration. Match that depth. If a section feels thinner, it needs more research, not shorter text.

---

## Content Voice and Style Rules

- **No marketing language.** "Revolutionary," "seamless," "best-in-class" — cut it. Every sentence should be informational.
- **Name the mechanism, not just the outcome.** Not "payments are fast." Instead: "Card authorization runs in ~1.5 seconds because the network routes between issuing and acquiring banks via the card scheme's private network, not the public internet."
- **Make tradeoffs explicit.** Every business model has a tradeoff. Every layer has a cost. Show both sides.
- **Scope claims precisely.** "AI models improve with data" is vague. "The underwriting model's predicted default probability improves as more labeled repayment outcomes are added to the training set" is precise.
- **Use numbers when they exist publicly.** Settlement timelines, fee ranges, processing speeds — these make diagrams credible. Cite the source in a comment if it's from a filing.
- **Write for re-reading, not skimming.** These are reference documents. They don't need to hook someone in the first paragraph. They need to be accurate and complete enough to return to.

---

## File Naming Convention

```
[industry-slug]-ecosystem-visual.html
```

Examples:
- `adtech-ecosystem-visual.html`
- `travel-ecosystem-visual.html`
- `healthcare-ecosystem-visual.html`
- `marketplace-ecosystem-visual.html`
- `saas-ecosystem-visual.html`

Draft location: `/Users/sidc/Projects/claude_code/product_breakdowns/drafts/`
Published location: `/Users/sidc/Projects/claude_code/fullstackpm.tech/code/app/static/resources/`

---

## Reference Files

| File | Purpose |
|---|---|
| `financial-ecosystem-visual-v2.html` | Gold standard reference — read before building anything |
| `financial-ecosystem-diagrams.md` | Mermaid source diagrams for the financial ecosystem (concept reference) |
| `09_Marketplace_Clearing_Deep_Dive.md` | Deep dive on how clearing works in lending — model for the depth of analysis expected |
| `2026-03-22-pm-prep-papers-business-model-deep-dives.md` | The series strategy — understand what each ecosystem map is part of |

All files at: `/Users/sidc/Projects/claude_code/product_breakdowns/drafts/` and `/Users/sidc/Projects/claude_code/linkedin_job_search/March2026 applications/Upstart/`

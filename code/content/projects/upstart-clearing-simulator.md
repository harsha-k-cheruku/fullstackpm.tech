---
title: "Upstart Lifecycle Simulator"
description: "Full loan lifecycle simulator for Upstart's capital marketplace — pipeline generation, three-layer clearing engine, animated 36-month portfolio performance, capital partner health monitoring, and mid-simulation intervention testing."
tech_stack: [Vanilla JS, Chart.js, Tailwind CSS, Jinja2, FastAPI]
status: "live"
featured: true
display_order: 2
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/lifecycle-simulator"
problem: "Marketplace clearing decisions have a 90-day feedback delay — a PM changes partner eligibility today but doesn't see the EPD impact for months. The 2022 capital crunch showed what happens when this delay prevents preventive action: Upstart held $1B+ on its balance sheet."
approach: "Build an interactive lifecycle simulator that compresses 36 months of portfolio evolution into 3 minutes. Generate synthetic borrowers, clear them through a three-layer engine, then watch month-by-month performance with live capital partner metrics — including the ability to intervene mid-simulation and see downstream effects."
solution: "A browser-based sandbox with 5 connected views: Pipeline & Clearing (generate + match 100 loans), Portfolio Timeline (animated month-by-month with intervention), Marketplace Analytics (three-stakeholder health dashboard), Loan Deep Dive (step-by-step borrower walkthrough), and Re-Application Funnel (product roadmap framing). All client-side JS — no backend computation."
---

## What

A full lifecycle simulator for Upstart's capital marketplace. Not just the clearing moment — the entire journey from borrower pipeline through 36 months of portfolio performance.

### Five Core Views

**1. Pipeline & Clearing**
Generate 100 synthetic borrowers and run them through the three-layer engine: eligibility → pricing (Classic vs Model 18 side-by-side) → waterfall routing across 5 capital partners. See clearing outcomes for each model and compare.

**2. Marketplace Performance**
Real-time aggregated health dashboard showing total loan amount, average APR, default rates, and partner utilization. Compare "Total Marketplace" vs individual partners, or Partner A vs Partner B.

**3. Portfolio Timeline**
Scrub through 36 months of loan performance: payments, delinquencies, defaults, early payoffs. Charts show portfolio health evolution and loss trends.

**4. Loan Deep Dive**
Click any borrower in Pipeline to walk through their clearing decision step-by-step (eligibility → pricing → routing → funded), with payment history if lifecycle has run.

**5. Re-Application Funnel**
Product roadmap stub showing how lifecycle data can predict re-applications and lower CAC for returning borrowers.

### Key Features

- **Side-by-side Model Comparison** — See Model 18 vs Classic outcomes for the same borrower
- **Scenario Presets** — Healthy Market, Capital Crunch (2022), Rate Spike — each with different clearing rules
- **Hidden-Prime Discovery** — Model 18 Score shows effective FICO (FICO + 50 if hidden-prime) for easy comparison
- **Dynamic Updates** — Change a scenario and run clearing again; all metrics in Marketplace Performance update instantly

## Why

Upstart's capital marketplace is one of the most sophisticated clearing engines in fintech — but the feedback loops are invisible. A PM adjusting partner eligibility today doesn't see the EPD impact for 90 days. This simulator makes the causal chain visible:

### The Problem
- **90-day feedback delay** — Changes to clearing rules or partner eligibility take months to show in portfolio performance
- **2022 lesson** — Capital crunch happened partly because decision-makers couldn't see the compounding effect of tighter partner capacity in real-time
- **Black box clearing** — Few people outside the team understand how FICO pricing → Model 18 → partner routing → marketplace economics all connect

### What This Solves
**Compress time:** 36 months of portfolio evolution in 3 minutes

**Make tradeoffs tangible:** See clearing rate ↔ partner EPD ↔ balance sheet exposure in real-time

**Test interventions safely:** What if you tighten Aperture's FICO floor at Month 8? Month 14? Run both, compare outcomes.

**Three-stakeholder thinking:** Borrower experience, platform economics, and partner returns all in one view

**Model 18 intuition:** See exactly how APR-as-feature discovers hidden-prime borrowers and creates marketplace value — not just hear about it

### Who It's For
PM candidates learning marketplace dynamics, marketplace operators stress-testing decisions, data scientists understanding the pipeline, anyone curious how lending marketplaces actually work.

## How

### Technical Architecture

**Client-Side Computation**
- Entirely browser-based JavaScript — no backend API calls, no database, no network latency
- 100 borrowers × 5 partners × 36 months = 3,600 state transitions per simulation
- Completes in <200ms total

**Tech Stack**
- **Rendering:** Chart.js (time-series charts), Tailwind CSS + Jinja2 (template inheritance from site base.html)
- **Modules:** 4 self-contained JS files
  - `borrower_generation.js` — Synthetic borrower creation with realistic FICO/purpose distributions
  - `clearing_engine.js` — Three-layer engine: eligibility → pricing → waterfall routing
  - `lifecycle_engine.js` — 36-month Markov chain loan performance simulation
  - `lifecycle_simulator.js` — Main coordinator: pipeline controls, side-by-side model comparison, deep dive walkthrough

### User Flow

1. **Select Scenario** — Choose Healthy Market, Capital Crunch, or Rate Spike (or customize parameters)
2. **Generate Pipeline** — Create 100 synthetic borrowers
3. **Run Clearing** — Process through eligibility → pricing (Classic vs Model 18) → partner routing
4. **Review Results** — See KPIs, borrower table with side-by-side model comparison, filter by outcome
5. **Explore Timeline** — Scrub through 36 months; watch portfolio health and loss trends
6. **Compare Partners** — Switch to Marketplace Performance tab to see Total vs individual partner metrics
7. **Deep Dive** — Click any borrower to walk through clearing logic and payment history

### Data & Modeling

**Borrower Generation**
- FICO score distribution reflects near-prime market (620–740 mean)
- 28% hidden-prime rate (non-traditional credit strength)
- Loan amounts: $2K–$40K; purposes: debt consolidation, home improvement, etc.

**Lifecycle Model**
- Markov chain with grade-based transition probabilities (Grade A–E)
- Grade-specific 30DPD→60DPD→90DPD→default recovery rates
- Hidden-prime borrowers transition one grade better under Model 18

**Partner Configuration**
- 5 partners with FICO floors, APR minimums, capacity caps
- Forward-flow, bank, and spot-fund types (inspired by real fintech partners)
- All names obfuscated; structures based on public filings

### Limitations

- **Simplified model** — Markov chain is illustrative, not vintage-calibrated or econometrically precise
- **Scale** — 100-borrower demos show dynamics, not statistical significance
- **Statefulness** — No persistence; page refresh resets simulation
- **Stub feature** — Re-application stage is product roadmap framing, not full simulation

### Documentation

This is part of a larger PM portfolio. Product strategy documents (PRFAQ, BRD) are available on request.
- **PRFAQ** — Press release, customer FAQ, and internal context
- **BRD** — Business requirements, success metrics, and strategic context

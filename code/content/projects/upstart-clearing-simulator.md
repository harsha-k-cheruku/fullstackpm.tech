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

**Features:**
- **Pipeline & Clearing** — Generate 100 synthetic borrowers, run them through eligibility → pricing (Classic vs Model 18) → waterfall routing across 5 capital partners
- **Animated Portfolio Timeline** — Watch loans perform month-by-month: payments, delinquencies, defaults, early payoffs. Partner metrics update live.
- **Mid-Simulation Intervention** — Pause at any month, tighten a partner's eligibility or capacity, resume and see the downstream impact immediately
- **Three-Stakeholder Analytics** — Borrower Health, Upstart Platform Health, and Capital Partner Health dashboards with traffic-light indicators
- **Loan Deep Dive** — Click any borrower to walk through their clearing decision step-by-step, plus payment history if lifecycle has run
- **Scenario Presets** — Healthy Market, Capital Crunch (2022), Rate Spike — each tells a different marketplace story
- **Hidden-Prime Discovery** — See Model 18 unlock borrowers that FICO undervalues, with side-by-side pricing comparison

## Why

Upstart's capital marketplace is one of the most sophisticated clearing engines in fintech — but the feedback loops are invisible. A PM adjusting partner eligibility today doesn't see the EPD impact for 90 days. This simulator makes the causal chain visible:

- **Compress time** — 36 months of portfolio evolution in 3 minutes
- **Make tradeoffs tangible** — See clearing rate vs. partner EPD vs. balance sheet exposure in real-time
- **Test interventions safely** — What if you tighten Aperture's FICO floor at Month 8 vs. Month 14? Run both scenarios.
- **Three-stakeholder thinking** — Borrower experience, platform economics, and partner returns all in one view
- **Model 18 intuition** — See exactly how APR-as-feature discovers hidden-prime borrowers and creates marketplace value

Built for PM candidates, marketplace operators, and anyone curious about how lending marketplaces actually work.

## How

**Architecture:**
- **Computation:** Entirely client-side JavaScript — no backend API calls, no database, no network latency
- **Rendering:** Chart.js for animated charts, Tailwind CSS + Jinja2 templates (extends site base.html)
- **Modules:** 4 JS files — `borrower_generation.js` (synthetic data), `clearing_engine.js` (eligibility + pricing + routing), `lifecycle_engine.js` (month-by-month simulation), `animation_controller.js` (play/pause/resume + Chart.js updates)
- **Scale:** 100 borrowers × 5 partners × 36 months = 3,600 state transitions per simulation. Runs in <200ms total.

**The flow:**
1. Select a scenario (Healthy Market, Capital Crunch, Rate Spike) or configure custom parameters
2. Generate 100 borrowers and run them through the three-layer clearing engine
3. Review clearing results — KPIs, borrower table, filter by outcome
4. Play the portfolio timeline — watch metrics evolve month by month, animated
5. Pause → adjust partner eligibility → resume → see the intervention's impact
6. Switch to Analytics dashboard — identify at-risk partners, check platform health
7. Deep dive into any individual borrower's clearing decision and payment history

**Data sources:**
- Transition probabilities based on industry personal lending data (configurable)
- Partner structures inspired by Upstart's public filings (names obfuscated)
- Credit score distributions reflect market reality for near-prime personal lending
- All data synthetic — clear disclaimer displayed

**Limitations:**
- Simplified lifecycle model (Markov chain, not vintage-calibrated)
- 100-borrower scale (sufficient for demo, not for statistical analysis)
- No persistence — simulation state resets on page refresh
- Re-application stage is a product roadmap stub, not simulated

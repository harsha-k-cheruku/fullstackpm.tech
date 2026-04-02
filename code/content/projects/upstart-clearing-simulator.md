---
title: "Upstart Lifecycle Simulator"
description: "Browser-based simulator for Upstart's capital marketplace — generate borrower pipelines, run side-by-side Model 18 vs Classic clearing, compare 36-month portfolio performance across market scenarios, and walk through individual loan decisions step-by-step."
tech_stack: [Vanilla JS, Tailwind CSS, Jinja2, FastAPI]
status: "live"
featured: true
display_order: 2
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/lifecycle-simulator"
problem: "Marketplace clearing decisions have a 90-day feedback delay — a PM changes partner eligibility today but doesn't see the EPD impact for months. The 2022 capital crunch showed what happens when this delay prevents preventive action: Upstart held hundreds of millions in loans on its balance sheet."
approach: "Build an interactive lifecycle simulator that compresses 36 months of portfolio evolution into seconds. Generate synthetic borrowers, clear them through a three-layer engine with side-by-side model comparison, then compare performance across scenarios."
solution: "A browser-based sandbox with 7 tabs: PRFAQ, User Manual, Pipeline & Clearing, Marketplace Performance, Loan Deep Dive, Personas, and Re-Application. All client-side JS — no backend computation, no database, no API calls."
---

## What

A full lifecycle simulator for Upstart's capital marketplace — from borrower pipeline through clearing to 36 months of portfolio performance.

### Seven Tabs

**1. PRFAQ**
Amazon-style press release, customer FAQ, and internal FAQ framing the problem, the solution, and the v2 roadmap.

**2. User Manual**
Methodology behind the simulator (borrower generation, three-layer clearing, Markov chain lifecycle) plus step-by-step usage guide and disclaimers.

**3. Pipeline & Clearing**
Generate 1–100 synthetic borrowers, then run them through the clearing engine. Results show a 13-column side-by-side table: FICO, Model 18 Score, amount, purpose, hidden-prime flag, then APR/outcome/partner for both Model 18 and Classic. Filter by outcome (Cleared, APR Rejected, No Partner).

**4. Marketplace Performance**
Fixed 100-loan baseline (20 per partner) run through 36-month lifecycle under all three scenarios simultaneously. Compare Healthy Market vs Capital Crunch vs Rate Spike side-by-side with partner filtering and month scrubbing.

**5. Loan Deep Dive**
Click "Walk" on any borrower to see their 4-step journey: eligibility matrix (with failure reasons per partner) → pricing comparison → waterfall routing → funding & payment history strip.

**6. Personas**
Three borrower archetypes — Maria (hidden-prime), Carlos (ineligible/subprime), James (prime/balance sheet) — explaining the risk segments the simulator generates from.

**7. Re-Application**
Product roadmap stub framing how lifecycle data can predict re-applications and lower CAC for returning borrowers.

### Key Features

- **Side-by-side Model Comparison** — Every loan shows Model 18 and Classic outcomes in the same row
- **Scenario Presets** — Healthy Market, Capital Crunch (2022), Rate Spike — each adjusts FICO distribution and lifecycle parameters
- **Hidden-Prime Discovery** — Model 18 Score = FICO + 50 for hidden-prime borrowers, visible in every table
- **NO_PARTNER Explanations** — Deep Dive shows exactly why a borrower failed: FICO too low, capacity exhausted, APR mismatch

## Why

Upstart's capital marketplace is one of the most sophisticated clearing engines in fintech — but the feedback loops are invisible.

### The Problem

- **90-day feedback delay** — Changes to clearing rules take months to show in portfolio performance
- **2022 lesson** — The capital crunch happened partly because decision-makers couldn't see the compounding effect of tighter partner capacity in real-time
- **Black box clearing** — Few people understand how FICO pricing → Model 18 → partner routing → marketplace economics all connect

### What This Solves

- **Compress time** — 36 months of portfolio evolution, instant
- **Make tradeoffs tangible** — Clearing rate vs partner EPD vs balance sheet exposure, visible in one view
- **Three-stakeholder thinking** — Borrower experience, platform economics, and partner returns all in one tool
- **Model 18 intuition** — See exactly how APR-as-feature discovers hidden-prime borrowers and where the value is created

### Who It's For

PM candidates learning marketplace dynamics, marketplace operators stress-testing decisions, data scientists understanding the pipeline, anyone curious how lending marketplaces actually work.

## How

### Architecture

**Client-Side Only**
- Entirely browser-based JavaScript — no backend, no database, no network latency
- 100 borrowers × 5 partners × 36 months × 3 scenarios computed on page load
- FastAPI serves the HTML template; all computation happens in the browser

**Modules**
- `borrower_generation.js` — Synthetic borrower creation with FICO distributions, hidden-prime flags, seeded PRNG
- `clearing_engine.js` — Three-layer engine: eligibility → pricing → waterfall routing
- `lifecycle_engine.js` — 36-month Markov chain with grade-based transition probabilities
- `lifecycle_simulator.js` — Main coordinator: pipeline controls, side-by-side rendering, deep dive, marketplace performance

### User Flow

1. **Read PRFAQ** — Understand the problem and context
2. **Check User Manual** — Review methodology and step-by-step instructions
3. **Select Scenario** — Choose Healthy Market, Capital Crunch, or Rate Spike
4. **Generate Pipeline** — Create 1–100 synthetic borrowers
5. **Run Clearing** — Process through both models; review side-by-side results
6. **Deep Dive** — Click "Walk" on any borrower to trace their clearing journey
7. **Compare Scenarios** — Switch to Marketplace Performance to see baseline comparison

### Limitations

- **Illustrative, not production-grade** — Markov chain is directionally correct but not vintage-calibrated
- **Small scale** — 100-borrower demos show dynamics, not statistical significance
- **No persistence** — Page refresh resets everything; no backend storage
- **Obfuscated partners** — Names are fictional; structures inspired by public filings
- **Re-Application is a stub** — Product roadmap framing, not full simulation

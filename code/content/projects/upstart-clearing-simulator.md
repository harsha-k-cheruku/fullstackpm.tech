---
title: "Upstart Clearing Simulator"
description: "Interactive simulator of Upstart's marketplace clearing engine—borrower applications, capital partner matching, APR optimization, and waterfall routing with real numbers."
tech_stack: [FastAPI, Python, Pandas, Interactive Tables, HTMX, Tailwind CSS]
status: "live"
featured: true
display_order: 2
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/upstart-clearing-simulator"
problem: "Upstart's clearing mechanism is the core of their marketplace—how borrowers get matched to capital partners at optimal APRs. But it's a black box to most people. Understanding it requires reading 30-page SEC filings or reverse-engineering the logic from press releases."
approach: "Build an interactive step-by-step simulator that walks through the entire clearing process with real borrower profiles, capital partner constraints, APR optimization (Model 18), and waterfall routing decisions. Make the invisible visible."
solution: "An interactive tool with pre-loaded scenarios that show exactly how borrowers route through the system, how APR gets set, which capital partner wins each loan, and what the waterfall looks like. Includes companion methodology page with data sources and calculations."
---

## What

An interactive simulator that walks you through Upstart's marketplace clearing engine step-by-step. See how borrowers route to capital partners, how APRs are optimized, and how the waterfall works—with real data and actual constraints.

**Features:**
- **Borrower Pool** — Pre-loaded borrower profiles with credit scores, loan amounts, and risk grades (A–E)
- **Capital Partner Setup** — Available capital partners with funding capacity, APR bands, and risk preferences
- **Matching Engine** — Step through how each borrower gets matched based on constraints and optimization rules
- **APR Optimization** — See Model 18 in action: how Upstart sets APRs to maximize conversion while respecting partner constraints
- **Waterfall Routing** — Visualize how loans flow through the waterfall when the primary partner is full
- **Real Numbers** — Data-driven scenarios based on Upstart's actual filing disclosures and public statements
- **Methodology Companion** — Linked page explaining data sources, calculation logic, and assumptions

## Why

Upstart is one of the most technically sophisticated fintech companies—their marketplace clearing engine is a work of product engineering. But for PM candidates, founders, and investors, it's hard to understand how the pieces fit together.

This simulator solves that by:
- **Making the mechanism transparent** — Every step is visible and explainable
- **Building intuition at scale** — See how individual borrower-partner matches aggregate into business metrics
- **Demonstrating PM thinking** — The tradeoffs between borrower conversion, partner satisfaction, and company take-rate are all embedded in the design
- **Enabling learning through play** — You can adjust parameters and see outcomes change in real-time

It's designed for PM candidates preparing for Upstart interviews, fintech founders building marketplace engines, and anyone curious about how loan marketplaces actually work.

## How

**Architecture:**
- **Backend:** FastAPI routes serve the simulator interface and handle real-time matching/routing calculations
- **Data:** Deterministic borrower profiles and capital partner constraints based on Upstart's public filings
- **Frontend:** Interactive step-by-step flow with tables, status indicators, and real-time results
- **Styling:** Tailwind CSS with consistent design tokens (currently basic—will be refined to match site design language)

**The flow:**
1. Start with a borrower pool and capital partner setup
2. Step through the matching engine decision for each borrower
3. See APR optimization logic applied
4. Watch waterfall routing when capacity constraints kick in
5. Review final outcomes and key metrics
6. Access companion methodology page for deeper understanding

**Data sources:**
- Upstart S-1 (2021) — Revenue by capital partner, loan volume, take-rate evolution
- Quarterly earnings calls (2021–2026) — Capital partner names, market dynamics, platform changes
- Public blog posts & product releases — Feature announcements, algorithm improvements
- Fintech research reports — Market positioning, competitor comparisons

**Assumptions & Limitations:**
- Model simplified for clarity—real Upstart system is far more complex
- Capital partner data obfuscated (names changed, capacity adjusted for privacy)
- APR optimization model is an approximation of Model 18, not the actual proprietary formula
- Borrower profiles are synthetic, though credit score/loan amount distributions reflect market reality

---

**Companion page:** [Upstart Data & Methods](/tools/upstart-data-methods) — Full methodology, data sources, calculations, and limitations.

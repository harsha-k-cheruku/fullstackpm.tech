---
title: "Project Artha — SPY Options Simulation"
description: "Rules-based SPY options paper-trading pipeline that runs twice daily, recommends defined-risk setups, and maintains a structured learning journal. One contract, no real money."
tech_stack: [Python, yfinance, launchd, Black-Scholes, pandas]
status: "live"
featured: true
display_order: 3
github_url: ""
live_url: ""
problem: "❌ Learning SPY options by reading about them builds familiarity but not judgment. You need reps — but real money creates emotional noise that distorts learning."
approach: "💡 Simulate one contract daily. Rules-based recommender picks the setup. Human can override. Every decision and outcome is logged with a structured 4-step journal entry."
solution: "✅ Two automated runs daily (9 AM and 12:15 PM PT). Recommender handles IV rank, catalyst buffers, trend filters, and strike selection. Journal tracks system vs human decisions over time."
---

## What

Project Artha (Sanskrit for wealth and purpose) is a paper-trading simulation for SPY options. It runs twice per day via launchd, fetches live market data, recommends one defined-risk options setup (or no trade), and records the decision in a structured learning journal.

One contract. No real money. Goal: build options intuition through systematic simulation and deliberate journaling.

## The Recommender

A rules-based engine that gates every trade:

**Filters (in order):**
1. IV Rank < 25 → NO TRADE (options are cheap, not worth selling)
2. DTE outside 1–45 day window → NO TRADE
3. CPI / FOMC / NFP within 4 days → NO TRADE (catalyst buffer)
4. ATR elevated + SPY extended upward → Bear call spread
5. ATR elevated + SPY extended downward → Bull put spread
6. Default → Iron condor

**Strike selection — the critical rule:**
- DTE > 7: use 16-delta (standard)
- DTE ≤ 7: use **1.5× implied move** from the ATM straddle price

At short DTE, 16-delta places strikes *inside* the expected range. The ATM straddle price (call_mid + put_mid) is the market's honest assessment of the expected ±move. Multiplying by 1.5 places strikes safely outside it.

## The Journal

Each trade gets a 4-step entry:
1. **Evaluated setups** — all candidates considered with metrics
2. **Trade setup** — legs, credit, max loss, visual range bar
3. **Outcome** — filled after expiry (actual P&L)
4. **Lesson learned** — manual entry (what this confirmed or challenged)

**Human Override Tracker** — records when the system recommended a trade but the human passed, and vice versa. Over time this surfaces where human judgment adds vs destroys value.

## Technical Details

- CPI calendar uses hardcoded BLS release dates (formula-based calculation was unreliable — BLS doesn't always release on the 2nd Wednesday)
- Same-day morning releases (CPI at 8:30 AM ET) are treated as already-past by the 9 AM PT pipeline run — no blocking
- FOMC decisions (2 PM ET) still block on same-day runs since pipeline runs before them
- Pre-close run (12:15 PM PT) evaluates positions expiring today against 50% profit target, breakeven breach, or gamma risk proximity

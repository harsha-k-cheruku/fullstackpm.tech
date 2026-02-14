---
title: "Marketplace Analytics Dashboard"
description: "Interactive seller performance analytics with revenue trends, category analysis, and cohort insights."
tech_stack: [FastAPI, Python, Pandas, Chart.js, HTMX, SQLite]
status: "live"
featured: true
display_order: 3
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/marketplace-analytics"
problem: "Marketplace sellers have fragmented metrics across spreadsheets and dashboards. Revenue trends, category performance, and cohort health are hard to see quickly, making fast decision-making impossible."
approach: "Build an interactive dashboard with real-time filtering, trend analysis, and cohort segmentation. Use deterministic mock data for demo, structured to support real data integration. Focus on clarity over complexity."
solution: "A fast, responsive analytics dashboard with overview cards, revenue trends (Chart.js), category performance tables, cohort analysis, and CSV export—all filtered in real-time via HTMX without page reloads."
---

## What

An interactive analytics dashboard for marketplace sellers that surfaces performance metrics at a glance and enables data-driven decisions in seconds.

**Features:**
- **Overview Cards** — Total revenue (with % delta), active listings, average rating, customer satisfaction score
- **Revenue Trends** — 12-week line chart by week, category filtering, revenue per listing
- **Category Performance** — Sortable table showing category, listings, revenue, avg price, avg rating with top/bottom performer highlighting
- **Cohort Analysis** — Cohort retention and revenue by seller signup month to identify best-performing acquisition waves
- **Real-time Filtering** — Date range (30/90/365 days) and category dropdown with instant chart/table updates via HTMX
- **CSV Export** — Download filtered data for deeper analysis or reporting

## Why

Most marketplace sellers rely on fragmented data sources—spreadsheets, Looker dashboards, manual exports. **This creates decision lag.** Questions like "Which category should we invest in?" or "Are our new sellers as strong as last quarter?" require piecing together data from multiple places.

The analytics dashboard solves this by:
- **Centralizing key metrics** — One place to understand business health
- **Enabling fast iteration** — Filter, sort, and export in seconds, not hours
- **Supporting real decisions** — Revenue trends inform pricing, category performance drives seller support allocation, cohort analysis guides marketing spend

I built this to demonstrate how a Full Stack PM can prototype and ship data products without needing a dedicated analytics team.

## How

**Architecture:**
- **Backend:** FastAPI routes serve dashboard views and HTMX partials for filtering
- **Data:** Deterministic mock dataset (sellers, listings, sales) with aggregation logic in analytics.py
- **Frontend:** Jinja2 templates + HTMX for progressive enhancement + Chart.js for visualization
- **Styling:** Tailwind CSS + design system tokens for responsive dark mode support

**The data flow:**
1. Dashboard loads with 30-day default view
2. User selects date range or category
3. HTMX submits filter request to backend
4. Backend re-aggregates data and re-renders partials
5. Charts and tables update without page reload
6. User can export filtered data as CSV

**Why this approach works:**
- Mock data is deterministic, so charts always render correctly
- HTMX avoids JavaScript framework bloat—just progressive enhancement
- No database overhead (SQLite for production-ready schema if needed)
- Dashboard is fast enough for real-time exploration

## Technical Stack

- **Backend:** FastAPI (Python) — lightweight, async, auto-docs
- **Data Processing:** Pandas (Python) — aggregations, filtering, export
- **Frontend:** Jinja2 + HTMX — server-side rendering, real-time updates
- **Charting:** Chart.js — responsive, dark mode compatible, lightweight
- **Styling:** Tailwind CSS + custom design tokens
- **Deployment:** Render (auto-deploys from GitHub)

---

**Next steps:** Replace mock data with real seller/listing/sales data from your marketplace database.

# BUILD: Marketplace Analytics Dashboard

## Project Overview

Build an interactive analytics dashboard for marketplace sellers. The dashboard surfaces revenue trends, category performance, and cohort insights with clean filters, summary cards, and exportable data.

**Audience:** Marketplace sellers + product ops
**Outcome:** Faster decisions, clearer performance signals, less spreadsheet chaos
**Timeline:** ~5 phases (see below)

---

## Problem Statement & Goals

**Problem:** Sellers have fragmented metrics across exports and dashboards. Trends, cohort health, and category performance are hard to see quickly.

**Goals:**
- Centralize the core seller performance metrics
- Provide at-a-glance insights (cards + charts)
- Enable fast filtering and export
- Keep UI simple, fast, and consistent with the design system

---

## Feature Breakdown

### 1) Overview Cards
- Total Revenue (period + % delta)
- Active Listings
- Average Rating
- Customer Satisfaction (NPS-style score)

### 2) Revenue Trends
- Line chart by week (last 12 weeks)
- Optional category filter
- Show average revenue per listing

### 3) Category Performance
- Table with: category, listings, revenue, avg price, avg rating
- Sortable columns
- Highlight top/bottom performers

### 4) Cohort Analysis
- Cohorts by signup month
- Table for Month 1/2 revenue + retention
- Quick visibility into best cohorts

### 5) Filters + Export
- Date range (30/90/365)
- Category dropdown
- Export filtered data to CSV

---

## Technical Architecture

**Backend:** FastAPI routes + service layer for aggregation
**Frontend:** Jinja2 templates + Tailwind + HTMX partials
**Charts:** Chart.js (CDN)
**Data:** Mock dataset (structured, deterministic)

**Core files:**
```
code/app/
├── routers/
│   └── marketplace.py
├── services/
│   └── analytics.py
├── templates/
│   └── marketplace-analytics/
│       ├── index.html
│       └── partials/
│           ├── overview_cards.html
│           ├── revenue_chart.html
│           ├── category_table.html
│           └── filters.html
└── static/
    └── js/
        └── charts.js
```

---

## Step-by-Step Build Plan (5 Phases)

### Phase 1: Data + Wiring
- Add router + service skeleton
- Seed mock data schema
- Build template scaffold

### Phase 2: UI Shell
- Layout grid + overview cards
- Filters (date range + category)
- Consistent spacing + typography

### Phase 3: Charts + Table
- Revenue trend chart
- Category table with sorting
- HTMX filter hooks

### Phase 4: Cohorts + Export
- Cohort table
- CSV export
- Loading states

### Phase 5: Polish
- Dark mode + responsive QA
- Empty states + error handling
- Performance cleanup

---

## Acceptance Criteria

### MVP (Must Have)
- Dashboard loads at `/tools/marketplace-analytics`
- Overview cards show revenue, listings, rating, satisfaction
- Revenue trend chart renders (last 12 weeks)
- Category table renders and sorts
- Filters update cards, charts, and table
- Responsive + dark mode ready
- No console errors

### Nice-to-Haves
- CSV export works
- Cohort analysis table present
- Interactive chart tooltips
- Fast load (<1s)

---

## Design System Guidelines

Use existing tokens + typography:
- Colors via CSS variables (`--color-bg-secondary`, `--color-text-primary`, `--color-accent`)
- Typography: `text-h2`, `text-body`, `text-small`
- Cards: `rounded-xl`, `border-color: var(--color-border)`
- Tables: consistent border + zebra rows

---

## Mock Data Structure

Use a small deterministic dataset:
- `sellers`: id, name, signup_month
- `listings`: id, seller_id, category, price, rating, created_at
- `sales`: id, listing_id, amount, timestamp

Derived metrics:
- Weekly revenue trends
- Category rollups
- Cohort retention + revenue

---

## Deployment Notes

- No schema migrations required for MVP
- Chart.js via CDN
- Add route in `main.py`
- Deploy to Render (FastAPI)

---

## Next Project

**Interactive analytics dashboard for marketplace sellers:**
- Revenue trends, category performance, cohort analysis
- Charts with Chart.js, tables, filtering, export

---

**Ready to build when you are.**

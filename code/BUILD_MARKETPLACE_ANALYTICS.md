# BUILD: Marketplace Analytics Dashboard

## Overview

Build an interactive analytics dashboard for marketplace sellers to view performance metrics, trends, and insights. This is a Full Stack PM project that demonstrates data visualization, real-time updates, and product decision-making.

**Scope:** ~3-5 days of development
**Team:** 1 engineer (you) + PM vision (me)
**Complexity:** Medium

---

## The Problem

Marketplace sellers have data, but it's scattered:
- Revenue trends hidden in spreadsheets
- Category performance unclear
- Cohort analysis requires manual work
- No quick way to spot problems or opportunities

This tool solves that by giving sellers a single dashboard to understand their business.

---

## What to Build

### Page: `/tools/marketplace-analytics`

**Landing/Dashboard View:**
- Overview cards (top metrics)
- Charts for key trends
- Filters by date range and category
- Export functionality

### Features

#### 1. Overview Section
Cards showing:
- **Total Revenue** (current month vs last month % change)
- **Active Listings** (count with trend)
- **Average Rating** (1-5 stars)
- **Customer Satisfaction** (NPS score)

#### 2. Revenue Trends
- Line chart: Revenue by week (last 12 weeks)
- Breakdown by: All Categories OR filter to 1 category
- Show average revenue per listing

#### 3. Category Performance
- Table showing:
  - Category name
  - # of listings
  - Total revenue
  - Avg price per item
  - Avg rating
- Sortable by any column
- Highlight top/bottom performers

#### 4. Cohort Analysis (Optional but nice)
- Cohorts by: Sign-up month
- Table: Cohort | Month 1 Revenue | Month 2 Revenue | Retention
- Identifies best-performing seller cohorts

#### 5. Filters & Export
- Date range picker (last 30/90/365 days)
- Category filter (dropdown)
- Export to CSV button

---

## Technical Stack

**Frontend:**
- Tailwind CSS for styling
- HTMX for interactive filtering
- Chart.js or Plotly for visualizations (lightweight)
- No React/Vue

**Backend:**
- FastAPI (existing)
- Pandas for data aggregation
- SQLite (existing)

**Data:**
- Use mock/sample data for MVP
- OR if you want real data: generate synthetic seller data in a script

---

## Architecture

### New Files to Create

```
code/app/
├── routers/
│   └── marketplace.py          # Routes for dashboard
├── services/
│   └── analytics.py            # Data aggregation logic
├── templates/
│   └── marketplace-analytics/
│       ├── index.html          # Dashboard page
│       └── partials/
│           ├── overview_cards.html
│           ├── revenue_chart.html
│           ├── category_table.html
│           └── filters.html
└── static/
    └── js/
        └── charts.js           # Chart initialization
```

### Sample Data Structure

Create sample data for 10-20 sellers with:
- Listings (id, seller_id, category, price, rating, created_at)
- Sales (id, listing_id, amount, timestamp)
- Categories (id, name)

**OR** Use the existing portfolio database and create a simple analytics schema.

---

## Step-by-Step Build Plan

### Phase 1: Setup & Data (Day 1)
1. Create `marketplace.py` router
2. Create `analytics.py` service for data aggregation
3. Generate mock data (or use script to create sample data)
4. Create base template structure

### Phase 2: Dashboard UI (Day 2)
1. Build `/tools/marketplace-analytics` landing page
2. Create overview cards layout
3. Add filter controls (date range, category dropdown)
4. Style everything with Tailwind

### Phase 3: Data & Charts (Day 3)
1. Implement revenue trends chart
2. Build category performance table
3. Wire up filters with HTMX
4. Test filtering and data updates

### Phase 4: Polish (Day 4)
1. Add export to CSV functionality
2. Responsive mobile design
3. Dark mode compatibility
4. Performance optimization (cache data if needed)

### Phase 5: Optional Enhancements (Day 5)
1. Add cohort analysis table
2. Add seller comparison feature
3. Add anomaly detection (highlight unusual trends)
4. Add tooltips/help text

---

## Acceptance Criteria

### MVP (Must Have)
- ✅ Dashboard loads at `/tools/marketplace-analytics`
- ✅ Overview cards show: revenue, listings, rating, satisfaction
- ✅ Revenue trend chart displays (last 12 weeks)
- ✅ Category performance table displays all data
- ✅ Date range filter works (affects all charts/tables)
- ✅ Category filter works (affects all data)
- ✅ Mobile responsive (works on phone/tablet/desktop)
- ✅ Dark mode compatible
- ✅ No console errors

### Nice to Have
- ✅ CSV export button works
- ✅ Cohort analysis table present
- ✅ Charts are interactive (hover tooltips)
- ✅ Fast page load (<1s)

### Testing
1. Test filters (date + category combinations)
2. Test mobile layout on actual phone
3. Test dark mode toggle
4. Verify CSV export data matches dashboard

---

## Design System

Use existing design:
- **Colors:** Use `--color-text-primary`, `--color-bg-secondary`, `--color-accent`
- **Typography:** Use `text-h2`, `text-body`, `text-small` classes
- **Cards:** Use rounded borders with `border-color: var(--color-border)`
- **Tables:** Follow existing table styling from projects/comments sections

---

## Questions for You

Before starting, clarify:
1. Should we use mock data or connect to a real data source?
2. Which chart library do you prefer? (Chart.js is lightweight)
3. Do you want real seller data or synthetic data?
4. Should this be real-time or snapshot-based?
5. Any specific metrics you want highlighted?

---

## Deployment

- No new dependencies needed (Pandas is fast, Chart.js is CDN)
- Add new route to main.py
- No database migrations needed
- Push to GitHub → auto-deploy on Render

---

## Success Metrics

When complete:
- Dashboard is useful and fast
- Demonstrates data visualization skills
- Shows PM ability to spot insights
- Easy to extend with more metrics later

---

**Ready to build? Let me know if you have questions!**

# Project 2: Marketplace Analytics Dashboard

## Product Brief

### Problem
Every PM claims to be "data-driven," but few can build the tooling to prove it. At Amazon and Walmart, marketplace health depends on understanding seller performance, customer behavior, and revenue dynamics simultaneously. This project demonstrates that you can not only define the right metrics but build a dashboard to track them.

### Solution
An interactive analytics dashboard built on synthetic 3P marketplace data (modeled on Amazon/Walmart patterns). Features seller health scoring, customer segmentation (RFM), cohort analysis, CLV predictions, conversion funnels, and customer journey visualization. Filterable by time range, category, and seller tier.

### Target Audience
- Interviewers evaluating your analytical and domain expertise
- PMs who want a reference implementation for marketplace analytics
- You, as a demonstration of data + product skills

### Non-Goals
- Not connected to real marketplace data (synthetic only)
- Not a production-grade BI tool
- No real-time streaming data
- No user authentication

---

## Features

### MVP

| Feature | Description |
|---------|-------------|
| **Synthetic Data Generator** | Python script generating realistic marketplace data: sellers, products, transactions, reviews, customers with realistic distributions |
| **Seller Health Scores** | Composite score from: order defect rate, late shipment rate, review sentiment, cancellation rate. Color-coded tiers (Healthy/At Risk/Critical) |
| **Cohort Analysis** | Monthly seller and customer cohorts with retention curves |
| **RFM Segmentation** | Customers segmented by Recency, Frequency, Monetary value into segments: Champions, Loyal, At Risk, Lost, etc. |
| **CLV Predictions** | Simple CLV model per customer segment using historical purchase patterns |
| **Revenue Dashboard** | GMV trends, category performance, seller tier contribution, conversion rates |
| **Conversion Funnel** | View → Add to Cart → Checkout → Purchase funnel with drop-off rates |
| **Customer Journey** | Visualization of typical customer paths from first visit to repeat purchase |
| **Churn Analysis** | Customer and seller churn rates by cohort with early warning indicators |
| **Filters** | Global filters: date range, product category, seller tier |

### v2
- Anomaly detection (flag unusual metric movements)
- What-if simulator (adjust pricing/promotions, see projected impact)
- Automated insight generation via AI ("Seller churn in Electronics is 2x the average...")

---

## Technical Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | HTMX + Tailwind CSS |
| Charts | Chart.js (line, bar, doughnut, funnel) + Plotly (heatmaps, sankey) |
| Data Processing | Pandas + NumPy |
| ML | Scikit-learn (K-means for RFM, simple regression for CLV) |
| Database | SQLite |

### Data Model

```sql
sellers (
  id INTEGER PK,
  name TEXT,
  tier TEXT,                -- "gold", "silver", "bronze", "new"
  category TEXT,            -- primary category
  join_date DATE,
  status TEXT,              -- "active", "suspended", "churned"
  region TEXT
)

products (
  id INTEGER PK,
  seller_id INTEGER FK,
  name TEXT,
  category TEXT,
  subcategory TEXT,
  price REAL,
  cost REAL,
  listed_date DATE,
  status TEXT               -- "active", "out_of_stock", "delisted"
)

customers (
  id INTEGER PK,
  first_purchase_date DATE,
  segment TEXT,             -- RFM segment label
  lifetime_value REAL,
  region TEXT
)

transactions (
  id INTEGER PK,
  customer_id INTEGER FK,
  seller_id INTEGER FK,
  product_id INTEGER FK,
  order_date DATE,
  quantity INTEGER,
  revenue REAL,
  status TEXT,              -- "completed", "returned", "cancelled"
  delivery_days INTEGER,
  was_late BOOLEAN
)

reviews (
  id INTEGER PK,
  transaction_id INTEGER FK,
  seller_id INTEGER FK,
  product_id INTEGER FK,
  rating INTEGER,           -- 1-5
  sentiment REAL,           -- -1.0 to 1.0
  review_date DATE
)

page_events (
  id INTEGER PK,
  customer_id INTEGER FK,
  product_id INTEGER FK,
  event_type TEXT,          -- "view", "add_to_cart", "checkout_start", "purchase"
  event_date DATETIME
)
```

**Synthetic data targets:** ~500 sellers, ~5,000 products, ~50,000 customers, ~200,000 transactions, ~80,000 reviews, ~500,000 page events over 12 months.

### API Endpoints

**Pages:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Dashboard home (revenue overview + key metrics) |
| GET | `/sellers` | Seller health scorecard |
| GET | `/customers` | Customer segmentation + CLV |
| GET | `/cohorts` | Cohort analysis (seller + customer) |
| GET | `/funnel` | Conversion funnel + journey |

**API (HTMX partials + JSON for charts):**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/revenue/summary` | Revenue metrics for date range |
| GET | `/api/revenue/trend` | GMV trend data (line chart) |
| GET | `/api/revenue/by-category` | Revenue by category (bar chart) |
| GET | `/api/sellers/health` | Seller health scores with tier breakdown |
| GET | `/api/sellers/cohort` | Seller cohort retention data |
| GET | `/api/customers/segments` | RFM segment distribution |
| GET | `/api/customers/clv` | CLV by segment |
| GET | `/api/customers/cohort` | Customer cohort retention curves |
| GET | `/api/funnel/conversion` | Funnel conversion rates |
| GET | `/api/funnel/journey` | Customer journey sankey data |
| GET | `/api/churn/customers` | Customer churn rates by cohort |
| GET | `/api/churn/sellers` | Seller churn rates by tier |

All API endpoints accept query params: `date_from`, `date_to`, `category`, `seller_tier`.

### Application Structure

```
marketplace-dashboard/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── routers/ (pages.py, revenue.py, sellers.py, customers.py, funnel.py)
│   ├── services/
│   │   ├── analytics.py      # Core query engine (Pandas + SQL)
│   │   ├── rfm.py             # RFM segmentation logic
│   │   ├── clv.py             # CLV prediction model
│   │   ├── health_score.py    # Seller health scoring
│   │   └── cohort.py          # Cohort analysis engine
│   ├── templates/ (base, dashboard, sellers, customers, cohorts, funnel + partials/)
│   └── static/
├── scripts/
│   ├── generate_data.py       # Synthetic data generator
│   └── seed_db.py             # Load generated data into SQLite
├── tests/
├── requirements.txt
└── README.md
```

---

## UI/UX

### Dashboard Home (`/`)
- **Top bar:** Global filters (date range picker, category dropdown, seller tier dropdown)
- **KPI cards row:** Total GMV, Active Sellers, Active Customers, Avg Order Value, Conversion Rate — each with trend arrow vs. prior period
- **Revenue trend:** Line chart (daily/weekly/monthly toggle)
- **Category performance:** Horizontal bar chart
- **Quick links:** Cards to Sellers, Customers, Cohorts, Funnel sections

### Seller Health (`/sellers`)
- Health score distribution (doughnut: Healthy/At Risk/Critical)
- Sortable table: Seller, Tier, Health Score, Order Defect Rate, Late Ship %, Avg Rating, Revenue
- Click seller → detail view with metric trends
- Seller churn rate by tier (bar chart)

### Customer Segmentation (`/customers`)
- RFM segment treemap or bubble chart
- Segment table: Segment Name, Customer Count, Avg CLV, Avg Order Frequency, Avg Recency
- CLV distribution by segment (box plot or violin chart)
- Customer churn by segment (line chart)

### Cohort Analysis (`/cohorts`)
- Toggle: Customer Cohorts / Seller Cohorts
- Heatmap: rows = cohort month, columns = months since join, cells = retention %
- Retention curves: line chart with one line per cohort

### Conversion Funnel (`/funnel`)
- Funnel visualization: View → Cart → Checkout → Purchase with drop-off percentages
- Customer journey sankey diagram: paths from entry to purchase/exit
- Funnel by category comparison

**All charts update via HTMX** when global filters change — no full page reload.

---

## Development Phases

### Phase 1: Data Foundation (Days 1-3)
- [ ] Design and build synthetic data generator with realistic distributions
- [ ] Create SQLite schema and seed script
- [ ] Generate 12 months of synthetic data
- [ ] Validate data quality (distributions, relationships, edge cases)

### Phase 2: Revenue & Seller Dashboards (Days 4-7)
- [ ] Project scaffold (FastAPI, templates, Tailwind, HTMX)
- [ ] Dashboard home with KPI cards and revenue charts
- [ ] Global filter bar with HTMX-powered chart updates
- [ ] Seller health scoring engine
- [ ] Seller health page with scorecard and table

### Phase 3: Customer Analytics (Days 8-11)
- [ ] RFM segmentation engine (Pandas + Scikit-learn K-means)
- [ ] CLV prediction model
- [ ] Customer segmentation page with visualizations
- [ ] Cohort analysis engine and heatmap page
- [ ] Churn analysis for both customers and sellers

### Phase 4: Funnel & Polish (Days 12-15)
- [ ] Conversion funnel calculation from page_events
- [ ] Funnel visualization page
- [ ] Customer journey sankey diagram
- [ ] Responsive design pass
- [ ] Tests and deploy
- [ ] Add to portfolio site

---

## Next Step

Build `scripts/generate_data.py` first. The quality of the dashboard depends entirely on having realistic synthetic data with proper distributions, seasonality, and correlations between entities. Model the data on real marketplace patterns: power-law seller distribution, seasonal purchase spikes, correlated review sentiment and churn.

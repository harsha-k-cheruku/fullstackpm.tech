"""Marketplace analytics service.

Generates deterministic mock data and aggregates metrics for the dashboard.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple
import random


CATEGORIES = [
    "Home",
    "Electronics",
    "Fashion",
    "Beauty",
    "Sports",
]


@dataclass(frozen=True)
class Seller:
    id: int
    name: str
    signup_date: date


@dataclass(frozen=True)
class Listing:
    id: int
    seller_id: int
    category: str
    price: float
    rating: float
    created_at: date


@dataclass(frozen=True)
class Sale:
    id: int
    listing_id: int
    amount: float
    timestamp: date


@dataclass(frozen=True)
class OverviewMetrics:
    total_revenue: float
    revenue_delta_pct: Optional[float]
    active_listings: int
    average_rating: float
    satisfaction_score: int


@dataclass(frozen=True)
class TrendPoint:
    label: str
    revenue: float


@dataclass(frozen=True)
class CategoryPerformance:
    category: str
    listings: int
    revenue: float
    avg_price: float
    avg_rating: float


@dataclass(frozen=True)
class CohortRow:
    cohort: str
    month1_revenue: float
    month2_revenue: float
    retention_pct: float


@dataclass(frozen=True)
class AnalyticsSnapshot:
    overview: OverviewMetrics
    trends: List[TrendPoint]
    categories: List[CategoryPerformance]
    cohorts: List[CohortRow]
    available_categories: List[str]


_DATA_CACHE: Dict[str, List] = {}


def get_snapshot(
    *,
    date_range_days: int,
    category: Optional[str],
    sort_by: str,
    sort_dir: str,
) -> AnalyticsSnapshot:
    sellers, listings, sales = _load_mock_data()
    filtered_listings = _filter_listings(listings, category)
    listing_ids = {listing.id for listing in filtered_listings}
    start_date, end_date = _resolve_range(date_range_days)

    filtered_sales = [
        sale
        for sale in sales
        if sale.listing_id in listing_ids
        and start_date <= sale.timestamp <= end_date
    ]

    overview = _build_overview(
        sales=filtered_sales,
        listings=filtered_listings,
        date_range_days=date_range_days,
        start_date=start_date,
        end_date=end_date,
        all_sales=sales,
        category_listing_ids=listing_ids,
    )
    trends = _build_trends(filtered_sales, end_date=end_date)
    categories = _build_category_table(
        listings=filtered_listings,
        sales=filtered_sales,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    cohorts = _build_cohorts(
        sellers=sellers,
        listings=filtered_listings,
        sales=filtered_sales,
    )

    available_categories = sorted({listing.category for listing in listings})
    return AnalyticsSnapshot(
        overview=overview,
        trends=trends,
        categories=categories,
        cohorts=cohorts,
        available_categories=available_categories,
    )


def _load_mock_data() -> Tuple[List[Seller], List[Listing], List[Sale]]:
    if _DATA_CACHE:
        return (
            _DATA_CACHE["sellers"],
            _DATA_CACHE["listings"],
            _DATA_CACHE["sales"],
        )

    rng = random.Random(42)
    today = date.today()

    sellers: List[Seller] = []
    listings: List[Listing] = []
    sales: List[Sale] = []

    for seller_id in range(1, 13):
        signup_date = today - timedelta(days=30 * (seller_id % 8 + 1))
        sellers.append(
            Seller(
                id=seller_id,
                name=f"Seller {seller_id:02d}",
                signup_date=signup_date,
            )
        )

    listing_id = 1
    sale_id = 1
    for seller in sellers:
        listing_count = rng.randint(3, 6)
        for _ in range(listing_count):
            category = rng.choice(CATEGORIES)
            price = round(rng.uniform(15, 250), 2)
            rating = round(rng.uniform(3.4, 4.9), 2)
            created_at = seller.signup_date + timedelta(days=rng.randint(0, 60))
            listings.append(
                Listing(
                    id=listing_id,
                    seller_id=seller.id,
                    category=category,
                    price=price,
                    rating=rating,
                    created_at=created_at,
                )
            )

            for _ in range(rng.randint(8, 16)):
                days_ago = rng.randint(0, 320)
                timestamp = today - timedelta(days=days_ago)
                amount = round(price * rng.uniform(0.8, 1.4), 2)
                sales.append(
                    Sale(
                        id=sale_id,
                        listing_id=listing_id,
                        amount=amount,
                        timestamp=timestamp,
                    )
                )
                sale_id += 1
            listing_id += 1

    _DATA_CACHE["sellers"] = sellers
    _DATA_CACHE["listings"] = listings
    _DATA_CACHE["sales"] = sales
    return sellers, listings, sales


def _filter_listings(listings: Iterable[Listing], category: Optional[str]) -> List[Listing]:
    if not category or category.lower() == "all":
        return list(listings)
    return [listing for listing in listings if listing.category == category]


def _resolve_range(date_range_days: int) -> tuple[date, date]:
    end_date = date.today()
    start_date = end_date - timedelta(days=date_range_days)
    return start_date, end_date


def _build_overview(
    *,
    sales: list[Sale],
    listings: list[Listing],
    date_range_days: int,
    start_date: date,
    end_date: date,
    all_sales: list[Sale],
    category_listing_ids: set[int],
) -> OverviewMetrics:
    total_revenue = sum(sale.amount for sale in sales)
    active_listings = len(listings)
    avg_rating = (
        sum(listing.rating for listing in listings) / active_listings
        if active_listings
        else 0.0
    )
    satisfaction = int(round(avg_rating * 20))

    previous_start = start_date - timedelta(days=date_range_days)
    previous_end = start_date
    previous_sales = [
        sale
        for sale in all_sales
        if sale.listing_id in category_listing_ids
        and previous_start <= sale.timestamp < previous_end
    ]
    previous_revenue = sum(sale.amount for sale in previous_sales)
    delta_pct = None
    if previous_revenue > 0:
        delta_pct = ((total_revenue - previous_revenue) / previous_revenue) * 100

    return OverviewMetrics(
        total_revenue=total_revenue,
        revenue_delta_pct=delta_pct,
        active_listings=active_listings,
        average_rating=avg_rating,
        satisfaction_score=satisfaction,
    )


def _build_trends(sales: list[Sale], *, end_date: date) -> list[TrendPoint]:
    buckets = [0.0 for _ in range(12)]
    for sale in sales:
        days_diff = (end_date - sale.timestamp).days
        if 0 <= days_diff < 84:
            bucket_index = 11 - (days_diff // 7)
            buckets[bucket_index] += sale.amount

    trend_points: list[TrendPoint] = []
    for index in range(12):
        week_start = end_date - timedelta(days=(11 - index) * 7 + 6)
        label = week_start.strftime("%b %d")
        trend_points.append(TrendPoint(label=label, revenue=round(buckets[index], 2)))
    return trend_points


def _build_category_table(
    *,
    listings: list[Listing],
    sales: list[Sale],
    sort_by: str,
    sort_dir: str,
) -> list[CategoryPerformance]:
    category_map: dict[str, list[Listing]] = {}
    for listing in listings:
        category_map.setdefault(listing.category, []).append(listing)

    sales_by_listing: dict[int, float] = {}
    for sale in sales:
        sales_by_listing[sale.listing_id] = sales_by_listing.get(sale.listing_id, 0.0) + sale.amount

    rows: list[CategoryPerformance] = []
    for category, items in category_map.items():
        listing_count = len(items)
        revenue = sum(sales_by_listing.get(item.id, 0.0) for item in items)
        avg_price = sum(item.price for item in items) / listing_count if listing_count else 0.0
        avg_rating = sum(item.rating for item in items) / listing_count if listing_count else 0.0
        rows.append(
            CategoryPerformance(
                category=category,
                listings=listing_count,
                revenue=revenue,
                avg_price=avg_price,
                avg_rating=avg_rating,
            )
        )

    sort_key = {
        "category": lambda row: row.category,
        "listings": lambda row: row.listings,
        "revenue": lambda row: row.revenue,
        "price": lambda row: row.avg_price,
        "rating": lambda row: row.avg_rating,
    }.get(sort_by, lambda row: row.revenue)

    reverse = sort_dir == "desc"
    rows.sort(key=sort_key, reverse=reverse)
    return rows


def _build_cohorts(
    *,
    sellers: list[Seller],
    listings: list[Listing],
    sales: list[Sale],
) -> list[CohortRow]:
    listing_to_seller = {listing.id: listing.seller_id for listing in listings}
    seller_map = {seller.id: seller for seller in sellers}
    cohorts: dict[str, list[int]] = {}
    for seller in sellers:
        cohort_key = seller.signup_date.strftime("%b %Y")
        cohorts.setdefault(cohort_key, []).append(seller.id)

    rows: list[CohortRow] = []
    for cohort_key, seller_ids in cohorts.items():
        month1_total = 0.0
        month2_total = 0.0
        for sale in sales:
            seller_id = listing_to_seller.get(sale.listing_id)
            if seller_id not in seller_ids:
                continue
            signup = seller_map[seller_id].signup_date
            day_delta = (sale.timestamp - signup).days
            if 0 <= day_delta < 30:
                month1_total += sale.amount
            elif 30 <= day_delta < 60:
                month2_total += sale.amount

        retention = (month2_total / month1_total * 100) if month1_total else 0.0
        rows.append(
            CohortRow(
                cohort=cohort_key,
                month1_revenue=month1_total,
                month2_revenue=month2_total,
                retention_pct=retention,
            )
        )

    rows.sort(key=lambda row: datetime.strptime(row.cohort, "%b %Y"), reverse=True)
    return rows

"""Netra — Company Intelligence Reports served at /netra/{ticker}."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

NETRA_DIR = settings.static_dir / "data" / "netra"

COMPANY_NAMES = {
    "NVDA": "NVIDIA",
    "AMZN": "Amazon",
    "MSFT": "Microsoft",
    "META": "Meta",
    "GOOGL": "Alphabet",
    "AAPL": "Apple",
    "AVGO": "Broadcom",
    "TSLA": "Tesla",
    "JPM": "JPMorgan",
    "BRK-B": "Berkshire Hathaway",
}


def _report_files(ticker: str) -> list[Path]:
    """Sorted list of report HTML files for a ticker (newest last)."""
    d = NETRA_DIR / ticker
    if not d.exists():
        return []
    return sorted(
        [f for f in d.glob(f"{ticker}-*.html")],
        key=lambda p: p.stem.split("-", 1)[-1],
    )


def _ticker_index() -> list[dict]:
    """All tickers that have at least one report, with latest date."""
    result = []
    for ticker_dir in sorted(NETRA_DIR.iterdir()):
        if not ticker_dir.is_dir():
            continue
        files = _report_files(ticker_dir.name)
        if not files:
            continue
        latest = files[-1]
        date_str = latest.stem[len(ticker_dir.name) + 1:]  # strip "TICKER-"
        result.append({
            "ticker": ticker_dir.name,
            "name": COMPANY_NAMES.get(ticker_dir.name, ticker_dir.name),
            "latest_date": date_str,
            "report_count": len(files),
        })
    return result


@router.get("/netra", response_class=HTMLResponse)
async def netra_index(request: Request):
    tickers = _ticker_index()
    return templates.TemplateResponse("netra_index.html", {
        "request": request,
        "title": "Netra — Company Intelligence",
        "tickers": tickers,
    })


@router.get("/netra/{ticker}", response_class=HTMLResponse)
async def netra_ticker(ticker: str, date: Optional[str] = None):
    """Serve the latest (or specified date) report for a ticker."""
    ticker = ticker.upper()
    files = _report_files(ticker)
    if not files:
        raise HTTPException(status_code=404, detail=f"No reports found for {ticker}")

    if date:
        target = NETRA_DIR / ticker / f"{ticker}-{date}.html"
        if not target.exists():
            raise HTTPException(status_code=404, detail=f"No report for {ticker} on {date}")
        return HTMLResponse(content=target.read_text())

    return HTMLResponse(content=files[-1].read_text())

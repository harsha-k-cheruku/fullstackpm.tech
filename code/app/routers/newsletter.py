# app/routers/newsletter.py
"""Newsletter subscription API routes using Google Sheets."""
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, StreamingResponse

from app.config import settings
from app.services.google_sheets_service import GoogleSheetsSubscriberService

router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])

# Initialize subscriber service
try:
    subscriber_service = GoogleSheetsSubscriberService(
        credentials_json=settings.google_sheets_credentials_path,
        spreadsheet_id=settings.google_sheets_id,
    )
except Exception as e:
    print(f"Warning: Could not initialize Google Sheets service: {e}")
    subscriber_service = None


@router.post("/subscribe", response_class=HTMLResponse)
async def subscribe(
    email: str = Form(...),
    name: str = Form(None),
    source: str = Form("footer"),
):
    """Subscribe an email to the newsletter. Returns HTMX HTML snippet."""
    if not subscriber_service:
        return HTMLResponse(
            '<p class="text-sm font-medium" style="color: var(--color-error, #ef4444);">Service unavailable. Please try again later.</p>'
        )

    result = subscriber_service.subscribe(email, name, source)
    color = "var(--color-accent)" if result["success"] else "var(--color-error, #ef4444)"
    return HTMLResponse(
        f'<p class="text-sm font-medium" style="color: {color};">{result["message"]}</p>'
    )


@router.get("/export")
async def export_subscribers():
    """Export subscribers as CSV."""
    if not subscriber_service:
        return StreamingResponse(
            iter(["error"]),
            media_type="text/csv",
        )

    csv_data = subscriber_service.export_csv()
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=subscribers.csv"},
    )

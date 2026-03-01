# app/routers/newsletter.py
"""Newsletter subscription API routes."""
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, StreamingResponse

from app.config import settings
from app.services.subscriber_service import SubscriberService

router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])

# Initialize subscriber service
subscriber_service = SubscriberService(settings.static_dir / "data")


@router.post("/subscribe", response_class=HTMLResponse)
async def subscribe(
    email: str = Form(...),
    name: str = Form(None),
    source: str = Form("footer"),
):
    """Subscribe an email to the newsletter. Returns HTMX HTML snippet."""
    result = subscriber_service.subscribe(email, name, source)

    color = "var(--color-accent)" if result["success"] else "var(--color-error, #ef4444)"
    return HTMLResponse(
        f'<p class="text-sm font-medium" style="color: {color};">{result["message"]}</p>'
    )


@router.get("/export")
async def export_subscribers():
    """Export active subscribers as CSV."""
    csv_data = subscriber_service.export_csv()
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=subscribers.csv"},
    )

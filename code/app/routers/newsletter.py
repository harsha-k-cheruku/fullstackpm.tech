# app/routers/newsletter.py
"""Newsletter subscription API routes."""
import csv
import io

from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subscriber import Subscriber

router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])


@router.post("/subscribe", response_class=HTMLResponse)
async def subscribe(
    email: str = Form(...),
    name: str = Form(None),
    source: str = Form("footer"),
    db: Session = Depends(get_db),
):
    """Subscribe an email to the newsletter. Returns HTMX HTML snippet."""
    email = email.strip().lower()

    # Basic validation
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        return HTMLResponse(
            '<p class="text-sm font-medium" style="color: var(--color-error, #ef4444);">'
            "Please enter a valid email address.</p>",
            status_code=200,
        )

    # Check for existing subscriber
    existing = db.query(Subscriber).filter(Subscriber.email == email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.commit()
            return HTMLResponse(
                '<p class="text-sm font-medium" style="color: var(--color-accent);">'
                "Welcome back! You've been re-subscribed.</p>"
            )
        return HTMLResponse(
            '<p class="text-sm font-medium" style="color: var(--color-accent);">'
            "You're already on the list! We'll keep you posted.</p>"
        )

    # Create new subscriber
    subscriber = Subscriber(
        email=email,
        name=name.strip() if name else None,
        source=source,
    )
    db.add(subscriber)
    db.commit()

    return HTMLResponse(
        '<p class="text-sm font-medium" style="color: var(--color-accent);">'
        "You're in! Thanks for subscribing.</p>"
    )


@router.get("/export")
async def export_subscribers(db: Session = Depends(get_db)):
    """Export active subscribers as CSV."""
    subscribers = (
        db.query(Subscriber)
        .filter(Subscriber.is_active == True)
        .order_by(Subscriber.subscribed_at.desc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["email", "name", "source", "subscribed_at"])
    for sub in subscribers:
        writer.writerow([
            sub.email,
            sub.name or "",
            sub.source,
            sub.subscribed_at.isoformat() if sub.subscribed_at else "",
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=subscribers.csv"},
    )

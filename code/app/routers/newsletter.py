# app/routers/newsletter.py
"""Newsletter subscription API routes using Google Sheets."""
import logging
import urllib.error
import urllib.request
import urllib.parse
from urllib.parse import quote

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Form, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.google_sheets_service import GoogleSheetsSubscriberService

router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])
templates = Jinja2Templates(directory=str(settings.templates_dir))

# Initialize subscriber service
try:
    subscriber_service = GoogleSheetsSubscriberService(
        credentials_json=settings.google_sheets_credentials_path,
        spreadsheet_id=settings.google_sheets_id,
    )
    print(f"✅ Newsletter service initialized successfully")
except FileNotFoundError as e:
    print(f"❌ Credentials file not found: {settings.google_sheets_credentials_path}")
    print(f"   Error: {e}")
    subscriber_service = None
except ImportError as e:
    print(f"❌ Google Sheets library not installed: {e}")
    subscriber_service = None
except Exception as e:
    print(f"❌ Could not initialize Google Sheets service")
    print(f"   Credentials path: {settings.google_sheets_credentials_path}")
    print(f"   Spreadsheet ID: {settings.google_sheets_id}")
    print(f"   Error type: {type(e).__name__}")
    print(f"   Error message: {e}")
    import traceback
    traceback.print_exc()
    subscriber_service = None


def _success_html(message: str, email: str = "") -> str:
    """Styled success snippet for HTMX swap."""
    unsubscribe_link = ""
    if email:
        encoded_email = quote(email, safe="")  # URL-encode email address
        unsubscribe_link = f"""
        <p class="text-xs mt-2" style="color: var(--color-text-tertiary, #9ca3af);">
          Changed your mind? <a href="/api/newsletter/unsubscribe?email={encoded_email}"
            style="color: var(--color-accent); text-decoration: underline;">Unsubscribe</a>
        </p>"""
    return f"""
    <div class="text-center py-4">
      <p class="text-sm font-semibold" style="color: var(--color-accent);">{message}</p>
      {unsubscribe_link}
    </div>"""


def _error_html(message: str) -> str:
    """Styled error snippet for HTMX swap."""
    return f"""
    <div class="text-center py-4">
      <p class="text-sm font-medium" style="color: var(--color-error, #ef4444);">{message}</p>
    </div>"""


def _is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"


@router.post("/subscribe", response_class=HTMLResponse)
async def subscribe(
    request: Request,
    email: str = Form(...),
    name: str = Form(None),
    source: str = Form("footer"),
):
    """Subscribe an email to the newsletter. Returns HTMX HTML snippet or full page."""
    try:
        if not subscriber_service:
            snippet = _error_html("Service unavailable. Please try again later.")
        else:
            result = subscriber_service.subscribe(email, name, source)
            if result["success"]:
                snippet = _success_html(result["message"], email=email)
            else:
                snippet = _error_html(result["message"])

        # HTMX request → return just the snippet
        if _is_htmx(request):
            return HTMLResponse(snippet)

        # Full POST fallback → render a proper page
        return templates.TemplateResponse("newsletter_result.html", {
            "request": request,
            "title": "Newsletter",
            "snippet": snippet,
        })
    except Exception as e:
        print(f"❌ Error in /subscribe endpoint: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

        error_snippet = _error_html("Something went wrong. Please try again.")
        if _is_htmx(request):
            return HTMLResponse(error_snippet)
        return templates.TemplateResponse("newsletter_result.html", {
            "request": request,
            "title": "Newsletter",
            "snippet": error_snippet,
        })


@router.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(
    request: Request,
    email: str = Query(...),
):
    """Unsubscribe an email from the newsletter."""
    try:
        if not subscriber_service:
            snippet = _error_html("Service unavailable. Please try again later.")
        else:
            result = subscriber_service.unsubscribe(email)
            if result["success"]:
                snippet = f"""
                <div class="text-center py-4">
                  <p class="text-sm font-semibold" style="color: var(--color-accent);">{result["message"]}</p>
                </div>"""
            else:
                snippet = _error_html(result["message"])

        return templates.TemplateResponse("newsletter_result.html", {
            "request": request,
            "title": "Unsubscribe",
            "snippet": snippet,
        })
    except Exception as e:
        print(f"❌ Error in /unsubscribe endpoint: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

        snippet = _error_html("Something went wrong during unsubscribe.")
        return templates.TemplateResponse("newsletter_result.html", {
            "request": request,
            "title": "Unsubscribe",
            "snippet": snippet,
        })


KIT_FORM_ID = "9506742"


@router.post("/kit-subscribe", response_class=JSONResponse)
async def kit_subscribe(email: str = Form(...)):
    """Proxy subscription to Kit — server-side POST avoids CORS and redirect issues."""
    data = urllib.parse.urlencode({
        "email_address": email,
        "first_name": "",
        "utf8": "✓",
    }).encode("utf-8")
    req = urllib.request.Request(
        f"https://app.kit.com/forms/{KIT_FORM_ID}/subscriptions",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*",
            "User-Agent": "Mozilla/5.0 (compatible; fullstackpm.tech)",
            "Origin": "https://fullstackpm.tech",
            "Referer": "https://fullstackpm.tech/",
            "X-Requested-With": "XMLHttpRequest",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
        logger.info("Kit subscribe response %s: %.200s", status, body)
        if status in (200, 201):
            return JSONResponse({"ok": True})
        return JSONResponse({"ok": False, "detail": f"Kit returned {status}"}, status_code=502)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        logger.error("Kit subscribe HTTPError %s: %.300s", exc.code, body)
        return JSONResponse({"ok": False, "detail": f"Kit error {exc.code}"}, status_code=502)
    except Exception as exc:
        logger.error("Kit subscribe failed: %s", exc)
        return JSONResponse({"ok": False, "detail": str(exc)}, status_code=502)


@router.get("/status")
async def status():
    """Check if newsletter service is operational (for debugging)."""
    from pathlib import Path
    creds_path = Path(settings.google_sheets_credentials_path)

    return {
        "service_running": subscriber_service is not None,
        "credentials_path": settings.google_sheets_credentials_path,
        "credentials_file_exists": creds_path.exists(),
        "spreadsheet_id": settings.google_sheets_id,
    }


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

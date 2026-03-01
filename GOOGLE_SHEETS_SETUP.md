# Google Sheets Newsletter Setup Instructions

## Step 1: Create Google Sheet
1. Go to https://sheets.google.com
2. Create new blank spreadsheet
3. Name it: "Newsletter Subscribers"
4. **In Row 1, add headers:** `email`, `name`, `source`, `subscribed_at`
5. Copy the sheet ID from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
   - Extract the part between `/d/` and `/edit`
   - Example: `1a2b3c4d5e6f7g8h9i0j`

## Step 2: Create Google Service Account
1. Go to https://console.cloud.google.com
2. Create new project (or use existing)
3. Search for "Google Sheets API" → Enable it
4. Go to "Credentials" (left sidebar)
5. Click "Create Credentials" → "Service Account"
6. Fill in:
   - Service account name: `newsletter-bot`
   - Leave other fields blank
   - Click "Create and Continue"
7. Grant role: `Editor` (or just click "Continue")
8. Click "Create Key" → JSON
9. Download the JSON file and save it

## Step 3: Share Sheet with Service Account
1. Open your Google Sheet
2. Click "Share" (top right)
3. Copy the email from the JSON file:
   - Open downloaded JSON with a text editor
   - Find the line: `"client_email": "xxx@xxx.iam.gserviceaccount.com"`
   - Copy that email address
4. Paste in the "Share" dialog
5. Give it "Editor" access
6. Click "Share"

## Step 4: Update Code in GitHub

### File: `code/requirements.txt`
Add these two lines:
```
gspread==6.1.0
google-auth-oauthlib==1.2.0
```

### File: `code/app/config.py`
Add these environment variables at the top (after imports):
```python
import os

# Google Sheets Newsletter
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "code/secrets/credentials.json")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "PLACEHOLDER_SHEET_ID")
```

Replace `PLACEHOLDER_SHEET_ID` with your actual sheet ID from Step 1.

### File: `code/app/routers/newsletter.py`
Replace entire file with:
```python
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
        credentials_json=settings.GOOGLE_SHEETS_CREDENTIALS_PATH,
        spreadsheet_id=settings.GOOGLE_SHEETS_ID,
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
```

## Step 5: Set Environment Variables in Render

1. Go to https://dashboard.render.com
2. Select your fullstackpm.tech service
3. Go to "Environment" (left sidebar)
4. Add these variables:
   ```
   GOOGLE_SHEETS_ID = YOUR_SHEET_ID_HERE
   GOOGLE_SHEETS_CREDENTIALS_PATH = code/secrets/credentials.json
   ```

5. Create `code/secrets/` folder in your repo (create it locally)
6. Add the JSON file you downloaded: `code/secrets/credentials.json`
7. In GitHub, create `.gitignore` entry (if not already there):
   ```
   code/secrets/
   ```

## Testing

1. Push all changes to GitHub
2. Render auto-deploys in 1-2 min
3. Go to fullstackpm.tech
4. Fill out the newsletter form
5. Check your Google Sheet — new row should appear!

## Troubleshooting

- **"Service unavailable"**: Check that `GOOGLE_SHEETS_ID` is set correctly in Render
- **"Email already subscribed"**: Works! You can unsubscribe by deleting the row in Google Sheets
- **No new row appearing**: Check that the service account email has Editor access to the sheet

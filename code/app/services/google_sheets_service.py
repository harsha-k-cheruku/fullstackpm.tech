# app/services/google_sheets_service.py
"""Newsletter subscriber storage using Google Sheets."""
from datetime import datetime
from typing import Dict, Optional

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False
    print("Warning: gspread not installed. Newsletter will show 'service unavailable'.")


class GoogleSheetsSubscriberService:
    """Manage newsletter subscribers using Google Sheets."""

    def __init__(self, credentials_json: str, spreadsheet_id: str):
        """
        Initialize Google Sheets service.

        Args:
            credentials_json: Path to Google service account JSON file
            spreadsheet_id: ID from your Google Sheet URL (between /d/ and /edit)
                           Example: "1a2b3c4d5e6f7g8h9i0j"
        """
        if not GSPREAD_AVAILABLE:
            raise ImportError("gspread is not installed")

        self.spreadsheet_id = spreadsheet_id

        # Authenticate with Google Sheets API
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(credentials_json, scopes=scopes)
        self.client = gspread.authorize(creds)

        # Open the spreadsheet
        self.sheet = self.client.open_by_key(spreadsheet_id)
        self.worksheet = self.sheet.sheet1

    def subscribe(self, email: str, name: Optional[str] = None, source: str = "footer") -> Dict:
        """Add subscriber to Google Sheet."""
        email = email.lower().strip()

        # Validate email
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            return {"success": False, "message": "Please enter a valid email address."}

        # Check if already subscribed (read all emails from column A)
        try:
            all_emails = self.worksheet.col_values(1)[1:]  # Skip header
            if email in all_emails:
                return {"success": True, "message": "You're already on the list! We'll keep you posted."}
        except Exception as e:
            print(f"Error checking existing subscribers: {e}")
            return {"success": False, "message": "Something went wrong. Please try again."}

        # Add new row to sheet
        try:
            new_row = [
                email,
                name.strip() if name else "",
                source,
                datetime.now().isoformat(),
            ]
            self.worksheet.append_row(new_row)
            return {"success": True, "message": "You're in! Thanks for subscribing."}
        except Exception as e:
            print(f"Error adding subscriber: {e}")
            return {"success": False, "message": "Something went wrong. Please try again."}

    def export_csv(self) -> str:
        """Export all subscribers as CSV string."""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        try:
            all_rows = self.worksheet.get_all_values()
            for row in all_rows:
                writer.writerow(row)
            return output.getvalue()
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return "error"

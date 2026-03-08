#!/usr/bin/env python3
"""Debug script to test Google Sheets newsletter service."""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.services.google_sheets_service import GoogleSheetsSubscriberService

print("=" * 60)
print("NEWSLETTER SERVICE DEBUG")
print("=" * 60)

print(f"\n1. Checking credentials path:")
print(f"   Config path: {settings.google_sheets_credentials_path}")
creds_path = Path(settings.google_sheets_credentials_path)
print(f"   File exists: {creds_path.exists()}")
if creds_path.exists():
    print(f"   File size: {creds_path.stat().st_size} bytes")

print(f"\n2. Checking Google Sheets ID:")
print(f"   Spreadsheet ID: {settings.google_sheets_id}")

print(f"\n3. Attempting to initialize service...")
try:
    service = GoogleSheetsSubscriberService(
        credentials_json=settings.google_sheets_credentials_path,
        spreadsheet_id=settings.google_sheets_id,
    )
    print("   ✅ Service initialized successfully!")

    print(f"\n4. Testing subscribe endpoint...")
    result = service.subscribe("test@example.com", "Test User", "debug")
    print(f"   Result: {result}")

    if result["success"]:
        print("   ✅ Subscribe works!")
    else:
        print(f"   ❌ Subscribe failed: {result['message']}")

except ImportError as e:
    print(f"   ❌ Import error (gspread not installed): {e}")
except FileNotFoundError as e:
    print(f"   ❌ File not found: {e}")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

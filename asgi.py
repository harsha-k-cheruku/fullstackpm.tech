"""
ASGI entry point for Render deployment.
Imports and exposes the FastAPI app from code/app/main.py
"""
import sys
from pathlib import Path

# Add code directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "code"))

# Import the app
from app.main import app

__all__ = ["app"]

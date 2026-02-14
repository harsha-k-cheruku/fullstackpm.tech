"""
ASGI entry point for Render deployment.
Imports and exposes the FastAPI app from app/main.py
"""
import sys
from pathlib import Path

# Add current directory to Python path so app module can be imported
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app

__all__ = ["app"]

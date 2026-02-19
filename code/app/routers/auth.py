# app/routers/auth.py
"""Authentication routes for SDE Prep Tool."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/api/sde-prep/auth", tags=["auth"])


def get_current_user_id(request: Request) -> Optional[int]:
    """Extract user_id from session cookie."""
    user_id = request.cookies.get("user_id")
    return int(user_id) if user_id else None


@router.post("/login")
async def login(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Login or create user."""
    if not email:
        raise HTTPException(status_code=400, detail="Email required")

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(first_name=first_name, last_name=last_name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        db.commit()
        db.refresh(user)

    response = JSONResponse(content=user.to_dict())
    response.set_cookie(
        "user_id",
        str(user.id),
        httponly=True,
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
    )
    return response


@router.post("/logout")
async def logout() -> JSONResponse:
    """Logout current user."""
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("user_id")
    return response


@router.get("/current-user")
async def current_user(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Get currently logged-in user."""
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(user.to_dict())

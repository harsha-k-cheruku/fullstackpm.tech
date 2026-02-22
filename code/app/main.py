# app/main.py
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import init_db
from app.routers import auth, blog, comments, interview_coach, marketplace, pages, pm_multiverse, projects, sde_prep, seo
from app.services.content import ContentService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    init_db()

    # Load content
    content_service = ContentService(settings.content_dir)
    content_service.load()
    app.state.content_service = content_service
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

# Include routers
app.include_router(pages.router)
app.include_router(pm_multiverse.router)
app.include_router(projects.router)
app.include_router(blog.router)
app.include_router(comments.router)
app.include_router(interview_coach.router)
app.include_router(marketplace.router)
app.include_router(sde_prep.router)
app.include_router(auth.router)
app.include_router(seo.router)
app.include_router(seo.router)

# Templates
templates = Jinja2Templates(directory=str(settings.templates_dir))


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> HTMLResponse:
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "title": "Page Not Found", "config": settings, "current_page": "", "year": datetime.now().year},
        status_code=404,
    )
# app/main.py
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import SessionLocal, ensure_feed_layer2_columns, init_db
from app.models.like import Like  # noqa: F401 — ensures table is created by init_db
from app.models.episode import Episode  # noqa: F401 — ensures table is created by init_db
from app.models.narada_override import NaradaOverride  # noqa: F401 — ensures table is created by init_db
from app.models.josaa_scenario import JosaaScenario  # noqa: F401 — ensures table is created by init_db
from app.models.feed_article import FeedArticle  # noqa: F401 — ensures table is created by init_db
from app.routers import auth, backstory, blog, comments, daily_brief, feed, interview_coach, josaa_tool, learning_brief, likes, marketplace, narada_admin, newsletter, pages, pm_multiverse, pm_prep, podcast, projects, resources, sde_prep, seo
from app.services.content import ContentService
from app.services.feed_service import feed_service
from app.services.reading_service import ReadingService


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    ensure_feed_layer2_columns()

    content_service = ContentService(settings.content_dir)
    content_service.load()
    app.state.content_service = content_service

    app.state.reading_service = ReadingService(settings.static_dir / "data")

    # Populate feed from pre-processed articles.json (committed to git, survives deploys).
    # This runs synchronously on startup so the homepage is never empty after a deploy.
    _articles_json = settings.static_dir / "feed" / "articles.json"
    _sync_db = SessionLocal()
    try:
        feed_service.sync_from_json(_sync_db, _articles_json)
    finally:
        _sync_db.close()

    # Background RSS fetch every 6 hours catches articles published between
    # local feed pipeline runs. No AI processing — just URL capture.
    async def _fetch_loop():
        while True:
            await asyncio.sleep(6 * 3600)
            db = SessionLocal()
            try:
                feed_service.fetch_all(db)
            finally:
                db.close()

    task = asyncio.create_task(_fetch_loop())
    yield
    task.cancel()


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
app.include_router(feed.router)
app.include_router(podcast.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(newsletter.router)
app.include_router(interview_coach.router)
app.include_router(josaa_tool.router)
app.include_router(marketplace.router)
app.include_router(resources.router)
app.include_router(daily_brief.router)
app.include_router(learning_brief.router)
app.include_router(backstory.router)
app.include_router(sde_prep.router)
app.include_router(pm_prep.router)
app.include_router(narada_admin.router)
app.include_router(auth.router)
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
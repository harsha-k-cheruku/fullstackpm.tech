# app/routers/projects.py
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def _ctx(request: Request, **kwargs) -> dict:
    """Build the standard template context."""
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request) -> HTMLResponse:
    content_service = request.app.state.content_service
    project_list = content_service.get_projects()
    return templates.TemplateResponse(
        "projects/gallery.html",
        _ctx(
            request,
            title="Projects  fullstackpm.tech",
            current_page="/projects",
            projects=project_list,
            active_filter="all",
        ),
    )


@router.get("/projects/{slug}", response_class=HTMLResponse)
async def project_detail(request: Request, slug: str) -> HTMLResponse:
    content_service = request.app.state.content_service
    project = content_service.get_project_by_slug(slug)
    if project is None:
        return templates.TemplateResponse(
            "404.html",
            _ctx(request, title="Page Not Found", current_page=""),
            status_code=404,
        )

    return templates.TemplateResponse(
        "projects/detail.html",
        _ctx(
            request,
            title=f"{project.title}  Projects",
            current_page="/projects",
            project=project,
        ),
    )


# HTMX Endpoints
@router.get("/api/projects/filter", response_class=HTMLResponse)
async def projects_filter_htmx(request: Request, status: str = "all") -> HTMLResponse:
    """HTMX endpoint for filtering projects by status."""
    content_service = request.app.state.content_service
    project_list = content_service.get_projects()

    # Filter by status if not "all"
    if status != "all":
        # Normalize status: replace underscores and spaces, then compare
        normalized_filter = status.lower().replace("_", "").replace(" ", "")
        project_list = [p for p in project_list if p.status.lower().replace("_", "").replace(" ", "") == normalized_filter]

    return templates.TemplateResponse(
        "projects/partials/project_grid.html",
        _ctx(
            request,
            projects=project_list,
            active_filter=status,
        ),
    )

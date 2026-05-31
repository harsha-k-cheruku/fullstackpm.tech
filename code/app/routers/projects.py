# app/routers/projects.py
from datetime import datetime

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.course_explainer_service import CourseExplainerService

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))
_explainer = CourseExplainerService()


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
    visible_statuses = {"live", "inprogress"}
    project_list = [
        p for p in project_list
        if p.status.lower().replace("_", "").replace(" ", "") in visible_statuses
    ]

    # Sort: live projects first, then others by display_order
    project_list = sorted(project_list, key=lambda p: (p.status != "live", p.display_order))
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


# ── Engineering Course Explainer (India) ──────────────────────
# These MUST be before the /projects/{slug} catch-all.

@router.get("/projects/engineering-course-explainer-india/explore", response_class=HTMLResponse)
async def explainer_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "resources/engineering_course_explainer_index.html",
        _ctx(request, title="Engineering Course Explainer (India) — fullstackpm.tech",
             current_page="/projects", courses=_explainer.all_courses()),
    )


@router.get("/projects/engineering-course-explainer-india/explore/compare", response_class=HTMLResponse)
async def explainer_compare(
    request: Request,
    left: str = Query("computer-science-and-engineering"),
    right: str = Query("mechanical-engineering"),
) -> HTMLResponse:
    courses = _explainer.all_courses()
    left_course = _explainer.get_by_slug(left) or courses[0]
    right_course = _explainer.get_by_slug(right) or courses[1]
    return templates.TemplateResponse(
        "resources/engineering_course_explainer_compare.html",
        _ctx(request, title=f"Compare {left_course.name} vs {right_course.name} | fullstackpm.tech",
             current_page="/projects", courses=courses,
             left_course=left_course, right_course=right_course),
    )


@router.get("/projects/engineering-course-explainer-india/explore/{course_slug}", response_class=HTMLResponse)
async def explainer_detail(request: Request, course_slug: str) -> HTMLResponse:
    course = _explainer.get_by_slug(course_slug)
    if not course:
        return templates.TemplateResponse(
            "404.html", _ctx(request, title="Course Not Found", current_page="/projects"),
            status_code=404,
        )
    return templates.TemplateResponse(
        "resources/engineering_course_explainer_detail.html",
        _ctx(request, title=f"{course.name} — Engineering Course Explainer | fullstackpm.tech",
             current_page="/projects", course=course, courses=_explainer.all_courses()),
    )


@router.get("/projects/upstart-clearing-simulator/prfaq", response_class=HTMLResponse)
async def upstart_lifecycle_prfaq(request: Request) -> HTMLResponse:
    """PRFAQ page for Upstart Lifecycle Simulator."""
    return templates.TemplateResponse(
        "projects/upstart_prfaq.html",
        _ctx(
            request,
            title="Upstart Lifecycle Simulator PRFAQ — fullstackpm.tech",
            current_page="/projects",
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
    visible_statuses = {"live", "inprogress"}
    project_list = [
        p for p in project_list
        if p.status.lower().replace("_", "").replace(" ", "") in visible_statuses
    ]

    # Filter by status if not "all"
    if status != "all":
        # Normalize status: replace underscores and spaces, then compare
        normalized_filter = status.lower().replace("_", "").replace(" ", "")
        project_list = [p for p in project_list if p.status.lower().replace("_", "").replace(" ", "") == normalized_filter]

    # Sort: live projects first, then others by display_order
    project_list = sorted(project_list, key=lambda p: (p.status != "live", p.display_order))

    return templates.TemplateResponse(
        "projects/partials/project_grid.html",
        _ctx(
            request,
            projects=project_list,
            active_filter=status,
        ),
    )

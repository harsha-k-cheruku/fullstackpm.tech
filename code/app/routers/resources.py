# app/routers/resources.py
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.course_explainer_service import CourseExplainerService

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))
course_service = CourseExplainerService()


def _ctx(request: Request, **kwargs) -> dict:
    """Build the standard template context."""
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


@router.get("/resources", response_class=HTMLResponse)
async def resources_hub(request: Request) -> HTMLResponse:
    """Resources hub page."""
    return templates.TemplateResponse(
        "resources/index.html",
        _ctx(
            request,
            title="Resources - fullstackpm.tech",
            current_page="/resources",
        ),
    )


@router.get("/resources/engineering-course-explainer", response_class=HTMLResponse)
async def engineering_course_explainer_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "resources/engineering_course_explainer_index.html",
        _ctx(
            request,
            title="Engineering Course Explainer (India) — fullstackpm.tech",
            current_page="/resources/engineering-course-explainer",
            courses=course_service.all_courses(),
        ),
    )


@router.get("/resources/engineering-course-explainer/compare", response_class=HTMLResponse)
async def engineering_course_explainer_compare(
    request: Request,
    left: str = Query("computer-science-and-engineering"),
    right: str = Query("mechanical-engineering"),
) -> HTMLResponse:
    courses = course_service.all_courses()
    left_course = course_service.get_by_slug(left) or courses[0]
    right_course = course_service.get_by_slug(right) or courses[1]
    return templates.TemplateResponse(
        "resources/engineering_course_explainer_compare.html",
        _ctx(
            request,
            title=f"Compare {left_course.name} vs {right_course.name} | fullstackpm.tech",
            current_page="/resources/engineering-course-explainer",
            courses=courses,
            left_course=left_course,
            right_course=right_course,
        ),
    )


@router.get("/resources/engineering-course-explainer/{course_slug}", response_class=HTMLResponse)
async def engineering_course_explainer_detail(request: Request, course_slug: str) -> HTMLResponse:
    course = course_service.get_by_slug(course_slug)
    if not course:
        return templates.TemplateResponse(
            "404.html",
            _ctx(request, title="Course Not Found", current_page="/resources/engineering-course-explainer"),
            status_code=404,
        )
    return templates.TemplateResponse(
        "resources/engineering_course_explainer_detail.html",
        _ctx(
            request,
            title=f"{course.name} — Engineering Course Explainer | fullstackpm.tech",
            current_page="/resources/engineering-course-explainer",
            course=course,
            courses=course_service.all_courses(),
        ),
    )


@router.get("/resources/product-breakdowns", response_class=HTMLResponse)
async def product_breakdowns(request: Request) -> HTMLResponse:
    """Product Breakdowns placeholder page."""
    return templates.TemplateResponse(
        "resources/product_breakdowns.html",
        _ctx(
            request,
            title="Product Breakdowns - fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/product-breakdowns/search-and-discovery", response_class=HTMLResponse)
async def search_and_discovery_breakdown(request: Request) -> HTMLResponse:
    """Serve the Search & Discovery product deep dive."""
    return templates.TemplateResponse(
        "resources/product_breakdowns/search_and_discovery.html",
        _ctx(
            request,
            title="Search & Discovery Deep Dive — PM Product Breakdown | fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/product-breakdowns/trust-and-safety", response_class=HTMLResponse)
async def trust_and_safety(request: Request) -> HTMLResponse:
    """Serve the Trust & Safety deep dive."""
    return templates.TemplateResponse(
        "resources/product_breakdowns/trust_and_safety.html",
        _ctx(
            request,
            title="Trust & Safety — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/product-breakdowns/ratings-and-reviews", response_class=HTMLResponse)
async def ratings_and_reviews(request: Request) -> HTMLResponse:
    """Serve the Ratings & Reviews deep dive."""
    return templates.TemplateResponse(
        "resources/product_breakdowns/ratings_and_reviews.html",
        _ctx(
            request,
            title="Ratings & Reviews — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/product-breakdowns/payments-and-checkout", response_class=HTMLResponse)
async def payments_and_checkout(request: Request) -> HTMLResponse:
    """Serve the Payments & Checkout deep dive."""
    return templates.TemplateResponse(
        "resources/product_breakdowns/payments_and_checkout.html",
        _ctx(
            request,
            title="Payments & Checkout — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/product-breakdowns/recommendations-personalization", response_class=HTMLResponse)
async def recommendations_personalization(request: Request) -> HTMLResponse:
    """Serve the Recommendations & Personalization deep dive."""
    return templates.TemplateResponse(
        "resources/product_breakdowns/recommendations_and_personalization.html",
        _ctx(
            request,
            title="Recommendations & Personalization — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/product-breakdowns/onboarding-activation", response_class=HTMLResponse)
async def onboarding_activation(request: Request) -> HTMLResponse:
    """Serve the Onboarding & Activation deep dive."""
    return templates.TemplateResponse(
        "resources/product_breakdowns/onboarding_and_activation.html",
        _ctx(
            request,
            title="Onboarding & Activation — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/ecosystem-maps", response_class=HTMLResponse)
async def ecosystem_maps(request: Request) -> HTMLResponse:
    """Ecosystem Maps gallery page."""
    return templates.TemplateResponse(
        "resources/ecosystem_maps.html",
        _ctx(
            request,
            title="Ecosystem Maps - fullstackpm.tech",
            current_page="/resources/ecosystem-maps",
        ),
    )


@router.get("/resources/ecosystem-maps/financial-ecosystem", response_class=HTMLResponse)
async def financial_ecosystem(request: Request) -> HTMLResponse:
    """Serve the Financial Ecosystem visual map."""
    return templates.TemplateResponse(
        "resources/financial_ecosystem.html",
        _ctx(
            request,
            title="Financial Ecosystem — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/ecosystem-maps",
        ),
    )


@router.get("/resources/ecosystem-maps/two-sided-marketplace", response_class=HTMLResponse)
async def two_sided_marketplace(request: Request) -> HTMLResponse:
    """Serve the Two-Sided Marketplace visual map."""
    return templates.TemplateResponse(
        "resources/two_sided_marketplace.html",
        _ctx(
            request,
            title="Two-Sided Marketplace Ecosystem — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/ecosystem-maps",
        ),
    )


@router.get("/resources/ecosystem-maps/adtech-ecosystem", response_class=HTMLResponse)
async def adtech_ecosystem(request: Request) -> HTMLResponse:
    """Serve the Adtech / Programmatic ecosystem visual map."""
    return templates.TemplateResponse(
        "resources/adtech_ecosystem.html",
        _ctx(
            request,
            title="Adtech / Programmatic Ecosystem — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/ecosystem-maps",
        ),
    )


@router.get("/resources/ecosystem-maps/healthcare-ecosystem", response_class=HTMLResponse)
async def healthcare_ecosystem(request: Request) -> HTMLResponse:
    """Serve the US Healthcare ecosystem visual map."""
    return templates.TemplateResponse(
        "resources/healthcare_ecosystem.html",
        _ctx(
            request,
            title="US Healthcare Ecosystem — PM Visual Guide | fullstackpm.tech",
            current_page="/resources/ecosystem-maps",
        ),
    )

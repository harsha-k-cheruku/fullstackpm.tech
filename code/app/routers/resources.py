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
course_service = CourseExplainerService(settings.data_dir / "engineering_course_explainers.json")

FAMILY_SUMMARIES = {
    "computing": {
        "title": "Computing branches",
        "summary": "Good for students who like coding, logic, software systems, and digital problem solving.",
        "compare": "Compare these if you're deciding between broad software flexibility vs more math-heavy or AI/data-flavored paths.",
    },
    "electronics": {
        "title": "Electronics branches",
        "summary": "Good for students who want circuits, devices, communication systems, embedded systems, or chip-facing work.",
        "compare": "Compare these if you're deciding between hardware depth, embedded overlap, and flexibility into software later.",
    },
    "mechanical": {
        "title": "Mechanical / industrial branches",
        "summary": "Good for students who like machines, manufacturing, automation, industrial systems, and physical engineering.",
        "compare": "Compare these if you care about design, production, operations, robotics, or applied physical systems work.",
    },
    "civil": {
        "title": "Civil / infrastructure branches",
        "summary": "Good for students who care about structures, cities, infrastructure, and visible real-world physical impact.",
        "compare": "Compare these if you want roads, buildings, water, transport, or site/project-heavy engineering work.",
    },
    "process": {
        "title": "Process / chemical branches",
        "summary": "Good for students who enjoy chemistry-linked systems, industrial plants, production, and transformation at scale.",
        "compare": "Compare these if you're weighing chemicals, food, pharma, petroleum, or process-heavy manufacturing roles.",
    },
    "materials": {
        "title": "Materials branches",
        "summary": "Good for students curious about metals, ceramics, alloys, durability, and why materials behave differently.",
        "compare": "Compare these if you're interested in manufacturing, material science, heavy industry, or specialized process roles.",
    },
    "bio": {
        "title": "Bio-linked branches",
        "summary": "Good for students who want biology + engineering combinations in health, biotech, devices, or applied life sciences.",
        "compare": "Compare these if you're deciding between biotech, biomedical, bioengineering, and adjacent research-heavy paths.",
    },
    "advanced": {
        "title": "Physics / frontier branches",
        "summary": "Good for students who enjoy physics-heavy engineering, advanced analytical systems, and specialized technical domains.",
        "compare": "Compare these if you're drawn to aerospace, energy, engineering physics, or research-oriented engineering depth.",
    },
    "general": {
        "title": "Other engineering branches",
        "summary": "Mixed engineering branches that are practical, domain-specific, and often best understood through actual course detail pages.",
        "compare": "Use the detail pages to judge fit based on work, not just branch name familiarity.",
    },
}


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
            grouped_courses=course_service.grouped_courses(),
            popular_courses=course_service.popular_courses(),
            curated_top_courses=course_service.curated_top_courses(),
            family_summaries=FAMILY_SUMMARIES,
        ),
    )


@router.get("/resources/engineering-course-explainer/compare", response_class=HTMLResponse)
async def engineering_course_explainer_compare(
    request: Request,
    left: str = Query(...),
    right: str = Query(...),
) -> HTMLResponse:
    left_course = course_service.get_by_slug(left)
    right_course = course_service.get_by_slug(right)
    if not left_course or not right_course:
        return templates.TemplateResponse(
            "404.html",
            _ctx(request, title="Course Comparison Not Found", current_page="/resources/engineering-course-explainer"),
            status_code=404,
        )
    return templates.TemplateResponse(
        "resources/engineering_course_explainer_compare.html",
        _ctx(
            request,
            title=f"Compare {left_course.name} vs {right_course.name} | fullstackpm.tech",
            current_page="/resources/engineering-course-explainer",
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

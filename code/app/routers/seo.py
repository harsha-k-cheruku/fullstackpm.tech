# app/routers/seo.py
from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.config import settings
from app.services.feed import FeedService

router = APIRouter()


@router.get("/feed.xml")
async def rss_feed(request: Request) -> Response:
    content_service = request.app.state.content_service
    posts, _ = content_service.get_posts(page=1, per_page=100)
    feed_service = FeedService(
        site_url=settings.site_url,
        site_title=settings.site_title,
        site_description=settings.site_description,
    )
    xml_content = feed_service.generate_rss(posts)
    return Response(content=xml_content, media_type="application/xml")


@router.get("/sitemap.xml")
async def sitemap(request: Request) -> Response:
    content_service = request.app.state.content_service
    today = date.today().isoformat()
    base = settings.site_url

    static_pages = [
        ("/", "daily", "1.0"),
        ("/about", "monthly", "0.7"),
        ("/contact", "monthly", "0.5"),
        ("/resume", "monthly", "0.7"),
        ("/projects", "weekly", "0.8"),
        ("/blog", "daily", "0.9"),
    ]

    urls: list[str] = []
    for path, freq, priority in static_pages:
        urls.append(
            f"  <url>\n"
            f"    <loc>{base}{path}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )

    for project in content_service.get_projects():
        urls.append(
            f"  <url>\n"
            f"    <loc>{base}/projects/{project.slug}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.6</priority>\n"
            f"  </url>"
        )

    posts, _ = content_service.get_posts(page=1, per_page=100)
    for post in posts:
        urls.append(
            f"  <url>\n"
            f"    <loc>{base}/blog/{post.slug}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.7</priority>\n"
            f"  </url>"
        )

    for tag in content_service.get_all_tags():
        urls.append(
            f"  <url>\n"
            f"    <loc>{base}/blog/tag/{tag}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>weekly</changefreq>\n"
            f"    <priority>0.5</priority>\n"
            f"  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>"
    )
    return Response(content=xml, media_type="application/xml")


@router.get("/robots.txt")
async def robots_txt() -> Response:
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {settings.site_url}/sitemap.xml\n"
    )
    return Response(content=content, media_type="text/plain")

# app/services/content.py
from __future__ import annotations

import math
import re
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import frontmatter
import markdown
from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    slug: str
    date: datetime
    tags: list[str]
    excerpt: str
    author: str
    reading_time: str
    html_content: str


class Project(BaseModel):
    title: str
    slug: str
    description: str
    tech_stack: list[str]
    status: str
    featured: bool
    display_order: int
    github_url: str
    live_url: str
    problem: str | None = None
    approach: str | None = None
    solution: str | None = None
    html_content: str


class ContentService:
    def __init__(self, content_dir: str | Path) -> None:
        self.content_dir = Path(content_dir)
        self._posts: list[BlogPost] = []
        self._projects: list[Project] = []
        self._tags: set[str] = set()

    def load(self) -> None:
        self._posts = self._load_posts()
        self._projects = self._load_projects()
        self._tags = {tag for post in self._posts for tag in post.tags}

    def get_posts(self, page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]:
        return self._paginate(self._posts, page, per_page)

    def get_post_by_slug(self, slug: str) -> BlogPost | None:
        return next((post for post in self._posts if post.slug == slug), None)

    def get_posts_by_tag(self, tag: str, page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]:
        normalized_tag = tag.lower()
        filtered = [post for post in self._posts if normalized_tag in {t.lower() for t in post.tags}]
        return self._paginate(filtered, page, per_page)

    def get_all_tags(self) -> list[str]:
        return sorted(self._tags, key=str.lower)

    def get_projects(self) -> list[Project]:
        return list(self._projects)

    def get_project_by_slug(self, slug: str) -> Project | None:
        return next((project for project in self._projects if project.slug == slug), None)

    def get_featured_projects(self, limit: int = 3) -> list[Project]:
        return [project for project in self._projects if project.featured][:limit]

    def _load_posts(self) -> list[BlogPost]:
        blog_dir = self.content_dir / "blog"
        posts: list[BlogPost] = []
        for path in sorted(blog_dir.glob("*.md")):
            post = frontmatter.load(path)
            metadata = post.metadata
            content_html = self._render_markdown(post.content)
            slug = self._slug_from_filename(path.name)
            tags = self._normalize_list(metadata.get("tags", []))

            posts.append(
                BlogPost(
                    title=str(metadata.get("title", "")),
                    slug=slug,
                    date=self._parse_date(metadata.get("date")),
                    tags=tags,
                    excerpt=str(metadata.get("excerpt", "")),
                    author=str(metadata.get("author", "")),
                    reading_time=self._calculate_reading_time(post.content),
                    html_content=content_html,
                )
            )
        return sorted(posts, key=lambda item: item.date, reverse=True)

    def _load_projects(self) -> list[Project]:
        projects_dir = self.content_dir / "projects"
        projects: list[Project] = []
        for path in sorted(projects_dir.glob("*.md")):
            project = frontmatter.load(path)
            metadata = project.metadata
            content_html = self._render_markdown(project.content)
            slug = self._slug_from_filename(path.name)

            projects.append(
                Project(
                    title=str(metadata.get("title", "")),
                    slug=slug,
                    description=str(metadata.get("description", "")),
                    tech_stack=self._normalize_list(metadata.get("tech_stack", [])),
                    status=str(metadata.get("status", "planned")),
                    featured=bool(metadata.get("featured", False)),
                    display_order=int(metadata.get("display_order", 9999)),
                    github_url=str(metadata.get("github_url", "")),
                    live_url=str(metadata.get("live_url", "")),
                    problem=str(metadata.get("problem", "")) or None,
                    approach=str(metadata.get("approach", "")) or None,
                    solution=str(metadata.get("solution", "")) or None,
                    html_content=content_html,
                )
            )
        return sorted(projects, key=lambda item: (item.display_order, item.title.lower()))

    def _render_markdown(self, content: str) -> str:
        """Render markdown to HTML with extended formatting support."""
        return markdown.markdown(
            content,
            extensions=[
                "extra",           # Includes: tables, strikethrough, attr_list, fenced_code, etc.
                "codehilite",      # Syntax highlighting for code blocks
                "toc",             # Table of contents support
                "smarty",          # Smart typography (quotes, dashes, etc.)
            ],
            extension_configs={
                "codehilite": {"use_pygments": False},  # Fallback if pygments not available
            },
        )

    def _calculate_reading_time(self, content: str) -> str:
        words = len(re.findall(r"\w+", content))
        minutes = max(1, math.ceil(words / 200))
        return f"{minutes} min read"

    def _slug_from_filename(self, filename: str) -> str:
        stem = Path(filename).stem
        stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
        stem = stem.replace("_", " ").strip().lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", stem)
        slug = re.sub(r"\s+", "-", slug)
        return slug

    def _parse_date(self, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return datetime.now()

    def _normalize_list(self, value: Iterable[str] | str) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return [str(item).strip() for item in value if str(item).strip()]

    def _paginate(self, items: list[BlogPost] | list[Project], page: int, per_page: int) -> tuple[list, int]:
        total = len(items)
        page_index = max(page, 1) - 1
        per_page = max(per_page, 1)
        start = page_index * per_page
        end = start + per_page
        return items[start:end], total

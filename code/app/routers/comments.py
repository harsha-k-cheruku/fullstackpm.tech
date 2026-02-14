# app/routers/comments.py
"""Comments API routes for blog posts."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment

router = APIRouter(prefix="/api/comments", tags=["comments"])


class CommentCreate:
    """Pydantic-free comment creation."""

    def __init__(self, blog_post_slug: str, author_name: str, author_email: str, content: str):
        self.blog_post_slug = blog_post_slug
        self.author_name = author_name
        self.author_email = author_email
        self.content = content


@router.post("/{blog_post_slug}")
async def create_comment(
    blog_post_slug: str,
    author_name: str,
    author_email: str,
    content: str,
    db: Session = Depends(get_db),
):
    """Create a new comment on a blog post."""
    # Validate inputs
    if not author_name or len(author_name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    if not author_email or "@" not in author_email:
        raise HTTPException(status_code=400, detail="Valid email required")
    if not content or len(content.strip()) < 5:
        raise HTTPException(status_code=400, detail="Comment must be at least 5 characters")

    # Create comment
    comment = Comment(
        blog_post_slug=blog_post_slug,
        author_name=author_name.strip(),
        author_email=author_email.strip().lower(),
        content=content.strip(),
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment.to_dict()


@router.get("/{blog_post_slug}")
async def get_comments(blog_post_slug: str, db: Session = Depends(get_db)):
    """Get all comments for a blog post, ordered by newest first."""
    comments = (
        db.query(Comment)
        .filter(Comment.blog_post_slug == blog_post_slug)
        .order_by(Comment.created_at.desc())
        .all()
    )
    return [comment.to_dict() for comment in comments]

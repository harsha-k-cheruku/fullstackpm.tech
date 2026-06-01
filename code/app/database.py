# app/database.py
"""Database setup for blog comments."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    poolclass=StaticPool if "sqlite" in settings.database_url else None,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def ensure_feed_layer2_columns() -> None:
    """Idempotent migration: add Layer 2 columns to feed_articles if missing."""
    from sqlalchemy import inspect, text

    existing = {col["name"] for col in inspect(engine).get_columns("feed_articles")}
    new_columns = {
        "is_dismissed": "ALTER TABLE feed_articles ADD COLUMN is_dismissed BOOLEAN DEFAULT 0",
        "ai_summary": "ALTER TABLE feed_articles ADD COLUMN ai_summary TEXT",
        "first_principle": "ALTER TABLE feed_articles ADD COLUMN first_principle TEXT",
        "key_insight": "ALTER TABLE feed_articles ADD COLUMN key_insight TEXT",
        "ai_insight": "ALTER TABLE feed_articles ADD COLUMN ai_insight TEXT",
        "ai_score": "ALTER TABLE feed_articles ADD COLUMN ai_score INTEGER",
        "ai_score_reason": "ALTER TABLE feed_articles ADD COLUMN ai_score_reason TEXT",
        "ai_processed_at": "ALTER TABLE feed_articles ADD COLUMN ai_processed_at DATETIME",
    }
    with engine.begin() as conn:
        for column, statement in new_columns.items():
            if column not in existing:
                conn.execute(text(statement))

"""Stage 1: fetch RSS into feed_articles. No AI."""
from pipeline import config  # noqa: F401 — wires DATABASE_URL + sys.path

from app.database import SessionLocal, ensure_feed_layer2_columns, ensure_pipeline_tables, init_db
from app.services.feed_service import feed_service


def run() -> dict:
    init_db()
    ensure_feed_layer2_columns()
    ensure_pipeline_tables()

    db = SessionLocal()
    try:
        new = feed_service.fetch_all(db)
        return {"stage": "fetch", "new_articles": new}
    finally:
        db.close()


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))

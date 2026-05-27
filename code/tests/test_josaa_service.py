from app.services.josaa_service import JosaaService, JosaaQuery


DATA_PATH = "/Users/sidc/Projects/josaa-data-pipeline/data/normalized/josaa_master.csv"


def test_basic_query_returns_results():
    service = JosaaService(DATA_PATH)
    q = JosaaQuery(rank=15000, year=2025, mode="basic")
    rows, meta = service.top_25(q)
    assert len(rows) > 0
    assert meta["total_candidates"] > 0


def test_constrained_query_respects_institute_term():
    service = JosaaService(DATA_PATH)
    q = JosaaQuery(
        rank=15000,
        year=2025,
        preferred_institutes=["iit delhi"],
        mode="basic",
    )
    rows, _ = service.top_25(q)
    assert all("iit delhi" in r["institute"].lower() for r in rows)


def test_strict_mode_runs():
    service = JosaaService(DATA_PATH)
    q = JosaaQuery(rank=20000, year=2024, mode="strict")
    rows, _ = service.top_25(q)
    assert isinstance(rows, list)

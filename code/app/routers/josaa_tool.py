from datetime import datetime

import io
import csv
import json
import secrets

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import get_db
from app.models.josaa_scenario import JosaaScenario
from app.services.josaa_service import JosaaQuery, get_josaa_service

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def _ctx(request: Request, **kwargs) -> dict:
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


def _get_or_create_session_key(request: Request) -> str:
    key = request.cookies.get("josaa_session_key")
    if key:
        return key
    return secrets.token_urlsafe(18)


def _list_scenarios(db: Session, session_key: str) -> list[JosaaScenario]:
    return (
        db.query(JosaaScenario)
        .filter(JosaaScenario.session_key == session_key)
        .order_by(JosaaScenario.created_at.desc())
        .limit(20)
        .all()
    )


def _build_form_state(**kwargs) -> dict:
    defaults = {
        "rank": "",
        "year": None,
        "history_window": "3",
        "round_number": "",
        "quota": "",
        "gender": "",
        "preferred_branches": "",
        "preferred_institutes": "",
        "mode": "basic",
        "branch_weight": "0.15",
        "institute_weight": "0.10",
        "compare_rank": "",
    }
    defaults.update(kwargs)
    return defaults


@router.get("/tools/josaa-top-25", response_class=HTMLResponse)
async def josaa_top_25_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    # Keep GET ultra-fast: do NOT parse the large CSV on first page load.
    # Heavy dataset work is deferred to form submission.
    years = [2025, 2024, 2023, 2022, 2021, 2020]
    default_year = 2025
    rounds = []
    quotas = []
    genders = []
    error = (
        "Tip: first run may take a bit while dataset warms up on server. "
        "If it fails, retry in a few seconds."
    )

    session_key = _get_or_create_session_key(request)
    response = templates.TemplateResponse(
        "tools/josaa_top25.html",
        _ctx(
            request,
            title="JoSAA Top 25 Predictor — fullstackpm.tech",
            current_page="/tools/josaa-top-25",
            years=years,
            rounds=rounds,
            quotas=quotas,
            genders=genders,
            form_state=_build_form_state(year=default_year, compare_rank=""),
            results=[],
            meta=None,
            error=error,
            round_insights=[],
            saved_scenarios=_list_scenarios(db, session_key),
        ),
    )
    response.set_cookie("josaa_session_key", session_key, max_age=60 * 60 * 24 * 90)
    return response


@router.post("/tools/josaa-top-25", response_class=HTMLResponse)
async def josaa_top_25_run(
    request: Request,
    db: Session = Depends(get_db),
    rank: int = Form(...),
    history_window: int = Form(3),
    round_number: str = Form(""),
    quota: str = Form(""),
    gender: str = Form(""),
    preferred_branches: str = Form(""),
    preferred_institutes: str = Form(""),
    mode: str = Form("basic"),
    branch_weight: float = Form(0.15),
    institute_weight: float = Form(0.10),
    compare_rank: str = Form(""),
) -> HTMLResponse:
    service = get_josaa_service(settings.josaa_data_path)
    years = service.get_years()
    available_years = service.get_years()
    target_year = available_years[-1] if available_years else datetime.now().year
    rounds = service.get_rounds_for_year(target_year)

    try:
        round_value = int(round_number) if round_number.strip() else None
    except ValueError:
        round_value = None

    quota_clean = quota.strip()
    gender_clean = gender.strip()
    if not quota_clean or not gender_clean:
        return templates.TemplateResponse(
            "tools/josaa_top25.html",
            _ctx(
                request,
                title="JoSAA Top 25 Predictor — fullstackpm.tech",
                current_page="/tools/josaa-top-25",
                years=available_years,
                rounds=rounds,
                quotas=service.get_quotas(),
                genders=service.get_genders(),
                form_state=_build_form_state(
                    rank=str(rank),
                    year=target_year,
                    history_window=str(history_window),
                    round_number=round_number,
                    quota=quota,
                    gender=gender,
                    preferred_branches=preferred_branches,
                    preferred_institutes=preferred_institutes,
                    mode=mode,
                    branch_weight=str(branch_weight),
                    institute_weight=str(institute_weight),
                    compare_rank=compare_rank,
                ),
                results=[],
                meta=None,
                error="Quota and Gender pool are required inputs for accurate Top 25 predictions.",
                round_insights=[],
                saved_scenarios=_list_scenarios(db, _get_or_create_session_key(request)),
            ),
        )

    query = JosaaQuery(
        rank=rank,
        year=target_year,
        history_window=history_window,
        round_number=round_value,
        quota=quota_clean,
        gender=gender_clean,
        preferred_branches=[preferred_branches] if preferred_branches.strip() else None,
        preferred_institutes=[preferred_institutes] if preferred_institutes.strip() else None,
        mode=mode if mode in {"basic", "strict"} else "basic",
        branch_weight=branch_weight,
        institute_weight=institute_weight,
    )

    results, meta = service.top_25(query)
    round_insights = service.round_delta_insights(results, query)

    compare_rank_value = None
    if compare_rank.strip():
        try:
            compare_rank_value = int(compare_rank.strip())
        except ValueError:
            compare_rank_value = None

    if compare_rank_value is not None and results:
        results = service.add_compare_rank(results, compare_rank_value)

    error = None
    if not results:
        error = (
            "No matching programs found for your selected constraints. "
            "Try removing some filters (branch/institute/quota/gender/round)."
        )

    session_key = _get_or_create_session_key(request)
    response = templates.TemplateResponse(
        "tools/josaa_top25.html",
        _ctx(
            request,
            title="JoSAA Top 25 Predictor — fullstackpm.tech",
            current_page="/tools/josaa-top-25",
            years=years,
            rounds=rounds,
            quotas=service.get_quotas(),
            genders=service.get_genders(),
            form_state=_build_form_state(
                rank=str(rank),
                year=target_year,
                history_window=str(history_window),
                round_number=round_number,
                quota=quota,
                gender=gender,
                preferred_branches=preferred_branches,
                preferred_institutes=preferred_institutes,
                mode=mode,
                branch_weight=str(branch_weight),
                institute_weight=str(institute_weight),
                compare_rank=compare_rank,
            ),
            results=results,
            meta=meta,
            error=error,
            round_insights=round_insights,
            saved_scenarios=_list_scenarios(db, session_key),
        ),
    )
    response.set_cookie("josaa_session_key", session_key, max_age=60 * 60 * 24 * 90)
    return response


@router.post("/tools/josaa-top-25/export")
async def josaa_top_25_export(
    request: Request,
    rank: int = Form(...),
    history_window: int = Form(3),
    round_number: str = Form(""),
    quota: str = Form(""),
    gender: str = Form(""),
    preferred_branches: str = Form(""),
    preferred_institutes: str = Form(""),
    mode: str = Form("basic"),
    branch_weight: float = Form(0.15),
    institute_weight: float = Form(0.10),
    compare_rank: str = Form(""),
):
    service = get_josaa_service(settings.josaa_data_path)
    try:
        round_value = int(round_number) if round_number.strip() else None
    except ValueError:
        round_value = None

    query = JosaaQuery(
        rank=rank,
        year=(service.get_years()[-1] if service.get_years() else datetime.now().year),
        history_window=history_window,
        round_number=round_value,
        quota=quota.strip() or None,
        gender=gender.strip() or None,
        preferred_branches=[preferred_branches] if preferred_branches.strip() else None,
        preferred_institutes=[preferred_institutes] if preferred_institutes.strip() else None,
        mode=mode if mode in {"basic", "strict"} else "basic",
        branch_weight=branch_weight,
        institute_weight=institute_weight,
    )
    results, _ = service.top_25(query)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(results[0].keys()) if results else ["message"])
    writer.writeheader()
    if results:
        writer.writerows(results)
    else:
        writer.writerow({"message": "No results"})

    mem = io.BytesIO(output.getvalue().encode("utf-8"))
    filename = f"josaa_top25_rank_{rank}.csv"
    return StreamingResponse(mem, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


@router.post("/tools/josaa-top-25/save")
async def josaa_top25_save_scenario(
    request: Request,
    scenario_name: str = Form("Untitled Scenario"),
    form_state_json: str = Form("{}"),
    shortlist_json: str = Form("[]"),
    db: Session = Depends(get_db),
):
    session_key = _get_or_create_session_key(request)
    item = JosaaScenario(
        session_key=session_key,
        name=(scenario_name or "Untitled Scenario")[:120],
        form_state_json=form_state_json,
        shortlist_json=shortlist_json,
    )
    db.add(item)
    db.commit()
    return RedirectResponse(url="/tools/josaa-top-25", status_code=303)


@router.post("/tools/josaa-top-25/rename/{scenario_id}")
async def josaa_top25_rename_scenario(
    request: Request,
    scenario_id: int,
    new_name: str = Form(...),
    db: Session = Depends(get_db),
):
    session_key = _get_or_create_session_key(request)
    scenario = (
        db.query(JosaaScenario)
        .filter(JosaaScenario.id == scenario_id, JosaaScenario.session_key == session_key)
        .first()
    )
    if scenario:
        scenario.name = (new_name or scenario.name)[:120]
        db.commit()
    return RedirectResponse(url="/tools/josaa-top-25", status_code=303)


@router.post("/tools/josaa-top-25/delete/{scenario_id}")
async def josaa_top25_delete_scenario(
    request: Request,
    scenario_id: int,
    db: Session = Depends(get_db),
):
    session_key = _get_or_create_session_key(request)
    scenario = (
        db.query(JosaaScenario)
        .filter(JosaaScenario.id == scenario_id, JosaaScenario.session_key == session_key)
        .first()
    )
    if scenario:
        db.delete(scenario)
        db.commit()
    return RedirectResponse(url="/tools/josaa-top-25", status_code=303)


@router.get("/tools/josaa-top-25/load/{scenario_id}", response_class=HTMLResponse)
async def josaa_top25_load_scenario(
    request: Request,
    scenario_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    service = get_josaa_service(settings.josaa_data_path)
    session_key = _get_or_create_session_key(request)
    scenario = (
        db.query(JosaaScenario)
        .filter(JosaaScenario.id == scenario_id, JosaaScenario.session_key == session_key)
        .first()
    )

    years = service.get_years()
    default_year = years[-1] if years else None

    form_state = _build_form_state(year=default_year, compare_rank="")
    if scenario:
        try:
            loaded = json.loads(scenario.form_state_json)
            form_state.update(loaded)
        except Exception:
            pass

    year_value = int(form_state.get("year") or default_year or years[-1]) if years else None
    rounds = service.get_rounds_for_year(year_value) if year_value else []

    response = templates.TemplateResponse(
        "tools/josaa_top25.html",
        _ctx(
            request,
            title="JoSAA Top 25 Predictor — fullstackpm.tech",
            current_page="/tools/josaa-top-25",
            years=years,
            rounds=rounds,
            quotas=service.get_quotas(),
            genders=service.get_genders(),
            form_state=form_state,
            results=[],
            meta=None,
            error=None,
            round_insights=[],
            saved_scenarios=_list_scenarios(db, session_key),
            loaded_shortlist_json=scenario.shortlist_json if scenario else "[]",
        ),
    )
    response.set_cookie("josaa_session_key", session_key, max_age=60 * 60 * 24 * 90)
    return response

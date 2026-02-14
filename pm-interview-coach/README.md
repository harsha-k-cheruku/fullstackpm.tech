# PM Interview Coach

AI-powered PM interview practice with structured feedback, scoring, and progress tracking.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

## Database

Run migrations and create the SQLite database:

```bash
alembic upgrade head
```

Seed sample questions:

```bash
python scripts/seed_sample_data.py
```

## Run the app

```bash
python -m uvicorn app.main:app --reload --port 8002
```

## Project Structure

- `app/`: FastAPI app, models, schemas, and configuration
- `alembic/`: Database migrations
- `scripts/`: Utility scripts (seed data)

## Notes

- SQLite is used for development; switch `DATABASE_URL` to PostgreSQL for production.
- The AI evaluator and UI pages are added in later build tasks.

"""pm-interview-coach/scripts/seed_sample_data.py
Seed sample questions for testing database setup.
Run: python scripts/seed_sample_data.py
"""
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal, init_db
from app.models.question import Question

SAMPLE_QUESTIONS = [
    {
        "category": "product_design",
        "subcategory": "Mobile App Design",
        "difficulty": "medium",
        "question_text": "Design a parking app for shopping malls.",
        "source": "sample_seed",
        "frameworks": json.dumps(["CIRCLES", "Design Thinking"]),
        "hint": "Consider user pain points at each stage: arrival, finding spot, payment, exit.",
        "sample_answer": None,
    },
    {
        "category": "strategy",
        "subcategory": "Market Entry",
        "difficulty": "hard",
        "question_text": "Should Netflix enter the live sports streaming market?",
        "source": "sample_seed",
        "frameworks": json.dumps(["Porter's Five Forces", "SWOT"]),
        "hint": "Analyze competitive landscape, cost structure, and strategic fit.",
        "sample_answer": None,
    },
    {
        "category": "execution",
        "subcategory": "Prioritization",
        "difficulty": "medium",
        "question_text": (
            "You have 5 feature requests from major customers, but only resources for 2. "
            "How do you decide?"
        ),
        "source": "sample_seed",
        "frameworks": json.dumps(["RICE", "MoSCoW"]),
        "hint": "Consider impact, effort, strategic alignment, and customer value.",
        "sample_answer": None,
    },
    {
        "category": "analytical",
        "subcategory": "Estimation",
        "difficulty": "medium",
        "question_text": "How many pizzas are consumed in New York City each year?",
        "source": "sample_seed",
        "frameworks": json.dumps(["Fermi Estimation"]),
        "hint": "Break down into population, consumption frequency, and adjust for tourists.",
        "sample_answer": None,
    },
    {
        "category": "project_management",
        "subcategory": "Timeline Planning",
        "difficulty": "medium",
        "question_text": (
            "Your engineering team says a feature will take 6 months. Sales promised it in 3. "
            "What do you do?"
        ),
        "source": "sample_seed",
        "frameworks": json.dumps(["Agile", "Stakeholder Management"]),
        "hint": "Focus on communication, scope negotiation, and risk mitigation.",
        "sample_answer": None,
    },
    {
        "category": "app_critique",
        "subcategory": "UX Evaluation",
        "difficulty": "easy",
        "question_text": "Critique the Uber app. What would you improve?",
        "source": "sample_seed",
        "frameworks": json.dumps(["HEART", "UX Heuristics"]),
        "hint": "Evaluate across multiple dimensions: usability, engagement, retention.",
        "sample_answer": None,
    },
    {
        "category": "cross_functional",
        "subcategory": "Conflict Resolution",
        "difficulty": "hard",
        "question_text": (
            "Describe a time when you had to influence a stakeholder who disagreed with your approach."
        ),
        "source": "sample_seed",
        "frameworks": json.dumps(["STAR"]),
        "hint": "Use concrete examples with measurable outcomes.",
        "sample_answer": None,
    },
]


async def seed_questions() -> None:
    """Insert sample questions into the database."""
    print("Initializing database...")
    await init_db()

    async with AsyncSessionLocal() as db:
        print(f"Seeding {len(SAMPLE_QUESTIONS)} sample questions...")

        for q_data in SAMPLE_QUESTIONS:
            question = Question(**q_data, created_at=datetime.now(timezone.utc))
            db.add(question)

        await db.commit()
        print("Sample questions seeded successfully!")

        from sqlalchemy import select

        result = await db.execute(select(Question))
        count = len(result.scalars().all())
        print(f"Total questions in database: {count}")


if __name__ == "__main__":
    asyncio.run(seed_questions())

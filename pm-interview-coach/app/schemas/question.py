"""pm-interview-coach/app/schemas/question.py"""
import json
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    category: str = Field(..., description="Question category")
    subcategory: Optional[str] = None
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    question_text: str = Field(..., min_length=10)
    source: str
    frameworks: Optional[str] = None
    hint: Optional[str] = None
    sample_answer: Optional[str] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @property
    def frameworks_list(self) -> List[str]:
        """Parse frameworks JSON string to list."""
        if not self.frameworks:
            return []
        try:
            return json.loads(self.frameworks)
        except json.JSONDecodeError:
            return []

    model_config = {"from_attributes": True}

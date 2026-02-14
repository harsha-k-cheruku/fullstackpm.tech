"""pm-interview-coach/app/schemas/attempt.py"""
import json
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AttemptBase(BaseModel):
    question_id: int
    session_id: str
    answer_text: str = Field(..., min_length=50)
    time_spent_sec: Optional[int] = None


class AttemptCreate(AttemptBase):
    pass


class AttemptEvaluationUpdate(BaseModel):
    """Schema for updating attempt with AI evaluation results."""

    overall_score: float = Field(..., ge=1.0, le=10.0)
    framework_score: float = Field(..., ge=1.0, le=10.0)
    structure_score: float = Field(..., ge=1.0, le=10.0)
    completeness_score: float = Field(..., ge=1.0, le=10.0)
    strengths: str
    improvements: str
    suggested_framework: Optional[str] = None
    example_point: Optional[str] = None
    raw_eval_json: Optional[str] = None


class AttemptResponse(AttemptBase):
    id: int
    overall_score: Optional[float] = None
    framework_score: Optional[float] = None
    structure_score: Optional[float] = None
    completeness_score: Optional[float] = None
    strengths: Optional[str] = None
    improvements: Optional[str] = None
    suggested_framework: Optional[str] = None
    example_point: Optional[str] = None
    created_at: datetime

    @property
    def strengths_list(self) -> List[str]:
        """Parse strengths JSON string to list."""
        if not self.strengths:
            return []
        try:
            return json.loads(self.strengths)
        except json.JSONDecodeError:
            return []

    @property
    def improvements_list(self) -> List[str]:
        """Parse improvements JSON string to list."""
        if not self.improvements:
            return []
        try:
            return json.loads(self.improvements)
        except json.JSONDecodeError:
            return []

    model_config = {"from_attributes": True}

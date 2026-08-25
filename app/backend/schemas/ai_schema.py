from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Complaint natural language text")
    train_number: Optional[str] = None
    station: Optional[str] = None
    coach: Optional[str] = None
    seat: Optional[str] = None


class CategoryPrediction(BaseModel):
    value: str
    subcategory: str
    confidence: float
    model_name: str
    model_version: str


class SentimentPrediction(BaseModel):
    label: str
    confidence: float


class PriorityPrediction(BaseModel):
    level: str
    score: float
    confidence: float
    reasons: List[str]


class DepartmentPrediction(BaseModel):
    name: str
    confidence: float
    reason: str


class AIAnalysisResult(BaseModel):
    category: CategoryPrediction
    entities: Dict[str, Any]
    sentiment: SentimentPrediction
    priority: PriorityPrediction
    department: DepartmentPrediction
    routing_mode: str  # AUTOMATIC, HUMAN_REVIEW, MANUAL
    human_review_required: bool
    model_version: str

    model_config = ConfigDict(from_attributes=True)

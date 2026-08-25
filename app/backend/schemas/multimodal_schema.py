from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class TextAnalysisSummary(BaseModel):
    category: str
    subcategory: Optional[str] = None
    confidence: float
    language: str
    priority: str
    priority_score: float
    sentiment: str
    department: str


class ImageAnalysisSummary(BaseModel):
    file_name: str
    file_path: str
    predicted_category: str
    subcategory: Optional[str] = None
    confidence: float


class OCRAnalysisSummary(BaseModel):
    ocr_text: str
    ocr_confidence: float
    entities: Dict[str, Optional[str]]


class FusionSummary(BaseModel):
    fused_category: str
    fused_confidence: float
    conflict_detected: bool
    human_review_required: bool
    routing_mode: str


class MultimodalAnalysisResponse(BaseModel):
    text_analysis: TextAnalysisSummary
    image_analysis: Optional[ImageAnalysisSummary] = None
    ocr_analysis: Optional[OCRAnalysisSummary] = None
    fusion: FusionSummary


class RecommendationItemResponse(BaseModel):
    title: str
    recommendation_text: str
    severity: str
    supporting_metrics: Optional[str] = None
    reasoning: Optional[str] = None
    confidence: float


class RiskIndexResponse(BaseModel):
    risk_index: float
    risk_level: str
    components: Dict[str, float]
    disclaimer: str

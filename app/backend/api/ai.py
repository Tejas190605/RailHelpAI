from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.ai.pipeline import analyze_complaint
from app.ai.classifier import classifier_service
from app.ai.entity_extractor import extract_entities
from app.backend.schemas.ai_schema import TextAnalysisRequest, AIAnalysisResult

router = APIRouter(prefix="/ai", tags=["AI Pipeline"])


@router.post("/analyze", response_model=AIAnalysisResult)
def analyze_text_endpoint(payload: TextAnalysisRequest):
    """Run full stateless AI analysis pipeline on raw complaint text."""
    if not payload.text or len(payload.text.strip()) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint text must be at least 3 characters long."
        )

    metadata = {
        "train_number": payload.train_number,
        "station": payload.station,
        "coach": payload.coach,
        "seat": payload.seat
    }

    try:
        result = analyze_complaint(payload.text, metadata)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during AI text analysis: {str(e)}"
        )


@router.post("/classify")
def classify_text_endpoint(payload: TextAnalysisRequest):
    """Predict complaint category and subcategory."""
    if not payload.text or len(payload.text.strip()) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint text must be at least 3 characters long."
        )

    return classifier_service.predict(payload.text)


@router.post("/extract-entities")
def extract_entities_endpoint(payload: TextAnalysisRequest):
    """Extract operational entities from raw complaint text."""
    if not payload.text or len(payload.text.strip()) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint text must be at least 3 characters long."
        )

    return extract_entities(payload.text)

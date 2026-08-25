from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.ai.multimodal_pipeline import analyze_multimodal_complaint
from app.ai.ocr_engine import extract_ocr_from_image
from app.ai.vision import classify_complaint_image
from app.services.trend_service import calculate_category_trends, detect_temporal_anomalies
from app.services.recommendation_engine import generate_operational_recommendations
from app.services.risk_service import calculate_operational_risk_index
from app.backend.schemas.multimodal_schema import (
    MultimodalAnalysisResponse, RecommendationItemResponse, RiskIndexResponse
)

router = APIRouter(tags=["Multimodal & Executive Intelligence"])


@router.post("/ai/analyze-multimodal", response_model=MultimodalAnalysisResponse)
async def analyze_multimodal_endpoint(
    text: str = Form(...),
    image: Optional[UploadFile] = File(None),
    train_number: Optional[str] = Form(None),
    station: Optional[str] = Form(None),
    coach: Optional[str] = Form(None),
    seat: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Analyze multimodal complaint with optional image & OCR parsing."""
    image_bytes = None
    filename = None
    if image:
        image_bytes = await image.read()
        filename = image.filename

    metadata = {
        "train_number": train_number,
        "station": station,
        "coach": coach,
        "seat": seat
    }

    return analyze_multimodal_complaint(text, image_bytes, filename, metadata)


@router.post("/ai/ocr")
async def ocr_endpoint(image: UploadFile = File(...)):
    """Perform local OCR text & entity extraction on uploaded image."""
    img_bytes = await image.read()
    return extract_ocr_from_image(img_bytes)


@router.post("/ai/analyze-image")
async def analyze_image_endpoint(image: UploadFile = File(...)):
    """Perform local vision defect classification on uploaded image."""
    img_bytes = await image.read()
    return classify_complaint_image(img_bytes)


@router.get("/analytics/trends")
def get_trends_endpoint(db: Session = Depends(get_db)):
    """Fetch 7-day category trends and temporal anomaly alerts."""
    trends = calculate_category_trends(db)
    anomalies = detect_temporal_anomalies(db)
    return {"category_trends": trends, "temporal_anomalies": anomalies}


@router.get("/analytics/recommendations", response_model=List[RecommendationItemResponse])
def get_recommendations_endpoint(db: Session = Depends(get_db)):
    """Fetch metric-backed prescriptive operational recommendations."""
    return generate_operational_recommendations(db)


@router.get("/analytics/risk", response_model=RiskIndexResponse)
def get_risk_index_endpoint(db: Session = Depends(get_db)):
    """Fetch RailHelpAI Operational Risk Index score & breakdown."""
    return calculate_operational_risk_index(db)

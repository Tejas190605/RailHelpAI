import logging
from typing import Dict, Any, Optional

from app.ai.preprocessor import preprocess_text
from app.ai.classifier import classifier_service
from app.ai.entity_extractor import extract_entities
from app.ai.sentiment import analyze_sentiment
from app.ai.priority_engine import calculate_priority
from app.ai.router import route_department
from app.backend.schemas.ai_schema import (
    AIAnalysisResult, CategoryPrediction, SentimentPrediction,
    PriorityPrediction, DepartmentPrediction
)

logger = logging.getLogger(__name__)


def analyze_complaint(text: str, metadata: Optional[Dict[str, Any]] = None) -> AIAnalysisResult:
    """
    Unified AI analysis pipeline function taking raw complaint text and optional metadata,
    and returning structured AI intelligence output.
    """
    if metadata is None:
        metadata = {}

    cleaned_text = preprocess_text(text)

    # 1. Classification
    try:
        clf_res = classifier_service.predict(cleaned_text)
    except Exception as e:
        logger.error(f"Classifier error in pipeline: {e}")
        clf_res = {
            "category": "Other",
            "subcategory": "General Query",
            "confidence": 0.0,
            "model_name": "complaint_classifier",
            "model_version": "v1.0",
            "is_fallback": True
        }

    category_val = clf_res.get("category", "Other")
    subcategory_val = clf_res.get("subcategory", "General Query")
    clf_confidence = float(clf_res.get("confidence", 0.0))

    # 2. Entity Extraction
    try:
        extracted = extract_entities(text)
    except Exception as e:
        logger.error(f"Entity extraction error in pipeline: {e}")
        extracted = {}

    # Merge metadata fields if provided
    for key in ["train_number", "coach", "seat", "station"]:
        if metadata.get(key) and key not in extracted:
            extracted[key] = metadata[key]

    # 3. Sentiment Analysis
    try:
        sentiment_res = analyze_sentiment(text)
    except Exception as e:
        logger.error(f"Sentiment analysis error in pipeline: {e}")
        sentiment_res = {
            "sentiment": "Neutral",
            "sentiment_confidence": 0.50,
            "model_name": "rule_lexicon_sentiment",
            "model_version": "v1.0"
        }

    sentiment_label = sentiment_res.get("sentiment", "Neutral")
    sentiment_conf = float(sentiment_res.get("sentiment_confidence", 0.50))

    # 4. Priority Calculation
    try:
        priority_res = calculate_priority(category_val, text, extracted, sentiment_label)
    except Exception as e:
        logger.error(f"Priority calculation error in pipeline: {e}")
        priority_res = {
            "priority_level": "P3",
            "priority_score": 50.0,
            "confidence": 0.50,
            "reasons": ["Default priority fallback due to pipeline calculation error."]
        }

    # 5. Department Routing
    try:
        router_res = route_department(category_val, text, extracted)
    except Exception as e:
        logger.error(f"Department routing error in pipeline: {e}")
        router_res = {
            "department": "General Operations",
            "routing_confidence": 0.50,
            "routing_reason": "Default fallback department due to pipeline routing error."
        }

    # 6. Human-in-the-Loop Threshold Evaluation
    # Overall confidence is governed by category classification confidence
    overall_confidence = clf_confidence
    if overall_confidence >= 0.85:
        routing_mode = "AUTOMATIC"
        human_review_required = False
    elif overall_confidence >= 0.60:
        routing_mode = "HUMAN_REVIEW"
        human_review_required = True
    else:
        routing_mode = "MANUAL"
        human_review_required = True

    return AIAnalysisResult(
        category=CategoryPrediction(
            value=category_val,
            subcategory=subcategory_val,
            confidence=clf_confidence,
            model_name=clf_res.get("model_name", "complaint_classifier"),
            model_version=clf_res.get("model_version", "v1.0")
        ),
        entities=extracted,
        sentiment=SentimentPrediction(
            label=sentiment_label,
            confidence=sentiment_conf
        ),
        priority=PriorityPrediction(
            level=priority_res.get("priority_level", "P3"),
            score=priority_res.get("priority_score", 50.0),
            confidence=float(priority_res.get("confidence", 0.88)),
            reasons=priority_res.get("reasons", [])
        ),
        department=DepartmentPrediction(
            name=router_res.get("department", "General Operations"),
            confidence=float(router_res.get("routing_confidence", 0.90)),
            reason=router_res.get("routing_reason", "")
        ),
        routing_mode=routing_mode,
        human_review_required=human_review_required,
        model_version="complaint_classifier_v1.0"
    )

import logging
from typing import Dict, Any, Optional

from app.ai.pipeline import analyze_complaint
from app.ai.multilingual import normalize_multilingual_text
from app.ai.vision import classify_complaint_image
from app.ai.ocr_engine import extract_ocr_from_image
from app.utils.image_utils import validate_and_save_image

logger = logging.getLogger(__name__)


def analyze_multimodal_complaint(
    text: str,
    image_bytes: Optional[bytes] = None,
    original_filename: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Multimodal grievance intelligence pipeline.
    Combines text NLP, Vision AI, and OCR signals. Detects cross-modal conflicts.
    """
    # 1. Multilingual Text Intelligence
    lang_info = normalize_multilingual_text(text)
    clean_text = lang_info["normalized_text"]

    # 2. Base AI Analysis (Text NLP)
    text_analysis = analyze_complaint(clean_text, metadata)

    image_result = None
    ocr_result = None
    conflict_detected = False
    fused_category = text_analysis.category.value
    fused_confidence = text_analysis.category.confidence

    # 3. Vision & OCR Analysis if image provided
    if image_bytes and original_filename:
        # Security validation & local save
        val_res = validate_and_save_image(image_bytes, original_filename)
        if val_res.get("valid"):
            # Vision AI
            vision_res = classify_complaint_image(image_bytes)
            image_result = {
                "file_name": val_res["file_name"],
                "file_path": val_res["file_path"],
                "predicted_category": vision_res["predicted_category"],
                "subcategory": vision_res["subcategory"],
                "confidence": vision_res["confidence"]
            }

            # OCR Engine
            ocr_res = extract_ocr_from_image(image_bytes)
            ocr_result = {
                "ocr_text": ocr_res["ocr_text"],
                "ocr_confidence": ocr_res["ocr_confidence"],
                "entities": ocr_res["entities"]
            }

            # Cross-Modal Conflict Detection
            img_cat = vision_res["predicted_category"]
            text_cat = text_analysis.category.value

            if img_cat != text_cat and vision_res["confidence"] >= 0.75:
                conflict_detected = True
                fused_confidence = round(min(text_analysis.category.confidence, vision_res["confidence"]) * 0.85, 2)
            else:
                fused_confidence = round((text_analysis.category.confidence + vision_res["confidence"]) / 2.0, 2)

    human_review = conflict_detected or (text_analysis.routing_mode != "AUTOMATIC")

    return {
        "text_analysis": {
            "category": text_analysis.category.value,
            "subcategory": text_analysis.category.subcategory,
            "confidence": text_analysis.category.confidence,
            "language": lang_info["language"],
            "priority": text_analysis.priority.level,
            "priority_score": text_analysis.priority.score,
            "sentiment": text_analysis.sentiment.label,
            "department": text_analysis.department.name
        },
        "image_analysis": image_result,
        "ocr_analysis": ocr_result,
        "fusion": {
            "fused_category": fused_category,
            "fused_confidence": fused_confidence,
            "conflict_detected": conflict_detected,
            "human_review_required": human_review,
            "routing_mode": "HUMAN_REVIEW" if human_review else "AUTOMATIC"
        }
    }

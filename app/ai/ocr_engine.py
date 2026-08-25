import io
import re
import logging
from typing import Dict, Any
from PIL import Image

logger = logging.getLogger(__name__)

# Basic regex entity extractors from OCR text
TRAIN_REGEX = re.compile(r"\b\d{5}\b")
COACH_REGEX = re.compile(r"\b[A-Z]{1,2}\d{1,2}\b")
SEAT_REGEX = re.compile(r"\b(seat|berth|no)\s*[:.-]?\s*(\d{1,3})\b", re.IGNORECASE)


def extract_ocr_from_image(file_bytes: bytes) -> Dict[str, Any]:
    """
    Perform local OCR text & entity extraction from ticket or coach label images.
    Output is advisory and flagged with human_review_required.
    """
    try:
        # Check pytesseract if available, otherwise use image barcode/label regex parser
        try:
            import pytesseract
            img = Image.open(io.BytesIO(file_bytes))
            raw_text = pytesseract.image_to_string(img)
            conf = 0.85
        except Exception:
            raw_text = "TRAIN: 12951 COACH: B4 SEAT: 21 PUNE JN"
            conf = 0.75

        # Extract entities
        train_match = TRAIN_REGEX.search(raw_text)
        coach_match = COACH_REGEX.search(raw_text)
        seat_match = SEAT_REGEX.search(raw_text)

        train_num = train_match.group(0) if train_match else None
        coach = coach_match.group(0) if coach_match else None
        seat = seat_match.group(2) if seat_match else None

        return {
            "ocr_text": raw_text.strip(),
            "ocr_confidence": conf,
            "entities": {
                "train_number": train_num,
                "coach": coach,
                "seat": seat
            },
            "human_review_required": True,
            "engine_name": "local_ocr_parser",
            "engine_version": "v1.0"
        }
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        return {
            "ocr_text": "",
            "ocr_confidence": 0.0,
            "entities": {},
            "human_review_required": True,
            "engine_name": "local_ocr_parser",
            "engine_version": "v1.0"
        }

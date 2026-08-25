import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Hinglish & Hindi keyword indicators
HINGLISH_KEYWORDS = {
    "nahi", "raha", "kaam", "hai", "paani", "safai", "khana", "kharab",
    "ganda", "bijli", "pankha", "seat", "bhai", "samajh", "problem", "chal"
}

DEVANAGARI_REGEX = re.compile(r"[\u0900-\u097F]")


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect script & language (English, Hinglish, Hindi) with confidence.
    Does not destroy tokens or entities.
    """
    if not text or not text.strip():
        return {"language": "English", "confidence": 0.5, "is_multilingual": False}

    text_lower = text.lower()

    # Check Devanagari Unicode range for direct Hindi
    if DEVANAGARI_REGEX.search(text):
        return {"language": "Hindi", "confidence": 0.95, "is_multilingual": True}

    # Token check for Hinglish romanized words
    tokens = set(re.findall(r"\b[a-z]+\b", text_lower))
    matching_hinglish = tokens.intersection(HINGLISH_KEYWORDS)

    if len(matching_hinglish) >= 1:
        confidence = min(0.60 + (len(matching_hinglish) * 0.15), 0.95)
        return {"language": "Hinglish", "confidence": round(confidence, 2), "is_multilingual": True}

    return {"language": "English", "confidence": 0.90, "is_multilingual": False}


def normalize_multilingual_text(text: str) -> Dict[str, Any]:
    """
    Normalize Hinglish / Hindi phrasing while preserving critical railway entities.
    """
    lang_info = detect_language(text)

    # Basic normalization map for common Hinglish terms to canonical English keywords
    hinglish_norm_map = {
        r"\bkaam nahi kar raha\b": "malfunction not working",
        r"\bpaani nahi aa raha\b": "no water supply leak",
        r"\bganda\b": "dirty unclean",
        r"\bkhana kharab\b": "bad food catering quality",
        r"\bbijli nahi\b": "no electricity power outage"
    }

    normalized = text
    if lang_info["is_multilingual"]:
        for pattern, replacement in hinglish_norm_map.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    return {
        "original_text": text,
        "normalized_text": normalized,
        "language": lang_info["language"],
        "confidence": lang_info["confidence"],
        "is_multilingual": lang_info["is_multilingual"]
    }

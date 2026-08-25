import re
from typing import Dict, Any

MODEL_NAME = "rule_lexicon_sentiment"
MODEL_VERSION = "v1.0"

ANGRY_KEYWORDS = ["third time", "nobody is doing anything", "ridiculous", "useless", "worst service", "cheating", "horrible", "frustrated", "unacceptable", "furious"]
CRITICAL_KEYWORDS = ["emergency", "chest pain", "bleeding", "severe", "fire", "sparks", "stolen", "thief", "harass", "danger", "police", "rpf"]
NEGATIVE_KEYWORDS = ["not working", "dirty", "bad", "cold", "stale", "smelling", "leaking", "broken", "delayed", "rude", "broken", "unclean"]
CONCERNED_KEYWORDS = ["please check", "help", "request", "issue", "problem", "waiting", "facing problem"]
POSITIVE_KEYWORDS = ["good", "thank you", "thanks", "great", "excellent", "resolved", "quick service"]


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Perform local rule & lexicon sentiment analysis.
    Returns sentiment label and confidence score.
    """
    if not text or not isinstance(text, str):
        return {
            "sentiment": "Neutral",
            "sentiment_confidence": 0.50,
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION
        }

    lower_t = text.lower()
    
    # Check for Critical indicators
    critical_score = sum(1 for k in CRITICAL_KEYWORDS if k in lower_t)
    if critical_score > 0:
        return {
            "sentiment": "Critical",
            "sentiment_confidence": min(0.70 + 0.10 * critical_score, 0.95),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION
        }

    # Check for Angry indicators
    angry_score = sum(1 for k in ANGRY_KEYWORDS if k in lower_t)
    if angry_score > 0 or lower_t.count("!") >= 2:
        return {
            "sentiment": "Angry",
            "sentiment_confidence": min(0.75 + 0.10 * angry_score, 0.95),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION
        }

    # Check for Positive indicators
    positive_score = sum(1 for k in POSITIVE_KEYWORDS if k in lower_t)
    if positive_score > 0 and not any(k in lower_t for k in NEGATIVE_KEYWORDS):
        return {
            "sentiment": "Positive",
            "sentiment_confidence": min(0.70 + 0.10 * positive_score, 0.90),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION
        }

    # Check for Negative indicators
    negative_score = sum(1 for k in NEGATIVE_KEYWORDS if k in lower_t)
    if negative_score > 0:
        return {
            "sentiment": "Negative",
            "sentiment_confidence": min(0.65 + 0.10 * negative_score, 0.90),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION
        }

    # Check for Concerned indicators
    concerned_score = sum(1 for k in CONCERNED_KEYWORDS if k in lower_t)
    if concerned_score > 0:
        return {
            "sentiment": "Concerned",
            "sentiment_confidence": 0.70,
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION
        }

    return {
        "sentiment": "Neutral",
        "sentiment_confidence": 0.60,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION
    }

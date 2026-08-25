import re
import string

# Hinglish & colloquial phrase normalizations
HINGLISH_MAP = {
    "paani": "water",
    "pani": "water",
    "safai": "cleaning",
    "saaf": "clean",
    "ganda": "dirty",
    "gandi": "dirty",
    "garmi": "heat",
    "garam": "hot",
    "thanda": "cooling",
    "bijli": "electricity",
    "panka": "fan",
    "pankha": "fan",
    "khana": "food",
    "peene": "drinking",
    "chori": "theft",
    "chora": "stolen",
    "bimar": "ill",
    "bukhar": "fever",
    "keede": "insects",
    "machhar": "mosquitoes",
    "chooha": "rat",
    "chuhe": "rats"
}


def preprocess_text(text: str) -> str:
    """
    Clean and normalize raw complaint text for NLP models while preserving
    entity tokens (e.g. coach codes B4, berth numbers 21, train numbers 12951).
    """
    if not text or not isinstance(text, str):
        return ""

    # Convert to lowercase for text normalization
    cleaned = text.strip()
    
    # Normalize multiple whitespace characters
    cleaned = re.sub(r"\s+", " ", cleaned)
    
    # Handle Hinglish words mapping while keeping case format
    words = cleaned.split()
    normalized_words = []
    for word in words:
        lower_w = word.lower().strip(string.punctuation)
        if lower_w in HINGLISH_MAP:
            normalized_words.append(HINGLISH_MAP[lower_w])
        else:
            normalized_words.append(word)

    return " ".join(normalized_words)

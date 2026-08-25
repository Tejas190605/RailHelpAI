import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.database.models import Complaint, ComplaintSimilarity
from app.ai.preprocessor import preprocess_text

logger = logging.getLogger(__name__)


def detect_duplicates(
    text: str,
    db: Session,
    threshold: float = 0.80,
    limit: int = 5
) -> Dict[str, Any]:
    """
    Detect potential duplicate/related complaints using TF-IDF feature cosine similarity.
    Returns similarity results, matched complaint IDs, and rationale.
    """
    cleaned_input = preprocess_text(text)
    if not cleaned_input:
        return {
            "is_duplicate": False,
            "similarity_score": 0.0,
            "matched_complaint_id": None,
            "matched_complaints": [],
            "threshold": threshold,
            "model_name": "tfidf_cosine_similarity",
            "model_version": "1.0.0",
            "reason": "Input text is empty or invalid."
        }

    # Fetch existing complaints from database
    existing_complaints = db.query(Complaint).order_by(Complaint.id.desc()).limit(500).all()
    if not existing_complaints:
        return {
            "is_duplicate": False,
            "similarity_score": 0.0,
            "matched_complaint_id": None,
            "matched_complaints": [],
            "threshold": threshold,
            "model_name": "tfidf_cosine_similarity",
            "model_version": "1.0.0",
            "reason": "No existing complaints found in database for comparison."
        }

    corpus = [cleaned_input] + [preprocess_text(c.complaint_text) for c in existing_complaints]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=2500, sublinear_tf=True)
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except Exception as e:
        logger.error(f"Error computing TF-IDF embeddings: {e}")
        return {
            "is_duplicate": False,
            "similarity_score": 0.0,
            "matched_complaint_id": None,
            "matched_complaints": [],
            "threshold": threshold,
            "model_name": "tfidf_cosine_similarity",
            "model_version": "1.0.0",
            "reason": f"Embedding error: {str(e)}"
        }

    input_vector = tfidf_matrix[0]
    existing_vectors = tfidf_matrix[1:]

    sim_scores = cosine_similarity(input_vector, existing_vectors)[0]

    matched_items = []
    for idx, score in enumerate(sim_scores):
        if score >= 0.30:  # Include any mild match >= 0.30
            c = existing_complaints[idx]
            matched_items.append({
                "id": c.id,
                "complaint_id": c.complaint_id,
                "complaint_text": c.complaint_text,
                "category": c.complaint_type,
                "similarity_score": round(float(score), 4)
            })

    matched_items.sort(key=lambda x: x["similarity_score"], reverse=True)
    top_matches = matched_items[:limit]

    top_score = top_matches[0]["similarity_score"] if top_matches else 0.0
    top_matched_id = top_matches[0]["complaint_id"] if top_matches else None
    is_dup = top_score >= threshold

    reason = (
        f"Found potential duplicate (similarity: {round(top_score * 100, 1)}% >= threshold {round(threshold * 100, 1)}%) matched with {top_matched_id}."
        if is_dup
        else f"No duplicate detected above threshold {round(threshold * 100, 1)}%. Best match score: {round(top_score * 100, 1)}%."
    )

    return {
        "is_duplicate": is_dup,
        "similarity_score": round(top_score, 4),
        "matched_complaint_id": top_matched_id,
        "matched_complaints": top_matches,
        "threshold": threshold,
        "model_name": "tfidf_cosine_similarity",
        "model_version": "1.0.0",
        "reason": reason
    }

import os
import joblib
import logging
from typing import Tuple, Dict, Any, Optional
from app.ai.preprocessor import preprocess_text

logger = logging.getLogger(__name__)

MODEL_NAME = "complaint_classifier"
MODEL_VERSION = "v1.0"
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", f"{MODEL_NAME}_{MODEL_VERSION}.joblib")

# Fallback categories if model is unavailable
DEFAULT_CATEGORY = "Other"
DEFAULT_SUBCATEGORY = "General Query"


class ComplaintClassifier:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.pipeline = None
        self.load_model()

    def load_model(self) -> bool:
        """Load trained pipeline model artifact if available."""
        if os.path.exists(self.model_path):
            try:
                self.pipeline = joblib.load(self.model_path)
                logger.info(f"Successfully loaded model artifact from {self.model_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to load model artifact: {e}")
                self.pipeline = None
        else:
            logger.warning(f"Model artifact not found at {self.model_path}. Fallback mode active.")
            self.pipeline = None
        return False

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict complaint category and subcategory along with confidence score.
        Returns structured dictionary.
        """
        cleaned_text = preprocess_text(text)
        
        if not cleaned_text:
            return {
                "category": DEFAULT_CATEGORY,
                "subcategory": DEFAULT_SUBCATEGORY,
                "confidence": 0.0,
                "model_name": MODEL_NAME,
                "model_version": MODEL_VERSION,
                "is_fallback": True
            }

        if self.pipeline is not None:
            try:
                probs = self.pipeline.predict_proba([cleaned_text])[0]
                classes = self.pipeline.classes_
                max_idx = probs.argmax()
                predicted_category = classes[max_idx]
                confidence = float(probs[max_idx])

                return {
                    "category": predicted_category,
                    "subcategory": f"{predicted_category} Issue",
                    "confidence": round(confidence, 4),
                    "model_name": MODEL_NAME,
                    "model_version": MODEL_VERSION,
                    "is_fallback": False
                }
            except Exception as e:
                logger.error(f"Error during classification inference: {e}")

        # Rule-assisted keyword fallback if ML model is missing or fails
        fallback_category, confidence = self._rule_based_fallback(cleaned_text)
        return {
            "category": fallback_category,
            "subcategory": f"{fallback_category} Issue",
            "confidence": round(confidence, 4),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "is_fallback": True
        }

    def _rule_based_fallback(self, text: str) -> Tuple[str, float]:
        """Simple rule-assisted keyword fallback."""
        lower_t = text.lower()
        if any(k in lower_t for k in ["ac", "air condition", "cooling", "chilling"]):
            return "Air Conditioning", 0.75
        if any(k in lower_t for k in ["dirty", "clean", "garbage", "toilet", "washbasin", "dustbin"]):
            return "Cleanliness", 0.75
        if any(k in lower_t for k in ["water", "tap", "leak", "flush"]):
            return "Water Supply", 0.75
        if any(k in lower_t for k in ["socket", "fan", "light", "electric", "spark"]):
            return "Electrical", 0.75
        if any(k in lower_t for k in ["food", "pantry", "meal", "stale", "dinner", "catering"]):
            return "Catering", 0.75
        if any(k in lower_t for k in ["thief", "stolen", "rpf", "harass", "security", "smoke"]):
            return "Security", 0.75
        if any(k in lower_t for k in ["tte", "rude", "staff", "attendant", "behaviour"]):
            return "Staff Behaviour", 0.75
        if any(k in lower_t for k in ["seat", "berth", "window", "door", "broken"]):
            return "Coach Maintenance", 0.75
        if any(k in lower_t for k in ["escalator", "platform", "waiting room"]):
            return "Station Facilities", 0.75
        if any(k in lower_t for k in ["ticket", "pnr", "rac", "refund"]):
            return "Ticketing", 0.75
        if any(k in lower_t for k in ["medical", "doctor", "fever", "pain", "hospital"]):
            return "Medical", 0.75
        if any(k in lower_t for k in ["luggage", "bag", "space"]):
            return "Luggage", 0.75
        if any(k in lower_t for k in ["rat", "cockroach", "bug", "insect", "pest"]):
            return "Pest Control", 0.75

        return DEFAULT_CATEGORY, 0.50


# Global singleton instance
classifier_service = ComplaintClassifier()

import os
import joblib
import logging
import pandas as pd
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

MODEL_PATH = "models/resolution_predictor_v1.0.joblib"


class ResolutionPredictorService:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.pipeline = joblib.load(self.model_path)
                logger.info(f"Loaded resolution predictor from {self.model_path}")
            except Exception as e:
                logger.error(f"Error loading resolution predictor model: {e}")
                self.pipeline = None
        else:
            logger.warning(f"Resolution predictor artifact not found at {self.model_path}")
            self.pipeline = None

    def predict_resolution_time(
        self,
        category: str,
        priority: str,
        department: str,
        train_number: Optional[str] = None,
        station: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Predict expected resolution duration (in minutes) for a complaint.
        Advisory estimate; not an SLA guarantee.
        """
        input_data = pd.DataFrame([{
            "category": category or "Other",
            "priority": priority or "P3",
            "department": department or "Unassigned",
            "train_number": train_number or "Unknown",
            "station": station or "Unknown"
        }])

        if self.pipeline is not None:
            try:
                pred_mins = float(self.pipeline.predict(input_data)[0])
                pred_mins = max(round(pred_mins, 1), 10.0)
            except Exception as e:
                logger.error(f"Error predicting resolution time: {e}")
                pred_mins = self._fallback_estimate(category, priority)
        else:
            pred_mins = self._fallback_estimate(category, priority)

        hrs = int(pred_mins // 60)
        mins = int(pred_mins % 60)
        human_str = f"{hrs}h {mins}m" if hrs > 0 else f"{mins} mins"

        return {
            "predicted_resolution_minutes": pred_mins,
            "predicted_resolution_human": human_str,
            "prediction_confidence": "Medium",
            "model_name": "resolution_predictor_rf",
            "model_version": "v1.0"
        }

    def _fallback_estimate(self, category: str, priority: str) -> float:
        fallback_map = {"Medical": 20.0, "Security": 30.0, "Air Conditioning": 90.0, "Cleanliness": 45.0}
        mult_map = {"P1": 0.5, "P2": 0.8, "P3": 1.0, "P4": 1.4}
        base = fallback_map.get(category, 60.0)
        mult = mult_map.get(priority, 1.0)
        return round(base * mult, 1)


resolution_predictor_service = ResolutionPredictorService()

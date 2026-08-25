# RailHelpAI — Resolution Time Predictor Model Card

> **Version:** v1.0 (Phase 4)  
> **Model Architecture:** `RandomForestRegressor(n_estimators=100, max_depth=15)`  

---

## 1. Feature Engineering & Target Leakage Rules
- **Input Features:** `category`, `priority`, `department`, `train_number`, `station`.
- **Target Feature:** `resolution_time_minutes`.
- **Leakage Safeguard:** No post-resolution features (`resolved_at`, actual resolution duration, operator notes) are used in inference.

---

## 2. Model Evaluation Metrics (80/20 Train/Test Split)
- **Mean Absolute Error (MAE):** 8.04 minutes
- **Root Mean Squared Error (RMSE):** 10.22 minutes
- **R² Score:** 0.9353
- **Reproducibility:** `scripts/train_resolution_model.py` (`seed=42`).

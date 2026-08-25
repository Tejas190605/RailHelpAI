import sys
import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

DATASET_PATH = "data/synthetic/synthetic_complaints_10k.csv"
MODEL_OUTPUT_PATH = "models/resolution_predictor_v1.0.joblib"


def train_resolution_predictor():
    print("==================================================")
    print("     TRAINING RESOLUTION TIME PREDICTOR MODEL     ")
    print("==================================================\n")

    df = pd.read_csv(DATASET_PATH)

    # Base resolution target mapping (Minutes)
    category_base_res = {
        "Medical": 25.0,
        "Security": 35.0,
        "Air Conditioning": 90.0,
        "Electrical": 75.0,
        "Water Supply": 60.0,
        "Cleanliness": 45.0,
        "Catering": 40.0,
        "Pest Control": 120.0,
        "Coach Maintenance": 110.0,
        "Staff Behaviour": 80.0,
        "Luggage": 50.0,
        "Ticketing": 65.0,
        "Station Facilities": 70.0,
        "Other": 60.0
    }

    priority_multiplier = {
        "P1": 0.5,
        "P2": 0.8,
        "P3": 1.0,
        "P4": 1.4
    }

    np.random.seed(42)

    # Calculate target synthetic resolution minutes
    def synth_duration(row):
        base = category_base_res.get(row["category"], 60.0)
        mult = priority_multiplier.get(row["priority"], 1.0)
        noise = np.random.normal(0, 10.0)
        return max(round(base * mult + noise, 1), 10.0)

    df["resolution_time_minutes"] = df.apply(synth_duration, axis=1)

    # Select features (Strictly pre-resolution operational features ONLY)
    feature_cols = ["category", "priority", "department", "train_number", "station"]
    X = df[feature_cols].fillna("Unknown")
    y = df["resolution_time_minutes"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    # Feature Transformer & Model Pipeline
    categorical_features = feature_cols
    preprocessor = ColumnTransformer(
        transformers=[("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)]
    )

    model_pipeline = Pipeline([
        ("prep", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42))
    ])

    model_pipeline.fit(X_train, y_train)

    y_pred = model_pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("--- MODEL EVALUATION METRICS ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f} minutes")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f} minutes")
    print(f"R² Score: {r2:.4f}\n")

    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    joblib.dump(model_pipeline, MODEL_OUTPUT_PATH)
    print(f"Saved resolution predictor artifact to {MODEL_OUTPUT_PATH}\n")


if __name__ == "__main__":
    train_resolution_predictor()

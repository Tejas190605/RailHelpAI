import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
)

from app.ai.preprocessor import preprocess_text

DATASET_PATH = "data/synthetic/synthetic_complaints_10k.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "complaint_classifier_v1.0.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")
MODEL_CARD_PATH = os.path.join(MODEL_DIR, "model_card.json")

SEED = 42


def train_and_evaluate():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}. Please run scripts/generate_synthetic_data.py first.")

    print(f"Loading synthetic dataset from {DATASET_PATH}...")
    df = pd.read_csv(DATASET_PATH)

    print("Preprocessing text data...")
    df["cleaned_text"] = df["complaint_text"].apply(preprocess_text)

    X = df["cleaned_text"]
    y = df["category"]

    print("Performing stratified 80/20 train/test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=SEED, stratify=y
    )

    print("Building TF-IDF + LogisticRegression model pipeline...")
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1000, random_state=SEED, C=1.0))
    ])

    print("Training classification model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model performance on test set...")
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(y_test, y_pred, average="macro")
    w_p, w_r, w_f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
    conf_mat = confusion_matrix(y_test, y_pred, labels=pipeline.classes_)

    metrics = {
        "accuracy": round(float(acc), 4),
        "macro_precision": round(float(macro_p), 4),
        "macro_recall": round(float(macro_r), 4),
        "macro_f1": round(float(macro_f1), 4),
        "weighted_precision": round(float(w_p), 4),
        "weighted_recall": round(float(w_r), 4),
        "weighted_f1": round(float(w_f1), 4),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "classes": list(pipeline.classes_)
    }

    print("\n--- MODEL EVALUATION SUMMARY ---")
    print(f"Accuracy:            {metrics['accuracy']:.4f}")
    print(f"Macro F1 Score:      {metrics['macro_f1']:.4f}")
    print(f"Weighted F1 Score:   {metrics['weighted_f1']:.4f}")
    print("--------------------------------\n")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"[SUCCESS] Saved trained model artifact to {MODEL_PATH}")

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"[SUCCESS] Saved evaluation metrics to {METRICS_PATH}")

    model_card = {
        "model_name": "complaint_classifier",
        "model_version": "v1.0",
        "algorithm": "TF-IDF (1,2 n-grams) + Logistic Regression",
        "training_dataset": "synthetic_complaints_10k.csv",
        "dataset_size": len(df),
        "features": ["complaint_text"],
        "target": "category (14 classes)",
        "random_seed": SEED,
        "metrics": metrics,
        "limitations": [
            "Trained on synthetic railway complaints data.",
            "May require additional domain tuning for heavily ambiguous or dialectical inputs."
        ]
    }

    with open(MODEL_CARD_PATH, "w", encoding="utf-8") as f:
        json.dump(model_card, f, indent=2)
    print(f"[SUCCESS] Saved model card to {MODEL_CARD_PATH}")


if __name__ == "__main__":
    train_and_evaluate()

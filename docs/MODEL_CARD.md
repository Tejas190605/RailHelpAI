# Model Card — Complaint Category Classifier v1.0

## Model Details
- **Model Name:** `complaint_classifier`
- **Model Version:** `v1.0`
- **Model Type:** TF-IDF Vectorizer (ngram_range=(1,2), max_features=5000) + Logistic Regression (C=1.0)
- **Developer:** RailHelpAI Core Project
- **License:** MIT

## Intended Use
- **Primary Use Case:** Automated classification of natural language passenger grievances into 14 operational categories.
- **Out of Scope:** Direct automated control of critical physical train systems without human operator oversight.

## Training Data
- **Dataset Name:** `synthetic_complaints_10k.csv`
- **Dataset Size:** 10,000 synthetic complaints
- **Data Source:** Synthetic dataset generated reproducibly (`seed=42`) using template variations, typos, and Hinglish terms.
- **Split:** Stratified 80% Train (8,000 samples) / 20% Test (2,000 samples).

## Evaluation Metrics (Test Set Evaluation)
- **Accuracy:** 94.90%
- **Macro Precision:** 94.91%
- **Macro Recall:** 94.90%
- **Macro F1 Score:** 0.9491
- **Weighted F1 Score:** 0.9494

## Limitations & Ethical Considerations
- Training data consists of synthetic complaints designed for academic/portfolio purposes.
- Predictions are advisory; confidence scores below 85% trigger Human-in-the-Loop review.

# RailHelpAI — AI Core Pipeline Architecture

> **Version:** v1.0  
> **Status:** Production-Inspired Baseline Pipeline  

---

## Overview

The RailHelpAI Core Engine processes unstructured natural language complaint text into structured, prioritized, and routed operational intelligence.

```text
               UNSTRUCTURED COMPLAINT TEXT
                            │
                            ▼
                  [ Text Preprocessor ]
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   [ Classifier ]   [ Entity Extractor ] [ Sentiment Engine ]
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                   [ Priority Engine ]
                            │
                            ▼
                  [ Department Router ]
                            │
                            ▼
             [ AI Confidence & HITL Thresholds ]
                            │
                            ▼
                   [ Explainability ]
                            │
                            ▼
              STRUCTURED AI ANALYSIS OUTPUT
```

---

## Sequential Stages

### 1. Text Preprocessor (`app/ai/preprocessor.py`)
- Lowercases text and normalizes excess whitespace.
- Standardizes common Hinglish & Hindi terms (e.g. *paani* $\rightarrow$ *water*, *safai* $\rightarrow$ *cleaning*).
- Strictly preserves entity tokens (coach codes like `B4`, seat numbers like `21`, train numbers like `12951`).

### 2. Complaint Category Classifier (`app/ai/classifier.py`)
- Model: `TF-IDF (1,2 n-grams)` + `LogisticRegression`.
- Trained on 10,000 synthetic complaints across 14 categories.
- Model Identifier: `complaint_classifier_v1.0`.
- Outputs predicted category, subcategory, and prediction confidence via `predict_proba`.

### 3. Hybrid NER Entity Extractor (`app/ai/entity_extractor.py`)
- Uses regular expression patterns + spaCy NER fallback.
- Extracted entities: `train_number`, `coach`, `seats`, `station`, `location`, `duration`, `issue`.

### 4. Local Sentiment Engine (`app/ai/sentiment.py`)
- Evaluates lexicon intensity and keyword indicators.
- Outputs sentiment label (`Positive`, `Neutral`, `Concerned`, `Negative`, `Angry`, `Critical`) and confidence.
- Sentiment contributes to rationale but does **not** independently dictate priority level.

### 5. Configurable Weighted Priority Engine (`app/ai/priority_engine.py`)
- Formula:
  $$\text{Priority Score} = (\text{Severity} \times 0.45) + (\text{Safety Risk} \times 0.30) + (\text{Passenger Impact} \times 0.15) + (\text{Waiting Duration} \times 0.10)$$
- Level Mapping:
  - **P1 Critical:** Score $\ge 80.0$
  - **P2 High:** Score $65.0 – 79.9$
  - **P3 Medium:** Score $45.0 – 64.9$
  - **P4 Low:** Score $< 45.0$
- Rationale Generation: Produces plain-text explanation bullet points explaining why the score was assigned.

### 6. Centralized Department Router (`app/ai/router.py`)
- Routes complaint to responsible unit based on category and keyword overrides.
- Outputs `department`, `routing_confidence`, and `routing_reason`.

### 7. Human-in-the-Loop Threshold Policy
- Model Confidence $\ge 85\% \rightarrow \text{AUTOMATIC}$ (Direct routing)
- Model Confidence $60\% – 84\% \rightarrow \text{HUMAN\_REVIEW}$ (Flagged for review queue)
- Model Confidence $< 60\% \rightarrow \text{MANUAL}$ (Manual classification required)

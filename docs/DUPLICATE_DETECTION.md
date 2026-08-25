# RailHelpAI — Semantic Duplicate Detection Engine

> **Version:** v1.0 (Phase 4)  

---

## 1. Overview
The duplicate detection engine identifies related complaints describing the same underlying issue, even when phrased differently (e.g. *"AC not working in coach B4"* vs *"B4 AC has stopped"*).

---

## 2. Model Pipeline
```text
Complaint Text ──► Preprocessor ──► TF-IDF / Sentence Vector ──► Cosine Similarity Matrix ──► Threshold Filter (>= 0.80)
```

---

## 3. Input & Output Schema
- **Input:** Raw complaint text, optional threshold.
- **Output:** `is_duplicate` (boolean), `similarity_score` (float 0–1), `matched_complaint_id` (str), `reason` (str).

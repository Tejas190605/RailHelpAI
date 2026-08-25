# RailHelpAI — AI Pipeline Testing & Contract Guide

> **Document Type:** AI & Machine Learning Contract Test Suite  
> **Status:** Fully Tested & Verified  

---

## 📌 Overview

RailHelpAI's AI intelligence core consists of deterministic ML models, rule-based engines, hybrid NER regex parsers, and vector similarity matchers. The pipeline contract tests verify component inputs, edge cases, fallback behaviors, and output schemas.

---

## 🧪 Verified AI Pipeline Contract Tests

| AI Component | Target Module | Contract Verified | Test Case | Status |
| :--- | :--- | :--- | :--- | :---: |
| **14-Category Classifier** | `app/ai/classifier.py` | TF-IDF + LogisticRegression inference | `test_classifier_prediction_ac` | ✅ **PASS** |
| **Hybrid Entity Extractor** | `app/ai/entity_extractor.py` | NER Regex parsing (Train, Coach, Seat, Station) | `test_extract_train_coach_seat_station` | ✅ **PASS** |
| **Priority Engine** | `app/ai/priority_engine.py` | P1–P4 evaluation & safety keyword override | `test_priority_p1_critical_medical` | ✅ **PASS** |
| **Department Router** | `app/ai/router.py` | Department mapping & RPF safety override | `test_router_rpf_keyword_override` | ✅ **PASS** |
| **Duplicate Detector** | `app/ai/duplicate_detector.py` | Cosine vector similarity engine | `test_duplicate_detection_high_similarity` | ✅ **PASS** |
| **DBSCAN Clustering** | `app/ai/clustering.py` | Active complaint spatial/temporal clustering | `test_rebuild_incident_clusters` | ✅ **PASS** |
| **Resolution Predictor** | `app/ai/resolution_predictor.py` | RandomForest regressionduration prediction | `test_predict_resolution_time_ac` | ✅ **PASS** |
| **Multilingual Normalizer**| `app/ai/multilingual.py` | Hinglish normalization & script detection | `test_detect_language_hinglish` | ✅ **PASS** |
| **Local Vision Classifier** | `app/ai/vision.py` | Zero-cost defect feature extraction | `test_classify_complaint_image_dark_cleanliness` | ✅ **PASS** |
| **Multimodal Conflict Fusion**| `app/ai/multimodal_pipeline.py` | Cross-modal text/vision conflict detection | `test_multimodal_with_image` | ✅ **PASS** |

---

## ⚙️ Running AI Pipeline Tests Locally

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_classifier.py tests/test_entity_extractor.py tests/test_priority_engine.py tests/test_duplicate_detector.py -v
```

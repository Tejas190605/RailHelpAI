# RailHelpAI — Known Limitations & Honest Model Evaluation

> **Version:** v1.0 (Phase 6 Final Release)  

---

## 1. Synthetic Dataset Template Leakage
- **Standard Random Split Metric:** 94.90% accuracy (Optimistic due to synthetic template leakage).
- **Template-Grouped Split Metric:** 30.50% accuracy (Conservative estimate of real-world generalization).
- **Transparency Statement:** RailHelpAI transparently preserves both metrics to demonstrate honest model evaluation practices.

---

## 2. Local Vision & OCR Scope
- Local visual defect feature extractor uses deterministic RGB intensity profiles rather than heavy cloud vision models to honor zero-cost deployment requirements.
- OCR text extraction is treated as advisory input and always sets `human_review_required=True`.

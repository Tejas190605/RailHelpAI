# RailHelpAI — Multimodal Complaint Intelligence & Conflict Fusion

> **Version:** v1.0 (Phase 5)  

---

## 1. Overview
The Multimodal Intelligence Pipeline fuses text NLP, vision feature classification, and OCR parsing.

```text
Text ──► Multilingual NLP ──► Category Candidate ┐
                                                 ├─► Fusion Matrix ──► Fused Category & Conflict Flag
Image ──► Vision Defect AI ──► Category Candidate ┘
```

---

## 2. Cross-Modal Conflict Detection
If the text analysis category and vision classification category disagree with vision confidence $\ge 0.75$:
- `conflict_detected` is set to `True`.
- `human_review_required` is set to `True`.
- Fused confidence is adjusted defensively.

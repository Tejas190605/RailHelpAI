# RailHelpAI — Local OCR Specification

> **Version:** v1.0 (Phase 5)  

---

## 1. Overview
The local OCR engine extracts visible text and entities (`train_number`, `coach`, `seat`) from ticket images or coach labels.

---

## 2. Advisory Disclaimer
OCR results are treated as uncertain advisory evidence (`ocr_confidence`). Output always sets `human_review_required=True`.

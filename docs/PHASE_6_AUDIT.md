# RailHelpAI — Phase 6 Baseline Architecture & Risk Audit

> **Date:** 2026-08-24  
> **Phase:** Phase 6 — Production Hardening, Security, Reliability, Observability & Packaging  

---

## 1. Repository Baseline Architecture Summary

RailHelpAI is an independent, zero-cost, locally runnable AI grievance intelligence prototype for railway operations.

```text
Streamlit UI (Port 8501)
     │
     ▼
FastAPI Backend (Port 8000)
     │
     ├── Middleware: Request Correlation ID (X-Request-ID), CORS, Centralized Error Handler
     ├── Endpoints: /health/live, /health/ready, /complaints, /ai/*, /operations/*, /analytics/*
     │
     ├── AI Core Pipeline:
     │    ├── Preprocessor (Entity-Preserving Normalization)
     │    ├── Classifier (TF-IDF + LogisticRegression)
     │    ├── Entity Extractor (NER - Train, Coach, Seat, Station)
     │    ├── Priority & Sentiment Engine (Rules + Lexicon)
     │    ├── Department Router
     │    ├── Duplicate Detector (SentenceTransformer / Cosine Vector Similarity)
     │    ├── DBSCAN Clustering Engine
     │    ├── Resolution Predictor (RandomForest Regressor)
     │    ├── Vision Defect Classifier (Local RGB Feature Extractor)
     │    ├── Local OCR Engine (Advisory Text & Label Extractor)
     │    └── Multimodal Fusion Pipeline (Cross-Modal Conflict Detector)
     │
     └── Persistence: SQLite (`railhelpai.db` with SQLAlchemy ORM)
```

---

## 2. Risk Assessment & Audit Findings

| Audit Domain | Identified Baseline Risk | Phase 6 Hardening Strategy |
| :--- | :--- | :--- |
| **Configuration** | Machine-specific paths or un-isolated env variables | Centralize `app/config.py` with `python-dotenv`, ensure `.env` in `.gitignore`, create safe `.env.example`. |
| **Security & Validation** | Missing correlation IDs; unhandled exception stack traces | Add `X-Request-ID` middleware, uniform error response schema (`APIErrorResponse`), validate path/query params. |
| **Database** | SQLite WAL mode & index coverage | Enforce SQLite foreign keys on connection, verify database indexes on `complaint_id`, `status`, `priority`, `department`, `train_number`, `station`, `created_at`. |
| **Health Observability** | Single `/health` endpoint | Split into `/health/live` and `/health/ready` (checking SQLite connection & model availability). |
| **Demo Reproducibility** | Manual multi-step CLI commands | Create powershell startup scripts `scripts/start_backend.ps1`, `scripts/start_frontend.ps1`, and controlled demo data seeder `scripts/seed_demo_data.py`. |
| **Documentation & Transparency**| Synthetic dataset template leakage | Keep Phase 2 dataset leakage transparently documented (94.90% random split vs 30.50% template-grouped split). |

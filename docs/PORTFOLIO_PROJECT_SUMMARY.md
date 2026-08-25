# RailHelpAI — Portfolio Project Summary & Technical Overview

> **Project:** RailHelpAI — AI-Powered Railway Complaint Intelligence & Operations Platform  
> **Type:** Production-Inspired Portfolio Prototype  

---

## 📄 Project Description & Resume Positioning

### Short Project Description
RailHelpAI is an independent, production-inspired portfolio project that transforms raw railway passenger grievances into structured, actionable operational intelligence using NLP, machine learning, multimodal evidence analysis, workflow automation, and human-in-the-loop review.

### One-line Resume Description
- **RailHelpAI:** Production-inspired railway complaint intelligence platform using FastAPI, Streamlit, scikit-learn, and SQLite with automated NLP classification, SLA workflows, DBSCAN incident clustering, and multimodal vision fusion (85/85 automated tests passing).

---

### 3 Resume Bullet Versions

#### Version A: ATS-Optimized Technical Resume Bullets
- **RailHelpAI — AI-Powered Railway Complaint Intelligence & Operations Platform**
  - Engineered an end-to-end railway complaint triage system using **FastAPI**, **Streamlit**, **scikit-learn**, and **SQLite**, processing raw text/image grievances into prioritized operational tickets.
  - Implemented an **AI NLP pipeline** incorporating TF-IDF classification, entity extraction (NER), priority scoring (P1–P4), rule-based sentiment analysis, and automated department routing with confidence-based human-in-the-loop thresholds ($\ge 85\%$ auto, $60-84\%$ human review).
  - Developed advanced intelligence services including **cosine vector duplicate detection**, **DBSCAN incident clustering**, **RandomForest resolution-time prediction** (MAE: 8.04 min, $R^2$: 0.9353), and a multimodal vision/OCR fusion engine with cross-modal conflict detection.
  - Hardened backend API with `X-Request-ID` correlation middleware, health liveness/readiness checks, structured error handling, and SQLite indexing; verified **85/85 automated tests passing**.

#### Version B: Deep Technical Bullets
- **RailHelpAI — Multimodal Railway Operations & Grievance Intelligence System**
  - Built a 14-category NLP complaint classifier and entity extractor handling Hinglish/Hindi text normalization, priority evaluation, and SLA target monitoring.
  - Integrated DBSCAN spatial/temporal clustering to group correlated complaints into active incident clusters, alongside a cosine similarity engine for duplicate complaint suppression.
  - Designed an operational Streamlit UI across 11 workstations with a custom visual design system (9.2/10 Visual QA score).
  - Conducted transparent ML model evaluation, documenting synthetic template leakage (94.90% random split vs 30.50% zero-leakage template-grouped evaluation).

#### Version C: Concise Resume Entry
- **RailHelpAI:** End-to-end railway complaint intelligence platform using FastAPI, Streamlit, scikit-learn, and SQLite with automated NLP classification, SLA workflows, DBSCAN incident clustering, and multimodal vision fusion (85/85 automated tests passing).

---

## 🛠️ Technical Stack Matrix

- **Backend API:** Python 3.10+, FastAPI 0.109, Uvicorn, Pydantic v2
- **Frontend UI:** Streamlit 1.31, Plotly Express
- **Machine Learning & NLP:** scikit-learn (TF-IDF + LogisticRegression, RandomForest), SentenceTransformers (Cosine Similarity), DBSCAN
- **Image & OCR:** Pillow (PIL Image Security & Feature Extractor), PyTesseract
- **Database & Persistence:** SQLite, SQLAlchemy ORM
- **Testing & Tooling:** pytest, Starlette TestClient, python-dotenv

---

## 🏛️ Architecture & System Design

RailHelpAI decouples ingestion, AI prediction, operational services, and frontend visualization:

```text
Streamlit UI (Port 8501 / 11 Workstations)
     │
     ▼
FastAPI Backend (Port 8000 / OpenAPI)
     │
     ├── Middleware: X-Request-ID Correlation, CORS, Global Error Handler
     ├── Endpoints: /health/live, /health/ready, /complaints, /ai/*, /operations/*, /analytics/*
     │
     ├── AI Core Pipeline:
     │    ├── Preprocessor (Entity-Preserving Normalization)
     │    ├── Classifier (TF-IDF + LogisticRegression)
     │    ├── Entity Extractor (NER - Train, Coach, Seat, Station)
     │    ├── Priority & Sentiment Engine (Rules + Lexicon)
     │    ├── Department Router
     │    ├── Duplicate Detector (Cosine Vector Similarity)
     │    ├── DBSCAN Clustering Engine
     │    ├── Resolution Predictor (RandomForest Regressor)
     │    ├── Vision Defect Classifier (Local Visual Feature Extractor)
     │    ├── Local OCR Engine (Advisory Text Extractor)
     │    └── Multimodal Fusion Pipeline (Conflict Detector)
     │
     └── Persistence: SQLite (railhelpai.db with SQLAlchemy ORM)
```

---

## 🌟 Major Technical Capabilities

1. **AI Grievance Triage Pipeline:** Instant NLP classification across 14 categories with hybrid NER entity extraction.
2. **Confidence-Based Human-in-the-Loop Safeguards:** Automatically routes predictions below $85\%$ confidence to an Operator Review Queue for supervisor approval or override.
3. **Incident Intelligence & Suppression:** DBSCAN clustering groups recurring complaints into incident clusters (`INC-042`), while vector cosine similarity suppresses duplicate filings.
4. **Multimodal Evidence Fusion:** Fuses text NLP, local vision defect classification, and OCR label text. Flags `conflict_detected=True` when text and vision categories disagree.
5. **Prescriptive Recommendations & Risk Index:** Calculates composite RailHelpAI Operational Risk Index and generates metric-backed action items.

---

## 📊 Transparent Model Evaluation & Limitations

- **Standard Random Split Metric:** 94.90% Accuracy (Optimistic due to synthetic template leakage).
- **Template-Grouped Split Metric:** 30.50% Accuracy (Conservative estimate of real-world generalization).
- **Resolution Predictor:** MAE = 8.04 min, RMSE = 10.22 min, $R^2$ = 0.9353.
- **Transparency Statement:** Both metrics are preserved and documented to demonstrate honest machine learning evaluation practices.

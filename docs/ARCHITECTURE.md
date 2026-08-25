# RailHelpAI — End-to-End System Architecture

> **Version:** v1.0 (Phase 6 Final Release)  

---

## 1. System Architecture Diagram

```text
                                  ┌─────────────────────────────┐
                                  │   Streamlit Web Frontend    │
                                  │   (Port 8501 / Multipage)   │
                                  └──────────────┬──────────────┘
                                                 │ REST APIs (HTTP / JSON)
                                                 ▼
                                  ┌─────────────────────────────┐
                                  │      FastAPI Backend        │
                                  │   (Port 8000 / OpenAPI)     │
                                  └──────────────┬──────────────┘
                                                 │
                  ┌──────────────────────────────┼──────────────────────────────┐
                  ▼                              ▼                              ▼
     ┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────────────┐
     │   AI Core Pipeline     │    │  Multimodal AI Engine  │    │  Operations & Analytics│
     │ ├── Preprocessor       │    │ ├── Local Vision Defect│    │ ├── SLA Engine         │
     │ ├── Classifier         │    │ ├── Local OCR Parser   │    │ ├── State Machine      │
     │ ├── Entity Extraction  │    │ └── Conflict Fusion    │    │ ├── Hotspot Risk       │
     │ ├── Priority Engine    │    └────────────────────────┘    │ ├── Train/Station      │
     │ ├── Department Router  │                                  │ └── Risk Index         │
     │ ├── Duplicate Detector │                                  └────────────────────────┘
     │ ├── DBSCAN Clustering  │
     │ └── Resolution Time    │
     └────────────┬───────────┘
                  │
                  ▼
     ┌────────────────────────┐
     │  SQLite Database       │
     │  (railhelpai.db)       │
     └────────────────────────┘
```

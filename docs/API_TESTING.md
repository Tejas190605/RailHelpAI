# RailHelpAI — API Testing & Verification Guide

> **Document Type:** Backend API Test Suite Specification  
> **Status:** Fully Tested & Verified  

---

## 📌 Overview

The RailHelpAI backend REST API is built with **FastAPI** and **Pydantic v2**. The API test suite uses FastAPI `TestClient` and `pytest` to validate endpoint contracts, input validation, state machine rules, error handling, and response invariants.

---

## 🧪 Verified API Test Matrix

| Endpoint Route | Method | Purpose | Test Case | Status |
| :--- | :---: | :--- | :--- | :---: |
| `/health/live` | `GET` | System Liveness Check | `test_health_live_endpoint` | ✅ **PASS** |
| `/health/ready` | `GET` | DB & ML Readiness Check | `test_health_ready_endpoint` | ✅ **PASS** |
| `/api/v1/complaints` | `POST` | Create Complaint | `test_create_complaint` | ✅ **PASS** |
| `/api/v1/complaints` | `GET` | List Complaints | `test_list_complaints` | ✅ **PASS** |
| `/api/v1/complaints/{id}` | `GET` | Get Complaint by ID | `test_get_complaint_by_id` | ✅ **PASS** |
| `/api/v1/complaints/{id}/status` | `PATCH` | State Machine Transition | `test_invalid_state_transition` | ✅ **PASS** |
| `/api/v1/ai/analyze` | `POST` | Full AI Triage Pipeline | `test_canonical_demo_complaint_workflow` | ✅ **PASS** |
| `/api/v1/intelligence/duplicates` | `POST` | Cosine Duplicate Matching | `test_duplicate_detection_schema` | ✅ **PASS** |
| `/api/v1/intelligence/predict-resolution`| `POST` | Resolution Time Regression | `test_resolution_prediction_schema` | ✅ **PASS** |
| `/api/v1/operations/complaints/{id}/assign`| `POST` | Assign Department | `test_operations_assign` | ✅ **PASS** |
| `/api/v1/operations/complaints/{id}/resolve`| `POST` | Mark Resolved | `test_operations_resolve` | ✅ **PASS** |

---

## ⚙️ Running API Tests Locally

```powershell
# Run full backend API and pipeline test suite
.\venv\Scripts\python.exe -m pytest tests/ -v
```

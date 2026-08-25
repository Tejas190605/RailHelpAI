# RailHelpAI — Streamlit Native AppTest Testing Guide

> **Document Type:** Frontend & UI Testing Architecture Specification  
> **Framework:** Streamlit Native `AppTest` (`streamlit.testing.v1`)  
> **Status:** Fully Tested & Integrated in CI  

---

## 📌 Purpose of AppTest Framework

RailHelpAI employs **Streamlit `AppTest`** (`streamlit.testing.v1`) for deterministic, headless UI verification of the 11 registered workstation pages.

Unlike end-to-end browser automation (Playwright), `AppTest` simulates the Streamlit execution engine directly in Python memory without requiring a running web server or browser process. This makes UI layout, widget state, widget interaction, and exception assertion tests execute in seconds within zero-cost CI pipelines.

---

## 🆚 AppTest vs Playwright Browser Automation

| Dimension | Streamlit AppTest (`tests/test_streamlit_app.py`) | Playwright Browser Audit (`scripts/capture_screenshots.py`) |
| :--- | :--- | :--- |
| **Execution Environment** | Headless Python memory test harness | Real Chromium browser instance |
| **Target Scope** | Component widgets, session state, layout exceptions | End-to-end DOM rendering, visual layout, screenshots |
| **Execution Speed** | Fast (~10 seconds for 12 tests) | Slow (~45 seconds browser navigation) |
| **CI Integration** | Native `pytest` test runner in GitHub Actions | Local visual acceptance & portfolio screenshot generation |
| **Backend Requirement**| Self-contained (uses fallback safe API utilities) | Requires live FastAPI server on `http://127.0.0.1:8000` |

---

## 🧪 Tested Pages & Widgets

1. **`app.py` Navigation Shell:** Validates multipage structure & CSS injection.
2. **`01_Overview.py` (Command Center):** Validates KPI cards and chart layout.
3. **`02_Submit_Complaint.py` (Submit Complaint):** Tests form text area, inputs, and form submission.
4. **`03_AI_Analysis.py` (AI Analysis):** Tests sample preset selection and analysis trigger.
5. **`04_Complaint_Queue.py` (Complaint Queue):** Validates complaint list rendering and search filters.
6. **`05_SLA_Monitor.py` (SLA Monitor):** Validates SLA breach metrics and response timers.
7. **`06_Human_Review_Queue.py` (Human Review Queue):** Validates HITL low-confidence review queue.
8. **`07_Complaint_Detail.py` (Complaint Detail):** Validates detailed grievance investigation view.
9. **`08_Train_Intelligence.py` (Train Intelligence):** Validates train-level analytical breakdown.
10. **`09_Station_Intelligence.py` (Station Intelligence):** Validates station-level analytical profile.
11. **`10_Incident_Clusters.py` (Incident Clusters):** Validates spatial/temporal DBSCAN cluster list.
12. **`11_Executive_Intelligence.py` (Executive Intelligence):** Validates operational risk index and trend analytics.

---

## ⚙️ Running Streamlit AppTest Locally

```powershell
# Run Streamlit AppTest suite
.\venv\Scripts\python.exe -m pytest tests/test_streamlit_app.py -v
```

# RailHelpAI — Prescriptive Recommendation Engine

> **Version:** v1.0 (Phase 5)  

---

## 1. Prescriptive Rules Engine
Generates explainable operational advice strictly derived from database evidence:
1. **Rule 1 (High SLA Breach Rate):** Triggers when a category breach rate $\ge 25\%$.
2. **Rule 2 (Active Incident Clusters):** Triggers when a DBSCAN cluster contains $\ge 3$ correlated complaints.
3. **Rule 3 (Category Volume Surge):** Triggers when a category exhibits a 7-day volume surge $\ge +20\%$.

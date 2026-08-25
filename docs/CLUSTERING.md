# RailHelpAI — Complaint Clustering & Incident Detection

> **Version:** v1.0 (Phase 4)  

---

## 1. Overview
The complaint clustering module scans open complaints and groups related reports into active operational incidents (e.g. `INC-042: Air Conditioning Issue — Coach B4`).

---

## 2. Clustering Algorithm
- **Algorithm:** DBSCAN (`eps=0.65`, `min_samples=2`, `metric="cosine"`).
- **Label Generator:** Synthesizes category, train, coach, and incident report count into a human-readable title.

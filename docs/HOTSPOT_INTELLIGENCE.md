# RailHelpAI — Hotspot Risk Scoring Specification

> **Version:** v1.0 (Phase 4)  
> ⚠️ **Disclaimer:** All risk scores are prototype analytical indicators and do not represent official Indian Railways safety ratings.

---

## 1. Hotspot Score Formula
$$\text{Hotspot Score} = (\text{Volume Score} \times 0.35) + (\text{Severity Score} \times 0.30) + (\text{SLA Breach Rate} \times 0.20) + (\text{Incident Cluster Score} \times 0.15)$$

---

## 2. Risk Level Thresholds
- **LOW:** $< 30.0$
- **MEDIUM:** $30.0 – 59.9$
- **HIGH:** $60.0 – 79.9$
- **CRITICAL:** $\ge 80.0$

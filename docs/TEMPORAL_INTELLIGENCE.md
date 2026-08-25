# RailHelpAI — Temporal Intelligence & Anomaly Detection

> **Version:** v1.0 (Phase 5)  

---

## 1. Category Trend Directions
Calculates 7-day volume changes against prior 7-day baselines:
- **INCREASING:** $\ge +20\%$ change
- **DECREASING:** $\le -20\%$ change
- **STABLE:** $-19.9\%$ to $+19.9\%$ change

---

## 2. Statistical Anomaly Detection
Uses rolling hourly mean + 2 standard deviations ($\mu + 2\sigma$) to flag statistical volume spikes.

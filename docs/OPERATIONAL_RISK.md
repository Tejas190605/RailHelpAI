# RailHelpAI — Operational Risk Index Specification

> **Version:** v1.0 (Phase 5)  
> ⚠️ **Disclaimer:** Prototype analytical score — not an official railway risk metric.

---

## 1. Risk Index Formula
$$\text{Risk Index} = (\text{Volume} \times 0.25) + (\text{Severity} \times 0.30) + (\text{SLA Breach Rate} \times 0.25) + (\text{Incident Activity} \times 0.20)$$

---

## 2. Risk Bands
- **LOW:** $< 30.0$
- **MEDIUM:** $30.0 – 59.9$
- **HIGH:** $60.0 – 79.9$
- **CRITICAL:** $\ge 80.0$

# RailHelpAI — SLA Engine Specification

> **Version:** v1.0 (Phase 3)  
> ⚠️ **Disclaimer:** All SLA parameters are demonstration values for prototype testing and do not represent official Indian Railways SLA commitments.

---

## 1. Prototype SLA Target Matrix

| Priority | Response Target | Resolution Target |
|---|---|---|
| **P1 - Critical** | 10 minutes | 30 minutes |
| **P2 - High** | 30 minutes | 2 hours (120 mins) |
| **P3 - Medium** | 2 hours (120 mins) | 8 hours (480 mins) |
| **P4 - Low** | 8 hours (480 mins) | 24 hours (1440 mins) |

---

## 2. Dynamic SLA Status Tracking

- **WITHIN_SLA:** $< 50\%$ elapsed time.
- **APPROACHING_SLA:** $50\% – 89.9\%$ elapsed time.
- **ESCALATION_WARNING:** $90\% – 99.9\%$ elapsed time.
- **BREACHED:** $\ge 100\%$ elapsed time or resolution deadline exceeded.

---

## 3. SLA Formulas

### SLA Compliance Rate Formula
$$\text{SLA Compliance Rate} = \frac{\text{Complaints Resolved Within Resolution Deadline}}{\text{Total Resolved Complaints}} \times 100$$

### AI Automation Rate Formula
$$\text{AI Automation Rate} = \frac{\text{Complaints Automatically Routed without Human Review}}{\text{Total AI-Analyzed Complaints}} \times 100$$

# RailHelpAI — Operations & Workflow Specification

> **Version:** v1.0 (Phase 3)  

---

## 1. Complaint State Machine

Complaints progress through an enforced state machine:

```text
NEW ──► AI_ANALYZED ──► PENDING_REVIEW ──► ASSIGNED ──► IN_PROGRESS ──► WAITING_FOR_INFORMATION ──► RESOLVED ──► CLOSED
```

### Lifecycle States
- **NEW:** Raw complaint received.
- **AI_ANALYZED:** Processed by AI pipeline.
- **PENDING_REVIEW:** Sent to AI Review Queue (confidence $< 85\%$).
- **ASSIGNED:** Assigned to operational department and operator.
- **IN_PROGRESS:** Active operational work ongoing.
- **WAITING_FOR_INFORMATION:** Operator requested additional details from passenger.
- **RESOLVED:** Fix applied; resolution recorded.
- **CLOSED:** Resolved grievance formally closed.

---

## 2. Human-in-the-Loop Review Audit Trail

When an operator approves or overrides AI predictions, an entry is recorded in the `ai_reviews` database table:
- `original_category` vs `final_category`
- `original_priority` vs `final_priority`
- `original_department` vs `final_department`
- `action` (`Approve` or `Override`)
- `reason`

---

## 3. Resolution Types
- `FIXED`: Issue physically repaired / resolved.
- `INFORMATION_PROVIDED`: Guidance provided to passenger.
- `ESCALATED`: Escalated to senior authority.
- `DUPLICATE`: Flagged as duplicate.
- `INVALID`: Invalid or spam report.
- `NO_ACTION_REQUIRED`: Issue resolved automatically.
- `OTHER`: General resolution action.

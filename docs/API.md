# RailHelpAI — REST API Specification

## Endpoints

### Complaints
- `POST /api/v1/complaints` — Submit complaint & execute AI pipeline
- `GET /api/v1/complaints` — List complaints with pagination & filters
- `GET /api/v1/complaints/{id}` — Get complaint detail
- `PATCH /api/v1/complaints/{id}` — Update complaint fields
- `DELETE /api/v1/complaints/{id}` — Delete complaint

### AI Pipeline
- `POST /api/v1/ai/analyze` — Run full AI analysis
- `POST /api/v1/ai/classify` — Predict category
- `POST /api/v1/ai/extract-entities` — Extract entities

### Operations & Workflow
- `POST /api/v1/complaints/{id}/assign` — Assign department & operator
- `POST /api/v1/complaints/{id}/review` — Process human AI review override/approval
- `POST /api/v1/complaints/{id}/resolve` — Resolve complaint with resolution notes
- `POST /api/v1/complaints/{id}/feedback` — Record passenger satisfaction rating & feedback

### Analytics
- `GET /api/v1/analytics/overview` — Operational KPIs
- `GET /api/v1/analytics/categories` — Category breakdown
- `GET /api/v1/analytics/priority` — Priority breakdown
- `GET /api/v1/analytics/departments` — Department workload
- `GET /api/v1/analytics/sla` — SLA performance breakdown

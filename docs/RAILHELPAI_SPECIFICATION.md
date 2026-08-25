# RailHelpAI — Antigravity Project Specification

> **Source of truth:** `RailHelpAI PROJ Soecification.docx`
>
> **Project:** RailHelpAI
>
> **Full name:** AI-Powered Railway Complaint Intelligence & Resolution Platform
>
> **Type:** AI/ML + NLP + Web Application
>
> **Target:** Resume / Portfolio / Academic Project
>
> **Development level:** Production-inspired prototype
>
> **Cost target:** ₹0
>
> **Status:** Specification / implementation baseline

---

## 0. Agent Instructions

This file is the implementation-oriented version of the RailHelpAI Project Specification.

When developing RailHelpAI:

1. Treat this file as the primary project requirements document.
2. Preserve the scope and terminology defined here unless a change is explicitly approved.
3. Do not implement the whole specification in one step.
4. Work in phases and verify each phase before moving to the next.
5. Prefer a smaller set of genuinely working features over many fake or placeholder features.
6. Never fabricate ML metrics, railway data, SLA commitments, API results, or model capabilities.
7. Use synthetic/anonymized data only.
8. Keep all paid APIs/services optional; the core application must work without paid API keys.
9. Use local/open-source ML and NLP components wherever practical.
10. Before major implementation, create/update an implementation plan and identify dependencies, risks, and verification steps.
11. After implementation, run tests and verify the actual application rather than assuming generated code works.
12. Preserve working code and make targeted changes rather than unnecessary rewrites.

---

# 1. Project Definition

## 1.1 One-line definition

RailHelpAI is an AI-powered railway complaint intelligence platform that converts unstructured passenger grievances into structured, prioritized, routed, and actionable operational intelligence.

## 1.2 Core pipeline

```text
UNSTRUCTURED COMPLAINT
        ↓
   NLP / AI
        ↓
 STRUCTURED DATA
        ↓
 CLASSIFICATION
        ↓
 ENTITY EXTRACTION
        ↓
    PRIORITY
        ↓
  DEPARTMENT
        ↓
      SLA
        ↓
   RESOLUTION
        ↓
   ANALYTICS
        ↓
PREDICTIVE INSIGHTS
```

## 1.3 Product positioning

RailHelpAI is inspired by railway grievance-management workflows such as RailMadad and the SIH 2024 railway complaint-management problem.

It is **not** an official Indian Railways system and must not be represented as one.

It demonstrates how AI could:

- reduce manual complaint categorization
- improve complaint routing
- identify urgent issues
- detect recurring incidents
- monitor SLA risk
- identify train/station hotspots
- predict approximate resolution time
- generate operational insights

---

# 2. Problem Statement

Railway passengers may report:

- Air conditioning problems
- Cleanliness problems
- Water supply problems
- Electrical issues
- Catering issues
- Staff behaviour
- Security issues
- Coach maintenance issues
- Station facility issues
- Ticketing issues
- Medical assistance
- Luggage issues
- Pest control

Traditional grievance systems primarily receive, track, and resolve complaints.

RailHelpAI adds an intelligence layer that converts unstructured passenger complaints into structured operational information.

### Example

Input:

> "AC isn't working in coach B4 and we've been waiting for 30 minutes."

Expected structured result:

```text
Category: Air Conditioning
Subcategory: AC Not Cooling
Coach: B4
Duration: 30 minutes
Sentiment: Negative
Priority: P2 - High
Department: Electrical / Coach Maintenance
SLA: 2 hours
```

Workflow:

```text
Complaint
   ↓
AI Analysis
   ↓
Classification
   ↓
Entity Extraction
   ↓
Priority Prediction
   ↓
Department Routing
   ↓
SLA Assignment
   ↓
Resolution
   ↓
Analytics
```

---

# 3. Objectives

## 3.1 Primary objectives

1. Automatically classify railway complaints.
2. Extract useful information from natural-language complaints.
3. Automatically determine complaint priority.
4. Route complaints to appropriate departments.
5. Assign configurable SLA targets.
6. Detect duplicate or related complaints.
7. Identify recurring complaint clusters.
8. Predict approximate resolution time.
9. Provide train and station analytics.
10. Identify operational hotspots.
11. Provide explainable AI decisions.
12. Provide a centralized administrator dashboard.

## 3.2 Secondary / advanced objectives

- Sentiment analysis
- Multilingual/Hinglish complaints
- OCR from uploaded images
- Basic image-based complaint classification
- AI-generated complaint summaries
- AI assistant/chatbot
- Complaint escalation
- Resolution feedback
- Model performance monitoring

These are advanced modules and are not required for the first MVP.

---

# 4. Target Users

## Passenger

Can:

- submit complaints
- upload supporting evidence
- track complaint status
- view AI-generated complaint details
- receive complaint ID
- provide resolution feedback

## Railway Operator / Support Agent

Can:

- view assigned complaints
- understand complaint summaries
- see AI priority
- view extracted entities
- update complaint status
- add resolution information
- monitor SLA deadlines

## Administrator

Can:

- monitor all complaints
- view system KPIs
- analyze departments
- monitor SLA compliance
- identify hotspots
- analyze train/station problems
- review AI predictions
- review low-confidence predictions

---

# 5. System Scope

## In scope

- Complaint management
- NLP classification
- Entity extraction
- Priority scoring
- Department routing
- SLA management
- Sentiment analysis
- Duplicate detection
- Complaint clustering
- Analytics
- Train intelligence
- Station intelligence
- Resolution prediction
- OCR
- Basic image analysis
- Explainable AI
- Synthetic dataset
- REST APIs
- Web dashboard
- Testing
- Free deployment

## Out of scope

- Actual Indian Railways backend
- Real PNR verification
- Real railway employee accounts
- Real railway control systems
- Real-time train control
- Payment processing
- Production passenger data
- Government authentication systems
- Production SLA commitments
- Real railway operational decisions

---

# 6. Functional Requirements

## FR-01 — Complaint Submission

Required fields:

- Complaint description
- Train/Station
- Train number
- Coach
- Seat
- Incident date/time
- Location

Optional:

- Image
- Video
- PDF
- Additional information

The prototype should support complaint descriptions and evidence uploads.

---

## FR-02 — Complaint Classification

Initial categories:

1. Air Conditioning
2. Cleanliness
3. Water Supply
4. Electrical
5. Catering
6. Security
7. Staff Behaviour
8. Coach Maintenance
9. Station Facilities
10. Ticketing
11. Medical
12. Luggage
13. Pest Control
14. Other

Example:

```text
Input:
"AC isn't cooling in B4"

Output:
Category = Air Conditioning
Subcategory = AC Not Cooling
```

---

## FR-03 — Entity Extraction

Extract:

- TRAIN_NUMBER
- TRAIN_NAME
- COACH
- SEAT
- STATION
- LOCATION
- ISSUE
- DURATION
- DATE
- TIME
- DEPARTMENT

Example:

```text
Input:
"The charging sockets in B4 seats 21 and 22 haven't worked since Pune."

Output:
{
  "issue": "charging socket failure",
  "coach": "B4",
  "seats": ["21", "22"],
  "location": "Pune"
}
```

---

## FR-04 — Priority Intelligence

Priority levels:

| Priority | Meaning |
|---|---|
| P1 | Critical |
| P2 | High |
| P3 | Medium |
| P4 | Low |

Initial configurable scoring:

```text
Priority Score =
Severity × 0.45
+ Safety Risk × 0.30
+ Passenger Impact × 0.15
+ Waiting Time × 0.10
```

Weights must be configurable.

Factors:

- severity
- safety risk
- passenger impact
- waiting duration
- sentiment
- complaint recurrence

Sentiment must support prioritization but must not determine priority by itself.

---

## FR-05 — Department Routing

Routing must be configurable.

Examples:

```text
AC malfunction
    ↓
Electrical / Coach Maintenance

Dirty toilet
    ↓
Housekeeping / Sanitation

Food quality
    ↓
Catering

Theft
    ↓
Security

Medical emergency
    ↓
Medical
```

Do not scatter routing rules throughout the codebase.

---

## FR-06 — SLA Management

Prototype/demo SLA policy:

| Priority | Response | Resolution |
|---|---:|---:|
| P1 | 10 min | 30 min |
| P2 | 30 min | 2 hr |
| P3 | 2 hr | 8 hr |
| P4 | 8 hr | 24 hr |

**Important:** These are configurable demonstration values and must never be presented as official Indian Railways SLA commitments.

---

## FR-07 — SLA Escalation

Lifecycle:

```text
Complaint Created
      ↓
SLA Started
      ↓
50% elapsed → Warning
      ↓
90% elapsed → Escalation Warning
      ↓
100% → SLA Breach
```

Dashboard states:

- Within SLA
- Approaching SLA
- SLA Breached

The implementation may also represent escalation explicitly.

---

## FR-08 — Sentiment Analysis

Possible labels:

- Positive
- Neutral
- Concerned
- Negative
- Angry
- Critical

Example:

> "This is the third time I've complained and nobody is doing anything!"

Expected:

```text
Sentiment = Angry
```

Sentiment confidence should be stored.

---

## FR-09 — Duplicate Complaint Detection

Use semantic similarity.

Pipeline:

```text
Complaint
    ↓
Sentence Embedding
    ↓
Vector
    ↓
Cosine Similarity
    ↓
Similarity Threshold
    ↓
Potential Duplicate
```

Example related complaints:

- "AC isn't working in B4"
- "B4 AC has stopped"
- "No AC in coach B4"

Store similarity score.

Threshold must be configurable.

---

## FR-10 — Complaint Clustering

Identify recurring complaint groups.

Potential algorithms:

- K-Means
- DBSCAN
- HDBSCAN

Example:

```text
Cluster 1 → AC complaints
Cluster 2 → Toilet cleanliness
Cluster 3 → Water shortage
Cluster 4 → Staff behaviour
```

---

## FR-11 — Resolution Time Prediction

Input features:

- Category
- Priority
- Department
- Station
- Train
- Time of day
- Day
- Historical resolution time
- Complaint volume

Output:

- Estimated resolution time
- Prediction confidence

Potential models:

- Random Forest
- Gradient Boosting
- XGBoost

Evaluate with:

- MAE
- RMSE
- R²

---

## FR-12 — Hotspot Detection

Identify locations with unusually high complaint volumes.

Potential signals:

- Complaint count
- Complaint density
- Complaint severity
- SLA breaches
- Recurring incidents

Example display:

```text
Mumbai Central 🔴
Pune           🟠
Thane          🟡
Nashik         🟢
```

These are prototype analytics, not official railway risk ratings.

---

## FR-13 — Train Intelligence

Each train should have an analytical profile.

Metrics:

- Total complaints
- Open complaints
- Resolved complaints
- SLA compliance
- Average resolution
- Top problems
- Complaint trends
- Worst coaches
- Risk score

Example:

```text
Train: 12951
Total Complaints: 428
Open Complaints: 37
Resolved: 391
SLA Compliance: 91.4%
Average Resolution: 1h 42m

Top problems:
AC 31%
Cleanliness 24%
Catering 17%
Water 11%
Other 17%
```

Use actual database-derived values in the application.

---

## FR-14 — Station Intelligence

Metrics:

- Station complaint volume
- Top complaint categories
- Peak complaint periods
- Recurring issues
- SLA breaches
- Complaint trends
- SLA performance
- Hotspot status

---

## FR-15 — Explainable AI

Every major AI decision should provide an explanation.

Example:

```text
Priority: P2
Score: 72/100

Reasons:
✓ Coach-wide AC failure
✓ Passenger comfort significantly affected
✓ Complaint unresolved for 30 minutes
✓ No immediate life-threatening risk detected
```

Explanations must correspond to actual signals used by the system.

Do not fabricate explanations.

---

## FR-16 — Human-in-the-Loop

Confidence policy:

```text
Confidence >= 85%
    ↓
Automatic routing

60–84%
    ↓
Human review

<60%
    ↓
Manual classification
```

Create an AI Review Queue.

Example:

```text
Complaint #RAI-1204

AI:
Category = Electrical
Confidence = 57%

Actions:
[Approve]
[Change Category]
```

Store human corrections so they can become future training data.

---

## FR-17 — OCR

Optional OCR should extract information from images containing:

- Coach information
- Train information
- Station information
- Complaint evidence

Technology:

- Tesseract
- pytesseract

OCR failure must not crash the complaint workflow.

---

## FR-18 — Image Intelligence

Advanced feature.

Potential categories:

- Dirty Toilet
- Garbage
- Broken Seat
- Damaged Window
- Water Leakage
- Electrical Damage
- AC Issue
- Other

Output:

- Detected issue
- Confidence
- Suggested category

If reliable local/free image intelligence cannot be implemented, provide an extension point rather than pretending the feature works.

---

## FR-19 — Complaint Summarization

Long complaint → concise operator-facing summary.

Example:

```text
AC failure reported in coach B4.
Passenger states the issue has remained unresolved
for approximately 30 minutes.
```

---

## FR-20 — AI Chatbot

Optional feature for collecting missing complaint information.

Example:

```text
Passenger:
"My AC isn't working."

AI:
"Which coach are you travelling in?"

Passenger:
"B4."

AI:
"What is your seat number?"

Passenger:
"41."
```

The chatbot eventually creates a structured complaint.

A local/rule-based implementation is acceptable initially.

---

# 7. Non-Functional Requirements

## NFR-01 — Performance

Targets:

- Normal complaint analysis: < 5 seconds
- API response: < 2 seconds
- Dashboard load: < 5 seconds
- Database query: < 1 second

These are engineering targets, not guarantees.

## NFR-02 — Reliability

Handle:

- invalid input
- missing fields
- unsupported files
- AI prediction failures
- malformed complaints

Provide fallbacks where practical.

## NFR-03 — Security

- Never expose API keys.
- Use environment variables/secrets.
- Validate uploads.
- Limit file sizes.
- Avoid real PII.
- Use synthetic data for public deployment.
- Sanitize user input.
- Avoid exposing stack traces.

---

# 8. Technology Specification

## Frontend

- Streamlit
- HTML/CSS where required
- Plotly
- Folium / PyDeck

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## Database

- SQLite for MVP
- PostgreSQL optional for advanced deployment

## Machine Learning

- scikit-learn
- pandas
- numpy

## NLP

- spaCy
- NLTK
- Sentence Transformers
- Hugging Face Transformers

## OCR

- Tesseract
- pytesseract

## Visualization

- Plotly
- Folium
- PyDeck

---

# 9. AI Architecture

```text
Complaint
    │
    ▼
Text Preprocessing
    │
    ├──────────────┬──────────────┐
    ▼              ▼              ▼
Classifier        NER        Sentiment
    │              │              │
    └──────────────┼──────────────┘
                   ▼
             Priority Engine
                   │
                   ▼
          Duplicate Detection
                   │
                   ▼
          Department Router
                   │
                   ▼
               SLA Engine
                   │
                   ▼
             Human Review
                   │
                   ▼
              Resolution
                   │
                   ▼
             Analytics Engine
             ┌─────┼─────┐
             ▼     ▼     ▼
         Hotspots Trends Prediction
```

---

# 10. System Architecture

```text
┌──────────────────────────────────────────────┐
│                 STREAMLIT UI                 │
│                                              │
│ Passenger | Operator | Admin | Analytics     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                FASTAPI BACKEND               │
│                                              │
│ Complaint API | User API | Analytics API     │
└──────────────────────┬───────────────────────┘
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
             AI     BUSINESS  DATABASE
          SERVICES    LOGIC    │
              │        │       │
              ▼        ▼       ▼
           NLP/ML    SLA/Router SQLite/Postgres
              │
              ▼
       Models / Embeddings
```

---

# 11. Database Specification

## complaints

Fields:

- id
- complaint_id
- complaint_text
- complaint_type
- subcategory
- train_number
- train_name
- station
- coach
- seat
- incident_datetime
- priority
- priority_score
- sentiment
- language
- department
- status
- sla_deadline
- created_at
- updated_at
- resolved_at

## ai_predictions

- id
- complaint_id
- model_name
- model_version
- category
- category_confidence
- priority
- priority_confidence
- sentiment
- sentiment_confidence
- created_at

## departments

- id
- department_name
- category
- default_sla
- active

## assignments

- id
- complaint_id
- department
- assigned_to
- assigned_at
- status

## resolutions

- id
- complaint_id
- resolution_text
- resolution_type
- resolved_at
- resolution_time

## complaint_clusters

- id
- cluster_id
- complaint_id
- similarity_score
- cluster_label

Add appropriate database indexes where useful.

---

# 12. API Specification

## Complaint APIs

```text
POST   /api/v1/complaints
GET    /api/v1/complaints
GET    /api/v1/complaints/{id}
PATCH  /api/v1/complaints/{id}
DELETE /api/v1/complaints/{id}
```

## AI APIs

```text
POST /api/v1/ai/analyze
POST /api/v1/ai/classify
POST /api/v1/ai/extract-entities
POST /api/v1/ai/detect-duplicates
POST /api/v1/ai/predict-resolution
```

## Operations

```text
POST  /api/v1/complaints/{id}/assign
PATCH /api/v1/complaints/{id}/status
POST  /api/v1/complaints/{id}/resolve
```

## Analytics

```text
GET /api/v1/analytics/overview
GET /api/v1/analytics/trends
GET /api/v1/analytics/hotspots
GET /api/v1/analytics/sla
GET /api/v1/analytics/categories
GET /api/v1/analytics/trains
GET /api/v1/analytics/stations
```

Use Pydantic request/response schemas and proper HTTP status codes.

---

# 13. Frontend Specification

## Page 1 — Overview

KPIs:

- Total Complaints
- Open Complaints
- Resolved Complaints
- Critical Complaints
- SLA Breaches
- Average Resolution Time
- AI Automation Rate

Charts:

- Complaint Trend
- Category Distribution
- Priority Distribution
- SLA Performance

## Page 2 — Submit Complaint

Fields:

- Complaint Description
- Train Number
- Coach
- Seat
- Station
- Incident Date
- Evidence Upload

Action:

```text
Analyze Complaint
```

## Page 3 — AI Analysis

Display:

- Category
- Subcategory
- Entities
- Priority
- Sentiment
- Department
- SLA
- Confidence
- Explanation
- Duplicate status

## Page 4 — Complaint Queue

Filters:

- Category
- Priority
- Department
- Train
- Station
- Status
- SLA
- Date

Sorting:

- Newest
- Oldest
- Highest Priority
- SLA Risk

## Page 5 — SLA Monitor

Display:

- Within SLA
- Approaching SLA
- Breached SLA
- Average Response Time
- Average Resolution Time

## Page 6 — Hotspot Analytics

Display:

- India / Maharashtra map
- Station heatmap
- Train hotspots
- Complaint density
- SLA breach hotspots

## Page 7 — Train Intelligence

Search:

- Train number

Display:

- Complaint volume
- Top categories
- Complaint trend
- Worst coaches
- SLA performance
- Average resolution
- Risk score

## Page 8 — Station Intelligence

Display:

- Station complaint volume
- Top issues
- Peak hours
- SLA performance
- Trend
- Hotspot status

## Page 9 — Incident Clusters

Display:

- Cluster ID
- Number of complaints
- Common issue
- Train
- Coach
- Station
- Similarity
- Status

Example:

```text
INC-042
AC Failure — Coach B4
27 complaints
Similarity: 91%
Status: ACTIVE INCIDENT
```

## Page 10 — Model Performance

Display:

- Classification Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
- Prediction Confidence
- Human Review Rate

Only display metrics that were actually calculated.

---

# 14. Dataset Specification

Use synthetic railway complaint data for the public portfolio version.

Initial target:

**10,000 complaints**

Fields:

```text
complaint_id
complaint_text
category
subcategory
train_number
train_name
station
coach
seat
priority
department
sentiment
status
created_at
resolved_at
resolution_time
```

Dataset should intentionally contain:

- Short complaints
- Long complaints
- Typos
- Hinglish
- Hindi
- Ambiguous complaints
- Angry complaints
- Duplicate complaints
- Multi-issue complaints

Generation should be reproducible.

Do not create meaningless random text.

---

# 15. Machine Learning Specification

## Model 1 — Complaint Classification

Baseline:

```text
TF-IDF
   +
Logistic Regression
```

Advanced:

```text
Sentence Transformer
       +
Classifier
```

Metrics:

- Accuracy
- Precision
- Recall
- Macro F1
- Weighted F1
- Confusion Matrix

Do not fabricate results.

## Model 2 — Resolution Prediction

Inputs:

- Category
- Priority
- Department
- Station
- Train
- Time
- Historical workload

Metrics:

- MAE
- RMSE
- R²

## Model 3 — Duplicate Detection

```text
Sentence Transformer
        ↓
Embeddings
        ↓
Cosine Similarity
```

## Model 4 — Complaint Clustering

```text
Embeddings
    ↓
Clustering
    ↓
Recurring incident groups
```

---

# 16. AI Confidence System

Every AI prediction must include:

- prediction
- confidence
- model_version
- timestamp

Example:

```text
Category:
AC

Confidence:
94.3%

Model:
complaint_classifier_v1.0
```

---

# 17. Human Review System

Low-confidence predictions enter:

```text
AI REVIEW QUEUE
```

Example:

```text
Complaint #RAI-1204

AI:
Category = Electrical
Confidence = 57%

Actions:
[Approve]
[Change Category]
```

Human corrections should be stored for future training/retraining.

---

# 18. Security & Privacy

## Security

- Keep secrets outside source code.
- Use `.env` locally.
- Use deployment secrets in cloud.
- Never commit `.env`.
- Validate uploaded files.
- Limit upload size.
- Sanitize user input.
- Avoid exposing stack traces.

## Privacy

Public project must use synthetic/anonymized data only.

Never upload/store real:

- PNR
- mobile numbers
- passenger names
- addresses
- railway employee information

---

# 19. Testing Specification

Target:

**30+ meaningful automated tests**

## Unit tests

- classifier
- entity extraction
- priority
- routing
- SLA
- duplicate detection
- resolution prediction

## API tests

- POST complaint
- GET complaint
- PATCH status
- POST analysis
- POST assignment
- POST resolution

## UI tests / smoke checks

Verify:

- dashboard loads
- complaint submission works
- AI analysis displays
- filters work
- charts render
- invalid input is handled

Tests should verify behavior, not merely inflate test count.

---

# 20. Performance Targets

Prototype targets:

```text
API response      < 2 seconds
AI text analysis  < 5 seconds
Dashboard load    < 5 seconds
DB query          < 1 second
```

These are targets, not guarantees.

---

# 21. Deployment Specification

## Recommended zero-cost architecture

```text
GitHub
   ↓
Streamlit Community Cloud
   ├── Streamlit UI
   ├── ML models
   └── Analytics
```

For the first version, keep the application sufficiently monolithic to avoid unnecessary hosting complexity.

Optional advanced architecture:

```text
Streamlit
    ↓
FastAPI
    ↓
PostgreSQL
```

Deployment must not require paid infrastructure.

---

# 22. Repository Specification

Recommended structure:

```text
railhelpai/
│
├── app/
│   ├── frontend/
│   ├── backend/
│   ├── ai/
│   └── database/
│
├── models/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
│
├── notebooks/
│
├── scripts/
│
├── tests/
│
├── docs/
│
├── screenshots/
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

The implementation may use a more modular structure if it remains understandable and aligned with the specification.

---

# 23. Recommended Development Phases

## Phase 0 — Foundation & Planning

Create:

- Architecture
- Repository structure
- Database design
- API design
- AI pipeline design
- Development roadmap
- Testing strategy
- Dataset strategy

Deliverable:

A documented implementation plan.

Do not implement advanced AI.

---

## Phase 1 — Foundation

Build:

- Project setup
- Database
- FastAPI
- Streamlit
- Complaint CRUD
- Configuration
- Logging
- Health endpoint
- Basic validation

Deliverable:

Working complaint-management application.

---

## Phase 2 — AI Core

Build:

- Synthetic dataset
- Preprocessing
- Complaint classification
- Entity extraction
- Sentiment
- Priority
- Department routing

Deliverable:

Working AI complaint pipeline.

---

## Phase 3 — Operations

Build:

- SLA
- Escalation
- Status workflow
- Operator dashboard
- Human review queue
- Resolution workflow

Deliverable:

End-to-end complaint lifecycle.

---

## Phase 4 — Intelligence

Build:

- Sentence embeddings
- Duplicate detection
- Complaint clustering
- Resolution prediction
- Hotspot detection
- Train intelligence
- Station intelligence

Deliverable:

AI-powered operational analytics.

---

## Phase 5 — Advanced AI

Select only the features that can be implemented reliably:

- OCR
- Image analysis
- Multilingual/Hinglish
- Chatbot
- Summarization

Deliverable:

Multimodal intelligent complaint platform.

---

## Phase 6 — Production-Inspired Polish

Build:

- Automated tests
- Logging
- Error handling
- Model versioning
- Explainability
- Documentation
- Deployment
- Screenshots
- Demo video

Deliverable:

Resume-ready portfolio project.

---

# 24. MVP Definition

MVP is complete when:

```text
1. Submit complaint
        ↓
2. AI classifies it
        ↓
3. Entities extracted
        ↓
4. Priority calculated
        ↓
5. Department selected
        ↓
6. SLA assigned
        ↓
7. Complaint enters queue
        ↓
8. Operator resolves it
        ↓
9. Dashboard updates
```

Administrator must be able to see:

- Total complaints
- Open complaints
- Priority distribution
- Category distribution
- SLA status
- Department workload
- Train hotspots
- Station hotspots

---

# 25. Resume-Flagship Definition

The project becomes substantially stronger when it includes:

- Semantic duplicate detection
- Complaint clustering
- Resolution-time prediction
- Explainable AI
- Human-in-the-loop
- OCR
- Image analysis
- Multilingual/Hinglish
- AI chatbot
- Model evaluation
- Model versioning
- Automated tests
- Public deployment

Do not attempt every advanced feature if quality suffers.

**MVP + 3–4 excellent advanced features is preferable to 15 half-working features.**

---

# 26. Success Criteria

## Functional

- Complaints can be submitted.
- Complaints are classified.
- Entities are extracted.
- Priority is generated.
- Department is assigned.
- SLA is calculated.
- Status can be updated.
- Analytics are generated.

## ML

- Model has measurable evaluation metrics.
- Dataset is reproducible.
- Predictions have confidence.
- Low-confidence predictions go to human review.

## Engineering

- Modular code
- REST APIs
- Database
- Error handling
- Automated tests
- Git version control
- Documentation

## Deployment

- Application runs publicly.
- No paid API is required.
- No secret keys are exposed.
- Demo uses synthetic data.

---

# 27. Project Limitations — Must Be in README

The README must explicitly state:

1. This is an educational prototype.
2. It is not affiliated with Indian Railways.
3. It does not connect to RailMadad production systems.
4. Complaint data is synthetic.
5. SLA values are configurable demonstration values.
6. AI predictions are advisory.
7. Resolution predictions are not guarantees.
8. Image/OCR performance depends on input quality.
9. Free cloud resources may have limitations.

---

# 28. Final Technology Stack

```text
Python
│
├── FastAPI
├── Streamlit
├── SQLite / PostgreSQL
├── scikit-learn
├── spaCy
├── Sentence Transformers
├── Hugging Face
├── Tesseract OCR
├── Pandas
├── NumPy
├── Plotly
└── Folium
```

---

# 29. Engineering Principles

## Prefer correctness over feature count

Do not add a feature unless its underlying functionality works.

## Prefer reproducibility

Dataset generation, model training, and evaluation must be reproducible.

## Prefer explainability

Important AI decisions should expose prediction confidence and understandable reasons.

## Prefer modularity

Keep:

- API
- business logic
- database
- AI services
- UI

separated.

## Prefer graceful degradation

Optional AI features must fail safely.

## Prefer local/free tooling

The core project must work without paid AI APIs.

## Prefer real evaluation

Every ML model must have actual evaluation code.

## Prefer synthetic data

Public deployment must not depend on real passenger information.

---

# 30. Antigravity Execution Protocol

When asked to implement a phase:

### Step 1 — Inspect

Inspect the current repository and existing implementation.

### Step 2 — Plan

Identify:

- files to create
- files to modify
- dependencies
- risks
- tests
- verification steps

### Step 3 — Implement

Make focused changes.

### Step 4 — Run

Run relevant commands, tests, and application checks.

### Step 5 — Verify

Verify:

- functionality
- API behavior
- UI behavior
- database behavior
- model behavior

### Step 6 — Fix

Resolve discovered issues.

### Step 7 — Document

Update relevant documentation.

### Step 8 — Report

Provide:

- what changed
- files changed
- tests run
- verification results
- known limitations
- next recommended task

Do not claim completion without verification.

---

# 31. Change Control

Before changing a core requirement:

1. Identify the conflict.
2. Explain the proposed change.
3. Explain the impact.
4. Prefer the original specification unless there is a strong engineering reason.
5. Record approved architectural changes in documentation.

Do not silently replace requirements with unrelated architecture.

---

# 32. Definition of Done

A feature is considered complete only when:

- implementation exists
- expected behavior works
- invalid/error cases are handled
- relevant tests exist
- tests pass
- UI/API integration is verified where applicable
- documentation is updated
- no fake data/metrics are presented as real
- no secrets are committed

---

# 33. Immediate Starting Task

When this specification is first introduced to the Agent:

**DO NOT implement the full application.**

First:

1. Inspect the workspace.
2. Read this specification completely.
3. Analyze the current repository state.
4. Propose the architecture.
5. Propose the repository structure.
6. Propose the database schema.
7. Propose the API structure.
8. Propose the AI pipeline.
9. Propose the development roadmap.
10. Identify dependencies.
11. Identify implementation risks.
12. Identify zero-cost/local alternatives.
13. Identify the first implementation milestone.
14. Produce a clear implementation plan/artifact.
15. STOP and wait for approval before implementing Phase 1.

---

# 34. Important Disclaimer

RailHelpAI is an educational/portfolio prototype.

It is not affiliated with Indian Railways.

It does not connect to RailMadad production systems.

Its complaint data is synthetic/anonymized.

Its SLA values are demonstration/configurable values.

Its AI predictions are advisory.

Its resolution predictions are estimates.

It does not make real railway operational decisions.

---

# 35. Build Strategy

The intended implementation sequence is:

```text
MVP
 ↓
AI Core
 ↓
SLA / Operations
 ↓
Duplicate Detection
 ↓
Analytics
 ↓
Resolution Prediction
 ↓
2–3 Advanced AI Features
 ↓
Testing
 ↓
Deployment
 ↓
Documentation / Demo
```

The goal is a technically credible, portfolio-ready project that is production-inspired without pretending to be production railway infrastructure.

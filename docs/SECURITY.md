# RailHelpAI — Security Architecture & Guidelines

> **Version:** v1.0 (Phase 6 Final Release)  

---

## 1. Security Controls
- **Request Correlation IDs:** `X-Request-ID` middleware traces every HTTP request.
- **Image Security Validator:** $\le 5$MB size restriction, MIME magic check, EXIF metadata stripper.
- **Data Protection:** No credentials committed to source; `.env` listed in `.gitignore`.
- **Database Safety:** SQLite foreign key enforcement (`PRAGMA foreign_keys=ON;`), parameterized queries.

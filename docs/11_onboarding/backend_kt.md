# Backend Knowledge Transfer (KT) Guide

## Audience

New backend engineers joining the CHECK-360 team.

## Prerequisites

- Python 3.10+ experience
- FastAPI or Flask familiarity
- SQL/PostgreSQL basics
- Git proficiency

## Day 1: Architecture Overview

### Reading (2 hours)
1. [Product Vision](../00_overview/product_vision.md)
2. [System Overview](../02_architecture/system_overview.md)
3. [Data Flow](../02_architecture/data_flow.md)

### Exercise
- Clone repo, set up local environment
- Run `uvicorn src.main:app --reload`
- Hit `/health` endpoint

## Day 2: Database & Models

### Reading (2 hours)
1. Review all models in `src/models/`
2. Study migrations in `src/migrations/`

### Exercise
- Run all migrations locally
- Create a test candidate via API
- Query database directly

## Day 3: Core Services

### Reading (2 hours)
1. [Verification Session](../05_services/verification_session.md)
2. [Trust Score Engine](../05_services/trust_score_engine.md)

### Exercise
- Trace a verification flow in code
- Run `scripts/create_sample_data.py`
- Verify trust score calculation

## Day 4: Vendor Integrations

### Reading (2 hours)
1. [Surepass Integration](../05_services/surepass_integration.md)
2. [Face Verification](../05_services/face_verification.md)

### Exercise
- Test mock mode for Surepass
- Test mock mode for Face
- Review error handling

## Day 5: API & HR Flows

### Reading (2 hours)
1. [HR API](../06_api_contracts/hr_api.md)
2. [HR Review Flow](../07_workflows/hr_review_flow.md)

### Exercise
- Test all HR endpoints via Swagger
- Simulate an override flow
- Review audit trail

## Key Files to Know

| File | Purpose |
|------|---------|
| `src/main.py` | Application entry point |
| `src/services/trust_score/calculator.py` | Core scoring logic |
| `src/services/document/analyze.py` | Forensic engine |
| `src/api/routes/hr.py` | HR API endpoints |
| `src/models/trust_score.py` | Score data model |

## Common Tasks

| Task | How |
|------|-----|
| Add new API endpoint | Create in `src/api/routes/`, register in `main.py` |
| Add new model | Create in `src/models/`, update `__init__.py` |
| Add migration | Create SQL file in `src/migrations/` |
| Test locally | `pytest` or manual API calls |

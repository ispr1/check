# HR API Contract

**Base URL:** `/api/v1/hr`

## Authentication
Requires `Bearer <JWT>` with role `HR` or `ADMIN`.

## Endpoints

### 1. Get Candidate Summary
`GET /candidates/{candidate_id}/summary`

**Response:**
```json
{
  "candidate": { ... },
  "trust_score": {
    "score": 85.5,
    "status": "VERIFIED",
    "deductions": [
        {"category": "face", "reason": "Low Confidence", "points": 10}
    ]
  },
  "documents": { ... },
  "decisions": [ ... ]
}
```

### 2. Upload HR Document
`POST /documents/upload`

**Form Data:**
*   `file`: (Binary)
*   `document_type`: "education" | "experience"
*   `candidate_id`: Int

**Behavior:**
*   Uploads to S3.
*   Triggers auto-analysis.
*   Does **NOT** update Trust Score (HR uploads are supplementary).

### 3. Record Decision
`POST /decision/{verification_id}`

**Payload:**
```json
{
  "decision": "APPROVED",
  "reason_codes": ["SCORE_OK"],
  "comments": "Looks good."
}
```

**Constraints:**
*   Immutable. Cannot be edited once submitted.

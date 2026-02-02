# Trust Score API

**Base URL:** `/api/v1/trust-score`  
**Authentication:** Bearer Token (HR/Admin)

---

## Endpoints

### 1. Get Trust Score

`GET /trust-score/{verification_id}`

**Response:**
```json
{
  "id": 1,
  "verification_id": 14,
  "score": 96.2,
  "status": "VERIFIED",
  "completion_rate": 100.0,
  "breakdown": {
    "aadhaar": 20.0,
    "pan": 10.0,
    "uan": 10.0,
    "face": 25.0,
    "documents": 21.2,
    "cross_match": 10.0
  },
  "flags": ["DOCUMENTS_ACCEPTABLE_LEGITIMACY_80%"],
  "recommendations": ["Review experience document"],
  "is_overridden": false,
  "calculated_at": "2026-02-02T06:01:38Z"
}
```

**Errors:**
- `404`: Trust score not calculated yet

---

### 2. Calculate Trust Score

`POST /trust-score/{verification_id}/calculate`

**Purpose:** Manually trigger score calculation.

**Response:**
```json
{
  "score": 85.5,
  "status": "VERIFIED",
  "flags": [],
  "message": "Trust score calculated"
}
```

---

### 3. Override Trust Score

`POST /trust-score/{verification_id}/override`

**Request:**
```json
{
  "adjustment": 15.0,
  "reason": "EXPLAINABLE",
  "comment": "Marriage certificate verified for name change"
}
```

**Response:**
```json
{
  "message": "Override applied",
  "new_score": 80.5,
  "previous_score": 65.5,
  "is_overridden": true
}
```

**Authorization:** Requires `senior_hr` or `admin` role.

---

## Status Values

| Status | Score Range | Description |
|--------|-------------|-------------|
| `VERIFIED` | ≥ 85 | Auto-approvable |
| `REVIEW_REQUIRED` | 70-84 | HR must review |
| `HIGH_RISK` | 50-69 | Senior HR review |
| `FLAGGED` | < 50 | Cannot proceed without override |
| `NOT_CALCULATED` | N/A | Pending calculation |

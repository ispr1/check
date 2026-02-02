# Public Candidate API

**Base URL:** `/api/v1`  
**Authentication:** Bearer Token (Verification Session Token)

## Overview

These endpoints are used by candidates during the verification process.

---

## Endpoints

### 1. Start Verification Session

`GET /verify/{token}`

**Purpose:** Validate token and retrieve session info.

**Response:**
```json
{
  "verification_id": 123,
  "candidate_name": "Rajesh Kumar",
  "company_name": "Acme Corp",
  "steps_required": ["aadhaar", "pan", "face", "documents"],
  "expires_at": "2026-02-05T10:00:00Z"
}
```

**Errors:**
- `410`: Token expired
- `404`: Token not found

---

### 2. Submit Aadhaar

`POST /steps/aadhaar/verify`

**Request:**
```json
{
  "verification_id": 123,
  "aadhaar_number": "123456789012"
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "message": "Aadhaar verified successfully"
}
```

---

### 3. Upload Document

`POST /documents/analyze`

**Request (multipart/form-data):**
- `file`: PDF/Image
- `document_type`: "education" | "experience"
- `candidate_id`: int
- `verification_request_id`: int

**Response:**
```json
{
  "id": 456,
  "legitimacy_score": 87.5,
  "status": "LEGITIMATE",
  "flags": []
}
```

---

### 4. Submit Selfie for Face Match

`POST /steps/face/compare`

**Request:**
```json
{
  "verification_id": 123,
  "selfie_base64": "base64-encoded-image"
}
```

**Response:**
```json
{
  "decision": "MATCH",
  "confidence": 94.5
}
```

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| All Candidate APIs | 60/min per session |

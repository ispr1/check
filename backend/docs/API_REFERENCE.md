# CHECK-360 API Reference

Complete guide to all API endpoints with examples.

---

## Authentication

All protected APIs require a **Bearer Token** in the header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

---

## 1. Authentication APIs

### 1.1 Login

Get an access token to use other APIs.

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
```json
{
  "email": "admin@check360.com",
  "password": "admin123"
}
```

**Response (Success):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (Error):**
```json
{
  "detail": "Incorrect email or password"
}
```

**Testing with curl:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@check360.com", "password": "admin123"}'
```

---

## 2. Candidate APIs (HR Portal)

### 2.1 Create Candidate

**Endpoint:** `POST /api/v1/candidates`  
**Auth Required:** Yes

**Request:**
```json
{
  "full_name": "Rajesh Kumar",
  "email": "rajesh@example.com",
  "dob": "1990-05-15"
}
```

**Response:**
```json
{
  "id": 1,
  "full_name": "Rajesh Kumar",
  "email": "rajesh@example.com",
  "dob": "1990-05-15",
  "company_id": 1,
  "created_at": "2026-01-27T12:00:00"
}
```

### 2.2 List Candidates

**Endpoint:** `GET /api/v1/candidates`  
**Auth Required:** Yes

**Response:**
```json
[
  {
    "id": 1,
    "full_name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "dob": "1990-05-15"
  },
  {
    "id": 2,
    "full_name": "Priya Sharma",
    "email": "priya@example.com",
    "dob": "1992-08-20"
  }
]
```

---

## 3. Verification APIs (HR Portal)

### 3.1 Start Verification

Creates a verification session and generates a link for the candidate.

**Endpoint:** `POST /api/v1/verifications/start`  
**Auth Required:** Yes

**Request:**
```json
{
  "candidate_id": 1,
  "include_uan": true,
  "include_education": false,
  "include_experience": false
}
```

**Response:**
```json
{
  "id": 1,
  "token": "abc123def456...",
  "verification_url": "https://check360.com/verify/abc123def456...",
  "status": "PENDING",
  "expires_at": "2026-02-03T12:00:00",
  "steps": [
    {"step_type": "PERSONAL_INFO", "is_mandatory": true, "status": "PENDING"},
    {"step_type": "FACE_LIVENESS", "is_mandatory": true, "status": "PENDING"},
    {"step_type": "AADHAAR", "is_mandatory": true, "status": "PENDING"},
    {"step_type": "PAN", "is_mandatory": true, "status": "PENDING"},
    {"step_type": "UAN", "is_mandatory": false, "status": "PENDING"}
  ]
}
```

### 3.2 Get Verification Status

**Endpoint:** `GET /api/v1/verifications/{verification_id}`  
**Auth Required:** Yes

**Response:**
```json
{
  "id": 1,
  "status": "IN_PROGRESS",
  "candidate": {
    "full_name": "Rajesh Kumar",
    "email": "rajesh@example.com"
  },
  "steps": [
    {"step_type": "PERSONAL_INFO", "status": "COMPLETED"},
    {"step_type": "FACE_LIVENESS", "status": "COMPLETED"},
    {"step_type": "AADHAAR", "status": "COMPLETED", "flags": []},
    {"step_type": "PAN", "status": "PENDING"},
    {"step_type": "UAN", "status": "PENDING"}
  ]
}
```

---

## 4. Candidate Verification APIs (Public - No Auth)

These APIs are used by candidates via the verification link.

### 4.1 Get Verification Session

**Endpoint:** `GET /api/v1/verify/{token}`

**Response:**
```json
{
  "status": "IN_PROGRESS",
  "candidate_name": "Rajesh Kumar",
  "steps": [
    {"step_type": "PERSONAL_INFO", "status": "PENDING", "is_mandatory": true},
    {"step_type": "FACE_LIVENESS", "status": "PENDING", "is_mandatory": true},
    {"step_type": "AADHAAR", "status": "PENDING", "is_mandatory": true},
    {"step_type": "PAN", "status": "PENDING", "is_mandatory": true}
  ],
  "can_submit": false
}
```

### 4.2 Submit Personal Info

**Endpoint:** `POST /api/v1/verify/{token}/personal-info`

**Request:**
```json
{
  "phone": "9876543210",
  "current_address": "123, MG Road, Bangalore - 560001"
}
```

**Response:**
```json
{
  "step_type": "PERSONAL_INFO",
  "status": "COMPLETED",
  "message": "Personal information saved"
}
```

### 4.3 Submit Face (Selfie)

**Endpoint:** `POST /api/v1/verify/{token}/face`

**Request:**
```json
{
  "selfie_image_base64": "/9j/4AAQSkZJRg..."
}
```

> **Note:** In Phase 2, face is stored only. ML verification happens in Phase 3.

### 4.4 Aadhaar OTP Flow

#### Step 1: Generate OTP

**Endpoint:** `POST /api/v1/verify/{token}/aadhaar/generate-otp`

**Request:**
```json
{
  "aadhaar_number": "234567891234"
}
```

**Response:**
```json
{
  "message": "OTP sent to registered mobile",
  "client_id": "surepass_client_id_here"
}
```

#### Step 2: Submit OTP

**Endpoint:** `POST /api/v1/verify/{token}/aadhaar/submit-otp`

**Request:**
```json
{
  "client_id": "surepass_client_id_here",
  "otp": "123456"
}
```

**Response:**
```json
{
  "step_type": "AADHAAR",
  "status": "COMPLETED",
  "verification_result": {
    "status": "MATCH",
    "confidence": "HIGH",
    "details": {
      "name_match": true,
      "name_score": 95,
      "dob_match": true
    }
  }
}
```

### 4.5 PAN Verification

**Endpoint:** `POST /api/v1/verify/{token}/pan`

**Request:**
```json
{
  "pan_number": "ABCDE1234F"
}
```

**Response:**
```json
{
  "step_type": "PAN",
  "status": "COMPLETED",
  "verification_result": {
    "status": "MATCH",
    "confidence": "HIGH",
    "details": {
      "name_match": true,
      "dob_match": true,
      "aadhaar_seeding": "LINKED"
    }
  }
}
```

### 4.6 UAN Verification

**Endpoint:** `POST /api/v1/verify/{token}/uan`

**Request:**
```json
{
  "uan_number": "123456789012",
  "claimed_experience_years": 5
}
```

**Response:**
```json
{
  "step_type": "UAN",
  "status": "COMPLETED",
  "verification_result": {
    "status": "PARTIAL_MATCH",
    "confidence": "MEDIUM",
    "flags": ["OVERLAPPING_EMPLOYMENT"],
    "details": {
      "identity_match": true,
      "total_experience_years": 5,
      "employers_count": 3,
      "has_overlaps": true
    }
  }
}
```

### 4.7 Submit Final Verification

**Endpoint:** `POST /api/v1/verify/{token}/submit`

**Request:** (empty body)

**Response:**
```json
{
  "status": "COMPLETED",
  "message": "Verification submitted successfully",
  "summary": {
    "total_steps": 5,
    "completed": 5,
    "failed": 0
  }
}
```

---

## 5. Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (no/invalid token) |
| 404 | Not Found |
| 422 | Validation Error (wrong data format) |
| 500 | Server Error |
| 502 | External API Error (Surepass down) |

---

## 6. Verification Status Reference

### Step Statuses

| Status | Meaning |
|--------|---------|
| PENDING | Not yet submitted |
| COMPLETED | Successfully verified |
| FAILED | Verification failed |
| SKIPPED | Optional step skipped |

### Verification Statuses

| Status | Meaning |
|--------|---------|
| PENDING | Just created |
| IN_PROGRESS | Candidate started |
| COMPLETED | All steps done |
| EXPIRED | Token expired (7 days) |

### Comparison Results (External)

| Result | Meaning |
|--------|---------|
| MATCH | All data matches |
| PARTIAL_MATCH | Some data matches |
| MISMATCH | Data does not match |
| NOT_AVAILABLE | Could not verify |

---

## 7. Testing Workflow

### Complete Test Flow

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@check360.com", "password": "admin123"}' | jq -r '.access_token')

# 2. Create Candidate
CANDIDATE=$(curl -s -X POST http://localhost:8000/api/v1/candidates \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"full_name": "Test User", "email": "test@example.com", "dob": "1990-01-01"}')

CANDIDATE_ID=$(echo $CANDIDATE | jq -r '.id')

# 3. Start Verification
VERIFICATION=$(curl -s -X POST http://localhost:8000/api/v1/verifications/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"candidate_id\": $CANDIDATE_ID, \"include_uan\": true}")

VERIFY_TOKEN=$(echo $VERIFICATION | jq -r '.token')

# 4. Submit Steps (as candidate)
curl -X POST http://localhost:8000/api/v1/verify/$VERIFY_TOKEN/personal-info \
  -H "Content-Type: application/json" \
  -d '{"phone": "9876543210", "current_address": "Test Address"}'

# Continue with other steps...
```

---

*API Version: 2.5.0 | Last Updated: January 2026*

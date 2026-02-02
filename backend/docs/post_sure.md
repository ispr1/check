# Surepass API Reference

> Source: [Postman Documentation](https://documenter.getpostman.com/view/29589138/2s9YBz4GEX)

---

## Overview

Surepass provides KYC verification APIs for Indian identity documents.

### Trial Usage
- **Aadhaar API**: 3-day trial with 50 requests limit
- Contact: `techsupport@surepass.io` to start trial

---

## Endpoints

### Base URLs

| Environment | Base URL |
|-------------|----------|
| **Production** | `https://kyc-api.surepass.io/api/v1` |
| **Sandbox** | `https://sandbox.surepass.io/api/v1` |

All requests must be made over **HTTPS**.

---

## Authentication

Token-based authentication via Bearer token in headers.

```
Authorization: Bearer <YOUR_TOKEN>
```

- **Live tokens**: For production
- **Sandbox tokens**: For testing (50 trial credits)

---

## Response Format

All responses are wrapped in a `data` tag:

```json
{
    "data": {
        "pan_number": "AAAPM1234L",
        "full_name": "MUNNA BHAIYA",
        "father_name": "KALEEN BHAIYA",
        "client_id": "takdTqhCxo",
        "dob": "1990-01-01"
    },
    "status_code": 200,
    "message": "",
    "success": true
}
```

---

## Status Codes

### Success Codes

| Code | Name | Meaning |
|------|------|---------|
| 200 | OK | Successful Request |
| 201 | Created | Resource successfully created |
| 202 | Accepted | Async request - response sent to webhook |
| 204 | No Content | Successful with no response |

### Error Codes

| Code | Name | Meaning |
|------|------|---------|
| 400 | Bad Request | Malformed request |
| 401 | Unauthorized | Invalid authorization credentials |
| 403 | Forbidden | Action prohibited |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit reached |
| 500 | Internal Server Error | Unexpected API error |

---

## API Endpoints

### PAN Verification

#### PAN Udyam Check 
`POST /corporate/pan-udyam-check`

**Request Body:**
```json
{
    "pan_number": "ABBCS1234D",
    "full_name": "SURJAL PRIVATE LIMITED",
    "dob": "2018-11-15"
}
```

**Response:**
```json
{
    "data": {
        "client_id": "unique_id",
        "pan_number": "ABBCS1234D",
        "udyam_exists": true,
        "migration_status": "migrated"
    },
    "status_code": 200,
    "success": true
}
```

**migration_status values:**
- `migrated`
- `not_migrated`

---

### Aadhaar Verification (OTP-based)

#### Generate OTP
`POST /aadhaar-v2/generate-otp`

**Request Body:**
```json
{
    "id_number": "123456789012"
}
```

**Response:**
```json
{
    "data": {
        "client_id": "abc123"
    },
    "status_code": 200,
    "success": true,
    "message": "OTP sent successfully"
}
```

#### Submit OTP
`POST /aadhaar-v2/submit-otp`

**Request Body:**
```json
{
    "client_id": "abc123",
    "otp": "123456"
}
```

**Response:**
```json
{
    "data": {
        "full_name": "RAJESH KUMAR",
        "dob": "15-05-1990",
        "gender": "M",
        "address": {
            "house": "123",
            "street": "MG Road",
            "district": "Bangalore",
            "state": "Karnataka",
            "pincode": "560001"
        },
        "photo": "base64_encoded_string"
    },
    "status_code": 200,
    "success": true
}
```

---

### DigiLocker

#### Initialize Session
`POST /digilocker/init`

**Request Body:**
```json
{
    "callback_url": "https://your-domain.com/callback",
    "documents": ["AADHAAR", "PAN"]
}
```

#### Fetch Documents
`POST /digilocker/fetch`

**Request Body:**
```json
{
    "session_id": "session_xyz"
}
```

---

### UAN/Employment Verification

#### Employment History UAN V2
`POST /employment/employment-history-uan-v2`

**Request Body:**
```json
{
    "uan_number": "123456789012"
}
```

**Response:**
```json
{
    "data": {
        "member_name": "RAJESH KUMAR",
        "dob": "1990-05-15",
        "establishments": [
            {
                "establishment_name": "ABC Corp",
                "date_of_joining": "2020-01-15",
                "date_of_exit": "2022-06-30"
            }
        ]
    },
    "status_code": 200,
    "success": true
}
```

---

## cURL Examples

### PAN Verification
```bash
curl --location 'https://kyc-api.surepass.io/api/v1/corporate/pan-udyam-check' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "pan_number": "ABBCS1234D",
    "full_name": "SURJAL SERVICES PRIVATE LIMITED",
    "dob": "2018-11-15"
}'
```

### Aadhaar OTP Generate
```bash
curl --location 'https://sandbox.surepass.io/api/v1/aadhaar-v2/generate-otp' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "id_number": "123456789012"
}'
```

---

## Our Granted APIs

| API | Endpoint Path | Status |
|-----|---------------|--------|
| PAN Comprehensive | `identity/pan-comprehensive` | ❓ 404 - Need correct path |
| Digilocker Via Link | `identity/digilocker` | ❓ Untested |
| Employment UAN V2 | `employment/employment-history-uan-v2` | ❓ Untested |
| Aadhaar OTP | `aadhaar-v2/*` | ❌ 401 - Not in token scope |

---

## Testing Results (2026-01-28)

### Sandbox URL: `https://sandbox.surepass.io/api/v1`

| Endpoint | Status | Response |
|----------|--------|----------|
| `/identity/pan-comprehensive` | 404 | Not Found |
| `/aadhaar-v2/generate-otp` | 401 | Token not valid for this scope |

---

## Next Steps

1. **Contact Surepass** to get correct endpoint path for PAN Comprehensive
2. **Request Aadhaar trial** from `techsupport@surepass.io`
3. Test `/employment/employment-history-uan-v2` for UAN verification

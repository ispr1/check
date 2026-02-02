# API Error Codes

## Standard HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| `200` | Success | Request completed |
| `201` | Created | Resource created |
| `400` | Bad Request | Validation failed |
| `401` | Unauthorized | Missing/invalid token |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource doesn't exist |
| `410` | Gone | Token expired |
| `422` | Unprocessable | Valid format, invalid data |
| `429` | Rate Limited | Too many requests |
| `500` | Server Error | Unexpected failure |

---

## Application Error Codes

All error responses follow this structure:

```json
{
  "detail": "Human readable message",
  "error_code": "MACHINE_READABLE_CODE",
  "context": {}
}
```

### Authentication Errors

| Code | Message |
|------|---------|
| `AUTH_TOKEN_MISSING` | Authorization header required |
| `AUTH_TOKEN_INVALID` | Token is malformed or expired |
| `AUTH_TOKEN_EXPIRED` | Token has expired |
| `AUTH_INSUFFICIENT_ROLE` | User role cannot access this resource |

### Verification Errors

| Code | Message |
|------|---------|
| `VERIFICATION_NOT_FOUND` | Verification session does not exist |
| `VERIFICATION_EXPIRED` | Session has expired |
| `VERIFICATION_ALREADY_COMPLETED` | Cannot modify completed verification |
| `STEP_ALREADY_SUBMITTED` | This step was already submitted |

### Document Errors

| Code | Message |
|------|---------|
| `DOC_TOO_LARGE` | File exceeds 10MB limit |
| `DOC_INVALID_TYPE` | Only PDF and images allowed |
| `DOC_ANALYSIS_FAILED` | Could not analyze document |

### Vendor Errors

| Code | Message |
|------|---------|
| `SUREPASS_UNAVAILABLE` | Identity verification service down |
| `REKOGNITION_UNAVAILABLE` | Face verification service down |
| `VENDOR_RATE_LIMITED` | External API rate limit hit |

### Trust Score Errors

| Code | Message |
|------|---------|
| `SCORE_NOT_CALCULATED` | Trust score not yet calculated |
| `SCORE_INCOMPLETE_DATA` | Minimum data not provided |
| `OVERRIDE_NOT_ALLOWED` | User cannot override scores |

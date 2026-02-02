# Surepass Integration Service

## Responsibility

Wrapper around Surepass API for Government ID verification.

## Supported Verifications

| API | Purpose | Response Time |
|-----|---------|---------------|
| Aadhaar Verification | Validate Aadhaar + fetch demographics | 2-5s |
| PAN Validation | Validate PAN + fetch name/status | 1-3s |
| Aadhaar-PAN Link | Check if Aadhaar is linked to PAN | 1-2s |
| UAN Lookup | Fetch employment history from EPFO | 3-5s |

## Architecture

```
API Request → SurepassClient → Surepass API
                    ↓
              Response Validator
                    ↓
              Encrypt & Store
```

## Configuration

```env
SUREPASS_API_KEY=your-api-key
SUREPASS_BASE_URL=https://kyc-api.surepass.io/api/v1
SUREPASS_ENABLED=true  # false for mock mode
```

## Mock Mode

For development, `MockSurepassClient` returns predefined responses:

```python
if settings.SUREPASS_ENABLED:
    client = SurepassClient()
else:
    client = MockSurepassClient()
```

## Response Handling

All Surepass responses are:

1. **Validated** against expected schema.
2. **Encrypted** using Fernet before DB storage.
3. **Parsed** into domain models (e.g., `AadhaarVerification`).

## Error Codes

| Surepass Code | Our Interpretation |
|---------------|--------------------|
| `200` | Success |
| `422` | Invalid input (bad Aadhaar format) |
| `404` | Record not found in government DB |
| `500` | Vendor error (retry later) |

## Rate Limits

| API | Limit |
|-----|-------|
| Aadhaar | 100/min |
| PAN | 200/min |

Exceeded limits return `429 Too Many Requests`.

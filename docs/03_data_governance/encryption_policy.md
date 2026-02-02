# Encryption Policy

## Overview

All sensitive data in CHECK-360 is encrypted both at rest and in transit.

## Encryption at Rest

### Database Fields

| Field | Algorithm | Key Management |
|-------|-----------|----------------|
| Aadhaar Number | Fernet (AES-128-CBC) | `DATA_ENCRYPTION_KEY` env var |
| PAN Number | Fernet | Same |
| Phone Number | Fernet | Same |
| Surepass Raw Response | Fernet | Same |

**Implementation:**

```python
# src/utils/encryption.py
from cryptography.fernet import Fernet

cipher = Fernet(settings.DATA_ENCRYPTION_KEY)
encrypted = cipher.encrypt(plaintext.encode())
decrypted = cipher.decrypt(encrypted).decode()
```

### File Storage (S3)

| Object Type | Encryption | Key |
|-------------|------------|-----|
| Selfie Images | SSE-S3 | AWS Managed |
| ID Documents | SSE-S3 | AWS Managed |
| HR Uploads | SSE-S3 | AWS Managed |

**Bucket Policy:** Block public access. Private ACLs only.

## Encryption in Transit

| Connection | Protocol | Minimum Version |
|------------|----------|-----------------|
| Client → API | HTTPS | TLS 1.2 |
| API → PostgreSQL | SSL | Required |
| API → S3 | HTTPS | TLS 1.2 |
| API → Surepass | HTTPS | TLS 1.2 |
| API → Rekognition | HTTPS | TLS 1.2 |

## Key Rotation

| Key Type | Rotation Frequency | Procedure |
|----------|-------------------|-----------|
| `DATA_ENCRYPTION_KEY` | Annual | Re-encrypt affected columns |
| AWS IAM Keys | 90 days | Rotate via IAM console |
| JWT Secret | On breach | Invalidate all tokens |

## Key Storage

- **Production:** AWS Secrets Manager or SSM Parameter Store.
- **Development:** `.env` file (gitignored).

> ⚠️ **NEVER** commit encryption keys to version control.

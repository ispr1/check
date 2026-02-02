# PII Handling Policy

## Scope

This policy governs how CHECK-360 collects, processes, and stores Personal Identifiable Information (PII).

## PII Categories in CHECK-360

| Data Element | Classification | Storage | Access |
|--------------|----------------|---------|--------|
| Aadhaar Number | **Restricted** | Encrypted | Auth + Audit |
| PAN Number | **Restricted** | Encrypted | Auth + Audit |
| Full Name | Confidential | Encrypted | Auth |
| Date of Birth | Confidential | Encrypted | Auth |
| Phone Number | Confidential | Encrypted | Auth |
| Email | Confidential | Plaintext | Auth |
| Selfie Image | **Restricted** | S3 Private | Auth + Audit |
| ID Document | **Restricted** | S3 Private | Auth + Audit |

## Collection Principles

1. **Minimization:** Collect only what is required for verification.
2. **Consent:** Candidate must accept T&C before submission.
3. **Purpose Limitation:** Data used only for BGV, not marketing.

## Processing Rules

1. **Encryption in Transit:** All API calls use TLS 1.2+.
2. **Encryption at Rest:** All Restricted fields use AES-256.
3. **No Logging of PII:** `logger.info()` calls must NOT include raw PII.
4. **Masking:** When displaying Aadhaar to HR, show `XXXX-XXXX-1234`.

## Vendor Data

- Surepass responses (raw JSON) are stored encrypted.
- Rekognition responses do not contain PII (only confidence scores).

## Access Control

| Role | Can View PII | Can Export PII |
|------|--------------|----------------|
| Candidate | Own data only | No |
| HR | Company candidates | No |
| Admin | All | Audit-logged |
| System | N/A (automated) | N/A |

## Right to Erasure (DPDP Compliance)

Upon candidate request:
1. All PII is purged from DB.
2. S3 objects (images, docs) are deleted.
3. Audit log entry created: "Data Deleted per DPDP Request".

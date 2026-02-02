# Face Verification Service

## Responsibility

Biometric identity confirmation via face comparison.

## Process Flow

```
1. Candidate uploads Selfie
2. System retrieves Reference (from Aadhaar/ID)
3. AWS Rekognition compares faces
4. Result stored with confidence score
```

## Comparison Types

| Type | Source | Target | Use Case |
|------|--------|--------|----------|
| Selfie vs Aadhaar | Live selfie | Aadhaar photo | Primary identity |
| Selfie vs PAN | Live selfie | PAN photo | Fallback |
| Selfie vs Document | Live selfie | Photo from ID doc | When no Aadhaar |

## Decision Thresholds

| Confidence | Decision | Trust Impact |
|------------|----------|--------------|
| ≥ 90% | `MATCH` | None (verified) |
| 70-89% | `LOW_CONFIDENCE` | -10 points |
| < 70% | `MISMATCH` | -25 points |

## Providers

| Provider | Status | Usage |
|----------|--------|-------|
| AWS Rekognition | Production | Default |
| MockFaceProvider | Development | Testing |

**Toggle via:**
```env
FACE_PROVIDER=aws    # or "mock"
```

## Storage

| Item | Location | Access |
|------|----------|--------|
| Selfie | `s3://{bucket}/selfies/{candidate_id}.jpg` | Private |
| Reference | `s3://{bucket}/references/{candidate_id}.jpg` | Private |

## Anti-Spoofing

Rekognition provides passive liveness detection. For explicit liveness:
- Future: Integrate challenge-response video.

## Database Model

```sql
CREATE TABLE face_comparisons (
    id SERIAL PRIMARY KEY,
    verification_id INT REFERENCES verifications(id),
    candidate_id INT REFERENCES candidates(id),
    decision VARCHAR(50),  -- MATCH, LOW_CONFIDENCE, MISMATCH
    confidence_score FLOAT,
    reference_source VARCHAR(50),  -- aadhaar, pan, document
    selfie_s3_key VARCHAR(500),
    reference_s3_key VARCHAR(500),
    created_at TIMESTAMP
);
```

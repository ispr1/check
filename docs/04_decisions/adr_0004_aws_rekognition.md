# ADR 004: AWS Rekognition for Face Verification

**Status:** Accepted  
**Date:** 2026-01-22  
**Authors:** Core Engineering Team

## Context

We needed biometric verification: Selfie vs ID photo. Options:

| Option | Accuracy | Cost | Data Residency |
|--------|----------|------|----------------|
| **AWS Rekognition** | 99.5%+ | $1/1000 | ap-south-1 ✓ |
| Azure Face API | 99%+ | $1/1000 | India ✓ |
| Open Source (InsightFace) | 95%+ | Free | Local ✓ |
| Hyperverge | 99%+ | $5/1000 | India ✓ |

## Decision

We chose **AWS Rekognition**.

## Rationale

1. **Accuracy:** Industry-leading face comparison (99.5%+ true positive rate).
2. **Liveness Detection:** Built-in anti-spoofing (passive).
3. **Data Residency:** Mumbai region (ap-south-1) satisfies Indian data localization.
4. **Integration:** Already using AWS (S3), minimal new infra.
5. **Cost:** $0.001 per face comparison is negligible at our scale.

## Consequences

- AWS vendor lock-in for biometrics.
- Face images stored in S3 (private bucket).
- Must handle Rekognition quotas (default 50 TPS).

## API Usage

```python
# src/services/face/rekognition.py
rekognition.compare_faces(
    SourceImage={'S3Object': {'Bucket': bucket, 'Name': selfie_key}},
    TargetImage={'S3Object': {'Bucket': bucket, 'Name': id_key}},
    SimilarityThreshold=70
)
```

## Thresholds

| Confidence | Decision |
|------------|----------|
| ≥ 90% | MATCH |
| 70-89% | LOW_CONFIDENCE |
| < 70% | MISMATCH |

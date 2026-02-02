# Vendor Risk Assessment

## Overview

CHECK-360 depends on external vendors. This document assesses their risks.

## Vendor Matrix

| Vendor | Service | Data Shared | Risk Level |
|--------|---------|-------------|------------|
| **Surepass** | Aadhaar/PAN API | Aadhaar, PAN numbers | High |
| **AWS Rekognition** | Face Comparison | Face images | High |
| **AWS S3** | File Storage | All uploads | Medium |
| **PostgreSQL (RDS)** | Database | All data | High |

## Vendor: Surepass

### Services Used
- Aadhaar Verification
- PAN Validation
- UAN Lookup

### Data Exposure
- Aadhaar number sent for validation
- Aadhaar demographics returned

### Risk Assessment
| Risk | Likelihood | Impact |
|------|------------|--------|
| Data breach at Surepass | Low | High |
| API unavailability | Medium | Medium |
| Incorrect data returned | Low | Medium |

### Mitigations
- Encrypt Surepass responses before storage
- Implement fallback (manual verification)
- Validate response schema

## Vendor: AWS

### Services Used
- Rekognition (Face Match)
- S3 (Storage)
- RDS (Database)

### Data Exposure
- Face images sent to Rekognition
- All files stored in S3
- All PII in RDS

### Risk Assessment
| Risk | Likelihood | Impact |
|------|------------|--------|
| AWS region outage | Very Low | High |
| S3 misconfiguration | Low | High |
| IAM key theft | Low | Critical |

### Mitigations
- Use ap-south-1 (India region)
- Block public access on S3
- IAM least privilege + rotation

## Contractual Requirements

For all vendors:
- [ ] Data Processing Agreement (DPA) signed
- [ ] SOC 2 report available
- [ ] Breach notification clause (72 hours)
- [ ] Data localization compliance (India)

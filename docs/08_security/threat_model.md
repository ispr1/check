# Threat Model

## Overview

This document identifies potential threats to CHECK-360 and their mitigations.

## Asset Inventory

| Asset | Classification | Impact if Compromised |
|-------|----------------|----------------------|
| Aadhaar Data | Restricted | Identity theft, legal liability |
| Trust Scores | Confidential | Bad hires, reputation damage |
| Face Images | Restricted | Privacy violation |
| Session Tokens | Confidential | Unauthorized access |
| AWS Credentials | Restricted | Full system compromise |

## Threat Actors

| Actor | Motivation | Capability |
|-------|------------|------------|
| **Malicious Candidate** | Get hired despite fraud | Low-Medium |
| **Competitor** | Extract business logic | Medium |
| **Insider (HR)** | Sell candidate data | Medium |
| **External Attacker** | Data theft, ransom | High |
| **Nation State** | Mass surveillance | Very High |

## STRIDE Analysis

### Spoofing

| Threat | Mitigation |
|--------|------------|
| Fake selfie (photo of photo) | Liveness detection |
| Stolen verification token | Token expiry (72h) |
| Impersonating HR | JWT + RBAC |

### Tampering

| Threat | Mitigation |
|--------|------------|
| Modify trust score in transit | TLS encryption |
| Alter document after upload | Immutable S3 storage |
| SQL injection | Parameterized queries (SQLAlchemy) |

### Repudiation

| Threat | Mitigation |
|--------|------------|
| HR denies override | Immutable audit trail |
| Candidate denies consent | Consent timestamp logged |

### Information Disclosure

| Threat | Mitigation |
|--------|------------|
| PII in logs | Log redaction |
| S3 bucket public | Private ACLs enforced |
| Error messages leak data | Generic error responses |

### Denial of Service

| Threat | Mitigation |
|--------|------------|
| API flood | Rate limiting |
| Large file upload | 10MB limit |
| Slow loris | Timeout configuration |

### Elevation of Privilege

| Threat | Mitigation |
|--------|------------|
| HR → Admin escalation | Role-based access |
| Token manipulation | JWT signature verification |

## Risk Matrix

| Risk | Likelihood | Impact | Priority |
|------|------------|--------|----------|
| Candidate submits fake ID | High | Medium | **P1** |
| HR leaks candidate data | Medium | High | **P1** |
| Vendor breach (Surepass) | Low | High | P2 |
| DDoS attack | Medium | Medium | P2 |

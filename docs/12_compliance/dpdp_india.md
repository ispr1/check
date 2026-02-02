# DPDP Act Compliance (India)

## Overview

The Digital Personal Data Protection Act (DPDP), 2023 is India's primary data protection law. CHECK-360 is designed to comply with its requirements.

## Key Requirements & Our Compliance

### 1. Lawful Purpose (Section 4)

| Requirement | Our Implementation |
|-------------|-------------------|
| Process data only for lawful purposes | BGV is legitimate business purpose |
| Obtain consent before processing | T&C acceptance before verification |
| Limit processing to stated purpose | Data used only for verification |

### 2. Consent (Section 6)

| Requirement | Our Implementation |
|-------------|-------------------|
| Free, specific, informed consent | Clear consent screen at start |
| Easy withdrawal mechanism | Support ticket process |
| Language clarity | Multi-language support planned |

**Consent Capture:**
```sql
-- Logged in verification session
consent_given_at TIMESTAMP NOT NULL
consent_ip_address VARCHAR(50)
```

### 3. Data Principal Rights (Section 11-14)

| Right | Our Implementation |
|-------|-------------------|
| Right to Access | API to fetch own data |
| Right to Correction | HR can update via support |
| Right to Erasure | Deletion API (anonymization) |
| Right to Grievance Redressal | Support email + DPO contact |

### 4. Data Security (Section 8)

| Requirement | Our Implementation |
|-------------|-------------------|
| Reasonable security safeguards | AES-256 encryption, TLS 1.2+ |
| Prevent unauthorized access | RBAC, JWT authentication |
| Data breach notification | 72-hour notification process |

### 5. Data Localization

| Requirement | Our Implementation |
|-------------|-------------------|
| Store Indian citizen data in India | AWS ap-south-1 (Mumbai) |

### 6. Data Fiduciary Obligations (Section 8)

We are a Data Processor; our customers (enterprises) are Data Fiduciaries. We:

- [ ] Have DPA agreements with customers
- [ ] Process only as instructed
- [ ] Assist with rights requests
- [ ] Delete data on request

## Data Protection Officer

Required for significant data processors:

| Role | Contact |
|------|---------|
| DPO | dpo@check360.in |
| Grievance Officer | grievance@check360.in |

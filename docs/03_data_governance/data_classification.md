# Data Classification Policy

## 1. Public Data
**Definition:** Data intended for public consumption.
**Handling:** No restrictions.
*   Marketing content
*   Public API Docs

## 2. Internal Data
**Definition:** Business data, not sensitive.
**Handling:** Auth required.
*   Company Names
*   Configuration Rules
*   System Logs (Redacted)

## 3. Confidential (PII)
**Definition:** Identifies an individual.
**Handling:** Encrypted at rest. Access logged.
*   Full Name
*   Email / Phone
*   Candidate Photos (Selfies)
*   Resumes

## 4. Restricted (SPII)
**Definition:** High-risk sensitive data.
**Handling:** Strong Encryption. Strict access control. Audit trail mandatory.
*   Aadhaar Number / Image
*   PAN Number / Image
*   Trust Score Breakdown (Forensic details)
*   HR Decision Comments

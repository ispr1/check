# Data Flow Architecture

## 1. Candidate Submission Flow
Data moves from Trusted Sources -> System -> Scoring. User input is treated as "Claim".

1.  **Ingest:** Candidate uploads File/ID.
2.  **Storage:** Raw file -> S3 (Private Bucket).
3.  **Process:**
    *   File ID sent to Analysis Worker.
    *   Result (JSON) returned.
4.  **Persist:**
    *   Result -> DB (VerificationStep).
    *   PII (like Aadhaar Number) -> Encrypted Column.
5.  **Score:** Trust Engine reads DB -> Updates Score.

## 2. PII Flow (Privacy)
Personal Identifiable Information (PII) is strictly controlled.

*   **Candidate Inputs:** Encrypted at rest.
*   **Vendor Responses:** Raw JSON stored Encrypted.
*   **HR View:** Decrypted on-the-fly for authenticated sessions only.
*   **Logs:** PII is **redacted** in logs.

## 3. Trust Score Calculation Flow
Triggered on every verification step completion.

1.  **Event:** `VerificationStep` status changes to `COMPLETED`.
2.  **Aggregation:** Trust Calculator fetches all Steps + Face + Docs.
3.  **Computation:** Applies weights and deductions.
4.  **Update:** new Score saved to `trust_scores` table.

## Data Retention
*   **In-flight:** Data active during verification session.
*   **Archived:** After decision, data moved to cold storage (conceptual).
*   **Purge:** Candidate data deleted upon request (DPDP compliance).

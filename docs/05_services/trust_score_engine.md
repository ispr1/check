# Trust Score Engine Service

## Responsibility
Calculates the final `TrustScore` and generates `Flags`.

## Input
*   Verification Data (Aadhaar, PAN results).
*   Face Comparison Result (Confidence, Decision).
*   Document Analysis Results (Legitimacy Scores).

## Logic
Purely deterministic rule engine based on `weights` and `deductions`.

### Weights
*   Face: 25%
*   Documents: 25%
*   Aadhaar: 20%
*   PAN: 10%
*   Cross-Match: 10%
*   UAN: 10%

### Deduction Rules
*   **Mismatch:** Heavy penalty (20-100 pts).
*   **Suspicious:** Moderate penalty (15 pts).
*   **Review Required:** Light penalty (5 pts).

## Output
*   **Score:** Float (0-100).
*   **Status:** `VERIFIED` | `REVIEW_REQUIRED` | `HIGH_RISK` | `FLAGGED`.
*   **Flags:** List of machine-readable error codes (e.g., `FACE_LOW_CONFIDENCE`).

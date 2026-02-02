# User Journeys

## Journey 1: The "Golden Path" (Auto-Success)

1.  **Trigger:** HR creates candidate via API (`POST /candidates`).
2.  **Notification:** Candidate receives "Start Verification" link.
3.  **Submission:**
    *   Accepts Terms (Consent).
    *   Uploads Selfie.
    *   Enters Aadhaar/PAN (Backend verifies instantly via Surepass).
    *   Uploads Degree Cert (Backend analyzes for forgery).
4.  **Processing:**
    *   System runs 1:1 Face Match (Selfie vs ID).
    *   System calculates Trust Score (e.g., 96/100).
5.  **Outcome:** Status `VERIFIED`. HR notified.

## Journey 2: The "Suspicious Document" (Flagged)

1.  **Submission:** Candidate uploads Experience Letter.
2.  **Analysis:**
    *   Metadata Analyzer detects "Adobe Photoshop CS6".
    *   Font Analyzer detects mixed font families in salary area.
3.  **Scoring:**
    *   Trust Score Deduction: -15 (Suspicious Doc).
    *   Final Score: 60/100.
    *   Status: `REVIEW_REQUIRED`.
4.  **HR Review:**
    *   HR pulls summary (`GET /hr/candidates/{id}/summary`).
    *   Sees Flag: `DOC_SUSPICIOUS`.
    *   HR requests original copy via email.
5.  **Decision:** HR uploads new doc (`POST /hr/documents/upload`) OR Rejects (`POST /hr/decision` -> `REJECTED`).

## Journey 3: The "Senior Override" (Exception)

1.  **Context:** Candidate has `PAN_NAME_MISMATCH` (-50 points). Score: 50.
2.  **Resolution:** Candidate proves they changed name recently (Marriage Affidavit).
3.  **HR Action:**
    *   HR Manager logs in.
    *   Calls Override API (`POST /trust-score/override`).
    *   Provides Reason: `EXPLAINABLE` + "Marriage Certificate Verified".
    *   Status changes to `APPROVED`.
4.  **Audit:** The deviation is permanently logged in `trust_score_overrides` table.

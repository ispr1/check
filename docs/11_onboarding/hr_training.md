# HR Training Guide

## Audience

HR Operations team members using CHECK-360 for background verification.

## System Overview

CHECK-360 helps you verify candidate identity and documents before hiring. The system automatically:

1. Verifies Government IDs (Aadhaar, PAN)
2. Matches face (selfie vs ID photo)
3. Analyzes documents for tampering
4. Calculates a Trust Score

## Understanding Trust Score

| Score | Status | What It Means |
|-------|--------|---------------|
| 85-100 | ✅ VERIFIED | Safe to proceed |
| 70-84 | 🟡 REVIEW_REQUIRED | Check flags, decide |
| 50-69 | 🟠 HIGH_RISK | Senior review needed |
| 0-49 | 🔴 FLAGGED | Cannot proceed without override |

## Reading the Summary

When you view a candidate, you'll see:

### Trust Score Section
- **Score:** The number (0-100)
- **Status:** Color-coded status
- **Deductions:** Why points were lost
- **Flags:** Specific issues found

### Documents Section
- **Legitimacy Score:** How trustworthy the document is
- **Status:** LEGITIMATE, REVIEW_REQUIRED, or SUSPICIOUS
- **Flags:** Specific concerns (e.g., "Metadata shows Photoshop")

### Face Verification
- **Decision:** MATCH, LOW_CONFIDENCE, or MISMATCH
- **Confidence:** How similar the faces are (%)

## Making Decisions

### When to Approve
- Score ≥ 85 with no major flags
- All identity checks passed
- Documents look legitimate

### When to Reject
- Face mismatch confirmed
- Document clearly forged
- Identity verification failed

### When to Request More Info
- Low confidence face match
- Missing documents
- Score in review range

## Using Override

If you have external evidence that contradicts the system:

1. Request override with clear justification
2. Upload supporting documents
3. Wait for senior approval
4. Decision is logged permanently

## Common Flags and Actions

| Flag | Meaning | Action |
|------|---------|--------|
| `FACE_MISMATCH` | Selfie doesn't match ID | Verify identity manually |
| `DOC_SUSPICIOUS_education` | Degree cert may be fake | Request original |
| `AADHAAR_NAME_MISMATCH` | Name differs from PAN | Ask for marriage cert/affidavit |
| `UAN_EMPLOYMENT_GAP` | Gap in employment history | Ask for explanation |

# Product Requirements Document (PRD)

**Product:** CHECK-360  
**Version:** MVP (Phases 1-6 Implemented)  
**Status:** Stable / Deployment Ready  

## 1. Introduction
CHECK-360 is a backend-first verification orchestrator. It allows companies to verify candidate identities, documents, and employment history in real-time, generating a Trust Score to aid hiring decisions.

## 2. Target Audience
*   **Primary:** Enterprise HR Ops Teams (high volume hiring).
*   **Secondary:** Compliance / Risk Officers.

## 3. Key Features Scope (MVP)

### 3.1 Identity Verification
*   **Feature:** Verify Government IDs (Aadhaar, PAN).
*   **Requirement:** Match candidate name/DOB against official databases.
*   **Method:** API wrapper around Surepass.

### 3.2 Biometric Verification
*   **Feature:** Face Match (Liveness + 1:1 Compare).
*   **Requirement:** Ensure person submitting data == person on ID card.
*   **Method:** AWS Rekognition.

### 3.3 Document Forensics
*   **Feature:** Detect digital forgery in PDFs (Education/Experience docs).
*   **Requirement:** Flag Photoshop edits, metadata inconsistency, font manipultion.
*   **Method:** Multi-layer Python analysis (Metadata, Fonts, Noise).

### 3.4 Trust Score Engine
*   **Feature:** Explainable Risk Scoring.
*   **Requirement:** 0-100 score, starts perfect, deducts for observed risks.
*   **Method:** Deterministic Rule Engine (`rules.py`).

### 3.5 HR Decision Workflow
*   **Feature:** Human Review Interface (API level).
*   **Requirement:** View aggregate data, override scores (with audit), commit final decision.
*   **Method:** HR Aggregation Service + Audit Tables.

## 4. Functional Constraints
*   **Latency:** Analysis should take < 30s per candidate.
*   **Data Residency:** All PII must reside in India (AWS ap-south-1).
*   **Immutability:** Once a decision is made, it cannot be deleted.

## 5. Success Metrics
*   **Auto-Approval Rate:** Target > 60% (Clear legitimate cases).
*   **False Positive Rate:** Target < 5% (Legit candidates flagged).
*   **API Error Rate:** < 1%.

# Candidate Verification Flow

## Overview

This document describes the complete verification journey from candidate link to final score.

## Sequence Diagram

```mermaid
sequenceDiagram
    participant HR as HR System
    participant API as CHECK-360 API
    participant C as Candidate
    participant SP as Surepass
    participant AWS as AWS Rekognition
    
    HR->>API: POST /candidates (create)
    API->>API: Generate verification session
    API->>C: Send magic link (email)
    
    C->>API: GET /verify/{token}
    API-->>C: Session info + required steps
    
    C->>API: POST /steps/aadhaar
    API->>SP: Verify Aadhaar
    SP-->>API: Demographics + Photo
    API-->>C: Success
    
    C->>API: POST /steps/pan
    API->>SP: Validate PAN
    SP-->>API: Name + Status
    API-->>C: Success
    
    C->>API: POST /steps/face (selfie)
    API->>AWS: CompareFaces
    AWS-->>API: Confidence score
    API-->>C: MATCH / MISMATCH
    
    C->>API: POST /documents/analyze
    API->>API: Forensic analysis
    API-->>C: Legitimacy score
    
    API->>API: Calculate Trust Score
    API->>HR: Verification complete
```

## Step Details

### Step 1: Session Creation
- HR creates candidate via API.
- System generates one-time token.
- Email sent to candidate.

### Step 2: Identity Verification
- Candidate enters Aadhaar.
- Surepass validates against UIDAI.
- Photo extracted for face match.

### Step 3: Face Verification
- Candidate captures live selfie.
- Rekognition compares to Aadhaar photo.
- Confidence score recorded.

### Step 4: Document Upload
- Candidate uploads education/experience docs.
- Forensic engine analyzes for tampering.
- Legitimacy score calculated.

### Step 5: Score Calculation
- All data aggregated.
- Trust Score computed.
- Status assigned (VERIFIED/FLAGGED).

## Timing

| Step | Expected Duration |
|------|-------------------|
| Aadhaar verify | 3-5 seconds |
| PAN verify | 2-3 seconds |
| Face compare | 2-4 seconds |
| Document analysis | 5-15 seconds |
| Score calculation | < 1 second |
| **Total** | **~30 seconds** |

# HR Review Flow

## Overview

After candidate completes verification, HR reviews the results and makes a decision.

## Flow Diagram

```mermaid
flowchart TD
    A[Verification Completed] --> B{Score >= 85?}
    B -->|Yes| C[Status: VERIFIED]
    B -->|No| D{Score >= 70?}
    D -->|Yes| E[Status: REVIEW_REQUIRED]
    D -->|No| F{Score >= 50?}
    F -->|Yes| G[Status: HIGH_RISK]
    F -->|No| H[Status: FLAGGED]
    
    C --> I[HR Notified]
    E --> I
    G --> I
    H --> I
    
    I --> J[HR Reviews Summary]
    J --> K{Decision?}
    
    K -->|Approve| L[Record APPROVED]
    K -->|Reject| M[Record REJECTED]
    K -->|Need Info| N[Request More Docs]
    
    N --> O[Candidate Uploads]
    O --> J
```

## HR Actions

### 1. View Summary
`GET /hr/candidates/{id}/summary`

HR sees:
- Candidate info
- Trust Score with breakdown
- All flags by category
- Face comparison result
- Document analysis results

### 2. Upload Additional Documents
`POST /hr/documents/upload`

For missing or clarification documents.

### 3. Record Decision
`POST /hr/decision/{verification_id}`

Options:
- `APPROVED` - Candidate cleared
- `REJECTED` - Candidate failed
- `NEED_MORE_INFO` - Additional documents required

### 4. Override (If Needed)
When score is low but HR has external evidence:

1. HR requests override.
2. Senior HR approves.
3. Override logged with justification.

## Audit Requirements

Every HR action is logged:
- Who viewed what
- Who uploaded what
- Who decided what
- Who overrode what

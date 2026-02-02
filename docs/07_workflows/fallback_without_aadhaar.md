# Fallback Without Aadhaar

## Context

Some candidates may not have Aadhaar or may refuse to share it. This workflow handles verification without primary identity.

## Alternative Identity Sources

| Priority | Source | Reliability |
|----------|--------|-------------|
| 1 | PAN Card | High |
| 2 | Passport | High |
| 3 | Voter ID | Medium |
| 4 | Driving License | Medium |

## Fallback Flow

```
1. Candidate indicates no Aadhaar
2. System prompts for PAN
3. If PAN verified, request face photo from PAN card
4. Face comparison: Selfie vs PAN photo
5. Additional document verification emphasized
6. Trust Score calculated with "AADHAAR_MISSING" flag
```

## Scoring Impact

| Scenario | Impact |
|----------|--------|
| Aadhaar provided | Full 20% weight |
| Aadhaar missing, PAN provided | -5 points (10% of Aadhaar weight) |
| Both missing | -20 points + INCOMPLETE status |

## Face Match Without Aadhaar

| Comparison | Priority |
|------------|----------|
| Selfie vs PAN Photo | Primary fallback |
| Selfie vs Passport Photo | Secondary fallback |
| Selfie vs Document ID Photo | Tertiary fallback |

## Implementation

```python
if not aadhaar_available:
    reference_source = "pan"  # or "passport"
    flags.append("AADHAAR_MISSING")
    score_deduction = 5  # Lighter penalty
```

## HR Visibility

When Aadhaar is missing:
- Flag displayed prominently
- HR advised to request additional identity proof
- System recommendation includes "Request Aadhaar"

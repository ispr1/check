# HR Review Service

## Responsibility

Aggregates verification data for human review and records final decisions.

## Key Principles

1. **Read-Only Scores:** HR can view Trust Scores but NOT modify them directly.
2. **Immutable Decisions:** Once recorded, decisions cannot be edited.
3. **Explainability:** Every flag has a human-readable reason.
4. **Audit Trail:** All HR actions are logged.

## Components

### 1. Summary Aggregator

Collects data from multiple tables into a single HR-friendly view:

```python
class HRSummaryService:
    def get_candidate_summary(db, candidate_id) -> HRSummary:
        # Aggregates: Candidate + Verification + Score + Docs + Face
```

### 2. Decision Recorder

Immutable decision storage:

```python
class HRDecision:
    decision: APPROVED | REJECTED | NEED_MORE_INFO
    reason_codes: List[str]
    comments: str
    trust_score_at_decision: float  # Snapshot
```

### 3. Document Upload Handler

HR can upload supplementary documents:
- Missing certificates
- Clarification letters
- Experience proofs

These are analyzed but do NOT auto-update trust score.

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/hr/candidates/{id}/summary` | GET | Full candidate view |
| `/hr/documents/upload` | POST | Upload HR doc |
| `/hr/decision/{verification_id}` | POST | Record decision |
| `/hr/audit/{verification_id}` | GET | Get audit trail |

## Explainability Contract

Every response includes:

```json
{
  "trust_score": {
    "score": 75.5,
    "status": "REVIEW_REQUIRED",
    "deductions": [
      {"category": "face", "reason": "Low Confidence", "points": 10},
      {"category": "documents", "reason": "Suspicious Metadata", "points": 15}
    ],
    "flags": {
      "face": ["FACE_LOW_CONFIDENCE"],
      "documents": ["DOC_SUSPICIOUS_education"]
    }
  }
}
```

## Override Flow

When HR overrides a low score:

1. HR submits override request with justification.
2. Senior HR (role: `senior_hr` or `admin`) approves.
3. Override logged in `trust_score_overrides` table.
4. Original score preserved; new effective score applied.

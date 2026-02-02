# Verification Session Service

## Responsibility

Manages the lifecycle of a verification request from creation to completion.

## Key Concepts

| Concept | Description |
|---------|-------------|
| Session | A time-bounded verification workflow for one candidate |
| Token | One-time use link sent to candidate |
| Steps | Individual checks (Aadhaar, PAN, Face, Docs) |
| Status | Overall verification state |

## Session States

```
CREATED → LINK_SENT → IN_PROGRESS → COMPLETED
                           ↓
                       EXPIRED / FLAGGED
```

## Token Management

- Token generated on session creation.
- Expires after 72 hours.
- Single-use (invalidated after first access).

```python
token = secrets.token_urlsafe(32)
expires = datetime.utcnow() + timedelta(hours=72)
```

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /verifications/start` | Create session, generate token |
| `GET /verifications/{id}` | Get session status |
| `POST /verifications/{id}/step` | Submit a verification step |

## Database Model

```sql
CREATE TABLE verifications (
    id SERIAL PRIMARY KEY,
    candidate_id INT REFERENCES candidates(id),
    company_id INT REFERENCES companies(id),
    token VARCHAR(64) UNIQUE,
    token_expires TIMESTAMP,
    status VARCHAR(50), -- CREATED, LINK_SENT, IN_PROGRESS...
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

## Error Handling

| Scenario | Response |
|----------|----------|
| Token expired | 410 Gone |
| Token already used | 400 Bad Request |
| Session not found | 404 Not Found |

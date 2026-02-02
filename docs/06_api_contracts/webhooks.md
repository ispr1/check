# Webhooks (Future)

> **Status:** Planned for Phase 7

## Overview

Webhooks will notify external systems of verification events in real-time.

## Planned Events

| Event | Trigger | Payload |
|-------|---------|---------|
| `verification.started` | Session created | `{verification_id, candidate_id}` |
| `verification.completed` | All steps done | `{verification_id, score, status}` |
| `verification.flagged` | Score < 50 | `{verification_id, flags}` |
| `decision.made` | HR records decision | `{verification_id, decision}` |

## Webhook Configuration

```json
{
  "url": "https://your-system.com/webhooks/check360",
  "events": ["verification.completed", "decision.made"],
  "secret": "sha256-signature-key"
}
```

## Security

- Payloads signed with HMAC-SHA256.
- Verify signature before processing.
- Retry on 5xx (max 3 attempts).

## Retry Policy

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 5 minutes |
| 3 | 30 minutes |
| Final | Marked failed |

# ADR 002: Surepass as Primary Truth Source

**Status:** Accepted  
**Date:** 2026-01-18  
**Authors:** Core Engineering Team

## Context

We needed a reliable source for Government ID verification (Aadhaar, PAN, UAN). Options evaluated:

| Vendor | Coverage | Latency | Pricing |
|--------|----------|---------|---------|
| **Surepass** | Aadhaar, PAN, UAN, Court | 2-5s | ₹2-5/call |
| Karza | Similar | 3-6s | ₹3-8/call |
| Signzy | Similar | 4-7s | ₹4-10/call |
| Direct UIDAI | Aadhaar only | Complex | Free (but hard) |

## Decision

We chose **Surepass** as the primary vendor for identity verification.

## Rationale

1. **Breadth:** One SDK for Aadhaar + PAN + UAN + Courts.
2. **Sandbox:** Excellent mock environment for development.
3. **Reliability:** 99.9% uptime SLA.
4. **Cost:** Most competitive per-call pricing.

## Consequences

- Single vendor dependency for identity layer.
- Must implement fallback (manual verification path) if Surepass is down.
- API responses are treated as **Source of Truth** for identity claims.
- All Surepass responses are encrypted before storage.

## Integration Points

```python
# src/services/surepass/client.py
class SurepassClient:
    def verify_aadhaar(self, aadhaar_number: str) -> AadhaarResponse
    def verify_pan(self, pan_number: str) -> PANResponse
    def verify_uan(self, uan_number: str) -> UANResponse
```

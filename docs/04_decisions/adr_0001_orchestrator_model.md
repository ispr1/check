# ADR 001: Orchestrator Model Architecture

**Status:** Accepted  
**Date:** 2026-01-15  
**Authors:** Core Engineering Team

## Context

We needed to decide the fundamental architecture for CHECK-360. The options were:

1. **Full-Stack Provider:** Build everything ourselves (OCR, Face Match, ID APIs).
2. **Pure Aggregator:** Just display vendor data, no logic.
3. **Orchestrator + Truth Comparator:** Integrate best-in-class vendors, add proprietary comparison logic.

## Decision

We chose **Option 3: Orchestrator Model**.

## Rationale

| Factor | Full-Stack | Aggregator | Orchestrator ✓ |
|--------|------------|------------|----------------|
| Time to Market | 18 months | 2 months | 4 months |
| Differentiation | High | Zero | High |
| Compliance Risk | High | Low | Medium |
| Cost | Very High | Low | Medium |

**Key Insight:** The value is not in *fetching* Aadhaar data. That's commodity. The value is in *comparing* Aadhaar data against PAN data against UAN data and computing a confidence signal.

## Consequences

- We depend on vendor uptime (Surepass, AWS).
- We must handle vendor failures gracefully.
- We own the "Truth Comparison" layer, not the "Data Fetching" layer.
- We can swap vendors without changing core logic.

## Diagram

```
Candidate Input → CHECK-360 Orchestrator → [Surepass, Rekognition, PyMuPDF]
                           ↓
                    Truth Comparator
                           ↓
                      Trust Score
```

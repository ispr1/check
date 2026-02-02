# ADR 003: Deductive Scoring Model

**Status:** Accepted  
**Date:** 2026-02-01

## Context
We need a way to calculate a "Trust Score" for candidates.
Options:
1.  **Additive:** Start at 0, add points for every verified item.
2.  **Deductive:** Start at 100, deduct points for discrepancies.
3.  **ML-Based:** Black box model trained on historical data.

## Decision
We chose **Option 2: Deductive Scoring (Start at 100)**.

## Rationale
1.  **Psychology:** Candidates start "innocent until proven guilty". A perfect candidate naturally has 100.
2.  **Explainability:** It is easier to explain "You lost 20 points because of a face mismatch" than "You gained 5 points for...".
3.  **Simplicity:** Additive scoring requires complex weighting for "how much is an Aadhaar worth?". Deductive focuses purely on risk.
4.  **No Training Data:** We are day-1. We cannot train an ML model (Option 3).

## Consequences
*   Rules must be tuned carefully to avoid 0 scores for minor issues.
*   We need a "Minimum Viable Verification" set; otherwise, a candidate who submits nothing might technically have 100 (solved by "Incomplete" status).

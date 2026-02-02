"""
Trust Score Service Package.

Phase 5: Professional trust score calculation with explainable deductions.
"""

from .calculator import TrustScoreCalculator, get_trust_calculator, TrustScoreResult
from .rules import TrustScoreStatus, WEIGHTS, THRESHOLDS

__all__ = [
    "TrustScoreCalculator",
    "get_trust_calculator",
    "TrustScoreResult",
    "TrustScoreStatus",
    "WEIGHTS",
    "THRESHOLDS",
]

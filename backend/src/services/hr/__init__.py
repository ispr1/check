"""
HR Services Package.

Phase 6: HR review, document handling, and decision APIs.
"""

from .summary_service import HRSummaryService, get_hr_summary_service, HRSummary, ExplainableScore

__all__ = [
    "HRSummaryService",
    "get_hr_summary_service",
    "HRSummary",
    "ExplainableScore",
]

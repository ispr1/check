"""
Status mapper for internal vs external representation.

Internal (DB/code): VERIFIED, PARTIAL, FAILED
External (API/HR): MATCH, PARTIAL_MATCH, MISMATCH, NOT_AVAILABLE
"""


# Internal to External mapping
_STATUS_MAP = {
    "VERIFIED": "MATCH",
    "PARTIAL": "PARTIAL_MATCH",
    "FAILED": "MISMATCH",
    "PENDING": "NOT_AVAILABLE",
    "SKIPPED": "NOT_AVAILABLE",
}

# Reverse for logging/debugging
_EXTERNAL_TO_INTERNAL = {v: k for k, v in _STATUS_MAP.items()}


def to_external_status(internal_status: str) -> str:
    """
    Map internal verification status to HR-friendly external status.
    
    Args:
        internal_status: VERIFIED, PARTIAL, FAILED, etc.
        
    Returns:
        MATCH, PARTIAL_MATCH, MISMATCH, or NOT_AVAILABLE
    """
    return _STATUS_MAP.get(internal_status.upper(), "NOT_AVAILABLE")


def to_internal_status(external_status: str) -> str:
    """
    Map external status back to internal (for admin tools).
    """
    return _EXTERNAL_TO_INTERNAL.get(external_status.upper(), "PENDING")


def format_comparison_for_hr(comparison_result: dict) -> dict:
    """
    Format comparison result for HR display.
    
    - Removes internal scoring details
    - Uses external status terminology
    - Hides raw technical flags
    
    Args:
        comparison_result: Raw comparison dict from services
        
    Returns:
        HR-safe comparison summary
    """
    return {
        "status": to_external_status(comparison_result.get("status", "PENDING")),
        "confidence": _score_to_confidence(comparison_result.get("score", 0)),
        "summary": _generate_summary(comparison_result),
        "requires_review": comparison_result.get("status") == "PARTIAL" or 
                          bool(comparison_result.get("flags")),
    }


def _score_to_confidence(score: int) -> str:
    """Convert numeric score to confidence level."""
    if score >= 90:
        return "HIGH"
    elif score >= 70:
        return "MEDIUM"
    elif score >= 50:
        return "LOW"
    else:
        return "VERY_LOW"


def _generate_summary(comparison_result: dict) -> str:
    """Generate human-readable summary for HR."""
    status = comparison_result.get("status", "PENDING")
    flags = comparison_result.get("flags", [])
    
    if status == "VERIFIED":
        return "All checks passed successfully."
    elif status == "PARTIAL":
        if "OVERLAPPING_EMPLOYMENT" in flags:
            return "Verified with overlapping employment detected. Manual review recommended."
        elif "EXPERIENCE_MISMATCH" in flags:
            return "Verified but claimed experience differs from records."
        else:
            return "Partial match - some details need verification."
    elif status == "FAILED":
        return "Verification failed. Identity mismatch detected."
    else:
        return "Verification pending."


def format_flags_for_hr(flags: list) -> list:
    """
    Convert internal flags to HR-friendly descriptions.
    """
    flag_descriptions = {
        "OVERLAPPING_EMPLOYMENT": {
            "label": "Overlapping Employment",
            "description": "Candidate had concurrent employment at multiple companies.",
            "severity": "MEDIUM",
        },
        "EXPERIENCE_MISMATCH": {
            "label": "Experience Discrepancy",
            "description": "Claimed experience differs from verified records.",
            "severity": "LOW",
        },
        "IDENTITY_MISMATCH": {
            "label": "Identity Mismatch",
            "description": "Name or DOB doesn't match across documents.",
            "severity": "HIGH",
        },
    }
    
    return [
        flag_descriptions.get(flag, {
            "label": flag.replace("_", " ").title(),
            "description": "Requires manual review.",
            "severity": "MEDIUM",
        })
        for flag in flags
    ]

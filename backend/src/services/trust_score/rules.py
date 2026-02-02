"""
Trust Score Rules and Configuration.

Centralized weights, thresholds, and deduction values.
"""

from enum import Enum


class TrustScoreStatus(str, Enum):
    """Trust score status."""
    VERIFIED = "VERIFIED"               # Score >= 85
    REVIEW_REQUIRED = "REVIEW_REQUIRED"  # Score 70-84
    HIGH_RISK = "HIGH_RISK"             # Score 50-69
    FLAGGED = "FLAGGED"                 # Score < 50
    INCOMPLETE = "INCOMPLETE"           # Completion < 70%


# ============ COMPONENT WEIGHTS ============
# Total = 100%

WEIGHTS = {
    "aadhaar": 20,       # Core identity
    "pan": 10,           # Financial identity
    "uan": 10,           # Employment (conditional)
    "face": 25,          # Identity confirmation
    "documents": 25,     # Education + Experience
    "cross_match": 10,   # Consistency checks
}

# ============ STATUS THRESHOLDS ============

THRESHOLDS = {
    "verified": 85.0,
    "review_required": 70.0,
    "high_risk": 50.0,
    "flagged": 0.0,
}

# ============ COMPLETION ============

MIN_COMPLETION_RATE = 0.70  # 70% minimum

# ============ AADHAAR DEDUCTIONS ============

AADHAAR_DEDUCTIONS = {
    "not_verified": 100,       # Full component loss
    "failed": 100,
    "name_mismatch": 30,
    "dob_mismatch": 40,
    "gender_mismatch": 10,
    "low_match": 20,           # Match < 80%
}

# ============ PAN DEDUCTIONS ============

PAN_DEDUCTIONS = {
    "not_verified": 100,
    "invalid": 100,
    "name_mismatch": 50,
    "dob_mismatch": 30,
    "aadhaar_not_linked": 20,
}

# ============ UAN DEDUCTIONS ============

UAN_DEDUCTIONS = {
    "not_provided_fresher": 0,        # No penalty for freshers
    "not_provided_junior": 50,        # 1-3 years experience
    "not_provided_senior": 100,       # 3+ years experience
    "invalid": 100,
    "experience_mismatch": 30,        # Claimed vs verified
    "employment_gap": 5,              # Per gap (max 20)
}

# Experience thresholds for UAN
UAN_EXPERIENCE_THRESHOLDS = {
    "fresher": 0,      # No UAN expected
    "junior": 1,       # Soft penalty if missing
    "senior": 3,       # Hard penalty if missing
}

# ============ FACE DEDUCTIONS ============

FACE_DEDUCTIONS = {
    "not_verified": 100,
    "mismatch": 100,
    "low_confidence": 40,        # Decision = LOW_CONFIDENCE
    "moderate_confidence": 15,   # Confidence 70-85%
    "liveness_failed": 30,
}

# ============ DOCUMENT DEDUCTIONS ============

DOCUMENT_DEDUCTIONS = {
    "no_documents": 100,
    "missing_education": 50,
    "missing_experience": 30,       # Only if experienced
    "low_legitimacy": 40,           # Avg < 60
    "moderate_legitimacy": 20,      # Avg 60-74
    "acceptable_legitimacy": 10,    # Avg 75-84
    "suspicious_document": 15,      # Per suspicious doc
    "review_required_document": 5,  # Per review doc
}

# Document legitimacy thresholds
DOCUMENT_LEGITIMACY_THRESHOLDS = {
    "excellent": 85,
    "acceptable": 75,
    "moderate": 60,
}

# ============ CROSS-MATCH DEDUCTIONS ============

CROSS_MATCH_DEDUCTIONS = {
    "aadhaar_pan_name": 30,       # < 90% similarity
    "aadhaar_pan_dob": 50,        # Exact mismatch
    "aadhaar_uan_name": 20,       # < 80% similarity
    "document_name": 10,          # < 70% similarity
}

# Fuzzy match thresholds
FUZZY_MATCH_THRESHOLDS = {
    "aadhaar_pan": 90,       # Strict - government data
    "aadhaar_uan": 80,       # Moderate - employment data
    "document": 70,          # Lenient - OCR errors
}

# ============ OVERRIDE RULES ============

OVERRIDE_RULES = {
    "hr_can_override_min": 70,        # HR can override >= 70
    "manager_required_min": 50,       # 50-69 needs manager
    "senior_required_max": 50,        # < 50 needs senior approval
}

OVERRIDE_CATEGORIES = [
    "FALSE_POSITIVE",        # System incorrectly flagged
    "EXPLAINABLE",           # Candidate explained discrepancy
    "ACCEPTABLE_RISK",       # Company accepts the risk
    "DOCUMENT_UPDATED",      # Candidate provided new docs
    "MANUAL_VERIFICATION",   # HR did manual verification
]

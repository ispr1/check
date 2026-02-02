"""
Surepass API Contracts.

Defines request/response shapes for each API endpoint.
When Surepass confirms correct endpoint paths, just update ENDPOINTS dict.

Status: AWAITING SUREPASS CONFIRMATION
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


# ============================================================
# ENDPOINT CONFIGURATION (UPDATE WHEN SUREPASS CONFIRMS)
# ============================================================

ENDPOINTS = {
    # Format: "service": "endpoint_path"
    # These are PLACEHOLDER paths - update when Surepass confirms
    "aadhaar_generate_otp": "aadhaar-v2/generate-otp",
    "aadhaar_submit_otp": "aadhaar-v2/submit-otp",
    "pan_comprehensive": "pan-verification",  # TODO: confirm with Surepass
    "pan_verification": "pan-verification",
    "uan_verification": "uan-verification",  # TODO: confirm with Surepass
    "digilocker_init": "digilocker/init",  # TODO: confirm with Surepass
    "digilocker_fetch": "digilocker/fetch",  # TODO: confirm with Surepass
}


# ============================================================
# VERIFICATION STATUS
# ============================================================

class VerificationStepStatus(str, Enum):
    """Status values for verification steps."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFIED = "VERIFIED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    NOT_AVAILABLE = "NOT_AVAILABLE"  # API endpoint not accessible
    SKIPPED = "SKIPPED"


# ============================================================
# REQUEST CONTRACTS
# ============================================================

@dataclass
class AadhaarOTPRequest:
    """Request body for Aadhaar OTP generation."""
    id_number: str  # 12-digit Aadhaar


@dataclass
class AadhaarSubmitRequest:
    """Request body for Aadhaar OTP submission."""
    client_id: str
    otp: str  # 6-digit OTP


@dataclass
class PANVerificationRequest:
    """Request body for PAN verification."""
    pan_number: str  # or id_number depending on API
    name: Optional[str] = None  # For name matching
    dob: Optional[str] = None  # YYYY-MM-DD for DOB matching


@dataclass
class UANVerificationRequest:
    """Request body for UAN verification."""
    uan_number: str  # 12-digit UAN


@dataclass
class DigilockerInitRequest:
    """Request body for DigiLocker initialization."""
    callback_url: str
    documents: List[str]  # Document types to fetch


# ============================================================
# RESPONSE CONTRACTS
# ============================================================

@dataclass
class SurepassBaseResponse:
    """Base fields present in all Surepass responses."""
    status_code: int
    success: bool
    message: Optional[str] = None
    message_code: Optional[str] = None


@dataclass
class AadhaarOTPResponse:
    """Response from Aadhaar OTP generation."""
    client_id: str
    message: str
    status: str = "OTP_SENT"


@dataclass
class AadhaarVerifiedData:
    """Verified Aadhaar data from OTP submission."""
    full_name: str
    dob: str  # DD-MM-YYYY format from Aadhaar
    gender: str
    address: Dict[str, str]
    photo: Optional[str] = None  # Base64 encoded
    care_of: Optional[str] = None
    masked_aadhaar: Optional[str] = None


@dataclass
class PANVerifiedData:
    """Verified PAN data."""
    pan_number: str
    full_name: str
    dob: Optional[str] = None
    valid: bool = False
    name_match: Optional[bool] = None
    name_match_score: Optional[int] = None
    dob_match: Optional[bool] = None
    aadhaar_seeding_status: Optional[str] = None  # "Y" or "N"
    pan_status: Optional[str] = None  # "E" = Existing, etc.


@dataclass
class EmploymentRecord:
    """Single employment record from UAN."""
    establishment_name: str
    establishment_id: Optional[str] = None
    date_of_joining: Optional[str] = None
    date_of_exit: Optional[str] = None
    member_id: Optional[str] = None
    is_current: bool = False


@dataclass
class UANVerifiedData:
    """Verified UAN/employment data."""
    uan_number: str
    member_name: str
    dob: Optional[str] = None
    establishments: List[EmploymentRecord] = None
    
    def __post_init__(self):
        if self.establishments is None:
            self.establishments = []


# ============================================================
# VERIFICATION RESULT CONTRACTS
# ============================================================

@dataclass
class VerificationResult:
    """Standard verification result structure."""
    status: VerificationStepStatus
    score: int
    message: str
    details: Dict[str, Any]
    verified_at: Optional[str] = None
    flags: List[str] = None
    
    def __post_init__(self):
        if self.flags is None:
            self.flags = []
    
    def to_dict(self) -> dict:
        return {
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "score": self.score,
            "message": self.message,
            "details": self.details,
            "verified_at": self.verified_at,
            "flags": self.flags,
        }


# ============================================================
# NOT_AVAILABLE RESULT FACTORY
# ============================================================

def not_available_result(service_name: str, details: Optional[dict] = None) -> dict:
    """
    Create a NOT_AVAILABLE verification result.
    
    Use when Surepass API returns 404 or is not accessible.
    This is NOT a failure - it's a graceful degradation.
    """
    return {
        "status": VerificationStepStatus.NOT_AVAILABLE.value,
        "score": 0,
        "message": f"{service_name} verification service temporarily unavailable",
        "details": details or {
            "error": "API_NOT_AVAILABLE",
            "reason": "Surepass endpoint not configured or accessible",
        },
        "verified_at": None,
        "flags": ["SERVICE_UNAVAILABLE"],
    }


# ============================================================
# ERROR NORMALIZATION
# ============================================================

def normalize_error(status_code: int, message: str = "") -> dict:
    """
    Normalize Surepass errors to standard format.
    
    Returns dict with:
    - status: VerificationStepStatus value
    - should_retry: bool
    - message: str
    """
    if status_code == 404:
        return {
            "status": VerificationStepStatus.NOT_AVAILABLE,
            "should_retry": False,
            "message": "API endpoint not available",
        }
    elif status_code == 401:
        return {
            "status": VerificationStepStatus.FAILED,
            "should_retry": False,
            "message": "Authentication failed - check API key",
        }
    elif status_code == 429:
        return {
            "status": VerificationStepStatus.PENDING,
            "should_retry": True,
            "message": "Rate limit exceeded - retry later",
        }
    elif status_code >= 500:
        return {
            "status": VerificationStepStatus.PENDING,
            "should_retry": True,
            "message": f"Server error: {message or status_code}",
        }
    elif status_code == 422:
        return {
            "status": VerificationStepStatus.FAILED,
            "should_retry": False,
            "message": f"Invalid input: {message}",
        }
    else:
        return {
            "status": VerificationStepStatus.FAILED,
            "should_retry": False,
            "message": message or f"Unknown error: {status_code}",
        }

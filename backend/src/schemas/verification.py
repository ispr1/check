"""
Pydantic schemas for verification endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Re-export enums for schema use
class VerificationStatusSchema(str, Enum):
    CREATED = "CREATED"
    LINK_SENT = "LINK_SENT"
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"
    SCORED = "SCORED"


class StepTypeSchema(str, Enum):
    PERSONAL_INFO = "PERSONAL_INFO"
    FACE_LIVENESS = "FACE_LIVENESS"
    AADHAAR = "AADHAAR"
    PAN = "PAN"
    UAN = "UAN"
    EDUCATION = "EDUCATION"
    EXPERIENCE = "EXPERIENCE"


class StepStatusSchema(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


# ============ Request Schemas ============

class VerificationStartRequest(BaseModel):
    """Request to start a verification for a candidate."""
    candidate_id: int = Field(..., description="ID of the candidate to verify")
    
    # Optional: specify which conditional steps to include
    include_uan: bool = Field(default=False, description="Include UAN verification (for employed candidates)")
    include_education: bool = Field(default=True, description="Include education document verification")
    include_experience: bool = Field(default=False, description="Include experience document verification")


class PersonalInfoSubmission(BaseModel):
    """Personal info submitted by candidate."""
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    current_address: str = Field(..., min_length=10, max_length=500, description="Current address")
    permanent_address: Optional[str] = Field(None, max_length=500, description="Permanent address if different")
    father_name: Optional[str] = Field(None, max_length=255, description="Father's name")
    mother_name: Optional[str] = Field(None, max_length=255, description="Mother's name")


class FaceLivenessSubmission(BaseModel):
    """Face liveness data submitted by candidate."""
    selfie_image_base64: str = Field(..., description="Base64 encoded selfie image")
    # Additional fields for Phase 3


class AadhaarSubmission(BaseModel):
    """Aadhaar verification data."""
    aadhaar_number: str = Field(..., min_length=12, max_length=12, description="12-digit Aadhaar number")
    # OTP flow handled in Phase 2


class PANSubmission(BaseModel):
    """PAN verification data."""
    pan_number: str = Field(..., min_length=10, max_length=10, description="10-character PAN")


class UANSubmission(BaseModel):
    """UAN verification data."""
    uan_number: str = Field(..., description="Universal Account Number")


class EducationDocSubmission(BaseModel):
    """Education document submission."""
    document_type: str = Field(..., description="Type of document (degree, marksheet, etc.)")
    document_base64: str = Field(..., description="Base64 encoded document")
    institution_name: Optional[str] = Field(None, description="Name of institution")
    year_of_passing: Optional[int] = Field(None, description="Year of passing")


class ExperienceDocSubmission(BaseModel):
    """Experience document submission."""
    document_type: str = Field(..., description="Type of document (offer letter, experience letter, etc.)")
    document_base64: str = Field(..., description="Base64 encoded document")
    company_name: Optional[str] = Field(None, description="Company name")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")


# ============ Response Schemas ============

class VerificationStepResponse(BaseModel):
    """Response for a single verification step."""
    id: int
    step_type: StepTypeSchema
    is_mandatory: bool
    status: StepStatusSchema
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VerificationResponse(BaseModel):
    """Full verification response for HR view."""
    id: int
    candidate_id: int
    candidate_name: str
    company_id: int
    token: str
    verification_link: str
    token_expires_at: datetime
    status: VerificationStatusSchema
    trust_score: Optional[int] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime
    steps: List[VerificationStepResponse] = []

    class Config:
        from_attributes = True


class VerificationListItem(BaseModel):
    """Summary item for verification lists."""
    id: int
    candidate_id: int
    candidate_name: str
    status: VerificationStatusSchema
    trust_score: Optional[int] = None
    created_at: datetime
    token_expires_at: datetime
    steps_completed: int
    steps_total: int

    class Config:
        from_attributes = True


class CandidateVerificationSession(BaseModel):
    """Verification session state for candidate view (no sensitive data)."""
    status: VerificationStatusSchema
    token_expires_at: datetime
    steps: List[VerificationStepResponse]
    next_step: Optional[StepTypeSchema] = None
    can_submit: bool = False

    class Config:
        from_attributes = True


class StepSubmissionResponse(BaseModel):
    """Response after submitting a step."""
    step_type: StepTypeSchema
    status: StepStatusSchema
    message: str


class VerificationSubmitResponse(BaseModel):
    """Response after final submission."""
    status: VerificationStatusSchema
    message: str
    submitted_at: datetime


# ============ Phase 2: Surepass Integration Schemas ============

class AadhaarOTPRequest(BaseModel):
    """Request to generate Aadhaar OTP."""
    aadhaar_number: str = Field(
        ..., 
        min_length=12, 
        max_length=14,
        description="12-digit Aadhaar number (spaces/dashes allowed)"
    )


class AadhaarOTPSubmitRequest(BaseModel):
    """Request to submit Aadhaar OTP for verification."""
    client_id: str = Field(..., description="Client ID from generate-otp response")
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit OTP")


class AadhaarOTPResponse(BaseModel):
    """Response from Aadhaar OTP generation."""
    client_id: str
    otp_sent: bool
    message: str


class PANVerificationRequest(BaseModel):
    """Request for PAN verification with cross-check."""
    pan_number: str = Field(..., min_length=10, max_length=10, description="10-character PAN")


class UANVerificationRequest(BaseModel):
    """Request for UAN/employment verification."""
    uan_number: str = Field(..., min_length=12, max_length=12, description="12-digit UAN")
    claimed_experience_years: Optional[int] = Field(
        None, 
        ge=0, 
        le=50,
        description="Candidate's claimed total experience in years"
    )


class ComparisonDetails(BaseModel):
    """Detailed comparison result."""
    name_match: bool
    name_score: Optional[int] = None
    dob_match: bool
    address_match: Optional[str] = None


class VerificationComparisonResult(BaseModel):
    """Result of Surepass verification with comparison."""
    status: str = Field(..., description="VERIFIED, PARTIAL, or FAILED")
    score: int = Field(..., ge=0, le=100)
    message: Optional[str] = None
    details: dict = Field(default_factory=dict)
    flags: List[str] = Field(default_factory=list)
    verified_at: Optional[datetime] = None


class StepVerificationResponse(BaseModel):
    """Response after Surepass verification step."""
    step_type: StepTypeSchema
    status: StepStatusSchema
    verification_result: VerificationComparisonResult
    message: str


# ============ Phase 3: Face Verification Schemas ============

class FaceDecisionSchema(str, Enum):
    """Face comparison decision."""
    MATCH = "MATCH"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    MISMATCH = "MISMATCH"
    PENDING_REFERENCE = "PENDING_REFERENCE"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    ERROR = "ERROR"


class ReferenceSourceSchema(str, Enum):
    """Source of face reference image."""
    HR_UPLOAD = "hr_upload"
    AADHAAR = "aadhaar"
    ID_CARD = "id_card"
    OTHER = "other"


class FaceSubmission(BaseModel):
    """Face verification submission from candidate."""
    selfie_image_base64: str = Field(
        ..., 
        description="Base64 encoded selfie image (JPEG/PNG)"
    )


class FaceReferenceUpload(BaseModel):
    """HR uploads reference image for comparison."""
    reference_image_base64: str = Field(
        ...,
        description="Base64 encoded reference image"
    )
    source: ReferenceSourceSchema = Field(
        default=ReferenceSourceSchema.HR_UPLOAD,
        description="Source of reference image"
    )


class FaceComparisonResponse(BaseModel):
    """Response from face comparison - HR safe view."""
    id: int
    decision: FaceDecisionSchema
    confidence_score: float = Field(..., ge=0, le=100)
    reference_source: Optional[ReferenceSourceSchema] = None
    selfie_url: Optional[str] = Field(None, description="Presigned URL for selfie")
    reference_url: Optional[str] = Field(None, description="Presigned URL for reference")
    flags: List[str] = Field(default_factory=list)
    compared_at: Optional[datetime] = None
    message: Optional[str] = None

    class Config:
        from_attributes = True


class FaceStepResponse(BaseModel):
    """Response after face step submission."""
    step_type: StepTypeSchema = StepTypeSchema.FACE_LIVENESS
    status: StepStatusSchema
    comparison: Optional[FaceComparisonResponse] = None
    message: str

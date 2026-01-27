"""
Candidate-side verification APIs (public, token-authenticated).

These endpoints are accessed via the one-time verification link.
No JWT required - authentication is via the verification token.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import logging

from ..database import get_db
from ..models import (
    Verification,
    VerificationStatus,
    VerificationStep,
    StepType,
    StepStatus,
    Candidate,
)
from ..schemas.verification import (
    CandidateVerificationSession,
    VerificationStepResponse,
    StepSubmissionResponse,
    VerificationSubmitResponse,
    PersonalInfoSubmission,
    FaceLivenessSubmission,
    AadhaarSubmission,
    PANSubmission,
    UANSubmission,
    EducationDocSubmission,
    ExperienceDocSubmission,
    StepTypeSchema,
    StepStatusSchema,
    # Phase 2 schemas
    AadhaarOTPRequest,
    AadhaarOTPSubmitRequest,
    AadhaarOTPResponse,
    PANVerificationRequest,
    UANVerificationRequest,
    StepVerificationResponse,
    VerificationComparisonResult,
)
from ..services.surepass import (
    AadhaarService,
    PANService,
    UANService,
    SurepassError,
    SurepassInvalidInputError,
)
from ..services.surepass.aadhaar import get_aadhaar_service
from ..services.surepass.pan import get_pan_service
from ..services.surepass.uan import get_uan_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/verify", tags=["Candidate Verification"])


def get_verification_by_token(token: str, db: Session) -> Verification:
    """
    Get verification by token.
    Validates token exists and is not expired.
    """
    verification = db.query(Verification).filter(
        Verification.token == token,
    ).first()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification not found. The link may be invalid.",
        )
    
    if verification.is_expired():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This verification link has expired. Please contact HR for a new link.",
        )
    
    if verification.status in [VerificationStatus.SUBMITTED, VerificationStatus.SCORED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This verification has already been submitted.",
        )
    
    return verification


def get_step_by_type(verification: Verification, step_type: StepType) -> VerificationStep:
    """Get a specific step from verification."""
    for step in verification.steps:
        if step.step_type == step_type:
            return step
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Step {step_type.value} not found in this verification.",
    )


def get_next_pending_step(verification: Verification) -> Optional[StepType]:
    """Get the next pending step in order."""
    step_order = [
        StepType.PERSONAL_INFO,
        StepType.FACE_LIVENESS,
        StepType.AADHAAR,
        StepType.PAN,
        StepType.UAN,
        StepType.EDUCATION,
        StepType.EXPERIENCE,
    ]
    
    for step_type in step_order:
        for step in verification.steps:
            if step.step_type == step_type and step.status == StepStatus.PENDING:
                return step_type
    return None


def can_submit_verification(verification: Verification) -> bool:
    """Check if all mandatory steps are completed."""
    for step in verification.steps:
        if step.is_mandatory and step.status not in [StepStatus.COMPLETED, StepStatus.SKIPPED]:
            return False
    return True


def _build_session_response(verification: Verification) -> CandidateVerificationSession:
    """Build session response for candidate."""
    steps = [
        VerificationStepResponse(
            id=step.id,
            step_type=step.step_type,
            is_mandatory=step.is_mandatory,
            status=step.status,
            completed_at=step.completed_at,
        )
        for step in verification.steps
    ]
    
    return CandidateVerificationSession(
        status=verification.status,
        token_expires_at=verification.token_expires_at,
        steps=steps,
        next_step=get_next_pending_step(verification),
        can_submit=can_submit_verification(verification),
    )


@router.get(
    "/{token}",
    response_model=CandidateVerificationSession,
    summary="Get verification session",
    description="Get the current state of the verification session. Use this to resume.",
)
async def get_verification_session(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Get verification session state.
    
    Returns:
    - Current status
    - All steps with their completion status
    - Next pending step
    - Whether submission is allowed
    """
    verification = get_verification_by_token(token, db)
    
    # Transition to IN_PROGRESS if this is first access
    if verification.status == VerificationStatus.LINK_SENT:
        verification.status = VerificationStatus.IN_PROGRESS
        db.commit()
        db.refresh(verification)
    
    return _build_session_response(verification)


@router.post(
    "/{token}/personal-info",
    response_model=StepSubmissionResponse,
    summary="Submit personal information",
)
async def submit_personal_info(
    token: str,
    data: PersonalInfoSubmission,
    db: Session = Depends(get_db),
):
    """Submit personal information step."""
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.PERSONAL_INFO)
    
    if step.status == StepStatus.COMPLETED:
        return StepSubmissionResponse(
            step_type=StepTypeSchema.PERSONAL_INFO,
            status=StepStatusSchema.COMPLETED,
            message="Personal info already submitted.",
        )
    
    # Store the input data
    step.mark_completed(input_data=data.model_dump())
    
    # Ensure status is IN_PROGRESS
    if verification.status == VerificationStatus.LINK_SENT:
        verification.status = VerificationStatus.IN_PROGRESS
    
    db.commit()
    
    return StepSubmissionResponse(
        step_type=StepTypeSchema.PERSONAL_INFO,
        status=StepStatusSchema.COMPLETED,
        message="Personal info submitted successfully.",
    )


@router.post(
    "/{token}/face",
    response_model=StepSubmissionResponse,
    summary="Submit face liveness",
)
async def submit_face_liveness(
    token: str,
    data: FaceLivenessSubmission,
    db: Session = Depends(get_db),
):
    """
    Submit face liveness step.
    
    Note: Phase 1 placeholder - stores data but doesn't call Rekognition.
    """
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.FACE_LIVENESS)
    
    if step.status == StepStatus.COMPLETED:
        return StepSubmissionResponse(
            step_type=StepTypeSchema.FACE_LIVENESS,
            status=StepStatusSchema.COMPLETED,
            message="Face liveness already submitted.",
        )
    
    # Store the data (actual verification in Phase 3)
    step.mark_completed(input_data={"selfie_submitted": True})
    
    if verification.status == VerificationStatus.LINK_SENT:
        verification.status = VerificationStatus.IN_PROGRESS
    
    db.commit()
    
    return StepSubmissionResponse(
        step_type=StepTypeSchema.FACE_LIVENESS,
        status=StepStatusSchema.COMPLETED,
        message="Face liveness submitted successfully.",
    )


@router.post(
    "/{token}/aadhaar",
    response_model=StepSubmissionResponse,
    summary="Submit Aadhaar verification (Phase 1 backward compat)",
    deprecated=True,
)
async def submit_aadhaar(
    token: str,
    data: AadhaarSubmission,
    db: Session = Depends(get_db),
):
    """
    Deprecated: Use /aadhaar/generate-otp and /aadhaar/submit-otp for OTP flow.
    
    This endpoint marks the step as pending for OTP verification.
    """
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.AADHAAR)
    
    if step.status == StepStatus.COMPLETED:
        return StepSubmissionResponse(
            step_type=StepTypeSchema.AADHAAR,
            status=StepStatusSchema.COMPLETED,
            message="Aadhaar already verified.",
        )
    
    # Store Aadhaar number for OTP flow
    step.input_data = {
        "aadhaar_number_masked": f"XXXX-XXXX-{data.aadhaar_number[-4:]}",
        "awaiting_otp": True,
    }
    
    if verification.status == VerificationStatus.LINK_SENT:
        verification.status = VerificationStatus.IN_PROGRESS
    
    db.commit()
    
    return StepSubmissionResponse(
        step_type=StepTypeSchema.AADHAAR,
        status=StepStatusSchema.PENDING,
        message="Aadhaar number stored. Please complete OTP verification via /aadhaar/generate-otp.",
    )


# ============ Phase 2: Aadhaar OTP Flow ============

@router.post(
    "/{token}/aadhaar/generate-otp",
    response_model=AadhaarOTPResponse,
    summary="Generate Aadhaar OTP",
    description="Request OTP to be sent to registered mobile number linked to Aadhaar.",
)
async def generate_aadhaar_otp(
    token: str,
    data: AadhaarOTPRequest,
    db: Session = Depends(get_db),
):
    """
    Generate Aadhaar OTP for verification.
    
    Flow:
    1. Validate Aadhaar number
    2. Call Surepass API (or mock)
    3. Return client_id for OTP submission
    """
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.AADHAAR)
    
    if step.status == StepStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aadhaar already verified.",
        )
    
    try:
        aadhaar_service = get_aadhaar_service()
        result = aadhaar_service.generate_otp(data.aadhaar_number)
        
        # Store client_id in step for later use
        step.input_data = {
            "aadhaar_number_masked": f"XXXX-XXXX-{data.aadhaar_number[-4:]}",
            "client_id": result.get("client_id"),
            "otp_sent_at": datetime.utcnow().isoformat(),
        }
        
        if verification.status == VerificationStatus.LINK_SENT:
            verification.status = VerificationStatus.IN_PROGRESS
        
        db.commit()
        
        logger.info(f"Aadhaar OTP generated for verification {verification.id}")
        
        return AadhaarOTPResponse(
            client_id=result.get("client_id", ""),
            otp_sent=result.get("otp_sent", True),
            message="OTP sent to registered mobile number.",
        )
        
    except SurepassInvalidInputError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except SurepassError as e:
        logger.error(f"Surepass error in generate_aadhaar_otp: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to send OTP. Please try again.",
        )


@router.post(
    "/{token}/aadhaar/submit-otp",
    response_model=StepVerificationResponse,
    summary="Submit Aadhaar OTP and verify",
    description="Submit OTP and complete Aadhaar verification with identity comparison.",
)
async def submit_aadhaar_otp(
    token: str,
    data: AadhaarOTPSubmitRequest,
    db: Session = Depends(get_db),
):
    """
    Submit Aadhaar OTP and complete verification.
    
    Flow:
    1. Submit OTP to Surepass
    2. Get verified Aadhaar data (name, DOB, address, photo)
    3. Compare with candidate data
    4. Mark step as COMPLETED/PARTIAL/FAILED
    """
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.AADHAAR)
    
    if step.status == StepStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aadhaar already verified.",
        )
    
    # Get stored client_id
    stored_client_id = step.input_data.get("client_id") if step.input_data else None
    
    # Use provided client_id or stored one
    client_id = data.client_id or stored_client_id
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing client_id. Please call /aadhaar/generate-otp first.",
        )
    
    try:
        aadhaar_service = get_aadhaar_service()
        
        # Submit OTP and get verified data
        surepass_data = aadhaar_service.submit_otp(client_id, data.otp)
        
        # Get candidate data for comparison
        candidate = verification.candidate
        
        # Compare Surepass data with candidate data
        comparison = aadhaar_service.compare(
            surepass_data=surepass_data,
            candidate_name=candidate.full_name,
            candidate_dob=str(candidate.dob) if candidate.dob else "",
        )
        
        # Determine step status based on comparison
        if comparison["status"] == "VERIFIED":
            step.status = StepStatus.COMPLETED
        elif comparison["status"] == "PARTIAL":
            step.status = StepStatus.COMPLETED  # Still mark as completed but with lower score
        else:
            step.status = StepStatus.FAILED
        
        step.completed_at = datetime.utcnow()
        step.score_contribution = comparison["score"]
        step.input_data = {
            **(step.input_data or {}),
            "verified": True,
            "comparison": comparison["details"],
        }
        step.raw_response = surepass_data  # Store for audit (encrypted at DB level)
        
        db.commit()
        
        logger.info(f"Aadhaar verification completed for verification {verification.id}: {comparison['status']}")
        
        return StepVerificationResponse(
            step_type=StepTypeSchema.AADHAAR,
            status=step.status,
            verification_result=VerificationComparisonResult(
                status=comparison["status"],
                score=comparison["score"],
                details=comparison["details"],
                verified_at=datetime.utcnow(),
            ),
            message=f"Aadhaar verification {comparison['status'].lower()}.",
        )
        
    except SurepassInvalidInputError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except SurepassError as e:
        logger.error(f"Surepass error in submit_aadhaar_otp: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OTP verification failed. Please try again.",
        )


@router.post(
    "/{token}/pan",
    response_model=StepVerificationResponse,
    summary="Submit PAN verification",
    description="Verify PAN and cross-check with Aadhaar-verified name/DOB.",
)
async def submit_pan(
    token: str,
    data: PANSubmission,
    db: Session = Depends(get_db),
):
    """
    Submit PAN verification step.
    
    Uses Aadhaar-verified name and DOB for cross-check.
    Surepass returns name_match, dob_match, aadhaar_seeding_status.
    """
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.PAN)
    
    if step.status == StepStatus.COMPLETED:
        return StepVerificationResponse(
            step_type=StepTypeSchema.PAN,
            status=StepStatusSchema.COMPLETED,
            verification_result=VerificationComparisonResult(
                status="VERIFIED",
                score=step.score_contribution or 100,
                details={},
            ),
            message="PAN already verified.",
        )
    
    # Get Aadhaar step to retrieve verified name/DOB
    aadhaar_step = get_step_by_type(verification, StepType.AADHAAR)
    
    # Get verified name/DOB from Aadhaar (or candidate profile)
    candidate = verification.candidate
    aadhaar_name = candidate.full_name
    aadhaar_dob = str(candidate.dob) if candidate.dob else ""
    
    # If Aadhaar was verified, try to get the verified data
    if aadhaar_step.raw_response:
        aadhaar_name = aadhaar_step.raw_response.get("full_name", aadhaar_name)
        aadhaar_dob = aadhaar_step.raw_response.get("dob", aadhaar_dob)
    
    try:
        pan_service = get_pan_service()
        result = pan_service.verify(
            pan_number=data.pan_number,
            name=aadhaar_name,
            dob=aadhaar_dob,
        )
        
        # Determine step status
        if result["status"] == "VERIFIED":
            step.status = StepStatus.COMPLETED
        elif result["status"] == "PARTIAL":
            step.status = StepStatus.COMPLETED  # Still complete but flag
        else:
            step.status = StepStatus.FAILED
        
        step.completed_at = datetime.utcnow()
        step.score_contribution = result["score"]
        step.input_data = {
            "pan_number": data.pan_number.upper(),
            "verification_result": result["details"],
        }
        
        if verification.status == VerificationStatus.LINK_SENT:
            verification.status = VerificationStatus.IN_PROGRESS
        
        db.commit()
        
        logger.info(f"PAN verification completed for verification {verification.id}: {result['status']}")
        
        return StepVerificationResponse(
            step_type=StepTypeSchema.PAN,
            status=step.status,
            verification_result=VerificationComparisonResult(
                status=result["status"],
                score=result["score"],
                message=result.get("message"),
                details=result["details"],
                verified_at=datetime.utcnow(),
            ),
            message=result.get("message", f"PAN verification {result['status'].lower()}."),
        )
        
    except SurepassInvalidInputError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except SurepassError as e:
        logger.error(f"Surepass error in submit_pan: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="PAN verification failed. Please try again.",
        )


@router.post(
    "/{token}/uan",
    response_model=StepVerificationResponse,
    summary="Submit UAN verification (conditional)",
    description="Verify UAN and analyze employment history. Detects overlaps.",
)
async def submit_uan(
    token: str,
    data: UANVerificationRequest,
    db: Session = Depends(get_db),
):
    """
    Submit UAN verification step (conditional).
    
    Flow:
    1. Verify UAN with Surepass
    2. Compare identity with Aadhaar
    3. Analyze employment history for overlaps
    4. Flag moonlighting if detected (but don't auto-reject)
    """
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.UAN)
    
    if step.status == StepStatus.COMPLETED:
        return StepVerificationResponse(
            step_type=StepTypeSchema.UAN,
            status=StepStatusSchema.COMPLETED,
            verification_result=VerificationComparisonResult(
                status="VERIFIED",
                score=step.score_contribution or 100,
                details={},
            ),
            message="UAN already verified.",
        )
    
    # Get Aadhaar-verified data for identity comparison
    aadhaar_step = get_step_by_type(verification, StepType.AADHAAR)
    candidate = verification.candidate
    
    aadhaar_name = candidate.full_name
    aadhaar_dob = str(candidate.dob) if candidate.dob else ""
    
    if aadhaar_step.raw_response:
        aadhaar_name = aadhaar_step.raw_response.get("full_name", aadhaar_name)
        aadhaar_dob = aadhaar_step.raw_response.get("dob", aadhaar_dob)
    
    try:
        uan_service = get_uan_service()
        
        # Verify UAN
        uan_data = uan_service.verify(data.uan_number)
        
        # Analyze employment and compare identity
        analysis = uan_service.analyze(
            surepass_data=uan_data,
            aadhaar_name=aadhaar_name,
            aadhaar_dob=aadhaar_dob,
            claimed_experience_years=data.claimed_experience_years,
        )
        
        # Determine step status
        if analysis["status"] == "VERIFIED":
            step.status = StepStatus.COMPLETED
        elif analysis["status"] == "PARTIAL":
            step.status = StepStatus.COMPLETED  # Still complete but with flags
        else:
            step.status = StepStatus.FAILED
        
        step.completed_at = datetime.utcnow()
        step.score_contribution = analysis["score"]
        step.input_data = {
            "uan_number": data.uan_number,
            "claimed_experience_years": data.claimed_experience_years,
            "analysis": analysis["details"],
            "flags": analysis["flags"],
        }
        step.raw_response = uan_data
        
        if verification.status == VerificationStatus.LINK_SENT:
            verification.status = VerificationStatus.IN_PROGRESS
        
        db.commit()
        
        logger.info(f"UAN verification completed for verification {verification.id}: {analysis['status']} with flags {analysis['flags']}")
        
        return StepVerificationResponse(
            step_type=StepTypeSchema.UAN,
            status=step.status,
            verification_result=VerificationComparisonResult(
                status=analysis["status"],
                score=analysis["score"],
                details=analysis["details"],
                flags=analysis["flags"],
                verified_at=datetime.utcnow(),
            ),
            message=f"UAN verification {analysis['status'].lower()}." + 
                    (f" Flags: {', '.join(analysis['flags'])}" if analysis["flags"] else ""),
        )
        
    except SurepassInvalidInputError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except SurepassError as e:
        logger.error(f"Surepass error in submit_uan: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="UAN verification failed. Please try again.",
        )


@router.post(
    "/{token}/education",
    response_model=StepSubmissionResponse,
    summary="Submit education documents (conditional)",
)
async def submit_education(
    token: str,
    data: EducationDocSubmission,
    db: Session = Depends(get_db),
):
    """Submit education document step (conditional)."""
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.EDUCATION)
    
    if step.status == StepStatus.COMPLETED:
        return StepSubmissionResponse(
            step_type=StepTypeSchema.EDUCATION,
            status=StepStatusSchema.COMPLETED,
            message="Education document already submitted.",
        )
    
    step.mark_completed(input_data={
        "document_type": data.document_type,
        "institution_name": data.institution_name,
        "year_of_passing": data.year_of_passing,
        "document_submitted": True,
    })
    
    if verification.status == VerificationStatus.LINK_SENT:
        verification.status = VerificationStatus.IN_PROGRESS
    
    db.commit()
    
    return StepSubmissionResponse(
        step_type=StepTypeSchema.EDUCATION,
        status=StepStatusSchema.COMPLETED,
        message="Education document submitted successfully.",
    )


@router.post(
    "/{token}/experience",
    response_model=StepSubmissionResponse,
    summary="Submit experience documents (conditional)",
)
async def submit_experience(
    token: str,
    data: ExperienceDocSubmission,
    db: Session = Depends(get_db),
):
    """Submit experience document step (conditional)."""
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.EXPERIENCE)
    
    if step.status == StepStatus.COMPLETED:
        return StepSubmissionResponse(
            step_type=StepTypeSchema.EXPERIENCE,
            status=StepStatusSchema.COMPLETED,
            message="Experience document already submitted.",
        )
    
    step.mark_completed(input_data={
        "document_type": data.document_type,
        "company_name": data.company_name,
        "start_date": data.start_date,
        "end_date": data.end_date,
        "document_submitted": True,
    })
    
    if verification.status == VerificationStatus.LINK_SENT:
        verification.status = VerificationStatus.IN_PROGRESS
    
    db.commit()
    
    return StepSubmissionResponse(
        step_type=StepTypeSchema.EXPERIENCE,
        status=StepStatusSchema.COMPLETED,
        message="Experience document submitted successfully.",
    )


@router.post(
    "/{token}/skip/{step_type}",
    response_model=StepSubmissionResponse,
    summary="Skip an optional step",
)
async def skip_step(
    token: str,
    step_type: str,
    db: Session = Depends(get_db),
):
    """Skip an optional (non-mandatory) step."""
    verification = get_verification_by_token(token, db)
    
    try:
        step_type_enum = StepType(step_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid step type: {step_type}",
        )
    
    step = get_step_by_type(verification, step_type_enum)
    
    if step.is_mandatory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot skip mandatory steps.",
        )
    
    if step.status != StepStatus.PENDING:
        return StepSubmissionResponse(
            step_type=step_type_enum,
            status=step.status,
            message=f"Step already {step.status.value.lower()}.",
        )
    
    step.mark_skipped()
    db.commit()
    
    return StepSubmissionResponse(
        step_type=step_type_enum,
        status=StepStatusSchema.SKIPPED,
        message=f"Step {step_type} skipped.",
    )


@router.post(
    "/{token}/submit",
    response_model=VerificationSubmitResponse,
    summary="Final submission",
    description="Submit the verification for scoring. All mandatory steps must be completed.",
)
async def final_submit(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Final submission of verification.
    
    - Validates all mandatory steps are completed
    - Transitions status to SUBMITTED
    - Trust score remains NULL (calculated in Phase 4)
    """
    verification = get_verification_by_token(token, db)
    
    # Check all mandatory steps are completed
    incomplete_mandatory = []
    for step in verification.steps:
        if step.is_mandatory and step.status not in [StepStatus.COMPLETED]:
            incomplete_mandatory.append(step.step_type.value)
    
    if incomplete_mandatory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot submit: incomplete mandatory steps: {', '.join(incomplete_mandatory)}",
        )
    
    # Transition to SUBMITTED
    verification.status = VerificationStatus.SUBMITTED
    verification.submitted_at = datetime.utcnow()
    # trust_score remains NULL - Phase 4 will calculate it
    
    db.commit()
    db.refresh(verification)
    
    return VerificationSubmitResponse(
        status=VerificationStatus.SUBMITTED,
        message="Verification submitted successfully. Trust score will be calculated shortly.",
        submitted_at=verification.submitted_at,
    )

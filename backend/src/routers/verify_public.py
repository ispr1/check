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
    AadhaarDigiLockerInitRequest,
    AadhaarDigiLockerResponse,
    AadhaarDigiLockerCompleteRequest,
    PANVerificationRequest,
    UANVerificationRequest,
    StepVerificationResponse,
    VerificationComparisonResult,
    CandidatePublicProfile,
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
from ..services.face.rekognition import RekognitionProvider

# Duplicate removal complete
from ..utils.face_storage import get_face_storage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/verify", tags=["Candidate Verification"])


async def _run_face_comparison(
    verification: Verification,
    face_step: VerificationStep,
    selfie_key: str,
    reference_key: str,
    db: Session,
):
    """
    Run face comparison between selfie and reference.
    Updates face_step status and metadata.
    """
    try:
        storage = get_face_storage()
        rekognition = RekognitionProvider()
        
        # Get images
        selfie_bytes = storage.get_image(selfie_key)
        reference_bytes = storage.get_image(reference_key)
        
        if not selfie_bytes or not reference_bytes:
            logger.error(f"Missing image bytes for verification {verification.id}")
            return

        # Run comparison
        result = rekognition.compare_faces(
            source_bytes=selfie_bytes,
            target_bytes=reference_bytes,
            source_key=selfie_key,
            target_key=reference_key,
        )
        
        # Update step based on result
        face_step.score_contribution = result.confidence_score
        
        # Update metadata
        input_data = face_step.input_data or {}
        input_data.update({
            "comparison_status": result.decision.value,
            "confidence_score": result.confidence_score,
            "flags": result.flags,
            "compared_at": result.compared_at.isoformat(),
            "reference_source": result.reference_source.value,
        })
        face_step.input_data = input_data
        
        # Mark step status
        if result.decision.value == "MATCH":
            face_step.status = StepStatus.COMPLETED
            logger.info(f"Face MATCH for verification {verification.id} ({result.confidence_score}%)")
        elif result.decision.value == "MISMATCH":
            # We mark as COMPLETED even on mismatch so user can proceed to next steps.
            # The mismatch is flagged in metadata for HR review.
            face_step.status = StepStatus.COMPLETED
            logger.warning(f"Face MISMATCH for verification {verification.id} ({result.confidence_score}%)")
        else:
            # Low confidence / Review needed
            face_step.status = StepStatus.COMPLETED
            logger.warning(f"Face LOW_CONFIDENCE for verification {verification.id} ({result.confidence_score}%)")
            
        db.commit()
        
    except Exception as e:
        logger.error(f"Face comparison failed for verification {verification.id}: {e}")
        # Don't fail the request, just log error



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
            metadata=step.input_data  # Mapped input_data to metadata
        )
        for step in verification.steps
    ]
    
    return CandidateVerificationSession(
        status=verification.status,
        token_expires_at=verification.token_expires_at,
        candidate=CandidatePublicProfile(
            full_name=verification.candidate.full_name,
            email=verification.candidate.email, # Ensure model has email
        ),
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
    
    # Self-healing: Ensure mandatory steps exist if in initial states
    if not verification.steps and verification.status in [VerificationStatus.CREATED, VerificationStatus.LINK_SENT, VerificationStatus.IN_PROGRESS]:
        logger.warning(f"Verification {verification.id} has no steps. Re-initializing mandatory steps.")
        for step_type in MANDATORY_STEPS:
            step = VerificationStep(
                verification_id=verification.id,
                step_type=step_type,
                is_mandatory=True,
                status=StepStatus.PENDING,
            )
            db.add(step)
        db.commit()
        db.refresh(verification)
    
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
    
    # Update Candidate Profile
    candidate = verification.candidate
    candidate.full_name = data.full_name
    candidate.dob = data.dob
    candidate.email = data.email
    # Phone if needed, but usually phone is verified separately or assumed valid
    
    # Store the input data (including address/parents)
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
    
    # Save Selfie to Storage
    storage = get_face_storage()
    try:
        candidate_id = verification.candidate_id
        selfie_key = storage.save_selfie(candidate_id, data.selfie_image_base64)
    except Exception as e:
        logger.error(f"Failed to save selfie: {e}")
        raise HTTPException(status_code=500, detail="Failed to save selfie image.")

    # Update Step with storage key
    step.mark_completed(input_data={
        "selfie_submitted": True,
        "source_key": selfie_key
    })
    
    if verification.status == VerificationStatus.LINK_SENT:
        verification.status = VerificationStatus.IN_PROGRESS
    
    db.commit()
    
    return StepSubmissionResponse(
        step_type=StepTypeSchema.FACE_LIVENESS,
        status=StepStatusSchema.COMPLETED, # Or based on comparison result if immediate
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


# ============ Phase 2: Aadhaar DigiLocker Flow (Production) ============

@router.post(
    "/{token}/aadhaar/initiate",
    response_model=AadhaarDigiLockerResponse,
    summary="Initiate Aadhaar DigiLocker flow",
    description="Start DigiLocker session and get redirect URL.",
)
async def initiate_aadhaar_digilocker(
    token: str,
    data: AadhaarDigiLockerInitRequest,
    db: Session = Depends(get_db),
):
    """
    Start DigiLocker verification flow.
    Replaces the OTP flow for production.
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
        
        # Initiate session
        result = aadhaar_service.initiate_digilocker_flow(data.redirect_url)
        
        # Store client_id in step
        step.input_data = {
            "client_id": result.get("client_id"),
            "token": result.get("token"),
            "initiated_at": datetime.utcnow().isoformat(),
            "status": "awaiting_redirect"
        }
        
        if verification.status == VerificationStatus.LINK_SENT:
            verification.status = VerificationStatus.IN_PROGRESS
        
        db.commit()
        db.refresh(step)
        
        logger.info(f"Initiated Aadhaar DigiLocker session for step {step.id}: {step.input_data}")
        
        return AadhaarDigiLockerResponse(
            client_id=result.get("client_id"),
            url=result.get("url"),
            expiry_seconds=result.get("expiry_seconds", 1800),
            message="DigiLocker session initiated.",
        )
        
    except SurepassError as e:
        logger.error(f"Surepass error in initiate_aadhaar: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to initiate DigiLocker. Please try again.",
        )


@router.post(
    "/{token}/aadhaar/complete",
    response_model=StepVerificationResponse,
    summary="Complete Aadhaar verification (DigiLocker)",
    description="Fetch data from DigiLocker after user returns, and verify identity.",
)
async def complete_aadhaar_digilocker(
    token: str,
    data: Optional[AadhaarDigiLockerCompleteRequest] = None,
    db: Session = Depends(get_db),
):
    """
    Complete Aadhaar verification after DigiLocker redirect.
    """
    logger.info(f"Received Aadhaar completion request for token: {token}")
    verification = get_verification_by_token(token, db)
    step = get_step_by_type(verification, StepType.AADHAAR)
    
    if step.status == StepStatus.COMPLETED:
        if step.input_data and step.input_data.get("comparison"):
            return StepVerificationResponse(
                step_type=StepTypeSchema.AADHAAR,
                status=StepStatusSchema.COMPLETED,
                verification_result=VerificationComparisonResult(
                    status="VERIFIED",
                    score=step.score_contribution or 100,
                    details=step.input_data["comparison"],
                    verified_at=step.completed_at,
                ),
                message="Aadhaar already verified.",
            )
    
    # Get stored client_id
    client_id = data.client_id if data and data.client_id else None
    if not client_id:
        client_id = step.input_data.get("client_id") if step.input_data else None
    
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active DigiLocker session found. Please initiate first.",
        )
        
    try:
        aadhaar_service = get_aadhaar_service()
        logger.info(f"Fetching DigiLocker data for client_id: {client_id}")
        
        # Fetch data
        response = aadhaar_service.fetch_digilocker_data(client_id)
        
        # DEBUG: Log exact type and snippet
        logger.info(f"Aadhaar service response type: {type(response)}")
        with open("aadhaar_debug.txt", "w") as f:
            f.write(f"Type: {type(response)}\n")
            f.write(f"Content: {str(response)[:1000]}\n")

        # Robust unwrapping: handle lists and dicts
        surepass_data = None
        if isinstance(response, list) and len(response) > 0:
            logger.info("Aadhaar response is a list, taking first element")
            response = response[0]
            
        if isinstance(response, dict):
            if "data" in response:
                surepass_data = response["data"]
            elif "aadhaar_xml_data" in response:
                # FIX: Extract the nested dictionary instead of keeping the root
                surepass_data = response["aadhaar_xml_data"]
            else:
                surepass_data = response
        
        # Ensure we have a dict before proceeding
        if not isinstance(surepass_data, dict):
            type_name = type(response).__name__ if response is not None else "NoneType"
            logger.error(f"Unexpected response type from Aadhaar service: {type_name}")
            raise SurepassError(f"Aadhaar service returned empty or invalid data (Type: {type_name}). Please try Re-connecting.")

        # SAVE ASAP: Ensure we store the raw data even if comparison fails
        step.raw_response = surepass_data
        db.commit()
        
        logger.info(f"Processing Aadhaar data. Keys: {list(surepass_data.keys())}")

        # Validate basic data presence
        if not any(k in surepass_data for k in ["full_name", "name", "aadhaar_xml_data"]):
             logger.warning(f"Surepass data missing primary identification keys. Data: {surepass_data}")

        # Compare
        candidate = verification.candidate
        comparison = aadhaar_service.compare(
            surepass_data=surepass_data,
            candidate_name=candidate.full_name,
            candidate_dob=str(candidate.dob) if candidate.dob else "",
        )
        
        logger.info(f"Aadhaar comparison complete: {comparison['status']} (Score: {comparison['score']})")

        # Update Status
        if comparison["status"] in ["VERIFIED", "PARTIAL"]:
            step.status = StepStatus.COMPLETED
        else:
            step.status = StepStatus.FAILED
            
        step.completed_at = datetime.utcnow()
        step.score_contribution = comparison["score"]
        
        # Save Aadhaar Photo as Reference
        reference_key = None
        if "profile_image" in surepass_data.get("aadhaar_xml_data", {}):
            try:
                storage = get_face_storage()
                raw_image = surepass_data["aadhaar_xml_data"]["profile_image"]
                reference_key = storage.save_reference(
                    verification.candidate_id, 
                    raw_image, 
                    source="aadhaar"
                )
            except Exception as e:
                logger.error(f"Failed to save Aadhaar reference photo: {e}")

        step.input_data = {
            **(step.input_data or {}),
            "verified": True,
            "comparison": comparison["details"],
            "status": "completed",
            "reference_key": reference_key
        }
        step.raw_response = surepass_data
        
        db.commit()
        db.refresh(step)
        
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
        
    except Exception as e:
        import traceback
        logger.error(f"CRITICAL ERROR in complete_aadhaar: {str(e)}")
        logger.error(traceback.format_exc())
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )


@router.post(
    "/{token}/pan",
    response_model=StepVerificationResponse,
    summary="Submit PAN verification",
    description="Verify PAN and cross-check with Aadhaar-verified name/DOB.",
)
async def submit_pan(
    token: str,
    data: PANVerificationRequest,
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
    
    # SKIP VERIFICATION (User Request: Store only)
    # comparison = pan_service.verify(data.pan_number, aadhaar_name, aadhaar_dob)
    
    # Store Input Only
    step.input_data = {
        "pan_number": data.pan_number,
        "verified": False, # pending batch verification
        "status": "pending"
    }
    step.status = StepStatus.COMPLETED
    step.score_contribution = 0 # No score yet
    step.completed_at = datetime.utcnow()
    
    db.commit()

    return StepVerificationResponse(
        step_type=StepTypeSchema.PAN,
        status=StepStatusSchema.COMPLETED,
        verification_result=VerificationComparisonResult(
            status="PENDING",
            score=0,
            details={"message": "PAN stored for later verification"},
            verified_at=None,
        ),
        message="PAN details stored successfully.",
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
    
    # Handle Fresher Case
    if data.is_fresher:
        step.status = StepStatus.SKIPPED
        step.input_data = {
            "is_fresher": True,
            "uan_number": None,
            "claimed_experience_years": 0
        }
        step.completed_at = datetime.utcnow()
        step.score_contribution = 100 # Neutral/Full score as it's not applicable
        
        if verification.status == VerificationStatus.LINK_SENT:
            verification.status = VerificationStatus.IN_PROGRESS
            
        db.commit()
        
        return StepVerificationResponse(
            step_type=StepTypeSchema.UAN,
            status=StepStatusSchema.SKIPPED,
            verification_result=VerificationComparisonResult(
                status="SKIPPED",
                score=100,
                details={"message": "Candidate is a fresher"},
                verified_at=datetime.utcnow(),
            ),
            message="UAN skipped (Fresher).",
        )

    # Validate UAN if not fresher
    if not data.uan_number:
         raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="UAN number is required for experienced candidates.",
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
    
    step.status = StepStatus.SKIPPED
    db.commit()
    
    return StepSubmissionResponse(
        step_type=step_type_enum,
        status=StepStatusSchema.SKIPPED,
        message=f"Step skipped.",
    )


@router.post(
    "/{token}/submit",
    response_model=VerificationSubmitResponse,
    summary="Finalize verification submission",
)
async def submit_verification(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Finalize the verification process.
    Matches the user's "Consent & Submit" action.
    """
    verification = get_verification_by_token(token, db)
    
    # Check if all mandatory steps are completed
    pending_mandatory = db.query(VerificationStep).filter(
        VerificationStep.verification_id == verification.id,
        VerificationStep.is_mandatory == True,
        VerificationStep.status.in_([StepStatus.PENDING, StepStatus.FAILED])
    ).count()
    
    if pending_mandatory > 0:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot submit. Mandatory steps are pending.",
        )
        
    # Update status
    verification.status = VerificationStatus.SUBMITTED
    verification.submitted_at = datetime.utcnow()
    
    # Run Face Comparison (deferred until submission)
    face_step = get_step_by_type(verification, StepType.FACE_LIVENESS)
    aadhaar_step = get_step_by_type(verification, StepType.AADHAAR)
    
    if (face_step.status == StepStatus.COMPLETED and face_step.input_data and 
        aadhaar_step.status == StepStatus.COMPLETED and aadhaar_step.input_data):
        
        selfie_key = face_step.input_data.get("source_key")
        reference_key = aadhaar_step.input_data.get("reference_key")
        
        if selfie_key and reference_key:
            logger.info(f"Running deferred face comparison for {verification.id}")
            # We don't await so the user doesn't wait, but for sqlite/simplicity we might have to.
            # Using await ensures DB consistency before response.
            await _run_face_comparison(verification, face_step, selfie_key, reference_key, db)

    db.commit()
    
    return VerificationSubmitResponse(
        status=VerificationStatusSchema.SUBMITTED,
        message="Verification submitted successfully.",
        submitted_at=verification.submitted_at
    )

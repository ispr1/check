"""
HR-side verification APIs.

Endpoints for HR to start, view, and list verification sessions.
Requires JWT authentication with admin/hr role.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import (
    Verification,
    VerificationStatus,
    VerificationStep,
    StepType,
    StepStatus,
    MANDATORY_STEPS,
    Candidate,
    User,
)
from ..schemas.verification import (
    VerificationStartRequest,
    VerificationResponse,
    VerificationListItem,
    VerificationStepResponse,
)
from ..dependencies import get_current_user, require_roles


router = APIRouter(prefix="/verifications", tags=["Verifications"])

# Base URL for verification links - should come from config
VERIFICATION_BASE_URL = "http://localhost:8000/api/v1/verify"


def _create_verification_steps(
    verification_id: int,
    include_uan: bool,
    include_education: bool,
    include_experience: bool,
    db: Session,
) -> List[VerificationStep]:
    """Create verification steps based on configuration."""
    steps = []
    
    # Create mandatory steps
    for step_type in MANDATORY_STEPS:
        step = VerificationStep(
            verification_id=verification_id,
            step_type=step_type,
            is_mandatory=True,
            status=StepStatus.PENDING,
        )
        steps.append(step)
        db.add(step)
    
    # Create conditional steps based on flags
    if include_uan:
        step = VerificationStep(
            verification_id=verification_id,
            step_type=StepType.UAN,
            is_mandatory=False,
            status=StepStatus.PENDING,
        )
        steps.append(step)
        db.add(step)
    
    if include_education:
        step = VerificationStep(
            verification_id=verification_id,
            step_type=StepType.EDUCATION,
            is_mandatory=False,
            status=StepStatus.PENDING,
        )
        steps.append(step)
        db.add(step)
    
    if include_experience:
        step = VerificationStep(
            verification_id=verification_id,
            step_type=StepType.EXPERIENCE,
            is_mandatory=False,
            status=StepStatus.PENDING,
        )
        steps.append(step)
        db.add(step)
    
    return steps


def _build_verification_response(
    verification: Verification,
    candidate: Candidate,
) -> VerificationResponse:
    """Build response with verification link."""
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
    
    return VerificationResponse(
        id=verification.id,
        candidate_id=verification.candidate_id,
        candidate_name=candidate.full_name,
        company_id=verification.company_id,
        token=verification.token,
        verification_link=f"{VERIFICATION_BASE_URL}/{verification.token}",
        token_expires_at=verification.token_expires_at,
        status=verification.status,
        trust_score=verification.trust_score,
        submitted_at=verification.submitted_at,
        created_at=verification.created_at,
        steps=steps,
    )


@router.post(
    "/start",
    response_model=VerificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start a verification for a candidate",
    description="Generate a one-time verification link that the candidate uses to complete verification steps.",
)
async def start_verification(
    request: VerificationStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "hr"])),
):
    """
    Start a verification session for a candidate.
    
    - Generates a unique, secure token valid for 7 days
    - Creates mandatory steps (Personal Info, Face, Aadhaar, PAN)
    - Creates conditional steps based on request flags
    - Returns verification link for the candidate
    """
    # Check if candidate exists and belongs to user's company
    candidate = db.query(Candidate).filter(
        Candidate.id == request.candidate_id,
        Candidate.company_id == current_user.company_id,
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found in your company",
        )
    
    # Check if candidate already has an active verification
    existing_verification = db.query(Verification).filter(
        Verification.candidate_id == request.candidate_id,
    ).first()
    
    if existing_verification:
        # If expired or scored, allow creating new one by deleting old
        if existing_verification.is_expired() or existing_verification.status == VerificationStatus.SCORED:
            db.delete(existing_verification)
            db.flush()
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Candidate already has an active verification (status: {existing_verification.status.value}). "
                       f"Complete or wait for expiry before starting a new one.",
            )
    
    # Create new verification
    verification = Verification(
        candidate_id=request.candidate_id,
        company_id=current_user.company_id,
        status=VerificationStatus.LINK_SENT,
    )
    db.add(verification)
    db.flush()  # Get the ID
    
    # Create steps
    _create_verification_steps(
        verification_id=verification.id,
        include_uan=request.include_uan,
        include_education=request.include_education,
        include_experience=request.include_experience,
        db=db,
    )
    
    db.commit()
    db.refresh(verification)
    
    return _build_verification_response(verification, candidate)


@router.get(
    "/{verification_id}",
    response_model=VerificationResponse,
    summary="Get verification details",
    description="Get full details of a verification including all steps and their status.",
)
async def get_verification(
    verification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "hr"])),
):
    """Get verification details by ID."""
    verification = db.query(Verification).filter(
        Verification.id == verification_id,
        Verification.company_id == current_user.company_id,
    ).first()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification not found",
        )
    
    candidate = db.query(Candidate).filter(
        Candidate.id == verification.candidate_id,
    ).first()
    
    return _build_verification_response(verification, candidate)


@router.get(
    "",
    response_model=List[VerificationListItem],
    summary="List all verifications",
    description="Get all verifications for the current user's company with optional status filter.",
)
async def list_verifications(
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "hr"])),
):
    """List all verifications for the company."""
    query = db.query(Verification).filter(
        Verification.company_id == current_user.company_id,
    )
    
    # Apply status filter if provided
    if status_filter:
        try:
            status_enum = VerificationStatus(status_filter)
            query = query.filter(Verification.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter. Valid values: {[s.value for s in VerificationStatus]}",
            )
    
    verifications = query.order_by(Verification.created_at.desc()).all()
    
    result = []
    for v in verifications:
        candidate = db.query(Candidate).filter(Candidate.id == v.candidate_id).first()
        steps_completed = len([s for s in v.steps if s.status == StepStatus.COMPLETED])
        steps_total = len(v.steps)
        
        result.append(
            VerificationListItem(
                id=v.id,
                candidate_id=v.candidate_id,
                candidate_name=candidate.full_name if candidate else "Unknown",
                status=v.status,
                trust_score=v.trust_score,
                created_at=v.created_at,
                token_expires_at=v.token_expires_at,
                steps_completed=steps_completed,
                steps_total=steps_total,
            )
        )
    
    return result

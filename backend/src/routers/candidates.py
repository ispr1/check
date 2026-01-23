from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.candidate import Candidate
from ..schemas.candidate import CandidateCreate, CandidateResponse, CandidateListItem
from ..dependencies import get_current_user, require_roles
from ..models.user import User

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new candidate",
    description="Create a candidate linked to the current user's company. HR/Admin only.",
)
async def create_candidate(
    candidate_data: CandidateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "hr"])),
):
    """
    Create a new candidate for the current user's company.

    - **full_name**: Candidate's full name (required)
    - **dob**: Date of birth (required)
    - **email**: Email address (optional, must be unique per company if provided)
    """
    # Check for duplicate email within the same company
    if candidate_data.email:
        existing = (
            db.query(Candidate)
            .filter(
                Candidate.email == candidate_data.email,
                Candidate.company_id == current_user.company_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A candidate with this email already exists in your company",
            )

    # Create new candidate
    new_candidate = Candidate(
        company_id=current_user.company_id,
        full_name=candidate_data.full_name,
        dob=candidate_data.dob,
        email=candidate_data.email,
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


@router.get(
    "",
    response_model=List[CandidateListItem],
    summary="List all candidates",
    description="Get all candidates belonging to the current user's company. HR/Admin only.",
)
async def list_candidates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "hr"])),
):
    """
    Retrieve all candidates for the current user's company.

    Returns basic information including:
    - Candidate ID
    - Full name
    - Created date
    - Trust score (if available)
    """
    candidates = (
        db.query(Candidate)
        .filter(Candidate.company_id == current_user.company_id)
        .order_by(Candidate.created_at.desc())
        .all()
    )

    # Map to response format with trust_score placeholder
    result = []
    for candidate in candidates:
        result.append(
            CandidateListItem(
                id=candidate.id,
                full_name=candidate.full_name,
                created_at=candidate.created_at,
                trust_score=None,  # Will be calculated later when trust scoring is implemented
            )
        )

    return result

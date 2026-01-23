from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.verification_request import VerificationRequest
from ..models.candidate import Candidate
from ..schemas.verification_request import (
    VerificationRequestCreate,
    VerificationRequestResponse,
    VerificationRequestListItem,
)
from ..dependencies import get_current_user, require_roles
from ..models.user import User

router = APIRouter(prefix="/verification-requests", tags=["Verification Requests"])


@router.post(
    "",
    response_model=VerificationRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a verification request",
    description="Create a new verification request for a candidate. HR/Admin only.",
)
async def create_verification_request(
    request_data: VerificationRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "hr"])),
):
    """
    Create a verification request for a candidate.

    - **candidate_id**: ID of the candidate to verify (required)

    The candidate must belong to the current user's company.
    Status is automatically set to 'draft'.
    """
    # Verify candidate exists and belongs to user's company
    candidate = (
        db.query(Candidate).filter(Candidate.id == request_data.candidate_id).first()
    )

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )

    if candidate.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create verification requests for candidates in your company",
        )

    # Check if there's already an active request for this candidate
    existing_request = (
        db.query(VerificationRequest)
        .filter(
            VerificationRequest.candidate_id == request_data.candidate_id,
            VerificationRequest.company_id == current_user.company_id,
            VerificationRequest.status.in_(["draft", "pending", "in_progress"]),
        )
        .first()
    )

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An active verification request already exists for this candidate (Status: {existing_request.status})",
        )

    # Create new verification request
    new_request = VerificationRequest(
        candidate_id=request_data.candidate_id,
        company_id=current_user.company_id,
        status="draft",
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # Prepare response with candidate name
    response = VerificationRequestResponse(
        id=new_request.id,
        candidate_id=new_request.candidate_id,
        company_id=new_request.company_id,
        status=new_request.status,
        created_at=new_request.created_at,
        candidate_name=candidate.full_name,
    )

    return response


@router.get(
    "",
    response_model=List[VerificationRequestListItem],
    summary="List verification requests",
    description="Get all verification requests for the current user's company. HR/Admin only.",
)
async def list_verification_requests(
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "hr"])),
):
    """
    Retrieve all verification requests for the current user's company.

    Query Parameters:
    - **status_filter**: Optional filter by status (draft, pending, in_progress, completed, cancelled)

    Returns:
    - Request ID
    - Candidate ID and name
    - Request status
    - Created date
    """
    query = db.query(VerificationRequest).filter(
        VerificationRequest.company_id == current_user.company_id
    )

    # Apply status filter if provided
    if status_filter:
        query = query.filter(VerificationRequest.status == status_filter)

    # Join with candidate to get candidate info
    query = query.join(Candidate)

    # Order by most recent first
    requests = query.order_by(VerificationRequest.created_at.desc()).all()

    # Map to response format
    result = []
    for req in requests:
        result.append(
            VerificationRequestListItem(
                id=req.id,
                candidate_id=req.candidate_id,
                candidate_name=req.candidate.full_name,
                status=req.status,
                created_at=req.created_at,
            )
        )

    return result

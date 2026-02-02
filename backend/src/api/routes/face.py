"""
Face verification API routes.

Phase 3: Face comparison endpoints for candidate selfie and HR reference upload.
"""

import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from ...database import get_db
from ...models import Verification, VerificationStep, StepType, StepStatus, FaceComparison
from ...schemas.verification import (
    FaceSubmission,
    FaceReferenceUpload,
    FaceStepResponse,
    FaceComparisonResponse,
    FaceDecisionSchema,
    ReferenceSourceSchema,
    StepStatusSchema,
)
from ...services.face import get_face_service, FaceDecision, ReferenceSource
from ...utils.face_storage import get_face_storage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/face", tags=["Face Verification"])


def get_verification_by_token(token: str, db: Session) -> Verification:
    """Validate token and return verification."""
    verification = db.query(Verification).filter(
        Verification.token == token,
        Verification.token_expires_at > datetime.utcnow()
    ).first()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found or expired")
    
    return verification


def get_face_step(verification: Verification, db: Session) -> VerificationStep:
    """Get FACE_LIVENESS step for verification."""
    step = db.query(VerificationStep).filter(
        VerificationStep.verification_id == verification.id,
        VerificationStep.step_type == StepType.FACE_LIVENESS
    ).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Face step not found for this verification")
    
    return step


@router.post("/submit", response_model=FaceStepResponse)
async def submit_face(
    submission: FaceSubmission,
    token: str = Query(..., description="Verification token"),
    db: Session = Depends(get_db)
):
    """
    Submit candidate selfie for face verification.
    
    If reference exists, performs comparison.
    If no reference, stores selfie with PENDING_REFERENCE status.
    """
    # 1. Validate token and get verification
    verification = get_verification_by_token(token, db)
    step = get_face_step(verification, db)
    
    if step.status == StepStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Face step already completed")
    
    # 2. Get services
    face_service = get_face_service()
    face_storage = get_face_storage()
    
    # 3. Store selfie
    selfie_key = face_storage.save_selfie(
        candidate_id=verification.candidate_id,
        image_base64=submission.selfie_image_base64
    )
    
    # 4. Check for existing reference
    existing_ref = db.query(FaceComparison).filter(
        FaceComparison.candidate_id == verification.candidate_id,
        FaceComparison.reference_s3_key.isnot(None)
    ).order_by(FaceComparison.created_at.desc()).first()
    
    if existing_ref and existing_ref.reference_s3_key:
        # 5a. Compare with existing reference
        reference_bytes = face_storage.get_image(existing_ref.reference_s3_key)
        if reference_bytes:
            import base64
            reference_b64 = base64.b64encode(reference_bytes).decode()
            
            result = face_service.compare_faces(
                selfie_base64=submission.selfie_image_base64,
                reference_base64=reference_b64,
                selfie_s3_key=selfie_key,
                reference_s3_key=existing_ref.reference_s3_key,
                reference_source=ReferenceSource(existing_ref.reference_source or "other"),
            )
            
            # Determine step status
            if result.decision == FaceDecision.MATCH:
                step_status = StepStatus.COMPLETED
            elif result.decision == FaceDecision.LOW_CONFIDENCE:
                step_status = StepStatus.COMPLETED  # Still complete, but flagged
            else:
                step_status = StepStatus.FAILED
            
            # Create comparison record
            comparison = FaceComparison(
                verification_id=verification.id,
                step_id=step.id,
                candidate_id=verification.candidate_id,
                selfie_s3_key=selfie_key,
                reference_s3_key=existing_ref.reference_s3_key,
                reference_source=existing_ref.reference_source,
                confidence_score=result.confidence_score,
                decision=result.decision.value,
                flags=result.flags,
                raw_response_encrypted=result.raw_response_encrypted,
                triggered_by="candidate",
                compared_at=result.compared_at,
            )
            comparison.add_audit_entry("COMPARED", "candidate")
            db.add(comparison)
            
            # Update step
            step.status = step_status
            step.input_data = {"selfie_s3_key": selfie_key}
            step.completed_at = datetime.utcnow()
            if result.flags:
                step.flags = result.flags
            
            db.commit()
            db.refresh(comparison)
            
            return FaceStepResponse(
                status=StepStatusSchema(step_status.value),
                comparison=FaceComparisonResponse(
                    id=comparison.id,
                    decision=FaceDecisionSchema(result.decision.value),
                    confidence_score=result.confidence_score,
                    reference_source=ReferenceSourceSchema(existing_ref.reference_source) if existing_ref.reference_source else None,
                    selfie_url=face_storage.get_presigned_url(selfie_key),
                    reference_url=face_storage.get_presigned_url(existing_ref.reference_s3_key),
                    flags=result.flags,
                    compared_at=result.compared_at,
                ),
                message=f"Face comparison: {result.decision.value}"
            )
    
    # 5b. No reference - store selfie with pending status
    comparison = FaceComparison(
        verification_id=verification.id,
        step_id=step.id,
        candidate_id=verification.candidate_id,
        selfie_s3_key=selfie_key,
        reference_s3_key=None,
        reference_source=None,
        confidence_score=0.0,
        decision=FaceDecision.PENDING_REFERENCE.value,
        flags=["AWAITING_REFERENCE"],
        triggered_by="candidate",
    )
    comparison.add_audit_entry("SELFIE_UPLOADED", "candidate")
    db.add(comparison)
    
    # Update step input but don't complete yet
    step.input_data = {"selfie_s3_key": selfie_key}
    step.flags = ["AWAITING_REFERENCE"]
    
    db.commit()
    db.refresh(comparison)
    
    return FaceStepResponse(
        status=StepStatusSchema.PENDING,
        comparison=FaceComparisonResponse(
            id=comparison.id,
            decision=FaceDecisionSchema.PENDING_REFERENCE,
            confidence_score=0.0,
            selfie_url=face_storage.get_presigned_url(selfie_key),
            flags=["AWAITING_REFERENCE"],
            message="Selfie uploaded. Awaiting reference image from HR.",
        ),
        message="Selfie uploaded. Awaiting reference image for comparison."
    )


@router.post("/reference/{candidate_id}", response_model=FaceComparisonResponse)
async def upload_reference(
    candidate_id: int,
    upload: FaceReferenceUpload,
    db: Session = Depends(get_db)
):
    """
    HR uploads reference image for candidate.
    
    If selfie already exists, triggers comparison.
    """
    face_service = get_face_service()
    face_storage = get_face_storage()
    
    # Store reference
    reference_key = face_storage.save_reference(
        candidate_id=candidate_id,
        image_base64=upload.reference_image_base64,
        source=upload.source.value,
    )
    
    # Find pending comparison for this candidate
    pending = db.query(FaceComparison).filter(
        FaceComparison.candidate_id == candidate_id,
        FaceComparison.decision == FaceDecision.PENDING_REFERENCE.value
    ).order_by(FaceComparison.created_at.desc()).first()
    
    if pending and pending.selfie_s3_key:
        # Compare with stored selfie
        selfie_bytes = face_storage.get_image(pending.selfie_s3_key)
        if selfie_bytes:
            import base64
            selfie_b64 = base64.b64encode(selfie_bytes).decode()
            
            result = face_service.compare_faces(
                selfie_base64=selfie_b64,
                reference_base64=upload.reference_image_base64,
                selfie_s3_key=pending.selfie_s3_key,
                reference_s3_key=reference_key,
                reference_source=ReferenceSource(upload.source.value),
            )
            
            # Update comparison record
            pending.reference_s3_key = reference_key
            pending.reference_source = upload.source.value
            pending.confidence_score = result.confidence_score
            pending.decision = result.decision.value
            pending.flags = result.flags
            pending.raw_response_encrypted = result.raw_response_encrypted
            pending.compared_at = result.compared_at
            pending.add_audit_entry("HR_REFERENCE_ADDED", "hr")
            pending.add_audit_entry("COMPARED", "hr")
            
            # Update step if exists
            if pending.step_id:
                step = db.query(VerificationStep).get(pending.step_id)
                if step:
                    if result.decision == FaceDecision.MATCH:
                        step.status = StepStatus.COMPLETED
                    elif result.decision == FaceDecision.LOW_CONFIDENCE:
                        step.status = StepStatus.COMPLETED
                    else:
                        step.status = StepStatus.FAILED
                    step.completed_at = datetime.utcnow()
                    step.flags = result.flags
            
            db.commit()
            db.refresh(pending)
            
            return FaceComparisonResponse(
                id=pending.id,
                decision=FaceDecisionSchema(result.decision.value),
                confidence_score=result.confidence_score,
                reference_source=ReferenceSourceSchema(upload.source.value),
                selfie_url=face_storage.get_presigned_url(pending.selfie_s3_key),
                reference_url=face_storage.get_presigned_url(reference_key),
                flags=result.flags,
                compared_at=result.compared_at,
            )
    
    # No pending selfie - just store reference for future use
    comparison = FaceComparison(
        verification_id=pending.verification_id if pending else None,
        step_id=pending.step_id if pending else None,
        candidate_id=candidate_id,
        selfie_s3_key=None,
        reference_s3_key=reference_key,
        reference_source=upload.source.value,
        confidence_score=0.0,
        decision=FaceDecision.PENDING_REFERENCE.value,
        flags=["AWAITING_SELFIE"],
        triggered_by="hr",
    )
    comparison.add_audit_entry("HR_REFERENCE_UPLOADED", "hr")
    db.add(comparison)
    db.commit()
    db.refresh(comparison)
    
    return FaceComparisonResponse(
        id=comparison.id,
        decision=FaceDecisionSchema.PENDING_REFERENCE,
        confidence_score=0.0,
        reference_source=ReferenceSourceSchema(upload.source.value),
        reference_url=face_storage.get_presigned_url(reference_key),
        flags=["AWAITING_SELFIE"],
        message="Reference uploaded. Awaiting candidate selfie."
    )


@router.get("/comparison/{candidate_id}", response_model=FaceComparisonResponse)
async def get_face_comparison(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Get latest face comparison for candidate (HR view)."""
    face_storage = get_face_storage()
    
    comparison = db.query(FaceComparison).filter(
        FaceComparison.candidate_id == candidate_id
    ).order_by(FaceComparison.created_at.desc()).first()
    
    if not comparison:
        raise HTTPException(status_code=404, detail="No face comparison found for candidate")
    
    return FaceComparisonResponse(
        id=comparison.id,
        decision=FaceDecisionSchema(comparison.decision),
        confidence_score=comparison.confidence_score,
        reference_source=ReferenceSourceSchema(comparison.reference_source) if comparison.reference_source else None,
        selfie_url=face_storage.get_presigned_url(comparison.selfie_s3_key) if comparison.selfie_s3_key else None,
        reference_url=face_storage.get_presigned_url(comparison.reference_s3_key) if comparison.reference_s3_key else None,
        flags=comparison.flags or [],
        compared_at=comparison.compared_at,
    )

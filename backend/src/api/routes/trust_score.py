"""
Trust Score API routes.

Phase 5: Calculate, view, and override trust scores.
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from ...database import get_db
from ...models import Verification, Candidate
from ...models.trust_score import TrustScore, TrustScoreOverride
from ...models.face_comparison import FaceComparison
from ...models.document_verification import DocumentVerification
from ...services.trust_score import get_trust_calculator, TrustScoreStatus
from ...services.trust_score.rules import OVERRIDE_RULES, OVERRIDE_CATEGORIES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trust-score", tags=["Trust Score"])


# ============ REQUEST MODELS ============

class OverrideRequest(BaseModel):
    """Request to override a trust score."""
    overridden_status: str = Field(..., description="APPROVED or REJECTED")
    override_reason: str = Field(..., min_length=10, description="Reason for override")
    override_category: str = Field(..., description="Category: FALSE_POSITIVE, EXPLAINABLE, etc.")
    notes: Optional[str] = None


# ============ ENDPOINTS ============

@router.post("/calculate/{verification_id}")
async def calculate_trust_score(
    verification_id: int,
    db: Session = Depends(get_db),
):
    """
    Calculate trust score for a verification.
    
    Aggregates all verification steps and calculates weighted score.
    """
    # Get verification
    verification = db.query(Verification).filter(
        Verification.id == verification_id
    ).first()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    # Get candidate
    candidate = db.query(Candidate).filter(
        Candidate.id == verification.candidate_id
    ).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Gather verification data
    verification_data = _gather_verification_data(db, verification, candidate)
    
    # Calculate score
    calculator = get_trust_calculator()
    result = calculator.calculate(verification_data)
    
    # Check if score already exists
    existing = db.query(TrustScore).filter(
        TrustScore.verification_id == verification_id
    ).first()
    
    if existing:
        # Update existing score
        existing.score = result.score
        existing.status = result.status.value
        existing.completion_rate = result.completion_rate
        existing.breakdown = result.breakdown
        existing.flags = result.flags
        existing.recommendations = result.recommendations
        existing.calculated_at = result.calculated_at
        db.commit()
        db.refresh(existing)
        trust_score = existing
    else:
        # Create new score
        trust_score = TrustScore(
            verification_id=verification_id,
            candidate_id=candidate.id,
            score=result.score,
            status=result.status.value,
            completion_rate=result.completion_rate,
            breakdown=result.breakdown,
            flags=result.flags,
            recommendations=result.recommendations,
            calculated_at=result.calculated_at,
        )
        db.add(trust_score)
        db.commit()
        db.refresh(trust_score)
    
    return {
        "id": trust_score.id,
        "verification_id": verification_id,
        "score": round(result.score, 1),
        "status": result.status.value,
        "completion_rate": round(result.completion_rate * 100, 1),
        "breakdown": {k: round(v, 1) for k, v in result.breakdown.items()},
        "flags": result.flags,
        "recommendations": result.recommendations,
        "calculated_at": result.calculated_at.isoformat(),
    }


@router.get("/{verification_id}")
async def get_trust_score(
    verification_id: int,
    db: Session = Depends(get_db),
):
    """Get trust score for a verification."""
    trust_score = db.query(TrustScore).filter(
        TrustScore.verification_id == verification_id
    ).first()
    
    if not trust_score:
        raise HTTPException(status_code=404, detail="Trust score not found. Calculate first.")
    
    return trust_score.to_hr_view()


@router.get("/candidate/{candidate_id}")
async def get_candidate_trust_scores(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    """Get all trust scores for a candidate."""
    scores = db.query(TrustScore).filter(
        TrustScore.candidate_id == candidate_id
    ).order_by(TrustScore.calculated_at.desc()).all()
    
    return [s.to_hr_view() for s in scores]


@router.post("/override/{trust_score_id}")
async def override_trust_score(
    trust_score_id: int,
    request: OverrideRequest,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user),  # TODO: Add auth
):
    """
    Override a trust score decision.
    
    Requires appropriate permission level based on score.
    """
    # Get trust score
    trust_score = db.query(TrustScore).filter(
        TrustScore.id == trust_score_id
    ).first()
    
    if not trust_score:
        raise HTTPException(status_code=404, detail="Trust score not found")
    
    # Validate override category
    if request.override_category not in OVERRIDE_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: {OVERRIDE_CATEGORIES}"
        )
    
    # Validate override status
    if request.overridden_status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail="overridden_status must be APPROVED or REJECTED"
        )
    
    # Check if override is allowed (simplified - add proper auth later)
    requires_senior = trust_score.score < OVERRIDE_RULES["senior_required_max"]
    
    # Create override record
    override = TrustScoreOverride(
        trust_score_id=trust_score_id,
        original_score=trust_score.score,
        original_status=trust_score.status,
        original_flags=trust_score.flags,
        overridden_status=request.overridden_status,
        override_reason=request.override_reason,
        override_category=request.override_category,
        notes=request.notes,
        requires_senior_approval=requires_senior,
        overridden_by=None,  # TODO: Add current_user.id
    )
    
    db.add(override)
    db.commit()
    db.refresh(override)
    
    # Update trust score
    trust_score.is_overridden = True
    trust_score.override_id = override.id
    db.commit()
    
    return {
        "id": override.id,
        "trust_score_id": trust_score_id,
        "original_score": override.original_score,
        "original_status": override.original_status,
        "overridden_status": override.overridden_status,
        "requires_senior_approval": override.requires_senior_approval,
        "override_category": override.override_category,
        "message": "Override recorded" + (
            ". Awaiting senior approval." if requires_senior else ""
        ),
    }


@router.get("/overrides/{trust_score_id}")
async def get_override_history(
    trust_score_id: int,
    db: Session = Depends(get_db),
):
    """Get override history for a trust score."""
    overrides = db.query(TrustScoreOverride).filter(
        TrustScoreOverride.trust_score_id == trust_score_id
    ).order_by(TrustScoreOverride.created_at.desc()).all()
    
    return [o.to_audit() for o in overrides]


# ============ HELPERS ============

def _gather_verification_data(db: Session, verification: Verification, candidate: Candidate) -> dict:
    """Gather all verification data for score calculation."""
    
    # Get face comparison
    face = db.query(FaceComparison).filter(
        FaceComparison.candidate_id == candidate.id
    ).order_by(FaceComparison.created_at.desc()).first()
    
    # Get documents
    documents = db.query(DocumentVerification).filter(
        DocumentVerification.candidate_id == candidate.id
    ).all()
    
    # Build verification data dict
    # Note: Aadhaar, PAN, UAN data would come from verification_steps
    # For now we're using a simplified structure
    
    return {
        "candidate": {
            "id": candidate.id,
            "experience_years": getattr(candidate, "experience_years", 0),
        },
        "aadhaar": _get_step_data(verification, "aadhaar"),
        "pan": _get_step_data(verification, "pan"),
        "uan": _get_step_data(verification, "uan"),
        "face": {
            "decision": face.decision if face else None,
            "confidence": face.confidence_score if face else None,
            "liveness_passed": True,  # Default for now
        } if face else None,
        "documents": [
            {
                "document_type": doc.document_type,
                "legitimacy_score": doc.legitimacy_score,
                "status": doc.status,
            }
            for doc in documents
        ],
    }


def _get_step_data(verification: Verification, step_type: str) -> Optional[dict]:
    """Get verification step data by type."""
    # This would query verification_steps table
    # For now, returning None as placeholder
    # TODO: Integrate with actual verification step data
    return None

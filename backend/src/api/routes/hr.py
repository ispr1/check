"""
HR Review API Routes.

Phase 6: HR document handling, summary viewing, and decision APIs.
"""

import logging
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from ...database import get_db
from ...models import Candidate, Verification
from ...models.hr_review import HRDocument, HRDecision, HRDecisionStatus
from ...models.trust_score import TrustScore
from ...models.document_verification import DocumentVerification
from ...services.hr import get_hr_summary_service
from ...services.document import get_document_service
from ...utils.face_storage import get_face_storage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hr", tags=["HR Review"])


# ============ REQUEST MODELS ============

class DecisionRequest(BaseModel):
    """Request to record HR decision."""
    decision: str = Field(..., description="APPROVED, REJECTED, or NEED_MORE_INFO")
    reason_codes: List[str] = Field(default_factory=list)
    comments: Optional[str] = None
    override_requested: bool = False


# ============ DOCUMENT UPLOAD ============

@router.post("/documents/upload")
async def upload_hr_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    candidate_id: int = Form(...),
    verification_id: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user),  # TODO: Add auth
):
    """
    Upload a document as HR.
    
    Use cases:
    - Missing education certificate
    - Experience proof
    - Clarification documents
    - Bonafide letters
    
    Document is auto-analyzed via Phase 4 pipeline.
    Does NOT auto-change trust score.
    """
    # Validate document type
    valid_types = ["education", "experience", "clarification", "payslip", "bonafide", "other"]
    if document_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid document_type. Must be one of: {valid_types}"
        )
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith(("application/pdf", "image/")):
        raise HTTPException(status_code=400, detail="Only PDF and image files are supported")
    
    # Validate candidate exists
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Read file
    file_bytes = await file.read()
    
    if len(file_bytes) < 100:
        raise HTTPException(status_code=400, detail="File too small")
    
    if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    # Store file
    storage = get_face_storage()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_key = f"hr_documents/{candidate_id}/{document_type}_{timestamp}.pdf"
    
    # For local mode, save directly
    if storage._storage_type == "local":
        from pathlib import Path
        path = storage._local_path / s3_key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file_bytes)
    
    # Analyze document via Phase 4 pipeline
    doc_service = get_document_service()
    
    try:
        analysis_result = doc_service.analyze(file_bytes, document_type)
        is_analyzed = True
        analysis_status = analysis_result.status.value
        legitimacy_score = analysis_result.legitimacy_score
    except Exception as e:
        logger.error(f"Document analysis failed: {e}")
        is_analyzed = False
        analysis_status = None
        legitimacy_score = None
    
    # Create HR document record
    hr_doc = HRDocument(
        candidate_id=candidate_id,
        verification_id=verification_id,
        document_type=document_type,
        s3_key=s3_key,
        original_filename=file.filename,
        source="hr_upload",
        uploaded_by=None,  # TODO: current_user.id
        notes=notes,
        is_analyzed=is_analyzed,
        analysis_status=analysis_status,
        legitimacy_score=legitimacy_score,
    )
    
    db.add(hr_doc)
    db.commit()
    db.refresh(hr_doc)
    
    logger.info(f"HR document uploaded: candidate={candidate_id}, type={document_type}, id={hr_doc.id}")
    
    return {
        "id": hr_doc.id,
        "document_type": document_type,
        "original_filename": file.filename,
        "source": "hr_upload",
        "is_analyzed": is_analyzed,
        "analysis_status": analysis_status,
        "legitimacy_score": round(legitimacy_score, 1) if legitimacy_score else None,
        "message": "Document uploaded and analyzed" if is_analyzed else "Document uploaded, analysis pending",
    }


@router.get("/documents/{candidate_id}")
async def get_hr_documents(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    """Get all HR-uploaded documents for a candidate."""
    # Validate candidate exists
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    hr_docs = db.query(HRDocument).filter(
        HRDocument.candidate_id == candidate_id
    ).order_by(HRDocument.created_at.desc()).all()
    
    return {
        "candidate_id": candidate_id,
        "total": len(hr_docs),
        "documents": [d.to_hr_view() for d in hr_docs],
    }


# ============ SUMMARY & DETAILS ============

@router.get("/candidates/{candidate_id}/summary")
async def get_candidate_summary(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    """
    Get complete candidate summary for HR review.
    
    Includes:
    - Candidate info
    - Verification status
    - Trust score (read-only)
    - Flags by category
    - Face verification
    - Documents
    - Audit trail
    """
    service = get_hr_summary_service()
    summary = service.get_candidate_summary(db, candidate_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Format explainable score
    trust_score = summary.trust_score
    
    return {
        "candidate": summary.candidate,
        "verification": summary.verification,
        "trust_score": {
            "score": trust_score.score,
            "status": trust_score.status,
            "system_recommendation": trust_score.system_recommendation,
            "deductions": [
                {"category": d.category, "reason": d.reason, "points": d.points}
                for d in trust_score.deductions
            ],
            "flags": trust_score.flags_by_category,
        },
        "face_verification": summary.face_verification,
        "documents": {
            "candidate_uploaded": summary.documents,
            "hr_uploaded": summary.hr_documents,
        },
        "identity_checks": summary.identity_checks,
        "decisions": summary.decisions,
    }


@router.get("/verifications/{verification_id}/details")
async def get_verification_details(
    verification_id: int,
    db: Session = Depends(get_db),
):
    """
    Get detailed verification view.
    
    Same as candidate summary but keyed by verification ID.
    """
    verification = db.query(Verification).filter(
        Verification.id == verification_id
    ).first()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    service = get_hr_summary_service()
    summary = service.get_candidate_summary(db, verification.candidate_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    trust_score = summary.trust_score
    
    return {
        "verification_id": verification_id,
        "candidate": summary.candidate,
        "verification": summary.verification,
        "trust_score": {
            "score": trust_score.score,
            "status": trust_score.status,
            "system_recommendation": trust_score.system_recommendation,
            "deductions": [
                {"category": d.category, "reason": d.reason, "points": d.points}
                for d in trust_score.deductions
            ],
            "flags": trust_score.flags_by_category,
        },
        "face_verification": summary.face_verification,
        "documents": {
            "candidate_uploaded": summary.documents,
            "hr_uploaded": summary.hr_documents,
        },
        "identity_checks": summary.identity_checks,
        "audit_trail": summary.audit_trail,
    }


# ============ DECISIONS ============

@router.post("/decision/{verification_id}")
async def record_hr_decision(
    verification_id: int,
    request: DecisionRequest,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user),  # TODO: Add auth
):
    """
    Record HR hiring decision.
    
    Decisions are IMMUTABLE for audit compliance.
    """
    # Validate decision
    valid_decisions = ["APPROVED", "REJECTED", "NEED_MORE_INFO"]
    if request.decision not in valid_decisions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid decision. Must be one of: {valid_decisions}"
        )
    
    # Get verification
    verification = db.query(Verification).filter(
        Verification.id == verification_id
    ).first()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    # Get current trust score
    trust_score = db.query(TrustScore).filter(
        TrustScore.verification_id == verification_id
    ).first()
    
    # Create decision record (immutable)
    decision = HRDecision(
        verification_id=verification_id,
        candidate_id=verification.candidate_id,
        decision=request.decision,
        decided_by=None,  # TODO: current_user.id
        reason_codes=request.reason_codes,
        comments=request.comments,
        override_requested=request.override_requested,
        trust_score_at_decision=trust_score.score if trust_score else None,
        trust_status_at_decision=trust_score.status if trust_score else None,
    )
    
    db.add(decision)
    db.commit()
    db.refresh(decision)
    
    logger.info(f"HR decision recorded: verification={verification_id}, decision={request.decision}")
    
    return {
        "id": decision.id,
        "verification_id": verification_id,
        "decision": decision.decision,
        "trust_score_at_decision": decision.trust_score_at_decision,
        "trust_status_at_decision": decision.trust_status_at_decision,
        "override_requested": decision.override_requested,
        "decided_at": decision.decided_at.isoformat(),
        "message": f"Decision recorded: {decision.decision}",
    }


@router.get("/audit/{verification_id}")
async def get_audit_trail(
    verification_id: int,
    db: Session = Depends(get_db),
):
    """
    Get complete audit trail for a verification.
    
    Includes all events, decisions, and document uploads.
    """
    verification = db.query(Verification).filter(
        Verification.id == verification_id
    ).first()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    service = get_hr_summary_service()
    summary = service.get_candidate_summary(db, verification.candidate_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return {
        "verification_id": verification_id,
        "candidate_id": verification.candidate_id,
        "audit_trail": summary.audit_trail,
        "decisions": summary.decisions,
    }


# ============ DECISION HISTORY ============

@router.get("/decisions/{candidate_id}")
async def get_decision_history(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    """Get all HR decisions for a candidate."""
    decisions = db.query(HRDecision).filter(
        HRDecision.candidate_id == candidate_id
    ).order_by(HRDecision.created_at.desc()).all()
    
    return {
        "candidate_id": candidate_id,
        "total": len(decisions),
        "decisions": [d.to_audit() for d in decisions],
    }

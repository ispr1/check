"""
Document verification API routes.

Phase 4: Document analysis endpoints for legitimacy scoring.
"""

import logging
import base64
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from ...database import get_db
from ...models import DocumentVerification
from ...services.document import get_document_service, DocumentStatus
from ...utils.face_storage import get_face_storage  # Reuse for document storage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Document Analysis"])


@router.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    candidate_id: int = Form(...),
    verification_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    """
    Upload and analyze a document for legitimacy.
    
    Returns legitimacy score and status.
    """
    # Validate document type
    valid_types = ["education", "experience", "id_card", "other"]
    if document_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid document_type. Must be one of: {valid_types}"
        )
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith(("application/pdf", "image/")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and image files are supported"
        )
    
    # Read file
    file_bytes = await file.read()
    
    if len(file_bytes) < 100:
        raise HTTPException(status_code=400, detail="File too small")
    
    if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    # Store file
    storage = get_face_storage()  # Reusing storage utility
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_key = f"documents/{candidate_id}/{document_type}_{timestamp}.pdf"
    
    # For local mode, save directly
    if storage._storage_type == "local":
        from pathlib import Path
        path = storage._local_path / s3_key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file_bytes)
    
    # Analyze document
    service = get_document_service()
    
    try:
        result = service.analyze(file_bytes, document_type)
    except Exception as e:
        logger.error(f"Document analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")
    
    # Save to database
    doc_verification = DocumentVerification(
        verification_id=verification_id,
        candidate_id=candidate_id,
        document_type=document_type,
        s3_key=s3_key,
        original_filename=file.filename,
        legitimacy_score=result.legitimacy_score,
        status=result.status.value,
        breakdown=result.breakdown,
        flags=result.flags,
        analyzed_at=result.analyzed_at,
    )
    
    db.add(doc_verification)
    db.commit()
    db.refresh(doc_verification)
    
    return {
        "id": doc_verification.id,
        "legitimacy_score": round(result.legitimacy_score, 1),
        "status": result.status.value,
        "review_required": result.status != DocumentStatus.LEGITIMATE,
        "flags": result.flags,
        "breakdown": {k: round(v, 1) for k, v in result.breakdown.items()},
        "message": _get_status_message(result.status),
    }


@router.get("/{candidate_id}")
async def get_candidate_documents(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    """Get all document verifications for a candidate."""
    docs = db.query(DocumentVerification).filter(
        DocumentVerification.candidate_id == candidate_id
    ).order_by(DocumentVerification.created_at.desc()).all()
    
    return [doc.to_hr_view() for doc in docs]


@router.get("/{candidate_id}/{document_type}")
async def get_document_by_type(
    candidate_id: int,
    document_type: str,
    db: Session = Depends(get_db),
):
    """Get latest document verification by type."""
    doc = db.query(DocumentVerification).filter(
        DocumentVerification.candidate_id == candidate_id,
        DocumentVerification.document_type == document_type
    ).order_by(DocumentVerification.created_at.desc()).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return doc.to_hr_view()


def _get_status_message(status: DocumentStatus) -> str:
    """Get human-readable status message."""
    messages = {
        DocumentStatus.LEGITIMATE: "Document appears legitimate",
        DocumentStatus.REVIEW_REQUIRED: "Document requires HR review",
        DocumentStatus.SUSPICIOUS: "Document has anomalies requiring review",
        DocumentStatus.ERROR: "Analysis could not be completed",
        DocumentStatus.PENDING: "Analysis pending",
    }
    return messages.get(status, "Unknown status")

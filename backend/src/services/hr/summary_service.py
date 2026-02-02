"""
HR Summary Aggregation Service.

Provides read-only aggregated views for HR review.
NEVER exposes raw vendor data or encrypted payloads.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy.orm import Session

from ...models import Candidate, Verification, VerificationStep
from ...models.face_comparison import FaceComparison
from ...models.document_verification import DocumentVerification
from ...models.trust_score import TrustScore, TrustScoreOverride
from ...models.hr_review import HRDocument, HRDecision

logger = logging.getLogger(__name__)


@dataclass
class DeductionItem:
    """Single deduction for explainability."""
    category: str  # identity, face, documents, employment
    reason: str
    points: float


@dataclass
class ExplainableScore:
    """Explainable trust score for HR."""
    score: float
    status: str
    deductions: List[DeductionItem] = field(default_factory=list)
    flags_by_category: Dict[str, List[str]] = field(default_factory=dict)
    system_recommendation: str = "REVIEW_REQUIRED"


@dataclass
class HRSummary:
    """Complete HR review summary."""
    candidate: Dict[str, Any]
    verification: Dict[str, Any]
    trust_score: ExplainableScore
    face_verification: Optional[Dict[str, Any]]
    documents: List[Dict[str, Any]]
    hr_documents: List[Dict[str, Any]]
    identity_checks: Dict[str, Any]
    decisions: List[Dict[str, Any]]
    audit_trail: List[Dict[str, Any]]


class HRSummaryService:
    """
    Aggregates verification data for HR review.
    
    Rules:
    - Read-only access to scores
    - NEVER expose raw vendor JSON
    - NEVER expose encrypted payloads
    - Explainability only
    """
    
    def get_candidate_summary(self, db: Session, candidate_id: int) -> Optional[HRSummary]:
        """
        Get complete summary for a candidate.
        
        Aggregates all verification data for HR review.
        """
        # Get candidate
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return None
        
        # Get latest verification
        verification = db.query(Verification).filter(
            Verification.candidate_id == candidate_id
        ).order_by(Verification.created_at.desc()).first()
        
        # Get trust score
        trust_score = None
        if verification:
            trust_score = db.query(TrustScore).filter(
                TrustScore.verification_id == verification.id
            ).first()
        
        # Get face comparison
        face = db.query(FaceComparison).filter(
            FaceComparison.candidate_id == candidate_id
        ).order_by(FaceComparison.created_at.desc()).first()
        
        # Get documents (candidate-uploaded)
        documents = db.query(DocumentVerification).filter(
            DocumentVerification.candidate_id == candidate_id
        ).all()
        
        # Get HR documents
        hr_documents = db.query(HRDocument).filter(
            HRDocument.candidate_id == candidate_id
        ).all()
        
        # Get decisions
        decisions = db.query(HRDecision).filter(
            HRDecision.candidate_id == candidate_id
        ).order_by(HRDecision.created_at.desc()).all()
        
        return HRSummary(
            candidate=self._format_candidate(candidate),
            verification=self._format_verification(verification) if verification else {},
            trust_score=self._format_explainable_score(trust_score),
            face_verification=self._format_face(face) if face else None,
            documents=[self._format_document(d) for d in documents],
            hr_documents=[d.to_hr_view() for d in hr_documents],
            identity_checks=self._get_identity_checks(db, verification),
            decisions=[d.to_audit() for d in decisions],
            audit_trail=self._get_audit_trail(db, candidate_id, verification),
        )
    
    def get_verification_details(self, db: Session, verification_id: int) -> Optional[Dict]:
        """
        Get detailed verification view for HR.
        """
        verification = db.query(Verification).filter(
            Verification.id == verification_id
        ).first()
        
        if not verification:
            return None
        
        return self.get_candidate_summary(db, verification.candidate_id)
    
    # ============ FORMATTERS (HR-SAFE) ============
    
    def _format_candidate(self, candidate: Candidate) -> Dict[str, Any]:
        """Format candidate info (no sensitive data)."""
        return {
            "id": candidate.id,
            "name": getattr(candidate, "name", None) or getattr(candidate, "full_name", "Unknown"),
            "email": getattr(candidate, "email", None),
            "phone": getattr(candidate, "phone", None),
            "experience_years": getattr(candidate, "experience_years", 0),
            "created_at": candidate.created_at.isoformat() if hasattr(candidate, "created_at") and candidate.created_at else None,
        }
    
    def _format_verification(self, verification: Verification) -> Dict[str, Any]:
        """Format verification status."""
        return {
            "id": verification.id,
            "status": verification.status.value if hasattr(verification.status, "value") else str(verification.status),
            "started_at": verification.created_at.isoformat() if verification.created_at else None,
            "completed_at": getattr(verification, "completed_at", None),
        }
    
    def _format_explainable_score(self, trust_score: Optional[TrustScore]) -> ExplainableScore:
        """
        Format trust score with full explainability.
        
        This is the MANDATORY explainability contract.
        """
        if not trust_score:
            return ExplainableScore(
                score=0,
                status="NOT_CALCULATED",
                deductions=[],
                flags_by_category={},
                system_recommendation="PENDING",
            )
        
        # Parse flags into categories
        flags = trust_score.flags or []
        breakdown = trust_score.breakdown or {}
        
        flags_by_category = {
            "identity": [],
            "face": [],
            "documents": [],
            "employment": [],
        }
        
        deductions = []
        
        # Categorize flags and calculate deductions
        for flag in flags:
            if any(x in flag for x in ["AADHAAR", "PAN"]):
                flags_by_category["identity"].append(flag)
                deductions.append(DeductionItem(
                    category="identity",
                    reason=flag.replace("_", " ").title(),
                    points=self._estimate_deduction(flag, breakdown)
                ))
            elif any(x in flag for x in ["FACE", "LIVENESS"]):
                flags_by_category["face"].append(flag)
                deductions.append(DeductionItem(
                    category="face",
                    reason=flag.replace("_", " ").title(),
                    points=self._estimate_deduction(flag, breakdown)
                ))
            elif any(x in flag for x in ["DOC", "DOCUMENT", "EDUCATION", "EXPERIENCE"]):
                flags_by_category["documents"].append(flag)
                deductions.append(DeductionItem(
                    category="documents",
                    reason=flag.replace("_", " ").title(),
                    points=self._estimate_deduction(flag, breakdown)
                ))
            elif any(x in flag for x in ["UAN", "EMPLOYMENT", "GAP"]):
                flags_by_category["employment"].append(flag)
                deductions.append(DeductionItem(
                    category="employment",
                    reason=flag.replace("_", " ").title(),
                    points=self._estimate_deduction(flag, breakdown)
                ))
        
        return ExplainableScore(
            score=round(trust_score.score, 1),
            status=trust_score.status,
            deductions=deductions,
            flags_by_category=flags_by_category,
            system_recommendation=trust_score.status,
        )
    
    def _format_face(self, face: FaceComparison) -> Dict[str, Any]:
        """Format face verification (HR-safe view)."""
        return {
            "decision": face.decision,
            "confidence": round(face.confidence_score, 1) if face.confidence_score else None,
            "reference_source": face.reference_source,
            "compared_at": face.created_at.isoformat() if face.created_at else None,
            # NOTE: Never expose raw Rekognition response
        }
    
    def _format_document(self, doc: DocumentVerification) -> Dict[str, Any]:
        """Format document verification (HR-safe view)."""
        return {
            "id": doc.id,
            "document_type": doc.document_type,
            "source": "candidate_upload",
            "legitimacy_score": round(doc.legitimacy_score, 1) if doc.legitimacy_score else None,
            "status": doc.status,
            "flags": doc.flags or [],
            "breakdown": {k: round(v, 1) for k, v in (doc.breakdown or {}).items()},
            "analyzed_at": doc.analyzed_at.isoformat() if doc.analyzed_at else None,
        }
    
    def _get_identity_checks(self, db: Session, verification: Optional[Verification]) -> Dict[str, Any]:
        """
        Get identity verification status.
        
        NOTE: Never expose raw Surepass responses.
        """
        if not verification:
            return {"aadhaar": None, "pan": None, "uan": None}
        
        # Get verification steps
        steps = db.query(VerificationStep).filter(
            VerificationStep.verification_id == verification.id
        ).all()
        
        result = {"aadhaar": None, "pan": None, "uan": None}
        
        for step in steps:
            step_type = step.step_type.value if hasattr(step.step_type, "value") else str(step.step_type)
            
            if "aadhaar" in step_type.lower():
                result["aadhaar"] = {
                    "status": step.status.value if hasattr(step.status, "value") else str(step.status),
                    "verified_at": step.completed_at.isoformat() if step.completed_at else None,
                    # NOTE: Never expose raw response
                }
            elif "pan" in step_type.lower():
                result["pan"] = {
                    "status": step.status.value if hasattr(step.status, "value") else str(step.status),
                    "verified_at": step.completed_at.isoformat() if step.completed_at else None,
                }
            elif "uan" in step_type.lower():
                result["uan"] = {
                    "status": step.status.value if hasattr(step.status, "value") else str(step.status),
                    "verified_at": step.completed_at.isoformat() if step.completed_at else None,
                }
        
        return result
    
    def _get_audit_trail(self, db: Session, candidate_id: int, verification: Optional[Verification]) -> List[Dict]:
        """Get audit trail for candidate."""
        trail = []
        
        # Add verification events
        if verification:
            trail.append({
                "event": "VERIFICATION_STARTED",
                "timestamp": verification.created_at.isoformat() if verification.created_at else None,
                "details": {"verification_id": verification.id},
            })
        
        # Add document uploads
        docs = db.query(DocumentVerification).filter(
            DocumentVerification.candidate_id == candidate_id
        ).all()
        
        for doc in docs:
            trail.append({
                "event": "DOCUMENT_UPLOADED",
                "timestamp": doc.created_at.isoformat() if doc.created_at else None,
                "details": {
                    "type": doc.document_type,
                    "source": "candidate",
                },
            })
        
        # Add HR document uploads
        hr_docs = db.query(HRDocument).filter(
            HRDocument.candidate_id == candidate_id
        ).all()
        
        for doc in hr_docs:
            trail.append({
                "event": "HR_DOCUMENT_UPLOADED",
                "timestamp": doc.created_at.isoformat() if doc.created_at else None,
                "details": {
                    "type": doc.document_type,
                    "uploaded_by": doc.uploaded_by,
                },
            })
        
        # Add decisions
        decisions = db.query(HRDecision).filter(
            HRDecision.candidate_id == candidate_id
        ).all()
        
        for d in decisions:
            trail.append({
                "event": f"HR_DECISION_{d.decision}",
                "timestamp": d.decided_at.isoformat() if d.decided_at else None,
                "details": {
                    "decision": d.decision,
                    "decided_by": d.decided_by,
                },
            })
        
        # Sort by timestamp
        trail.sort(key=lambda x: x["timestamp"] or "", reverse=True)
        
        return trail
    
    def _estimate_deduction(self, flag: str, breakdown: Dict) -> float:
        """Estimate deduction points from flag (approximate)."""
        # This is a simplified estimation
        if "MISMATCH" in flag:
            return 10.0
        elif "LOW" in flag:
            return 5.0
        elif "MISSING" in flag:
            return 15.0
        elif "SUSPICIOUS" in flag:
            return 15.0
        else:
            return 5.0


# Singleton instance
_service_instance: Optional[HRSummaryService] = None


def get_hr_summary_service() -> HRSummaryService:
    """Get or create singleton HRSummaryService."""
    global _service_instance
    if _service_instance is None:
        _service_instance = HRSummaryService()
    return _service_instance

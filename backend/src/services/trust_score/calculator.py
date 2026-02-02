"""
Trust Score Calculator.

Calculates explainable trust score with deductions.
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher

from .rules import (
    TrustScoreStatus,
    WEIGHTS,
    THRESHOLDS,
    MIN_COMPLETION_RATE,
    AADHAAR_DEDUCTIONS,
    PAN_DEDUCTIONS,
    UAN_DEDUCTIONS,
    UAN_EXPERIENCE_THRESHOLDS,
    FACE_DEDUCTIONS,
    DOCUMENT_DEDUCTIONS,
    DOCUMENT_LEGITIMACY_THRESHOLDS,
    CROSS_MATCH_DEDUCTIONS,
    FUZZY_MATCH_THRESHOLDS,
)

logger = logging.getLogger(__name__)


@dataclass
class TrustScoreResult:
    """Complete trust score result."""
    score: float
    status: TrustScoreStatus
    flags: List[str] = field(default_factory=list)
    breakdown: Dict[str, float] = field(default_factory=dict)
    completion_rate: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    calculated_at: Optional[datetime] = None
    
    def to_hr_view(self) -> Dict[str, Any]:
        """Return HR-safe summary."""
        return {
            "score": round(self.score, 1),
            "status": self.status.value,
            "flags": self.flags,
            "breakdown": {k: round(v, 1) for k, v in self.breakdown.items()},
            "completion_rate": round(self.completion_rate * 100, 1),
            "recommendations": self.recommendations,
            "calculated_at": self.calculated_at.isoformat() if self.calculated_at else None,
        }
    
    def to_audit(self) -> Dict[str, Any]:
        """Full audit record."""
        return {
            "score": self.score,
            "status": self.status.value,
            "flags": self.flags,
            "breakdown": self.breakdown,
            "completion_rate": self.completion_rate,
            "recommendations": self.recommendations,
            "calculated_at": self.calculated_at.isoformat() if self.calculated_at else None,
        }


class TrustScoreCalculator:
    """
    Professional trust score calculation.
    
    Starts at 100, deducts for issues.
    Explainable scoring with component breakdown.
    """
    
    def calculate(self, verification_data: Dict[str, Any]) -> TrustScoreResult:
        """
        Calculate trust score from verification data.
        
        Args:
            verification_data: Dict with aadhaar, pan, uan, face, documents, candidate
            
        Returns:
            TrustScoreResult with score, status, flags, breakdown
        """
        score = 100.0
        flags = []
        breakdown = {}
        recommendations = []
        
        # Get candidate info
        candidate = verification_data.get("candidate", {})
        experience_years = candidate.get("experience_years", 0)
        
        # Check completion first
        completion_rate = self._check_completion(verification_data)
        if completion_rate < MIN_COMPLETION_RATE:
            return TrustScoreResult(
                score=0,
                status=TrustScoreStatus.INCOMPLETE,
                flags=["INCOMPLETE_VERIFICATION"],
                breakdown={},
                completion_rate=completion_rate,
                recommendations=["Complete all mandatory verification steps"],
                calculated_at=datetime.utcnow(),
            )
        
        # 1. Aadhaar Verification (20%)
        aadhaar_score, aadhaar_flags = self._evaluate_aadhaar(
            verification_data.get("aadhaar")
        )
        component_deduction = (100 - aadhaar_score) * (WEIGHTS["aadhaar"] / 100)
        score -= component_deduction
        flags.extend(aadhaar_flags)
        breakdown["aadhaar"] = aadhaar_score
        
        # 2. PAN Verification (10%)
        pan_score, pan_flags = self._evaluate_pan(
            verification_data.get("pan")
        )
        component_deduction = (100 - pan_score) * (WEIGHTS["pan"] / 100)
        score -= component_deduction
        flags.extend(pan_flags)
        breakdown["pan"] = pan_score
        
        # 3. UAN Verification (10% - conditional)
        uan_score, uan_flags = self._evaluate_uan(
            verification_data.get("uan"),
            experience_years
        )
        component_deduction = (100 - uan_score) * (WEIGHTS["uan"] / 100)
        score -= component_deduction
        flags.extend(uan_flags)
        breakdown["uan"] = uan_score
        
        # 4. Face Verification (25%)
        face_score, face_flags = self._evaluate_face(
            verification_data.get("face")
        )
        component_deduction = (100 - face_score) * (WEIGHTS["face"] / 100)
        score -= component_deduction
        flags.extend(face_flags)
        breakdown["face"] = face_score
        
        # 5. Document Legitimacy (25%)
        doc_score, doc_flags = self._evaluate_documents(
            verification_data.get("documents", []),
            experience_years
        )
        component_deduction = (100 - doc_score) * (WEIGHTS["documents"] / 100)
        score -= component_deduction
        flags.extend(doc_flags)
        breakdown["documents"] = doc_score
        
        # 6. Cross-Match Consistency (10%)
        cross_score, cross_flags = self._evaluate_cross_match(verification_data)
        component_deduction = (100 - cross_score) * (WEIGHTS["cross_match"] / 100)
        score -= component_deduction
        flags.extend(cross_flags)
        breakdown["cross_match"] = cross_score
        
        # Ensure score doesn't go below 0
        final_score = max(0, round(score, 2))
        
        # Determine status
        status = self._determine_status(final_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(flags, breakdown)
        
        return TrustScoreResult(
            score=final_score,
            status=status,
            flags=list(set(flags)),  # Dedupe
            breakdown=breakdown,
            completion_rate=completion_rate,
            recommendations=recommendations,
            calculated_at=datetime.utcnow(),
        )
    
    # ============ COMPONENT EVALUATORS ============
    
    def _evaluate_aadhaar(self, aadhaar_data: Optional[Dict]) -> Tuple[float, List[str]]:
        """Evaluate Aadhaar verification (20% weight)."""
        score = 100.0
        flags = []
        
        if not aadhaar_data:
            return 0, ["AADHAAR_NOT_VERIFIED"]
        
        status = aadhaar_data.get("status", "").upper()
        
        if status == "FAILED":
            return 0, ["AADHAAR_VERIFICATION_FAILED"]
        
        # Check match quality
        match_score = aadhaar_data.get("match_score", 100)
        if match_score < 80:
            score -= AADHAAR_DEDUCTIONS["low_match"]
            flags.append(f"AADHAAR_LOW_MATCH_{match_score}%")
        
        # Check field comparisons
        comparisons = aadhaar_data.get("comparisons", {})
        
        if not comparisons.get("name", {}).get("match", True):
            score -= AADHAAR_DEDUCTIONS["name_mismatch"]
            flags.append("AADHAAR_NAME_MISMATCH")
        
        if not comparisons.get("dob", {}).get("match", True):
            score -= AADHAAR_DEDUCTIONS["dob_mismatch"]
            flags.append("AADHAAR_DOB_MISMATCH")
        
        if not comparisons.get("gender", {}).get("match", True):
            score -= AADHAAR_DEDUCTIONS["gender_mismatch"]
            flags.append("AADHAAR_GENDER_MISMATCH")
        
        return max(0, score), flags
    
    def _evaluate_pan(self, pan_data: Optional[Dict]) -> Tuple[float, List[str]]:
        """Evaluate PAN verification (10% weight)."""
        score = 100.0
        flags = []
        
        if not pan_data:
            return 0, ["PAN_NOT_VERIFIED"]
        
        if not pan_data.get("valid", True):
            return 0, ["PAN_INVALID"]
        
        if pan_data.get("name_match") == False:
            score -= PAN_DEDUCTIONS["name_mismatch"]
            flags.append("PAN_NAME_MISMATCH")
        
        if pan_data.get("dob_match") == False:
            score -= PAN_DEDUCTIONS["dob_mismatch"]
            flags.append("PAN_DOB_MISMATCH")
        
        if pan_data.get("aadhaar_linked") == False:
            score -= PAN_DEDUCTIONS["aadhaar_not_linked"]
            flags.append("PAN_AADHAAR_NOT_LINKED")
        
        return max(0, score), flags
    
    def _evaluate_uan(self, uan_data: Optional[Dict], experience_years: int) -> Tuple[float, List[str]]:
        """Evaluate UAN verification (10% weight - conditional)."""
        score = 100.0
        flags = []
        
        # Fresher - UAN not expected
        if experience_years < UAN_EXPERIENCE_THRESHOLDS["junior"]:
            return 100, []  # No penalty
        
        # Experienced - check if UAN provided
        if not uan_data:
            if experience_years < UAN_EXPERIENCE_THRESHOLDS["senior"]:
                # Junior (1-3 years) - soft penalty
                score -= UAN_DEDUCTIONS["not_provided_junior"]
                flags.append("UAN_NOT_PROVIDED_JUNIOR")
            else:
                # Senior (3+ years) - hard penalty
                score = 0
                flags.append("UAN_NOT_PROVIDED_SENIOR")
            return max(0, score), flags
        
        # UAN provided - validate
        if not uan_data.get("valid", True):
            return 0, ["UAN_INVALID"]
        
        # Check experience mismatch
        claimed_months = experience_years * 12
        verified_months = uan_data.get("total_experience_months", claimed_months)
        
        if verified_months < claimed_months * 0.8:  # 20% tolerance
            score -= UAN_DEDUCTIONS["experience_mismatch"]
            flags.append(f"UAN_EXPERIENCE_MISMATCH_{verified_months}mo_vs_{claimed_months}mo")
        
        # Check employment gaps
        gaps = uan_data.get("employment_gaps", 0)
        if gaps > 0:
            deduction = min(gaps * UAN_DEDUCTIONS["employment_gap"], 20)
            score -= deduction
            flags.append(f"UAN_EMPLOYMENT_GAPS_{gaps}")
        
        return max(0, score), flags
    
    def _evaluate_face(self, face_data: Optional[Dict]) -> Tuple[float, List[str]]:
        """Evaluate face verification (25% weight)."""
        score = 100.0
        flags = []
        
        if not face_data:
            return 0, ["FACE_NOT_VERIFIED"]
        
        decision = face_data.get("decision", "").upper()
        confidence = face_data.get("confidence", 100)
        
        if decision == "MISMATCH":
            return 0, ["FACE_MISMATCH"]
        
        if decision == "LOW_CONFIDENCE":
            score -= FACE_DEDUCTIONS["low_confidence"]
            flags.append(f"FACE_LOW_CONFIDENCE_{confidence}%")
        elif confidence < 85:
            score -= FACE_DEDUCTIONS["moderate_confidence"]
            flags.append(f"FACE_MODERATE_CONFIDENCE_{confidence}%")
        
        # Check liveness
        if face_data.get("liveness_passed") == False:
            score -= FACE_DEDUCTIONS["liveness_failed"]
            flags.append("LIVENESS_FAILED")
        
        return max(0, score), flags
    
    def _evaluate_documents(self, documents: List[Dict], experience_years: int) -> Tuple[float, List[str]]:
        """Evaluate document legitimacy (25% weight)."""
        score = 100.0
        flags = []
        
        if not documents:
            return 0, ["NO_DOCUMENTS_UPLOADED"]
        
        # Check minimum requirements
        edu_docs = [d for d in documents if d.get("document_type") == "education"]
        exp_docs = [d for d in documents if d.get("document_type") in ["experience", "payslip"]]
        
        if not edu_docs:
            score -= DOCUMENT_DEDUCTIONS["missing_education"]
            flags.append("MISSING_EDUCATION_DOCUMENTS")
        
        if experience_years > 0 and not exp_docs:
            score -= DOCUMENT_DEDUCTIONS["missing_experience"]
            flags.append("MISSING_EXPERIENCE_DOCUMENTS")
        
        # Calculate average legitimacy
        doc_scores = [d.get("legitimacy_score", 100) for d in documents]
        avg_legitimacy = sum(doc_scores) / len(doc_scores) if doc_scores else 0
        
        # Deduct based on average
        if avg_legitimacy < DOCUMENT_LEGITIMACY_THRESHOLDS["moderate"]:
            score -= DOCUMENT_DEDUCTIONS["low_legitimacy"]
            flags.append(f"DOCUMENTS_LOW_LEGITIMACY_{avg_legitimacy:.0f}%")
        elif avg_legitimacy < DOCUMENT_LEGITIMACY_THRESHOLDS["acceptable"]:
            score -= DOCUMENT_DEDUCTIONS["moderate_legitimacy"]
            flags.append(f"DOCUMENTS_MODERATE_LEGITIMACY_{avg_legitimacy:.0f}%")
        elif avg_legitimacy < DOCUMENT_LEGITIMACY_THRESHOLDS["excellent"]:
            score -= DOCUMENT_DEDUCTIONS["acceptable_legitimacy"]
            flags.append(f"DOCUMENTS_ACCEPTABLE_LEGITIMACY_{avg_legitimacy:.0f}%")
        
        # Check individual suspicious documents
        for doc in documents:
            status = doc.get("status", "").upper()
            if status == "SUSPICIOUS":
                score -= DOCUMENT_DEDUCTIONS["suspicious_document"]
                flags.append(f"SUSPICIOUS_DOC_{doc.get('document_type', 'unknown')}")
            elif status == "REVIEW_REQUIRED":
                score -= DOCUMENT_DEDUCTIONS["review_required_document"]
                flags.append(f"REVIEW_DOC_{doc.get('document_type', 'unknown')}")
        
        return max(0, score), flags
    
    def _evaluate_cross_match(self, verification_data: Dict) -> Tuple[float, List[str]]:
        """Evaluate cross-source consistency (10% weight)."""
        score = 100.0
        flags = []
        
        aadhaar = verification_data.get("aadhaar", {})
        pan = verification_data.get("pan", {})
        uan = verification_data.get("uan", {})
        
        # Aadhaar ↔ PAN (strict - 90% similarity required)
        if aadhaar and pan:
            aadhaar_name = aadhaar.get("data", {}).get("full_name", "")
            pan_name = pan.get("data", {}).get("full_name", "")
            
            if aadhaar_name and pan_name:
                similarity = self._fuzzy_match(aadhaar_name, pan_name)
                if similarity < FUZZY_MATCH_THRESHOLDS["aadhaar_pan"]:
                    score -= CROSS_MATCH_DEDUCTIONS["aadhaar_pan_name"]
                    flags.append(f"AADHAAR_PAN_NAME_DIFF_{similarity:.0f}%")
            
            # DOB must match exactly
            aadhaar_dob = aadhaar.get("data", {}).get("dob")
            pan_dob = pan.get("data", {}).get("dob")
            
            if aadhaar_dob and pan_dob and aadhaar_dob != pan_dob:
                score -= CROSS_MATCH_DEDUCTIONS["aadhaar_pan_dob"]
                flags.append("AADHAAR_PAN_DOB_MISMATCH")
        
        # Aadhaar ↔ UAN (moderate - 80% similarity)
        if aadhaar and uan:
            aadhaar_name = aadhaar.get("data", {}).get("full_name", "")
            uan_name = uan.get("data", {}).get("name", "")
            
            if aadhaar_name and uan_name:
                similarity = self._fuzzy_match(aadhaar_name, uan_name)
                if similarity < FUZZY_MATCH_THRESHOLDS["aadhaar_uan"]:
                    score -= CROSS_MATCH_DEDUCTIONS["aadhaar_uan_name"]
                    flags.append(f"AADHAAR_UAN_NAME_DIFF_{similarity:.0f}%")
        
        return max(0, score), flags
    
    # ============ HELPERS ============
    
    def _fuzzy_match(self, str1: str, str2: str) -> float:
        """Calculate fuzzy string match percentage (0-100)."""
        s1 = " ".join(str1.upper().strip().split())
        s2 = " ".join(str2.upper().strip().split())
        return SequenceMatcher(None, s1, s2).ratio() * 100
    
    def _check_completion(self, verification_data: Dict) -> float:
        """Check verification completion rate."""
        required_steps = {
            "personal_data": verification_data.get("candidate") is not None,
            "aadhaar": verification_data.get("aadhaar") is not None,
            "pan": verification_data.get("pan") is not None,
            "face": verification_data.get("face") is not None,
            "documents": len(verification_data.get("documents", [])) > 0,
        }
        
        completed = sum(required_steps.values())
        total = len(required_steps)
        
        return completed / total if total > 0 else 0
    
    def _determine_status(self, score: float) -> TrustScoreStatus:
        """Determine status based on score thresholds."""
        if score >= THRESHOLDS["verified"]:
            return TrustScoreStatus.VERIFIED
        elif score >= THRESHOLDS["review_required"]:
            return TrustScoreStatus.REVIEW_REQUIRED
        elif score >= THRESHOLDS["high_risk"]:
            return TrustScoreStatus.HIGH_RISK
        else:
            return TrustScoreStatus.FLAGGED
    
    def _generate_recommendations(self, flags: List[str], breakdown: Dict) -> List[str]:
        """Generate actionable recommendations for HR."""
        recommendations = []
        
        if any("AADHAAR" in f for f in flags):
            recommendations.append("Review Aadhaar verification details")
        
        if any("FACE" in f for f in flags):
            recommendations.append("Conduct manual face verification with candidate")
        
        if any("DOC" in f or "DOCUMENT" in f for f in flags):
            recommendations.append("Request original documents for verification")
        
        if any("MISMATCH" in f for f in flags):
            recommendations.append("Verify name/DOB discrepancies with candidate")
        
        if any("UAN" in f for f in flags):
            recommendations.append("Request additional employment proof")
        
        if any("PAN" in f for f in flags):
            recommendations.append("Verify PAN details with candidate")
        
        return recommendations if recommendations else ["No specific recommendations"]


# Singleton instance
_calculator_instance: Optional[TrustScoreCalculator] = None


def get_trust_calculator() -> TrustScoreCalculator:
    """Get or create singleton TrustScoreCalculator."""
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = TrustScoreCalculator()
    return _calculator_instance

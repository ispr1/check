"""
Sample Test Data Generator for CHECK-360.

Creates test candidates, verifications, and documents for E2E testing.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import (
    Candidate, 
    Verification, 
    VerificationStatus,
    VerificationStep,
    StepType,
    StepStatus,
)
from src.models.face_comparison import FaceComparison
from src.models.document_verification import DocumentVerification
from src.models.trust_score import TrustScore


def create_sample_data():
    """Create sample test data."""
    db = SessionLocal()
    
    try:
        print("=== Creating Sample Test Data ===\n")
        
        # 1. Create test candidate
        existing = db.query(Candidate).filter(Candidate.email == "test.candidate@example.com").first()
        
        if existing:
            candidate = existing
            print(f"✓ Using existing candidate: ID {candidate.id}")
        else:
            from datetime import date
            candidate = Candidate(
                company_id=1,  # Assumes company ID 1 exists
                email="test.candidate@example.com",
                full_name="Rajesh Kumar",
                dob=date(1995, 5, 15),
            )
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            print(f"✓ Created candidate: ID {candidate.id} - {candidate.full_name}")
        
        # 2. Create verification
        verification = db.query(Verification).filter(
            Verification.candidate_id == candidate.id
        ).first()
        
        if not verification:
            verification = Verification(
                candidate_id=candidate.id,
                company_id=candidate.company_id,
                status=VerificationStatus.IN_PROGRESS,
            )
            db.add(verification)
            db.commit()
            db.refresh(verification)
            print(f"✓ Created verification: ID {verification.id}")
        else:
            print(f"✓ Using existing verification: ID {verification.id}")
        
        # 3. Create face comparison (mock data)
        face = db.query(FaceComparison).filter(
            FaceComparison.candidate_id == candidate.id
        ).first()
        
        if not face:
            face = FaceComparison(
                verification_id=verification.id,
                candidate_id=candidate.id,
                decision="MATCH",
                confidence_score=91.5,
                reference_source="aadhaar",
                selfie_s3_key="faces/test_selfie.jpg",
                reference_s3_key="faces/test_reference.jpg",
            )
            db.add(face)
            db.commit()
            db.refresh(face)
            print(f"✓ Created face comparison: ID {face.id} - MATCH 91.5%")
        else:
            print(f"✓ Using existing face comparison: ID {face.id}")
        
        # 4. Create document verifications
        doc_types = [
            ("education", 87.5, "LEGITIMATE"),
            ("experience", 72.0, "REVIEW_REQUIRED"),
        ]
        
        for doc_type, score, status in doc_types:
            existing_doc = db.query(DocumentVerification).filter(
                DocumentVerification.candidate_id == candidate.id,
                DocumentVerification.document_type == doc_type,
            ).first()
            
            if not existing_doc:
                doc = DocumentVerification(
                    candidate_id=candidate.id,
                    verification_id=verification.id,
                    document_type=doc_type,
                    s3_key=f"documents/{candidate.id}/{doc_type}.pdf",
                    original_filename=f"{doc_type}_certificate.pdf",
                    legitimacy_score=score,
                    status=status,
                    flags=[f"{doc_type.upper()}_SAMPLE_FLAG"] if status != "LEGITIMATE" else [],
                    breakdown={
                        "metadata": 90.0,
                        "fonts": 85.0,
                        "forensics": 80.0,
                        "text": score,
                    },
                    analyzed_at=datetime.utcnow(),
                )
                db.add(doc)
                db.commit()
                db.refresh(doc)
                print(f"✓ Created document: {doc_type} - Score {score} ({status})")
            else:
                print(f"✓ Using existing document: {doc_type}")
        
        # 5. Calculate trust score
        from src.services.trust_score import get_trust_calculator
        
        calculator = get_trust_calculator()
        
        # Get documents
        documents = db.query(DocumentVerification).filter(
            DocumentVerification.candidate_id == candidate.id
        ).all()
        
        verification_data = {
            "candidate": {
                "id": candidate.id,
                "experience_years": 3,
            },
            "aadhaar": {
                "status": "SUCCESS",
                "match_score": 95,
                "comparisons": {
                    "name": {"match": True},
                    "dob": {"match": True},
                    "gender": {"match": True},
                },
                "data": {"full_name": "Rajesh Kumar", "dob": "1995-05-15"},
            },
            "pan": {
                "valid": True,
                "name_match": True,
                "dob_match": True,
                "aadhaar_linked": True,
                "data": {"full_name": "Rajesh Kumar", "dob": "1995-05-15"},
            },
            "uan": {
                "valid": True,
                "total_experience_months": 36,
                "employment_gaps": 0,
                "data": {"name": "Rajesh Kumar"},
            },
            "face": {
                "decision": "MATCH",
                "confidence": 91.5,
                "liveness_passed": True,
            },
            "documents": [
                {
                    "document_type": d.document_type,
                    "legitimacy_score": d.legitimacy_score,
                    "status": d.status,
                }
                for d in documents
            ],
        }
        
        result = calculator.calculate(verification_data)
        
        # Save trust score
        existing_score = db.query(TrustScore).filter(
            TrustScore.verification_id == verification.id
        ).first()
        
        if existing_score:
            existing_score.score = result.score
            existing_score.status = result.status.value
            existing_score.breakdown = result.breakdown
            existing_score.flags = result.flags
            existing_score.recommendations = result.recommendations
            existing_score.completion_rate = result.completion_rate
            db.commit()
            print(f"\n✓ Updated trust score: {result.score:.1f} ({result.status.value})")
        else:
            trust_score = TrustScore(
                verification_id=verification.id,
                candidate_id=candidate.id,
                score=result.score,
                status=result.status.value,
                breakdown=result.breakdown,
                flags=result.flags,
                recommendations=result.recommendations,
                completion_rate=result.completion_rate,
            )
            db.add(trust_score)
            db.commit()
            print(f"\n✓ Created trust score: {result.score:.1f} ({result.status.value})")
        
        print(f"\n=== Summary ===")
        print(f"Candidate ID: {candidate.id}")
        print(f"Verification ID: {verification.id}")
        print(f"Trust Score: {result.score:.1f}")
        print(f"Status: {result.status.value}")
        print(f"Flags: {result.flags}")
        print(f"\nTest with: curl http://localhost:8000/api/v1/hr/candidates/{candidate.id}/summary")
        
        return candidate.id, verification.id
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()

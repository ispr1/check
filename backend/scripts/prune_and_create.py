import sys
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load env variables
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Verification, VerificationStep, StepType, StepStatus, MANDATORY_STEPS, Candidate, VerificationStatus
from src.database import SessionLocal

def prune_and_create_new(candidate_name="IRAGAMREDDY SIVA PRASAD REDDY"):
    db = SessionLocal()
    try:
        # 1. Find Candidate
        candidate = db.query(Candidate).filter(Candidate.full_name == candidate_name).first()
        if not candidate:
            print(f"Candidate not found: {candidate_name}")
            return

        print(f"Candidate ID: {candidate.id}")

        # 2. Delete Existing Verification(s)
        old_verifications = db.query(Verification).filter(Verification.candidate_id == candidate.id).all()
        for v in old_verifications:
            print(f"Deleting old verification ID: {v.id}")
            db.delete(v)
        
        db.flush()

        # 3. Create New Verification
        new_v = Verification(
            candidate_id=candidate.id,
            company_id=candidate.company_id,
            status=VerificationStatus.LINK_SENT,
        )
        db.add(new_v)
        db.flush()

        print(f"New Verification ID: {new_v.id}")
        print(f"New Token: {new_v.token}")

        # 4. Create Initial Steps
        for step_type in MANDATORY_STEPS:
            step = VerificationStep(
                verification_id=new_v.id,
                step_type=step_type,
                is_mandatory=True,
                status=StepStatus.PENDING,
            )
            db.add(step)
            print(f"Added step: {step_type}")

        db.commit()
        print("\nPrune and Create successful.")
        print(f"NEW LINK: http://localhost:3000/verify/{new_v.token}")
        
        # Use existing tunnel host if possible
        tunnel_host = "41da66149d9193.lhr.life"
        print(f"TUNNEL LINK: https://{tunnel_host}/verify/{new_v.token}")
                
    finally:
        db.close()

if __name__ == "__main__":
    prune_and_create_new()

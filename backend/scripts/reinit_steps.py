import sys
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load env variables
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Verification, VerificationStep, StepType, StepStatus, MANDATORY_STEPS
from src.database import SessionLocal

def reinit_steps(token):
    db = SessionLocal()
    try:
        verification = db.query(Verification).filter(Verification.token == token).first()
        if not verification:
            print(f"Verification not found for token: {token}")
            return

        print(f"Initializing steps for Verification ID: {verification.id}")
        
        # 1. Create mandatory steps
        for step_type in MANDATORY_STEPS:
            # Check if exists (shouldn't, but be safe)
            existing = db.query(VerificationStep).filter(
                VerificationStep.verification_id == verification.id,
                VerificationStep.step_type == step_type
            ).first()
            
            if not existing:
                step = VerificationStep(
                    verification_id=verification.id,
                    step_type=step_type,
                    is_mandatory=True,
                    status=StepStatus.PENDING,
                )
                db.add(step)
                print(f"Added step: {step_type}")
            else:
                print(f"Step already exists: {step_type}")
        
        db.commit()
        print("Initialization successful.")
                
    finally:
        db.close()

if __name__ == "__main__":
    token = "f1e13705-1612-43ca-827d-828ea9180fbd"
    reinit_steps(token)

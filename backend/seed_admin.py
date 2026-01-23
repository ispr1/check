import sys
import os
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import from src package using absolute imports
from src.database import SessionLocal, engine, Base
from src.models.company import Company
from src.models.user import User


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def seed_admin():
    """Create demo company and admin user"""
    db: Session = SessionLocal()

    try:
        # Check if company already exists
        existing_company = (
            db.query(Company).filter(Company.name == "CHECK-360 Demo").first()
        )

        if existing_company:
            print(
                f"[INFO] Company already exists: {existing_company.name} (ID: {existing_company.id})"
            )
            company = existing_company
        else:
            # Create demo company
            company = Company(name="CHECK-360 Demo")
            db.add(company)
            db.commit()
            db.refresh(company)
            print(f"[OK] Created company: {company.name} (ID: {company.id})")

        # Check if admin already exists
        existing_admin = (
            db.query(User).filter(User.email == "admin@check360.com").first()
        )

        if existing_admin:
            print(f"[INFO] Admin user already exists: {existing_admin.email}")
            return

        # Create admin user
        admin_user = User(
            company_id=company.id,
            email="admin@check360.com",
            full_name="System Administrator",
            role="admin",
            hashed_password=hash_password(
                "admin123"
            ),  # Fixed: changed from password_hash
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"[OK] Created admin user: {admin_user.email}")
        print(f"[OK] Login credentials:")
        print(f"     Email: admin@check360.com")
        print(f"     Password: admin123")
        print(f"[OK] Seed completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seed failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    seed_admin()

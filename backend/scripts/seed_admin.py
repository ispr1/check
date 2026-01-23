import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import SessionLocal
from src.models import Company, User
from src.core.security import get_password_hash


def seed_admin():
    """Seed initial admin user for CHECK-360."""
    db = SessionLocal()

    try:
        # Check if admin already exists
        existing_admin = (
            db.query(User).filter(User.email == "admin@check360.com").first()
        )
        if existing_admin:
            print("✓ Admin user already exists")
            return

        # Create company if not exists
        company = db.query(Company).filter(Company.name == "CHECK-360 Demo").first()
        if not company:
            company = Company(name="CHECK-360 Demo", status="active")
            db.add(company)
            db.commit()
            db.refresh(company)
            print(f"✓ Created company: {company.name} (ID: {company.id})")

        # Create admin user
        admin_user = User(
            company_id=company.id,
            email="admin@check360.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"✓ Created admin user: {admin_user.email}")
        print(f"  User ID: {admin_user.id}")
        print(f"  Role: {admin_user.role}")
        print(f"  Password: admin123")
        print("\n✓ Seed completed successfully")

    except Exception as e:
        db.rollback()
        print(f"✗ Seed failed: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()

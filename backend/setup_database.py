import os
import sys
import subprocess

backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

from sqlalchemy import create_engine, text


def run_command(cmd, description):
    """Run a shell command and print status."""
    print(f"\n{'=' * 60}")
    print(f"▶ {description}")
    print(f"{'=' * 60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"✗ Failed: {description}")
        return False
    print(f"✓ Success: {description}")
    return True


def reset_database():
    """Drop and recreate all tables."""
    print("\n" + "=" * 60)
    print("▶ Resetting database tables")
    print("=" * 60)

    # Get DATABASE_URL from environment or use default
    database_url = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/check360"
    )

    engine = create_engine(database_url)

    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS candidates CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS companies CASCADE"))
            conn.commit()
        print("✓ All tables dropped successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to drop tables: {e}")
        return False
    finally:
        engine.dispose()


def main():
    """Complete database setup process."""
    print("\n" + "=" * 60)
    print("CHECK-360 Database Setup")
    print("=" * 60)

    # Step 1: Reset database
    if not reset_database():
        print("\n✗ Setup failed at database reset")
        return

    # Step 2: Remove old migration files
    old_migrations = [
        "alembic/versions/ccb0b6cb410f_initial_migration_companies_users_.py",
        "alembic/versions/__pycache__",
    ]
    for old_file in old_migrations:
        if os.path.exists(old_file):
            if os.path.isdir(old_file):
                import shutil

                shutil.rmtree(old_file)
            else:
                os.remove(old_file)
            print(f"✓ Removed {old_file}")

    # Step 3: Apply existing migration
    if not run_command("alembic upgrade head", "Applying database migrations"):
        print("\n✗ Setup failed at migration")
        return

    # Step 4: Seed admin user
    if not run_command("python seed_admin.py", "Seeding admin user"):
        print("\n✗ Setup failed at seeding")
        return

    print("\n" + "=" * 60)
    print("✅ DATABASE SETUP COMPLETE")
    print("=" * 60)
    print("\nLogin credentials:")
    print("  Email: admin@check360.com")
    print("  Password: admin123")
    print("\nStart server with: uvicorn src.main:app --reload")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

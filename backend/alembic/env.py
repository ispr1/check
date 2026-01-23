# filepath: d:\check\backend\alembic\env.py
import os
import sys
import src.models
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# Add backend directory to Python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

# Import Base and models
from src.database import Base
import src.models  # Registers all model classes

alembic_config = context.config

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

target_metadata = Base.metadata

# Force DB URL override for migration engine
database_url = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/check360"
)
alembic_config.set_main_option("sqlalchemy.url", database_url)


def apply_migrations_offline():
    """Offline mode: generate SQL without database connection."""
    db_url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def apply_migrations_online():
    """Online mode: apply migrations directly to database."""
    cfg_section = alembic_config.get_section(alembic_config.config_ini_section, {})

    engine = engine_from_config(
        cfg_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with engine.connect() as conn:
        context.configure(connection=conn, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    apply_migrations_offline()
else:
    apply_migrations_online()

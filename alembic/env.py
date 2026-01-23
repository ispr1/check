import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import Base and all models
from src.database import Base
from src.models import *

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url with environment variable or default
database_url = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/check360"
)
config.set_main_option("sqlalchemy.url", database_url)

# add your model's MetaData object here
target_metadata = Base.metadata


def apply_migrations_offline():
    """Offline mode: generate SQL without database connection."""
    db_url = config.get_main_option("sqlalchemy.url")
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
    cfg_section = config.get_section(config.config_ini_section, {})

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

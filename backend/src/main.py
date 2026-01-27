import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, candidates, verification_requests, verifications, verify_public

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============ Phase 2.5: Environment Safety Checks ============

def validate_environment():
    """
    Validate required environment variables on startup.
    
    Fails fast if:
    - SUREPASS_ENABLED=true but no API key
    - DATA_ENCRYPTION_KEY missing
    - Production mode with mock enabled
    """
    surepass_enabled = os.getenv("SUREPASS_ENABLED", "false").lower() == "true"
    surepass_key = os.getenv("SUREPASS_API_KEY", "")
    encryption_key = os.getenv("DATA_ENCRYPTION_KEY", "")
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    errors = []
    
    # Check 1: Surepass enabled but no key
    if surepass_enabled and not surepass_key:
        errors.append(
            "SUREPASS_ENABLED=true but SUREPASS_API_KEY is not set. "
            "Set the API key or disable Surepass (SUREPASS_ENABLED=false)."
        )
    
    # Check 2: Encryption key required for sensitive data
    if not encryption_key:
        if environment == "production":
            errors.append(
                "DATA_ENCRYPTION_KEY is required in production. "
                "Generate one with: python -c \"from src.utils.crypto import generate_encryption_key; print(generate_encryption_key())\""
            )
        else:
            logger.warning(
                "DATA_ENCRYPTION_KEY not set. Encryption disabled in development. "
                "This is NOT safe for production."
            )
    
    # Check 3: Production with mock enabled
    if environment == "production" and not surepass_enabled:
        errors.append(
            "Production mode detected but SUREPASS_ENABLED=false. "
            "Mock mode should never run in production."
        )
    
    # Fail fast if any critical errors
    if errors:
        for error in errors:
            logger.error(f"STARTUP VALIDATION FAILED: {error}")
        raise RuntimeError(
            f"Environment validation failed with {len(errors)} error(s). "
            "Check logs for details."
        )
    
    # Log successful validation
    logger.info(f"Environment validation passed: environment={environment}, surepass_enabled={surepass_enabled}")


# Run validation on import (before app starts)
validate_environment()


app = FastAPI(
    title="Check360 API",
    description="Background Check Management System - Verification Orchestrator",
    version="2.5.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(candidates.router, prefix="/api/v1")
app.include_router(verification_requests.router, prefix="/api/v1")
app.include_router(verifications.router, prefix="/api/v1")
app.include_router(verify_public.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Check360 API is running",
        "version": "2.5.0",
        "description": "Verification Orchestrator + Truth Comparator + Audit Engine"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.5.0"}


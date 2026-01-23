from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, candidates, verification_requests

app = FastAPI(
    title="Check360 API",
    description="Background Check Management System",
    version="1.0.0",
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


@app.get("/")
async def root():
    return {"message": "Check360 API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

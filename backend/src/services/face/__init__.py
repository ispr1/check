"""
Face Verification Service Package.

Phase 3: AWS Rekognition integration for identity confirmation.

NOT for:
- Liveness detection
- Proctoring
- Interview capture
- Emotion/age detection
"""

from .service import FaceVerificationService, get_face_service
from .contracts import (
    FaceCompareResult,
    FaceDecision,
    ReferenceSource,
)

__all__ = [
    "FaceVerificationService",
    "get_face_service",
    "FaceCompareResult",
    "FaceDecision",
    "ReferenceSource",
]

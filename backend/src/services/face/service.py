"""
Face Verification Service.

Orchestrates face comparison using configured provider.
Feature-flagged: mock | rekognition
"""

import os
import logging
import base64
from datetime import datetime
from typing import Optional, Union

from .contracts import (
    FaceCompareResult,
    FaceDecision,
    ReferenceSource,
    FaceNotAvailableResult,
)
from .mock import MockFaceProvider
from .rekognition import RekognitionProvider

logger = logging.getLogger(__name__)


class FaceVerificationService:
    """
    Face verification service with provider abstraction.
    
    Usage:
        service = get_face_service()
        result = service.compare_faces(selfie_b64, reference_b64, ...)
    """
    
    PROVIDER_MOCK = "mock"
    PROVIDER_REKOGNITION = "rekognition"
    
    def __init__(self):
        self._provider_name = os.getenv("FACE_PROVIDER", self.PROVIDER_MOCK)
        self._enabled = os.getenv("FACE_ENABLED", "true").lower() == "true"
        self._provider = None
        
        logger.info(f"FaceVerificationService: enabled={self._enabled}, provider={self._provider_name}")
    
    @property
    def provider(self):
        """Lazy-load provider based on config."""
        if self._provider is None:
            if self._provider_name == self.PROVIDER_REKOGNITION:
                self._provider = RekognitionProvider()
            else:
                self._provider = MockFaceProvider()
        return self._provider
    
    def is_mock_mode(self) -> bool:
        """Check if running in mock mode."""
        return self._provider_name == self.PROVIDER_MOCK
    
    def is_enabled(self) -> bool:
        """Check if face verification is enabled."""
        return self._enabled
    
    def compare_faces(
        self,
        selfie_base64: str,
        reference_base64: str,
        selfie_s3_key: str = "pending",
        reference_s3_key: str = "pending",
        reference_source: ReferenceSource = ReferenceSource.HR_UPLOAD,
    ) -> Union[FaceCompareResult, FaceNotAvailableResult]:
        """
        Compare selfie with reference image.
        
        Args:
            selfie_base64: Base64-encoded selfie image
            reference_base64: Base64-encoded reference image
            selfie_s3_key: S3 key where selfie is/will be stored
            reference_s3_key: S3 key where reference is/will be stored
            reference_source: Source of reference image
            
        Returns:
            FaceCompareResult with decision, confidence, and flags
        """
        if not self._enabled:
            logger.warning("Face verification is disabled")
            return FaceNotAvailableResult(message="Face verification is disabled")
        
        try:
            # Decode base64 to bytes
            selfie_bytes = base64.b64decode(selfie_base64)
            reference_bytes = base64.b64decode(reference_base64)
            
            # Validate minimum size (100 bytes = basically nothing)
            if len(selfie_bytes) < 100:
                return FaceCompareResult(
                    decision=FaceDecision.ERROR,
                    confidence_score=0.0,
                    reference_source=reference_source,
                    selfie_s3_key=selfie_s3_key,
                    reference_s3_key=reference_s3_key,
                    flags=["SELFIE_TOO_SMALL"],
                    compared_at=datetime.utcnow(),
                )
            
            if len(reference_bytes) < 100:
                return FaceCompareResult(
                    decision=FaceDecision.ERROR,
                    confidence_score=0.0,
                    reference_source=reference_source,
                    selfie_s3_key=selfie_s3_key,
                    reference_s3_key=reference_s3_key,
                    flags=["REFERENCE_TOO_SMALL"],
                    compared_at=datetime.utcnow(),
                )
            
            # Compare using provider
            result = self.provider.compare_faces(
                source_bytes=selfie_bytes,
                target_bytes=reference_bytes,
                source_key=selfie_s3_key,
                target_key=reference_s3_key,
                reference_source=reference_source,
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Face comparison failed: {e}")
            return FaceCompareResult(
                decision=FaceDecision.ERROR,
                confidence_score=0.0,
                reference_source=reference_source,
                selfie_s3_key=selfie_s3_key,
                reference_s3_key=reference_s3_key,
                flags=["COMPARISON_ERROR", str(e)],
                compared_at=datetime.utcnow(),
            )
    
    def compare_with_pending_reference(
        self,
        selfie_base64: str,
        selfie_s3_key: str = "pending",
    ) -> FaceCompareResult:
        """
        Handle case where no reference image exists yet.
        
        Returns PENDING_REFERENCE decision - HR must upload reference later.
        """
        return FaceCompareResult(
            decision=FaceDecision.PENDING_REFERENCE,
            confidence_score=0.0,
            reference_source=ReferenceSource.OTHER,
            selfie_s3_key=selfie_s3_key,
            reference_s3_key=None,
            flags=["AWAITING_REFERENCE"],
            compared_at=datetime.utcnow(),
        )


# Singleton instance
_service_instance: Optional[FaceVerificationService] = None


def get_face_service() -> FaceVerificationService:
    """Get or create singleton FaceVerificationService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = FaceVerificationService()
    return _service_instance

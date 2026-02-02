"""
Mock face comparison provider for development and testing.
"""

import logging
import random
from datetime import datetime
from typing import Optional

from .contracts import (
    FaceCompareResult,
    FaceDecision,
    ReferenceSource,
    get_decision_from_confidence,
)

logger = logging.getLogger(__name__)


class MockFaceProvider:
    """
    Mock face comparison provider.
    
    Returns configurable results for testing:
    - Default: High confidence match (92%)
    - Can simulate low confidence, mismatch, errors
    """
    
    # Configurable mock results
    MOCK_CONFIDENCE = 92.5
    MOCK_ENABLED = True
    
    def __init__(self):
        logger.info("MockFaceProvider initialized")
    
    def compare_faces(
        self,
        source_bytes: bytes,
        target_bytes: bytes,
        source_key: str = "mock_selfie.jpg",
        target_key: str = "mock_reference.jpg",
        reference_source: ReferenceSource = ReferenceSource.HR_UPLOAD,
    ) -> FaceCompareResult:
        """
        Mock face comparison.
        
        Returns configurable mock result for testing.
        """
        if not self.MOCK_ENABLED:
            return FaceCompareResult(
                decision=FaceDecision.NOT_AVAILABLE,
                confidence_score=0.0,
                reference_source=reference_source,
                selfie_s3_key=source_key,
                reference_s3_key=target_key,
                flags=["MOCK_DISABLED"],
            )
        
        # Simulate some processing time
        confidence = self.MOCK_CONFIDENCE
        
        # Add slight variance for realism
        confidence += random.uniform(-2.0, 2.0)
        confidence = max(0.0, min(100.0, confidence))
        
        decision = get_decision_from_confidence(confidence)
        
        flags = []
        if decision == FaceDecision.LOW_CONFIDENCE:
            flags.append("REQUIRES_HR_REVIEW")
        elif decision == FaceDecision.MISMATCH:
            flags.append("FACE_MISMATCH_DETECTED")
        
        logger.info(f"Mock compare: confidence={confidence:.1f}, decision={decision.value}")
        
        return FaceCompareResult(
            decision=decision,
            confidence_score=confidence,
            reference_source=reference_source,
            selfie_s3_key=source_key,
            reference_s3_key=target_key,
            flags=flags,
            compared_at=datetime.utcnow(),
            raw_response_encrypted=b"MOCK_ENCRYPTED_RESPONSE",
        )
    
    @classmethod
    def set_mock_confidence(cls, value: float):
        """Set mock confidence for testing different scenarios."""
        cls.MOCK_CONFIDENCE = max(0.0, min(100.0, value))
        logger.info(f"Mock confidence set to {cls.MOCK_CONFIDENCE}")
    
    @classmethod
    def set_mock_enabled(cls, enabled: bool):
        """Enable/disable mock provider."""
        cls.MOCK_ENABLED = enabled
        logger.info(f"Mock provider enabled={enabled}")

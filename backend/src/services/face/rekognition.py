"""
AWS Rekognition face comparison provider.

Feature-flagged: Only active when FACE_PROVIDER=rekognition
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional

from .contracts import (
    FaceCompareResult,
    FaceDecision,
    ReferenceSource,
    get_decision_from_confidence,
)

logger = logging.getLogger(__name__)


class RekognitionProvider:
    """
    AWS Rekognition CompareFaces wrapper.
    
    Uses boto3 to call Rekognition API.
    Raw response is encrypted and never exposed to HR.
    """
    
    def __init__(self):
        self._client = None
        self._region = os.getenv("AWS_REGION", "ap-south-1")
        logger.info(f"RekognitionProvider initialized (region={self._region})")
    
    @property
    def client(self):
        """Lazy-load boto3 client."""
        if self._client is None:
            try:
                import boto3
                self._client = boto3.client("rekognition", region_name=self._region)
            except ImportError:
                raise RuntimeError("boto3 not installed. Run: pip install boto3")
            except Exception as e:
                logger.error(f"Failed to create Rekognition client: {e}")
                raise
        return self._client
    
    def compare_faces(
        self,
        source_bytes: bytes,
        target_bytes: bytes,
        source_key: str,
        target_key: str,
        reference_source: ReferenceSource = ReferenceSource.HR_UPLOAD,
        similarity_threshold: float = 70.0,
    ) -> FaceCompareResult:
        """
        Compare two face images using AWS Rekognition.
        
        Args:
            source_bytes: Selfie image bytes
            target_bytes: Reference image bytes
            source_key: S3 key of selfie
            target_key: S3 key of reference
            reference_source: Source of reference image
            similarity_threshold: Minimum similarity to return matches (default 70)
            
        Returns:
            FaceCompareResult with confidence and decision
        """
        try:
            response = self.client.compare_faces(
                SourceImage={"Bytes": source_bytes},
                TargetImage={"Bytes": target_bytes},
                SimilarityThreshold=similarity_threshold,
            )
            
            # Get highest confidence match
            face_matches = response.get("FaceMatches", [])
            if face_matches:
                best_match = max(face_matches, key=lambda x: x.get("Similarity", 0))
                confidence = best_match.get("Similarity", 0.0)
            else:
                # No match found
                confidence = 0.0
            
            decision = get_decision_from_confidence(confidence)
            
            flags = []
            if decision == FaceDecision.LOW_CONFIDENCE:
                flags.append("REQUIRES_HR_REVIEW")
            elif decision == FaceDecision.MISMATCH:
                flags.append("FACE_MISMATCH_DETECTED")
            
            # Unmatched faces info
            unmatched = response.get("UnmatchedFaces", [])
            if unmatched:
                flags.append(f"UNMATCHED_FACES_{len(unmatched)}")
            
            # Encrypt raw response (actual encryption done at storage layer)
            raw_json = json.dumps(response, default=str).encode("utf-8")
            
            logger.info(f"Rekognition compare: confidence={confidence:.1f}, decision={decision.value}")
            
            return FaceCompareResult(
                decision=decision,
                confidence_score=confidence,
                reference_source=reference_source,
                selfie_s3_key=source_key,
                reference_s3_key=target_key,
                flags=flags,
                compared_at=datetime.utcnow(),
                raw_response_encrypted=raw_json,  # Will be encrypted before storage
            )
            
        except self.client.exceptions.InvalidParameterException as e:
            logger.warning(f"Rekognition invalid params: {e}")
            return FaceCompareResult(
                decision=FaceDecision.ERROR,
                confidence_score=0.0,
                reference_source=reference_source,
                selfie_s3_key=source_key,
                reference_s3_key=target_key,
                flags=["INVALID_IMAGE", str(e)],
                compared_at=datetime.utcnow(),
            )
        
        except Exception as e:
            logger.error(f"Rekognition error: {e}")
            return FaceCompareResult(
                decision=FaceDecision.NOT_AVAILABLE,
                confidence_score=0.0,
                reference_source=reference_source,
                selfie_s3_key=source_key,
                reference_s3_key=target_key,
                flags=["PROVIDER_ERROR", str(e)],
                compared_at=datetime.utcnow(),
            )

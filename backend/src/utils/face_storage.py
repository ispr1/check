"""
Face image storage utility.

Handles S3 storage for face images:
- Candidate selfies
- HR-uploaded references
- Encrypted audit data

S3 Structure:
s3://check360-faces/
├── candidates/{candidate_id}/selfie_{timestamp}.jpg
├── references/{candidate_id}/{source}_{timestamp}.jpg
└── audit/{verification_id}/comparison_{timestamp}.json.enc
"""

import os
import base64
import logging
import hashlib
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class FaceStorageError(Exception):
    """Face storage operation failed."""
    pass


class FaceStorage:
    """
    Face image storage handler.
    
    Supports:
    - Local filesystem (development)
    - AWS S3 (production)
    """
    
    STORAGE_LOCAL = "local"
    STORAGE_S3 = "s3"
    
    def __init__(self):
        self._storage_type = os.getenv("FACE_STORAGE", self.STORAGE_LOCAL)
        self._bucket = os.getenv("FACE_S3_BUCKET", "check360-faces")
        self._local_path = Path(os.getenv("FACE_LOCAL_PATH", "./face_images"))
        self._s3_client = None
        
        # Ensure local directory exists
        if self._storage_type == self.STORAGE_LOCAL:
            self._local_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"FaceStorage: local mode at {self._local_path}")
        else:
            logger.info(f"FaceStorage: S3 mode bucket={self._bucket}")
    
    @property
    def s3_client(self):
        """Lazy-load S3 client."""
        if self._s3_client is None:
            try:
                import boto3
                self._s3_client = boto3.client("s3")
            except ImportError:
                raise RuntimeError("boto3 not installed")
        return self._s3_client
    
    def _generate_key(self, prefix: str, candidate_id: int, suffix: str) -> str:
        """Generate storage key."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}/{candidate_id}/{suffix}_{timestamp}.jpg"
    
    def save_selfie(
        self,
        candidate_id: int,
        image_base64: str,
    ) -> str:
        """
        Save candidate selfie image.
        
        Returns: Storage key
        """
        key = self._generate_key("candidates", candidate_id, "selfie")
        image_bytes = base64.b64decode(image_base64)
        
        if self._storage_type == self.STORAGE_S3:
            self.s3_client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=image_bytes,
                ContentType="image/jpeg",
            )
        else:
            path = self._local_path / key
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(image_bytes)
        
        logger.info(f"Saved selfie for candidate {candidate_id}: {key}")
        return key
    
    def save_reference(
        self,
        candidate_id: int,
        image_base64: str,
        source: str = "hr_upload",
    ) -> str:
        """
        Save reference image.
        
        Args:
            candidate_id: Candidate ID
            image_base64: Base64-encoded image
            source: Source of image (hr_upload, aadhaar, id_card)
            
        Returns: Storage key
        """
        key = self._generate_key("references", candidate_id, source)
        image_bytes = base64.b64decode(image_base64)
        
        if self._storage_type == self.STORAGE_S3:
            self.s3_client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=image_bytes,
                ContentType="image/jpeg",
            )
        else:
            path = self._local_path / key
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(image_bytes)
        
        logger.info(f"Saved reference for candidate {candidate_id}: {key}")
        return key
    
    def save_audit(
        self,
        verification_id: int,
        comparison_data: bytes,
    ) -> str:
        """
        Save encrypted audit data.
        
        Args:
            verification_id: Verification ID
            comparison_data: Encrypted comparison result
            
        Returns: Storage key
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        key = f"audit/{verification_id}/comparison_{timestamp}.json.enc"
        
        if self._storage_type == self.STORAGE_S3:
            self.s3_client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=comparison_data,
                ContentType="application/octet-stream",
            )
        else:
            path = self._local_path / key
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(comparison_data)
        
        logger.info(f"Saved audit for verification {verification_id}: {key}")
        return key
    
    def get_image(self, key: str) -> Optional[bytes]:
        """
        Retrieve image bytes by key.
        """
        try:
            if self._storage_type == self.STORAGE_S3:
                response = self.s3_client.get_object(Bucket=self._bucket, Key=key)
                return response["Body"].read()
            else:
                path = self._local_path / key
                if path.exists():
                    return path.read_bytes()
                return None
        except Exception as e:
            logger.error(f"Failed to get image {key}: {e}")
            return None
    
    def get_presigned_url(self, key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate presigned URL for HR view.
        
        Args:
            key: Storage key
            expires_in: URL expiration in seconds (default 1 hour)
            
        Returns: Presigned URL or local file URL
        """
        if self._storage_type == self.STORAGE_S3:
            try:
                url = self.s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self._bucket, "Key": key},
                    ExpiresIn=expires_in,
                )
                return url
            except Exception as e:
                logger.error(f"Failed to generate presigned URL: {e}")
                return None
        else:
            # Local mode: return file path
            path = self._local_path / key
            if path.exists():
                return f"file://{path.absolute()}"
            return None


# Singleton instance
_storage_instance: Optional[FaceStorage] = None


def get_face_storage() -> FaceStorage:
    """Get or create singleton FaceStorage instance."""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = FaceStorage()
    return _storage_instance

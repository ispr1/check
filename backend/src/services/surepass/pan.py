"""
PAN verification service.

Uses Aadhaar-verified name/DOB for cross-check.
Surepass provides name_match, dob_match, aadhaar_seeding_status.
"""

import logging
import re
from typing import Optional
from datetime import datetime

from .client import get_surepass_client
from .exceptions import SurepassInvalidInputError
from . import mock_responses

logger = logging.getLogger(__name__)


class PANService:
    """Service for PAN verification."""
    
    def __init__(self):
        self.client = get_surepass_client()
    
    def validate_pan_number(self, pan_number: str) -> str:
        """Validate and clean PAN number."""
        cleaned = pan_number.upper().strip()
        
        # PAN format: AAAAA1234A (5 letters, 4 digits, 1 letter)
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
        if not re.match(pattern, cleaned):
            raise SurepassInvalidInputError(
                "pan_number", 
                "Invalid format. Must be 5 letters + 4 digits + 1 letter (e.g., ABCDE1234F)"
            )
        
        return cleaned
    
    def verify(
        self, 
        pan_number: str, 
        name: str, 
        dob: str
    ) -> dict:
        """
        Verify PAN and cross-check with Aadhaar-verified data.
        
        Args:
            pan_number: 10-character PAN
            name: Aadhaar-verified name for cross-check
            dob: Aadhaar-verified DOB for cross-check (YYYY-MM-DD)
            
        Returns:
            Verification result with match indicators
        """
        cleaned_pan = self.validate_pan_number(pan_number)
        
        if self.client.is_mock_mode():
            logger.info(f"Mock: Verifying PAN XXXXX{cleaned_pan[5:9]}X")
            response = mock_responses.mock_pan_verification(cleaned_pan, name, dob)["data"]
        else:
            response = self.client.post("pan-verification", {
                "pan_number": cleaned_pan,
                "name": name,
                "dob": dob
            })
        
        return self._process_response(response, cleaned_pan)
    
    def _process_response(self, response: dict, pan_number: str) -> dict:
        """Process Surepass response and determine verification status."""
        
        # Extract key fields
        valid = response.get("valid", False)
        name_match = response.get("name_match", False)
        dob_match = response.get("dob_match", False)
        aadhaar_linked = response.get("aadhaar_seeding_status", "N") == "Y"
        
        # Determine status based on decision logic
        if not valid:
            status = "FAILED"
            score = 0
            message = "PAN not found or invalid"
        elif valid and name_match and dob_match:
            status = "VERIFIED"
            score = 100
            message = "PAN verified with matching name and DOB"
        elif valid and name_match and not dob_match:
            status = "PARTIAL"
            score = 75
            message = "PAN valid, name matches but DOB mismatch"
        elif valid and not name_match and dob_match:
            status = "PARTIAL"
            score = 70
            message = "PAN valid, DOB matches but name mismatch"
        elif valid and not name_match and not dob_match:
            status = "PARTIAL"
            score = 50
            message = "PAN valid but name and DOB do not match Aadhaar"
        else:
            status = "PARTIAL"
            score = 60
            message = "PAN verification completed with partial match"
        
        return {
            "status": status,
            "score": score,
            "message": message,
            "details": {
                "pan_number": pan_number,
                "valid": valid,
                "name_match": name_match,
                "dob_match": dob_match,
                "aadhaar_linked": aadhaar_linked,
                "full_name_on_pan": response.get("full_name", ""),
                "dob_on_pan": response.get("dob", ""),
                "name_match_score": response.get("name_match_score", 0),
            },
            "verified_at": datetime.utcnow().isoformat(),
        }


# Singleton instance
_service_instance: Optional[PANService] = None


def get_pan_service() -> PANService:
    """Get or create singleton PANService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = PANService()
    return _service_instance

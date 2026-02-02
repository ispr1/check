"""
Aadhaar OTP verification service.

Flow:
1. generate_otp(aadhaar_number) → Returns client_id
2. submit_otp(client_id, otp) → Returns verified Aadhaar data
3. compare_aadhaar(surepass_data, candidate_data) → Returns comparison result
"""

import logging
from typing import Optional
from datetime import datetime

from .client import get_surepass_client
from .exceptions import SurepassError, SurepassInvalidInputError, SurepassNotAvailableError
from . import mock_responses

logger = logging.getLogger(__name__)


class AadhaarService:
    """Service for Aadhaar OTP-based verification."""
    
    def __init__(self):
        self.client = get_surepass_client()
    
    def validate_aadhaar_number(self, aadhaar_number: str) -> str:
        """Validate and clean Aadhaar number."""
        # Remove spaces and dashes
        cleaned = aadhaar_number.replace(" ", "").replace("-", "")
        
        if not cleaned.isdigit():
            raise SurepassInvalidInputError("aadhaar_number", "Must contain only digits")
        
        if len(cleaned) != 12:
            raise SurepassInvalidInputError("aadhaar_number", "Must be exactly 12 digits")
        
        # Basic Verhoeff checksum validation would go here
        # For now, just check first digit is not 0 or 1
        if cleaned[0] in "01":
            raise SurepassInvalidInputError("aadhaar_number", "Invalid Aadhaar number format")
        
        return cleaned
    
    def generate_otp(self, aadhaar_number: str) -> dict:
        """
        Request OTP for Aadhaar verification.
        
        Args:
            aadhaar_number: 12-digit Aadhaar number
            
        Returns:
            dict with client_id for OTP submission
        """
        cleaned = self.validate_aadhaar_number(aadhaar_number)
        
        if self.client.is_mock_mode():
            logger.info(f"Mock: Generating OTP for Aadhaar XXXX-XXXX-{cleaned[-4:]}")
            return mock_responses.mock_aadhaar_generate_otp(cleaned)["data"]
        
        try:
            response = self.client.post("aadhaar-v2/generate-otp", {
                "id_number": cleaned
            })
        except SurepassNotAvailableError as e:
            logger.warning(f"Aadhaar OTP API not available: {e.message}")
            return {
                "status": "NOT_AVAILABLE",
                "client_id": None,
                "message": "Aadhaar verification service temporarily unavailable",
                "error": "API_NOT_AVAILABLE",
            }
        
        return response
    
    def submit_otp(self, client_id: str, otp: str) -> dict:
        """
        Submit OTP and get verified Aadhaar data.
        
        Args:
            client_id: Client ID from generate_otp response
            otp: 6-digit OTP entered by user
            
        Returns:
            Verified Aadhaar data (name, DOB, address, photo, etc.)
        """
        if not otp or len(otp) != 6 or not otp.isdigit():
            raise SurepassInvalidInputError("otp", "Must be exactly 6 digits")
        
        if self.client.is_mock_mode():
            logger.info(f"Mock: Submitting OTP for client_id {client_id}")
            return mock_responses.mock_aadhaar_submit_otp(client_id, otp)["data"]
        
        try:
            response = self.client.post("aadhaar-v2/submit-otp", {
                "client_id": client_id,
                "otp": otp
            })
        except SurepassNotAvailableError as e:
            logger.warning(f"Aadhaar submit OTP API not available: {e.message}")
            return {
                "status": "NOT_AVAILABLE",
                "message": "Aadhaar verification service temporarily unavailable",
                "error": "API_NOT_AVAILABLE",
            }
        
        return response
    
    def compare(
        self, 
        surepass_data: dict, 
        candidate_name: str,
        candidate_dob: str,
        candidate_address: Optional[str] = None
    ) -> dict:
        """
        Compare Surepass Aadhaar data with candidate-provided data.
        
        Args:
            surepass_data: Verified data from submit_otp
            candidate_name: Name provided by candidate
            candidate_dob: DOB provided by candidate (YYYY-MM-DD)
            candidate_address: Address provided by candidate (optional)
            
        Returns:
            Comparison result with match scores
        """
        from src.utils.comparison import fuzzy_name_match, exact_match, address_similarity
        
        # Extract Surepass values
        sp_name = surepass_data.get("full_name", "")
        sp_dob = surepass_data.get("dob", "")
        sp_address = surepass_data.get("full_address", "")
        sp_gender = surepass_data.get("gender", "")
        
        # Calculate matches
        name_score = fuzzy_name_match(sp_name, candidate_name)
        name_match = name_score >= 85
        dob_match = exact_match(sp_dob, candidate_dob)
        address_match = address_similarity(sp_address, candidate_address) if candidate_address else "not_provided"
        
        # Calculate overall step score
        score = 0
        if name_match:
            score += 40  # Name is 40%
        elif name_score >= 70:
            score += 25  # Partial name match
        
        if dob_match:
            score += 30  # DOB is 30%
        
        if address_match == "full":
            score += 20
        elif address_match == "partial":
            score += 10
        elif address_match == "not_provided":
            score += 10  # No penalty for not provided
        
        # Gender always stored
        score += 10  # Base points for successful verification
        
        # Determine status
        if score >= 90:
            status = "VERIFIED"
        elif score >= 70:
            status = "PARTIAL"
        else:
            status = "FAILED"
        
        return {
            "status": status,
            "score": min(score, 100),
            "details": {
                "name_match": name_match,
                "name_score": name_score,
                "dob_match": dob_match,
                "address_match": address_match,
                "surepass_name": sp_name,
                "surepass_dob": sp_dob,
                "surepass_gender": sp_gender,
            },
            "photo_stored": "profile_image" in surepass_data,
            "verified_at": datetime.utcnow().isoformat(),
        }


# Singleton instance
_service_instance: Optional[AadhaarService] = None


def get_aadhaar_service() -> AadhaarService:
    """Get or create singleton AadhaarService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = AadhaarService()
    return _service_instance

"""
DigiLocker verification service.

Flow:
1. init_session() → Returns redirect URL for user auth
2. fetch_documents(session_id) → Returns document data from DigiLocker
3. parse_document(doc_type, data) → Extract identity fields
4. compare() → Compare with candidate data

Status: SKELETON - awaiting Surepass endpoint confirmation
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from .client import get_surepass_client
from .exceptions import SurepassInvalidInputError, SurepassNotAvailableError
from .contracts import VerificationStepStatus, not_available_result

logger = logging.getLogger(__name__)


class DigilockerDocType(str, Enum):
    """Supported DigiLocker document types."""
    AADHAAR = "AADHAAR"
    PAN = "PAN"
    DRIVING_LICENSE = "DL"
    VOTER_ID = "EPIC"
    CLASS_10_MARKSHEET = "CBSE10"
    CLASS_12_MARKSHEET = "CBSE12"


class DigilockerService:
    """
    Service for DigiLocker-based document verification.
    
    DigiLocker provides government-verified digital documents.
    Useful as alternative/complement to direct Aadhaar OTP.
    """
    
    # Endpoints - UPDATE WHEN SUREPASS CONFIRMS
    ENDPOINT_INIT = "digilocker/init"
    ENDPOINT_FETCH = "digilocker/fetch"
    
    def __init__(self):
        self.client = get_surepass_client()
    
    def init_session(
        self, 
        callback_url: str,
        documents: List[DigilockerDocType] = None
    ) -> dict:
        """
        Initialize DigiLocker session.
        
        Args:
            callback_url: URL to redirect after user auth
            documents: List of document types to request
            
        Returns:
            Dict with redirect_url and session_id
        """
        if documents is None:
            documents = [DigilockerDocType.AADHAAR]
        
        doc_codes = [d.value for d in documents]
        
        if self.client.is_mock_mode():
            logger.info(f"Mock: Initializing DigiLocker for docs={doc_codes}")
            return self._mock_init_response(callback_url, doc_codes)
        
        try:
            response = self.client.post(self.ENDPOINT_INIT, {
                "callback_url": callback_url,
                "documents": doc_codes,
            })
        except SurepassNotAvailableError as e:
            logger.warning(f"DigiLocker init API not available: {e.message}")
            return {
                "status": "NOT_AVAILABLE",
                "redirect_url": None,
                "session_id": None,
                "message": "DigiLocker service temporarily unavailable",
                "error": "API_NOT_AVAILABLE",
            }
        
        return response
    
    def fetch_documents(self, session_id: str) -> dict:
        """
        Fetch documents after user completes DigiLocker auth.
        
        Args:
            session_id: Session ID from init_session
            
        Returns:
            Dict with document data
        """
        if not session_id:
            raise SurepassInvalidInputError("session_id", "Required")
        
        if self.client.is_mock_mode():
            logger.info(f"Mock: Fetching DigiLocker docs for session={session_id}")
            return self._mock_fetch_response(session_id)
        
        try:
            response = self.client.post(self.ENDPOINT_FETCH, {
                "session_id": session_id,
            })
        except SurepassNotAvailableError as e:
            logger.warning(f"DigiLocker fetch API not available: {e.message}")
            return {
                "status": "NOT_AVAILABLE",
                "documents": [],
                "message": "DigiLocker service temporarily unavailable",
                "error": "API_NOT_AVAILABLE",
            }
        
        return response
    
    def parse_document(self, doc_type: DigilockerDocType, doc_data: dict) -> dict:
        """
        Parse identity fields from DigiLocker document.
        
        Args:
            doc_type: Type of document
            doc_data: Raw document data from DigiLocker
            
        Returns:
            Normalized identity fields
        """
        parser = {
            DigilockerDocType.AADHAAR: self._parse_aadhaar,
            DigilockerDocType.PAN: self._parse_pan,
            DigilockerDocType.DRIVING_LICENSE: self._parse_dl,
            DigilockerDocType.VOTER_ID: self._parse_voter_id,
        }.get(doc_type, self._parse_generic)
        
        return parser(doc_data)
    
    def compare(
        self,
        doc_data: dict,
        candidate_name: str,
        candidate_dob: str
    ) -> dict:
        """
        Compare DigiLocker document data with candidate input.
        
        Args:
            doc_data: Parsed document data
            candidate_name: Candidate-provided name
            candidate_dob: Candidate-provided DOB (YYYY-MM-DD)
            
        Returns:
            Comparison result with status
        """
        from src.utils.comparison import fuzzy_name_match, exact_match
        
        doc_name = doc_data.get("full_name", "")
        doc_dob = doc_data.get("dob", "")
        
        name_score = fuzzy_name_match(doc_name, candidate_name)
        name_match = name_score >= 85
        dob_match = exact_match(doc_dob, candidate_dob)
        
        if name_match and dob_match:
            status = VerificationStepStatus.VERIFIED
            score = 100
            message = "Identity verified via DigiLocker"
        elif name_match or dob_match:
            status = VerificationStepStatus.PARTIAL
            score = 70
            message = "Partial match - one field differs"
        else:
            status = VerificationStepStatus.FAILED
            score = 30
            message = "Identity mismatch"
        
        return {
            "status": status.value,
            "score": score,
            "message": message,
            "details": {
                "doc_name": doc_name,
                "candidate_name": candidate_name,
                "name_match": name_match,
                "name_score": name_score,
                "doc_dob": doc_dob,
                "candidate_dob": candidate_dob,
                "dob_match": dob_match,
            },
            "verified_at": datetime.utcnow().isoformat(),
        }
    
    # ============================================================
    # DOCUMENT PARSERS
    # ============================================================
    
    def _parse_aadhaar(self, doc_data: dict) -> dict:
        """Parse Aadhaar document."""
        return {
            "doc_type": "AADHAAR",
            "full_name": doc_data.get("name", ""),
            "dob": doc_data.get("dob", ""),
            "gender": doc_data.get("gender", ""),
            "address": doc_data.get("address", {}),
            "masked_number": doc_data.get("masked_aadhaar", ""),
        }
    
    def _parse_pan(self, doc_data: dict) -> dict:
        """Parse PAN document."""
        return {
            "doc_type": "PAN",
            "full_name": doc_data.get("name", ""),
            "dob": doc_data.get("dob", ""),
            "pan_number": doc_data.get("pan_number", ""),
        }
    
    def _parse_dl(self, doc_data: dict) -> dict:
        """Parse Driving License document."""
        return {
            "doc_type": "DL",
            "full_name": doc_data.get("name", ""),
            "dob": doc_data.get("dob", ""),
            "dl_number": doc_data.get("dl_number", ""),
            "validity": doc_data.get("validity", ""),
            "address": doc_data.get("address", {}),
        }
    
    def _parse_voter_id(self, doc_data: dict) -> dict:
        """Parse Voter ID document."""
        return {
            "doc_type": "VOTER_ID",
            "full_name": doc_data.get("name", ""),
            "dob": doc_data.get("dob", ""),
            "epic_number": doc_data.get("epic_number", ""),
            "father_name": doc_data.get("father_name", ""),
            "address": doc_data.get("address", {}),
        }
    
    def _parse_generic(self, doc_data: dict) -> dict:
        """Generic document parser."""
        return {
            "doc_type": "UNKNOWN",
            "full_name": doc_data.get("name", doc_data.get("full_name", "")),
            "dob": doc_data.get("dob", ""),
            "raw_data": doc_data,
        }
    
    # ============================================================
    # MOCK RESPONSES
    # ============================================================
    
    def _mock_init_response(self, callback_url: str, doc_codes: List[str]) -> dict:
        """Mock init session response."""
        return {
            "status": "SUCCESS",
            "redirect_url": f"https://digilocker.gov.in/auth?callback={callback_url}&session=mock-123",
            "session_id": "mock-digilocker-session-123",
            "message": "Session initialized. Redirect user to URL.",
        }
    
    def _mock_fetch_response(self, session_id: str) -> dict:
        """Mock fetch documents response."""
        return {
            "status": "SUCCESS",
            "documents": [
                {
                    "doc_type": "AADHAAR",
                    "name": "RAJESH KUMAR SHARMA",
                    "dob": "15-05-1990",
                    "gender": "M",
                    "masked_aadhaar": "XXXX-XXXX-1234",
                    "address": {
                        "house": "123",
                        "street": "MG Road",
                        "city": "Bangalore",
                        "state": "Karnataka",
                        "pincode": "560001",
                    },
                    "verified": True,
                }
            ],
            "session_id": session_id,
            "fetched_at": datetime.utcnow().isoformat(),
        }


# Singleton instance
_service_instance: Optional[DigilockerService] = None


def get_digilocker_service() -> DigilockerService:
    """Get or create singleton DigilockerService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = DigilockerService()
    return _service_instance

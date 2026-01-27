"""
Surepass API client with mock support.

Features:
- Bearer token authentication
- Configurable base URL (sandbox/production)
- Timeout + single retry
- Masked logging (never log full Aadhaar/PAN)
- Mock mode via SUREPASS_ENABLED flag
"""

import os
import re
import logging
import httpx
from typing import Optional

from .exceptions import (
    SurepassError,
    SurepassTimeoutError,
    SurepassAuthError,
    SurepassRateLimitError,
)

# Configure module logger
logger = logging.getLogger(__name__)


def mask_sensitive_data(data: str) -> str:
    """Mask Aadhaar, PAN, and UAN numbers in logs."""
    # Aadhaar: 12 digits → XXXX-XXXX-1234
    data = re.sub(r'\b\d{12}\b', lambda m: f"XXXX-XXXX-{m.group()[-4:]}", data)
    # PAN: 10 alphanumeric → XXXXX1234X
    data = re.sub(r'\b[A-Z]{5}\d{4}[A-Z]\b', lambda m: f"XXXXX{m.group()[5:9]}X", data)
    # UAN: 12 digits (same pattern as Aadhaar)
    return data


class SurepassClient:
    """
    HTTP client for Surepass API.
    
    Usage:
        client = SurepassClient()
        response = client.post("pan-verification", {"pan_number": "ABCDE1234F"})
    """
    
    DEFAULT_TIMEOUT = 10.0  # seconds
    MAX_RETRIES = 1
    
    def __init__(self):
        self.enabled = os.getenv("SUREPASS_ENABLED", "false").lower() == "true"
        self.base_url = os.getenv(
            "SUREPASS_BASE_URL", 
            "https://sandbox.surepass.io/api/v1"
        ).rstrip("/")
        self.api_key = os.getenv("SUREPASS_API_KEY", "")
        
        if self.enabled and not self.api_key:
            logger.warning("SUREPASS_ENABLED=true but SUREPASS_API_KEY is not set!")
        
        logger.info(f"SurepassClient initialized: enabled={self.enabled}, base_url={self.base_url}")
    
    def _get_headers(self) -> dict:
        """Get request headers with authorization."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        payload: Optional[dict] = None,
        retry_count: int = 0
    ) -> dict:
        """
        Make HTTP request to Surepass API.
        
        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint (e.g., "pan-verification")
            payload: Request body (for POST)
            retry_count: Current retry attempt
            
        Returns:
            Response JSON as dict
            
        Raises:
            SurepassError: On API errors
            SurepassTimeoutError: On timeout
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Log request (masked)
        masked_payload = mask_sensitive_data(str(payload)) if payload else "{}"
        logger.info(f"Surepass request: {method} {endpoint} - {masked_payload}")
        
        try:
            with httpx.Client(timeout=self.DEFAULT_TIMEOUT) as client:
                if method.upper() == "GET":
                    response = client.get(url, headers=self._get_headers())
                else:  # POST
                    response = client.post(url, headers=self._get_headers(), json=payload)
                
                # Log response status
                logger.info(f"Surepass response: {response.status_code}")
                
                # Handle HTTP errors
                if response.status_code == 401:
                    raise SurepassAuthError()
                elif response.status_code == 429:
                    raise SurepassRateLimitError()
                elif response.status_code >= 500:
                    if retry_count < self.MAX_RETRIES:
                        logger.warning(f"Surepass 5xx error, retrying ({retry_count + 1}/{self.MAX_RETRIES})")
                        return self._make_request(method, endpoint, payload, retry_count + 1)
                    raise SurepassError(
                        message=f"Surepass server error: {response.status_code}",
                        status_code=response.status_code
                    )
                
                # Parse response
                try:
                    return response.json()
                except Exception:
                    raise SurepassError(
                        message="Invalid JSON response from Surepass",
                        status_code=response.status_code
                    )
                    
        except httpx.TimeoutException:
            if retry_count < self.MAX_RETRIES:
                logger.warning(f"Surepass timeout, retrying ({retry_count + 1}/{self.MAX_RETRIES})")
                return self._make_request(method, endpoint, payload, retry_count + 1)
            raise SurepassTimeoutError(endpoint)
        except httpx.RequestError as e:
            raise SurepassError(message=f"Request failed: {str(e)}")
    
    def post(self, endpoint: str, payload: dict) -> dict:
        """
        Make POST request to Surepass API.
        
        Args:
            endpoint: API endpoint
            payload: Request body
            
        Returns:
            Response data (from "data" key if present, else full response)
        """
        if not self.enabled:
            logger.info(f"Mock mode: {endpoint}")
            # Return None to signal mock mode - callers should handle this
            return None
        
        response = self._make_request("POST", endpoint, payload)
        
        # Extract data if wrapped
        if isinstance(response, dict) and "data" in response:
            return response["data"]
        return response
    
    def get(self, endpoint: str) -> dict:
        """Make GET request to Surepass API."""
        if not self.enabled:
            logger.info(f"Mock mode: {endpoint}")
            return None
        
        response = self._make_request("GET", endpoint)
        
        if isinstance(response, dict) and "data" in response:
            return response["data"]
        return response
    
    def is_mock_mode(self) -> bool:
        """Check if client is in mock mode."""
        return not self.enabled


# Singleton instance for easy import
_client_instance: Optional[SurepassClient] = None


def get_surepass_client() -> SurepassClient:
    """Get or create singleton SurepassClient instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = SurepassClient()
    return _client_instance

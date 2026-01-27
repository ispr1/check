"""
Custom exceptions for Surepass API interactions.
"""


class SurepassError(Exception):
    """Base exception for Surepass errors."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)


class SurepassTimeoutError(SurepassError):
    """Raised when Surepass API request times out."""
    
    def __init__(self, endpoint: str):
        super().__init__(
            message=f"Surepass request to {endpoint} timed out",
            status_code=408
        )


class SurepassInvalidInputError(SurepassError):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Invalid input for {field}: {reason}",
            status_code=422
        )


class SurepassAuthError(SurepassError):
    """Raised when authentication fails."""
    
    def __init__(self):
        super().__init__(
            message="Surepass authentication failed - check API key",
            status_code=401
        )


class SurepassRateLimitError(SurepassError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self):
        super().__init__(
            message="Surepass rate limit exceeded - try again later",
            status_code=429
        )

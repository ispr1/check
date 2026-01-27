"""
Encryption utility for sensitive verification data.

AES-256-GCM encryption for:
- raw_response (government identity data)
- Sensitive fields in input_data (Aadhaar, PAN, UAN numbers)

NOT encrypted (HR needs visibility):
- Face images
- Uploaded documents
- Payslips
"""

import os
import json
import base64
import logging
from typing import Union, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logger = logging.getLogger(__name__)

# Key length for AES-256
KEY_LENGTH = 32  # 256 bits
NONCE_LENGTH = 12  # 96 bits (recommended for GCM)


class EncryptionError(Exception):
    """Raised when encryption/decryption fails."""
    pass


def _get_encryption_key() -> bytes:
    """
    Get encryption key from environment.
    Key must be 32 bytes (256 bits) base64 encoded.
    """
    key_b64 = os.getenv("DATA_ENCRYPTION_KEY")
    
    if not key_b64:
        raise EncryptionError(
            "DATA_ENCRYPTION_KEY not set. Cannot encrypt sensitive data."
        )
    
    try:
        key = base64.b64decode(key_b64)
        if len(key) != KEY_LENGTH:
            raise EncryptionError(
                f"DATA_ENCRYPTION_KEY must be {KEY_LENGTH} bytes (base64 encoded). "
                f"Got {len(key)} bytes."
            )
        return key
    except Exception as e:
        raise EncryptionError(f"Invalid DATA_ENCRYPTION_KEY: {e}")


def generate_encryption_key() -> str:
    """
    Generate a new random encryption key.
    Returns base64-encoded key for .env file.
    
    Usage:
        python -c "from src.utils.crypto import generate_encryption_key; print(generate_encryption_key())"
    """
    key = os.urandom(KEY_LENGTH)
    return base64.b64encode(key).decode('utf-8')


def encrypt(data: Union[dict, str]) -> str:
    """
    Encrypt data using AES-256-GCM.
    
    Args:
        data: Dictionary or string to encrypt
        
    Returns:
        Base64-encoded ciphertext (nonce + ciphertext + tag)
    """
    key = _get_encryption_key()
    aesgcm = AESGCM(key)
    
    # Convert dict to JSON string
    if isinstance(data, dict):
        plaintext = json.dumps(data, ensure_ascii=False).encode('utf-8')
    else:
        plaintext = data.encode('utf-8')
    
    # Generate random nonce
    nonce = os.urandom(NONCE_LENGTH)
    
    # Encrypt (includes authentication tag)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    
    # Combine nonce + ciphertext for storage
    encrypted = nonce + ciphertext
    
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt(ciphertext_b64: str) -> Union[dict, str]:
    """
    Decrypt data encrypted with encrypt().
    
    Args:
        ciphertext_b64: Base64-encoded ciphertext
        
    Returns:
        Original dict or string
    """
    if not ciphertext_b64:
        return None
    
    key = _get_encryption_key()
    aesgcm = AESGCM(key)
    
    try:
        encrypted = base64.b64decode(ciphertext_b64)
        
        # Extract nonce and ciphertext
        nonce = encrypted[:NONCE_LENGTH]
        ciphertext = encrypted[NONCE_LENGTH:]
        
        # Decrypt
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        plaintext_str = plaintext.decode('utf-8')
        
        # Try to parse as JSON
        try:
            return json.loads(plaintext_str)
        except json.JSONDecodeError:
            return plaintext_str
            
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise EncryptionError(f"Decryption failed: {e}")


def encrypt_sensitive_fields(data: dict, sensitive_keys: list) -> dict:
    """
    Encrypt only specific fields in a dict.
    
    Args:
        data: Input dictionary
        sensitive_keys: List of keys to encrypt (e.g., ["aadhaar_number", "pan_number"])
        
    Returns:
        Dictionary with sensitive fields encrypted
    """
    if not data:
        return data
    
    result = data.copy()
    
    for key in sensitive_keys:
        if key in result and result[key]:
            # Store encrypted value with marker
            result[key] = {
                "_encrypted": True,
                "_value": encrypt(str(result[key]))
            }
    
    return result


def decrypt_sensitive_fields(data: dict) -> dict:
    """
    Decrypt fields that were encrypted with encrypt_sensitive_fields().
    """
    if not data:
        return data
    
    result = data.copy()
    
    for key, value in result.items():
        if isinstance(value, dict) and value.get("_encrypted"):
            result[key] = decrypt(value["_value"])
    
    return result


def is_encryption_configured() -> bool:
    """Check if encryption key is configured."""
    return bool(os.getenv("DATA_ENCRYPTION_KEY"))


# Sensitive field keys that should be encrypted in input_data
SENSITIVE_INPUT_FIELDS = [
    "aadhaar_number",
    "pan_number", 
    "uan_number",
    "aadhaar_number_masked",  # Even masked version for extra safety
]

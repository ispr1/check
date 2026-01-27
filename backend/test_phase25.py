"""Quick test for Phase 2.5 encryption"""
import os
import base64
# Generate proper 32-byte key
key = base64.b64encode(os.urandom(32)).decode('utf-8')
os.environ["DATA_ENCRYPTION_KEY"] = key
print(f"Using key: {key[:20]}...")

from src.utils.crypto import encrypt, decrypt

# Test basic encryption
data = {"aadhaar": "234567891234", "name": "Rajesh Kumar"}
encrypted = encrypt(data)
print(f"✅ Encrypted: {encrypted[:50]}...")
decrypted = decrypt(encrypted)
print(f"✅ Decrypted: {decrypted}")

# Test field-level encryption
from src.utils.crypto import encrypt_sensitive_fields, decrypt_sensitive_fields

input_data = {
    "aadhaar_number": "234567891234",
    "pan_number": "ABCDE1234F",
    "phone": "9876543210"  # Not sensitive
}
encrypted_fields = encrypt_sensitive_fields(input_data, ["aadhaar_number", "pan_number"])
print(f"✅ Sensitive fields encrypted")
print(f"   Phone visible: {encrypted_fields['phone']}")
print(f"   Aadhaar encrypted: {encrypted_fields['aadhaar_number']['_encrypted']}")

# Test mapper
from src.utils.mapper import to_external_status, format_comparison_for_hr
print(f"✅ VERIFIED → {to_external_status('VERIFIED')}")
print(f"✅ PARTIAL → {to_external_status('PARTIAL')}")
print(f"✅ FAILED → {to_external_status('FAILED')}")

# Test audit
from src.utils.audit import log_verification_action, AuditAction
entry = log_verification_action(1, "AADHAAR", AuditAction.VERIFIED, details={"score": 95})
print(f"✅ Audit entry: {entry}")

print("\n✅ Phase 2.5 encryption tests passed!")

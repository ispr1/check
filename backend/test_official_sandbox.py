"""Test Surepass sandbox with CORRECT URL from docs: sandbox.surepass.io"""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SUREPASS_API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# From OFFICIAL DOCS: https://sandbox.surepass.io/api/v1
base_url = "https://sandbox.surepass.io/api/v1"

print("=" * 60)
print("  Testing OFFICIAL Sandbox URL from Docs")
print("=" * 60)
print(f"\nBase URL: {base_url}")
print(f"API Key: {API_KEY[:30]}...")

# Test PAN
pan_payload = {"id_number": "AMXPI3907M"}
pan_url = f"{base_url}/identity/pan-comprehensive"
print(f"\n[1] PAN Comprehensive: {pan_url}")
print(f"    Payload: {pan_payload}")

try:
    with httpx.Client(timeout=30.0) as client:
        r = client.post(pan_url, headers=headers, json=pan_payload)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        import json
        print(f"    SUCCESS! {json.dumps(r.json(), indent=2)[:500]}")
    else:
        print(f"    Response: {r.text[:300]}")
except Exception as e:
    print(f"    ERROR: {e}")

# Test Aadhaar OTP Generate
aadhaar_payload = {"id_number": "726944944577"}
aadhaar_url = f"{base_url}/aadhaar-v2/generate-otp"
print(f"\n[2] Aadhaar OTP Generate: {aadhaar_url}")
print(f"    Payload: {aadhaar_payload}")

try:
    with httpx.Client(timeout=30.0) as client:
        r = client.post(aadhaar_url, headers=headers, json=aadhaar_payload)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        import json
        print(f"    SUCCESS! {json.dumps(r.json(), indent=2)[:500]}")
    else:
        print(f"    Response: {r.text[:300]}")
except Exception as e:
    print(f"    ERROR: {e}")

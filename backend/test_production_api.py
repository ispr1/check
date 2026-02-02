"""Test Surepass PRODUCTION API (kyc-api.surepass.io)."""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SUREPASS_API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# From the docs: Production = https://kyc-api.surepass.io/api/v1
base_url = "https://kyc-api.surepass.io/api/v1"

# Test PAN with real PAN number
payload = {"id_number": "AMXPI3907M"}

print("=" * 60)
print("  Testing PRODUCTION Surepass API")
print("=" * 60)
print(f"\nBase URL: {base_url}")
print(f"API Key: {API_KEY[:30]}...")
print(f"Payload: {payload}")

url = f"{base_url}/identity/pan-comprehensive"
print(f"\n[>] Calling: {url}")

try:
    with httpx.Client(timeout=30.0) as client:
        r = client.post(url, headers=headers, json=payload)
    
    print(f"[<] Status: {r.status_code}")
    print(f"[<] Headers: {dict(r.headers)}")
    
    if r.status_code == 200:
        import json
        data = r.json()
        print("\n[SUCCESS] Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"\n[RESPONSE] {r.text[:500]}")
        
except Exception as e:
    print(f"[ERROR] {e}")

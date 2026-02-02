"""Test PAN with different field names and endpoint paths."""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SUREPASS_API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Test both field names
payloads = [
    {"id_number": "AMXPI3907M"},
    {"pan_number": "AMXPI3907M"},
]

# Possible endpoint paths based on Surepass patterns
endpoints = [
    "/identity/pan-comprehensive",
    "/corporate/pan-comprehensive", 
    "/pan/comprehensive",
    "/pan-comprehensive",
    "/pan/verify",
    "/pan-verification",
    "/identity/pan",
]

base_urls = [
    "https://kyc-api.surepass.io/api/v1",
    "https://sandbox.surepass.app/api/v1",
]

print("=" * 60)
print("  Testing PAN Endpoints with Both Field Names")
print("=" * 60)

with httpx.Client(timeout=30.0) as client:
    for base_url in base_urls:
        print(f"\n--- Base: {base_url} ---")
        for endpoint in endpoints:
            for payload in payloads:
                url = f"{base_url}{endpoint}"
                try:
                    r = client.post(url, headers=headers, json=payload)
                    field = list(payload.keys())[0]
                    if r.status_code != 404:
                        print(f"{r.status_code}: {endpoint} [{field}]")
                        if r.status_code == 200:
                            print(f"  SUCCESS! {r.text[:200]}")
                        elif r.status_code in [400, 401, 403, 422]:
                            print(f"  Response: {r.text[:200]}")
                except Exception as e:
                    pass

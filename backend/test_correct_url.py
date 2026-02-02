"""Test sandbox base URL WITHOUT /api/v1 as user specified."""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SUREPASS_API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
payload = {"id_number": "AMXPI3907M"}

# User clarified: Base URL is https://sandbox.surepass.app (no /api/v1)
base_urls = [
    "https://sandbox.surepass.app",  # User specified
    "https://sandbox.surepass.app/api/v1",  # What we had
]

endpoints = [
    "/identity/pan-comprehensive",
    "/api/v1/identity/pan-comprehensive",  # Full path under base
    "/identity/pan",
    "/pan-comprehensive",
    "/api/pan-comprehensive",
]

print("=" * 60)
print("  Testing with User-Specified Base URL")
print("=" * 60)

with httpx.Client(timeout=30.0) as client:
    for base in base_urls:
        print(f"\n--- Base: {base} ---")
        for endpoint in endpoints:
            url = f"{base}{endpoint}"
            try:
                r = client.post(url, headers=headers, json=payload)
                if r.status_code != 404:
                    print(f"{r.status_code}: {url}")
                    print(f"  Response: {r.text[:300]}")
                else:
                    print(f"404: {url}")
            except Exception as e:
                print(f"ERR: {url} - {e}")

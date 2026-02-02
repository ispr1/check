"""Test more Surepass sandbox URL variants based on email info."""
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

# From email: Console Dashboard URL: https://console.surepass.app/
# API Dashboard for PAN: identity/pan-comprehensive(https://console.surepass.app/product/console/api/pan-comprehensive)
# This suggests the path might just be "pan-comprehensive" not "identity/pan-comprehensive"

urls = [
    # Try without "identity/" prefix
    "https://sandbox.surepass.app/api/v1/pan-comprehensive",
    "https://sandbox.surepass.io/api/v1/pan-comprehensive",
    # Try different path structures
    "https://sandbox.surepass.app/api/v1/pan/comprehensive",
    "https://sandbox.surepass.io/api/v1/pan/comprehensive",
    # Try verify prefix
    "https://sandbox.surepass.app/api/v1/verify/pan-comprehensive",
    # Try v2
    "https://sandbox.surepass.app/api/v2/identity/pan-comprehensive",
]

print("Testing URL variants...")
print(f"API Key: {API_KEY[:30]}...")
print()

with httpx.Client(timeout=30.0) as client:
    for url in urls:
        try:
            r = client.post(url, headers=headers, json=payload)
            print(f"{r.status_code}: {url}")
            if r.status_code == 200:
                print(f"  SUCCESS! Response: {r.text[:300]}")
            elif r.status_code != 404:
                print(f"  Response: {r.text[:200]}")
        except Exception as e:
            print(f"ERROR: {url} - {e}")

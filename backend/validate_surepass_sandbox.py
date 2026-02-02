"""
Surepass Sandbox Validation Script (Phase 2)
Focus: Aadhaar OTP + PAN Comprehensive

Subject: Siva Prasad Reddy Iragamreddy
"""

import os
import json
import logging
import httpx
from datetime import datetime
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SurepassValidation")

load_dotenv()

# Config
BASE_URL = os.getenv("SUREPASS_BASE_URL", "https://sandbox.surepass.io/api/v1").rstrip("/")
API_KEY = os.getenv("SUREPASS_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Test Subject
SUBJECT = {
    "name": "Iragamreddy Siva Prasad Reddy",
    "dob": "28-Aug-2002",
    "normalized_dob": "2002-08-28",
    "aadhaar": "726944944577",
    "pan": "AMXPI3907M"
}

def normalize_name(name: str) -> str:
    """
    Normalization logic:
    1. Lowercase
    2. Remove all spaces
    3. Remove non-alphabetic characters
    """
    if not name:
        return ""
    name = name.lower()
    # Remove everything except a-z
    cleaned = "".join([c for c in name if 'a' <= c <= 'z'])
    return cleaned

def mask_id(id_val: str, prefix_len=0, suffix_len=4) -> str:
    if not id_val: return "N/A"
    return id_val[:prefix_len] + "X" * (len(id_val) - prefix_len - suffix_len) + id_val[-suffix_len:]

class SandboxValidator:
    def __init__(self):
        self.payload_log = {}

    def log_payload(self, step: str, url: str, request: dict, response: dict, status: int):
        self.payload_log[step] = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "request_masked": self._mask_payload(request),
            "response_status": status,
            "response": response
        }

    def _mask_payload(self, payload: dict) -> dict:
        masked = payload.copy()
        if "id_number" in masked:
            masked["id_number"] = mask_id(masked["id_number"])
        if "pan_number" in masked:
            masked["pan_number"] = mask_id(masked["pan_number"])
        if "otp" in masked:
            masked["otp"] = "XXXXXX"
        return masked

    async def generate_aadhaar_otp(self):
        url = f"{BASE_URL}/aadhaar-v2/generate-otp"
        payload = {"id_number": SUBJECT["aadhaar"]}
        
        logger.info(f"Generating Aadhaar OTP for {mask_id(SUBJECT['aadhaar'])}...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                r = await client.post(url, headers=HEADERS, json=payload)
                resp_json = r.json()
                self.log_payload("aadhaar_generate", url, payload, resp_json, r.status_code)
                
                if r.status_code == 200 and resp_json.get("success"):
                    logger.info("OTP generated successfully.")
                    return resp_json["data"].get("client_id")
                else:
                    logger.error(f"Failed to generate OTP: {resp_json.get('message')}")
                    return None
            except Exception as e:
                logger.error(f"Error calling Aadhaar API: {e}")
                return None

    async def submit_aadhaar_otp(self, client_id: str, otp: str):
        url = f"{BASE_URL}/aadhaar-v2/submit-otp"
        payload = {"client_id": client_id, "otp": otp}
        
        logger.info(f"Submitting OTP for client_id {client_id}...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                r = await client.post(url, headers=HEADERS, json=payload)
                resp_json = r.json()
                self.log_payload("aadhaar_submit", url, payload, resp_json, r.status_code)
                
                if r.status_code == 200 and resp_json.get("success"):
                    logger.info("Aadhaar verified successfully.")
                    return resp_json["data"]
                else:
                    logger.error(f"Failed to verify Aadhaar: {resp_json.get('message')}")
                    return None
            except Exception as e:
                logger.error(f"Error submitting OTP: {e}")
                return None

    async def verify_pan(self):
        base_urls = ["https://sandbox.surepass.app/api/v1", "https://sandbox.surepass.io/api/v1"]
        endpoints = [
            "identity/pan-comprehensive",
            "pan-comprehensive",
            "identity/pan"
        ]
        payloads = [
            {"pan_number": SUBJECT["pan"]},
            {"id_number": SUBJECT["pan"]}
        ]
        
        for base in base_urls:
            for ep in endpoints:
                for payload in payloads:
                    url = f"{base}/{ep}"
                    logger.info(f"Testing PAN URL: {url} with {payload}...")
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        try:
                            r = await client.post(url, headers=HEADERS, json=payload)
                            resp_json = r.json()
                            logger.info(f"Result: {r.status_code} - {resp_json.get('message', 'No message')}")
                            if r.status_code == 200 and resp_json.get("success"):
                                self.log_payload("pan_verification_success", url, payload, resp_json, r.status_code)
                                return resp_json["data"]
                        except Exception as e:
                            logger.error(f"Error for {url}: {e}")
        return None

    async def verify_uan(self):
        # We'll use the UAN number from a placeholder if not set, or skip if not needed
        # But let's check if the endpoint itself gives 401 or 404
        url = "https://sandbox.surepass.app/api/v1/employment/employment-history-uan-v2"
        payload = {"uan_number": "123456789012"} # Placeholder
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                r = await client.post(url, headers=HEADERS, json=payload)
                logger.info(f"UAN Check ({url}): {r.status_code} - {r.text[:100]}")
            except Exception as e:
                logger.error(f"UAN Error: {e}")

    def capture_report(self):
        with open("val_payloads.json", "w") as f:
            json.dump(self.payload_log, f, indent=2)
        logger.info("Payloads captured to val_payloads.json")

async def main():
    validator = SandboxValidator()
    
    # Try PAN first since it's confirmed granted
    print("\n--- Testing PAN Comprehensive ---")
    pan_data = await validator.verify_pan()
    
    if pan_data:
        print(f"PAN Result: VERIFIED")
        print(f"Name on PAN: {pan_data.get('full_name')}")
    else:
        print(f"PAN Verification Failed")

    print("\n--- Testing UAN Endpoint ---")
    await validator.verify_uan()

    # Try Aadhaar last
    print("\n--- Testing Aadhaar OTP ---")
    client_id = await validator.generate_aadhaar_otp()
    if not client_id:
        print("Aadhaar OTP Generation Failed (Likely access not granted)")
    else:
        print(f"Aadhaar OTP sent! Client ID: {client_id}")
    
    validator.capture_report()
    
    # Print the last response for clarity
    if "pan_verification" in validator.payload_log:
        p = validator.payload_log["pan_verification"]
        print(f"\nPAN Response ({p['response_status']}):")
        print(json.dumps(p['response'], indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

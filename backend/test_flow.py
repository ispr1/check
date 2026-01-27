"""Quick targeted test of complete verification flow."""
import requests
import time
import os
import base64

# Set encryption key
os.environ["DATA_ENCRYPTION_KEY"] = base64.b64encode(os.urandom(32)).decode()

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 50)
print("TARGETED VERIFICATION FLOW TEST")
print("=" * 50)

# 1. Login
print("\n1. Logging in...")
r = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@check360.com", 
    "password": "admin123"
})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("   [OK] Login OK")

# 2. Create candidate
print("\n2. Creating candidate...")
email = f"flow_test_{int(time.time())}@test.com"
r = requests.post(f"{BASE_URL}/candidates", headers=headers, json={
    "full_name": "Flow Test User",
    "dob": "1990-05-15",
    "email": email
})
candidate_id = r.json()["id"]
print(f"   [OK] Candidate ID: {candidate_id}")

# 3. Start verification (no optional steps)
print("\n3. Starting verification...")
r = requests.post(f"{BASE_URL}/verifications/start", headers=headers, json={
    "candidate_id": candidate_id,
    "include_uan": False,  # Skip optional
    "include_education": False,
    "include_experience": False
})
v = r.json()
vtoken = v["token"]
print(f"   [OK] Token: {vtoken[:30]}...")
print(f"   Steps: {[s['step_type'] for s in v['steps']]}")

# 4. Submit each mandatory step
print("\n4. Submitting mandatory steps...")

# 4a. Personal Info
r = requests.post(f"{BASE_URL}/verify/{vtoken}/personal-info", json={
    "phone": "9876543210",
    "current_address": "123 Test Street"
})
print(f"   4a. Personal Info: {r.status_code} - {r.json().get('status', 'ERROR')}")

# 4b. Face
r = requests.post(f"{BASE_URL}/verify/{vtoken}/face", json={
    "selfie_image_base64": "base64_image_data_here"
})
print(f"   4b. Face: {r.status_code} - {r.json().get('status', 'ERROR')}")

# 4c. Aadhaar OTP
r = requests.post(f"{BASE_URL}/verify/{vtoken}/aadhaar/generate-otp", json={
    "aadhaar_number": "234567891234"
})
client_id = r.json().get("client_id", "")
print(f"   4c. Aadhaar OTP Gen: {r.status_code} - client_id: {client_id[:20]}...")

r = requests.post(f"{BASE_URL}/verify/{vtoken}/aadhaar/submit-otp", json={
    "client_id": client_id,
    "otp": "123456"
})
print(f"   4c. Aadhaar OTP Submit: {r.status_code}")
if r.status_code == 200:
    print(f"       Result: {r.json().get('verification_result', {}).get('status')}")

# 4d. PAN
r = requests.post(f"{BASE_URL}/verify/{vtoken}/pan", json={
    "pan_number": "ABCDE1234F"
})
print(f"   4d. PAN: {r.status_code}")
if r.status_code == 200:
    print(f"       Result: {r.json().get('verification_result', {}).get('status')}")

# 5. Check session status
print("\n5. Checking session...")
r = requests.get(f"{BASE_URL}/verify/{vtoken}")
session = r.json()
print(f"   Verification Status: {session['status']}")
for s in session["steps"]:
    marker = "[OK]" if s["status"] == "COMPLETED" else "[FAIL]"
    print(f"   {marker} {s['step_type']}: {s['status']} (mandatory: {s['is_mandatory']})")
print(f"   can_submit: {session['can_submit']}")

# 6. Submit
print("\n6. Final submission...")
if session["can_submit"]:
    r = requests.post(f"{BASE_URL}/verify/{vtoken}/submit")
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   [OK] Verification submitted: {r.json().get('status')}")
    else:
        print(f"   [FAIL] Error: {r.text[:100]}")
else:
    print("   [WARN] Cannot submit - mandatory steps incomplete")
    # Show which are missing
    for s in session["steps"]:
        if s["is_mandatory"] and s["status"] != "COMPLETED":
            print(f"      Missing: {s['step_type']}")

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)


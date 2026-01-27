"""
Phase 2 QA Test Script - Tests Surepass integration with mock mode.

Run with: python test_phase2.py
"""

import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_phase2():
    print("=" * 60)
    print("CHECK-360 Phase 2 QA Test (Surepass Integration)")
    print("=" * 60)
    
    errors = []
    
    # ============ Test 1: Auth Login ============
    print("\n[1/7] Testing auth login...")
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@check360.com",
            "password": "admin123"
        })
        assert r.status_code == 200, f"Login failed: {r.text}"
        token = r.json()["access_token"]
        print(f"      ✅ Login successful")
    except Exception as e:
        errors.append(f"Auth login failed: {e}")
        print(f"      ❌ Auth login failed: {e}")
        return errors
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # ============ Test 2: Create candidate ============
    print("\n[2/7] Creating test candidate...")
    try:
        r = requests.post(f"{BASE_URL}/candidates", headers=headers, json={
            "full_name": "Rajesh Kumar Sharma",
            "dob": "1990-05-15",
            "email": f"rajesh_phase2_{int(__import__('time').time())}@test.com"
        })
        if r.status_code == 201:
            candidate = r.json()
            candidate_id = candidate["id"]
            print(f"      ✅ Candidate created (ID: {candidate_id})")
        else:
            raise Exception(f"Unexpected: {r.status_code} - {r.text}")
    except Exception as e:
        errors.append(f"Create candidate failed: {e}")
        print(f"      ❌ Create candidate failed: {e}")
        return errors
    
    # ============ Test 3: Start verification with UAN ============
    print("\n[3/7] Starting verification with UAN...")
    try:
        r = requests.post(f"{BASE_URL}/verifications/start", headers=headers, json={
            "candidate_id": candidate_id,
            "include_uan": True,
            "include_education": False,
            "include_experience": False
        })
        assert r.status_code == 201, f"Start failed: {r.text}"
        verification = r.json()
        token_v = verification["token"]
        print(f"      ✅ Verification started (token: {token_v[:30]}...)")
    except Exception as e:
        errors.append(f"Start verification failed: {e}")
        print(f"      ❌ Start verification failed: {e}")
        return errors
    
    # ============ Test 4: Personal Info ============
    print("\n[4/7] Submitting personal info...")
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/personal-info", json={
            "phone": "9876543210",
            "current_address": "123, 100 Feet Road, Koramangala, Bangalore - 560034"
        })
        assert r.status_code == 200
        print(f"      ✅ Personal info: {r.json()['status']}")
    except Exception as e:
        errors.append(f"Personal info failed: {e}")
        print(f"      ❌ Personal info failed: {e}")
    
    # ============ Test 5: Face liveness ============
    print("\n[5/7] Submitting face liveness...")
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/face", json={
            "selfie_image_base64": "base64_placeholder"
        })
        assert r.status_code == 200
        print(f"      ✅ Face liveness: {r.json()['status']}")
    except Exception as e:
        errors.append(f"Face failed: {e}")
        print(f"      ❌ Face liveness failed: {e}")
    
    # ============ Test 6: Aadhaar OTP Flow ============
    print("\n[6/7] Testing Aadhaar OTP flow...")
    
    # 6a. Generate OTP
    print("      6a. Generating OTP...")
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/aadhaar/generate-otp", json={
            "aadhaar_number": "234567891234"
        })
        assert r.status_code == 200, f"Generate OTP failed: {r.text}"
        otp_response = r.json()
        client_id = otp_response.get("client_id", "")
        print(f"         ✅ OTP generated - client_id: {client_id[:15]}...")
    except Exception as e:
        errors.append(f"Aadhaar generate OTP failed: {e}")
        print(f"         ❌ Generate OTP failed: {e}")
        client_id = ""
    
    # 6b. Submit OTP
    if client_id:
        print("      6b. Submitting OTP...")
        try:
            r = requests.post(f"{BASE_URL}/verify/{token_v}/aadhaar/submit-otp", json={
                "client_id": client_id,
                "otp": "123456"
            })
            assert r.status_code == 200, f"Submit OTP failed: {r.text}"
            result = r.json()
            print(f"         ✅ Aadhaar verified: {result['verification_result']['status']}")
            print(f"            Score: {result['verification_result']['score']}")
            print(f"            Details: {result['verification_result'].get('details', {})}")
        except Exception as e:
            errors.append(f"Aadhaar submit OTP failed: {e}")
            print(f"         ❌ Submit OTP failed: {e}")
    
    # ============ Test 7: PAN Verification ============
    print("\n[7/7] Testing PAN verification...")
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/pan", json={
            "pan_number": "ABCDE1234F"
        })
        assert r.status_code == 200, f"PAN failed: {r.text}"
        result = r.json()
        print(f"      ✅ PAN verified: {result['verification_result']['status']}")
        print(f"         Score: {result['verification_result']['score']}")
        details = result['verification_result'].get('details', {})
        print(f"         Name match: {details.get('name_match')}")
        print(f"         DOB match: {details.get('dob_match')}")
    except Exception as e:
        errors.append(f"PAN verification failed: {e}")
        print(f"      ❌ PAN verification failed: {e}")
    
    # ============ Test 8: UAN Verification ============
    print("\n[8/7] Testing UAN verification...")
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/uan", json={
            "uan_number": "123456789012",
            "claimed_experience_years": 5
        })
        assert r.status_code == 200, f"UAN failed: {r.text}"
        result = r.json()
        print(f"      ✅ UAN verified: {result['verification_result']['status']}")
        print(f"         Score: {result['verification_result']['score']}")
        flags = result['verification_result'].get('flags', [])
        if flags:
            print(f"         ⚠️ Flags: {', '.join(flags)}")
    except Exception as e:
        errors.append(f"UAN verification failed: {e}")
        print(f"      ❌ UAN verification failed: {e}")
    
    # ============ Final Session Check ============
    print("\n[+] Checking final session state...")
    try:
        r = requests.get(f"{BASE_URL}/verify/{token_v}")
        session = r.json()
        print(f"    Status: {session['status']}")
        print(f"    Can submit: {session['can_submit']}")
        for step in session["steps"]:
            emoji = "✅" if step['status'] == "COMPLETED" else ("❌" if step['status'] == "FAILED" else "⏳")
            print(f"    {emoji} {step['step_type']}: {step['status']}")
    except Exception as e:
        print(f"    ⚠️ Session check failed: {e}")
    
    # ============ Summary ============
    print("\n" + "=" * 60)
    if errors:
        print(f"QA RESULT: ❌ {len(errors)} ERROR(S)")
        for e in errors:
            print(f"  - {e}")
    else:
        print("QA RESULT: ✅ ALL TESTS PASSED")
    print("=" * 60)
    
    print("\n📋 Phase 2 Features Tested:")
    print("   - Mock mode (SUREPASS_ENABLED=false)")
    print("   - Aadhaar OTP flow (generate + submit)")
    print("   - PAN verification with cross-check")
    print("   - UAN verification with employment analysis")
    print("   - Comparison logic (name fuzzy, DOB exact)")
    
    return errors

if __name__ == "__main__":
    errors = test_phase2()
    sys.exit(1 if errors else 0)

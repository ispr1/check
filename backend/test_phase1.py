"""
Phase 1 QA Test Script - Tests the full verification flow.

Run with: python test_phase1.py
"""

import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_phase1():
    print("=" * 60)
    print("CHECK-360 Phase 1 QA Test")
    print("=" * 60)
    
    errors = []
    
    # ============ Test 1: Health Check ============
    print("\n[1/8] Testing health endpoint...")
    try:
        r = requests.get("http://localhost:8000/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"
        print("      ✅ Health check passed")
    except Exception as e:
        errors.append(f"Health check failed: {e}")
        print(f"      ❌ Health check failed: {e}")
    
    # ============ Test 2: Auth Login ============
    print("\n[2/8] Testing auth login...")
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@check360.com",
            "password": "admin123"
        })
        assert r.status_code == 200, f"Login failed: {r.text}"
        token = r.json()["access_token"]
        print(f"      ✅ Login successful (token: {token[:20]}...)")
    except Exception as e:
        errors.append(f"Auth login failed: {e}")
        print(f"      ❌ Auth login failed: {e}")
        return errors  # Can't continue without token
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # ============ Test 3: Get Current User ============
    print("\n[3/8] Testing get current user...")
    try:
        r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        assert r.status_code == 200
        user = r.json()
        print(f"      ✅ Current user: {user['email']} (role: {user['role']})")
    except Exception as e:
        errors.append(f"Get user failed: {e}")
        print(f"      ❌ Get user failed: {e}")
    
    # ============ Test 4: Create Candidate ============
    print("\n[4/8] Testing create candidate...")
    try:
        r = requests.post(f"{BASE_URL}/candidates", headers=headers, json={
            "full_name": "QA Test Candidate",
            "dob": "1990-05-15",
            "email": f"qa_test_{int(__import__('time').time())}@test.com"
        })
        if r.status_code == 201:
            candidate = r.json()
            candidate_id = candidate["id"]
            print(f"      ✅ Candidate created (ID: {candidate_id})")
        elif r.status_code == 409:
            # Already exists, get from list
            r = requests.get(f"{BASE_URL}/candidates", headers=headers)
            candidates = r.json()
            candidate_id = candidates[0]["id"] if candidates else None
            print(f"      ⚠️ Using existing candidate (ID: {candidate_id})")
        else:
            raise Exception(f"Unexpected status: {r.status_code} - {r.text}")
    except Exception as e:
        errors.append(f"Create candidate failed: {e}")
        print(f"      ❌ Create candidate failed: {e}")
        return errors
    
    # ============ Test 5: Start Verification ============
    print("\n[5/8] Testing start verification...")
    try:
        r = requests.post(f"{BASE_URL}/verifications/start", headers=headers, json={
            "candidate_id": candidate_id,
            "include_uan": False,
            "include_education": True,
            "include_experience": False
        })
        if r.status_code == 201:
            verification = r.json()
            token_v = verification["token"]
            print(f"      ✅ Verification started")
            print(f"         Token: {token_v[:30]}...")
            print(f"         Status: {verification['status']}")
            print(f"         Steps: {len(verification['steps'])}")
        elif r.status_code == 409:
            print(f"      ⚠️ Existing verification found - {r.json()['detail']}")
            # Get existing verification
            r = requests.get(f"{BASE_URL}/verifications", headers=headers)
            verifications = r.json()
            for v in verifications:
                if v["candidate_id"] == candidate_id:
                    token_v = None  # Will fetch from details
                    verification_id = v["id"]
                    r = requests.get(f"{BASE_URL}/verifications/{verification_id}", headers=headers)
                    verification = r.json()
                    token_v = verification["token"]
                    print(f"         Using existing token: {token_v[:30]}...")
                    break
        else:
            raise Exception(f"Unexpected: {r.status_code} - {r.text}")
    except Exception as e:
        errors.append(f"Start verification failed: {e}")
        print(f"      ❌ Start verification failed: {e}")
        return errors
    
    # ============ Test 6: Candidate Access Session ============
    print("\n[6/8] Testing candidate session access...")
    try:
        r = requests.get(f"{BASE_URL}/verify/{token_v}")
        assert r.status_code == 200, f"Session access failed: {r.text}"
        session = r.json()
        print(f"      ✅ Session accessed")
        print(f"         Status: {session['status']}")
        print(f"         Can submit: {session['can_submit']}")
        print(f"         Next step: {session.get('next_step')}")
        for step in session["steps"]:
            print(f"         - {step['step_type']}: {step['status']} (mandatory: {step['is_mandatory']})")
    except Exception as e:
        errors.append(f"Session access failed: {e}")
        print(f"      ❌ Session access failed: {e}")
    
    # ============ Test 7: Submit Steps ============
    print("\n[7/8] Testing step submissions...")
    
    # Personal Info
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/personal-info", json={
            "phone": "9876543210",
            "current_address": "123 Test Street, Bangalore, Karnataka 560001"
        })
        assert r.status_code == 200, f"Personal info failed: {r.text}"
        print(f"      ✅ Personal info: {r.json()['status']}")
    except Exception as e:
        errors.append(f"Personal info failed: {e}")
        print(f"      ❌ Personal info failed: {e}")
    
    # Face liveness
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/face", json={
            "selfie_image_base64": "base64_placeholder_for_phase1"
        })
        assert r.status_code == 200, f"Face failed: {r.text}"
        print(f"      ✅ Face liveness: {r.json()['status']}")
    except Exception as e:
        errors.append(f"Face failed: {e}")
        print(f"      ❌ Face liveness failed: {e}")
    
    # Aadhaar
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/aadhaar", json={
            "aadhaar_number": "123456789012"
        })
        assert r.status_code == 200, f"Aadhaar failed: {r.text}"
        print(f"      ✅ Aadhaar: {r.json()['status']}")
    except Exception as e:
        errors.append(f"Aadhaar failed: {e}")
        print(f"      ❌ Aadhaar failed: {e}")
    
    # PAN
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/pan", json={
            "pan_number": "ABCDE1234F"
        })
        assert r.status_code == 200, f"PAN failed: {r.text}"
        print(f"      ✅ PAN: {r.json()['status']}")
    except Exception as e:
        errors.append(f"PAN failed: {e}")
        print(f"      ❌ PAN failed: {e}")
    
    # Skip education (conditional)
    try:
        r = requests.post(f"{BASE_URL}/verify/{token_v}/skip/EDUCATION")
        if r.status_code == 200:
            print(f"      ✅ Education skipped: {r.json()['status']}")
        elif r.status_code == 404:
            print(f"      ⚠️ Education step not present (OK)")
    except Exception as e:
        print(f"      ⚠️ Education skip: {e}")
    
    # ============ Test 8: Final Submission ============
    print("\n[8/8] Testing final submission...")
    try:
        # Check session first
        r = requests.get(f"{BASE_URL}/verify/{token_v}")
        session = r.json()
        print(f"      Pre-submit status: {session['status']}")
        print(f"      Can submit: {session['can_submit']}")
        
        if session["can_submit"]:
            r = requests.post(f"{BASE_URL}/verify/{token_v}/submit")
            if r.status_code == 200:
                result = r.json()
                print(f"      ✅ SUBMITTED: {result['status']}")
                print(f"         Message: {result['message']}")
            else:
                print(f"      ❌ Submit failed: {r.status_code} - {r.text}")
                errors.append(f"Submit failed: {r.text}")
        else:
            # Check which steps are incomplete
            incomplete = [s for s in session["steps"] if s["is_mandatory"] and s["status"] == "PENDING"]
            print(f"      ⚠️ Cannot submit - incomplete mandatory steps: {[s['step_type'] for s in incomplete]}")
    except Exception as e:
        errors.append(f"Final submit failed: {e}")
        print(f"      ❌ Final submit failed: {e}")
    
    # ============ Summary ============
    print("\n" + "=" * 60)
    if errors:
        print(f"QA RESULT: ❌ {len(errors)} ERROR(S)")
        for e in errors:
            print(f"  - {e}")
    else:
        print("QA RESULT: ✅ ALL TESTS PASSED")
    print("=" * 60)
    
    return errors

if __name__ == "__main__":
    errors = test_phase1()
    sys.exit(1 if errors else 0)

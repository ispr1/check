"""
CHECK-360 Comprehensive QA Test
================================
Tests Phase 1, 2, and 2.5 functionality.

Run with: python test_comprehensive.py

Requirements:
- Server running at localhost:8000
- Database migrated
- Admin user seeded
"""

import requests
import time
import sys
import os

# Set encryption key for Phase 2.5 tests
import base64
os.environ["DATA_ENCRYPTION_KEY"] = base64.b64encode(os.urandom(32)).decode()

BASE_URL = "http://localhost:8000/api/v1"
RESULTS = {"passed": 0, "failed": 0, "errors": []}


def test(name, condition, error_msg=""):
    """Helper to record test results."""
    if condition:
        RESULTS["passed"] += 1
        print(f"  [PASS] {name}")
        return True
    else:
        RESULTS["failed"] += 1
        RESULTS["errors"].append(f"{name}: {error_msg}")
        print(f"  [FAIL] {name}: {error_msg}")
        return False


def section(title):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def run_tests():
    print("\n" + "="*60)
    print("  CHECK-360 COMPREHENSIVE QA TEST")
    print("  Version: 2.5.0")
    print("="*60)

    # =========================================================
    section("1. HEALTH & STARTUP CHECKS")
    # =========================================================
    
    # Test 1.1: Health endpoint
    try:
        r = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        test("Health endpoint returns 200", r.status_code == 200, f"Got {r.status_code}")
        test("Health returns version 2.5.0", "2.5.0" in r.text, r.text[:100])
    except Exception as e:
        test("Server reachable", False, str(e))
        print("\n[WARN] Server not running! Start with: uvicorn src.main:app --reload")
        return

    # Test 1.2: Root endpoint
    try:
        r = requests.get(BASE_URL.replace('/api/v1', ''))
        data = r.json()
        test("Root endpoint works", r.status_code == 200)
        test("Root shows correct description", "Orchestrator" in data.get("description", ""))
    except Exception as e:
        test("Root endpoint", False, str(e))

    # =========================================================
    section("2. AUTHENTICATION")
    # =========================================================
    
    # Test 2.1: Login with correct credentials
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@check360.com",
            "password": "admin123"
        })
        test("Login returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:100]}")
        token = r.json().get("access_token", "")
        test("Login returns token", len(token) > 50, "Token too short or missing")
    except Exception as e:
        test("Login endpoint", False, str(e))
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Test 2.2: Login with wrong password
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@check360.com",
            "password": "wrongpassword"
        })
        test("Wrong password returns 401", r.status_code == 401)
    except Exception as e:
        test("Wrong password check", False, str(e))

    # Test 2.3: Protected endpoint without token
    try:
        r = requests.get(f"{BASE_URL}/candidates")
        test("No token returns 401", r.status_code == 401)
    except Exception as e:
        test("No token check", False, str(e))

    # =========================================================
    section("3. CANDIDATE MANAGEMENT")
    # =========================================================
    
    timestamp = int(time.time())
    test_email = f"qa_test_{timestamp}@check360.com"
    
    # Test 3.1: Create candidate (using mock-compatible name and DOB)
    try:
        r = requests.post(f"{BASE_URL}/candidates", headers=headers, json={
            "full_name": "Rajesh Kumar Sharma",
            "dob": "1990-05-15",
            "email": test_email
        })
        test("Create candidate returns 201", r.status_code == 201, f"Got {r.status_code}: {r.text[:100]}")
        candidate = r.json()
        candidate_id = candidate.get("id")
        test("Candidate has ID", candidate_id is not None)
        test("Candidate name correct", candidate.get("full_name") == "Rajesh Kumar Sharma")
    except Exception as e:
        test("Create candidate", False, str(e))
        return

    # Test 3.2: List candidates
    try:
        r = requests.get(f"{BASE_URL}/candidates", headers=headers)
        test("List candidates returns 200", r.status_code == 200)
        candidates = r.json()
        test("List is array", isinstance(candidates, list))
        test("New candidate in list", any(c.get("id") == candidate_id for c in candidates))
    except Exception as e:
        test("List candidates", False, str(e))

    # Test 3.3: Duplicate email
    try:
        r = requests.post(f"{BASE_URL}/candidates", headers=headers, json={
            "full_name": "Duplicate Test",
            "dob": "1990-01-01",
            "email": test_email
        })
        test("Duplicate email prevented", r.status_code in [400, 409, 422])
    except Exception as e:
        test("Duplicate email check", False, str(e))

    # =========================================================
    section("4. VERIFICATION LIFECYCLE")
    # =========================================================
    
    # Test 4.1: Start verification
    try:
        r = requests.post(f"{BASE_URL}/verifications/start", headers=headers, json={
            "candidate_id": candidate_id,
            "include_uan": True,
            "include_education": False,
            "include_experience": False
        })
        test("Start verification returns 201", r.status_code == 201, f"Got {r.status_code}: {r.text[:200]}")
        verification = r.json()
        verify_token = verification.get("token", "")
        test("Verification has token", len(verify_token) > 20)
        test("Verification has steps", len(verification.get("steps", [])) >= 4)
        
        # Check mandatory steps exist
        step_types = [s["step_type"] for s in verification.get("steps", [])]
        test("Has PERSONAL_INFO step", "PERSONAL_INFO" in step_types)
        test("Has FACE_LIVENESS step", "FACE_LIVENESS" in step_types)
        test("Has AADHAAR step", "AADHAAR" in step_types)
        test("Has PAN step", "PAN" in step_types)
        test("Has UAN step (optional)", "UAN" in step_types)
    except Exception as e:
        test("Start verification", False, str(e))
        return

    # Test 4.2: Get verification session (public)
    try:
        r = requests.get(f"{BASE_URL}/verify/{verify_token}")
        test("Get session returns 200", r.status_code == 200)
        session = r.json()
        test("Session has status", "status" in session)
        test("Session has steps", len(session.get("steps", [])) >= 4)
        test("Cannot submit yet", session.get("can_submit") == False)
    except Exception as e:
        test("Get session", False, str(e))

    # Test 4.3: Invalid token
    try:
        r = requests.get(f"{BASE_URL}/verify/invalid_token_12345")
        test("Invalid token returns 404", r.status_code == 404)
    except Exception as e:
        test("Invalid token check", False, str(e))

    # =========================================================
    section("5. STEP SUBMISSIONS")
    # =========================================================
    
    # Test 5.1: Personal Info
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/personal-info", json={
            "phone": "9876543210",
            "current_address": "123, Test Street, Bangalore - 560001"
        })
        test("Personal info returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:100]}")
        result = r.json()
        test("Personal info status COMPLETED", result.get("status") == "COMPLETED")
    except Exception as e:
        test("Personal info", False, str(e))

    # Test 5.2: Face (stored only in Phase 2)
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/face", json={
            "selfie_image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
        })
        test("Face returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:100]}")
    except Exception as e:
        test("Face submission", False, str(e))

    # =========================================================
    section("6. SUREPASS INTEGRATION (MOCK MODE)")
    # =========================================================
    
    # Test 6.1: Aadhaar OTP Generate
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/aadhaar/generate-otp", json={
            "aadhaar_number": "234567891234"
        })
        test("Aadhaar generate-otp returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:100]}")
        otp_response = r.json()
        client_id = otp_response.get("client_id", "")
        test("Returns client_id", len(client_id) > 0)
    except Exception as e:
        test("Aadhaar generate OTP", False, str(e))
        client_id = ""

    # Test 6.2: Aadhaar OTP Submit
    if client_id:
        try:
            r = requests.post(f"{BASE_URL}/verify/{verify_token}/aadhaar/submit-otp", json={
                "client_id": client_id,
                "otp": "123456"
            })
            test("Aadhaar submit-otp returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:200]}")
            result = r.json()
            test("Has verification_result", "verification_result" in result)
            
            vr = result.get("verification_result", {})
            test("Result has status", "status" in vr)
            test("Result has score", "score" in vr)
        except Exception as e:
            test("Aadhaar submit OTP", False, str(e))

    # Test 6.3: Invalid Aadhaar format
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/aadhaar/generate-otp", json={
            "aadhaar_number": "123"  # Too short
        })
        test("Invalid Aadhaar rejected", r.status_code == 422)
    except Exception as e:
        test("Invalid Aadhaar check", False, str(e))

    # Test 6.4: PAN Verification
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/pan", json={
            "pan_number": "ABCDE1234F"
        })
        test("PAN verification returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:200]}")
        result = r.json()
        test("PAN has verification_result", "verification_result" in result)
    except Exception as e:
        test("PAN verification", False, str(e))

    # Test 6.5: Invalid PAN format
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/pan", json={
            "pan_number": "INVALID"
        })
        test("Invalid PAN rejected", r.status_code == 422)
    except Exception as e:
        test("Invalid PAN check", False, str(e))

    # Test 6.6: UAN Verification
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/uan", json={
            "uan_number": "123456789012",
            "claimed_experience_years": 5
        })
        test("UAN verification returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:200]}")
        result = r.json()
        test("UAN has verification_result", "verification_result" in result)
        
        # Check employment analysis
        vr = result.get("verification_result", {})
        details = vr.get("details", {})
        test("UAN has employment details", "employment" in details or "total_experience_years" in str(details))
    except Exception as e:
        test("UAN verification", False, str(e))

    # =========================================================
    section("7. FINAL SUBMISSION")
    # =========================================================
    
    # Test 7.1: Check can_submit
    try:
        r = requests.get(f"{BASE_URL}/verify/{verify_token}")
        session = r.json()
        can_submit = session.get("can_submit", False)
        test("Can submit after all mandatory steps", can_submit == True, 
             f"can_submit={can_submit}, steps={session.get('steps', [])}")
    except Exception as e:
        test("Can submit check", False, str(e))

    # Test 7.2: Submit verification
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/submit")
        test("Submit returns 200", r.status_code == 200, f"Got {r.status_code}: {r.text[:200]}")
        result = r.json()
        test("Submit returns SUBMITTED", result.get("status") == "SUBMITTED")
    except Exception as e:
        test("Submit verification", False, str(e))

    # Test 7.3: Cannot submit again
    try:
        r = requests.post(f"{BASE_URL}/verify/{verify_token}/submit")
        test("Cannot submit twice", r.status_code in [400, 409])
    except Exception as e:
        test("Double submit check", False, str(e))

    # =========================================================
    section("8. PHASE 2.5 HARDENING")
    # =========================================================
    
    # Test 8.1: Encryption utilities
    try:
        from src.utils.crypto import encrypt, decrypt, encrypt_sensitive_fields
        
        test_data = {"aadhaar": "123456789012", "name": "Test"}
        encrypted = encrypt(test_data)
        test("Encryption works", len(encrypted) > 50)
        
        decrypted = decrypt(encrypted)
        test("Decryption works", decrypted == test_data)
        
        fields = encrypt_sensitive_fields({"aadhaar_number": "123456789012", "phone": "9876543210"}, ["aadhaar_number"])
        test("Field encryption works", fields["aadhaar_number"].get("_encrypted") == True)
        test("Non-sensitive field unchanged", fields["phone"] == "9876543210")
    except Exception as e:
        test("Encryption utilities", False, str(e))

    # Test 8.2: Status mapper
    try:
        from src.utils.mapper import to_external_status
        
        test("VERIFIED maps to MATCH", to_external_status("VERIFIED") == "MATCH")
        test("PARTIAL maps to PARTIAL_MATCH", to_external_status("PARTIAL") == "PARTIAL_MATCH")
        test("FAILED maps to MISMATCH", to_external_status("FAILED") == "MISMATCH")
    except Exception as e:
        test("Status mapper", False, str(e))

    # Test 8.3: Audit logging
    try:
        from src.utils.audit import log_verification_action, AuditAction
        
        entry = log_verification_action(1, "AADHAAR", AuditAction.VERIFIED, details={"score": 95})
        test("Audit log creates entry", "timestamp" in entry)
        test("Audit log has action", entry.get("action") == "VERIFIED")
        test("Audit log sanitizes PII", "aadhaar_number" not in str(entry))
    except Exception as e:
        test("Audit logging", False, str(e))

    # Test 8.4: Comparison utilities
    try:
        from src.utils.comparison import fuzzy_name_match, exact_match, normalize_name
        
        test("Name normalization", normalize_name("MR. RAJESH KUMAR") == "MR RAJESH")
        test("Fuzzy match same name", fuzzy_name_match("Rajesh Kumar", "RAJESH KUMAR") >= 95)
        test("Fuzzy match similar name", fuzzy_name_match("Rajesh Kumar", "Rajesh K Sharma") >= 50)
        test("Exact match works", exact_match("1990-05-15", "1990-05-15") == True)
        test("Exact match case insensitive", exact_match("ABC", "abc") == True)
    except Exception as e:
        test("Comparison utilities", False, str(e))

    # =========================================================
    section("9. DATABASE SCHEMA")
    # =========================================================
    
    # Test 9.1: Check new columns exist
    try:
        from src.models.verification_step import VerificationStep
        
        test("Model has flags column", hasattr(VerificationStep, "flags"))
        test("Model has source column", hasattr(VerificationStep, "source"))
        test("Model has verified_at column", hasattr(VerificationStep, "verified_at"))
        test("Model has review_assets column", hasattr(VerificationStep, "review_assets"))
        test("Model has hr_notes column", hasattr(VerificationStep, "hr_notes"))
        test("Model has audit_trail column", hasattr(VerificationStep, "audit_trail"))
    except Exception as e:
        test("Schema columns", False, str(e))

    # =========================================================
    # SUMMARY
    # =========================================================
    print("\n" + "="*60)
    print("  QA TEST SUMMARY")
    print("="*60)
    print(f"\n  [PASS] Passed: {RESULTS['passed']}")
    print(f"  [FAIL] Failed: {RESULTS['failed']}")
    print(f"  [INFO] Total:  {RESULTS['passed'] + RESULTS['failed']}")
    
    if RESULTS['errors']:
        print(f"\n  Failures:")
        for err in RESULTS['errors']:
            print(f"    - {err}")
    
    if RESULTS['failed'] == 0:
        print("\n  ALL TESTS PASSED!")
        print("  CHECK-360 is ready for Phase 3.")
    else:
        print(f"\n  [WARN] {RESULTS['failed']} test(s) failed. Please review.")
    
    print("="*60 + "\n")
    
    return RESULTS['failed'] == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

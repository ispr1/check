"""
Surepass Sandbox Validation - PAN Comprehensive Test
=====================================================
Tests ONLY available APIs from sandbox grant.

Available:
- PAN Comprehensive (identity/pan-comprehensive)
- DigiLocker (identity/digilocker) 
- Employment UAN V2 (employment/employment-history-uan-v2)

NOT Available:
- Aadhaar OTP (NOT GRANTED)

Test Subject (consented):
- Name: Siva Prasad Reddy Iragamreddy
- DOB: 2002-08-28
- PAN: AMXPI3907M
"""

import os
import json
import httpx
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
BASE_URL = os.getenv("SUREPASS_BASE_URL", "https://sandbox.surepass.app/api/v1")
API_KEY = os.getenv("SUREPASS_API_KEY", "")

# Test subject data (consented)
TEST_SUBJECT = {
    "name": "Siva Prasad Reddy Iragamreddy",
    "dob": "2002-08-28",
    "pan": "AMXPI3907M"
}

# Results storage
RESULTS = {
    "pan_response": None,
    "comparisons": {},
    "findings": [],
    "errors": []
}


def mask_pan(pan: str) -> str:
    """Mask PAN for logging."""
    if len(pan) >= 10:
        return f"XXXXX{pan[5:9]}X"
    return "XXXXXXXXXX"


def normalize_name(name: str) -> str:
    """
    Normalize name for comparison.
    Removes non-alpha, converts to lowercase.
    """
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r'[^a-z]', '', name)
    return name


def normalize_name_sorted(name: str) -> str:
    """Sort characters for order-independent comparison."""
    return ''.join(sorted(normalize_name(name)))


def names_match(name1: str, name2: str) -> dict:
    """Compare two names using multiple strategies."""
    n1 = normalize_name(name1)
    n2 = normalize_name(name2)
    
    n1_sorted = normalize_name_sorted(name1)
    n2_sorted = normalize_name_sorted(name2)
    
    exact_match = n1 == n2
    sorted_match = n1_sorted == n2_sorted
    
    # Character overlap
    set1 = set(n1)
    set2 = set(n2)
    overlap = len(set1 & set2) / max(len(set1 | set2), 1) * 100
    
    return {
        "name1_raw": name1,
        "name2_raw": name2,
        "name1_normalized": n1,
        "name2_normalized": n2,
        "exact_match": exact_match,
        "sorted_match": sorted_match,
        "char_overlap_pct": round(overlap, 2),
        "verdict": "PASS" if sorted_match else ("PARTIAL" if overlap > 80 else "FAIL")
    }


def normalize_dob(dob: str) -> str:
    """Normalize DOB to YYYY-MM-DD format."""
    if not dob:
        return ""
    
    if re.match(r'^\d{4}-\d{2}-\d{2}$', dob):
        return dob
    
    # DD-MMM-YYYY
    try:
        dt = datetime.strptime(dob, "%d-%b-%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        pass
    
    # DD/MM/YYYY
    try:
        dt = datetime.strptime(dob, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        pass
    
    # DD-MM-YYYY
    try:
        dt = datetime.strptime(dob, "%d-%m-%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        pass
    
    return dob


def get_headers():
    """Get API headers."""
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def log_finding(category: str, finding: str, severity: str = "INFO"):
    RESULTS["findings"].append({
        "category": category,
        "finding": finding,
        "severity": severity
    })
    marker = {"INFO": "[i]", "WARN": "[!]", "ERROR": "[X]"}.get(severity, "[?]")
    print(f"  {marker} {finding}")


# ============================================================
# PAN COMPREHENSIVE VERIFICATION
# ============================================================

def test_pan_comprehensive():
    """Test PAN Comprehensive API."""
    section("1. PAN COMPREHENSIVE VERIFICATION")
    
    print(f"  PAN: {mask_pan(TEST_SUBJECT['pan'])}")
    print(f"  Endpoint: identity/pan-comprehensive")
    
    url = f"{BASE_URL}/identity/pan-comprehensive"
    payload = {"id_number": TEST_SUBJECT["pan"]}
    
    print(f"\n  [>] Calling API: {url}")
    print(f"  [>] Payload: {json.dumps(payload)}")
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=get_headers(), json=payload)
            
        print(f"  [<] Status: {response.status_code}")
        print(f"  [<] Headers: {dict(response.headers)}")
        
        # Try to parse response
        try:
            data = response.json()
        except:
            print(f"  [<] Raw response: {response.text[:500]}")
            RESULTS["errors"].append(f"PAN: Non-JSON response: {response.text[:200]}")
            return None
        
        # Store full response
        RESULTS["pan_response"] = {
            "status_code": response.status_code,
            "response": data
        }
        
        print(f"\n  --- RAW RESPONSE ---")
        print(json.dumps(data, indent=2))
        
        if response.status_code == 200 and data.get("success"):
            pan_data = data.get("data", data)
            
            print(f"\n  --- PAN RESPONSE ANALYSIS ---")
            print(f"  Response Keys: {list(pan_data.keys())}")
            
            # Extract fields
            pan_name = pan_data.get("full_name", pan_data.get("name", ""))
            pan_dob = pan_data.get("dob", "")
            pan_status = pan_data.get("pan_status", pan_data.get("status", ""))
            aadhaar_linked = pan_data.get("aadhaar_seeding_status", pan_data.get("aadhaar_linked", ""))
            
            print(f"\n  Extracted Fields:")
            print(f"    Name: {pan_name}")
            print(f"    DOB: {pan_dob}")
            print(f"    PAN Status: {pan_status}")
            print(f"    Aadhaar Linked: {aadhaar_linked}")
            
            # Compare with test subject
            section("1a. PAN NAME COMPARISON")
            name_result = names_match(TEST_SUBJECT["name"], pan_name)
            print(f"  User-entered: {name_result['name1_raw']}")
            print(f"  PAN returned: {name_result['name2_raw']}")
            print(f"  Normalized user: {name_result['name1_normalized']}")
            print(f"  Normalized PAN: {name_result['name2_normalized']}")
            print(f"  Exact match: {name_result['exact_match']}")
            print(f"  Sorted match: {name_result['sorted_match']}")
            print(f"  Char overlap: {name_result['char_overlap_pct']}%")
            print(f"  VERDICT: {name_result['verdict']}")
            
            RESULTS["comparisons"]["pan_name"] = name_result
            
            # DOB comparison
            section("1b. PAN DOB COMPARISON")
            normalized_user_dob = normalize_dob(TEST_SUBJECT["dob"])
            normalized_pan_dob = normalize_dob(pan_dob)
            dob_match = normalized_user_dob == normalized_pan_dob
            
            print(f"  User DOB: {TEST_SUBJECT['dob']} -> {normalized_user_dob}")
            print(f"  PAN DOB: {pan_dob} -> {normalized_pan_dob}")
            print(f"  MATCH: {dob_match}")
            
            RESULTS["comparisons"]["pan_dob"] = {
                "user_dob": normalized_user_dob,
                "pan_dob": normalized_pan_dob,
                "match": dob_match
            }
            
            # Log findings
            log_finding("PAN", f"Name format returned: '{pan_name}'")
            log_finding("PAN", f"DOB format returned: '{pan_dob}'")
            log_finding("PAN", f"PAN status: {pan_status}")
            log_finding("PAN", f"Aadhaar linkage: {aadhaar_linked}")
            
            if name_result["verdict"] == "PASS":
                log_finding("PAN", "Name comparison: PASS (sorted match)", "INFO")
            elif name_result["verdict"] == "PARTIAL":
                log_finding("PAN", "Name comparison: PARTIAL (>80% overlap)", "WARN")
            else:
                log_finding("PAN", "Name comparison: FAIL", "ERROR")
            
            return pan_data
        else:
            print(f"  [ERROR] API returned error")
            print(f"  Response: {json.dumps(data, indent=2)}")
            RESULTS["errors"].append(f"PAN verification failed: {data.get('message', 'Unknown')}")
            return None
            
    except Exception as e:
        print(f"  [ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        RESULTS["errors"].append(f"PAN verification exception: {str(e)}")
        return None


# ============================================================
# FINAL REPORT
# ============================================================

def generate_report():
    """Generate final validation report."""
    section("FINAL VALIDATION REPORT")
    
    print("\nA. PAYLOAD REALITY CHECK")
    print("-" * 40)
    
    if RESULTS["pan_response"]:
        pan_data = RESULTS["pan_response"]["response"].get("data", {})
        print(f"  PAN response keys: {list(pan_data.keys())}")
        print(f"  Status code: {RESULTS['pan_response']['status_code']}")
    else:
        print("  PAN: No response captured")
    
    print("\nB. COMPARISON RESULTS")
    print("-" * 40)
    for comp_name, comp_result in RESULTS["comparisons"].items():
        if isinstance(comp_result, dict):
            verdict = comp_result.get("verdict", comp_result.get("match", "N/A"))
            print(f"  {comp_name}: {verdict}")
    
    print("\nC. FINDINGS")
    print("-" * 40)
    for finding in RESULTS["findings"]:
        severity = finding["severity"]
        marker = {"INFO": "[i]", "WARN": "[!]", "ERROR": "[X]"}.get(severity, "[?]")
        print(f"  {marker} [{finding['category']}] {finding['finding']}")
    
    print("\nD. ERRORS")
    print("-" * 40)
    if RESULTS["errors"]:
        for error in RESULTS["errors"]:
            print(f"  [X] {error}")
    else:
        print("  None")
    
    print("\nE. PHASE-3 READINESS")
    print("-" * 40)
    
    pan_ok = RESULTS["pan_response"] and RESULTS["pan_response"]["status_code"] == 200
    
    if pan_ok and not RESULTS["errors"]:
        print("  VERDICT: READY (PAN verified)")
    elif pan_ok:
        print("  VERDICT: READY WITH MINOR FIXES")
    else:
        print("  VERDICT: NOT READY - ERRORS FOUND")
    
    print("\n" + "=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("  SUREPASS SANDBOX VALIDATION")
    print("  CHECK-360 Phase 2 - PAN Test")
    print("=" * 60)
    
    print(f"\n  API Base URL: {BASE_URL}")
    print(f"  API Key: {API_KEY[:20]}...{API_KEY[-10:] if len(API_KEY) > 30 else ''}")
    print(f"\n  Test Subject: {TEST_SUBJECT['name']}")
    print(f"  DOB: {TEST_SUBJECT['dob']}")
    print(f"  PAN: {mask_pan(TEST_SUBJECT['pan'])}")
    
    print("\n  Available APIs:")
    print("    [x] PAN Comprehensive")
    print("    [ ] DigiLocker (not tested yet)")
    print("    [ ] UAN V2 (not tested yet)")
    print("    [!] Aadhaar OTP (NOT GRANTED)")
    
    # Test PAN
    pan_data = test_pan_comprehensive()
    
    # Generate report
    generate_report()
    
    # Save results
    with open("sandbox_validation_results.json", "w") as f:
        json.dump(RESULTS, f, indent=2, default=str)
    print(f"\n  Results saved to: sandbox_validation_results.json")


if __name__ == "__main__":
    main()

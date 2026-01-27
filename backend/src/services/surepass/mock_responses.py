"""
Realistic mock responses for Surepass APIs.

Used when SUREPASS_ENABLED=false (default) for development and testing.
"""

from datetime import datetime, timedelta
import random
import string


def _generate_client_id() -> str:
    """Generate a mock client ID."""
    return "mock_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=10))


# ============ AADHAAR MOCK RESPONSES ============

def mock_aadhaar_generate_otp(aadhaar_number: str) -> dict:
    """Mock response for aadhaar-v2/generate-otp"""
    return {
        "data": {
            "client_id": _generate_client_id(),
            "otp_sent": True,
            "message": "OTP sent successfully to registered mobile",
            "if_number": True,
            "valid_aadhaar": True,
        },
        "status_code": 200,
        "message": "",
        "success": True,
    }


def mock_aadhaar_submit_otp(client_id: str, otp: str) -> dict:
    """Mock response for aadhaar-v2/submit-otp - returns verified Aadhaar data"""
    return {
        "data": {
            "client_id": client_id,
            "full_name": "RAJESH KUMAR SHARMA",
            "aadhaar_number": "XXXX-XXXX-1234",
            "dob": "1990-05-15",
            "gender": "M",
            "address": {
                "country": "India",
                "dist": "Bangalore Urban",
                "state": "Karnataka",
                "po": "Koramangala",
                "loc": "Koramangala 4th Block",
                "vtc": "Bangalore South",
                "subdist": "Bangalore South",
                "street": "100 Feet Road",
                "house": "123",
                "landmark": "Near Forum Mall",
            },
            "full_address": "123, 100 Feet Road, Near Forum Mall, Koramangala 4th Block, Bangalore South, Bangalore Urban, Karnataka - 560034",
            "zip": "560034",
            "profile_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD...",  # Truncated for mock
            "care_of": "S/O: MOHAN SHARMA",
            "share_code": "1234",
            "mobile_verified": True,
            "reference_id": f"AADHAAR_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        },
        "status_code": 200,
        "message": "",
        "success": True,
    }


def mock_aadhaar_invalid_otp() -> dict:
    """Mock response for invalid OTP"""
    return {
        "data": {},
        "status_code": 422,
        "message": "Invalid OTP. Please try again.",
        "success": False,
    }


# ============ PAN MOCK RESPONSES ============

def mock_pan_verification(pan_number: str, name: str, dob: str) -> dict:
    """Mock response for pan-verification API"""
    # Simulate realistic matching
    name_parts = name.upper().split()
    mock_name = "RAJESH KUMAR SHARMA"
    
    # Check if names are similar (simplified check)
    name_match = len(set(name_parts) & set(mock_name.split())) >= 2
    dob_match = dob == "1990-05-15"  # Mock DOB
    
    return {
        "data": {
            "client_id": _generate_client_id(),
            "pan_number": pan_number.upper(),
            "full_name": mock_name,
            "first_name": "RAJESH",
            "middle_name": "KUMAR",
            "last_name": "SHARMA",
            "father_name": "MOHAN SHARMA",
            "dob": "1990-05-15",
            "category": "Individual",
            "aadhaar_seeding_status": "Y",  # Y = linked, N = not linked
            "aadhaar_seeding_status_desc": "Aadhaar is linked with PAN",
            "last_updated": "2024-01-15",
            "name_match_score": 95 if name_match else 45,
            "name_match": name_match,
            "dob_match": dob_match,
            "valid": True,
        },
        "status_code": 200,
        "message": "",
        "success": True,
    }


def mock_pan_invalid() -> dict:
    """Mock response for invalid PAN"""
    return {
        "data": {
            "valid": False,
            "message": "PAN not found in records",
        },
        "status_code": 200,
        "message": "",
        "success": True,
    }


# ============ UAN MOCK RESPONSES ============

def mock_uan_verification(uan_number: str) -> dict:
    """Mock response for UAN verification with employment history"""
    current_date = datetime.now()
    
    return {
        "data": {
            "client_id": _generate_client_id(),
            "uan": uan_number,
            "member_name": "RAJESH KUMAR SHARMA",
            "dob": "1990-05-15",
            "gender": "Male",
            "father_name": "MOHAN SHARMA",
            "aadhaar_verified": True,
            "pan_verified": True,
            "bank_verified": True,
            "mobile_verified": True,
            "establishments": [
                {
                    "establishment_id": "KARAT0001234000",
                    "establishment_name": "ACME TECHNOLOGIES PVT LTD",
                    "member_id": "KARAT0001234000/12345",
                    "date_of_joining": "2020-01-15",
                    "date_of_exit": "2022-06-30",
                    "exit_reason": "Resignation",
                },
                {
                    "establishment_id": "KARAT0005678000",
                    "establishment_name": "TECHCORP SOLUTIONS PVT LTD",
                    "member_id": "KARAT0005678000/67890",
                    "date_of_joining": "2022-07-01",
                    "date_of_exit": None,  # Current employer
                    "exit_reason": None,
                },
            ],
            "total_service": {
                "years": 5,
                "months": 0,
            },
        },
        "status_code": 200,
        "message": "",
        "success": True,
    }


def mock_uan_with_overlap() -> dict:
    """Mock response showing overlapping employment (moonlighting indicator)"""
    return {
        "data": {
            "client_id": _generate_client_id(),
            "uan": "123456789012",
            "member_name": "SUSPECT EMPLOYEE",
            "dob": "1992-03-20",
            "gender": "Male",
            "father_name": "FATHER NAME",
            "establishments": [
                {
                    "establishment_id": "KARAT0001111000",
                    "establishment_name": "COMPANY A PVT LTD",
                    "member_id": "KARAT0001111000/11111",
                    "date_of_joining": "2022-01-01",
                    "date_of_exit": None,  # Still active
                    "exit_reason": None,
                },
                {
                    "establishment_id": "KARAT0002222000",
                    "establishment_name": "COMPANY B PVT LTD",
                    "member_id": "KARAT0002222000/22222",
                    "date_of_joining": "2023-06-01",  # Overlapping!
                    "date_of_exit": None,  # Still active
                    "exit_reason": None,
                },
            ],
            "total_service": {
                "years": 3,
                "months": 0,
            },
        },
        "status_code": 200,
        "message": "",
        "success": True,
    }


def mock_uan_not_found() -> dict:
    """Mock response for UAN not found"""
    return {
        "data": {},
        "status_code": 422,
        "message": "UAN not found in EPFO records",
        "success": False,
    }

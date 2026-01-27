"""
Comparison utilities for verification.

Functions for fuzzy matching names, comparing addresses, and calculating step scores.
No ML - pure rule-based comparison.
"""

import re
from difflib import SequenceMatcher
from typing import Optional


def normalize_name(name: str) -> str:
    """Normalize a name for comparison."""
    if not name:
        return ""
    
    # Convert to uppercase
    name = name.upper()
    
    # Remove common titles and suffixes
    titles = ["MR", "MRS", "MS", "DR", "SHRI", "SMT", "KUMAR", "KUMARI"]
    words = name.split()
    words = [w for w in words if w not in titles]
    
    # Remove special characters
    name = " ".join(words)
    name = re.sub(r'[^A-Z\s]', '', name)
    
    # Normalize whitespace
    name = " ".join(name.split())
    
    return name


def fuzzy_name_match(name1: str, name2: str) -> int:
    """
    Calculate fuzzy match score between two names.
    
    Args:
        name1: First name
        name2: Second name
        
    Returns:
        Match score 0-100 (>=85 is considered a match)
    """
    if not name1 or not name2:
        return 0
    
    # Normalize both names
    n1 = normalize_name(name1)
    n2 = normalize_name(name2)
    
    if not n1 or not n2:
        return 0
    
    # Exact match
    if n1 == n2:
        return 100
    
    # Sequence similarity
    ratio = SequenceMatcher(None, n1, n2).ratio()
    score = int(ratio * 100)
    
    # Token-based similarity (handles word reordering)
    tokens1 = set(n1.split())
    tokens2 = set(n2.split())
    
    if tokens1 and tokens2:
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        jaccard = len(intersection) / len(union)
        token_score = int(jaccard * 100)
        
        # Use higher of the two scores
        score = max(score, token_score)
    
    return score


def exact_match(value1: str, value2: str) -> bool:
    """
    Check if two values match exactly (after normalization).
    
    Args:
        value1: First value
        value2: Second value
        
    Returns:
        True if values match exactly
    """
    if not value1 or not value2:
        return False
    
    # Normalize: strip whitespace, convert to uppercase
    v1 = str(value1).strip().upper()
    v2 = str(value2).strip().upper()
    
    return v1 == v2


def normalize_address(address: str) -> str:
    """Normalize an address for comparison."""
    if not address:
        return ""
    
    address = address.upper()
    
    # Remove common abbreviations
    replacements = {
        "ROAD": "RD",
        "STREET": "ST",
        "AVENUE": "AVE",
        "FLOOR": "FLR",
        "BLOCK": "BLK",
        "BUILDING": "BLDG",
        "APARTMENT": "APT",
        "SECTOR": "SEC",
        "PHASE": "PH",
    }
    
    for full, abbr in replacements.items():
        address = address.replace(full, abbr)
    
    # Remove special characters except spaces
    address = re.sub(r'[^A-Z0-9\s]', '', address)
    
    # Normalize whitespace
    address = " ".join(address.split())
    
    return address


def address_similarity(address1: str, address2: str) -> str:
    """
    Compare two addresses for similarity.
    
    Args:
        address1: First address
        address2: Second address
        
    Returns:
        "full" (>=80%), "partial" (>=50%), "none" (<50%), or "not_provided"
    """
    if not address1 or not address2:
        return "not_provided"
    
    # Normalize addresses
    a1 = normalize_address(address1)
    a2 = normalize_address(address2)
    
    if not a1 or not a2:
        return "not_provided"
    
    # Calculate similarity
    ratio = SequenceMatcher(None, a1, a2).ratio()
    
    # Also check token overlap (important for addresses)
    tokens1 = set(a1.split())
    tokens2 = set(a2.split())
    
    if tokens1 and tokens2:
        intersection = tokens1 & tokens2
        # Check if key tokens (district, city, pin) match
        important_matches = sum(1 for t in intersection if len(t) >= 4)
        
        if important_matches >= 3:
            ratio = max(ratio, 0.7)
    
    if ratio >= 0.80:
        return "full"
    elif ratio >= 0.50:
        return "partial"
    else:
        return "none"


def calculate_step_score(
    name_match: bool,
    dob_match: bool,
    address_match: Optional[str] = None,
    additional_checks: dict = None
) -> int:
    """
    Calculate step score based on comparison results.
    
    Args:
        name_match: Whether name matched (>=85% fuzzy)
        dob_match: Whether DOB matched exactly
        address_match: "full", "partial", "none", or None
        additional_checks: Additional boolean checks
        
    Returns:
        Score 0-100
    """
    score = 0
    
    # Name: 40 points
    if name_match:
        score += 40
    
    # DOB: 30 points
    if dob_match:
        score += 30
    
    # Address: 20 points
    if address_match == "full":
        score += 20
    elif address_match == "partial":
        score += 10
    
    # Base points for successful verification: 10
    if name_match or dob_match:
        score += 10
    
    # Additional checks
    if additional_checks:
        for key, value in additional_checks.items():
            if value is True:
                score += 5
    
    return min(score, 100)


def determine_step_status(score: int) -> str:
    """
    Determine step status based on score.
    
    Args:
        score: Step score 0-100
        
    Returns:
        "VERIFIED", "PARTIAL", or "FAILED"
    """
    if score >= 90:
        return "VERIFIED"
    elif score >= 70:
        return "PARTIAL"
    else:
        return "FAILED"

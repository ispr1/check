"""
Document analysis rules and configuration.

Centralized weights, thresholds, and red-flag definitions.
Easy to tune without changing code.
"""

# ============ SCORING WEIGHTS ============
# Total must equal 1.0

WEIGHTS = {
    "metadata": 0.30,   # PDF creator, dates, producer
    "fonts": 0.25,      # Font consistency
    "forensics": 0.25,  # Image manipulation signals
    "text": 0.20,       # Format validation
}

# ============ STATUS THRESHOLDS ============

THRESHOLDS = {
    "legitimate": 85.0,      # Score >= 85 → LEGITIMATE
    "review_required": 60.0,  # Score 60-84 → REVIEW_REQUIRED
    # Score < 60 → SUSPICIOUS
}

# ============ METADATA RED FLAGS ============
# Software that suggests image manipulation (not document creation)

SUSPICIOUS_CREATORS = [
    "photoshop",
    "gimp",
    "canva",
    "paint",
    "pixlr",
    "fotor",
    "snapseed",
    "picsart",
    "photo editor",
    "image editor",
]

# Legitimate document creators (higher trust)
TRUSTED_CREATORS = [
    "microsoft word",
    "microsoft office",
    "libreoffice",
    "openoffice",
    "google docs",
    "adobe acrobat",
    "pdf creator",
    "chrome",
    "firefox",
    "edge",
    "safari",
]

# ============ FONT RULES ============

# Normal documents rarely use more than this many fonts
MAX_NORMAL_FONTS = 4

# ============ TEXT VALIDATION PATTERNS ============

# PAN format: 5 letters + 4 digits + 1 letter
# 4th character must be valid entity type
VALID_PAN_ENTITY_TYPES = ['P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G']

# Aadhaar format: 12 digits, no leading 0 or 1
AADHAAR_PATTERN = r'^[2-9][0-9]{11}$'

# Common date formats in Indian documents
DATE_PATTERNS = [
    r'\d{2}[/-]\d{2}[/-]\d{4}',  # DD/MM/YYYY or DD-MM-YYYY
    r'\d{4}[/-]\d{2}[/-]\d{2}',  # YYYY/MM/DD or YYYY-MM-DD
]

# ============ DOCUMENT TYPE CONFIGS ============

DOCUMENT_TYPES = {
    "education": {
        "expected_text": ["university", "college", "degree", "certificate", "passed"],
        "min_pages": 1,
        "max_pages": 10,
    },
    "experience": {
        "expected_text": ["employment", "experience", "company", "designation", "salary"],
        "min_pages": 1,
        "max_pages": 5,
    },
    "id_card": {
        "expected_text": ["employee", "id", "valid", "name"],
        "min_pages": 1,
        "max_pages": 2,
    },
}

# ============ LAYER SCORE DEFAULTS ============

DEFAULT_SCORES = {
    "clean": 100.0,      # No issues found
    "minor_issue": 80.0,  # Minor anomaly
    "moderate_issue": 60.0,  # Needs attention
    "major_issue": 40.0,  # Significant concern
    "critical_issue": 20.0,  # Very suspicious
}

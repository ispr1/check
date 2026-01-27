"""
Minimal audit trail for verification actions.

Logs per-step actions for compliance and dispute resolution.
Not full event sourcing - just essential evidence.
"""

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def log_verification_action(
    verification_id: int,
    step_type: str,
    action: str,
    actor: str = "SYSTEM",
    details: Optional[dict] = None,
) -> dict:
    """
    Create audit entry for a verification action.
    
    Args:
        verification_id: ID of the verification session
        step_type: AADHAAR, PAN, UAN, etc.
        action: VERIFIED, FAILED, SKIPPED, etc.
        actor: SYSTEM, CANDIDATE, HR, etc.
        details: Additional context (no PII)
        
    Returns:
        Audit entry dict to append to step/verification
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "step": step_type,
        "action": action,
        "actor": actor,
    }
    
    if details:
        # Sanitize - never include raw PII
        safe_details = {
            k: v for k, v in details.items()
            if k not in ("aadhaar_number", "pan_number", "uan_number", "raw_response")
        }
        entry["details"] = safe_details
    
    logger.info(f"AUDIT: verification={verification_id} step={step_type} action={action} actor={actor}")
    
    return entry


def build_audit_trail(existing_trail: list, new_entry: dict) -> list:
    """
    Append new entry to existing audit trail.
    
    Args:
        existing_trail: Current audit trail list (or None)
        new_entry: New audit entry from log_verification_action
        
    Returns:
        Updated audit trail
    """
    if existing_trail is None:
        existing_trail = []
    
    existing_trail.append(new_entry)
    return existing_trail


def format_audit_for_export(audit_trail: list) -> list:
    """
    Format audit trail for compliance export.
    Adds human-readable timestamps.
    """
    if not audit_trail:
        return []
    
    formatted = []
    for entry in audit_trail:
        formatted.append({
            **entry,
            "timestamp_readable": _format_timestamp(entry.get("timestamp", "")),
        })
    
    return formatted


def _format_timestamp(iso_timestamp: str) -> str:
    """Convert ISO timestamp to human readable."""
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        return dt.strftime("%d %b %Y, %H:%M:%S UTC")
    except Exception:
        return iso_timestamp


# Standard action types for consistency
class AuditAction:
    INITIATED = "INITIATED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    SKIPPED = "SKIPPED"
    SUBMITTED = "SUBMITTED"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FLAGGED = "FLAGGED"
    NOTE_ADDED = "NOTE_ADDED"


# Standard actor types
class AuditActor:
    SYSTEM = "SYSTEM"
    CANDIDATE = "CANDIDATE"
    HR = "HR"
    ADMIN = "ADMIN"
    SUREPASS = "SUREPASS"

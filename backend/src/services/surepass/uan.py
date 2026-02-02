"""
UAN/Employment verification service.

Verifies employment history, detects overlaps (moonlighting), calculates experience.
Flags are review hints, not verdicts.
"""

import logging
from typing import Optional, List
from datetime import datetime, date
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta

from .client import get_surepass_client
from .exceptions import SurepassInvalidInputError, SurepassNotAvailableError
from . import mock_responses

logger = logging.getLogger(__name__)


class UANService:
    """Service for UAN/Employment verification."""
    
    def __init__(self):
        self.client = get_surepass_client()
    
    def validate_uan_number(self, uan_number: str) -> str:
        """Validate and clean UAN number."""
        cleaned = uan_number.replace(" ", "").replace("-", "")
        
        if not cleaned.isdigit():
            raise SurepassInvalidInputError("uan_number", "Must contain only digits")
        
        if len(cleaned) != 12:
            raise SurepassInvalidInputError("uan_number", "Must be exactly 12 digits")
        
        return cleaned
    
    def verify(self, uan_number: str) -> dict:
        """
        Verify UAN and get employment history.
        
        Args:
            uan_number: 12-digit Universal Account Number
            
        Returns:
            UAN data including employment history
        """
        cleaned = self.validate_uan_number(uan_number)
        
        if self.client.is_mock_mode():
            logger.info(f"Mock: Verifying UAN XXXX-XXXX-{cleaned[-4:]}")
            return mock_responses.mock_uan_verification(cleaned)["data"]
        
        try:
            response = self.client.post("uan-verification", {
                "uan_number": cleaned
            })
        except SurepassNotAvailableError as e:
            logger.warning(f"UAN API not available: {e.message}")
            return {
                "status": "NOT_AVAILABLE",
                "message": "UAN verification service temporarily unavailable",
                "error": "API_NOT_AVAILABLE",
                "establishments": [],
            }
        
        return response
    
    def analyze(
        self, 
        surepass_data: dict,
        aadhaar_name: str,
        aadhaar_dob: str,
        claimed_experience_years: Optional[int] = None
    ) -> dict:
        """
        Analyze employment history and compare with Aadhaar identity.
        
        Args:
            surepass_data: Data from verify()
            aadhaar_name: Aadhaar-verified name
            aadhaar_dob: Aadhaar-verified DOB
            claimed_experience_years: Candidate's claimed experience
            
        Returns:
            Analysis result with flags
        """
        from src.utils.comparison import fuzzy_name_match, exact_match
        
        # Identity match
        uan_name = surepass_data.get("member_name", "")
        uan_dob = surepass_data.get("dob", "")
        
        name_score = fuzzy_name_match(uan_name, aadhaar_name)
        name_match = name_score >= 85
        dob_match = exact_match(uan_dob, aadhaar_dob)
        
        # Employment analysis
        establishments = surepass_data.get("establishments", [])
        employment_analysis = self._analyze_employment(establishments)
        
        # Experience comparison
        actual_experience = employment_analysis["total_experience_years"]
        experience_mismatch = False
        if claimed_experience_years is not None:
            # Allow 1 year variance
            experience_mismatch = abs(actual_experience - claimed_experience_years) > 1
        
        # Determine status
        has_identity_match = name_match and dob_match
        has_overlaps = employment_analysis["has_overlaps"]
        
        flags = []
        if has_overlaps:
            flags.append("OVERLAPPING_EMPLOYMENT")
        if experience_mismatch:
            flags.append("EXPERIENCE_MISMATCH")
        if not has_identity_match:
            flags.append("IDENTITY_MISMATCH")
        
        # Calculate score
        if not has_identity_match:
            status = "FAILED"
            score = 30
        elif has_overlaps or experience_mismatch:
            status = "PARTIAL"
            score = 70
        else:
            status = "VERIFIED"
            score = 100
        
        return {
            "status": status,
            "score": score,
            "flags": flags,
            "details": {
                "identity_match": {
                    "name_match": name_match,
                    "name_score": name_score,
                    "dob_match": dob_match,
                    "uan_name": uan_name,
                    "uan_dob": uan_dob,
                },
                "employment": employment_analysis,
                "experience": {
                    "actual_years": actual_experience,
                    "claimed_years": claimed_experience_years,
                    "mismatch": experience_mismatch,
                }
            },
            "verified_at": datetime.utcnow().isoformat(),
        }
    
    def _analyze_employment(self, establishments: List[dict]) -> dict:
        """Analyze employment history for overlaps and total experience."""
        if not establishments:
            return {
                "total_jobs": 0,
                "total_experience_years": 0,
                "total_experience_months": 0,
                "has_overlaps": False,
                "overlapping_periods": [],
                "current_employer": None,
                "employers": [],
            }
        
        # Parse dates and build timeline
        timeline = []
        current_employer = None
        employers = []
        
        for est in establishments:
            try:
                start_date = parse_date(est.get("date_of_joining", "")).date() if est.get("date_of_joining") else None
                end_date = parse_date(est.get("date_of_exit", "")).date() if est.get("date_of_exit") else date.today()
                
                if start_date:
                    timeline.append({
                        "name": est.get("establishment_name", "Unknown"),
                        "start": start_date,
                        "end": end_date,
                        "is_current": est.get("date_of_exit") is None,
                    })
                    
                    employers.append({
                        "name": est.get("establishment_name", ""),
                        "start_date": str(start_date),
                        "end_date": str(end_date) if est.get("date_of_exit") else None,
                        "is_current": est.get("date_of_exit") is None,
                    })
                    
                    if est.get("date_of_exit") is None:
                        current_employer = est.get("establishment_name", "")
            except Exception as e:
                logger.warning(f"Error parsing employment dates: {e}")
                continue
        
        # Detect overlaps
        overlaps = []
        for i, job1 in enumerate(timeline):
            for job2 in timeline[i+1:]:
                if self._periods_overlap(job1["start"], job1["end"], job2["start"], job2["end"]):
                    overlaps.append({
                        "employer1": job1["name"],
                        "employer2": job2["name"],
                        "overlap_start": str(max(job1["start"], job2["start"])),
                        "overlap_end": str(min(job1["end"], job2["end"])),
                    })
        
        # Calculate total experience (non-overlapping)
        total_months = self._calculate_total_experience(timeline)
        
        return {
            "total_jobs": len(timeline),
            "total_experience_years": total_months // 12,
            "total_experience_months": total_months,
            "has_overlaps": len(overlaps) > 0,
            "overlapping_periods": overlaps,
            "current_employer": current_employer,
            "employers": employers,
        }
    
    def _periods_overlap(self, start1: date, end1: date, start2: date, end2: date) -> bool:
        """Check if two date ranges overlap."""
        return start1 <= end2 and start2 <= end1
    
    def _calculate_total_experience(self, timeline: List[dict]) -> int:
        """Calculate total experience in months (merging overlapping periods)."""
        if not timeline:
            return 0
        
        # Sort by start date
        sorted_timeline = sorted(timeline, key=lambda x: x["start"])
        
        # Merge overlapping periods
        merged = []
        current = sorted_timeline[0]
        
        for job in sorted_timeline[1:]:
            if job["start"] <= current["end"]:
                # Extend current period
                current["end"] = max(current["end"], job["end"])
            else:
                merged.append(current)
                current = job
        merged.append(current)
        
        # Calculate total months
        total_months = 0
        for period in merged:
            diff = relativedelta(period["end"], period["start"])
            total_months += diff.years * 12 + diff.months
        
        return total_months


# Singleton instance
_service_instance: Optional[UANService] = None


def get_uan_service() -> UANService:
    """Get or create singleton UANService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = UANService()
    return _service_instance

"""
Font Consistency Analyzer.

Checks:
- Number of fonts used
- Font consistency across document
"""

import logging
from io import BytesIO
from typing import Dict, Set

from ..contracts import LayerResult
from ..rules import MAX_NORMAL_FONTS, DEFAULT_SCORES

logger = logging.getLogger(__name__)


class FontAnalyzer:
    """
    Analyze font usage for consistency.
    
    Red flags:
    - Too many different fonts (suggests copy-paste)
    - Unusual font combinations
    """
    
    def analyze(self, file_bytes: bytes) -> LayerResult:
        """
        Analyze font consistency in PDF.
        
        Returns LayerResult with score and flags.
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            logger.warning("PyMuPDF not installed, skipping font analysis")
            return LayerResult(
                name="fonts",
                score=DEFAULT_SCORES["clean"],
                flags=["ANALYZER_NOT_AVAILABLE"],
            )
        
        flags = []
        score = DEFAULT_SCORES["clean"]
        details = {}
        
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            
            fonts_used: Dict[str, int] = {}
            pages_with_fonts: Dict[str, Set[int]] = {}
            
            for page_num, page in enumerate(doc):
                page_fonts = page.get_fonts()
                
                for font in page_fonts:
                    font_name = font[3] if len(font) > 3 else "Unknown"
                    
                    # Count font occurrences
                    fonts_used[font_name] = fonts_used.get(font_name, 0) + 1
                    
                    # Track which pages use which fonts
                    if font_name not in pages_with_fonts:
                        pages_with_fonts[font_name] = set()
                    pages_with_fonts[font_name].add(page_num)
            
            doc.close()
            
            font_count = len(fonts_used)
            details = {
                "font_count": font_count,
                "fonts": list(fonts_used.keys())[:10],  # Limit for display
            }
            
            # Check 1: Too many fonts
            if font_count > MAX_NORMAL_FONTS * 2:
                flags.append(f"EXCESSIVE_FONTS: {font_count}")
                score = min(score, DEFAULT_SCORES["moderate_issue"])
            elif font_count > MAX_NORMAL_FONTS:
                flags.append(f"MANY_FONTS: {font_count}")
                score = min(score, DEFAULT_SCORES["minor_issue"])
            
            # Check 2: Inconsistent font usage (font only on one page in multi-page doc)
            if len(pages_with_fonts) > 0:
                page_count = max(max(pages) for pages in pages_with_fonts.values()) + 1
                
                if page_count > 1:
                    isolated_fonts = [
                        f for f, pages in pages_with_fonts.items()
                        if len(pages) == 1
                    ]
                    
                    # More than half fonts are isolated
                    if len(isolated_fonts) > font_count // 2 and font_count > 2:
                        flags.append("INCONSISTENT_FONT_USAGE")
                        score = min(score, DEFAULT_SCORES["minor_issue"])
            
        except Exception as e:
            logger.warning(f"Font analysis failed: {e}")
            return LayerResult(
                name="fonts",
                score=DEFAULT_SCORES["minor_issue"],
                flags=["ANALYSIS_ERROR"],
                details={"error": str(e)},
            )
        
        return LayerResult(
            name="fonts",
            score=score,
            flags=flags,
            details=details,
        )

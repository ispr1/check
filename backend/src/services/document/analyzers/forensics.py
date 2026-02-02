"""
Image Forensics Analyzer.

Checks for:
- Compression artifacts
- Variance inconsistencies
- Basic manipulation signals
"""

import logging
from io import BytesIO
from typing import Optional
import numpy as np

from ..contracts import LayerResult
from ..rules import DEFAULT_SCORES

logger = logging.getLogger(__name__)


class ForensicsAnalyzer:
    """
    Analyze image/scanned document for manipulation signals.
    
    Uses basic statistical analysis, not ML.
    """
    
    def analyze(self, file_bytes: bytes) -> LayerResult:
        """
        Analyze document for image manipulation signals.
        
        Returns LayerResult with score and flags.
        """
        try:
            import fitz  # PyMuPDF for PDF to image
        except ImportError:
            logger.warning("PyMuPDF not installed, skipping forensics analysis")
            return LayerResult(
                name="forensics",
                score=DEFAULT_SCORES["clean"],
                flags=["ANALYZER_NOT_AVAILABLE"],
            )
        
        flags = []
        score = DEFAULT_SCORES["clean"]
        details = {}
        
        try:
            # Convert first page to image
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            
            if len(doc) == 0:
                return LayerResult(
                    name="forensics",
                    score=DEFAULT_SCORES["minor_issue"],
                    flags=["EMPTY_DOCUMENT"],
                )
            
            # Get first page as pixmap
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))  # 1x scale
            
            # Convert to numpy array
            img_array = np.frombuffer(pix.samples, dtype=np.uint8)
            img_array = img_array.reshape(pix.height, pix.width, pix.n)
            
            # Convert to grayscale for analysis
            if pix.n >= 3:
                gray = np.mean(img_array[:, :, :3], axis=2)
            else:
                gray = img_array[:, :, 0]
            
            doc.close()
            
            details["image_size"] = f"{pix.width}x{pix.height}"
            
            # Analysis 1: Block variance analysis
            variance_result = self._analyze_block_variance(gray)
            if variance_result["suspicious"]:
                flags.append("INCONSISTENT_QUALITY_REGIONS")
                score = min(score, DEFAULT_SCORES["moderate_issue"])
            details["variance_std"] = round(variance_result["std"], 2)
            
            # Analysis 2: Edge density check
            edge_result = self._analyze_edge_density(gray)
            if edge_result["suspicious"]:
                flags.append("UNUSUAL_EDGE_PATTERN")
                score = min(score, DEFAULT_SCORES["minor_issue"])
            details["edge_density"] = round(edge_result["density"], 4)
            
            # Analysis 3: Entropy analysis
            entropy = self._calculate_entropy(gray)
            details["entropy"] = round(entropy, 2)
            
            # Very low entropy = possibly synthetic
            if entropy < 2.0:
                flags.append("LOW_ENTROPY")
                score = min(score, DEFAULT_SCORES["minor_issue"])
            
        except Exception as e:
            logger.warning(f"Forensics analysis failed: {e}")
            return LayerResult(
                name="forensics",
                score=DEFAULT_SCORES["minor_issue"],
                flags=["ANALYSIS_ERROR"],
                details={"error": str(e)},
            )
        
        return LayerResult(
            name="forensics",
            score=score,
            flags=flags,
            details=details,
        )
    
    def _analyze_block_variance(self, gray: np.ndarray, block_size: int = 50) -> dict:
        """
        Analyze variance across image blocks.
        
        Large variance differences between blocks may indicate editing.
        """
        h, w = gray.shape
        variances = []
        
        for i in range(0, h - block_size, block_size):
            for j in range(0, w - block_size, block_size):
                block = gray[i:i+block_size, j:j+block_size]
                variances.append(np.var(block))
        
        if not variances:
            return {"suspicious": False, "std": 0}
        
        variance_std = np.std(variances)
        
        # High variance between blocks = potential manipulation
        return {
            "suspicious": variance_std > 1500,
            "std": variance_std,
        }
    
    def _analyze_edge_density(self, gray: np.ndarray) -> dict:
        """
        Analyze edge density.
        
        Unusual patterns may indicate splicing.
        """
        try:
            # Simple edge detection using gradient
            gx = np.diff(gray, axis=1)
            gy = np.diff(gray, axis=0)
            
            # Count significant edges
            threshold = 30
            edges_x = np.sum(np.abs(gx) > threshold)
            edges_y = np.sum(np.abs(gy) > threshold)
            
            total_pixels = gray.size
            density = (edges_x + edges_y) / (2 * total_pixels)
            
            # Very high or very low density is suspicious
            return {
                "suspicious": density > 0.3 or density < 0.01,
                "density": density,
            }
        except:
            return {"suspicious": False, "density": 0}
    
    def _calculate_entropy(self, gray: np.ndarray) -> float:
        """
        Calculate image entropy.
        
        Low entropy = potentially synthetic image.
        """
        try:
            # Flatten and bin the values
            hist, _ = np.histogram(gray.flatten(), bins=256, range=(0, 256))
            
            # Normalize
            hist = hist / hist.sum()
            
            # Remove zeros
            hist = hist[hist > 0]
            
            # Calculate entropy
            entropy = -np.sum(hist * np.log2(hist))
            
            return entropy
        except:
            return 5.0  # Default to normal entropy

# Document Analysis Service

## Responsibility
Detects anomalies in uploaded PDF/Image documents.

## Components
1.  **Metadata Analyzer:**
    *   Checks `Producer`/`Creator` tags.
    *   Flags known editors: "Photoshop", "GIMP", "Canva", "ilovepdf".
    *   Checks modification dates vs creation dates.
2.  **Font Analyzer:**
    *   Extracts font families.
    *   Flags documents with > 3 fonts (anomaly in standard government docs).
3.  **Forensics Analyzer:**
    *   Error Level Analysis (ELA) - simplified variance check.
    *   Detects consistent noise patterns.
4.  **Text Validator:**
    *   Regex match for PAN/Aadhaar patterns.
    *   Date consistency checks.

## Key Classes
*   `DocumentAnalysisService`: Orchestrator.
*   `MetadataAnalyzer`: Metadata logic.
*   `ForensicsAnalyzer`: Image logic.

## Limitations
*   Cannot detect "perfect" physical forgeries (e.g., a fake ID printed and then scanned).
*   Relies on digital artifacts (more effective on "digital-born" or edited PDFs).

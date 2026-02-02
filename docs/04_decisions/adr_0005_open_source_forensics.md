# ADR 005: Open Source Forensics Stack

**Status:** Accepted  
**Date:** 2026-02-01

## Context
We need to analyze documents for forgery (metadata, text, fonts).
Options:
1.  **AWS Textract / Commercial OCR:** Expensive, data leaves our control, black box.
2.  **Open Source (PyMuPDF, pdfplumber):** Free, customizable, runs locally.

## Decision
We chose **Option 2: Open Source Stack**.

## Rationale
1.  **Cost:** Commercial OCR charges per page. Forensics requires deep inspection, not just text extraction.
2.  **Control:** We need to access raw PDF streams, metadata dictionaries, and font tables. Commercial APIs often sanitize this "noise" which is exactly what we need to detect fraud.
3.  **Indian Context:** Rules for PAN/Aadhaar formats are best implemented via custom regex, not generic OCR models.

## Consequences
*   We own the maintenance of these libraries.
*   We implement our own "heuristics" (e.g., Photoshop detection logic) which requires domain knowledge.

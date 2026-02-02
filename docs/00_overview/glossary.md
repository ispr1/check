# Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **Candidate** | The individual undergoing verification. | Core Entity |
| **Orchestrator** | The CHECK-360 service logic that dispatches requests to vendors (Surepass, AWS) and aggregates results. | Architecture |
| **Trust Score** | A calculated value (0-100) representing the system's confidence in the candidate's claims. Starts at 100, purely deductive. | Key Metric |
| **Trust Source / Source of Truth** | An immutable, third-party authority (UIDAI, NSDL, EPFO, Court Records) used to validate claims. | Data |
| **Verification Session** | A unique, time-bounded workflow where a candidate submits data and orchestrator verifies it. | Workflow |
| **Deduction** | A specific point penalty applied to the Trust Score based on a deviation (e.g., Name Mismatch, Face Low Confidence). | Scoring |
| **Flag** | A generated warning attached to a verification (e.g., `DOC_SUSPICIOUS`, `FACE_MISMATCH`). | Reporting |
| **Surepass** | Our primary vendor for Government ID APIs (Aadhaar, PAN). | Vendor |
| **Rekognition** | AWS Service used for Face Comparison (Selfie vs ID Card). | Vendor |
| **Legitimacy Score** | A sub-score (0-100) specifically for document forensics, derived from metadata, fonts, and noise analysis. | Document Analysis |
| **HR Decision** | The final immutable status (`APPROVED`, `REJECTED`) recorded by an HR user after reviewing the system outputs. | Human-in-the-loop |

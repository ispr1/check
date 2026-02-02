# Security Model

## 1. Authentication & Authorization
*   **JWT:** All API access requires valid Bearer tokens.
*   **Role-Based Access Control (RBAC):**
    *   `Candidate`: Can only access their own verification session.
    *   `HR`: Can view candidates within their Company.
    *   `Admin`: System-wide access.

## 2. Data Security
*   **Encryption at Rest:** Sensitive DB columns (Aadhaar, PAN, Phone) encrypted via `Fernet` (AES-128-CBC) or AES-256-GCM (Phase 2.5).
*   **Encryption in Transit:** TLS 1.2+ mandatory for all connections.

## 3. Trust Boundaries
*   **Public Internet:** Untrusted. WAF required.
*   **API Gateway:** Trust Boundary 1. Sanitizes inputs.
*   **Service Core:** Trusted Zone.
*   **Database/S3:** High Security Zone. No direct public access.

## 4. Vendor Isolation
*   We treat vendors (Surepass, AWS) as semi-trusted.
*   We validate their outputs (Schema validation).
*   We handle their failures gracefully without leaking stack traces to users.

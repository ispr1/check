# Test Strategy

## Levels of Testing

### 1. Unit Testing
*   **Scope:** Individual functions (e.g., `calculate_trust_score`, regex validators).
*   **Tools:** `pytest`.
*   **Mocking:** All vendor calls (Surepass, AWS) MUST be mocked.

### 2. Integration Testing
*   **Scope:** API Endpoints + Database.
*   **Validation:**
    *   Create Candidate -> DB record exists?
    *   Upload Document -> S3 key generated?
*   **Tools:** `TestClient` (FastAPI).

### 3. End-to-End (E2E) Testing
*   **Scope:** Full user flows.
*   **Script:** `scripts/create_sample_data.py`.
*   **Validation:** Simulates a full verification session from start to HR decision.

## Mock vs Live
*   **Development:** Uses `MockFaceProvider` and mocked Surepass responses.
*   **Staging/Prod:** Uses Real AWS Rekognition and Live Surepass APIs.
*   **Control:** Toggled via `.env` (`FACE_PROVIDER=mock` vs `aws`).

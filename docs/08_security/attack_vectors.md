# Attack Vectors and Mitigations

## 1. Fake Identity Attacks

### Attack: Photo Replay
**Method:** Candidate shows photo of someone else's face.  
**Detection:** Rekognition passive liveness.  
**Mitigation:** Require video in future (Phase 8).

### Attack: Manipulated Aadhaar
**Method:** Edited Aadhaar card image.  
**Detection:** We don't trust candidate images; we fetch from Surepass.  
**Mitigation:** Only Surepass response is trusted.

### Attack: UAN Mule
**Method:** Candidate uses someone else's UAN.  
**Detection:** Cross-match name from UAN with Aadhaar.  
**Mitigation:** Flag mismatch (-10 points).

## 2. Document Forgery

### Attack: Fake Experience Letter
**Method:** Photoshop or template-based PDF.  
**Detection:** Metadata, font, and noise analysis.  
**Mitigation:** Flag + HR review.

### Attack: Degree Mill Certificate
**Method:** Legitimate-looking cert from unaccredited institution.  
**Detection:** Out of scope (requires university database).  
**Mitigation:** Manual HR verification.

## 3. API Abuse

### Attack: Token Brute Force
**Method:** Guess verification tokens.  
**Detection:** Tokens are 256-bit random.  
**Mitigation:** Mathematically infeasible.

### Attack: Rate Limit Bypass
**Method:** Distributed requests.  
**Detection:** IP + token-based rate limiting.  
**Mitigation:** 429 responses, exponential backoff.

## 4. Injection Attacks

### Attack: SQL Injection
**Method:** Malicious input in fields.  
**Detection:** Parameterized queries.  
**Mitigation:** SQLAlchemy ORM prevents raw SQL.

### Attack: XSS (Future UI)
**Method:** Script injection.  
**Detection:** N/A (API only currently).  
**Mitigation:** Sanitize all outputs when UI built.

## 5. Insider Threats

### Attack: HR Data Export
**Method:** Bulk download candidate data.  
**Detection:** Audit logs on bulk queries.  
**Mitigation:** No bulk export API; individual requests only.

### Attack: Admin Key Theft
**Method:** Steal AWS keys.  
**Detection:** CloudTrail logging.  
**Mitigation:** IAM rotation every 90 days; MFA required.

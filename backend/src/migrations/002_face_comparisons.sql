-- Phase 3: Face Comparisons Table
-- For storing face verification results

CREATE TABLE IF NOT EXISTS face_comparisons (
    id SERIAL PRIMARY KEY,
    
    -- Foreign keys
    verification_id INTEGER NOT NULL REFERENCES verifications(id) ON DELETE CASCADE,
    step_id INTEGER REFERENCES verification_steps(id) ON DELETE CASCADE,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    
    -- Evidence (Images)
    selfie_s3_key VARCHAR(500) NOT NULL,
    reference_s3_key VARCHAR(500),
    reference_source VARCHAR(50),  -- hr_upload, aadhaar, id_card
    
    -- Truth (Scores)
    confidence_score FLOAT NOT NULL DEFAULT 0.0,
    decision VARCHAR(50) NOT NULL,  -- MATCH, LOW_CONFIDENCE, MISMATCH, PENDING_REFERENCE, NOT_AVAILABLE, ERROR
    flags JSONB DEFAULT '[]'::jsonb,
    
    -- Encrypted Data (Never Exposed to HR)
    raw_response_encrypted BYTEA,
    
    -- Audit
    triggered_by VARCHAR(100),  -- candidate, hr_upload, system
    audit_trail JSONB DEFAULT '[]'::jsonb,
    
    -- Timestamps
    compared_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS ix_face_comparisons_verification_id ON face_comparisons(verification_id);
CREATE INDEX IF NOT EXISTS ix_face_comparisons_candidate_id ON face_comparisons(candidate_id);
CREATE INDEX IF NOT EXISTS ix_face_comparisons_verification_candidate ON face_comparisons(verification_id, candidate_id);
CREATE INDEX IF NOT EXISTS ix_face_comparisons_decision ON face_comparisons(decision);

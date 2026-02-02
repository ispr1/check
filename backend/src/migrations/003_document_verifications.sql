-- Phase 4: Document Verifications Table
-- For storing document legitimacy analysis results

CREATE TABLE IF NOT EXISTS document_verifications (
    id SERIAL PRIMARY KEY,
    
    -- Foreign keys
    verification_id INTEGER REFERENCES verifications(id) ON DELETE CASCADE,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    
    -- Document info
    document_type VARCHAR(50) NOT NULL,  -- education, experience, id_card
    s3_key VARCHAR(500) NOT NULL,
    original_filename VARCHAR(255),
    
    -- Analysis results
    legitimacy_score FLOAT NOT NULL DEFAULT 0.0,
    status VARCHAR(50) NOT NULL,  -- LEGITIMATE, REVIEW_REQUIRED, SUSPICIOUS
    
    -- Breakdown by layer
    breakdown JSONB DEFAULT '{}'::jsonb,
    
    -- Flags for HR review
    flags JSONB DEFAULT '[]'::jsonb,
    
    -- Timestamps
    analyzed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS ix_doc_verifications_verification_id ON document_verifications(verification_id);
CREATE INDEX IF NOT EXISTS ix_doc_verifications_candidate_id ON document_verifications(candidate_id);
CREATE INDEX IF NOT EXISTS ix_doc_verifications_candidate_type ON document_verifications(candidate_id, document_type);
CREATE INDEX IF NOT EXISTS ix_doc_verifications_status ON document_verifications(status);

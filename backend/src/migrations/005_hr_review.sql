-- Phase 6: HR Review Tables
-- For HR document uploads and hiring decisions

-- HR Documents (uploaded by HR after candidate submission)
CREATE TABLE IF NOT EXISTS hr_documents (
    id SERIAL PRIMARY KEY,
    
    -- Foreign keys
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    verification_id INTEGER REFERENCES verifications(id) ON DELETE CASCADE,
    
    -- Document info
    document_type VARCHAR(50) NOT NULL,
    s3_key VARCHAR(500) NOT NULL,
    original_filename VARCHAR(255),
    
    -- Source tracking
    source VARCHAR(50) DEFAULT 'hr_upload',
    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- HR notes
    notes TEXT,
    
    -- Analysis results
    document_verification_id INTEGER REFERENCES document_verifications(id) ON DELETE SET NULL,
    is_analyzed BOOLEAN DEFAULT FALSE,
    analysis_status VARCHAR(50),
    legitimacy_score FLOAT,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- HR Decisions (immutable audit trail)
CREATE TABLE IF NOT EXISTS hr_decisions (
    id SERIAL PRIMARY KEY,
    
    -- Foreign keys
    verification_id INTEGER NOT NULL REFERENCES verifications(id) ON DELETE CASCADE,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    
    -- Decision
    decision VARCHAR(50) NOT NULL,  -- APPROVED, REJECTED, NEED_MORE_INFO
    
    -- Decision maker
    decided_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    decided_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Reasoning
    reason_codes JSONB DEFAULT '[]'::jsonb,
    comments TEXT,
    
    -- Override tracking
    override_requested BOOLEAN DEFAULT FALSE,
    override_approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    override_approved_at TIMESTAMP,
    override_comments TEXT,
    
    -- Trust score snapshot (immutable)
    trust_score_at_decision FLOAT,
    trust_status_at_decision VARCHAR(50),
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS ix_hr_documents_candidate_id ON hr_documents(candidate_id);
CREATE INDEX IF NOT EXISTS ix_hr_documents_verification_id ON hr_documents(verification_id);
CREATE INDEX IF NOT EXISTS ix_hr_documents_candidate_type ON hr_documents(candidate_id, document_type);
CREATE INDEX IF NOT EXISTS ix_hr_documents_uploaded_by ON hr_documents(uploaded_by);

CREATE INDEX IF NOT EXISTS ix_hr_decisions_verification_id ON hr_decisions(verification_id);
CREATE INDEX IF NOT EXISTS ix_hr_decisions_candidate_id ON hr_decisions(candidate_id);
CREATE INDEX IF NOT EXISTS ix_hr_decisions_decided_by ON hr_decisions(decided_by);
CREATE INDEX IF NOT EXISTS ix_hr_decisions_decision ON hr_decisions(decision);

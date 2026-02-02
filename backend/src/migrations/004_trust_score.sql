-- Phase 5: Trust Score Tables
-- For storing calculated trust scores and HR overrides

-- Trust Score Override table (created first for FK reference)
CREATE TABLE IF NOT EXISTS trust_score_overrides (
    id SERIAL PRIMARY KEY,
    
    -- Link to trust score (will be added after trust_scores created)
    trust_score_id INTEGER,
    
    -- Before override
    original_score FLOAT NOT NULL,
    original_status VARCHAR(50) NOT NULL,
    original_flags JSONB DEFAULT '[]'::jsonb,
    
    -- Override decision
    overridden_status VARCHAR(50) NOT NULL,  -- APPROVED, REJECTED
    
    -- Audit info
    overridden_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    override_reason TEXT NOT NULL,
    override_category VARCHAR(50) NOT NULL,  -- FALSE_POSITIVE, EXPLAINABLE, etc.
    
    -- Supporting evidence
    supporting_documents JSONB DEFAULT '[]'::jsonb,
    notes TEXT,
    
    -- Approval chain (for scores < 50)
    requires_senior_approval BOOLEAN DEFAULT FALSE,
    senior_approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    senior_approved_at TIMESTAMP,
    senior_notes TEXT,
    
    -- Timestamps
    overridden_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trust Score table
CREATE TABLE IF NOT EXISTS trust_scores (
    id SERIAL PRIMARY KEY,
    
    -- Foreign keys
    verification_id INTEGER NOT NULL REFERENCES verifications(id) ON DELETE CASCADE UNIQUE,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    
    -- Score and status
    score FLOAT NOT NULL DEFAULT 0.0,
    status VARCHAR(50) NOT NULL,  -- VERIFIED, REVIEW_REQUIRED, HIGH_RISK, FLAGGED
    
    -- Completion
    completion_rate FLOAT NOT NULL DEFAULT 0.0,
    
    -- Component breakdown
    breakdown JSONB DEFAULT '{}'::jsonb,
    
    -- Flags and recommendations
    flags JSONB DEFAULT '[]'::jsonb,
    recommendations JSONB DEFAULT '[]'::jsonb,
    
    -- Override tracking
    is_overridden BOOLEAN DEFAULT FALSE,
    override_id INTEGER REFERENCES trust_score_overrides(id),
    
    -- Timestamps
    calculated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add FK from overrides to trust_scores
ALTER TABLE trust_score_overrides 
ADD CONSTRAINT fk_trust_score_overrides_trust_score 
FOREIGN KEY (trust_score_id) REFERENCES trust_scores(id) ON DELETE CASCADE;

-- Indexes
CREATE INDEX IF NOT EXISTS ix_trust_scores_verification_id ON trust_scores(verification_id);
CREATE INDEX IF NOT EXISTS ix_trust_scores_candidate_id ON trust_scores(candidate_id);
CREATE INDEX IF NOT EXISTS ix_trust_scores_candidate_status ON trust_scores(candidate_id, status);
CREATE INDEX IF NOT EXISTS ix_trust_scores_status ON trust_scores(status);
CREATE INDEX IF NOT EXISTS ix_trust_overrides_trust_score_id ON trust_score_overrides(trust_score_id);
CREATE INDEX IF NOT EXISTS ix_trust_overrides_by_user ON trust_score_overrides(overridden_by);

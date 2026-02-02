import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { candidatesApi, Candidate } from '../api/candidates';
import { documentsApi, Document } from '../api/documents';
import { trustScoreApi, TrustScore } from '../api/trustScore';
import { DocumentUpload } from '../components/DocumentUpload';
import { TrustScoreGauge } from '../components/TrustScoreGauge';
import './CandidateDetailPage.css';

export const CandidateDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [candidate, setCandidate] = useState<Candidate | null>(null);
    const [documents, setDocuments] = useState<Document[]>([]);
    const [trustScore, setTrustScore] = useState<TrustScore | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const loadCandidateData = async () => {
        if (!id) return;

        try {
            setLoading(true);
            const [candidateData, documentsData] = await Promise.all([
                candidatesApi.get(id),
                documentsApi.list(id),
            ]);

            setCandidate(candidateData);
            setDocuments(documentsData);

            // Load trust score
            try {
                const scoreData = await trustScoreApi.get(id);
                setTrustScore(scoreData);
            } catch (err) {
                // Trust score might not exist yet
                console.log('No trust score available yet');
            }

            setError('');
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to load candidate data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadCandidateData();
    }, [id]);

    const handleUploadSuccess = () => {
        loadCandidateData(); // Reload documents
    };

    if (loading) {
        return (
            <div className="candidate-detail-container">
                <div className="loading-state">Loading candidate data...</div>
            </div>
        );
    }

    if (error || !candidate) {
        return (
            <div className="candidate-detail-container">
                <div className="error-state">
                    <p>{error || 'Candidate not found'}</p>
                    <button onClick={() => navigate('/dashboard')} className="back-button">
                        Back to Dashboard
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="candidate-detail-container">
            <div className="candidate-detail-header">
                <button onClick={() => navigate('/dashboard')} className="back-link">
                    ← Back to Dashboard
                </button>
            </div>

            <div className="candidate-detail-content">
                {/* Candidate Info Card */}
                <div className="info-card">
                    <h2>{candidate.name}</h2>
                    <div className="info-grid">
                        <div className="info-item">
                            <label>Email</label>
                            <p>{candidate.email}</p>
                        </div>
                        <div className="info-item">
                            <label>Phone</label>
                            <p>{candidate.phone || 'N/A'}</p>
                        </div>
                        <div className="info-item">
                            <label>Position</label>
                            <p>{candidate.position}</p>
                        </div>
                        <div className="info-item">
                            <label>Added</label>
                            <p>{new Date(candidate.createdAt).toLocaleDateString()}</p>
                        </div>
                    </div>
                </div>

                {/* Trust Score Section */}
                <div className="trust-score-section">
                    <h3>Trust Score</h3>
                    {trustScore ? (
                        <div className="trust-score-content">
                            <TrustScoreGauge score={trustScore.score} />

                            <div className="score-breakdown">
                                <h4>Score Breakdown</h4>
                                <div className="breakdown-grid">
                                    <div className="breakdown-item">
                                        <label>Aadhaar Match</label>
                                        <div className="breakdown-bar">
                                            <div
                                                className="breakdown-fill"
                                                style={{ width: `${trustScore.breakdown.aadhaarMatch}%` }}
                                            ></div>
                                        </div>
                                        <span>{trustScore.breakdown.aadhaarMatch}%</span>
                                    </div>

                                    <div className="breakdown-item">
                                        <label>Face Match</label>
                                        <div className="breakdown-bar">
                                            <div
                                                className="breakdown-fill"
                                                style={{ width: `${trustScore.breakdown.faceMatch}%` }}
                                            ></div>
                                        </div>
                                        <span>{trustScore.breakdown.faceMatch}%</span>
                                    </div>

                                    <div className="breakdown-item">
                                        <label>Document Authenticity</label>
                                        <div className="breakdown-bar">
                                            <div
                                                className="breakdown-fill"
                                                style={{ width: `${trustScore.breakdown.documentAuth}%` }}
                                            ></div>
                                        </div>
                                        <span>{trustScore.breakdown.documentAuth}%</span>
                                    </div>

                                    <div className="breakdown-item">
                                        <label>Address Risk</label>
                                        <div className="breakdown-bar">
                                            <div
                                                className="breakdown-fill"
                                                style={{ width: `${trustScore.breakdown.addressRisk}%` }}
                                            ></div>
                                        </div>
                                        <span>{trustScore.breakdown.addressRisk}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="no-trust-score">
                            <p>Trust Score not calculated yet</p>
                            <p className="hint">Upload documents to generate Trust Score</p>
                        </div>
                    )}
                </div>

                {/* Document Upload Section */}
                <div className="documents-section">
                    <h3>Documents</h3>
                    <DocumentUpload
                        candidateId={candidate.id}
                        onUploadSuccess={handleUploadSuccess}
                    />

                    {documents.length > 0 && (
                        <div className="documents-list">
                            <h4>Uploaded Documents</h4>
                            {documents.map((doc) => (
                                <div key={doc.id} className="document-item">
                                    <div className="document-icon">📄</div>
                                    <div className="document-info">
                                        <p className="document-name">{doc.fileName}</p>
                                        <p className="document-meta">
                                            {doc.docType} • {(doc.fileSize / 1024).toFixed(1)} KB •{' '}
                                            {new Date(doc.uploadedAt).toLocaleString()}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

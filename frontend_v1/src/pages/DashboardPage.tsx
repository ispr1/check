import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { candidatesApi, Candidate } from '../api/candidates';
import { AddCandidateModal } from '../components/AddCandidateModal';
import './DashboardPage.css';

export const DashboardPage: React.FC = () => {
    const [candidates, setCandidates] = useState<Candidate[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showAddModal, setShowAddModal] = useState(false);

    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const loadCandidates = async () => {
        try {
            setLoading(true);
            const data = await candidatesApi.list();
            setCandidates(data);
            setError('');
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to load candidates');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadCandidates();
    }, []);

    const handleCandidateClick = (id: string) => {
        navigate(`/candidates/${id}`);
    };

    const handleAddCandidate = () => {
        setShowAddModal(false);
        loadCandidates(); // Reload list
    };

    const getTrustScoreColor = (score?: number) => {
        if (!score) return '#94a3b8';
        if (score >= 75) return '#22c55e';
        if (score >= 50) return '#f59e0b';
        return '#ef4444';
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-left">
                    <h1>CHECK-360</h1>
                    <p className="company-name">{user?.company.name}</p>
                </div>
                <div className="header-right">
                    <span className="user-name">{user?.name}</span>
                    <button onClick={logout} className="logout-button">
                        Logout
                    </button>
                </div>
            </header>

            <main className="dashboard-main">
                <div className="dashboard-toolbar">
                    <h2>Candidates</h2>
                    <button
                        onClick={() => setShowAddModal(true)}
                        className="add-button"
                    >
                        + Add Candidate
                    </button>
                </div>

                {error && (
                    <div className="error-banner">{error}</div>
                )}

                {loading ? (
                    <div className="loading-state">Loading candidates...</div>
                ) : candidates.length === 0 ? (
                    <div className="empty-state">
                        <h3>No candidates yet</h3>
                        <p>Click "Add Candidate" to get started</p>
                    </div>
                ) : (
                    <div className="candidates-table-container">
                        <table className="candidates-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Position</th>
                                    <th>Documents</th>
                                    <th>Trust Score</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {candidates.map((candidate) => (
                                    <tr
                                        key={candidate.id}
                                        onClick={() => handleCandidateClick(candidate.id)}
                                        className="candidate-row"
                                    >
                                        <td>
                                            <strong>{candidate.name}</strong>
                                        </td>
                                        <td>{candidate.email}</td>
                                        <td>{candidate.position}</td>
                                        <td>
                                            <span className="document-badge">
                                                {candidate.documentCount || 0}
                                            </span>
                                        </td>
                                        <td>
                                            {candidate.trustScore ? (
                                                <span
                                                    className="trust-score-badge"
                                                    style={{
                                                        backgroundColor: getTrustScoreColor(candidate.trustScore.score),
                                                    }}
                                                >
                                                    {candidate.trustScore.score}/100
                                                </span>
                                            ) : (
                                                <span className="trust-score-badge pending">
                                                    Pending
                                                </span>
                                            )}
                                        </td>
                                        <td>
                                            <span className={`status-badge ${candidate.trustScore?.status || 'pending'}`}>
                                                {candidate.trustScore?.status || 'Pending'}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </main>

            {showAddModal && (
                <AddCandidateModal
                    onClose={() => setShowAddModal(false)}
                    onSuccess={handleAddCandidate}
                />
            )}
        </div>
    );
};

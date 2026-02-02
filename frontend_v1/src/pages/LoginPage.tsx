import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './LoginPage.css';

export const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await login({ email, password });
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.error || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h1>CHECK-360</h1>
                    <p className="login-subtitle">Employee Trust & Risk Intelligence</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            placeholder="hr@company.com"
                            disabled={loading}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder="••••••••"
                            disabled={loading}
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" className="login-button" disabled={loading}>
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>
                </form>

                <div className="demo-credentials">
                    <p><strong>Demo Credentials:</strong></p>
                    <p>Email: hr@techcorp.com</p>
                    <p>Password: password123</p>
                </div>
            </div>
        </div>
    );
};

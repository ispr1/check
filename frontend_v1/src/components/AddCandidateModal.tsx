import React, { useState } from 'react';
import { candidatesApi, CreateCandidateRequest } from '../api/candidates';
import './AddCandidateModal.css';

interface AddCandidateModalProps {
    onClose: () => void;
    onSuccess: () => void;
}

export const AddCandidateModal: React.FC<AddCandidateModalProps> = ({
    onClose,
    onSuccess,
}) => {
    const [formData, setFormData] = useState<CreateCandidateRequest>({
        name: '',
        email: '',
        phone: '',
        position: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await candidatesApi.create(formData);
            onSuccess();
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to create candidate');
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>Add New Candidate</h2>
                    <button onClick={onClose} className="modal-close">&times;</button>
                </div>

                <form onSubmit={handleSubmit} className="modal-form">
                    <div className="form-group">
                        <label htmlFor="name">Full Name *</label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            value={formData.name}
                            onChange={handleChange}
                            required
                            placeholder="John Doe"
                            disabled={loading}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email *</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            placeholder="john.doe@example.com"
                            disabled={loading}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="phone">Phone</label>
                        <input
                            id="phone"
                            name="phone"
                            type="tel"
                            value={formData.phone}
                            onChange={handleChange}
                            placeholder="+91 98765 43210"
                            disabled={loading}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="position">Position *</label>
                        <input
                            id="position"
                            name="position"
                            type="text"
                            value={formData.position}
                            onChange={handleChange}
                            required
                            placeholder="Software Engineer"
                            disabled={loading}
                        />
                    </div>

                    {error && <div className="form-error">{error}</div>}

                    <div className="modal-actions">
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn-cancel"
                            disabled={loading}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="btn-submit"
                            disabled={loading}
                        >
                            {loading ? 'Creating...' : 'Add Candidate'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

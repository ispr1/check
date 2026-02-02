import React, { useState } from 'react';
import { documentsApi } from '../api/documents';
import './DocumentUpload.css';

interface DocumentUploadProps {
    candidateId: string;
    onUploadSuccess: () => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
    candidateId,
    onUploadSuccess,
}) => {
    const [file, setFile] = useState<File | null>(null);
    const [docType, setDocType] = useState('aadhaar');
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setError('');
        setUploading(true);

        try {
            await documentsApi.upload(candidateId, docType, file);
            setFile(null);
            setDocType('aadhaar');
            onUploadSuccess();
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to upload document');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="document-upload">
            <div className="upload-form">
                <div className="doc-type-selector">
                    <label htmlFor="docType">Document Type</label>
                    <select
                        id="docType"
                        value={docType}
                        onChange={(e) => setDocType(e.target.value)}
                        disabled={uploading}
                    >
                        <option value="aadhaar">Aadhaar Card</option>
                        <option value="pan">PAN Card</option>
                        <option value="passport">Passport</option>
                        <option value="photo">Photo/Selfie</option>
                        <option value="other">Other</option>
                    </select>
                </div>

                <div
                    className={`drop-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={() => document.getElementById('fileInput')?.click()}
                >
                    <input
                        id="fileInput"
                        type="file"
                        onChange={handleFileChange}
                        accept="image/*,.pdf"
                        style={{ display: 'none' }}
                        disabled={uploading}
                    />

                    {file ? (
                        <div className="file-selected">
                            <div className="file-icon">📄</div>
                            <div className="file-name">{file.name}</div>
                            <div className="file-size">{(file.size / 1024).toFixed(1)} KB</div>
                        </div>
                    ) : (
                        <div className="drop-zone-content">
                            <div className="upload-icon">📤</div>
                            <p className="drop-text">Drag and drop file here</p>
                            <p className="or-text">or</p>
                            <button type="button" className="browse-button">
                                Browse Files
                            </button>
                            <p className="file-hint">Supported: JPG, PNG, PDF (Max 10MB)</p>
                        </div>
                    )}
                </div>

                {error && <div className="upload-error">{error}</div>}

                <button
                    onClick={handleUpload}
                    disabled={!file || uploading}
                    className="upload-button"
                >
                    {uploading ? 'Uploading...' : 'Upload Document'}
                </button>
            </div>
        </div>
    );
};

import apiClient from './client';

export interface Document {
    id: string;
    candidateId: string;
    docType: string;
    fileName: string;
    filePath: string;
    fileSize: number;
    mimeType: string;
    uploadedAt: string;
}

export const documentsApi = {
    upload: async (candidateId: string, docType: string, file: File): Promise<Document> => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('candidateId', candidateId);
        formData.append('docType', docType);

        const response = await apiClient.post('/documents/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    list: async (candidateId: string): Promise<Document[]> => {
        const response = await apiClient.get(`/documents/${candidateId}`);
        return response.data;
    },

    delete: async (id: string): Promise<void> => {
        await apiClient.delete(`/documents/${id}`);
    },
};

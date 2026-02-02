import apiClient from './client';

export interface Candidate {
    id: string;
    name: string;
    email: string;
    phone?: string;
    position: string;
    createdAt: string;
    documentCount?: number;
    trustScore?: {
        score: number;
        status: string;
        calculatedAt: string;
    } | null;
}

export interface CreateCandidateRequest {
    name: string;
    email: string;
    phone?: string;
    position: string;
}

export interface UpdateCandidateRequest {
    name?: string;
    email?: string;
    phone?: string;
    position?: string;
}

export const candidatesApi = {
    list: async (): Promise<Candidate[]> => {
        const response = await apiClient.get('/candidates');
        return response.data;
    },

    get: async (id: string): Promise<Candidate> => {
        const response = await apiClient.get(`/candidates/${id}`);
        return response.data;
    },

    create: async (data: CreateCandidateRequest): Promise<Candidate> => {
        const response = await apiClient.post('/candidates', data);
        return response.data;
    },

    update: async (id: string, data: UpdateCandidateRequest): Promise<Candidate> => {
        const response = await apiClient.put(`/candidates/${id}`, data);
        return response.data;
    },

    delete: async (id: string): Promise<void> => {
        await apiClient.delete(`/candidates/${id}`);
    },
};

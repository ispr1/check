import apiClient from './client';

export interface TrustScore {
    id: string;
    candidateId: string;
    score: number;
    breakdown: {
        aadhaarMatch: number;
        faceMatch: number;
        documentAuth: number;
        addressRisk: number;
    };
    status: string;
    calculatedAt: string;
}

export const trustScoreApi = {
    get: async (candidateId: string): Promise<TrustScore> => {
        const response = await apiClient.get(`/trust-score/${candidateId}`);
        return response.data;
    },

    recalculate: async (candidateId: string): Promise<{ message: string; status: string }> => {
        const response = await apiClient.post(`/trust-score/${candidateId}/recalculate`);
        return response.data;
    },
};

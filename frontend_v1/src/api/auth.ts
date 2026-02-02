import apiClient from './client';

export interface User {
    id: string;
    email: string;
    name: string;
    role: string;
    company: {
        id: string;
        name: string;
    };
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface LoginResponse {
    token: string;
    user: User;
}

export interface RegisterRequest {
    email: string;
    password: string;
    name: string;
    companyName: string;
}

export const authApi = {
    login: async (data: LoginRequest): Promise<LoginResponse> => {
        const response = await apiClient.post('/auth/login', data);
        return response.data;
    },

    register: async (data: RegisterRequest): Promise<LoginResponse> => {
        const response = await apiClient.post('/auth/register', data);
        return response.data;
    },
};

import $axios from '@/api';
import type { User } from '../types';

export const useUserRequests = () => {
    const getUser = async (): Promise<User> => {
        try {
            const response = await $axios.get<User>('/auth/me');
            return response.data;
        } catch (error) {
            console.error('Failed to fetch user:', error);
            throw error;
        }
    };

    return {
        getUser,
    };
};


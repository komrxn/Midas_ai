import { defineStore } from 'pinia';
import api from '../api';
import router from '../router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('admin_token') || null,
        admin: JSON.parse(localStorage.getItem('admin_user')) || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
    },
    actions: {
        async login(username, password) {
            try {
                const response = await api.post('/auth/login', { username, password });
                this.token = response.data.access_token;
                localStorage.setItem('admin_token', this.token);

                // Fetch me
                const meParams = await api.get('/auth/me');
                this.admin = meParams.data;
                localStorage.setItem('admin_user', JSON.stringify(this.admin));

                router.push('/dashboard');
                return true;
            } catch (error) {
                console.error('Login failed', error);
                throw error;
            }
        },
        logout() {
            this.token = null;
            this.admin = null;
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_user');
            router.push('/login');
        },
    },
});

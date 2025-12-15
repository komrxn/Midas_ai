import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { User } from '@/composables/User/types';
import { useUserRequests } from '@/composables/User/requests';

export const useUserStore = defineStore('user', () => {
    const user = ref<User | null>(null);
    const loading = ref<boolean>(false);
    const isLoaded = ref<boolean>(false);
    const { getUser: fetchUser } = useUserRequests();

    const loadUser = async (force = false) => {
        // Если данные уже загружены и не требуется принудительная загрузка, не загружаем заново
        if (!force && isLoaded.value && user.value) {
            return;
        }
        
        if (loading.value) return;

        try {
            loading.value = true;
            user.value = await fetchUser();
            isLoaded.value = true;
        } catch (error) {
            console.error('Failed to load user:', error);
            isLoaded.value = false;
            throw error;
        } finally {
            loading.value = false;
        }
    };

    const clearUser = () => {
        user.value = null;
        isLoaded.value = false;
    };

    return {
        user,
        loading,
        isLoaded,
        loadUser,
        clearUser,
    };
});


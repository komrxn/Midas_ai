import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { BalanceResponse } from '@/composables/Analytics/types';
import { useAnalyticsRequests } from '@/composables/Analytics/requests';

export const useBalanceStore = defineStore('balance', () => {
    const balance = ref<BalanceResponse | null>(null);
    const loading = ref<boolean>(false);
    const isLoaded = ref<boolean>(false);
    const { getBalance: fetchBalance } = useAnalyticsRequests();

    const loadBalance = async (params: { period: string }, force = false) => {
        // Если данные уже загружены и не требуется принудительная загрузка, не загружаем заново
        if (!force && isLoaded.value && balance.value) {
            return;
        }
        
        if (loading.value) return;

        try {
            loading.value = true;
            balance.value = await fetchBalance(params);
            isLoaded.value = true;
        } catch (error) {
            console.error('Failed to load balance:', error);
            isLoaded.value = false;
            throw error;
        } finally {
            loading.value = false;
        }
    };

    const clearBalance = () => {
        balance.value = null;
        isLoaded.value = false;
    };

    return {
        balance,
        loading,
        isLoaded,
        loadBalance,
        clearBalance,
    };
});


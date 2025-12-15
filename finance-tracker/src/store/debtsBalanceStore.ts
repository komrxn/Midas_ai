import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { DebtBalance } from '@/composables/Debts/types';
import { useDebtsRequests } from '@/composables/Debts/requests';

export const useDebtsBalanceStore = defineStore('debtsBalance', () => {
    const balance = ref<DebtBalance | null>(null);
    const loading = ref<boolean>(false);
    const isLoaded = ref<boolean>(false);
    const { getDebtBalance: fetchDebtBalance } = useDebtsRequests();

    const loadDebtBalance = async (force = false) => {
        // Если данные уже загружены и не требуется принудительная загрузка, не загружаем заново
        if (!force && isLoaded.value && balance.value) {
            return;
        }
        
        if (loading.value) return;

        try {
            loading.value = true;
            balance.value = await fetchDebtBalance();
            isLoaded.value = true;
        } catch (error) {
            console.error('Failed to load debt balance:', error);
            isLoaded.value = false;
            throw error;
        } finally {
            loading.value = false;
        }
    };

    const clearDebtBalance = () => {
        balance.value = null;
        isLoaded.value = false;
    };

    return {
        balance,
        loading,
        isLoaded,
        loadDebtBalance,
        clearDebtBalance,
    };
});


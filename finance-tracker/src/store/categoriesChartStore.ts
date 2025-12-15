import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { CategoryBreakdownResponse } from '@/composables/Analytics/types';
import { useAnalyticsRequests } from '@/composables/Analytics/requests';

export const useCategoriesChartStore = defineStore('categoriesChart', () => {
    const categoryBreakdown = ref<CategoryBreakdownResponse | null>(null);
    const loading = ref<boolean>(false);
    const isLoaded = ref<boolean>(false);
    const { getCategories: fetchCategories } = useAnalyticsRequests();

    const loadCategories = async (params: { period: string; type: string }, force = false) => {
        // Если данные уже загружены и не требуется принудительная загрузка, не загружаем заново
        if (!force && isLoaded.value && categoryBreakdown.value) {
            return;
        }
        
        if (loading.value) return;

        try {
            loading.value = true;
            categoryBreakdown.value = await fetchCategories(params);
            isLoaded.value = true;
        } catch (error) {
            console.error('Failed to load categories:', error);
            isLoaded.value = false;
            throw error;
        } finally {
            loading.value = false;
        }
    };

    const clearCategories = () => {
        categoryBreakdown.value = null;
        isLoaded.value = false;
    };

    return {
        categoryBreakdown,
        loading,
        isLoaded,
        loadCategories,
        clearCategories,
    };
});


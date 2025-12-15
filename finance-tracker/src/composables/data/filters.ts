import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { CategoryType } from '@/composables/Categories/types';

export interface CategoryTypeFilterOption {
    label: string;
    value: CategoryType | 'all';
}

export const useCategoryTypeFilterOptions = () => {
    const { t } = useI18n();
    return computed<CategoryTypeFilterOption[]>(() => [
        { label: t('filters.all'), value: 'all' },
        { label: t('transactions.income'), value: CategoryType.INCOME },
        { label: t('transactions.expense'), value: CategoryType.EXPENSE },
    ]);
};

// Для обратной совместимости
export const CATEGORY_TYPE_FILTER_OPTIONS: CategoryTypeFilterOption[] = [
    { label: 'Все', value: 'all' },
    { label: 'Доходы', value: CategoryType.INCOME },
    { label: 'Расходы', value: CategoryType.EXPENSE },
];

import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { DebtType, DebtStatus } from '../types';

export interface DebtTypeFilterOption {
    label: string;
    value: DebtType | 'all';
}

export interface DebtStatusFilterOption {
    label: string;
    value: DebtStatus | 'all';
}

export const useDebtTypeFilterOptions = () => {
    const { t } = useI18n();
    return computed<DebtTypeFilterOption[]>(() => [
        { label: t('filters.all'), value: 'all' },
        { label: t('debts.iOwe'), value: DebtType.I_OWE },
        { label: t('debts.oweMe'), value: DebtType.OWE_ME },
    ]);
};

export const useDebtStatusFilterOptions = () => {
    const { t } = useI18n();
    return computed<DebtStatusFilterOption[]>(() => [
        { label: t('filters.all'), value: 'all' },
        // { label: t('debts.open'), value: DebtStatus.OPEN },
        { label: t('debts.overdue'), value: DebtStatus.OVERDUE },
        { label: t('debts.paid'), value: DebtStatus.PAID },
    ]);
};

// Для обратной совместимости
export const DEBT_TYPE_FILTER_OPTIONS: DebtTypeFilterOption[] = [
    { label: 'Все', value: 'all' },
    { label: 'Я занял(а)', value: DebtType.I_OWE },
    { label: 'Мне должны', value: DebtType.OWE_ME },
];

export const DEBT_STATUS_FILTER_OPTIONS: DebtStatusFilterOption[] = [
    { label: 'Все', value: 'all' },
    // { label: 'Открытые', value: DebtStatus.OPEN },
    { label: 'Просрочено', value: DebtStatus.OVERDUE },
    { label: 'Погашено', value: DebtStatus.PAID },
];

import { useLocalStorage } from '@vueuse/core';

export type DebtType = 'borrowed' | 'lent'; // Я занял / Мне должны
export type DebtStatus = 'open' | 'overdue' | 'paid'; // Открытые / Просрочено / Погашено

export interface DebtFormData {
    type: DebtType;
    personName: string;
    amount: number;
    description?: string;
    dueDate?: string;
    status: DebtStatus;
}

export interface Debt {
    id: string;
    type: DebtType;
    personName: string;
    amount: number;
    description?: string;
    dueDate?: string;
    status: DebtStatus;
    createdAt: string;
    paidAt?: string;
}

const STORAGE_KEY = 'debts';

export const useDebts = () => {
    const debts = useLocalStorage<Debt[]>(STORAGE_KEY, []);

    const addDebt = (formData: DebtFormData) => {
        const newDebt: Debt = {
            ...formData,
            id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            createdAt: new Date().toISOString(),
        };

        debts.value = [...debts.value, newDebt];
        return newDebt;
    };

    const removeDebt = (id: string) => {
        debts.value = debts.value.filter(debt => debt.id !== id);
        return true;
    };

    const updateDebt = (id: string, formData: DebtFormData) => {
        const index = debts.value.findIndex(debt => debt.id === id);
        if (index !== -1) {
            debts.value[index] = {
                ...debts.value[index],
                ...formData,
            };
            return true;
        }
        return false;
    };

    const markAsPaid = (id: string) => {
        const index = debts.value.findIndex(debt => debt.id === id);
        if (index !== -1) {
            debts.value[index] = {
                ...debts.value[index],
                status: 'paid',
                paidAt: new Date().toISOString(),
            };
            return true;
        }
        return false;
    };

    const getDebtsByType = (type: DebtType | 'all') => {
        if (type === 'all') {
            return debts.value;
        }
        return debts.value.filter(debt => debt.type === type);
    };

    const getDebtsByStatus = (status: DebtStatus | 'all') => {
        if (status === 'all') {
            return debts.value;
        }
        return debts.value.filter(debt => debt.status === status);
    };

    const getFilteredDebts = (type: DebtType | 'all', status: DebtStatus | 'all') => {
        let filtered = debts.value;

        if (type !== 'all') {
            filtered = filtered.filter(debt => debt.type === type);
        }

        if (status !== 'all') {
            filtered = filtered.filter(debt => debt.status === status);
        }

        return filtered;
    };

    const getTotalBorrowed = () => {
        return debts.value
            .filter(debt => debt.type === 'borrowed' && debt.status !== 'paid')
            .reduce((sum, debt) => sum + debt.amount, 0);
    };

    const getTotalLent = () => {
        return debts.value
            .filter(debt => debt.type === 'lent' && debt.status !== 'paid')
            .reduce((sum, debt) => sum + debt.amount, 0);
    };

    return {
        debts,
        addDebt,
        removeDebt,
        updateDebt,
        markAsPaid,
        getDebtsByType,
        getDebtsByStatus,
        getFilteredDebts,
        getTotalBorrowed,
        getTotalLent,
    };
};



import $axios from "@/api";
import { DebtCreateData, DebtUpdateData } from "../types";
import { setDebt } from "../models";
import type { Debt, DebtBalance } from "../types";

export const useDebtsRequests = () => {
    const getDebts = async (): Promise<Debt[]> => {
        try {
            const response = await $axios.get<Debt[]>('/debts');
            return response.data.map(item => setDebt(item));
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const getDebt = async (id: string): Promise<Debt> => {
        try {
            const response = await $axios.get<Debt>(`/debts/${id}`);
            return setDebt(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const getDebtBalance = async (): Promise<DebtBalance> => {
        try {
            const response = await $axios.get<DebtBalance>('/debts/balance');
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const addDebt = async (debt: DebtCreateData): Promise<Debt> => {
        try {
            const response = await $axios.post<Debt>('/debts', debt);
            return setDebt(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const updateDebt = async (id: string, debt: DebtUpdateData): Promise<Debt> => {
        try {
            const response = await $axios.put<Debt>(`/debts/${id}`, debt);
            return setDebt(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const deleteDebt = async (id: string): Promise<void> => {
        try {
            await $axios.delete(`/debts/${id}`);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    const markDebtAsPaid = async (id: string): Promise<Debt> => {
        try {
            const response = await $axios.post<Debt>(`/debts/${id}/mark-paid`);
            return setDebt(response.data);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    return {
        getDebts,
        getDebt,
        getDebtBalance,
        addDebt,
        updateDebt,
        deleteDebt,
        markDebtAsPaid,
    }
}

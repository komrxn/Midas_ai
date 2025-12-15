import $axios from '@/api';
import type {
    BalanceResponse,
    CategoryBreakdownResponse,
    TrendsResponse,
    SummaryResponse,
    GetBalanceParams,
    GetCategoriesParams,
    GetTrendsParams,
    GetSummaryParams,
} from '../types';

export const useAnalyticsRequests = () => {
    const getBalance = async (params: GetBalanceParams): Promise<BalanceResponse> => {
        try {
            const response = await $axios.get<BalanceResponse>('/analytics/balance', { params });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch balance:', error);
            throw error;
        }
    };

    const getCategories = async (params: GetCategoriesParams): Promise<CategoryBreakdownResponse> => {
        try {
            const response = await $axios.get<CategoryBreakdownResponse>('/analytics/categories', { params });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch categories:', error);
            throw error;
        }
    };

    const getTrends = async (params: GetTrendsParams): Promise<TrendsResponse> => {
        try {
            const response = await $axios.get<TrendsResponse>('/analytics/trends', { params });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch trends:', error);
            throw error;
        }
    };

    const getSummary = async (params: GetSummaryParams): Promise<SummaryResponse> => {
        try {
            const response = await $axios.get<SummaryResponse>('/analytics/summary', { params });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch summary:', error);
            throw error;
        }
    };

    return {
        getBalance,
        getCategories,
        getTrends,
        getSummary,
    };
};

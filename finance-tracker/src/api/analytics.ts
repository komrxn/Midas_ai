import $axios from '@/api/index';

export interface AnalyticsBalanceResponse {
    balance: string;
    total_income: string;
    total_expense: string;
    income_change: number;
    expense_change: number;
    balance_change: number;
}

export interface AnalyticsCategory {
    category_name: string;
    amount: string;
    percentage: string;
    color?: string;
}

export interface AnalyticsCategoriesResponse {
    categories: AnalyticsCategory[];
}

export interface AnalyticsTrendPoint {
    date: string;
    income: string;
    expense: string;
}

export interface AnalyticsTrendsResponse {
    data: AnalyticsTrendPoint[];
}

export const analyticsApi = {
    async getBalance(period: string = 'month'): Promise<AnalyticsBalanceResponse> {
        const { data } = await $axios.get<AnalyticsBalanceResponse>(`/analytics/balance?period=${period}`);
        return data;
    },

    async getCategories(period: string = 'month', type: 'income' | 'expense' = 'expense'): Promise<AnalyticsCategoriesResponse> {
        const { data } = await $axios.get<AnalyticsCategoriesResponse>(`/analytics/categories?period=${period}&type=${type}`);
        return data;
    },

    async getTrends(period: string = 'month', granularity: string = 'day'): Promise<AnalyticsTrendsResponse> {
        const { data } = await $axios.get<AnalyticsTrendsResponse>(`/analytics/trends?period=${period}&granularity=${granularity}`);
        return data;
    }
};

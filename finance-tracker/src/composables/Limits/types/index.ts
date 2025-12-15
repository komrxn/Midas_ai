export interface Limit {
    category_id: string;
    amount: string;
    period_start: string;
    period_end: string;
    id: string;
    user_id: string;
    spent: string;
    remaining: string;
    percentage: number;
    is_exceeded: boolean;
    category_name: string;
    created_at: string;
    updated_at: string;
}

export interface LimitCreateData {
    category_id: string;
    amount: number;
    period_start: string;
    period_end: string;
}

export interface LimitUpdateData {
    amount: number;
    period_start: string;
    period_end: string;
}

export interface GetLimitsParams {
    period_start?: string;
    period_end?: string;
    category_id?: string;
}

export interface LimitFormData {
    category: string | undefined;
    budget: number;
}

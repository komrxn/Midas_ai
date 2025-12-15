import type { Limit } from "../types";

export type { Limit };

export const setLimits = (limits: Partial<Limit>): Limit => {

    return {
        category_id: limits.category_id || '',
        amount: limits.amount || '',
        period_start: limits.period_start || '',
        period_end: limits.period_end || '',
        id: limits.id || '',
        user_id: limits.user_id || '',
        spent: limits.spent || '',
        remaining: limits.remaining || '',
        percentage: limits.percentage || 0,
        is_exceeded: limits.is_exceeded || false,
        category_name: limits.category_name || '',
        created_at: limits.created_at || '',
        updated_at: limits.updated_at || '',
    }
}
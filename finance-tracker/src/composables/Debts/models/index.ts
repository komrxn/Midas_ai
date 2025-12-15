import type { Debt } from "../types";

export type { Debt };

export const setDebt = (debt: Partial<Debt>): Debt => {
    return {
        id: debt.id || '',
        type: debt.type || 'i_owe' as any,
        person_name: debt.person_name || '',
        amount: debt.amount || '0',
        currency: debt.currency || 'uzs',
        description: debt.description || '',
        due_date: debt.due_date || '',
        user_id: debt.user_id || '',
        status: debt.status || 'open' as any,
        settled_at: debt.settled_at || null,
        created_at: debt.created_at || '',
        updated_at: debt.updated_at || '',
    }
}

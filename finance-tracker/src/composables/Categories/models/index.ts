import { CategoryType, type Category } from "../types";

export type { Category };

export const setCategory = (category: Partial<Category>): Category => {
    return {
        id: category.id || '',
        name: category.name || '',
        slug: category.slug || '',
        type: category.type || CategoryType.EXPENSE,
        icon: category.icon || '',
        color: category.color || '',
        user_id: category.user_id || null,
        is_default: category.is_default || false,
        created_at: category.created_at || '',
    }
}
